---
title: "Rung 3: Superposition & Feature Geometry"
description: "Train toy autoencoders to study superposition — how models represent more features than dimensions"
tags: [superposition, autoencoder, feature-geometry, mechanistic-interpretability]
phase: 1
rung: 3
---

# Rung 3: Superposition & Feature Geometry

**Problem**: Study superposition — how neural networks represent more features than they have dimensions. Train sparse autoencoders on synthetic data with known ground-truth feature geometry to validate interpretability methods.

**Methodology**:
- Generate synthetic data with sparse features (varying sparsity, importance decay)
- Train toy autoencoders with bottleneck dimensionality
- Measure feature recovery: dimensionality, angular separation (pentagon geometry)
- Falsification tests: dense regime drops features, sparse regime represents all

**Key Result**:
<!-- manifest: results/exp3_superposition.json -->
Regular pentagon geometry (gaps 70.2°–73.8°, std ≤1.4° vs ideal 72°) is the sparse-phase attractor attained at sparsity ≤0.1. Dense regime (sparsity ≥0.2) sits off-pentagon with 4/5 features. Phase transition is dropout *within* the geometry.

**Figure**:
![Pentagon Geometry](figures/exp3_pentagon_geometry.png) <!-- manifest: results/exp3_superposition.json -->

**Notebook**: `notebooks/exp3_superposition_demo.ipynb`

**Limitations**:
- Synthetic data only — no real model activations yet
- Capacity limit at extreme sparsity (0.001): 14–16/20 features represented
- Pentagon geometry is a property of the *sparse phase*, not universal
- SAE on real activations shows sparsity gap (17% L0 vs 97.5% on synthetic)

**Next Steps**:
- SAE on real activations from confirmed induction head checkpoint (Rung 5)
- SAE on capstone model activations (MP-78)
- Scaling laws for dictionary size vs. feature recovery