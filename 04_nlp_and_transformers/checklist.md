---
tags: [checklist, phase/4]
---

# Checklist — Phase 4 · NLP & Transformers (LOAD-BEARING for MI)

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

**This is the most important phase for the MI thesis.** Every skill here directly feeds the capstone. The goal is not just to *use* transformers, but to *read* them — decompose attention into QK/OV circuits, identify induction heads, perform causal interventions.

## Phase gate
- [ ] **Proof passed** → I can move to the capstone.

## Core Transformer Architecture
- [ ] BPE tokenizer: implementation from scratch
- [ ] Self-attention: scaled dot-product, implementation in PyTorch
- [ ] Multi-head attention: concatenation, projection
- [ ] Positional encoding: sinusoidal, learned, RoPE (implement and compare)
- [ ] Decoder-only transformer: causal masking, autoregressive generation, full implementation
- [ ] Encoder-only (BERT): masked language modeling, bidirectional context (breadth)
- [ ] Scaling Laws: Kaplan & Chinchilla — compute-optimal training
- [ ] Sampling: temperature, top-k, top-p for generation

## Mechanistic Interpretability (Core MI Skills)
- [ ] **QK/OV circuit decomposition** — understand and implement: QK computes *where* to attend, OV computes *what* to copy
- [ ] **Residual stream as communication channel** — layers read from and write to this shared vector space
- [ ] **Induction heads** — prefix-matching + copying mechanism behind in-context learning
- [ ] **Logit lens** — project residual stream to vocabulary, observe predictions per layer
- [ ] **Activation patching** — causal intervention: replace activations and measure effect
- [ ] **Path patching** — trace effects along specific edges in the computational graph
- [ ] **Attribution patching (AtP)** — gradient-based linear approximation for fast hypothesis generation

## Tooling
- [ ] **TransformerLens:** HookedTransformer, hook points, ActivationCache, built-in patching
- [ ] **SAELens:** training and loading sparse autoencoders
- [ ] **nnsight:** PyTorch-compatible intervention graphs (optional, for larger models)
- [ ] **circuitsvis:** attention-pattern visualization
