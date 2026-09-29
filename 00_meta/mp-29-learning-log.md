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

### 2026-09-30 — P=59 Positive Control
- [x] Launched single seed (epoch 2470/5000, val_acc=0.0033, dense)
- [ ] Launch remaining 2 seeds
- [ ] Observations: NO-GROK confirmed at P=59 on CPU

### 2026-10-01 — Microscope Trials & Phase Diagram
- [ ] Trial 2 (constant LR, P=113) - skip, CPU won't grok
- [ ] Trial 3 (WD=1.5, P=113) - skip, CPU won't grok
- [x] Phase diagram sweep: run reduced scope (key cells only) to map dense regime
- [ ] Document dense algorithm characterization

### 2026-10-XX — GPU Flagship & Analysis
- [ ] Launch P=113 3-seed runs on Colab (GPU)
- [ ] Launch induction heads standard-scale on CPU (fresh batches)
- [ ] Analyze phase diagram results
- [ ] Write paper sections

## Key Insights (Accumulated)
- NO-GROK on CPU is not a bug — it's a reproducible regime (dense attractor)
- The embedding renormalization + cosine LR + weight decay protocol on CPU converges to a dense, memorizing solution
- Nanda et al. results require GPU (or at least different numerics)
- The phase diagram on CPU will show the boundary of the dense basin, not the sparse regime

## Open Questions
- #question What specific GPU numerical property enables sparse Fourier? (float16? cuDNN? different initialization?)
- #question Can we simulate GPU-like dynamics on CPU (e.g., gradient noise injection)?
- #question Is the dense solution at P=59 the same algorithm as at P=113? (ablation suggests yes — both need all frequencies)