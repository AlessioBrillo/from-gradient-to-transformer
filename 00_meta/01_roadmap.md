---
tags: [moc, roadmap]
---

# Roadmap — From Gradient to Transformer

Seven phases. Each phase has: **Goal**, **Topics**, **Resources**, **Must exercises**, **Proof to myself** (the gate to pass before moving to the next phase).

Rule: **do not move to the next phase until the gate is green.** The proof is passed by reconstructing the concept *without looking at notes*.

---

## Phase 1 — Foundations (Math + Python + Tooling + Data Basics)

**Goal:** acquire the mathematical and coding tools to actively engage with formulas. Understand *why* a derivative works, not just how to write it in NumPy. Build solid data manipulation skills from day one.

**Topics**
- Linear algebra: vectors, matrices, matrix-vector product as transformation, eigenvalues, norms.
- Calculus: derivatives, gradient, chain rule (the heart of backprop).
- Probability and statistics: random variables, distributions, expectation/variance, Bayes, maximum likelihood.
- Scientific Python: NumPy (vectorization), pandas, matplotlib; environments with `uv`/venv; Git.
- **Data fundamentals: SQL basics, ETL intuition, data quality checks, working with different file formats (CSV, JSON, Parquet).**

**Resources**
- 3Blue1Brown — *Essence of Linear Algebra* and *Essence of Calculus* (YouTube, free).
- *Mathematics for Machine Learning* — Deisenroth, Faisal, Ong (free PDF).
- StatQuest (Josh Starmer) for visual stats and ML explanations.
- *Python Data Science Handbook* — VanderPlas (free online); Kaggle micro-courses Python/Pandas.
- **Mode Analytics SQL Tutorial** (free) for data fundamentals.

**Must exercises**
1. Implement from scratch in NumPy: matrix-matrix product, normalization, PCA on a toy dataset.
2. Derive by hand then verify numerically the gradient of `f(x)=x²` and a sigmoid.
3. Clean a real dataset with pandas (missing values, types, join) and produce 3 readable charts.
4. **Write 5 SQL queries on a public dataset (joins, aggregations, window functions).**

**Proof to myself**
> Explain the chain rule on paper and show how it applies to a composition of 3 functions.
> Implement a numerical "gradient check" in 15 lines of NumPy. If you can do it without notes → gate green.

---

## Phase 2 — Classical Machine Learning

**Goal:** master the complete supervised model cycle and understand *evaluation* and *generalization*. Build bias/variance intuition.

**Topics**
- Supervised vs unsupervised; linear/logistic regression.
- Trees, random forest, gradient boosting (XGBoost/LightGBM).
- Evaluation: train/val/test, cross-validation, metrics (accuracy, precision/recall, F1, ROC-AUC, RMSE).
- Overfitting/underfitting, regularization, feature engineering, data leakage.
- Clustering (k-means), dimensionality reduction (PCA, t-SNE).

**Resources**
- *Machine Learning Specialization* — Andrew Ng (Coursera).
- *Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow* — Géron (part 1).
- scikit-learn documentation (their tutorials are excellent); Kaggle *Intro/Intermediate ML*.

**Must exercises**
1. Full pipeline on a Kaggle dataset: EDA → feature engineering → model → CV → metrics.
2. Compare 3 models (linear, random forest, boosting) and justify the choice with numbers.
3. Build a learning curve and bias/variance diagnosis by hand.

**Proof to myself**
> New, unseen dataset, 90 minutes: from raw row to an evaluated submission, writing *why* you chose metric and model. If you can defend every choice → gate green.

---

## Phase 3 — Deep Learning (expanded: now includes RNNs, LSTMs, GRUs, and RL fundamentals)

**Goal:** understand a neural network *from the inside* — build backprop by hand, then move to PyTorch knowing what is under the hood. Bridge the gap to sequences to prepare for Transformers.

**Topics**
- Neuron, layer, activation functions; forward and **backpropagation** (autograd).
- PyTorch: tensors, `nn.Module`, optimizers, training loop, GPU.
- Optimization: SGD, Adam, learning rate, batch, schedulers.
- Regularization: dropout, weight decay, batch/layer norm, early stopping.
- Architectures: MLP, CNN (vision).
- **Sequence modeling: RNN, LSTM, GRU — why they exist, their limitations, the vanishing gradient problem.**
- **Reinforcement Learning fundamentals: policy, value function, reward, basic Q-learning. (Essential for understanding RLHF/DPO in Phase 5.)**

