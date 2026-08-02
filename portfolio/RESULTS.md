---
tags: [portfolio, results]
---

# Results — Headline Findings

> **Thesis**: I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns — grokking modular addition with Fourier decomposition, induction heads, circuit verification via activation and path patching, and sparse autoencoder feature extraction.

All experiments are implemented in `src/experiments/`. Each has a `--quick` mode for fast
smoke tests (`make reproduce-quick`) and a full-scale mode (`make reproduce`).

---

## Honesty Ledger

Two audits have now caught real bugs in this repository's causal claims. Both entries stay
here — the point of this section is to make it easy to see the trend (are correctness
problems getting caught faster, or accumulating?), not to keep only the latest one.

### 2026-08-01 — Validity Pass: three causal claims were measuring the wrong thing

A code-level audit (not a re-run — a *reading* of what each intervention actually touches)
found that Rungs 1 and 4's causal claims rested on interventions that didn't do what their
names said:

| # | What was wrong | Where | What it actually did |
|---|---|---|---|
| 1 | Ablation zeroed a post-mixing tensor | `exp1_induction_heads.py`, `causal_ablation()` | Hooked `W_O`'s *output* — already mixed across every head — and zeroed an `n_heads`-way slice of it. That zeroes an arbitrary residual-stream subspace, not a head. |
| 2 | Patch never reached the residual stream | `exp4_circuit_patching.py`, `run_activation_patching()` | Hooked the MLP's *input* (a normalized copy of resid_mid). The residual skip two lines later re-reads the block's own unpatched `x` — the patch changed the MLP branch's output but nothing that survives to the next layer. |
| 3 | Metric measured confidence, not correctness | same function | `top1 − top2` on the model's own logits. A model confidently wrong scores identically to a model confidently right. |
| 4 | A plotted metric was on the wrong scale | `exp1_induction_heads.py`, `compute_attention_entropy()` | `diag1_mass` summed per-head signal across heads instead of taking the max — a `[0, n_heads]`-scale number plotted against a per-head `0.3` threshold. Root cause of the 2026-07-26 "mass ≈ 1.0 but 0 heads detected" discrepancy: never the same unit. |

**Fixes applied**, all with falsification tests that would have failed against the old code
(see [[05_llm_engineering/proofs/intervention-validity]] for the full reconstruction):
- `causal_ablation()` now uses a `head_mask` applied *before* `W_O`, matching the approach
  `exp4_circuit_patching.py` already had right for its own head ablation. Falsified with:
  ablating every head in every block must reproduce the model's no-attention baseline
  *exactly* — `tests/test_induction_heads.py::test_ablating_all_heads_collapses_to_no_attention_baseline`.
- `run_activation_patching()` now hooks the block's `attn` module directly (its output is
  already post-`W_O`, the exact tensor added to `resid_pre`), and defines
  `logit_diff = logits[answer] − logits[counterfactual]` against real task labels instead
  of `top1 − top2`. Falsified with: patching a run against *itself* must be an exact no-op
  — `tests/test_exp4_circuit_patching.py::TestActivationPatching::test_self_patching_is_a_no_op`.
- **Path patching was added** (`run_path_patching_to_logits()`) — it had a note
  (`04_nlp_and_transformers/notes/path-patching.md`) and a commit scope but no
  implementation anywhere in `src/` before this pass. It isolates a single head's *direct*
  effect on the logits by decomposing `attn_out` through `W_O`'s per-head column blocks,
  distinct from activation patching's inclusion of effects mediated through later layers.
- `diag1_mass` now takes the max over heads (and over layers), making it comparable to the
  0.3 per-head threshold it's plotted against.

**Also this pass:**
- **Rung 6 deleted, not fixed.** `exp6_automated_circuit.py` plotted `rng.poisson`/`rng.beta`/`rng.exponential`
  draws labeled "Faithfulness" and "Time to Discovery." Labeled a placeholder in logs, but
  fabricated numbers next to real results in a portfolio repo are a liability even when
  labeled. Revisit only with a real ACDC implementation.
