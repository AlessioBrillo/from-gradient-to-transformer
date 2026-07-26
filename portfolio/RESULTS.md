---
tags: [portfolio, results]
---

# Results — Headline Findings

> **Thesis**: I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns — grokking modular addition with Fourier decomposition, induction heads, circuit verification via activation patching, and sparse autoencoder feature extraction.

All experiments are implemented in `src/experiments/` and produce figures in `figures/`. Each has a `--quick` mode for fast smoke tests.

---

## Reproducibility Audit — 2026-07-26

`figures/` did not exist prior to this audit despite being referenced throughout this document
and `00_meta/00_home.md`. This session installed the minimal runtime deps (torch-cpu, numpy,
matplotlib, tqdm — none of the experiment scripts actually import transformer-lens/sae-lens
despite them being in `pyproject.toml`) and ran every rung's `--quick` mode on CPU to generate
real figures and cross-check the numbers already documented above. Findings:

- **Grokking (Rung 2): found and fixed a real bug**, not just a compute bottleneck — see Rung 2
  section. The train/val split made some target classes unreachable during training,
  guaranteeing 0% val accuracy regardless of GPU-hours spent. Fixed; full P=113 run still
  pending (needs GPU — see `notebooks/colab_grokking_full_run.ipynb`).
- **Induction heads (Rungs 1 & 4): quick-mode detects 0 heads** despite diagonal+1 attention
  mass near 1.0, contradicting the "Yes, detected" / "heads detected" claims in the
  standard-scale rows. Not yet root-caused — could be a real threshold/scale sensitivity (heads
  only sharpen enough at standard scale) or a bug in the detection function. Flagged as an open
  item; the standard-scale numbers are unconfirmed until re-run.
- **Superposition (Rung 3): completed a 2000-epoch/10k-sample sweep (default 5000×50k is too
  slow for CPU) and found no phase transition** — feature recovery stayed flat/near-zero (0.00–
  0.15) across the entire sparsity range instead of rising at the sparsest settings. Not
  root-caused; needs investigation before the "Complete" status can be trusted.
- **SAE (Rung 5): reproduced exactly** (97.2% FVE, 88.96/512 L0, 0.2% dead features) — this rung
  is genuinely reproducible, on synthetic data as already documented.
- **ACDC (Rung 6): confirmed simulated/placeholder**, exactly as labeled — no discrepancy.

Net effect: one root-cause bug fixed (grokking split), one open discrepancy flagged (induction
head detection at quick scale), figures now exist for every rung, and the two "Primary Flagship"
labels that previously pointed at different rungs are reconciled below.

---

## Rung 1 — Induction Heads (Fallback Flagship, currently the strongest verified result)

**Question**: Do induction heads emerge in a 2-layer attention-only transformer trained on repeated tokens? Can we detect, verify, and ablate them?

**Status**: [x] Complete at standard scale (below) — **but a 2026-07-26 CPU re-run in `--quick` mode
detected 0 induction heads** despite near-1.0 diagonal+1 attention mass (see Reproducibility
Audit). The standard-scale numbers below have not been re-verified in this session; treat them
as unconfirmed until re-run and cross-checked against the quick-mode discrepancy.

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

## Rung 2 — Grokking Modular Addition (Primary Flagship — NOT YET VERIFIED)

**Question**: Can I reproduce the grokking phase transition on modular addition (a+b mod P) and reverse-engineer the discrete Fourier transform algorithm the model learns?

**Status**: [ ] Not reproduced. A real bug was found and fixed on 2026-07-26 (see Reproducibility
Audit); the full P=113 run still needs to be executed on a GPU before this rung can be marked
complete. Do not treat this as the headline result until that run exists.

| Metric | Quick Test (P=29) | Full Run (P=113) |
|--------|-------------------|-------------------|
| Modulus P | 29 | 113 |
| Train fraction | 30% | 30% |
| Epochs | 1000 | 5000+ |
| Key finding | P=29 has only 8/29 target values at 30% split — too few for DFT generalization | P=113 is correct but needs ~5.5h on CPU |

**Improvements committed**: unembed normalization, weight decay parameter groups (embed/LN/pos_embed excluded), per-row embed norm tracking, progress measures plot, `--diagnose` flag.

**Bug fixed 2026-07-26**: `make_modular_addition_data` split train/val by **target class**
(`(a+b) % P`) instead of by **equation** `(a, b)`. This left some output classes with zero
training signal — the model was asked to predict classes its unembedding row never saw, which
is not generalization, it's an unsolvable task. This produced exactly 0% validation accuracy
even at trivial P=11 with no compute constraint, independent of the CPU/GPU bottleneck below.
Fixed to hold out random `(a, b)` pairs, matching the canonical Power et al. / Nanda et al.
setup where every target class appears in both splits. Test `test_split_disjoint` (which
encoded the bug as a requirement) was replaced with `test_pairs_disjoint` +
`test_target_classes_shared_across_splits`.