**Resources**
- **Andrej Karpathy — *Neural Networks: Zero to Hero*** (micrograd → makemore). The single best free course for building intuition.
- *Practical Deep Learning for Coders* — fast.ai (perfect for software engineers).
- *Dive into Deep Learning* (d2l.ai, free, with code).
- *Deep Learning Specialization* — Andrew Ng; official PyTorch tutorials.
- **Karpathy — *The spelled-out intro to neural networks and backpropagation*** (YouTube) for sequence modeling intuition.
- **Richard Sutton — *Reinforcement Learning: An Introduction*** (classic RL reference, free online draft).

**Must exercises**
1. Rewrite **micrograd** from scratch: a mini-autograd with backprop in pure Python.
2. Train an MLP on MNIST in PyTorch *without copying* the training loop.
3. Controlled experiment: same model, varying learning rates; trace and explain the loss curves.
4. **Implement an RNN cell from scratch in NumPy, train it on a character-level task (e.g., add two binary numbers).**

**Proof to myself**
> Draw the computation graph of `loss = MSE(W·x + b, y)` on paper and propagate gradients by hand.
> Then write the PyTorch training loop from memory. Gate green when both check out.

---

## Phase 4 — NLP & Transformers (expanded: sequence modeling bridge + multi-modal primer)

**Goal:** understand *the architecture* that powers GPT and Claude. Build the bridge to the capstone. Gain awareness of how these concepts extend beyond text.

**Topics**
- Text representation: tokenization, **BPE**, embeddings.
- Language models: n-gram → RNN → the leap to attention.
- **Why attention was invented: the limitations of fixed-length context in RNNs.**
- **Self-attention** and **multi-head attention**; positional encoding (absolute, RoPE).
- The **Transformer** architecture (encoder-decoder) and the **decoder-only** variant (GPT/Claude).
- Pre-training, causal language modeling, sampling (temperature, top-k, top-p).
- **Multi-modal primer: how attention bridges modalities (CLIP, vision encoders, cross-modal embeddings).**

**Resources**
- Paper *Attention Is All You Need* (Vaswani et al., 2017) — actually read it.
- Jay Alammar — *The Illustrated Transformer* (the reference visual explanation).
- **Karpathy — *Let's build GPT: from scratch, in code, spelled out*** (YouTube).
- *Hugging Face NLP/LLM Course* (huggingface.co/learn); Stanford **CS224N** and **CS25**.
- *Speech and Language Processing* — Jurafsky & Martin (free chapters on attention/transformer).
- **CLIP paper (Radford et al., 2021)** for multi-modal attention intuition.

**Must exercises**
1. Implement a **BPE tokenizer** from scratch and apply it to an English text.
2. Implement the **self-attention block** in PyTorch and verify it on a toy input.
3. Follow *Let's build GPT* and reconstruct it, annotating every line in your own words.

**Proof to myself**
> Explain what attention is to a non-technical colleague with a single analogy, then show the attention block code *without looking*. Gate green when you can hold both explanations.

---

## Phase 5 — LLM Engineering (expanded: now includes RLHF/DPO, alignment, safety, red teaming)

**Goal:** know how to build **products** on top of existing models. This is the most in-demand skill on the market today, and the one that directly interfaces with real projects.

**Topics**
- Serious prompt engineering (system prompt, few-shot, structured output).
- **RAG**: chunking, embedding, vector store, retrieval, retrieval evaluation.
- Fine-tuning: full vs **LoRA/QLoRA**; when it helps and when it does not.
- **Agents** and multi-agent orchestration; tool use; supervisor pattern.
- LLM evaluation (eval set, LLM-as-judge), guardrails, costs and latency, inference/serving.
- **Alignment: RLHF and DPO — the theory and practice of shaping model behavior.**
- **Safety: prompt injection, model extraction, content filtering, red teaming methodology.**

