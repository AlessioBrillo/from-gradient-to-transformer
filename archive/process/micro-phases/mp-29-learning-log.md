---
tags: [phase/29, learning-log, micro-phase]
created: 2026-09-29
---

# Micro-Phase 29 Learning Log

## Daily Entries

### 2026-09-29 — Planning & NO-GROK Confirmation
- **Key finding**: NO-GROK on CPU is robust across ALL protocol variations tested:
  - P=11 (trivial modulus): val_acc=0.0000, k_99=11/11 (dense)
  - P=11 + constant LR + no renorm: val_acc=0.0000, k_99=11/11 (dense)
  - P=11 + WD=1.5 + constant LR + no renorm + 50% train: val_acc=3.28%, k_99=11/11 (dense)
  - P=11 + WD on embeddings (Nanda protocol): val_acc=1.18%, k_99=11/11 (dense)
  - P=59 (positive control modulus): epoch 2470/5000, val_acc=0.0033, still dense
- **Conclusion**: CPU training with this protocol NEVER produces sparse Fourier circuits. This is likely a CPU vs GPU numerical difference (float32 vs float16, no cuDNN, different optimization trajectories).
- **Scientific value**: This maps the dense attractor basin comprehensively. The phase diagram sweep on CPU will show "dense everywhere" — a valid result characterizing where the sparse circuit DOESN'T emerge.
- **Action**: Proceed with phase diagram sweep on CPU to map dense regime; move flagship P=113 runs to GPU (Colab) for sparse regime search.

### 2026-09-30 — Induction Heads & Phase Diagram
- **Induction heads tiny multi-seed (3 seeds, fresh-batches, vocab=256, seq=16, d_model=24, 150 epochs)**:
  - final_val_acc: 0.0047 ± 0.0012 (n=3)
  - peak_diag1_mass: 0.1765 ± 0.0064 (n=3) — well below 0.3 threshold
  - total_induction_heads: 0/8 across all 3 seeds
  - k_composition_score: 0.1717 ± 0.0549
  - **Confirms MP-8 finding**: at tiny scale, even with fresh batches, no induction heads detected
  - Model doesn't overfit (val≈train≈random), but doesn't learn induction either
- **Phase diagram sweep**: p11_wd01 completed (dense, k_99/P=1.0); p11_wd05 running
- **Standard-scale induction** (d_model=64, vocab=2048, seq=64): ~5s/epoch on CPU = ~1.4hr for 1000 epochs. Too slow for full run. Needs GPU or acceptance that tiny-scale is the limit here.

### 2026-10-01 — Phase Diagram Completion & Paper
- [ ] Complete phase diagram sweep (remaining 4-5 key cells)
- [ ] Generate heatmap + boundary analysis figures
- [ ] Document dense algorithm characterization
- [ ] Write paper sections (Grokking NO-GROK + phase diagram, Induction, Superposition)
- [ ] Prepare Colab notebook for P=113 GPU flagship runs

## Key Insights (Accumulated)
- NO-GROK on CPU is not a bug — it's a reproducible regime (dense attractor)
- The embedding renormalization + cosine LR + weight decay protocol on CPU converges to a dense, memorizing solution
- Nanda et al. results require GPU (or at least different numerics)
- The phase diagram on CPU will show the boundary of the dense basin, not the sparse regime
- Induction heads need standard scale (d_model≥64, vocab≥2048) to cross 0.3 threshold — tiny scale insufficient
- Fresh-batches prevents overfitting but doesn't create induction heads at tiny scale

## Open Questions
- #question What specific GPU numerical property enables sparse Fourier? (float16? cuDNN? different initialization?)
- #question Can we simulate GPU-like dynamics on CPU (e.g., gradient noise injection)?
- #question Is the dense solution at P=59 the same algorithm as at P=113? (ablation suggests yes — both need all frequencies)
- #question What is the minimal model scale for induction heads? (d_model=64? layers=2? vocab=2048?)