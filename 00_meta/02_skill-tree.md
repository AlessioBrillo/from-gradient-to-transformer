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

## Phase 2 — Classical ML
- [ ] Linear/logistic regression
- [ ] Trees / ensembles / boosting
- [ ] Support Vector Machines (margin, kernel trick)
- [ ] Naive Bayes
- [ ] Cross-validation + correct metrics
- [ ] Bias/variance diagnosis
- [ ] Feature engineering without data leakage

## Phase 3 — Deep Learning
- [ ] Backprop from scratch (micrograd)
- [ ] PyTorch training loop from memory
- [ ] Optimization (Adam, LR, scheduler)
- [ ] Regularization (dropout, norm, weight decay)
- [ ] CNN and RNN/LSTM (implementation)
- [ ] Generative models (GAN / VAE / diffusion awareness)
- [ ] Reinforcement learning fundamentals

## Phase 4 — NLP & Transformers
- [ ] BPE tokenizer from scratch
- [ ] Self-attention implemented
- [ ] Multi-head + positional encoding
- [ ] Decoder-only architecture explained
- [ ] Encoder-only architecture (BERT, MLM)
- [ ] Scaling Laws (Kaplan, Chinchilla)
- [ ] Computational optimizations (FlashAttention, KV cache)
- [ ] Sampling (temperature/top-k/top-p)

## Phase 5 — LLM Engineering
- [ ] RAG end-to-end
- [ ] LoRA/QLoRA fine-tune measured
- [ ] Agent with tool use
- [ ] Eval set + LLM-as-judge + benchmarks
- [ ] RLHF/DPO alignment implemented
- [ ] LLM safety and red teaming
- [ ] Inference optimization (KV cache, structured output, speculative decoding)
- [ ] Model quantization (GPTQ, AWQ, GGUF)

## Phase 6 — Production AI
- [ ] ML system design doc
- [ ] Deploy + monitoring + rollback
- [ ] Experiment tracking (W&B)
- [ ] Reproducibility harness
- [ ] Interpretability (SHAP, LIME, mech interp)
- [ ] Privacy/GDPR + governance
- [ ] Production security (prompt injection, guardrails, adversarial robustness)

## Research Skills
- [ ] Tokenizer fertility analysis (Italian vs English)
- [ ] Reproducible experiment pipeline (≥3 seeds, mean ± std)
- [ ] From-scratch decoder-only Transformer
- [ ] Mini-paper writing (LaTeX, citations, ablations)

## Phase 7 — Capstone
- [ ] Custom tokenizer + dataset
- [ ] Complete decoder-only architecture
- [ ] Training loop + checkpoint + logging
- [ ] Coherent domain generation
- [ ] Architectural writeup + oral defense
