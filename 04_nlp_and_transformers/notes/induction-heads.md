---
tags: [phase/4, note, state/review, research/experiment]
MI-core: "Induction heads are the mechanism behind in-context learning. They are the most well-understood circuit in mechanistic interpretability."
---

# Induction Heads — The Mechanism of In-Context Learning

## Definition (Olsson et al. 2022)
An **induction head** is an attention head that performs the operation:
`[A][B]...[A] → [B]`

That is, when it sees token A at a later position, it attends to the token *after* the previous occurrence of A, predicting that B will follow again.

## The Induction Head Mechanism
An induction head requires two sub-mechanisms:

1. **Prefix-matching:** A head that attends from the current token to the previous occurrence of the same token (often a previous-token head or a duplicate-token head)
2. **Copying:** A head that copies the token after the matched position

In a 2-layer model:
- Layer 1: previous-token head attends to the position just before each token
- Layer 2: induction head uses the Layer 1 output to match prefixes and copy the correct continuation

## The Characteristic Attention Pattern
An induction head's attention pattern shows a distinctive diagonal-offset:
- Strong attention from position i to position i-1 (or more generally, to the position after the previous occurrence of the current token)
- Visualized as a diagonal band in the attention pattern heatmap

## Training Dynamics
Induction heads emerge partway through training, marked by:
- A sudden drop in validation loss (the "bump" or phase change)
- An increase in attention-pattern structure (from diffuse to diagonal)
- The increase of a specific progress measure: "induction-head score" = attention mass on the diagonal+1 offset

## Verification via Ablation
To causally verify an induction head:
1. Locate heads with the characteristic diagonal attention pattern
2. Ablate that head (zero its output)
3. Measure the drop in performance on repeated-token sequences
4. If performance drops significantly, the head is causally important

## Why This Is the Most Robust MI Result
Induction heads are the most reproduced result in MI because:
- They emerge reliably in small (2-layer) models
- The pattern is visually unmistakable
- Ablation produces clear, measurable effects
- The mechanism is simple enough to fully understand

## What the Task Distribution Has to Look Like

"Reliably" above has a precondition my own repeated-token generator violated for months:
the prefix `[A_0, A_1, ..., A_k]` must have **no repeated tokens**. If `A_i == A_j` for
`i ≠ j` inside the prefix, "the previous occurrence of the current token" is no longer
unique — there may be several candidate positions to attend to, with different correct
next tokens. That is not a harder induction task, it is an **ill-posed** one: no amount of
training or model scale fixes a task whose correct answer is ambiguous.

This is a birthday-problem question: drawing `k` tokens uniformly from a `V`-token
vocabulary, the probability of at least one repeat is approximately
`1 - exp(-k(k-1) / (2V))`. My repeated-token generator's defaults before 2026-08-02 —
`vocab_size=32`, prefix length 32 at the standard scale — put that probability at **>99%**;
the `--quick` defaults (`vocab_size=16`, prefix length 12) at **~98%**. The prefix was
ambiguous almost everywhere, at every scale I had ever run this experiment.

`src.experiments.exp1_induction_heads.prefix_duplicate_probability()` makes this
checkable, and `make_repeated_token_data` now warns above a 30% collision threshold. New
defaults (`vocab_size=2048` standard, `256` quick) bring the probability to ~20-23% at the
existing prefix lengths — see
[[06_production_ai/exercises/ex-03-induction-task-design]] for the derivation, and
[[05_llm_engineering/proofs/intervention-validity]] for the causal-measurement bugs found
in the same audit family (a different failure mode: those were about what a fixed
intervention actually touches; this one is about whether the *task itself* has a
well-defined answer).

**What fixing this did and didn't change:** re-running `--quick` scale (500 epochs) under
the corrected vocabulary produced **zero warnings and still zero detected induction
heads** — `diag1_mass` peaked at 0.125, well under the 0.3 threshold. The ambiguity bug was
real and worth fixing on correctness grounds, but it was not, by itself, the reason quick
scale shows no heads; the 2026-08-01 audit's read (heads genuinely haven't formed yet at
that epoch/scale budget) still stands. See
[[06_production_ai/exercises/ex-03-induction-task-design]] for the full before/after.

A second, independent question this pass added the tooling to test: does the fixed
dataset (generated once, then only reshuffled across epochs) let the model **memorize**
specific sequences rather than learn the general prefix-matching-and-copying rule? Olsson
et al.'s original setup resamples continuously. `train_model`'s new `fresh_batches_fn`
parameter (and `--fresh-batches` on the CLI) makes this an ablation instead of an
assumption.

**Ran it — matched, one variable changed.** `vocab_size=2048, seq_len=24, d_model=32,
n_layers=2, n_heads=4, num_train=1024, batch_size=32`, 800 epochs, same seed, everything
identical except `--fresh-batches`:

| | Fixed dataset (reused, reshuffled) | Fresh batches (resampled every epoch) |
|---|---|---|
| Final train loss | 0.021 | 3.647 |
| Final val loss | 24.31 | 3.648 |
| Final val accuracy | **0.05%** (below 1/2048 random chance) | **52.2%** |
| Peak diag+1 mass | 0.155 (epoch 99, then decays) | 0.145 (epoch 649, still rising at 800) |
| Induction heads detected | 0 / 8 | 0 / 8 |

Two clean, unambiguous, opposite failure modes:

- **Fixed dataset: textbook catastrophic overfitting.** Train loss collapses to near-zero
  (the model memorizes all 1024 sequences exactly) while val loss *climbs* monotonically to
  24.3 and val accuracy *decays* to below the random-chance floor. `diag1_mass` peaks early
  (epoch 99) and then decays — whatever attention structure started to form gets
  overwritten by memorization, not consolidated into a general rule.
- **Fresh batches: stable, substantial generalization, no induction head yet.** Train and
  val loss track each other almost exactly the entire run (expected — there is no
  distinction between "seen" and "unseen" data when every batch is novel), and validation
  accuracy stabilizes at **52%**, three orders of magnitude above the fixed-dataset
  condition and far above the ~0.05% random baseline — real, generalizing signal, without
  ever crossing the 0.3 diag+1 threshold for a clean induction head. Unlike the fixed
  condition, `diag1_mass` is still *rising* at epoch 800 (0.145, up from 0.125 at epoch
  100), not decaying — the trajectory looks like a slower, still-in-progress version of
  circuit formation, not a dead end.

**Both hypotheses ruled in, cleanly separated:** the vocabulary-ambiguity bug was real but
insufficient alone (fixing it did not, by itself, produce heads at quick scale — see
above); the fixed-dataset memorization effect is also real, large, and independently
harmful — reusing the training set doesn't just fail to help, it actively destroys the
generalization the fresh-batches condition shows is achievable within the same epoch
budget. Neither condition crossed the induction-head detection threshold within 800 epochs
at this (still sub-standard) scale — the honest reading is that fresh-batches training
combined with more epochs and/or standard scale (`d_model=64`, `seq_len=64`) is the
credible path to an actual detected head, not yet demonstrated here.

## Links

- [[04_nlp_and_transformers/notes/qk-ov-circuits]]
- [[04_nlp_and_transformers/notes/activation-patching]]
- [[06_production_ai/exercises/ex-03-induction-task-design]]
- [[07_capstone/README]]