- **RoPE convention fixed.** `cos`/`sin` were built with `repeat_interleave(2)` (interleaved-pairs
  convention) but rotated with a `chunk(2)`-based `_rotate_half` (half-split convention) — two
  incompatible layouts. Every position still got a distinct signal (so training didn't
  obviously break), but the relative-position property RoPE exists for — that the attention
  score between positions *i* and *j* depends only on *i − j* — did not hold. Fixed and now
  covered by `tests/test_decoder_only_transformer.py::test_relative_position_invariance`.
- **Superposition (Rung 3) weights are now tied** (`decoder.weight == encoder.weight.T`,
  the canonical Elhage et al. setup) instead of two independently-learned matrices. This
  was a real correctness fix — but a single-point empirical check (sparsity=0.01, quick
  mode) shows it **did not change** the flat/near-zero recovery the 2026-07-26 audit found
  (0.100 before, 0.100 after). My hypothesis that untied weights explained the
  discrepancy is **not supported**. The real root cause of Rung 3's non-reproduction is
  still open.
- **SAE dead-feature threshold fixed.** Was `1/(10·n_features)` — a threshold that got
  *looser* as the dictionary grew (backwards). Now a fixed `1e-4`, independent of
  dictionary size; `never_fires` (a stricter, unambiguous "dead") is also reported.
- **Unused MI tooling dependencies dropped**: `transformer-lens`, `sae-lens`, `circuitsvis`,
  `einops`, `seaborn`, `datasets`, `accelerate` were all pinned in `pyproject.toml` and
  never imported anywhere in `src/`. Removing them dropped ~100 transitive packages from
  `uv.lock`. The one prior reference (`transformer_lens.utils.reset_hooks()` in
  `src/reproducibility.py`) wasn't a real TransformerLens function and silently no-op'd.
- **`mypy`'s `python_version` was mismatched with the actual resolved interpreter**
  (config said 3.11, `uv.lock` resolves 3.12), which made mypy crash on numpy's stub files
  *before checking a single line of `src/`*. CI's `mypy ... || true` silently swallowed
  this, so the "54 pre-existing errors" comment that lived in `python-ci.yml` was never
  actually observed — mypy hadn't gotten far enough to produce it. Fixed the version
  mismatch; real strict-mode count is 154 errors (mostly missing generic type args, not
  caught bugs), left as tracked follow-up rather than rushed through in this pass.
- **Import-time filesystem side effect removed.** `import src` used to create a `figures/`
  directory as a side effect (each experiment module ran `FIGURES_DIR.mkdir()` at module
  scope). Moved into each `main()`.

### 2026-07-26 — Reproducibility Audit: Real Bug Found, Claims Reconciled to Evidence

`figures/` did not exist prior to this audit despite being referenced throughout this
document and `00_meta/00_home.md`. This session installed the minimal runtime deps
(torch-cpu, numpy, matplotlib, tqdm) and ran every rung's `--quick` mode on CPU to generate
real figures and cross-check the numbers already documented. Findings:

- **Grokking (Rung 2): found and fixed a real bug**, not just a compute bottleneck.
  `make_modular_addition_data` split train/val by **target class** (`(a+b) % P`) instead
  of by **equation** `(a, b)`. This left some output classes with zero training signal —
  the model was asked to predict classes its unembedding row never saw, which is not
  generalization, it's an unsolvable task. Produced exactly 0% validation accuracy even at
  trivial P=11 with no compute constraint, independent of the CPU/GPU bottleneck
  previously blamed. Fixed to hold out random `(a, b)` pairs, matching the canonical
  Power et al. / Nanda et al. setup where every target class appears in both splits.
- **Induction heads (Rungs 1 & 4): quick-mode detected 0 heads** despite diagonal+1
  attention mass reported near 1.0 — root-caused in the 2026-08-01 pass above (a metric
  scale bug, not a detection failure or a real absence of heads at standard scale).
- **Superposition (Rung 3): no phase transition observed** in a reduced sweep — flagged,
  partially investigated 2026-08-01 (see above), still open.
- **SAE (Rung 5): reproduced exactly** (97.2% FVE) on synthetic data.
- **ACDC (Rung 6): confirmed simulated/placeholder**, exactly as labeled — deleted 2026-08-01.

---

