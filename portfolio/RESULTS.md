---
tags: [portfolio, results]
---

# Results — Headline Findings

> **Thesis**: I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns — grokking modular addition with Fourier decomposition, induction heads, circuit verification via activation patching, and sparse autoencoder feature extraction.

---

## Rung 2 — Grokking Modular Addition ★ (Primary Flagship)

**Question**: Can I reproduce the grokking phase transition on modular addition (a+b mod P) and reverse-engineer the discrete Fourier transform algorithm the model learns?

**Status**: [ ] Planned

| Metric | Value |
|--------|-------|
| Modulus P | 113 |
| Train fraction | ~30% |
| Generalization step | — |
| Fourier frequencies used | — |
| Ablation: removing key frequencies → | — |
| Ablation: removing ~95% of frequencies → | — |

*Reference: Nanda et al., "Progress Measures for Grokking via Mechanistic Interpretability," ICLR 2023 (oral). Target: reproduce the three-phase dynamic (memorization → circuit formation → cleanup) and confirm the Fourier algorithm via frequency ablation.*

---

## Rung 1 — Induction Heads (Fallback Flagship)

**Question**: Do induction heads emerge in a 2-layer attention-only transformer trained on repeated tokens?

**Status**: [ ] Planned

| Metric | Value |
|--------|-------|
| Layers | 2 |
| Heads per layer | — |
| Induction heads identified | — |
| Ablation: removing induction heads → | — |

*Reference: Olsson, Elhage, Nanda et al., "In-context Learning and Induction Heads," Transformer Circuits Thread (Anthropic), 2022.*

---

## Rung 3 — Toy Models of Superposition

**Question**: How do features organize in a toy ReLU autoencoder under varying sparsity, and can I observe the phase change from monosemantic to superposed features?

**Status**: [ ] Planned

| Sparsity | Feature Dimension | Active Features | Geometry |
|----------|-------------------|-----------------|----------|
| — | — | — | — |

*Reference: Elhage et al., "Toy Models of Superposition," Transformer Circuits Thread (Anthropic), 2022.*

---

## Rung 4 — Circuit Verification via Activation Patching

**Question**: Can I find and causally validate a specific circuit (IOI or task-specific) via activation/path patching, and measure its faithfulness and minimality?

**Status**: [ ] Planned

| Component | Logit Diff Recovery | Faithfulness |
|-----------|--------------------|--------------|
| — | — | — |

*Reference: Wang et al., "Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small," ICLR 2023.*

---

## Rung 5 — Sparse Autoencoder Feature Dashboard

**Question**: Can I train an SAE on the capstone model's residual stream and produce a browsable dashboard of interpretable monosemantic features?

**Status**: [ ] Planned

| Metric | Value |
|--------|-------|
| Dictionary size | — |
| L0 sparsity | — |
| Loss recovered | — |
| Dead features | — / — (—%) |

*Reference: Bricken et al., "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning," Transformer Circuits Thread (Anthropic), 2023.*

---

## Rung 6 — Automated vs. Hand-Found Circuit (Stretch)

**Question**: How does automated circuit discovery (ACDC) compare against a hand-found circuit (Rung 4) — in edge recovery, runtime, and faithfulness?

**Status**: [ ] Stretch

| Method | Edges Selected | Recovery vs. Manual | Runtime |
|--------|---------------|---------------------|---------|
| Manual (Rung 4) | — | — | — |
| ACDC | — | — | — |

*Reference: Conmy et al., "Towards Automated Circuit Discovery for Mechanistic Interpretability," NeurIPS 2023 (spotlight).*
