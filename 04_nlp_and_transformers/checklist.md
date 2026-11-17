---
tags: [type/moc, phase/4, state/consolidated]
---

# Checklist — Phase 4 · NLP & Transformers (LOAD-BEARING for MI)

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

**This is the most important phase for the MI thesis.** Every skill here directly feeds the capstone. The goal is not just to *use* transformers, but to *read* them — decompose attention into QK/OV circuits, identify induction heads, perform causal interventions.

## Phase gate
- [x] **Proof passed** → I can move to the capstone. (gate proof: [[04_nlp_and_transformers/proofs/circuit-analysis-complete]])

## Core Transformer Architecture
- [~] BPE tokenizer: implementation from scratch (note: [[04_nlp_and_transformers/notes/bpe-tokenizer]], code: `src/models/bpe_tokenizer.py`)
- [~] Self-attention: scaled dot-product, implementation in PyTorch (code: `src/models/decoder_only_transformer.py`)
- [~] Multi-head attention: concatenation, projection (code: `src/models/decoder_only_transformer.py`)
- [~] Positional encoding: RoPE (code: `src/models/decoder_only_transformer.py`)
- [~] Decoder-only transformer: causal masking, autoregressive generation, full implementation (code: `src/models/decoder_only_transformer.py`)
- [~] Encoder-only (BERT): masked language modeling, bidirectional context (breadth)
- [~] Scaling Laws: Kaplan & Chinchilla — compute-optimal training (note: [[04_nlp_and_transformers/notes/scaling-laws]])
- [~] Sampling: temperature, top-k, top-p for generation (built into `DecoderOnlyTransformer.generate()`)

## Mechanistic Interpretability (Core MI Skills)
- [x] QK/OV circuit decomposition — exercise: [[04_nlp_and_transformers/exercises/ex-02-induction-head-detection]]; proof: [[04_nlp_and_transformers/proofs/qk-ov-decomposition]]
- [x] **Residual stream as communication channel** — exercise: [[04_nlp_and_transformers/exercises/ex-01-transformer-from-scratch]]; proof: [[04_nlp_and_transformers/proofs/residual-stream-communication-channel]]
- [x] **Induction heads** — exercise: [[04_nlp_and_transformers/exercises/ex-02-induction-head-detection]]; proof: [[04_nlp_and_transformers/proofs/circuit-analysis-complete]]
- [x] **Logit lens** — exercise: [[04_nlp_and_transformers/exercises/ex-01-transformer-from-scratch]]; proof: [[04_nlp_and_transformers/proofs/logit-lens]]
- [x] **Activation patching** — exercise: [[04_nlp_and_transformers/exercises/ex-03-activation-patching]]; proof: [[04_nlp_and_transformers/proofs/circuit-analysis-complete]]
- [x] **Path patching** — trace effects along specific edges in the computational graph (note: [[04_nlp_and_transformers/notes/path-patching]]) — exercise: [[04_nlp_and_transformers/exercises/ex-03-activation-patching]]; proof: [[04_nlp_and_transformers/proofs/circuit-analysis-complete]]
- [~] **Attribution patching (AtP)**

## Tooling
- [~] **TransformerLens:** HookedTransformer, hook points, ActivationCache, built-in patching (note: [[04_nlp_and_transformers/notes/mi-tooling]])
- [-] (descoped: the dependency was dropped 2026-08-01 because nothing imported it (`pyproject.toml`); the repository trains its own SAE in `exp5`) **SAELens:** training and loading sparse autoencoders (same note)
- [-] **nnsight:** (descoped 2026-10-11: no remote execution needed, see the descope register) PyTorch-compatible intervention graphs (optional, for larger models) (same note)
- [-] (descoped: the dependency was dropped 2026-08-01 because nothing imported it (`pyproject.toml`); the figures are drawn by the experiments) **circuitsvis:** attention-pattern visualization (same note)
