---
tags: [moc, roadmap]
---

# Roadmap — From Gradient to Transformer to Circuit

Seven phases. Each phase has: **Goal**, **Topics**, **Resources**, **Must exercises**, **Proof to myself** (the gate to pass before moving to the next phase).

Rule: **do not move to the next phase until the gate is green.** The proof is passed by reconstructing the concept *without looking at notes*.

The spine: from foundational math, through classical ML and deep learning, to transformer architecture, model instrumentation, reproducible research infra, and finally a capstone that trains a decoder-only transformer and reverse-engineers its internals. Every phase builds toward **mechanistic interpretability (MI)** — the ability to read a neural network's learned algorithms like source code.

---

## Phase 1 — Foundations (Math + Python + Tooling + Data Basics)

**Goal:** acquire the mathematical and coding tools to actively engage with formulas. Understand *why* a derivative works, not just how to write it in NumPy. Build solid data manipulation skills from day one.

**MI framing:** The residual stream is a vector space; attention heads compute low-rank (SVD-like) operations; the logit lens is a projection onto the vocabulary basis. Phase 1 gives you the linear-algebraic vocabulary to think about transformers this way.

**Topics**
- Linear algebra: vectors, matrices, matrix-vector product as transformation, eigenvalues, norms. → *MI connection: residual stream as vector space, QK/OV circuits as low-rank factorizations.*
- Calculus: derivatives, gradient, chain rule (the heart of backprop).
- Probability and statistics: random variables, distributions, expectation/variance, Bayes, maximum likelihood.
- **Information theory: entropy, cross-entropy, KL divergence** — the foundation of every loss function in classification and language modeling.
- Scientific Python: NumPy (vectorization), pandas, matplotlib; environments with `uv`/venv; Git.
- Data fundamentals: SQL basics, ETL intuition, data quality checks.

**Resources**
- 3Blue1Brown — *Essence of Linear Algebra* and *Essence of Calculus* (YouTube, free).
- *Mathematics for Machine Learning* — Deisenroth, Faisal, Ong (free PDF).
- StatQuest (Josh Starmer) for visual stats and ML explanations.
- *Python Data Science Handbook* — VanderPlas (free online).
- Elhage et al., *A Mathematical Framework for Transformer Circuits* (Anthropic, 2021) — MI framing for linear algebra.

**Must exercises**
1. Implement from scratch in NumPy: matrix-matrix product, normalization, PCA on a toy dataset.
2. Derive by hand then verify numerically the gradient of `f(x)=x²` and a sigmoid.
3. Clean a real dataset with pandas (missing values, types, join) and produce 3 readable charts.
4. Compute entropy, cross-entropy, and KL divergence by hand, then verify in NumPy.

**Proof to myself**
> Explain the chain rule on paper and show how it applies to a composition of 3 functions.
> Implement a numerical "gradient check" in 15 lines of NumPy. If you can do it without notes → gate green.

---

## Phase 2 — Classical Machine Learning

**Goal:** master the complete supervised model cycle and understand *evaluation* and *generalization*. Build intuition that maps forward to MI concepts.

**MI framing:** PCA/dictionary learning is the conceptual ancestor of sparse autoencoders. SVM maximum-margin intuition maps to how attention heads separate features. Bias/variance diagnosis maps to understanding memorization vs. generalization in grokking.

**Topics**
- Supervised vs unsupervised; linear/logistic regression (linear feature intuition).
- Trees, random forest, gradient boosting (XGBoost/LightGBM).
- Evaluation: train/val/test, cross-validation, metrics (accuracy, precision/recall, F1, ROC-AUC, RMSE).
- Overfitting/underfitting, regularization, feature engineering, data leakage.
- **PCA — key forward link: the conceptual ancestor of sparse autoencoders (SAEs).** Both find a sparse, interpretable basis for data.
- **Support Vector Machines — maximum margin, kernel trick, support vectors.** Margin intuition: attention heads also separate features via linear transformations.
- Clustering (k-means), dimensionality reduction.

**Resources**
- *Machine Learning Specialization* — Andrew Ng (Coursera).
- *Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow* — Géron (part 1).
- scikit-learn documentation; Kaggle *Intro/Intermediate ML*.

**Must exercises**
1. Full pipeline on a Kaggle dataset: EDA → feature engineering → model → CV → metrics.
2. PCA on a dataset: vary components, explain variance, visualize in 2D. *Connect to SAE sparsity.*
3. Build a learning curve and bias/variance diagnosis by hand.

