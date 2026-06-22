---
tags: [phase/7, capstone, writeup]
---

# Writeup — Reverse-Engineering a Micro-Transformer: Grokking, Circuits, and Sparse Features

Final document: explain the model and results as if you had to defend them in a conference poster session or research interview.

## 1. Thesis and Motivation
- From gradient to transformer to circuit: the case for small-scale mechanistic interpretability.
- Why micro-scale: the foundational results in MI were *obtained on tiny models* (1–2 layers, single-digit millions of parameters). Small scale is the *native* setting for circuit discovery, not a compromise.
- The experiment arc: train → observe emergence → form causal hypotheses → test with interventions → extract features.

## 2. Grokking Modular Addition (Flagship)
- Setup: 1-layer transformer, a+b mod P, 30% train fraction, AdamW with high weight decay.
- The grokking curve: delayed generalization, phase transition.
- Fourier decomposition: embeddings decompose into sparse frequencies; the model implements addition via trigonometric identities (sin(a+b) = sin a cos b + cos a sin b).
- Progress measures: three-phase training dynamic — memorization → circuit formation → cleanup.
- Causal confirmation: ablating the identified Fourier frequencies destroys performance; ablating the remaining ~95% *improves* it.
- Comparison to Nanda et al. (ICLR 2023): what reproduced identically, what differed, and what might explain the differences (seed sensitivity, hyperparameter drift).

## 3. Induction Heads
- Setup: 2-layer attention-only transformer on repeated random tokens.
- The induction-head pattern: [A][B]…[A]→[B] via prefix-matching + copying.
- Training dynamics: the loss "bump" / phase change at induction head formation.
- Causal verification: head ablation, logit-lens analysis, attention-pattern entropy.
- *If this is the primary flagship (grokking fallback):* then this section is expanded with full detail and Section 2 is condensed.

## 4. Toy Models of Superposition
- Setup: tiny ReLU autoencoder on synthetic sparse features.
- The geometry of superposition: feature polytopes, phase change with sparsity.
- Connection to SAEs: superposition is why we need dictionary learning — features are not neurons.

## 5. Circuit Discovery via Activation Patching
- Task: IOI or task-specific circuit (e.g., greater-than, docstring).
- Method: activation patching and path patching.
- Results: logit-difference recovery per component; circuit faithfulness and minimality.
- Comparison to the canonical circuit (Wang et al. 2023): where does the micro-scale circuit match or differ?

## 6. Sparse Autoencoder Extraction
- SAE training on the capstone model's residual stream.
- Feature dashboard: top-activating examples, logit effects, activation distributions.
- Sparsity/reconstruction tradeoff: L0 vs. loss-recovered.
- Dead feature analysis and mitigation strategies (BatchTopK, resampling).
- Connection to the circuits found in Rungs 2/4: do SAE features correspond to the same algorithmic components?

## 7. Limitations
- Micro-scale models: findings may not transfer to 7B+ models.
- Algorithmic tasks (modular addition) are cleaner than natural language; circuits found may not be representative.
- Attribution patching is a linear approximation (fails on large activations like the residual stream).
- Activation patching can mislead via layernorm denominator effects and subspace projection illusions.
- SAE interpretability is human-judged, inherently subjective, and features can be illusory (Makelov, Lange & Nanda 2023).
- Single architecture family, single seed distribution — no claims of universality.

## 8. Related Work
- The Circuits thread (Anthropic/Distill): Elhage, Olsson, Bricken, Templeton.
- Grokking literature: Power et al. 2022, Nanda et al. 2023, Liu et al. (Omnigrok) 2022.
- Circuit discovery: Wang et al. 2023 (IOI), Conmy et al. 2023 (ACDC).
- Sparse autoencoders: Bricken et al. 2023, Cunningham et al. 2024, Rajamanoharan et al. (Gated/JumpReLU SAEs, DeepMind 2024), Gao et al. (TopK SAEs, OpenAI 2024).
- Methodology: Meng et al. (ROME), Chan et al. (Causal Scrubbing), Nanda (Attribution Patching, 2023), Kramár et al. (AtP*, 2024).

## 9. What I Truly Understood
- The most important section: the intuition that stays with you after building everything.
- The residual stream is the single most useful abstraction: a shared vector space where every layer reads and writes.
- Attention heads are not monolithic: QK computes *where* to look, OV computes *what* to copy. They can be (and often are) trained independently.
- Grokking is not magic: it is the competition between memorization (low-weight, high-norm features) and generalizing circuits (high-weight, low-norm features), mediated by weight decay.
- The hardest part of MI is not running experiments — it is forming precise, falsifiable hypotheses about what the model is doing. The tools (patching, SAEs) are easier than the thinking.
- A negative result honestly reported is more valuable than a positive result overclaimed.
