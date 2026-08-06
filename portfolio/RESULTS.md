---
tags: [portfolio, results]
---

# Results — Headline Findings

> **Thesis**: I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns — grokking modular addition with Fourier decomposition, induction heads, circuit verification via activation and path patching, and sparse autoencoder feature extraction.

All experiments are implemented in `src/experiments/`. Each has a `--quick` mode for fast
smoke tests (`make reproduce-quick`) and a full-scale mode (`make reproduce`).

---

## Honesty Ledger

Three audits have now caught real bugs in this repository's causal claims and evidence
base. All entries stay here — the point of this section is to make it easy to see the
trend (are correctness problems getting caught faster, or accumulating?), not to keep only
the latest one.

### 2026-08-02 — Micro-Phase 8, the Evidence Pass: correct-but-unmeasured code gets measured

The 2026-08-01 Validity Pass fixed *what the code measures*. It left the repository
correct and almost entirely **unmeasured**: Rung 2 had never run, Rungs 1 and 4 had no
post-fix standard-scale numbers, Rung 3 had never reproduced, Rung 5 was real only on
synthetic data. This pass built a multi-seed provenance harness
(`src/experiments/runner.py`, `src/results.py`, `make verify-claims` —
[[06_production_ai/notes/results-manifests-and-provenance]]) and pointed it at every rung
that fits this machine's CPU budget. What it found:

- **Rung 3's root cause, finally found.** The 2026-07-26 and 2026-08-01 audits both
  observed flat, near-zero "feature recovery" and could not explain it (the 2026-08-01
  tied-weights fix was a real correctness fix that changed nothing measurable). The
  architecture had no actual bottleneck — the dataset pre-compressed features before the
  model ever saw them, so the model was expanding an already-solved problem, not
  compressing anything. Rewritten to the canonical Elhage et al. setup (real
  `n_dimensions < n_features` bottleneck, decoder bias, ground-truth-free metrics); the
  phase transition now reproduces cleanly and immediately: **10/20 → 20/20 features
  represented as sparsity drops from 0.5 to 0.01.** See
  [[05_llm_engineering/proofs/superposition-setup-validity]] for the full reconstruction
  with the diagnostic numbers that found it, and
  [[06_production_ai/exercises/ex-01-falsify-your-own-metric]] for why the *old* metric
  couldn't have told the difference between broken and working even if the architecture
  had been right.
- **Rung 1's task design was ill-posed for its entire history.** The repeated-token
  generator's prefix needs no repeated tokens (else "the previous occurrence of the current
  token" is ambiguous). The pre-existing `vocab_size=32`/prefix-length-32 default gave a
  **>99.99%** chance of a repeated token in the prefix — a birthday-problem calculation, not
  a guess (`prefix_duplicate_probability()`,
  [[06_production_ai/exercises/ex-03-induction-task-design]]). Fixed (`vocab_size=2048`
  standard / `256` quick, ~20-23% collision). Fixing it alone did **not** produce induction
  heads at quick scale (`diag1_mass` peaked at 0.125, still below the 0.3 threshold) — a
  second, independent question this pass also built the tooling to test.
- **The fixed-dataset memorization hypothesis: confirmed, and it's large.** A matched
  800-epoch comparison (identical config, only `--fresh-batches` toggled) found the fixed,
  reused-every-epoch dataset causes catastrophic overfitting — val accuracy decays to
  **0.05%** (below random chance) while val loss climbs to 24.3 — versus fresh, resampled
  batches stabilizing at **52.2%** val accuracy with no train/val gap at all. Neither
  condition crossed the induction-head detection threshold within this (still sub-standard)
  budget, but the fresh-batches trajectory was still improving at epoch 800 while the fixed
  condition was actively regressing. See
  [[04_nlp_and_transformers/notes/induction-heads]] for the full table.
- **SAE on real activations, for the first time.** `exp5_sae_dashboard.py --activations-from`
  now harvests genuine residual-stream activations from a trained induction-heads
  checkpoint via a forward hook on `ln_final`, instead of only ever training on
  `ActivationGenerator`'s synthetic baseline. Added the pre-encoder bias (`x - b_dec`,
  Bricken et al.'s actual architecture — the prior SAE had no `b_dec` at all). First real
  run: **99.97% FVE, L0 = 136/256 (53% of the dictionary active), 0% dead features** —
  reconstructs *better* than the synthetic baseline (97.2% FVE) but far less sparsely (53%
  active vs. 17.4%). Read honestly, not as an unqualified win: this is more consistent with
  a small, undertrained 32-dimensional residual stream being easy to reconstruct densely
  than with the SAE finding genuinely sparse, interpretable features — see Rung 5 below.
