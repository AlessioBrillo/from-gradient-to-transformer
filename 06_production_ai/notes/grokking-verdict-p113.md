---
tags: [type/lesson, phase/7, research/experiment, state/review]
created: 2026-08-11
---

# Grokking Verdict — P=113 (ADR-0003 row 1) — 2026-08-11

## The frozen criteria (ADR-0003, 2026-08-06, never edited)

Grok = val acc ≥ 0.95 sustained ≥ 5 checkpoints **AND** Fourier frequency
count < P/2 sustained. Generalization epoch reported.

## The manifest (results/exp2_grokking.json, from the final checkpoints)

| metric | seed 0 | seed 1 | seed 2 | mean ± std |
|--------|--------|--------|--------|------------|
| final_val_acc | 1.0000 | 1.0000 | 1.0000 | 1.0000 ± 0.0000 |
| generalization_epoch | 1250 | 1048 | 1326 | 1208 ± 117 |
| k_99_percent (freqs for 99% mass) | 111 | 111 | 111 | 111.0 ± 0.0 |
| k_90_percent | 92 | 94 | 92 | 92.7 ± 0.9 |
| total_mass_top_20 | 0.474 | 0.523 | 0.499 | 0.50 ± 0.02 |
| final fourier_sparsity (progress measure) | 0.085 | 0.082 | 0.071 | 0.079 ± 0.006 |

## The mechanical application

- **val acc criterion: MET.** All three seeds ≥ 0.95 at the 500-epoch
  checkpoint series from epoch 1500 onward — seed 0 from ckpt 1500 (0.9991)
  through 5000, seed 1 from 1500 (0.9937) through 5000, seed 2 from 2000
  (0.9998) through 5000 — i.e. ≥ 5 consecutive checkpoints sustained.
- **Fourier criterion: NOT MET.** k_99 = 111 of 113 frequencies carry 99%
  of the Fourier mass — essentially the full dense set. The runs' OWN final
  summaries printed the same verdict (`WARNING: Fourier representation is
  dense. Try increasing weight decay or training longer.`), so the analysis
  matches the experiment code on the same representation (the embedding
  re-normalization mutates weights in place every forward, so the saved
  weights ARE the used representation — no analysis mismatch).
- **Verdict: NO-GROK under the conjunctive frozen criterion** — accuracy
  PERFECT (100% val) but algorithm DENSE. The model solved modular addition
  at P=113 without forming the sparse Fourier solution the protocol defines
  as grokking. Generalization epochs: 1250 / 1048 / 1326.

## What this means (honest reading)

This is a **positive-negative**: the targeted phenomenon (sparse-Fourier
grokking at P=113 under the canonical recipe) is NOT reproduced, but the
machine, protocol and pipeline all worked — 3/3 seeds, 5000/5000 epochs,
checkpoint-every-500, manifest from disk. The negative is exactly the
pre-registered falsification case, so it ships as a contribution, not a
failure: "grokking modular addition at P=113 was not reproduced on CPU
under this protocol on this machine within this window; val_acc reached
1.0 but the Fourier representation stayed dense (k_99=111/113)."

The named suspects from the pre-registration (embedding re-normalization,
cosine schedule) are the microscope lane (ADR-0003 row 2):

1. **Embedding re-normalization** — the canonical config normalizes embedding
   and unembedding rows to unit norm after every optimizer step
   (`normalize_embeddings()` in-place, gated by `normalize_embed=True`,
   called at line 428). Hypothesis: constraining rows to the unit sphere
   interferes with the low-norm sparse Fourier circuit. Trial:
   `--no-normalize-embeddings` (new flag, default behavior unchanged).
2. **Cosine schedule** — CosineAnnealingLR is hardcoded (line 359).
   Hypothesis: the late-annealing LR decay disrupts the grokking transition
   at this scale. Trial: constant LR (needs a small `--schedule constant`
   flag, default unchanged — a recorded experiment-code change under a
   frozen protocol).
3. **My own third** — to be chosen with a one-line justification when trials
   1–2 land (candidate: weight decay 1.5×, or train fraction 0.5).

## The record

- Manifest: `results/exp2_grokking.json` (wall_clock=3418s, launch
  2026-08-11T19:40:05Z → final ckpt 20:37:03 local, all three seeds).
- Checkpoints: `checkpoints/exp2_checkpoint_seed{0,1,2}.pt` (final state,
  epoch 5000, val_acc 1.0).
- Verdict script: applied the frozen criteria mechanically; k_99 = the
  experiment's own CONFIRMED-line metric (one-off script removed in the
  2026-08-19 audit cleanup; criteria preserved in this note).
- Figures: `figures/exp2_grokking_curve.png`, `exp2_fourier_weights.png`,
  `exp2_frequency_ablation.png`, `exp2_progress_measures.png` (regenerated
  from best-seed checkpoint by the manifest producer).
- Row stamp: ADR-0003 row 1 → **CLOSED-with-verdict (2026-08-11,
  NO-GROK)**; row 2 (microscope) opened with the three trials above.
- Also landed on this date: fix for the `--help` crash (unescaped `%` in
  the `--probe` help string) and the `--no-normalize-embeddings` flag.

## Links

- [[docs/adr/0003-research-return-ledger]] — row 1 stamped, row 2 opened.
- [[06_production_ai/notes/scheduled-negatives-mp28]] — Negative 1 lands as
  written, one line added: the accuracy-perfect-but-dense reading.
- [[00_meta/27_micro-phase-28-the-execution]] — Session 4 record.
- [[portfolio/RESULTS]] — per-rung status updated.
