---
tags: [portfolio, results]
---

# Results — Headline Findings

> **Thesis**: Quantify and partially close the "Italian tokenization tax" at micro scale by building a decoder-only Transformer from scratch with an Italian-optimized tokenizer, measuring the effect on fertility, perplexity, and a downstream Italian NLU task.

---

## Exp 1 — Tokenizer Fertility Study

**Question**: Does an Italian-optimized tokenizer reduce the "Italian tax" compared to English-centric tokenizers of equal vocabulary size?

**Status**: [ ] Planned

| Tokenizer | Vocab | Italian Fertility (↓) | English Fertility (↓) | Ratio (It/En) |
|-----------|-------|----------------------|-----------------------|----------------|
| GPT-2 | 50,257 | — | — | — |
| Mistral-7B | 32,768 | — | — | — |
| Our BPE (English) | 16,000 | — | — | — |
| **Our BPE (Italian-optimized)** | **16,000** | **—** | **—** | **—** |

*Reference: Mistral-7B BPE tokenizer has fertility ~1.87 on Italian vs ~1.32 on English (Orlando et al., CLiC-it 2024). Our target: demonstrate that an Italian-optimized tokenizer of equal vocab size closes this gap.*

---

## Exp 2 — Tokenizer Ablation on Micro-LM

**Question**: Do fertility gains translate to measurable improvements in training efficiency?

**Status**: [ ] Planned

| Tokenizer | Bits-per-Byte (↓) | Tokens to Convergence | Wall Time |
|-----------|-------------------|----------------------|-----------|
| English-centric BPE | — | — | — |
| Italian-optimized BPE | — | — | — |

---

## Exp 3 — Positional Encoding Ablation

**Question**: How do sinusoidal, learned, and RoPE compare at micro scale?

**Status**: [ ] Planned

| Encoding | Validation Perplexity (↓) |
|----------|--------------------------|
| Sinusoidal | — |
| Learned | — |
| RoPE | — |

---

## Exp 4 — Downstream Italian NLU

**Question**: Does tokenizer-aware pretraining improve performance on Italian NLU tasks?

**Status**: [ ] Planned

| Model | Task | Metric | Score (mean ± std) |
|-------|------|--------|-------------------|
| Baseline (English tokenizer) | — | — | — |
| Italian-optimized tokenizer | — | — | — |

---

## Reference Results (from primary literature)

| Source | Tokenizer | Italian Fertility | English Fertility | Corpus |
|--------|-----------|-------------------|-------------------|--------|
| Orlando et al., CLiC-it 2024 | Mistral-7B BPE | 1.87 | 1.32 | CulturaX |
| Orlando et al., CLiC-it 2024 | Mistral-7B BPE | 2.05 | 1.57 | Wikipedia |
| Moroni et al., NAACL 2025 | Gemma-7B | 1.42 | 1.18 | CulturaX |
| Moroni et al., NAACL 2025 | Llama-3-8B | 1.67 | 1.15 | CulturaX |
| Moroni et al., NAACL 2025 | Minerva-LLMs | 1.39 | — | CulturaX |

Our micro-scale results will differ in absolute numbers but should reproduce the *relative* Italian-vs-English gap pattern.