## Rung 1 — Induction Heads (Fallback Flagship, currently the strongest verified result)

**Question**: Do induction heads emerge in a 2-layer attention-only transformer trained on repeated tokens? Can we detect, verify, and ablate them causally?

**Status**: `--quick` mode re-run 2026-08-01, post-fix. Standard-scale numbers below are
from before the ablation-site and metric-scale fixes and have **not been re-verified**
at that scale — the quick-mode row is the only row confirmed against the current code.

| Metric | Standard (unconfirmed post-fix) | Quick (confirmed 2026-08-01) |
|--------|----------|-------|
| Layers / Heads | 2 / 4 | 2 / 4 |
| d_model | 64 | 32 |
| Epochs | 5000 | 500 |
| Train samples | 8192 | 1024 |
| Val accuracy | — | 0.549 (final), 0.553 (peak, ~epoch 100) |
| Peak diag+1 mass (max over heads/layers, fixed metric) | — | 0.173 (epoch 50) |
| Induction heads detected (>0.3 threshold) | Yes (claimed, unconfirmed) | **0 / 8** — genuinely below threshold, not a metric artifact |

At quick scale, induction heads have **not** formed within 500 epochs — `diag1_mass` peaks
at 0.173 and *decays* over training (down to 0.170 by epoch 500), well under the 0.3
detection threshold. This is now a trustworthy negative result (the metric that reports it
is on the correct scale) rather than the contradictory "mass ≈ 1, 0 heads" reading from
before the fix. Whether heads emerge at standard scale (more epochs, larger model) remains
to be re-confirmed.

**Features**: attention entropy tracking, diagonal+1 induction signal plotted (now on a
metric scale consistent with the detection threshold), W&B logging (`--wandb`), model
saving (`--save-model`), loss bump detection, 2×2 training curves plot.

**Reference**: Olsson et al., "In-context Learning and Induction Heads," Transformer Circuits Thread (Anthropic), 2022.

**Figures**: `figures/exp1_training_bump.png`

---

## Rung 2 — Grokking Modular Addition (Primary Flagship — NOT YET VERIFIED)

**Question**: Can I reproduce the grokking phase transition on modular addition (a+b mod P) and reverse-engineer the discrete Fourier transform algorithm the model learns?

**Status**: [ ] Not reproduced. The train/val split bug that made this structurally
unreachable was fixed 2026-07-26. The full P=113 run needing GPU-hours still has not been
executed — this is the single most important open item in the repository, and the
2026-08-01 validity pass deliberately did not spend its budget chasing it, since fixing
the three actively-wrong causal claims in Rungs 1 and 4 was higher priority than a compute
bottleneck. See `notebooks/colab_grokking_full_run.ipynb` for a ready-to-run Colab notebook.

| Metric | Quick Test (P=29, fixed split, re-run 2026-08-01) | Full Run (P=113) |
|--------|-------------------|-------------------|
| Modulus P | 29 | 113 |
| Train fraction | 30% | 30% |
| Epochs | 2000 | 5000+ |
| Final val accuracy | 0.0017 | not yet run |
| Generalization epoch | none (-1) | not yet run — needs ~5.5h on CPU or minutes on a free Colab GPU |
| Fourier frequencies used | 29 / 29 (100% — dense, no clean algorithmic solution found) | not yet run |

The fixed split makes the task well-posed (every class is reachable), but P=29 at 2000
epochs still does not grok — consistent with the roadmap's own note that small P lacks the
combinatorial diversity for the Fourier algorithm to emerge, and with the quick-mode
config generally trading fidelity for speed. This is a genuine negative result, not the
old bug: the model *can* solve this task in principle now, it just hasn't within this
budget. The full P=113 run remains the only way to see the actual grokking transition.

**Bug fixed 2026-07-26** (see Honesty Ledger above): the split held out by target class,
not equation, making some output classes structurally unreachable. Fixed to hold out
random `(a, b)` pairs.

**Reference**: Nanda et al., "Progress Measures for Grokking via Mechanistic Interpretability," ICLR 2023 (oral).

**Figures**: `figures/exp2_grokking_curve.png`, `figures/exp2_fourier_weights.png`, `figures/exp2_frequency_ablation.png`, `figures/exp2_progress_measures.png`