**Resources**
- **Chip Huyen — *AI Engineering* (O'Reilly, 2025)** + repo `chiphuyen/aie-book`. If you read one book, this is it.
- *Hands-On Large Language Models* — Alammar & Grootendorst.
- *LLM Engineering Handbook* — Iusztin & Labonne.
- Hugging Face *LLM Course*; DeepLearning.AI short courses; LangChain / LlamaIndex docs.
- **DPO paper (Rafailov et al., 2023)** — direct preference optimization, simpler than RLHF.
- **OWASP Top 10 for LLM Applications** — the safety standard.

**Must exercises**
1. Build an end-to-end **RAG** on your own corpus (e.g., documentation of one of your projects).
2. Perform a **LoRA fine-tune** of a small model and measure the delta with your own eval set.
3. Build a mini **agent** with 2-3 tools and a planning/execution loop.
4. **Implement a simple DPO training loop on a small preference dataset. Document what changes in the model's outputs.**

**Proof to myself**
> Take a real problem (one of your products) and design on a single page: data → retrieval → model → evaluation → costs. Defend every choice. Gate green when the design holds up.

---

## Phase 6 — Production AI (MLOps + System Design + Product + Security)

**Goal:** turn models into **products that generate lasting value**. This is what separates "GPT users" from serious AI system designers.

**Topics**
- **ML system design**: requirements, data, training/serving, drift, feedback loop.
- **MLOps**: data/model versioning, CI/CD, monitoring, costs, reproducibility.
- Product thinking: defining the problem, business metrics vs model metrics, ROI.
- Architecture durability and *scalability* (anti-obsolescence): abstracting model from product.
- **Security: prompt injection mitigation, model extraction prevention, production guardrails.**
- Ethics, governance, privacy (including GDPR for EU contexts).

**Resources**
- **Chip Huyen — *Designing Machine Learning Systems*** (O'Reilly).
- *Made With ML* — Goku Mohandas (MLOps end-to-end, free).
- Google Cloud — MLOps guides; production chapters of *AI Engineering*.
- Andrew Ng — *AI for Everyone* (for business language).
- **OWASP LLM Top 10** — security reference for production AI.

**Must exercises**
1. Write a full **design doc** for a real AI system (data, model, serving, costs, risks).
2. Put a model into production (even minimal) with monitoring and a rollback plan.
3. Calculate the **ROI** of an AI feature with explicit assumptions and sensitivity analysis.

**Proof to myself**
> Present the design doc as if you were in front of a non-technical stakeholder: 10 minutes, zero unnecessary jargon, clear numbers. Gate green when you convince without technical slides.

---

## Phase 7 — Capstone: micro-LLM from scratch

**Goal:** build, train, and document a **complete LLM from scratch**, with the same architectural foundation as modern models (decoder-only Transformer). This is the centerpiece of the portfolio. Operational details in [[07_capstone/README]].

**Topics / pipeline**
- Data: corpus selection, cleaning, tokenizer (your own BPE).
- Decoder-only architecture: embedding + positional (RoPE) + blocks (attention + MLP) + norm (RMSNorm) + head.
- Training loop: batch, loss (cross-entropy), optimizer, scheduler, checkpoint, logging.
- Generation: sampling with temperature/top-k/top-p.
- (Stretch) fine-tuning/instruction-tuning of a tiny version; architectural comparison with GPT/Llama.

**Resources**
- **Sebastian Raschka — *Build a Large Language Model (From Scratch)*** (Manning) + official repo.
- **Karpathy — `nanoGPT`, `minGPT`, `llm.c`**; videos *Let's build GPT* and *Let's reproduce GPT-2*.
- Reference papers for modern choices: RoPE, RMSNorm, GQA, SwiGLU (Llama/Mistral series).

**Must exercises**
1. BPE tokenizer → dataset → model → training → generation, all yours, no blind copy-paste.
2. Tracked experiments: model size vs loss, ablation on one component (e.g., with/without norm).
3. Final **writeup** ([[07_capstone/writeup]]): architecture choices and *why*.

**Final proof (graduation)**
> The model generates coherent text in the chosen domain **and** you can explain every component and why it is there. If an examiner asks "why RMSNorm and not BatchNorm?" and you answer confidently → you are an AI Engineer.
