---
title: "Rung 5: SAE Feature Dashboard"
description: "Sparse Autoencoder feature extraction and interactive browser for real model activations"
tags: [sae, sparse-autoencoder, feature-extraction, mechanistic-interpretability]
phase: 1
rung: 5
---

**Problem**: Extract interpretable features from trained transformer activations using Sparse Autoencoders (SAEs). Build an interactive dashboard for feature exploration.

**Methodology**:
- Train SAE on activations from trained models (synthetic + real)
- Harvest real activations from the `ln_final` hook (residual stream) via `--activations-from`
- SAE architecture: encoder + ReLU + decoder with pre-encoder bias (`x - b_dec`, Bricken et al.) and unit-norm constraint
- Metrics: Fraction of Variance Explained (FVE), L0 sparsity, dead features (fixed 1e-4 threshold)

**Key Result**:
<!-- manifest: results/exp5_sae_dashboard.json -->
<!-- manifest: results/exp5_real_activations.json -->
Synthetic baseline (manifest-backed): FVE 0.9749, L0 96.6/512, 39/512 dead. On the real residual stream of Rung 1's confirmed-head checkpoint (`results/exp5_real_activations.json`, re-measured 2026-11-17): FVE 0.99998, L0 19.0/512 (3.7% active), but 66% of the features never fire. The dictionary is sparse and about eight times wider than the 64-dimensional stream it covers: the size, not the sparsity, is the open question. An older run on an undertrained checkpoint read dense (53% active); that was a statement about the model, not the SAE.

**Figures**:
![Sparsity Tradeoff](../../figures/exp5_sparsity_tradeoff.png) <!-- manifest: results/exp5_sae_dashboard.json -->
![Feature Histogram](../../figures/exp5_feature_histogram.png) <!-- manifest: results/exp5_sae_dashboard.json -->
Real-activation figures struck: the numbers came from a run whose plots were never saved — struck rather than left dangling.

**Reproduce**: `uv run python -m src.experiments.exp5_sae_dashboard --quick` (smoke test, synthetic).

**Limitations**:
- Sparsity gap: real model activations not sparse (L0=136 vs expected 20–30)
- Gated on Rung 1 producing confirmed induction heads for a meaningful real checkpoint
- Dictionary size (256) may be too small for real model capacity

**Links**:
- [RESULTS](../../RESULTS.md) — my honesty ledger and per-rung numbers
- [research-plan](../../../07_capstone/research-plan.md) — where this rung sits in the experiment ladder
- [trees-ensembles-pca](../../../02_classical_ml/proofs/trees-ensembles-pca.md) — PCA as the conceptual ancestor of SAEs

**Next Steps**:
- SAE on first confirmed head checkpoint (gated on Rung 1)
- SAE on capstone model at multiple checkpoints
- Deploy interactive browser to HF Spaces (gated on a real head)
- Scaling: larger dictionary (1024+), more training steps
