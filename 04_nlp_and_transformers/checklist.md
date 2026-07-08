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
- [x] Self-attention: scaled dot-product, implementation in PyTorch (code: `src/models/decoder_only_transformer.py`)
- [x] Multi-head attention: concatenation, projection (code: `src/models/decoder_only_transformer.py`)
- [x] Positional encoding: RoPE (code: `src/models/decoder_only_transformer.py`)
- [x] Decoder-only transformer: causal masking, autoregressive generation, full implementation (code: `src/models/decoder_only_transformer.py`)
- [ ] Encoder-only (BERT): masked language modeling, bidirectional context (breadth)
- [ ] Scaling Laws: Kaplan & Chinchilla — compute-optimal training
- [x] Sampling: temperature, top-k, top-p for generation (built into `DecoderOnlyTransformer.generate()`)

## Mechanistic Interpretability (Core MI Skills)
- [x] **QK/OV circuit decomposition** — note: [[04_nlp_and_transformers/notes/qk-ov-circuits]], proof: [[04_nlp_and_transformers/proofs/qk-ov-decomposition]]
- [x] **Residual stream as communication channel** — proof: [[04_nlp_and_transformers/proofs/residual-stream-communication-channel]]
- [x] **Induction heads** — note: [[04_nlp_and_transformers/notes/induction-heads]], exercise: [[04_nlp_and_transformers/exercises/ex-02-induction-head-detection]]
- [x] **Logit lens** — proof: [[04_nlp_and_transformers/proofs/logit-lens]]
- [x] **Activation patching** — note: [[04_nlp_and_transformers/notes/activation-patching]], exercise: [[04_nlp_and_transformers/exercises/ex-03-activation-patching]]
- [ ] **Path patching** — trace effects along specific edges in the computational graph
- [x] **Attribution patching (AtP)** — note: [[04_nlp_and_transformers/notes/activation-patching]]

## Tooling
- [ ] **TransformerLens:** HookedTransformer, hook points, ActivationCache, built-in patching
- [ ] **SAELens:** training and loading sparse autoencoders
- [ ] **nnsight:** PyTorch-compatible intervention graphs (optional, for larger models)
- [ ] **circuitsvis:** attention-pattern visualization
