---
tags: [moc, skills, checklist]
---

# Skill Tree — Competence Tree

Rule: check a skill **only** when an exercise (in `exercises/`) **and** a proof (in `proofs/`) demonstrate it. A checked box without proof is a lie you tell yourself.

Legend: `[ ]` todo · `[~]` in progress · `[x]` verified (with link to proof).

## Phase 1 — Foundations
- [~] Applied linear algebra (NumPy) — proof: pending (exercise done: [[01_foundations/exercises/2d-transformation-analysis]])
- [ ] Gradient + chain rule (gradient check)
- [ ] Probability and MLE
- [ ] Information theory (entropy, cross-entropy, KL divergence)
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
