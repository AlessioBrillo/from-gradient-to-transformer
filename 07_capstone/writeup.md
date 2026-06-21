---
tags: [phase/7, capstone, writeup]
---

# Writeup — micro-LLM: Quantifying the Italian Tokenization Tax

Final document: explain the model and results as if you had to defend them in an interview or conference poster session.

## 1. Thesis and Motivation
- The "Italian tokenization tax": English-centric tokenizers split Italian into 1.3–1.6× more tokens per word.
- Why this matters: more tokens → slower training, higher inference cost, shorter effective context.
- Our approach: build an Italian-optimized tokenizer and measure the effect end-to-end.

## 2. Tokenizer Analysis (Exp 1)
- Tokenizer training details (BPE vs Unigram, vocab sizes, corpus).
- Fertility, Rényi efficiency, and compression ratio on Italian vs English.
- Comparison to reference tokenizers (GPT-2, Mistral, Gemma, Llama-3, Minerva).
- Qualitative examples of Italian over-segmentation (verb conjugations, clitics).

## 3. Micro-LM Pretraining (Exp 2)
- Architecture: number of blocks, hidden dimensions, attention heads, positional encoding.
- Training: optimizer, scheduler, batch size, learning rate, total tokens seen.
- Tokenizer ablation results: bits-per-byte, tokens-to-convergence.
- Generated text samples (qualitative).

## 4. Positional Encoding Ablation (Exp 3)
- Sinusoidal vs learned vs RoPE: which works best at micro scale?
- Discussion: why RoPE is the modern default and whether it matters at 10–50M params.

## 5. Downstream Evaluation (Exp 4)
- Task: UINAUIL / ItaCoLA.
- Fine-tuning details.
- Results with mean ± std over ≥3 seeds.

## 6. Limitations
- Micro-scale only: findings may not transfer to 7B+ models.
- Single corpus family (web + Wikipedia).
- Generative evaluation is limited.
- ItaCoLA license caveat.

## 7. Related Work
- Minerva (Orlando et al., 2024) — Italian LLMs from scratch.
- SAVA (Moroni et al., 2025) — tokenizer adaptation.
- TinyStories (Eldan & Li, 2023) — micro-scale methodology.
- Scaling Laws (Kaplan et al., 2020; Hoffmann et al., 2022).

## 8. What I Truly Understood
- The most important section: the intuition that stays with you after building everything.