---

## Rung 3 — Toy Models of Superposition

**Question**: How do features organize in a toy ReLU autoencoder under varying sparsity?

**Status**: [ ] Not reproduced. No phase transition observed in the 2026-07-26 sweep;
the 2026-08-01 tied-weights fix (see Honesty Ledger) did not change this. Root cause
still open.

| Sparsity | Feature recovery | Monosemantic rate | Mean \|corr\| |
|----------|-------------------|--------------------|--------------|
| 0.500 | 0.050 | 0.100 | 0.282 |
| 0.200 | 0.100 | 0.100 | 0.316 |
| 0.100 | 0.150 | 0.150 | 0.302 |
| 0.050 | 0.100 | 0.100 | 0.345 |
| 0.020 | 0.050 | 0.050 | 0.305 |
| 0.010 (untied, 2026-07-26) | 0.100 | 0.100 | 0.311 |
| 0.010 (**tied**, 2026-08-01) | **0.100** | **0.100** | **0.299** |
| 0.005 | 0.050 | 0.050 | 0.305 |
| 0.002 | 0.000 | 0.000 | 0.324 |
| 0.001 | 0.000 | 0.000 | 0.341 |

Expected (Elhage et al.): recovery should rise toward monosemantic (→1.0) as sparsity
decreases (features rarely active). Observed: flat/near-zero with no such trend, and the
one variable I could think of that plausibly explained it (untied encoder/decoder weights
giving the model extra degrees of freedom to reconstruct without the encoder rows ever
converging to the ground-truth directions) turned out not to be it — tying the weights to
the canonical setup left the 0.01-sparsity result essentially unchanged. Candidates still
open: insufficient epochs even at 2000, the `feature_recovery_rate` metric/threshold
definition, or the `n_features=20` / `n_dimensions=5` ratio.

**Reference**: Elhage et al., "Toy Models of Superposition," Transformer Circuits Thread (Anthropic), 2022.

**Figures**: `figures/exp3_feature_geometry.png`, `figures/exp3_phase_change.png`

---

## Rung 4 — Circuit Verification via Activation and Path Patching

**Question**: Can I find and causally validate a specific circuit via activation patching, path patching, and head ablation?

**Status**: Patch site and metric fixed 2026-08-01 (see Honesty Ledger — the previous
implementation patched a tensor that never reached the residual stream, and measured
confidence rather than correctness). Path patching added; it did not exist in any form
before this pass. The pre-fix standard-scale recovery numbers (0.787, 0.270, ...) that
used to live in this section are **retracted** — they measured `top1 − top2` under a patch
that mostly didn't land, so they don't mean what they claimed to.

Quick mode re-run 2026-08-01 under the fixed code: activation patching ran cleanly across
10 (layer, position) combinations with no errors (`figures/exp4_attention_patterns.png`,
`figures/exp4_patching_results.png` regenerated). Consistent with Rung 1's finding at the
same scale, **0 induction heads were detected**, so head ablation and path patching were
skipped — meaning path patching's implementation is currently validated only by its unit
tests (self-patch-is-zero, runs-and-returns-expected-keys), not by an end-to-end run
against a real head. A standard-scale run, once heads are confirmed to form, is needed
before any recovery number can be reported here.

**Method**:
1. Train `DecoderOnlyTransformer` on repeated-token prediction (same task as Rung 1),
   detect induction heads via diagonal+1 attention mass.
2. **Residual stream activation patching**: hook the block's `attn` module directly (its
   output is already post-`W_O`) to override `resid_mid` at a given (layer, position) from
   a corrupted run — a second, disjoint batch from the same task generator, not a
   within-sequence permutation (which destroys the induction structure and leaves no
   well-defined correct answer). Metric: `logits[answer] − logits[counterfactual]` against
   each batch's real next-token label.
