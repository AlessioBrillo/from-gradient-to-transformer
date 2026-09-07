---
tags: [phase/7, research/experiment, type/note]
created: 2026-09-07
consumes: [ADR-0028]
---

# MP-88 Shakedown Verdict — Row 1 COMPLETE (RETUNE)

My Row 1 evidence for ADR-0028: the frozen 1-seed by 2k-step capstone
shakedown ran to completion and produced a dissociation — induction
learns strongly, modular addition stays at chance. Full roadmap:
[[88_micro-phase-88-from-transcripts-to-verdicts|MP-88 · From Transcripts
to Verdicts]]. Prior transcript:
[[07_capstone/notes/mp-78-session-capstone-checkpoint-fix|MP-78
checkpoint-fix session]].

## Provenance

- **Invocation** (frozen since MP-82, unchanged):
  `uv run python -m src.experiments.exp6_capstone --seed 0 --steps 2000
  --warmup-steps 100 --checkpoint-every 500 --save-model
  --manifest-path results/probe_capstone_shakedown.json`
- **Run window:** 2026-09-07 02:00–03:21 UTC, 4855.4 s wall (~81 min).
- **Manifest:** `results/probe_capstone_shakedown.json` (probe path;
  flagship bytes untouched, `verify-claims` at 0).
- **Tree:** `git_sha db9c4c6`, `git_dirty false`, `device cpu`,
  `torch 2.12.1+cpu`, 4,259,584 parameters.
- **Checkpoints** (all present, ~51 MB each):
  `checkpoints/exp6_capstone_seed0_step{500,1000,1500,2000}.pt`.
- **Config:** P=113 modular (30% train fraction) plus induction
  (vocab 2048, seq_len 128); d_model 256, 4 layers, 8 heads;
  cosine schedule, warmup 100, `modular_weight = induction_weight`.

## Numbers (seed 0, single seed — a verdict, not a statistic)

| Metric | Step 550 (MP-87) | Step 2000 | Reading |
|---|---|---|---|
| Modular accuracy | 0.0057 | 0.0047 | Flat; below chance (1/113 ≈ 0.0088) |
| Induction accuracy | 0.0005 | 0.5041 | ~1000× rise across the horizon |
| Fourier k_99 | 98.2 | 98.1 | Dense throughout |
| Fourier k_90 | — | 67.2 | Dense at every cutoff |
| Max K-comp | 0.31 | 0.394 | Detector alive, head unconfirmed |

## Verdict: harness GREEN, science RETUNE

**Harness GREEN** — every Row 1 success criterion met: both streams
flowed with task alternation, all four checkpoints reload via
`resume_step`, instrumentation fired at every 500-step boundary with
zero crashes after the MP-87 Fourier fix, manifest complete with clean
provenance.

**Science RETUNE** — joint training is viable (one task takes off) but
imbalanced (the other never leaves chance). No 20k-by-3-seed launch on
this config: a second seed would price statistics on top of an
unexamined confound.

## What I do not claim

- **No induction head.** K-comp 0.394 is a composition score, not the
  per-head diag+1 mass the 0.3 detection threshold applies to. Path
  patching stays unit-tested-only until a head is confirmed.
- **No modular mechanism.** k_99 98.1 is the dense regime, matching my
  P=113 NO-GROK baseline (111/113) — dense again, not sparse.
- **Below-chance modular is a footnote, not a finding.** 0.0047
  against 0.0088 chance is consistent with interference from the shared
  embedding rows (modular ids `0..P-1` collide with induction token
  ids), but consistency is not evidence. The Session-4 A/B decides.

## Session-4 decision rule (frozen at Session 0, executed with A/B data)

Retune A/B, 500 steps per arm: (arm A) vocab-offset — modular tokens
in a dedicated id range, implemented test-first; (arm B) curriculum
reweight — `modular_weight` raised against `induction_weight`. Single
score: modular accuracy movement off chance.

- Modular moves → launch the retuned full 2k; paper diff from
  manifests; teaching artifact on the new checkpoint.
- Nothing moves → dated "v20 is the record" memo; the interference
  pattern characterized as the contribution; no further horizons on
  this config.

**Decided:** 2026-09-07 · **Row:** ADR-0028 Row 1 · **Next:** Row 2
opens on the A/B, never before it.
