---
tags: [moc, skills, checklist]
---

# Skill Tree — Competence Tree

Rule: check a skill **only** when an exercise (in `exercises/`) **and** a proof (in `proofs/`) demonstrate it. A checked box without proof is a lie you tell yourself.

Legend: `[ ]` todo · `[~]` in progress · `[x]` verified (with link to proof).

## Phase 1 — Foundations
- [x] Applied linear algebra (NumPy) — proof: [[01_foundations/proofs/linear-algebra-foundations]] (exercises: [[01_foundations/exercises/2d-transformation-analysis]], [[01_foundations/exercises/dot-products-norms-and-basis-change]])
- [x] Gradient + chain rule (gradient check) — proof: [[01_foundations/proofs/chain-rule-and-gradient-check]] (exercise: [[01_foundations/exercises/gradient-verification]])
- [x] Probability and MLE — proof: [[01_foundations/proofs/probability-and-mle]] (exercises: [[01_foundations/exercises/maximum-likelihood-estimation-in-practice]], [[01_foundations/exercises/probability-sampling-and-expectation]])
- [x] Information theory (entropy, cross-entropy, KL divergence) — proof: [[01_foundations/proofs/information-theory-foundations]] (exercise: [[01_foundations/exercises/cross-entropy-from-first-principles]])
- [x] pandas + EDA + visualization — proof: [[01_foundations/proofs/pandas-eda-proof]] (exercise: [[01_foundations/exercises/pipeline-eda-and-visualization]])
- [x] SQL + data pipeline basics — proof: [[01_foundations/proofs/sql-data-fundamentals]] (exercise: [[01_foundations/exercises/sql-queries-for-ml]])
- [x] Git + reproducible environment — note: [[01_foundations/notes/git-and-reproducible-environments]]

### MI forward-links from foundations
> These links connect Phase 1 concepts to their mechanistic interpretability analogues:
> - Vector spaces → [[04_nlp_and_transformers/_MOC|residual stream as a shared vector space]]
> - Change of basis → projecting activations onto feature directions
> - SVD → low-rank QK/OV attention factorizations
> - Information theory → cross-entropy loss in language modeling
> - Numerical gradient check → gradient-based attribution patching (AtP)

## Phase 2 — Classical ML
- [ ] Linear/logistic regression (linear feature intuition)
- [ ] Trees / ensembles / boosting
- [ ] Support Vector Machines (margin, kernel trick — circuit intuition)
- [ ] Naive Bayes
- [ ] Cross-validation + correct metrics
- [ ] Bias/variance diagnosis
- [ ] PCA / dictionary learning — **conceptual ancestor of sparse autoencoders**

## Phase 3 — Deep Learning
- [ ] Backprop from scratch (micrograd)
- [ ] PyTorch training loop from memory
- [ ] Optimization (Adam/AdamW, LR schedulers)
- [ ] Regularization (dropout, norm, **weight decay — critical for grokking**)
- [ ] **Grokking dynamics: delayed generalization, phase transitions, progress measures**
- [ ] RNN/LSTM (vanishing gradient context for why attention matters)

## Phase 4 — NLP & Transformers (LOAD-BEARING for MI)
- [ ] BPE tokenizer from scratch
- [ ] Self-attention implemented (scaled dot-product)
- [ ] Multi-head + positional encoding (RoPE, sinusoidal)
- [ ] Decoder-only transformer from scratch (causal masking)
- [ ] **QK/OV circuit decomposition** (Elhage et al. 2021)
- [ ] **Residual stream as communication channel**
- [ ] **Induction heads: prefix-matching + copying mechanism**
- [ ] **Logit lens: projecting residual stream to vocabulary**
- [ ] **Activation patching / path patching / attribution patching**
- [ ] **TransformerLens: HookedTransformer, hook points, ActivationCache**
- [ ] Scaling Laws (Kaplan, Chinchilla)
- [ ] Computational optimizations (FlashAttention, KV cache)

## Phase 5 — LLM Engineering (reframed: model instrumentation)
- [ ] **Hooks and activation caching** (TransformerLens, nnsight)
- [ ] **Deterministic inference for reproducible circuit analysis**
- [ ] **Activation harvesting at scale**
- [ ] **Dataset construction for circuit tasks** (IOI, greater-than, docstring)
- [ ] RAG (light touch — retrieval as circuit analysis context)
- [ ] LoRA fine-tuning (light touch)

## Phase 6 — Production AI (reframed: reproducible research infra)
- [ ] **Reproducibility harness: seeds, deterministic flags, pinned deps**
- [ ] **Experiment tracking: W&B for loss curves and progress measures**
- [ ] **`make reproduce` for every experiment**
- [ ] **CI smoke tests** (fast per-experiment shape/gradient checks)
- [ ] **Feature dashboard deployment** (Hugging Face Spaces for SAE browser)
- [ ] ML system design (minimal — design doc for the capstone pipeline)

## Research Skills (Mechanistic Interpretability)
- [ ] **Induction head reproduction** — attention-pattern analysis, causal verification
- [ ] **Grokking reproduction + Fourier reverse-engineering** — the primary flagship 🌟
- [ ] **Toy Models of Superposition** — feature geometry, phase changes
- [ ] **Circuit discovery via activation patching** — find + causally validate
- [ ] **Sparse autoencoder training** — SAELens, feature dashboard
- [ ] **Automated circuit discovery** — ACDC, AtP, attribution patching
- [ ] Mini-paper writing (LaTeX, citations, ablations, limitations)

## Phase 7 — Capstone
- [ ] From-scratch decoder-only transformer (the model to reverse-engineer)
- [ ] Grokking experiment end-to-end (training + analysis + figures)
- [ ] At least one circuit verification (activation patching on the capstone model)
- [ ] SAE feature dashboard (browsable artifact)
- [ ] Mini-paper with all ablations and primary-literature citations
