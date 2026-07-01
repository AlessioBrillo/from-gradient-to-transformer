---
tags: [phase/7, capstone, research/experiment, plan]
---

# Research Plan — From Transformer to Circuit

## Thesis

> I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns. This repository demonstrates end-to-end research capability in mechanistic interpretability — training small models, forming causal hypotheses about their internals, and testing those hypotheses with activation patching, ablations, and sparse dictionary learning.

---

## Experiment Ladder

Ordered cheapest/highest-signal → more ambitious. Each is a defensible standalone result.

### Rung 1 — Induction Heads (safe-fallback flagship)

- **Scale/task:** 2-layer, attention-only, ~1–4 heads/layer, trained on repeated-random-token sequences.
- **Metric/visual:** per-token loss vs. context position; the induction attention pattern; prefix-matching + copying decomposition; the training-loss bump.
- **Compute:** minutes to a couple hours on one GPU.
- **Headline:** "Induction heads emerge and I show, causally (ablation/patching), that they implement [A][B]…[A]→[B]."
- **Reference:** Olsson, Elhage, Nanda et al., Transformer Circuits Thread (Anthropic), 2022.

### Rung 2 — Grokking on Modular Addition (PRIMARY FLAGSHIP ★)

- **Scale/task:** 1-layer transformer, d_model=128, 4 heads, d_mlp=512, ReLU; a+b mod 113; ~30% train fraction; AdamW lr 1e-3, high weight decay.
- **Metric/visual:** train/test loss showing delayed generalization (the grokking curve); Fourier decomposition of embeddings showing sparse key frequencies; ablations in Fourier space; three phases (memorization/circuit-formation/cleanup) via progress measures.
- **Compute:** ~minutes/GPU per seed.
- **Headline:** a complete scientific arc — train, observe emergence, reverse-engineer the exact algorithm, confirm by ablation.
- **Reference:** Nanda et al., *Progress Measures for Grokking via Mechanistic Interpretability*, ICLR 2023 (oral).

### Rung 3 — Toy Models of Superposition

- **Scale/task:** tiny ReLU autoencoder on synthetic sparse features; sweep sparsity.
- **Metric/visual:** feature-direction plots, phase change from monosemantic to superposed, dimensionality/"feature capacity."
- **Compute:** CPU-minutes to GPU-seconds.
- **Reference:** Elhage et al., *Toy Models of Superposition*, 2022.

### Rung 4 — Circuit Verification via Activation Patching

- **Scale/task:** from-scratch small GPT or GPT-2-small via TransformerLens on an IOI-style or simpler task.
- **Metric/visual:** logit-difference recovery under activation/path patching; attention-pattern atlas; hand-drawn circuit diagram with named head roles.
- **Compute:** hours; GPT-2-small inference is cheap.
- **Reference:** Wang et al., *Interpretability in the Wild: a Circuit for IOI in GPT-2 small*, ICLR 2023.

### Rung 5 — Sparse Autoencoder Feature Dashboard

- **Scale/task:** SAE (ReLU baseline → BatchTopK/JumpReLU) on activations from the capstone model or GPT-2-small, via SAELens.
- **Metric/visual:** sparsity/reconstruction (L0 vs. loss-recovered) tradeoff curve; dead-feature rate; feature dashboard via sae-vis; optionally pushed to Neuronpedia.
- **Compute:** moderate — activation harvesting + SAE training over a few hours to a day on one GPU.
- **Reference:** Bricken et al., *Towards Monosemanticity*, 2023; Cunningham et al., ICLR 2024.

### Rung 6 (Stretch) — Automated vs. Hand-Found Circuit Comparison

- **Scale/task:** run ACDC or attribution patching on the Rung 4 task and compare recovered subgraph to manual circuit.
- **Metric:** edge-recovery vs. ground truth; runtime comparison; where automation fails.
- **Reference:** Conmy et al., *Towards Automated Circuit Discovery for Mechanistic Interpretability*, NeurIPS 2023.

---

## Flagship Strategy

**Primary:** Rung 2 (grokking). **Committed fallback:** Rung 1 (induction heads). **Frontier capstone:** Rung 5 (SAE dashboard).

If grokking does not reproduce cleanly within ~2 weeks of honest effort (seed/weight-decay sensitivity), induction heads becomes the headline and grokking moves to "additional results."

---

## Canonical Literature Map

### Foundations — Circuits Worldview
- **Olah et al., "Zoom In: An Introduction to Circuits."** *Distill*, 2020. Founding manifesto: features, circuits, universality.
- **Elhage et al., "A Mathematical Framework for Transformer Circuits."** Anthropic, Dec 2021. QK/OV decomposition, residual stream, virtual weights, composition.
- **Elhage et al., "Toy Models of Superposition."** Anthropic, Sept 2022. Why networks pack more features than neurons; phase changes.
- **Olsson et al., "In-context Learning and Induction Heads."** Anthropic, 2022. Induction heads as the mechanism behind in-context learning.

