---
title: "Rung 2: Grokking Modular Addition"
description: "Train 1-layer transformer on modular addition and reverse-engineer the learned algorithm via Fourier analysis"
tags: [grokking, modular-addition, fourier-analysis, mechanistic-interpretability]
phase: 1
rung: 2
---

**Problem**: Train a 1-layer transformer on modular addition (a + b mod P) and observe delayed generalization (grokking). Reverse-engineer the learned algorithm via Fourier decomposition of embeddings: the model implements addition via discrete Fourier transforms and trigonometric identities.

**Methodology**:
- Train 1-layer transformer on modular addition with P=113, 30% train fraction
- Observe grokking: validation loss drops sharply after extended training
- Fourier decomposition of token embeddings reveals sparse frequency structure
- Frequency ablation confirms mechanism: ablating key frequencies destroys generalization

**Key Result**:
<!-- manifest: results/exp2_grokking.json -->
P=113 CPU 3-seed run: NO-GROK (val accuracy ~1.0, k₉₉ = 111/113). Dense Fourier solution at all 3 seeds.
GPU 3-seed run launched on Colab 2026-08-24 — verdict pending.
Neuron ablation on dense solution shows graceful degradation (distributed linear map, not sparse DFT).

**Figures**:
![Grokking Curve](figures/exp2_grokking_curve.png) <!-- manifest: results/exp2_grokking.json -->
![Fourier Weights](figures/exp2_fourier_weights.png) <!-- manifest: results/exp2_grokking.json -->
![Frequency Ablation](figures/exp2_frequency_ablation.png) <!-- manifest: results/exp2_grokking.json -->
![Neuron Ablation](figures/exp2_neuron_ablation.png) <!-- manifest: results/exp2_grokking.json -->

**Notebook**: `notebooks/exp2_grokking_demo.ipynb`

**Limitations**:
- No sparse Fourier solution ever produced in this repo's history (P=59, P=113 CPU)
- GPU run verdict pending — may produce sparse or dense solution
- Dense solution mechanism: distributed linear map in embedding space, not sparse DFT
- Small model (1-layer, d_model=128) — larger models may behave differently

**Next Steps**:
- Await GPU run verdict (MP-74 Sessions 2-3)
- Characterize dense attractor mathematically (Varma et al. 2023 circuit efficiency)
- Test at larger scales and different architectures