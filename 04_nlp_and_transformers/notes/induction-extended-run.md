---
tags: [phase/4, research/experiment, protocol, induction-heads]
created: 2026-08-21
---

# Extended Induction Heads Run — 10k Epochs ×3 Seeds

## Purpose

The standard-scale induction heads run (2026-08-14, 3000 epochs, fresh-batches) peaked at diag+1 mass 0.075 (threshold 0.3), with 0/8 heads detected. Nanda & Jacobsen (2023) show the two-step path: Step 1 (L0 duplicate-token head) forms first, then Step 2 (K-composition) crosses the threshold later. The 3000-epoch run may have been in the "pre-emergence" regime.

This extended run tests whether 10k epochs at the same standard scale produces confirmed induction heads.

## Protocol

```bash
uv run python -m src.experiments.exp1_induction_heads \
  --standard \
  --epochs 10000 \
  --checkpoint-every 500 \
  --save-model \
  --seeds 0,1,2
```

## Configuration (--standard pinning)

| Parameter | Value | Source |
|-----------|-------|--------|
| vocab_size | 2048 | Fixed 2026-08-02 (prefix ambiguity fix) |
| seq_len | 64 | Canonical |
| d_model | 64 | Standard scale |
| n_layers | 2 | Induction heads need ≥2 layers for K-composition |
| n_heads | 4 | Per layer |
| epochs | 10000 | Extended from 3000 |
| lr | 1e-3 | Canonical |
| weight_decay | 0.1 | Standard |
| batch_size | 64 | Standard |
| num_train | 8192 | Standard |
| fresh_batches | True | Critical: resample every epoch |
| checkpoint_every | 500 | 20 checkpoints per run |
| seeds | 0,1,2 | Multi-seed manifest |

## Measurements (Every 500 Epochs)

The experiment already instruments these via `diagnose_induction_formation`:

| Metric | Meaning | Target for "Confirmed Head" |
|--------|---------|----------------------------|
| `step1_l0_duplicate_mass` (max over heads) | L0 head attends to previous token | > 0.3 |
| `l0_peakedness` (max over heads) | L0 head's argmax is focused | > 0.5 |
| `step2_k_composition` (best pair) | L1 head composes with L0's prev+1 | > 0.3 |
| `diag1_mass` (max over layers/heads) | Direct induction signal | > 0.3 |
| `val_acc` | Next-token prediction accuracy | > 0.5 (above chance 1/2048) |

## Expected Trajectory (Hypothesis)

Based on Nanda & Jacobsen (2023) Figure 3:

| Epoch Range | Phase | Expected Metrics |
|-------------|-------|------------------|
| 0–2000 | Memorization / pre-emergence | val_acc ~ 0.05, diag1_mass ~ 0.1, Step 1 forming |
| 2000–6000 | Circuit formation | Step 1 > 0.3, Step 2 rising, val_acc climbing |
| 6000–10000 | Cleanup / consolidation | Step 2 > 0.3, diag1_mass > 0.3, heads detected |

## Outputs

### Per-500-Epoch Checkpoints
- `checkpoints/exp1_seed{0,1,2}_epoch{500,1000,...,10000}.pt`
- Each contains: model, optimizer, scheduler, RNG state, history

### Final Model
- `figures/exp1_trained_model_seed{0,1,2}.pt`

### Manifest
- `results/exp1_induction_heads.json` (multi-seed, written by `--seeds`)

### Figures (at final epoch, seed 0)
- `figures/exp1_training_bump.png` — loss/accuracy/entropy/diag1 curves
- `figures/exp1_induction_pattern_L{L}H{H}.png` — attention patterns for detected heads
- `figures/exp1_k_composition.png` — two-step diagnostic (Step 1 + Step 2)
- `figures/exp1_composition_diagnostic.png` — visual Step 1/2 overlay

### Console Log (per seed)
```
Step 1 — L0 duplicate-token head: max diag+1 mass 0.XX (peakedness 0.XX)
Step 2 — K-composition: best score 0.XX (L0 head X, L1 head Y)
Total induction heads: N / 8
Ablation L{L}H{H}: accuracy 0.XXXX → 0.XXXX (drop: +0.XXXX)
```

## Falsification Criteria

The hypothesis **"fresh-batches at standard scale produces induction heads"** is **falsified** if at 10k epochs:

- All 3 seeds: 0/8 induction heads detected (diag1_mass < 0.3 for all heads)
- All 3 seeds: `step2_k_composition` < 0.3 (K-composition never crosses threshold)
- Val accuracy plateaus below 0.3 (no generalization beyond memorization)

If falsified: document the boundary (scale, data, compute) where induction heads *don't* emerge. This is a valid scientific contribution — the emergence boundary is itself a result.

## Success Criteria

At least 1 seed produces:
- ≥1 induction head detected (diag1_mass > 0.3)
- `step2_k_composition` > 0.3 for some (L0, L1) pair
- Ablation drop > 0.05 on that head

If only 1/3 seeds succeeds: report seed variance honestly. The manifest captures per-seed spread.

## Downstream Dependencies

This run unblocks:
- **Rung 4 (Circuit Patching)**: Needs a checkpoint with confirmed head for activation/path patching validation
- **Rung 5 (SAE Real Activations)**: Needs `--activations-from` a head checkpoint to test if sparsity improves
- **Teaching Artifact**: Needs a real head checkpoint for the "induction heads exist" demo

## Timeline

| Session | Activity |
|---------|----------|
| S2 | Launch 3-seed run (background, ~20h CPU) |
| S3 | Monitor: check 2k/4k epoch checkpoints for Step 1 formation |
| S4 | Clean-clone proof (parallel) |
| S5 | If heads detected: launch SAE run (Row 5) |
| S6 | Teaching artifact recording |
| S7 | Paper/annex decision |
| S8 | Release |

## Resource Estimate

- **CPU time**: ~20 hours per seed × 3 seeds = ~60 CPU-hours (can run parallel on 12 threads)
- **Disk**: ~20 checkpoints × 3 seeds × ~5 MB = ~300 MB
- **Wall clock**: ~20 hours (parallel) to ~60 hours (sequential)

## Notes

- The `--standard` flag implies `--fresh-batches`, `--checkpoint-every 250`, `--save-model`, `--save-manifest`
- Checkpointing uses shared `src/experiments/checkpointing.py` with RNG continuity (bit-identical resume verified by tests)
- Multi-seed manifest format matches `exp2_grokking.json` schema for `verify-claims` compatibility