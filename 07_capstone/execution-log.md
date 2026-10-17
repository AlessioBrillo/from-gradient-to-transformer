---
tags: [phase/7, capstone, execution/log, state/review]
created: 2026-09-01
updated: 2026-10-15
consumes: [ADR-0027, configs/capstone.yaml]
---

# Capstone Execution Log

Only runs that actually happened are recorded here.

## What was run

| Date | Run | Result | Evidence |
|------|-----|--------|----------|
| **2026-10-14** | **The planned 3-seed, 20,000-step capstone run (`configs/capstone.yaml`), on a Kaggle T4** | **The dissociation persists at full budget**: induction accuracy 0.5034 ± 0.0002, modular accuracy 0.1699 ± 0.0286 (vs 1.0 solo at P=113); Fourier k_99 = 97.4/113 (L1 reading), max K-comp 0.136 ± 0.027 | `results/capstone_20k.json` (git_sha 8243ec5, clean tree, device cuda, torch 2.11.0+cu128) |
| **2026-10-17** | **Post-audit energy re-analysis of the 3×20k checkpoints** (`scripts/capstone_energy_from_checkpoints.py`, no retraining) | **Fourier regime DENSE under the energy criterion**: k_energy_90 = 49.0 ± 0.0 of 56, energy_sparse = 0/3 seeds, frac_energy_top5 = 0.185 ± 0.013 — the capstone's joint solution is not a sparse Fourier circuit. | `results/capstone_20k_energy.json` (re-analysis of results/capstone_20k.json checkpoints, git tree dirty at analysis time) |
| 2026-09-07 | MP-88 shakedown, seed 0, 2,000 steps, joint modular + induction | Induction accuracy 0.5041; modular accuracy 0.0047 (chance) | [mp-88-shakedown-verdict](notes/mp-88-shakedown-verdict.md), `results/probe_capstone_shakedown.json` |
| 2026-09 | MP-89 retune A/B, 500 steps per arm (control, vocab offset, curriculum reweight) | Neither arm moves modular accuracy off chance | [mp-89-retune-verdict](notes/mp-89-retune-verdict.md), `results/probe_capstone_ab_*.json` |
| 2026-10-03 | SAE smoke check on the induction checkpoint | L0 about 250/512, max activation about 8.1; not an induction-circuit test | `scripts/verify_sae_induction.py`, [RESULTS](../portfolio/RESULTS.md) |

**Reading the 2026-10-14 run honestly.** The headline is the *stability* of the
induction plateau: 0.5034 at 20k steps vs 0.5041 at 2k steps — a 10x budget moves
the induction accuracy by 0.0007, so the plateau is structural (capacity or
interference), not a training-budget artifact. Modular is above chance (0.17 vs
1/113 = 0.0088) but nowhere near the solo-run 1.0: the shared model learns a
partial modular solution and a stuck induction solution. Two caveats on the
measurements: exp6 records the **L1-mass** k_99 only (the P=113 reversal showed
that reader calls sparse embeddings dense, so the capstone's Fourier density was
*not* established by this run). The post-audit energy metric has since been
added to exp6 and the 20k checkpoints re-analysed 2026-10-17: the joint solution
is **dense under the energy criterion** (k_energy_90 = 49/56, sparse on 0/3
seeds, see `results/capstone_20k_energy.json`), so the caveat is resolved, not
pending. The individual task mechanisms were not ablated here, only the end
accuracies.

The SAE smoke check used a local `sae_model.pt` (d_model=32, 512 features) that
`exp5_sae_dashboard.py` does not write, and was observed on the author's machine only, so it is
not CI-reproducible.

## What is pending

- Weights & Biases was never connected (no credentials); see
  [mp-90-wandb-gpu-close](notes/mp-90-wandb-gpu-close.md). The 20k run is recorded
  manifest-only, which the manifests make reproducible.
- exp6 gaining the energy metric (so the capstone's Fourier reading is not
  hostage to the falsified L1 classifier) — done 2026-10-17; the 20k run reads
  dense under the energy criterion (see the table above and
  `results/capstone_20k_energy.json`).