3. **Path patching**: isolate a single head's *direct* effect on the logits by decomposing
   `attn_out` through `W_O`'s per-head column blocks and swapping only that head's
   contribution to the final residual stream — everything else (other heads, all MLPs,
   this head's own indirect effects through later layers) stays clean.
4. **Head-level zero ablation**: `head_mask` zeroes a head's contribution before `W_O`.

All three interventions carry falsification tests: self-patching (corrupted == clean) must
be an exact no-op for both activation and path patching
(`tests/test_exp4_circuit_patching.py`), and patching against a genuinely different run
must move the logit diff somewhere.

**Outputs**: `figures/exp4_attention_patterns.png`, `figures/exp4_patching_results.png`, `figures/exp4_head_ablation.png`

**Reference**: Wang et al., "Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small," ICLR 2023. Zhang & Nanda, "Towards Best Practices of Activation Patching," ICLR 2024 — the corrective paper for exactly the site/metric mistakes found here.

---

## Rung 5 — Sparse Autoencoder Feature Dashboard

**Question**: Can I train an SAE on synthetic residual stream activations and extract interpretable features?

**Status**: [x] Complete on synthetic data — ready to upgrade to real activations. Dead-feature threshold fixed 2026-08-01 (see Honesty Ledger).

| Metric | Value |
|--------|-------|
| Dictionary size (d_model=64) | 512 (8×) |
| L0 sparsity | 88.97 / 512 (17.4%) |
| Fraction of variance explained (FVE) | 0.9722 (97.2%) |
| Reconstruction MSE | 0.00113 |
| Dead features (< 1e-4 firing rate, fixed threshold, re-measured 2026-08-01) | 1 / 512 (0.2%) |

At `n_features=512`, the old size-scaled threshold (`1/(10·512) ≈ 1.95e-4`) and the new
fixed `1e-4` happen to land close enough together that the dead-feature count is unchanged
here — the fix matters more at other dictionary sizes, where the old formula would have
gotten silently more lenient as the dictionary grew.

**Next**: Upgrade to real activations from the trained induction-heads model.

**Reference**: Bricken et al., "Towards Monosemanticity" (2023); Cunningham et al., "Sparse Autoencoders Find Highly Interpretable Features in Language Models," ICLR 2024.

**Figures**: `figures/exp5_sparsity_tradeoff.png`, `figures/exp5_feature_histogram.png`

---

## Phase Gate Progress

| Phase | Status | Gate proof |
|-------|--------|------------|
| 1 — Foundations | ✅ Complete | — |
| 2 — Classical ML | ✅ Complete | complete-ml-pipeline |
| 3 — Deep Learning | ✅ Complete | gradient-flow-and-architectures |
| 4 — NLP & Transformers | ✅ Complete | circuit-analysis-complete |
| 5 — LLM Engineering | [~] Instrumentation done | — |
| 6 — Production AI | [ ] Not started | — |
| 7 — Capstone | [~] Research plan written | — |

## Summary

| Rung | Status | Key Result |
|------|--------|------------|
| 1 — Induction Heads (fallback flagship) | ⚠️ Quick-scale confirmed, standard-scale unconfirmed | Quick mode, post-fix: 0 heads detected, genuinely below threshold (diag+1 mass peaks 0.173 < 0.3) |
| 2 — Grokking (primary flagship) | ⏳ Not yet reproduced | Split bug fixed 2026-07-26; GPU run still pending — the top open item |
| 3 — Superposition | ⏳ Not reproduced | Flat/near-zero recovery across all sparsity levels; tied-weights fix tested and did not resolve it |
| 4 — Circuit Patching | ⚠️ Fixed, not yet re-verified | Patch site + metric were wrong pre-2026-08-01; path patching added; clean re-run pending |
| 5 — SAE Dashboard | ✅ Reproduced | 97.2% FVE, synthetic data; dead-feature threshold fixed, not yet re-measured |
| 6 — ACDC | ❌ Deleted | Was fabricated data; removed 2026-08-01 rather than fixed |

**What to trust right now, in order**: (1) Rung 5's FVE/MSE numbers — reproduced and
architecturally simple. (2) Rung 1's quick-mode "0 heads, below threshold" finding — the
metric bug that would have cast doubt on it is fixed. (3) Nothing else in this table yet —
Rung 2 needs its GPU run, Rung 3's discrepancy is unexplained, and Rung 4's numbers predate
today's fix and need a clean re-run before they mean anything.
