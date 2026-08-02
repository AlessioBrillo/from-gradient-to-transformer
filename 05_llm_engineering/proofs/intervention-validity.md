---
tags: [type/proof, phase/5, research/experiment]
created: 2026-08-01
---

# Proof to myself: An Intervention Is Only as Valid as Its Site, Its Counterfactual, and Its Metric

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate

That I understand, well enough to catch my own mistakes, the three things that make a
causal claim in mechanistic interpretability actually true rather than merely plausible:

1. **Site** — an intervention has to land on the tensor I think it lands on, at the point
   in the forward pass I think it lands, and it has to survive whatever the model does
   with that tensor afterwards (residual skips, normalization).
2. **Counterfactual** — "corrupted" has to mean something specific and known, or there is
   nothing for "recovery" to be measured against.
3. **Metric** — the number I read off the patched run has to isolate the thing I claim to
   be measuring, not something correlated with it.

I know these matter because I violated all three in [[04_nlp_and_transformers/notes/activation-patching]]'s
sibling code, `src/experiments/exp4_circuit_patching.py`, and shipped the wrong numbers
into `portfolio/RESULTS.md` until a 2026-08-01 validity pass caught it. This note is the
reconstruction of *why* each bug was a bug, not just the fix.

## What I produced from memory

### 1. Site: patching has to reach the residual stream, not a normalized copy of it

```python
import torch
from src.models.decoder_only_transformer import DecoderOnlyTransformer

model = DecoderOnlyTransformer(vocab_size=32, d_model=32, n_layers=2, n_heads=2, max_seq_len=16)
model.eval()
x = torch.randint(0, 32, (2, 10))

with torch.no_grad():
    _, cache = model(x, return_cache=True)

# TransformerBlock.forward does, in order:
#   x = x + attn_out          <- this sum IS resid_mid
#   h = ln_mlp(x)              <- normalized COPY, not resid_mid itself
#   mlp_out = mlp(h)
#   x = x + mlp_out            <- reuses the block's own `x`, i.e. resid_mid,
#                                  NOT whatever `h` a hook may have mutated

# WRONG (what I originally wrote): a forward_pre_hook on `block.mlp` that
# mutates its input tensor. That input IS `h = ln_mlp(resid_mid)` — normalized,
# and a dead end: the residual skip two lines later reads the block's own `x`
# variable, never the hook's mutated argument. This patches nothing that
# survives past the MLP branch.

# RIGHT: hook `block.attn` itself. Attention.forward returns (attn_out, kv)
# where attn_out is already POST-W_O — exactly the tensor added to resid_pre
# to produce resid_mid. Solve for the attn_out that lands resid_mid on a
# target value:
layer = 0
resid_pre = cache[f"blocks.{layer}.resid_pre"]       # input to this block's attn
target_resid_mid = cache[f"blocks.{layer}.resid_mid"]  # pretend this came from a corrupted run

def hook(module, inp, out):
    attn_out, kv = out
    attn_out = attn_out.clone()
    attn_out[:, 3:4, :] = target_resid_mid[:, 3:4, :] - resid_pre[:, 3:4, :]
    return (attn_out, kv)

h = model.blocks[layer].attn.register_forward_hook(hook)
with torch.no_grad():
    _, patched_cache = model(x, return_cache=True)
h.remove()

# resid_mid at position 3 must now equal the target exactly.
assert torch.allclose(
    patched_cache[f"blocks.{layer}.resid_mid"][:, 3, :],
    target_resid_mid[:, 3, :],
    atol=1e-5,
)
print("Site check passed: patched resid_mid lands exactly where intended.")
```

