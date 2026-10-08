---
tags: [phase/7, capstone, execution/log]
created: 2026-09-01
updated: 2026-10-08
consumes: [ADR-0027, configs/capstone.yaml]
---

# Capstone Execution Log

Only runs that actually happened are recorded here. The planned 3-seed, 20,000-step capstone
run (`configs/capstone.yaml`) has **not** been executed; an earlier version of this file held
empty session templates for it (Sessions 0-8, "Ready for Session 1") and was replaced on
2026-10-08 so that the log no longer promises work that was not done.

## What was run

| Date | Run | Result | Evidence |
|------|-----|--------|----------|
| 2026-09-07 | MP-88 shakedown, seed 0, 2,000 steps, joint modular + induction | Induction accuracy 0.5041; modular accuracy 0.0047 (chance) | [mp-88-shakedown-verdict](notes/mp-88-shakedown-verdict.md), `results/probe_capstone_shakedown.json` |
| 2026-09 | MP-89 retune A/B, 500 steps per arm (control, vocab offset, curriculum reweight) | Neither arm moves modular accuracy off chance | [mp-89-retune-verdict](notes/mp-89-retune-verdict.md), `results/probe_capstone_ab_*.json` |
| 2026-10-03 | SAE smoke check on the induction checkpoint | L0 about 250/512, max activation about 8.1; not an induction-circuit test | `scripts/verify_sae_induction.py`, [RESULTS](../portfolio/RESULTS.md) |

The SAE smoke check used a local `sae_model.pt` (d_model=32, 512 features) that
`exp5_sae_dashboard.py` does not write, and was observed on the author's machine only, so it is
not CI-reproducible.

## What is pending

- The 3-seed, 20,000-step capstone run needs a GPU (about 0.6 s/step on the author's CPU).
  It is gated on the Rung 2 protocol audit: see the Honesty Ledger in
  [RESULTS](../portfolio/RESULTS.md).
- Weights & Biases was never connected (no credentials); see
  [mp-90-wandb-gpu-close](notes/mp-90-wandb-gpu-close.md).
