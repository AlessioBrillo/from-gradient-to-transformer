---
tags: [type/moc, research/experiment, state/review]
created: 2026-08-06
---

# Micro-Phase 10 — The Evidence Run (roadmap + record)

Micro-Phase 9 ended with three blockers: Rung 2 (grokking) had never reproduced, Rung 1
(induction heads) had never formed a head, and the Rung 4/5 cascade was blocked on a
head-bearing checkpoint. This phase is about one thing: **building the instruments that
let me pull the trigger on GPU hours without burning them blindly** — progress measures
that exist *before* the run, a CPU de-risk path for the flagship, and a provenance path
for Colab results. Written from my perspective as a learning log, with the failed
hypotheses recorded as loudly as the confirmed ones.

## Where this started

- **Rung 2 (primary flagship)** — code and Colab notebook were ready, but the P=113 run
  needs GPU hours. CPU de-risk (P=59 probe) never existed; progress measures
  (Fourier sparsity, weight norm) were not committed. One bad GPU run costs a day.
- **Rung 1 (fallback flagship)** — fixed-vs-fresh comparison proved fresh batches keep
  improving at quick scale, but no induction head has ever formed. The standard-scale
  fresh-batches run was never executed; it has no canonical pinned config in code.
- **Rung 4/5 cascade** — path patching is unit-test-validated only; the SAE real-vs-synthetic
  comparison needs a real head checkpoint. One domino unblocks both.
- **Colab → manifest gap** — results run on Colab land outside the manifest universe;
  nothing pins the notebook to a committed SHA.
- **Rung 3 open question** — the geometry sweep at sparsity 0.001 represented only 16/20
  features; the under-training hypothesis was untested.

## Instruments built (the deliverable)

- **Grokking progress measures** (`exp2_grokking.py`): `fourier_sparsity_progress` and
  `weight_norm_progress` train alongside and are recorded per checkpoint interval
  (`--progress-interval`, default 10) — the phase transition is defined as
  validation accuracy crossing, with Fourier sparsity as the algorithmic-solution
  witness and weight norm as the weight-decay signature. Tests: `test_grokking.py`
  (`fourier_sparsity_progress`, `weight_norm_progress`, history keys).
- **Grokking CPU de-risk path**: `--probe` flag runs P=59, 1500 epochs, high weight
  decay, 30% train — a ~30-minute CPU run that validates the canonical recipe before
  any GPU hour is spent. The canonical pinned P=113 config (`d_model=128`, 4 heads,
  `d_mlp=512`, high weight decay, ~30% train, AdamW) is committed in the CLI defaults.
- **Canonical R1/R4 config pinned**: `--standard` flags on `exp1_induction_heads.py`
  and `exp4_circuit_patching.py` (`vocab_size=2048, seq_len=64, d_model=64, n_layers=2,
  n_heads=4, epochs=3000, num_train=8192, batch_size=64`, fresh batches on) — one
  committed config per rung, no drift between notes and code.
- **SAE multi-seed** (`exp5_sae_dashboard.py`): `--seeds` support via `run_single_seed`,
  joining the multi-seed manifest harness that exp1/3/4 already had.
- **Pentagon geometry check** (`exp3_superposition.py`): `compute_feature_angles`,
  `angular_gap_metrics`, `is_pentagon_like`, `plot_feature_directions` + `--geometry-check`
  CLI. Tests: `TestPentagonGeometry` (72° spacing, collinear-rejects, clustered-rejects,
  2D-only guard).
- **Colab provenance**: `ResultsManifest.notes` field (`src/results.py`) +
  `scripts/pin_colab_run.py` — pastes the notebook's output into the manifest system,
  refusing to record anything against a mismatched commit SHA. `scripts/clean_clone_check.sh`
  gates a fresh-clone → sync → CI → multi-seed → verify-claims sequence.
- **Makefile**: `reproduce-grokking-probe`, `reproduce-induction-standard`,
  `reproduce-induction-1layer`, `reproduce-exp3-geometry` targets.

## Pentagon geometry results (Rung 3)

Two separate measurements belong to two separate runs; the original writeup
conflated them and claimed the pentagon holds "at every level". Corrected table:

*20-feature capacity sweep* (`--single-sparsity` off, default 20 features, 2000
epochs / 16000 samples, figures `exp3_phase_change.png` + `exp3_feature_geometry.png`):

| Sparsity | Features represented |
|----------|----------------------|
| 0.5 … 0.01 | 20/20 |
| 0.001 | 14–16/20 (capacity-limited; the 2000-vs-600-epoch drill refuted under-training) |

*5→2 pentagon check* (re-run 2026-08-06, 600 epochs / 8000 samples each, figure
`figures/exp3_pentagon_geometry.png`):

| Sparsity | Features represented | Gap range (°) | Gap std (°) | Pentagon-like |
|----------|----------------------|---------------|-------------|---------------|
| 0.5      | 4/5                  | 38.1–90.6     | 22.4        | no |
| 0.2      | 4/5                  | 23.3–90.2     | 26.0        | no |
| 0.1      | 5/5                  | 70.3–73.8     | 1.4         | yes |
| 0.05     | 5/5                  | 70.2–72.9     | 1.0         | yes |
| 0.02     | 5/5                  | 71.6–73.0     | 0.5         | yes |
| 0.01     | 5/5                  | 70.6–72.8     | 0.8         | yes |

The honest claim is the interesting one: the regular pentagon is the **sparse-phase
attractor**, not a dense-phase property — in the dense regime (sparsity ≥ 0.2) the
bottleneck hosts 4/5 features with off-equiangular angles; once sparsity ≤ 0.1 the
directions sit on a regular pentagon (ideal 72°). A pure cosine reconstruction (two
spectral components, no symmetry) correctly measures 0.83 — the check is not
trivially always-pass.

## Honesty ledger (2026-08-06)

- **Under-training hypothesis for sparsity 0.001: refuted.** Retested with one variable
  changed (2000 vs 600 epochs, same 8000 samples): 15/20 represented, mean
  dimensionality 0.246 — *worse*, not better. The 16/20 at 600 epochs was run-to-run
  noise around a genuine capacity limit; the autoencoder at sparsity 0.001 is past its
  representational capacity, and no amount of compute fixes that. Recorded so the
  "more epochs would fix it" story doesn't get retold.
- **15/20 vs 16/20 spread is noise, not signal** — both sit at the same collapse point;
  the honest claim is "14–16/20, capacity-limited", not a specific count.

## State

Local CI mirror green at this commit: 168 pytest passed (161 baseline + 7 new
instrument tests), ruff clean, blocking mypy allowlist clean. Pushed and merged to
`main` (PR #34, 2026-08-06) — this "pending" line is superseded by
[[10_micro-phase-11-flagship-run]].

## Next

1. P=59 probe on CPU (de-risks the flagship recipe before any GPU spend).
2. Launch P=113 ×3 seeds on Colab, pin results via `scripts/pin_colab_run.py`.
3. Standard-scale fresh-batches run (Rung 1) — the domino for Rung 4/5.

All three are executed in [[10_micro-phase-11-flagship-run]].

## Links

- [[08_micro-phase-09-flagship-sprint]] — the roadmap this phase executes.
- [[07_micro-phase-08-evidence-pass]] — where the measurement infrastructure started.
- [[03_progress-log]] — chronological record.
- [[02_skill-tree]] — skill claims this phase's instruments make checkable.