**Why this is the right falsification test, not just a demonstration:** if I patch a run
with *its own* clean values as the "corrupted" source, the logit diff must not move *at
all* — not "move a little," exactly zero, because nothing actually changed. That is
`tests/test_exp4_circuit_patching.py::TestActivationPatching::test_self_patching_is_a_no_op`.
The old MLP-pre-hook version would have passed a weaker test ("patching changes
*something*") because it did perturb the MLP branch's output — just not resid_mid. Only
the self-patch-is-a-no-op test would have caught it, because a real no-op requires the
*entire* residual stream to be untouched, not just one branch of it.

### 2. Counterfactual: "corrupted" needs a known, correct answer

The induction task (`make_repeated_token_data`) generates `[prefix, prefix, ...]` where
the correct next token at every position — including the last — is deterministic: what
followed the same relative position in the previous repetition. That means **the val
labels `y` already are a legitimate answer/counterfactual pair between any two different
batches**, no extra corruption logic needed.

The bug I made: I built "corrupted" by permuting each clean sequence's own positions with
`torch.randperm`. That destroys the repeat structure — the permuted sequence has no
well-defined correct next token at all, so "the answer under the corrupted run" was not a
real, checkable thing. I was computing a `recovery` score against an undefined target.

The fix: draw two **disjoint, unpermuted** batches from the same generator. Both are
valid induction sequences with real labels; `clean_answers = y_clean[:, -1]`,
`counterfactual = y_corrupted[:, -1]`.

### 3. Metric: `top1 − top2` measures confidence, not correctness

```python
# WRONG: measures how peaked the output distribution is, regardless of
# whether the peak is even the right answer.
def logit_diff_wrong(logits):
    top_two = logits[:, -1, :].topk(2, dim=-1)
    return top_two.values[:, 0] - top_two.values[:, 1]

# A model that is very confident about the WRONG token scores just as high
# on this metric as a model that is very confident about the RIGHT token.
# "Recovery" computed against this metric tells me nothing about whether the
# circuit reconstructed the correct behavior — only whether it reconstructed
# *some* confident behavior.

# RIGHT: read the logit at the known answer token vs. the known
# counterfactual token — both are defined quantities tied to the task, not
# just "whatever the model currently prefers."
def logit_diff_right(logits, answer, counterfactual, idx):
    pos_logits = logits[:, -1, :]
    return pos_logits[idx, answer] - pos_logits[idx, counterfactual]
```

This is the IOI-paper convention (Wang et al., 2023) and it is the whole reason
`clean_answers`/`corrupted_answers` need to exist as real, checkable labels — the metric
is meaningless without them.

### 4. The same failure mode, twice more, in code I wrote for the *other* rungs

- **exp1's `causal_ablation`** hooked `block.W_O`'s *output* — already mixed across every
  head by the W_O projection — and zeroed an `n_heads`-way slice of it. That zeroes an
  arbitrary residual-stream subspace, not a head. Fix: a `head_mask` applied to
  `attn_probs @ V` *before* `W_O`, matching what I'd already gotten right in exp4's head
  ablation. Falsified with: ablate every head in every block; the result must equal the
  model's pure no-attention baseline (embed + pos_embed → ln_final → unembed) *exactly*,
  because a fully-masked block should contribute literally nothing to the residual stream.
- **`compute_attention_entropy`'s `diag1_mass`** aggregated per-head induction signal with
  `.sum()` across heads instead of `.max()`. The plotted training curve was on a
  `[0, n_heads]` scale, while `analyze_induction_heads`' detection threshold (0.3) is
  per-head — comparing a sum of several small numbers against a threshold meant for one
  number. That is why a curve that looked like it was approaching 1.0 coexisted with zero
  heads actually crossing 0.3: they were never the same unit.

## Limitations — what this note does *not* prove

- I have not re-verified the standard-scale (non `--quick`) numbers in
  `portfolio/RESULTS.md` under the fixed code; only quick-mode re-runs are confirmed
  post-fix as of this note's creation date.
- Path patching (`run_path_patching_to_logits`) isolates one head's *direct* effect on
  the logits by decomposing `attn_out` through `W_O`'s per-head column blocks. I have not
  independently cross-checked this decomposition against a from-scratch second
  implementation — only against the self-patch-is-zero falsification test, which would
  catch a broken hook but not necessarily a subtly wrong decomposition.
- The superposition (Rung 3) untied→tied weights fix did **not** change the observed
  flat/near-zero feature recovery (still 0.100 at sparsity=0.01, essentially identical to
  the untied version's 0.100). My hypothesis that untied weights explained the
  discrepancy is *not supported* by this one data point — the real root cause of Rung 3's
  non-reproduction is still open. Tying the weights is still the architecturally correct
  choice (matches Elhage et al.), but it should not be reported as "the fix."
- I have not implemented the multi-seed harness the vault's own conventions claim exists
  (`00_meta/04_conventions.md`). Every number in this note and in `RESULTS.md` is
  single-seed until that's built.

## Links
- [[04_nlp_and_transformers/notes/activation-patching]]
- [[04_nlp_and_transformers/notes/path-patching]]
- [[portfolio/RESULTS]]
- Code: `src/experiments/exp4_circuit_patching.py`, `src/experiments/exp1_induction_heads.py`
- Zhang & Nanda, *Towards Best Practices of Activation Patching*, ICLR 2024
- Wang et al., *Interpretability in the Wild* (IOI), ICLR 2023

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