- **Also this pass**: fixed a CI/local dev mismatch where `python-version: '3.11'` was
  pinned in `.github/workflows/python-ci.yml` while `uv.lock` and `[tool.mypy]` both target
  3.12 — the same class of silent mismatch that hid mypy crashing on numpy's stubs for an
  unknown period before 2026-08-01. The non-blocking mypy step now distinguishes "reported
  errors" (exit 1, fine) from "mypy itself crashed" (exit 2, now fails the build) instead of
  swallowing both with `|| true`. Added a small, honestly-scoped blocking mypy allowlist
  (`src/results.py`, `src/experiments/runner.py` — the only two candidate modules that
  turned out to actually be clean; `src/reproducibility.py` and `src/models/` were checked
  and are not). `portfolio/paper/` LaTeX scaffold added (structure only — no prose; see its
  own `main.tex` for what's still a `% TODO`).
- **Not done this pass, tracked as the next blocker**: the P=113 grokking flagship still
  has not run — `exp2_grokking.py` now has `--seeds` and
  `notebooks/colab_grokking_full_run.ipynb` is hardened for a 3-seed Colab run, but the run
  itself needs a GPU this environment doesn't have. This is still the single most important
  open item in the repository.

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

<!-- manifest: results/exp1_induction_heads.json -->

**Question**: Do induction heads emerge in a 2-layer attention-only transformer trained on repeated tokens? Can we detect, verify, and ablate them causally?

**Status**: task-design bug fixed 2026-08-02 (see Honesty Ledger) — the prefix-ambiguity bug
made the task ill-posed at nearly every position for the repository's entire history, at
every scale ever run. Fixing it alone did not produce heads at quick scale. A matched
fixed-vs-fresh-batches comparison (below) found a second, independently real effect: the
fixed-dataset training loop was actively harmful, not just insufficient. Standard-scale
numbers from before 2026-08-01 are **retracted** (ablation-site and metric-scale bugs; see
the Honesty Ledger's 2026-08-01 entry) — no standard-scale number in this table is
currently confirmed; the fixed/fresh comparison below is the only trustworthy scale.

| Metric | Tiny multi-seed (3 seeds, confirmed 2026-08-02) |
|--------|-------|
| Layers / Heads | 2 / 4 |
| d_model | 24 |
| Epochs | 150 |
| Train samples | 256 (resampled every epoch, `--fresh-batches`) |
| Val accuracy | 0.0047 ± 0.0012 (n=3) |
| Peak diag+1 mass | 0.177 ± 0.006 (n=3) |
| Induction heads detected (>0.3 threshold) | **0 / 8**, all 3 seeds |

**Fixed-vs-fresh-batches, matched 800-epoch comparison** (see
[[04_nlp_and_transformers/notes/induction-heads]] for the full writeup): identical config
(`vocab_size=2048, seq_len=24, d_model=32, num_train=1024`), only `--fresh-batches` toggled.

| | Fixed (reused every epoch) | Fresh (resampled every epoch) |
|---|---|---|
| Final val accuracy | **0.05%** (below random chance) | **52.2%** |
| Final val loss | 24.31 (climbing) | 3.65 (flat, tracks train loss exactly) |
| Peak diag+1 mass | 0.155 @ epoch 99, then decays | 0.145 @ epoch 649, still rising at 800 |

The fixed dataset produces textbook catastrophic overfitting; fresh batches produce
substantial, stable generalization without ever crossing the induction-head detection
threshold in this budget. Whether more epochs at this scale, or fresh-batches at standard
scale (`d_model=64`, `seq_len=64`), actually crosses the threshold is the next open
question — not yet run.

**Features**: attention entropy tracking, diagonal+1 induction signal plotted (metric scale
consistent with the detection threshold), W&B logging (`--wandb`), model saving
(`--save-model`), loss bump detection, 2×2 training curves plot, `--fresh-batches` (resample
per epoch) and `--seeds` (multi-seed manifest) added 2026-08-02.

**Reference**: Olsson et al., "In-context Learning and Induction Heads," Transformer Circuits Thread (Anthropic), 2022.

**Figures**: `figures/exp1_training_bump.png`

---

## Rung 2 — Grokking Modular Addition (Primary Flagship — NOT YET VERIFIED)

**Question**: Can I reproduce the grokking phase transition on modular addition (a+b mod P) and reverse-engineer the discrete Fourier transform algorithm the model learns?

**Status**: [ ] Not reproduced. The train/val split bug that made this structurally
unreachable was fixed 2026-07-26. The full P=113 run needing GPU-hours still has not been
executed — this is the single most important open item in the repository. The 2026-08-06
probe run finished the CPU-side de-risking (below): *the pipeline runs clean and the
failure to grok is a small-P phenomenon, not a recipe bug that a probe could catch*.
The P=113 GPU run is ready to go the moment a Colab session is available
(`notebooks/colab_grokking_full_run.ipynb`).

| Metric | P=29 (2026-08-01) | P=59 probe (2026-08-06) | Full Run (P=113) |
|--------|-------------------|-------------------------|-------------------|
| Modulus P | 29 | 59 | 113 |
| Train fraction | 30% | 30% | 30% |
| Epochs | 2000 | 1500 ctx / 3000 drill / wd 0.3 drill | 5000+ |
| Final val accuracy | 0.0017 | 0.0000–0.0012 (all three drills) | not yet run |
| Generalization epoch | none (-1) | none (-1), all drills | not yet run — needs ~5.5h CPU or minutes on a Colab GPU |
| Fourier frequencies used | 29 / 29 dense | 59 / 59 dense (all drills) | not yet run |

The fixed split makes the task well-posed (every class is reachable), but no small-P
run groks: P=29 at 2000 epochs, P=59 at 1500 epochs, P=59 at 3000 epochs (val loss
*rising* into the 9s at the end — active memorization, not slow progress), and P=59
at weight decay 0.3. Combined with the Fourier ablation (keep 59/59 frequencies →
0.0000) this is three P-values / two budgets / two weight-decay regimes pointing the
same way: small P lacks the combinatorial diversity for the Fourier algorithm to
emerge within a fixed budget. The full P=113 run remains the only way to see the
actual grokking transition; the probes narrowed the residual risk to P=113 itself
(the embedding re-normalization and cosine schedule are the named suspects if it
fails there too).

**Bug fixed 2026-07-26** (see Honesty Ledger above): the split held out by target class,
not equation, making some output classes structurally unreachable. Fixed to hold out
random `(a, b)` pairs.

**Reference**: Nanda et al., "Progress Measures for Grokking via Mechanistic Interpretability," ICLR 2023 (oral).

**Figures**: `figures/exp2_grokking_curve.png`, `figures/exp2_fourier_weights.png`,
`figures/exp2_frequency_ablation.png`, `figures/exp2_progress_measures.png` — current
contents are the last probe run (no-grokking sweeps), not a grokking curve.

---

## Rung 3 — Toy Models of Superposition

<!-- manifest: results/exp3_superposition.json -->

**Question**: How do features organize in a toy ReLU autoencoder under varying sparsity?

**Status**: [x] Phase transition reproduced 2026-08-02, after finding the actual root
cause of the 2026-07-26/2026-08-01 flat-recovery observations: the architecture had no
real bottleneck (see Honesty Ledger and
[[05_llm_engineering/proofs/superposition-setup-validity]]). Rewritten to the canonical
Elhage et al. setup; the transition reproduces on the first run, cleanly, with no tuning.

| Sparsity | Features represented | Mean dimensionality | Mean \|corr\| |
|----------|----------------------|----------------------|--------------|
| 0.500 | 10 / 20 | 0.250 | 0.302 |
| 0.200 | 15 / 20 | 0.250 | 0.316 |
| 0.100 | 19 / 20 | 0.250 | 0.340 |
| 0.050 | 20 / 20 | 0.250 | 0.349 |
| 0.020 | 20 / 20 | 0.250 | 0.348 |
| 0.010 | 20 / 20 | 0.248 | 0.352 |
| 0.005 | 20 / 20 | 0.248 | 0.352 |
| 0.002 | 20 / 20 | 0.249 | 0.350 |
| 0.001 | 16 / 20 | 0.250 | 0.326 |

Multi-seed manifest (3 seeds, `single_sparsity=0.01`, otherwise identical config):
`n_represented` = 19.67 ± 0.47 (one seed of three landed at 19/20 rather than 20/20 — a
real, small seed-to-seed spread, not noise-free).

Expected (Elhage et al.): as sparsity decreases (features rarely co-active), interference
pressure drops and the model represents more features. **Observed: exactly this — 10/20 at
the densest setting rising to 20/20 by sparsity=0.05, holding through 0.002.** (The drop to
16/20 at the sparsest setting, 0.001, is a genuine capacity limit — the 2000-vs-600-epoch
drill (2026-08-06) refuted the under-training hypothesis (see the MP10 honesty
ledger).) The old flat/near-zero "recovery" numbers above the fix are struck through in
spirit, not deleted from this table's history: the root cause was that the model had no
actual compression to perform (the dataset pre-embedded features before the model saw
them), not a metric-scale issue, not a training-budget issue, and not the untied-weights
hypothesis tested 2026-08-01. `mean_dimensionality` sits close to `1/n_dimensions × n_avg`
across the sweep as expected for features sharing the bottleneck roughly evenly.

**Geometry check (2026-08-06, 5 features → 2 dims)**: the small-case Gram check is now
done — at and below sparsity 0.1 the 5 directions sit on a regular pentagon (gaps
70.2–73.8°, std ≤ 1.4° vs ideal 72°; best 71.6–73.0°, std 0.5° at sparsity 0.02);
the dense regime (0.2–0.5) is 4/5 represented and off-pentagon (std 22°+). The
equiangular geometry is the sparse-phase attractor, not a dense-phase property.
Figure: `figures/exp3_pentagon_geometry.png`.

**Reference**: Elhage et al., "Toy Models of Superposition," Transformer Circuits Thread (Anthropic), 2022.

**Figures**: `figures/exp3_feature_geometry.png`, `figures/exp3_phase_change.png`

---

## Rung 4 — Circuit Verification via Activation and Path Patching

<!-- manifest: results/exp4_circuit_patching.json -->

**Question**: Can I find and causally validate a specific circuit via activation patching, path patching, and head ablation?

**Status**: Patch site and metric fixed 2026-08-01 (see Honesty Ledger — the previous
implementation patched a tensor that never reached the residual stream, and measured
confidence rather than correctness). Path patching added; it did not exist in any form
before this pass. The pre-fix standard-scale recovery numbers (0.787, 0.270, ...) that
used to live in this section are **retracted** — they measured `top1 − top2` under a patch
that mostly didn't land, so they don't mean what they claimed to. Vocabulary-ambiguity task
design bug (see Rung 1) fixed 2026-08-02, since this rung reuses
`make_repeated_token_data`; `--seeds` added.

**Quick-mode 3-seed manifest, 2026-08-02** (`vocab_size=64, seq_len=12, d_model=32,
epochs=500`):

| Metric | Value (mean ± std, n=3) |
|--------|--------------------------|
| Final val accuracy | 0.489 ± 0.014 |
| Mean activation-patching recovery (10 layer/position combos) | 0.197 ± 0.007 |
| Induction heads detected | **0 / 8**, all 3 seeds — consistent with Rung 1 at comparable scale |
| Head ablation / path patching | not run (no head to target) |

Activation patching runs cleanly and finds a real, small, consistent recovery signal
(~0.20, not zero) even without a detected induction head — some circuit sensitivity exists
at these (layer, position) combinations, just not concentrated enough in one head to cross
the 0.3 detection threshold. Because **0 induction heads were detected in all 3 seeds**,
head ablation and path patching were skipped again — meaning path patching's
implementation is *still* validated only by its unit tests (self-patch-is-zero,
runs-and-returns-expected-keys), not by an end-to-end run against a real head. This is now
the second consecutive confirmation (2026-08-01 quick, 2026-08-02 quick multi-seed) that a
real head is needed before this validation gap can close — the fix has to come from Rung
1's scale/fresh-batches work (see above), not from anything in this file.

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

**Question**: Can I train an SAE on synthetic residual stream activations and extract interpretable features? Does it work on real activations, not just synthetic ones?

**Status**: [x] Synthetic baseline reproduces exactly. [x] Real-activation upgrade shipped
2026-08-02: `--activations-from` harvests genuine residual-stream activations from a
trained induction-heads checkpoint via a forward hook on `ln_final`, and the architecture
gained the pre-encoder bias (`x - b_dec`) it was missing — Bricken et al.'s actual SAE, not
an approximation of it. Dead-feature threshold fixed 2026-08-01 (see Honesty Ledger).

| Metric | Synthetic (d_model=64, 8× dict) | Real (d_model=32, 8× dict, from a trained checkpoint) |
|--------|-------|-------|
| Dictionary size | 512 | 256 |
| L0 sparsity | 88.97 / 512 (17.4%) | 136.25 / 256 (**53.2%**) |
| Fraction of variance explained (FVE) | 0.9722 (97.2%) | **0.9997 (99.97%)** |
| Reconstruction MSE | 0.00113 | 0.1251 |
| Dead features (fixed 1e-4 threshold) | 1 / 512 (0.2%) | 0 / 256 (0%) |

**Read honestly, not as an unqualified win.** The real-activation run reconstructs *better*
but *far less sparsely* than synthetic — 53% of the dictionary fires per input versus 17%
for synthetic. That is not what a good SAE result looks like; it looks like a wide, dense
linear autoencoder that happens to reconstruct well because a 32-dimensional residual
stream from a small, undertrained model (150-300 epochs, no confirmed induction head — see
Rung 1) may simply not contain many genuinely sparse, disentangled features yet for the SAE
to find. This is exactly the "what did I add beyond the original?" distinctiveness gate
(`07_capstone/research-plan.md`) this rung was missing: a real degradation in the metric
that matters (sparsity, not just reconstruction) is a more informative result than a second
clean synthetic number would have been. Re-running this once Rung 1 has a checkpoint with a
confirmed induction head is the natural next step — right now the "real" activations come
from a model that hasn't yet learned the mechanism this pipeline exists to study.

**Reference**: Bricken et al., "Towards Monosemanticity" (2023); Cunningham et al., "Sparse Autoencoders Find Highly Interpretable Features in Language Models," ICLR 2024.

**Figures**: `figures/exp5_sparsity_tradeoff.png`, `figures/exp5_feature_histogram.png` (synthetic); `figures/exp5_sparsity_tradeoff_real.png`, `figures/exp5_feature_histogram_real.png` (real)

---

## Phase Gate Progress

| Phase | Status | Gate proof |
|-------|--------|------------|
| 1 — Foundations | ✅ Complete | — |
| 2 — Classical ML | ✅ Complete | complete-ml-pipeline |
| 3 — Deep Learning | ✅ Complete | gradient-flow-and-architectures |
| 4 — NLP & Transformers | ✅ Complete | circuit-analysis-complete |
| 5 — LLM Engineering | [~] Instrumentation done | — |
| 6 — Production AI | [~] Reproducibility harness built (multi-seed + manifests + `verify-claims`), CI/mypy fixed, paper scaffold added — W&B, Hugging Face Spaces, and the mini-paper prose are still open | [[06_production_ai/proofs/reproducible-from-clean-clone]] (not yet green — needs a post-commit clean-clone run) |
| 7 — Capstone | [~] Research plan written | — |

## Summary

| Rung | Status | Key Result |
|------|--------|------------|
| 1 — Induction Heads (fallback flagship) | ⚠️ Task design fixed, memorization confirmed, no head yet | Fresh-batches: 52.2% val acc vs. fixed dataset's 0.05% (matched 800-epoch comparison); 0/8 heads either way at this scale |
| 2 — Grokking (primary flagship) | ⏳ Not yet reproduced | `--seeds` added, Colab notebook hardened; GPU run still pending — the top open item |
| 3 — Superposition | ✅ Phase transition confirmed | Root cause found (no real bottleneck); rewritten, reproduces cleanly: 10/20 → 20/20 features represented |
| 4 — Circuit Patching | ⚠️ Fixed 2026-08-01, quick multi-seed re-run 2026-08-02 | See Rung 4 above for the current numbers; path patching still only unit-tested, no real head to validate against yet |
| 5 — SAE Dashboard | ✅ Synthetic reproduced; ⚠️ real-activation upgrade shipped | Real: 99.97% FVE but 53% L0 (dense, not sparse) — informative gap, not yet a clean win |
| 6 — ACDC | ❌ Deleted | Was fabricated data; removed 2026-08-01 rather than fixed |

**What to trust right now, in order**: (1) Rung 3's phase transition — reproduced cleanly,
root cause understood, multi-seed manifest backs it. (2) Rung 5's synthetic FVE/MSE numbers
— reproduced and architecturally simple; the real-activation numbers are real but need a
better checkpoint (one with a confirmed induction head) before the sparsity gap means
anything conclusive. (3) Rung 1's fixed-vs-fresh comparison — a real, large, matched effect,
though at a scale still well below standard. (4) Rung 4's quick multi-seed re-run — internal
consistency confirmed (activation patching runs cleanly, matches Rung 1's "0 heads" finding)
but path patching remains unvalidated against a real head. (5) Rung 2 — still nothing to
trust yet; the GPU run is the blocker.