### Circuit Discovery
- **Wang et al., "Interpretability in the Wild: a Circuit for IOI in GPT-2 small."** ICLR 2023. Canonical hand-found circuit: 26 heads in 7 classes.
- **Nanda et al., "Progress Measures for Grokking via Mechanistic Interpretability."** ICLR 2023 (oral). **Flagship anchor.**
- **Conmy et al., "Towards Automated Circuit Discovery for Mechanistic Interpretability."** NeurIPS 2023 (spotlight).

### Sparse Autoencoders
- **Bricken et al., "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning."** Anthropic, Oct 2023.
- **Cunningham et al., "Sparse Autoencoders Find Highly Interpretable Features in Language Models."** ICLR 2024.
- **Templeton et al., "Scaling Monosemanticity."** Anthropic, 2024. (Aspirational context.)
- **SAE variants:** Gated SAEs, JumpReLU SAEs (DeepMind 2024), TopK SAEs (OpenAI 2024), BatchTopK (Bussmann et al., 2024).

### Causal Methodology
- **Activation patching / causal tracing** — Meng et al. (ROME), NeurIPS 2022.
- **Path patching** — Wang et al., 2022.
- **Attribution patching** — Nanda, 2023; AtP\* (Kramár et al., DeepMind 2024).
- **Causal Scrubbing** — Chan et al., Redwood Research, 2022.

---

## Tooling Stack

| Job | Tool |
|-----|------|
| Core MI | TransformerLens (HookedTransformer, hook points, caching, ActivationCache) |
| Alternative | nnsight/NDIF for remote execution on large models |
| SAEs | SAELens for training/loading; sae-vis for dashboards; Neuronpedia for hosting |
| Visualization | circuitsvis (attention), matplotlib (grokking/Fourier/superposition), logit lens |
| Reproducibility | uv + pyproject.toml pinned; global seed control + deterministic flags |
| Tracking | Weights & Biases (loss curves, progress measures) |
| CI | pytest (shape/gradient checks), ruff (lint), mypy (types) |
| Figures | Committed + regenerable via `make reproduce` |

**Anti-bloat rule:** one library per job; no dead dependencies; every notebook either becomes a tested module or is deleted. Pin model + dataset versions so results are byte-stable.

---

## Timeline (Part-Time, ~4–6 Months)

| Period | Focus | Deliverable | Gate |
|--------|-------|-------------|------|
| Weeks 1–4 | Foundations + tooling spine | ARENA Ch.0/1, from-scratch transformer, repro infra | Transformer trains + passes tests |
| Weeks 4–8 | **First flagship** | Grokking (Rung 2) reproduction; README with figure | If grokking fails in ~2w → fallback to induction heads |
| Weeks 8–14 | Circuit work | Rung 4 (activation patching on GPT-2-small); optionally Rung 3 | Circuit verified causally |
| Weeks 14–20 | SAE frontier showpiece | Rung 5 (SAE training + dashboard) | If dead features >50% → smaller dict + honest negative report |
| Weeks 20–24 | Mini-paper + demo | 4–8 page writeup with ablations; HF Space interactive demo | Paper + demo shipped |

---

## Distinctiveness Gate

Before publishing any rung, answer in one sentence: **"What did I add beyond the original?"**

If you cannot, add a small ablation/extension (different modulus, different seed distribution, improved visualization) or do not headline it. A bare reproduction is table stakes.

---

## Honest Caveats

- **Reproductions commonly fail or under-replicate.** Grokking is sensitive to weight decay, train fraction, and seed; induction-head emergence depends on architecture/data; SAEs suffer dead features and can learn illusory features.
- **Methods have known limits.** Attribution patching is a flawed linear approximation (bad for large activations like the residual stream); activation patching can mislead via the layernorm denominator and subspace illusions (Makelov, Lange & Nanda 2023); circuit faithfulness metrics "are not robust" (Heimersheim & Janiak 2024). Cite these explicitly — doing so is itself a PhD-level signal.
- **Don't overclaim safety relevance.** Frame the work as rigorous science of small models, with safety as motivation, not as a solved alignment contribution.
- **Scope discipline.** One flagship, one frontier showpiece, one mini-paper, one demo — everything else is "additional results" or cut.
- **MI is popular but crowded.** "Re-running a notebook" is not research. The differentiator is rigor and tooling, not topic choice.

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-22 | Pivot to MI thesis | MI produces citable, visually striking results at small scale; rewards SWE rigor; aligns with frontier lab hiring |
| 2026-06-22 | Primary flagship: grokking | Unmatched ratio of scientific completeness + visual drama to compute; anchored to ICLR 2023 oral |
| 2026-06-22 | Fallback flagship: induction heads | Known TransformerLens replication to validate against; reliable if grokking is seed-sensitive |

*See [[00_meta/03_progress-log]] for the full research journal and experiment-by-experiment decisions.*
