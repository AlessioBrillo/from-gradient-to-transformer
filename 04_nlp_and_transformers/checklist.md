---
tags: [checklist, phase/4]
---

# Checklist — Phase 4 · NLP & Transformers (LOAD-BEARING for MI)

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

**This is the most important phase for the MI thesis.** Every skill here directly feeds the capstone. The goal is not just to *use* transformers, but to *read* them — decompose attention into QK/OV circuits, identify induction heads, perform causal interventions.

## Phase gate
- [x] **Proof passed** → I can move to the capstone. (gate proof: [[04_nlp_and_transformers/proofs/circuit-analysis-complete]])

## Core Transformer Architecture
- [x] BPE tokenizer: implementation from scratch (note: [[04_nlp_and_transformers/notes/bpe-tokenizer]], code: `src/models/bpe_tokenizer.py`)
- [x] Self-attention: scaled dot-product, implementation in PyTorch (code: `src/models/decoder_only_transformer.py`)
- [x] Multi-head attention: concatenation, projection (code: `src/models/decoder_only_transformer.py`)
- [x] Positional encoding: RoPE (code: `src/models/decoder_only_transformer.py`)
- [x] Decoder-only transformer: causal masking, autoregressive generation, full implementation (code: `src/models/decoder_only_transformer.py`)
- [x] Encoder-only (BERT): masked language modeling, bidirectional context (breadth)
- [x] Scaling Laws: Kaplan & Chinchilla — compute-optimal training (note: [[04_nlp_and_transformers/notes/scaling-laws]])
- [x] Sampling: temperature, top-k, top-p for generation (built into `DecoderOnlyTransformer.generate()`)

## Mechanistic Interpretability (Core MI Skills)
- [x] QK/OV circuit decomposition
- [x] **Residual stream as communication channel**
- [x] **Induction heads**
- [x] **Logit lens**
- [x] **Activation patching**
- [x] **Path patching** — trace effects along specific edges in the computational graph (note: [[04_nlp_and_transformers/notes/path-patching]])
- [x] **Attribution patching (AtP)**

## Tooling
- [x] **TransformerLens:** HookedTransformer, hook points, ActivationCache, built-in patching (note: [[04_nlp_and_transformers/notes/mi-tooling]])
- [x] **SAELens:** training and loading sparse autoencoders (same note)
- [x] **nnsight:** PyTorch-compatible intervention graphs (optional, for larger models) (same note)
- [x] **circuitsvis:** attention-pattern visualization (same note)