**Proof to myself**
> New, unseen dataset, 90 minutes: from raw row to an evaluated submission, writing *why* you chose metric and model. If you can defend every choice → gate green.

---

## Phase 3 — Deep Learning (expanded: training dynamics, grokking-relevant phenomena)

**Goal:** understand a neural network *from the inside* — build backprop by hand, then move to PyTorch knowing what is under the hood. Build the training-dynamics intuition needed for MI work.

**MI framing:** Grokking is a training-dynamics phenomenon (delayed generalization, phase transitions, weight decay's critical role). Understanding optimization is essential for reproducing and studying grokking.

**Topics**
- Neuron, layer, activation functions; forward and **backpropagation** (autograd).
- PyTorch: tensors, `nn.Module`, optimizers, training loop, GPU.
- Optimization: SGD, AdamW, learning rate, batch, schedulers. **Weight decay — critical for grokking.**
- Regularization: dropout, weight decay, batch/layer norm, early stopping.
- Architectures: MLP, CNN (vision).
- Sequence modeling: RNN, LSTM, GRU — why they exist, their limitations (context for why attention was invented).
- **Grokking-relevant dynamics: delayed generalization, phase transitions, the role of weight decay in circuit formation.**
- Training tricks: gradient accumulation, gradient clipping, mixed precision.

**Resources**
- Andrej Karpathy — *Neural Networks: Zero to Hero* (micrograd → makemore).
- *Practical Deep Learning for Coders* — fast.ai.
- *Dive into Deep Learning* (d2l.ai, free, with code).
- Power et al., *Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets* (2022).
- Nanda et al., *Progress Measures for Grokking via Mechanistic Interpretability* (ICLR 2023).

**Must exercises**
1. Rewrite **micrograd** from scratch: a mini-autograd with backprop in pure Python.
2. Train an MLP on MNIST in PyTorch *without copying* the training loop.
3. Controlled experiment: same model, varying learning rates; trace and explain the loss curves.
4. **Reproduce a mini-grokking experiment:** train a small transformer on modular addition (tiny P) and observe the delayed generalization curve.

**Proof to myself**
> Draw the computation graph of `loss = MSE(W·x + b, y)` on paper and propagate gradients by hand.
> Then write the PyTorch training loop from memory. Gate green when both check out.

---

## Phase 4 — NLP & Transformers (LOAD-BEARING for MI)

**Goal:** understand *the architecture* that powers GPT and Claude. Build the decoder-only transformer from scratch. Then — critically — learn to *read* it: decompose attention into QK/OV circuits, identify induction heads, use the logit lens, and perform causal interventions with activation patching.

**This is the most important phase for the MI thesis.** Every concept here directly feeds the capstone.

**Topics**
- **Building from scratch:** text representation, tokenization, BPE, embeddings.
- **Self-attention** and **multi-head attention**; positional encoding (absolute, RoPE).
- **Decoder-only architecture:** causal masking, autoregressive generation, full implementation.
- **QK/OV circuit decomposition** — the key conceptual tool: every attention head computes two separate functions (what to attend to → QK; what to copy → OV).
- **Residual stream as communication channel** — layers read from and write to a shared vector space.
- **Induction heads** — the mechanism behind in-context learning: prefix-matching + copying.
- **Logit lens** — projecting residual stream states to vocabulary to read the model's "thoughts."
- **Activation patching / path patching / attribution patching** — causal intervention tools.
- **TransformerLens:** `HookedTransformer`, hook points, `ActivationCache`, built-in patching utilities.
- Encoder-only architecture (BERT): masked language modeling, bidirectional context (for completeness).
- Scaling Laws (Kaplan, Chinchilla); computational optimizations (FlashAttention, KV cache).

**Resources**
- Vaswani et al., *Attention Is All You Need* (NeurIPS 2017) — read it.
- Jay Alammar — *The Illustrated Transformer*.
- **Elhage et al., *A Mathematical Framework for Transformer Circuits* (Anthropic, 2021)** — THE paper for QK/OV, residual stream, virtual weights.
- **Olsson, Elhage, Nanda et al., *In-context Learning and Induction Heads* (Anthropic, 2022)** — the induction heads paper.
- **Nanda's TransformerLens demo notebooks** — the single best hands-on resource.
- **ARENA Chapter 1** — build GPT-2, locate induction heads, IOI circuit.
- **Anthropic Transformer Circuits thread** — the full series.
- **Distill Circuits thread** — vision circuits for intuition transfer.
- Karpathy — *Let's build GPT: from scratch, in code, spelled out* (YouTube).

**Must exercises**
1. Build a **decoder-only transformer from scratch** in PyTorch (embed → blocks → unembed). This will be the capstone model.
2. **Load a model in TransformerLens**, inspect attention patterns, identify an induction head by its attention pattern.
3. **Use the logit lens:** project residual stream states at each layer and observe how predictions refine.
4. **Perform activation patching:** corrupt a specific position/layer and measure the change in output.
5. **Implement the QK/OV decomposition** for a single attention head and explain what each part computes.

**Proof to myself**
> Explain the residual stream metaphor to a non-technical colleague. Then show the QK/OV decomposition code for a single attention head *without looking*. Gate green when you can hold both explanations.

---

## Phase 5 — LLM Engineering (reframed: Model Instrumentation)

**Goal:** learn to *instrument* models — attach hooks, cache activations, run deterministic inference, and construct datasets specifically designed for circuit analysis. This is where the software-engineering background becomes a research asset.

**Reframing from the standard "LLM Engineering" phase:** Instead of building RAG pipelines and agents, the focus is on the engineering that powers MI research — reliable, reproducible, scalable activation harvesting.

**Topics**
- **TransformerLens hooks deep-dive:** pre/post hooks on any layer, module, or attention head; caching and reusing activations.
- **Deterministic inference:** seed control, deterministic algorithms, floating-point determinism across runs.
- **Activation harvesting:** efficiently collecting activations across many prompts; storage formats and memory management.
- **Dataset construction for circuit tasks:** synthetic data generation for IOI (indirect object identification), greater-than, docstring completion; ensuring balanced and controlled datasets.
- **nnsight:** PyTorch-compatible intervention graphs (optional — for when you need remote execution on larger models).
- Light touch: RAG, LoRA fine-tuning (useful context but not the focus).

**Resources**
- **TransformerLens documentation and demo notebooks** — the primary resource.
- **Nanda's Concrete Steps to Get Started in Transformer Mechanistic Interpretability** — excellent practical guide.
- **nnsight documentation** (for the intervention-graph approach).
- *AI Engineering* — Chip Huyen (O'Reilly, 2025) — for the general engineering mindset.

**Must exercises**
1. **Write a TransformerLens hook that captures all attention patterns** for a given model and stores them efficiently.
2. **Build a synthetic IOI dataset** (subject, verb, object templates) and verify balance.
3. **Implement a deterministic inference pipeline** that produces identical outputs across 3 runs with the same seed.

**Proof to myself**
> Someone gives you a new model and a circuit-hypothesis to test. Design on a single page: data → hook placement → intervention → analysis. Defend every engineering choice → gate green.

---

## Phase 6 — Production AI (reframed: Reproducible Research Infrastructure)

**Goal:** turn experiments into **reproducible, citable research**. This is what separates portfolio projects from PhD-level work. Every figure regenerates with one command, every experiment is tracked, and the entire pipeline is CI-tested.

**Reframing from the standard "Production AI" phase:** Instead of deployment and MLOps for product, the infrastructure serves the research goal: making every result auditable, extendable, and trustworthy.

**Topics**
- **Reproducibility harness:** global seed control, deterministic flags, pinned environment (`uv.lock`), `make reproduce`.
- **Experiment tracking:** Weights & Biases for loss curves, progress measures, hyperparameter sweeps.
- **CI for research:** GitHub Actions running fast smoke tests of each experiment (tiny model, few steps) on every push.
- **Figure generation:** matplotlib/`sae-vis` scripts that produce publication-quality figures; every figure has a deterministic generator under version control.
- **Feature dashboard deployment:** Hugging Face Spaces for the SAE feature browser.
- **Mini-paper workflow:** LaTeX template, `make paper` target, citation management.
- Light touch: system design, costs, security (the capstone's pipeline needs a design doc).

**Resources**
- Pineau et al., *Improving Reproducibility in ML Research* (JMLR 2021).
- **SAELens** + **sae-vis** documentation.
- Hugging Face Spaces documentation.
- *Designing Machine Learning Systems* — Chip Huyen (O'Reilly).

**Must exercises**
1. **Set up W&B logging** for one experiment (grokking or induction heads). Log loss, accuracy, and a custom progress measure.
2. **Write a CI workflow** that runs a smoke test of `exp2_grokking` (tiny P, 100 steps) on every push.
3. **Build a `make reproduce` that regenerates at least the flagship figure.**

**Proof to myself**
> Clone the repo on a clean machine, run `uv sync && make reproduce`, and get identical figures and numbers. Gate green: no manual steps needed.

---

## Cross-cutting topics (studied throughout all phases)

These are not a separate phase — they grow with you. Engage with them at each stage, at increasing depth.

- **The MI literature map:** Elhage et al. (Mathematical Framework), Olsson et al. (Induction Heads), Nanda et al. (Grokking), Wang et al. (IOI circuit), Bricken et al. (Towards Monosemanticity), Cunningham et al. (SAEs) — read and re-read as your understanding deepens.
- **Honest caveats about MI methods:** attribution patching is a linear approximation with known failure modes; activation patching can mislead through layernorm denominator effects; SAEs can learn illusory features. Document your methods and limitations explicitly.
- **Incremental contribution mindset:** a bare reproduction of a known result is table stakes. Add a novel small ablation, test on a different setup, or improve the tooling, then document the delta.

---

## Phase 7 — Capstone: Train + Reverse-Engineer

**Goal:** build a decoder-only transformer from scratch AND reverse-engineer its internals using the full MI toolkit. This is the centerpiece of both the portfolio and the research journey.

**Thesis:**
> I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns — grokking modular addition with Fourier decomposition, induction heads, circuit verification via activation patching, and sparse autoencoder feature extraction.

**Experiment ladder (do in order; each is a defensible standalone result):**

1. **Rung 1 — Induction heads in a 2-layer attention-only transformer** (safe fallback flagship). Train on repeated-random-token sequences; identify induction heads by their attention pattern; verify causally via ablation/patching.

2. **Rung 2 — Grokking on modular addition + Fourier reverse-engineering (PRIMARY FLAGSHIP 🌟).** Train a 1-layer transformer on a+b mod P; observe the grokking phase transition; decompose embeddings in Fourier space to reveal the trigonometric algorithm; ablate frequencies to confirm the mechanism.

3. **Rung 3 — Toy Models of Superposition reproduction.** Train a tiny ReLU autoencoder on synthetic sparse features; sweep sparsity; plot the geometric phase transition from monosemantic to superposed features.

4. **Rung 4 — Circuit verification via activation/path patching.** Identify a circuit (IOI-style or task-specific) in GPT-2-small or the capstone model; causally verify each component's role with activation/path patching.

5. **Rung 5 — Sparse autoencoder on residual stream.** Train an SAE on the capstone model's activations; build a feature dashboard; report sparsity/reconstruction tradeoff and dead feature rate.

6. **Rung 6 (stretch) — Automated vs. hand-found circuit comparison.** Run ACDC on the Rung 4 task and compare the recovered subgraph to the manual circuit.

**Topics / pipeline**
- Model: decoder-only transformer (embedding → RoPE → blocks → RMSNorm → unembed).
- Data: modular addition (a+b mod P), repeated-token sequences, synthetic IOI.
- Training: AdamW, weight decay (critical for grokking), cosine LR schedule.
- Analysis: TransformerLens hooks, activation caching, logit lens, Fourier decomposition.
- Causal intervention: activation patching, path patching, attribution patching.
- SAE: SAELens training, feature dashboard via `sae-vis`.

**Resources**
- **Nanda et al., *Progress Measures for Grokking via Mechanistic Interpretability* (ICLR 2023)** — the core paper for Rung 2.
- **Olsson et al., *In-context Learning and Induction Heads* (Anthropic, 2022)** — for Rung 1.
- **Elhage et al., *Toy Models of Superposition* (Anthropic, 2022)** — for Rung 3.
- **Wang et al., *Interpretability in the Wild: a Circuit for IOI in GPT-2 small* (ICLR 2023)** — for Rung 4.
- **Bricken et al., *Towards Monosemanticity* (Anthropic, 2023)** and **Cunningham et al. (ICLR 2024)** — for Rung 5.
- **TransformerLens + SAELens** documentation.
- Karpathy — `nanoGPT`, `minGPT` — architectural reference.
- Raschka — *Build a Large Language Model (From Scratch)* (Manning).

**Proof to myself (graduation)**
> Someone asks: "How does your transformer implement modular addition?" Explain the Fourier algorithm, show the progress measures, and demonstrate a causal ablation that confirms the mechanism. Gate green when you can defend every step, training to reverse-engineering.
