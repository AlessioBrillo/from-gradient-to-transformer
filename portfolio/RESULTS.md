---
tags: [portfolio, results]
---

# Results — Headline Findings

> **Thesis**: I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns — grokking modular addition with Fourier decomposition, induction heads, circuit verification via activation patching, and sparse autoencoder feature extraction.

All experiments are implemented in `src/experiments/` and produce figures in `figures/`. Each has a `--quick` mode for fast smoke tests.

---

## Rung 1 — Induction Heads (Primary Flagship)

**Question**: Do induction heads emerge in a 2-layer attention-only transformer trained on repeated tokens? Can we detect, verify, and ablate them?

**Status**: [x] Complete — code runs, heads detected, causal ablation validated

| Metric | Standard | Quick |
|--------|----------|-------|
| Layers / Heads | 2 / 4 | 2 / 2 |
| d_model | 64 | 32 |
| Epochs | 5000 | 500 |
| Train samples | 8192 | 1024 |
| Attention metrics | Entropy + Diag+1 mass | Same |
| Val accuracy (quick) | — | ~0.55 |
| Induction heads detected | Yes (at >0.3 threshold) | Yes (diag+1 ≈ 0.95+ by epoch 50) |

**Features**: attention entropy tracking, diagonal+1 induction signal plotted, W&B logging (`--wandb`), model saving (`--save-model`), loss bump detection, 2×2 training curves plot with attention metrics.

**Reference**: Olsson et al., "In-context Learning and Induction Heads," Transformer Circuits Thread (Anthropic), 2022.

**Figures**: `figures/exp1_training_bump.png`

---

## Rung 2 — Grokking Modular Addition

**Question**: Can I reproduce the grokking phase transition on modular addition (a+b mod P) and reverse-engineer the discrete Fourier transform algorithm the model learns?

**Status**: [~] Code fixed and committed — needs GPU-hours for P=113 training

| Metric | Quick Test (P=29) | Full Run (P=113) |
|--------|-------------------|-------------------|
| Modulus P | 29 | 113 |
| Train fraction | 30% | 30% |
| Epochs | 1000 | 5000+ |
| Key finding | P=29 has only 8/29 target values at 30% split — too few for DFT generalization | P=113 is correct but needs ~5.5h on CPU |

**Improvements committed**: unembed normalization, weight decay parameter groups (embed/LN/pos_embed excluded), per-row embed norm tracking, progress measures plot, `--diagnose` flag.

**Bottleneck**: CPU-only environment. P=113 at 5000 epochs requires GPU-hours. Per research plan fallback: induction heads is primary flagship if grokking does not reproduce cleanly on CPU.

**Reference**: Nanda et al., "Progress Measures for Grokking via Mechanistic Interpretability," ICLR 2023 (oral).

**Figures**: `figures/exp2_grokking_curve.png`, `figures/exp2_fourier_weights.png`, `figures/exp2_frequency_ablation.png`

---

## Rung 3 — Toy Models of Superposition

**Question**: How do features organize in a toy ReLU autoencoder under varying sparsity?

**Status**: [x] Complete — experiments run, phase change observed

**Reference**: Elhage et al., "Toy Models of Superposition," Transformer Circuits Thread (Anthropic), 2022.

**Figures**: `figures/exp3_feature_geometry.png`, `figures/exp3_phase_change.png`

---

## Rung 4 — Circuit Verification via Activation Patching

**Question**: Can I find and causally validate a specific circuit via activation patching and head ablation?

**Status**: [x] Complete — real activation patching implemented on induction heads

**Method**: Train DecoderOnlyTransformer on repeated-token prediction (same task as Rung 1), detect induction heads via diagonal+1 attention mass, then:
1. **Residual stream activation patching**: patch `resid_mid` from corrupted → clean via MLP pre-forward hooks per (layer, position). Measures logit-diff recovery.
2. **Head-level zero ablation**: suppress individual induction heads via Attention forward hooks and measure logit-diff drop.

| Component | Logit-diff recovery |
|-----------|--------------------|
| Layer 1, last position | 0.787 (strong) |
| Layer 0, last position | 0.270 (moderate) |
| Layer 0, mid positions | <0.20 (weak) |

**Outputs**: `figures/exp4_attention_patterns.png`, `figures/exp4_patching_results.png`, `figures/exp4_head_ablation.png`

**Reference**: Wang et al., "Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small," ICLR 2023.

---

## Rung 5 — Sparse Autoencoder Feature Dashboard

**Question**: Can I train an SAE on synthetic residual stream activations and extract interpretable features?

**Status**: [x] Complete — SAE trains on synthetic data, ready to upgrade to real activations

| Metric | Value |
|--------|-------|
| Dictionary size (d_model=64) | 512 (8×) |
| L0 sparsity | 88.97 / 512 (17.4%) |
| Fraction of variance explained (FVE) | 0.9722 (97.2%) |
| Reconstruction MSE | 0.00113 |
| Dead features | 1 / 512 (0.2%) |

**Next**: Upgrade to real activations from trained induction heads model.

**Reference**: Bricken et al., "Towards Monosemanticity" (2023); Cunningham et al., "Sparse Autoencoders Find Highly Interpretable Features in Language Models," ICLR 2024.

**Figures**: `figures/exp5_sparsity_tradeoff.png`, `figures/exp5_feature_histogram.png`

---

## Rung 6 — Automated vs. Hand-Found Circuit (Stretch)

**Question**: How does automated circuit discovery (ACDC) compare against a hand-found circuit?

**Status**: [~] Simulated — placeholder (stretch goal)

**Reference**: Conmy et al., "Towards Automated Circuit Discovery for Mechanistic Interpretability," NeurIPS 2023 (spotlight).

---

## Phase Gate Progress

| Phase | Status | Gate proof |
|-------|--------|------------|
| 1 — Foundations | ✅ Complete | — |
| 2 — Classical ML | ✅ Complete | complete-ml-pipeline |
| 3 — Deep Learning | ✅ Complete | gradient-flow-and-architectures |
| 4 — NLP & Transformers | ✅ Complete | circuit-analysis-complete |
| 5 — LLM Engineering | [~] Instrumentation done | — |
| 6 — Production AI | [ ] Not started | — |
| 7 — Capstone | [~] Research plan written | — |

## Summary

| Rung | Status | Key Result |
|------|--------|------------|
| 1 — Induction Heads ★ | ✅ Complete | Heads detected, causal ablation, attention metrics tracked |
| 2 — Grokking | ⏳ CPU-bound | Fixes committed, needs GPU to finish |
| 3 — Superposition | ✅ Complete | Phase change observed |
| 4 — Circuit Patching | ✅ Complete | Activation patching + head ablation on induction heads |
| 5 — SAE Dashboard | ✅ Synthetic | 97.2% FVE, ready for real activations |
| 6 — ACDC | 🛠 Placeholder | Stretch goal |

All experiments runnable with `python -m src.experiments.expN_* --quick`.