**Bottleneck**: CPU-only environment. Even after the split fix, a P=11 micro-scale CPU run
(5000 epochs) shows clean memorization (train loss → 0.0001) but **no grokking transition**
(val acc stays 0.0000 throughout) — consistent with the roadmap's own note that small P lacks
the combinatorial diversity for the Fourier algorithm to emerge. The full P=113 run is required
and needs GPU-hours; see `notebooks/colab_grokking_full_run.ipynb` for a ready-to-run Colab
notebook (free T4, a few minutes) that applies the split fix and produces the real figures.
Per research plan fallback: induction heads remains the strongest *verified* result until this
run is done.

**Reference**: Nanda et al., "Progress Measures for Grokking via Mechanistic Interpretability," ICLR 2023 (oral).

**Figures**: `figures/exp2_grokking_curve.png`, `figures/exp2_fourier_weights.png`, `figures/exp2_frequency_ablation.png`

---

## Rung 3 — Toy Models of Superposition

**Question**: How do features organize in a toy ReLU autoencoder under varying sparsity?

**Status**: [ ] Not reproduced. A completed sweep on 2026-07-26 (2000 epochs, 10k samples — the
default 5000×50k sweep is too slow for CPU, hours) found **no phase transition**: feature
recovery stayed flat and low (0.00–0.15) across the entire sparsity range, with no increase at
the sparsest settings as the canonical result predicts.

| Sparsity | Feature recovery | Monosemantic rate | Mean \|corr\| |
|----------|-------------------|--------------------|--------------|
| 0.500 | 0.050 | 0.100 | 0.282 |
| 0.200 | 0.100 | 0.100 | 0.316 |
| 0.100 | 0.150 | 0.150 | 0.302 |
| 0.050 | 0.100 | 0.100 | 0.345 |
| 0.020 | 0.050 | 0.050 | 0.305 |
| 0.010 | 0.100 | 0.100 | 0.311 |
| 0.005 | 0.050 | 0.050 | 0.305 |
| 0.002 | 0.000 | 0.000 | 0.324 |
| 0.001 | 0.000 | 0.000 | 0.341 |

Expected (Elhage et al.): recovery should rise toward monosemantic (→1.0) as sparsity decreases
(features rarely active). Observed: no such trend — recovery is noise-flat and drops to zero at
the sparsest settings, the opposite direction. Not yet root-caused; candidates are insufficient
epochs even at 2000, the `feature_recovery_rate` metric/threshold definition, or the
`n_features=20` / `n_dimensions=5` ratio. Needs investigation before this rung can be marked
complete — do not cite the phase-change figure as a verified result.

**Reference**: Elhage et al., "Toy Models of Superposition," Transformer Circuits Thread (Anthropic), 2022.

**Figures**: `figures/exp3_feature_geometry.png`, `figures/exp3_phase_change.png`

---

## Rung 4 — Circuit Verification via Activation Patching

**Question**: Can I find and causally validate a specific circuit via activation patching and head ablation?

**Status**: [x] Complete at standard scale (below) — activation patching mechanism itself works
and re-ran clean in `--quick` mode on 2026-07-26, but quick-mode also hit 0 induction heads
detected (same detection discrepancy as Rung 1), so head ablation was skipped in that run. The
patching numbers below are from the documented standard-scale run and were not re-verified at
that scale in this session.

**Method**: Train DecoderOnlyTransformer on repeated-token prediction (same task as Rung 1), detect induction heads via diagonal+1 attention mass, then:
1. **Residual stream activation patching**: patch `resid_mid` from corrupted → clean via MLP pre-forward hooks per (layer, position). Measures logit-diff recovery.
2. **Head-level zero ablation**: suppress individual induction heads via Attention forward hooks and measure logit-diff drop.

| Component | Logit-diff recovery |
|-----------|--------------------|
| Layer 1, last position | 0.787 (strong) — standard scale, unconfirmed this session |
| Layer 0, last position | 0.270 (moderate) — standard scale, unconfirmed this session |
| Layer 0, mid positions | <0.20 (weak) — standard scale, unconfirmed this session |
| Layer 0, Pos 5 (quick mode, 2026-07-26) | 0.447 (best of quick run; no heads detected → ablation skipped) |

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
| 1 — Induction Heads (fallback flagship) | ⚠️ Standard-scale claim unconfirmed | Quick-mode re-run 2026-07-26: 0 heads detected despite near-1.0 diag+1 mass — open discrepancy |
| 2 — Grokking (primary flagship) | ⏳ Not yet reproduced | Real data-split bug found + fixed 2026-07-26; still needs the GPU run in `notebooks/colab_grokking_full_run.ipynb` |
| 3 — Superposition | ⏳ Not reproduced | Completed 2000-epoch sweep shows no phase transition — recovery flat/near-zero across all sparsity levels |
| 4 — Circuit Patching | ⚠️ Standard-scale claim unconfirmed | Quick-mode re-run: patching works (0.447 recovery) but same 0-heads discrepancy as Rung 1 |
| 5 — SAE Dashboard | ✅ Reproduced | 97.2% FVE, on synthetic data (not yet real activations) |
| 6 — ACDC | 🛠 Placeholder | Confirmed simulated, as labeled |

All experiments runnable with `python -m src.experiments.expN_* --quick`. See "Reproducibility
Audit — 2026-07-26" above for what was actually re-verified in this session vs. what remains an
unconfirmed historical claim.
