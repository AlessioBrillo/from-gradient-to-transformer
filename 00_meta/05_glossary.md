---
tags: [glossary]
---

# Glossary

One term, one line, **linked** to the notes that use it. Keep only your own definitions here, not copied ones. When a term appears in 3+ notes, it deserves its own atomic note.

## Foundations
- **Backpropagation** — algorithm to compute gradients via the chain rule. → [[03_deep_learning/_MOC]]
- **Entropy** — measure of uncertainty in a probability distribution; minimum bits needed to encode a distribution. → [[01_foundations/_MOC]]
- **Cross-entropy** — loss function measuring difference between two probability distributions; the de facto loss for classification and language modeling. → [[01_foundations/_MOC]], [[04_nlp_and_transformers/_MOC]]
- **KL divergence** — Kullback–Leibler divergence: asymmetric measure of how one distribution diverges from another. → [[01_foundations/_MOC]]

## Transformer Architecture
- **Attention** — mechanism that weights token relevance to each other. → [[04_nlp_and_transformers/_MOC]]
- **Self-attention** — each token attends to all tokens in the sequence (including itself). → [[04_nlp_and_transformers/_MOC]]
- **RoPE** — Rotary Position Embedding: encoding token positions via rotation matrices. → [[04_nlp_and_transformers/_MOC]]
- **RMSNorm** — Root Mean Square Layer Normalization: a simpler, faster alternative to LayerNorm. → [[04_nlp_and_transformers/_MOC]]
- **KV cache** — Key-Value cache: stores attention keys/values from previous tokens to avoid recomputation during autoregressive generation. → [[04_nlp_and_transformers/_MOC]]
- **FlashAttention** — IO-aware exact attention algorithm that dramatically reduces memory reads/writes, enabling long-context Transformers. → [[04_nlp_and_transformers/_MOC]]
- **Scaling Laws** — empirical relationships between model size, data size, compute, and performance. → [[04_nlp_and_transformers/_MOC]]

## Mechanistic Interpretability (Core)
- **Mechanistic Interpretability (MI)** — reverse-engineering the algorithms a trained neural network has learned, akin to decompiling a binary into source code. → [[04_nlp_and_transformers/_MOC]], [[07_capstone/README]]
- **Residual stream** — the central communication channel of a transformer; each layer reads from and writes to this shared vector space. → [[04_nlp_and_transformers/_MOC]]
- **QK circuit** — the attention head's query-key computation: which previous tokens to attend to. → [[04_nlp_and_transformers/_MOC]]
- **OV circuit** — the attention head's output-value computation: what information to copy from the attended token. → [[04_nlp_and_transformers/_MOC]]
- **Induction head** — an attention head that implements [A][B]…[A]→[B]: attends to the previous occurrence of the current token and copies what followed it. The mechanism behind much in-context learning. → [[04_nlp_and_transformers/_MOC]]
- **Logit lens** — technique to project the residual stream's final state into vocabulary space via the unembedding matrix, revealing what the model "thinks" at each layer. → [[04_nlp_and_transformers/_MOC]]

## Mechanistic Interpretability (Advanced)
- **Grokking** — delayed generalization phenomenon where a model suddenly generalizes long after memorizing the training data, often accompanied by a phase transition in loss. → [[07_capstone/README]]
- **Superposition** — the phenomenon where a neural network represents more features than it has neurons by packing them into overlapping, nearly orthogonal directions. → [[04_nlp_and_transformers/_MOC]]
- **Sparse Autoencoder (SAE)** — a dictionary-learning method that decomposes model activations into interpretable, monosemantic features by enforcing sparsity. → [[07_capstone/README]]
- **Feature dashboard** — a browsable interface showing an SAE's learned features: top-activating examples, logit effects, and activation distributions. → [[07_capstone/README]]
- **Activation patching** — a causal intervention: replace an activation at a specific position/layer with a counterfactual value and measure the change in output. → [[04_nlp_and_transformers/_MOC]]
- **Path patching** — activation patching along specific edges or paths in the computational graph, isolating the contribution of a specific circuit. → [[04_nlp_and_transformers/_MOC]]
- **Attribution patching (AtP)** — a gradient-based linear approximation to activation patching, requiring only 2 forward + 1 backward passes. → [[04_nlp_and_transformers/_MOC]]
- **ACDC** — Automated Circuit DisCovery: systematic ablation to find minimal subgraphs responsible for a behavior. → [[07_capstone/README]]
- **Causal scrubbing** — a principled method to evaluate interpretability hypotheses via behavior-preserving resample ablations. → [[04_nlp_and_transformers/_MOC]]

## Tools
- **TransformerLens** — the de facto standard MI library for GPT-style models (HookedTransformer, hook points, caching, patching). → [[04_nlp_and_transformers/_MOC]]
- **SAELens** — library for training/loading sparse autoencoders on transformer activations. → [[07_capstone/README]]
- **nnsight** — PyTorch-compatible intervention graphs with remote execution for large models. → [[04_nlp_and_transformers/_MOC]]
- **Neuronpedia** — web platform for browsing SAE features. → [[07_capstone/README]]

## Production / Infra
- **RAG** — Retrieval-Augmented Generation. → [[05_llm_engineering/_MOC]]
- **RLHF** — Reinforcement Learning from Human Feedback. → [[05_llm_engineering/_MOC]]
- **DPO** — Direct Preference Optimization. → [[05_llm_engineering/_MOC]]
- **MLOps** — ML Operations: the practice of deploying, monitoring, and maintaining ML models in production. → [[06_production_ai/_MOC]]
