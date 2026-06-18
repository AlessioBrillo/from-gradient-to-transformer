---
tags: [moc, skills, checklist]
---

# Skill Tree — Competence Tree

Rule: check a skill **only** when an exercise (in `exercises/`) **and** a proof (in `proofs/`) demonstrate it. A checked box without proof is a lie you tell yourself.

Legend: `[ ]` todo · `[~]` in progress · `[x]` verified (with link to proof).

## Phase 1 — Foundations
- [x] Applied linear algebra (NumPy) — proof: [[01_foundations/proofs/linear-algebra-foundations]] (exercises: [[01_foundations/exercises/2d-transformation-analysis]], [[01_foundations/exercises/dot-products-norms-and-basis-change]])
- [x] Gradient + chain rule (gradient check) — proof: [[01_foundations/proofs/chain-rule-and-gradient-check]] (exercise: [[01_foundations/exercises/gradient-verification]])
- [ ] Probability and MLE
- [~] Information theory (entropy, cross-entropy, KL divergence) — exercise: [[01_foundations/exercises/cross-entropy-from-first-principles]]
- [ ] pandas + EDA + visualization
- [ ] SQL + data pipeline basics
- [ ] Git + reproducible environment

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
- [ ] Training tricks (gradient accumulation, mixed precision, gradient clipping)

## Phase 4 — NLP & Transformers
- [ ] BPE tokenizer from scratch
- [ ] Self-attention implemented
- [ ] Multi-head + positional encoding
- [ ] Decoder-only architecture explained
- [ ] Encoder-only architecture (BERT, MLM)
- [ ] Scaling Laws (Kaplan, Chinchilla)
- [ ] Computational optimizations (FlashAttention, KV cache)
- [ ] Sampling (temperature/top-k/top-p)
- [ ] Multi-modal awareness (CLIP, cross-modal)

## Phase 5 — LLM Engineering
- [ ] RAG end-to-end
- [ ] LoRA/QLoRA fine-tune measured
- [ ] Agent with tool use
- [ ] Eval set + LLM-as-judge + benchmarks
- [ ] RLHF/DPO alignment implemented
- [ ] LLM safety and red teaming
- [ ] Inference optimization (KV cache, structured output, speculative decoding)
- [ ] Model quantization (GPTQ, AWQ, GGUF)
- [ ] Cost/latency/serving reasoning

## Phase 6 — Production AI
- [ ] ML system design doc
- [ ] Deploy + monitoring + rollback
- [ ] ROI calculation with sensitivity
- [ ] Anti-obsolescence architecture
- [ ] Interpretability (SHAP, LIME, mech interp)
- [ ] Privacy/GDPR + governance
- [ ] Production security (prompt injection, guardrails, adversarial robustness)
- [ ] Data versioning + experiment tracking (DVC, MLflow/W&B)

## Cross-cutting (studied across phases)
- [ ] Ethics, fairness, bias in AI (dataset bias, fairness metrics, regulatory context)
- [ ] Interpretability stack (feature → neuron → mechanistic)

## Phase 7 — Capstone
- [ ] Custom tokenizer + dataset
- [ ] Complete decoder-only architecture
- [ ] Training loop + checkpoint + logging
- [ ] Coherent domain generation
- [ ] Architectural writeup + oral defense
