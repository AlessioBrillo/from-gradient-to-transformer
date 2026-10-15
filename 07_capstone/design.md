---
tags: [phase/7, type/lesson, state/review]
created: 2026-10-14
consumes: [configs/capstone.yaml, 07_capstone/checklist, portfolio/RESULTS]
---

# Capstone Design — the joint training + reverse-engineering pipeline

The capstone is one model trained on **two tasks at once**, instrumented so
that every mechanistic claim about it can be tested causally. This note is
the design document issue #170 asks for: what the pipeline is, why each
piece exists, and where the honest limits are. The 3×20k-step run is the
evidence; this is the design that run tests.

## The model

`src/models/decoder_only_transformer.py`: decoder-only, RMSNorm, RoPE,
causal multi-head attention with KV cache. Config (`configs/capstone.yaml`):
**d_model=256, 4 layers, 8 heads, d_mlp=1024, dropout 0.1** — ~25M
parameters at the capstone vocab. RoPE's relative-position property is
pinned by a test (`test_relative_position_invariance`); the convention
mismatch it caught in 2026-08 is the kind of bug that trains fine and
measures wrong.

## The tasks

| Task | Signal | Why joint |
|------|--------|-----------|
| Modular addition (P=113) | `(a+b) mod 113` at position 1 of a padded sequence | The grokking question: does the model build the sparse Fourier circuit? (See [[07_capstone/notes/grokking-verdict-p113\|the P=113 verdict]] — at solo scale, it does not: val 1.0 with a dense embedding.) |
| Repeated-token induction | prefix-matching-and-copying over a 2048-token vocab | The circuit question: do induction heads form, and can they be verified causally? |

**Why joint matters**: the MP-88 shakedown (2k steps) showed the two tasks
compete — induction took off (0.5041) while modular sat at chance (0.0047),
and the MP-89 A/B (vocab offset, curriculum reweight) could not move modular
off chance. The 20k run is the first budget where both tasks have room to
develop; whether the **dissociation** persists at scale is the question the
run exists to answer, not an afterthought.

## The instrumentation

Every measure runs inside the training loop, at a fixed cadence, on the
checkpoint-every boundary (1000 steps):

1. **Fourier decomposition** of the modular embeddings (`fourier_every`):
   the sparse/dense criterion. Recorded with **both** metrics — the L1-mass
   k₉₉ (historical, comparable with the P=113 NO-GROK record) and the
   post-audit **energy metric** (`k_energy_90`, `frac_energy_top5`,
   `energy_sparse`) that the 2026-10-08 audit installed. A run reported
   with only the L1 metric would repeat the falsified classification.
2. **K-composition** (`kcomp_every`): the two-step induction formation
   signal (Nanda & Jacobsen), with the vacuous-flag guard — a head
   attending to itself scores 1.0 without being an induction head, so the
   detector gates on that before reporting.
3. **Per-task validation split**: modular and induction accuracy logged
   separately, because the mixed mean hides the dissociation that is the
   result.
4. **Checkpoint/resume**: per-seed, per-step files (`exp6_capstone_seed<N>_step<S>.pt`),
   written atomically (tmp + replace) so a kill mid-save keeps the last
   valid state. The Kaggle/Colab notebook computes the last common step
   across seeds and passes `--resume` — a disconnected session is a pause,
   not a loss.

## The analysis chain (post-run)

1. Train 3 seeds × 20k steps, manifests via `--seeds --manifest-path`
   (pinned remotely, validated by `scripts/pin_remote_run.py`).
2. Per-seed: final modular/induction accuracy, Fourier density (both
   metrics), max K-comp.
3. Cross-seed: does the dissociation persist? Does any seed reach the
   sparse regime (k₉₉/P < 0.5 or `energy_sparse`)?
4. **Only if an induction head is confirmed**: exp4's head ablation and
   path patching against this checkpoint, then exp5's SAE on its residual
   stream — the cascade that has never been runnable end-to-end because no
   checkpoint ever had a confirmed head.

## Honest limits

- The sparse Fourier circuit has **never** been observed in this repository
  at any scale (every run dense, k₉₉ ≈ P). This run may well extend the
  negative; that is a result, not a failure, and the phase-gate note
  ([[07_capstone/notes/capstone-gate-honest-negative|the honest negative]])
  is written to stand either way.
- d_model=256/4L is small by grokking-paper standards; Nanda et al. used
  comparable models but different regularization. Deviations from the
  canonical recipe are documented per experiment rather than normalized
  away.
- The manifests record torch/python/device provenance; the remote runs use
  the runtime's preinstalled stack, not the local lockfile — the difference
  is visible in the manifest, not hidden.

## Update 2026-10-15: the run is in

The 3×20k run executed on a Kaggle T4 (`results/capstone_20k.json`; see the
[execution log](execution-log.md) for the full reading). The dissociation it
was built to test **persists at full budget**: induction accuracy 0.5034 ±
0.0002 — the same plateau as the 2k-step shakedown (0.5041), so it is
structural, not a budget artifact — and modular accuracy 0.1699 ± 0.0286,
above chance but far from the solo-run 1.0. Two measurements follow: the
joint model learns a *partial* modular solution, and the induction plateau
does not move with 10x the steps. The design's one unverified prediction —
that a longer budget would let both tasks develop — is falsified.

## Links
- [[07_capstone/research-plan|Capstone research plan]] — the ladder and the rung map
- [[portfolio/RESULTS|Honesty Ledger]] — the audit trail every number here answers to
- [[06_production_ai/notes/results-manifests-and-provenance|Results manifests and provenance]] — the manifest system this pipeline writes into
