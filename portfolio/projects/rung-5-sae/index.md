---
title: "Rung 5: SAE Feature Dashboard"
description: "Sparse Autoencoder feature extraction and interactive browser for real model activations"
tags: [sae, sparse-autoencoder, feature-extraction, mechanistic-interpretability]
phase: 1
rung: 5
---

**Problem**: Extract interpretable features from trained transformer activations using Sparse Autoencoders (SAEs). Build interactive dashboard for feature exploration.

**Methodology**:
- Train SAE on activations from trained models (synthetic + real)
- Harvest activations from `ln_final` hook (residual stream)
- SAE architecture: encoder → ReLU → decoder with unit norm constraint
- Metrics: Fraction of Variance Explained (FVE), L0 sparsity, dead features
- Export to Hugging Face Spaces for interactive browser

**Key Result**:
<!-- manifest: results/exp5_sae_dashboard.json -->
SAE achieves 99.97% FVE but only 17% sparsity (L0=136/256) on real activations vs 97.5% FVE at 18% sparsity on synthetic. Sparsity gap indicates real model (undertrained, no confirmed heads) has no genuinely sparse features yet.

**Figures**:
![SAE Training](figures/exp5_sae_training.png) <!-- manifest: results/exp5_sae_dashboard.json -->
![Feature Analysis](figures/exp5_feature_analysis.png) <!-- manifest: results/exp5_sae_dashboard.json -->
![FVE vs L0](figures/exp5_fve_l0_tradeoff.png) <!-- manifest: results/exp5_sae_dashboard.json -->

**Notebook**: `notebooks/exp5_sae_dashboard_demo.ipynb`

**Limitations**:
- Sparsity gap: real model activations not sparse (L0=136 vs expected 20-30)
- Gated on Rung 1 producing confirmed induction heads for real checkpoint
- Synthetic baseline shows SAE *can* find sparse features when they exist
- Dictionary size (256) may be too small for real model capacity

**Next Steps**:
- SAE on first confirmed head checkpoint (MP-74 R5, gated on R2)
- SAE on capstone model at multiple checkpoints (MP-78)
- Deploy interactive browser to HF Spaces (MP-78 Row 4)
- Scaling: larger dictionary (1024+), more training steps