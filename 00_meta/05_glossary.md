---
tags: [glossary]
---

# Glossary

One term, one line, **linked** to the notes that use it. Keep only your own definitions here, not copied ones. When a term appears in 3+ notes, it deserves its own atomic note.

- **Backpropagation** — algorithm to compute gradients via the chain rule. → [[03_deep_learning/_MOC]]
- **Attention** — mechanism that weights token relevance to each other. → [[04_nlp_and_transformers/_MOC]]
- **RAG** — Retrieval-Augmented Generation. → [[05_llm_engineering/_MOC]]
- **RLHF** — Reinforcement Learning from Human Feedback: aligning model outputs with human preferences. → [[05_llm_engineering/_MOC]]
- **DPO** — Direct Preference Optimization: aligning models without a separate reward model. → [[05_llm_engineering/_MOC]]
- **RoPE** — Rotary Position Embedding: encoding token positions via rotation matrices. → [[04_nlp_and_transformers/_MOC]]
- **RMSNorm** — Root Mean Square Layer Normalization: a simpler, faster alternative to LayerNorm. → [[04_nlp_and_transformers/_MOC]]
- **MLOps** — ML Operations: the practice of deploying, monitoring, and maintaining ML models in production. → [[06_production_ai/_MOC]]
- **Entropy** — measure of uncertainty in a probability distribution; minimum bits needed to encode a distribution. → [[01_foundations/_MOC]]
- **Cross-entropy** — loss function measuring difference between two probability distributions; the de facto loss for classification and language modeling. → [[01_foundations/_MOC]], [[04_nlp_and_transformers/_MOC]]
- **KL divergence** — Kullback–Leibler divergence: asymmetric measure of how one distribution diverges from another; foundation of DPO and variational inference. → [[01_foundations/_MOC]], [[05_llm_engineering/_MOC]]
- **Scaling Laws** — empirical relationships between model size, data size, compute, and performance; guide optimal resource allocation. → [[04_nlp_and_transformers/_MOC]]
- **KV cache** — Key-Value cache: stores attention keys/values from previous tokens to avoid recomputation during autoregressive generation. → [[04_nlp_and_transformers/_MOC]], [[05_llm_engineering/_MOC]]
- **FlashAttention** — IO-aware exact attention algorithm that dramatically reduces memory reads/writes, enabling long-context Transformers. → [[04_nlp_and_transformers/_MOC]]
- **Masked Language Modeling (MLM)** — BERT-style training: predict masked tokens using bidirectional context. → [[04_nlp_and_transformers/_MOC]]
