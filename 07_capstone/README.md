---
tags: [moc, phase/7, capstone]
---

# Capstone — Building a micro-LLM from Scratch

The goal is not to compete with GPT or Claude. It is to **replicate their architectural foundation** (decoder-only Transformer) at a minuscule scale, understanding every single component — because *understanding* is the real deliverable. This is also the portfolio piece that sets you apart: very few can say "I built an LLM from scratch and can explain it line by line."

## Distinctive idea (optional but strong)
Instead of the usual TinyShakespeare, train the model on **your own English corpus** — for example, historical/academic texts from a domain you already work with. A micro-LLM that "speaks" the English of a specific domain is far more memorable in a portfolio than yet another Shakespeare generator. (Start with TinyShakespeare to validate the pipeline, then swap.)

## Pipeline (what you build, in order)
1. **Data** → corpus selection, cleaning, train/val split. (`data/`)
2. **Tokenizer** → your own BPE, saved and versioned. (`src/tokenizer.py`)
3. **Model** → decoder-only: embedding + positional (RoPE) + N blocks (causal attention + MLP) + RMSNorm + output head with weight tying. (`src/model.py`)
4. **Training** → cross-entropy loss, AdamW, scheduler, gradient clipping, checkpoint, metric logging. (`src/train.py`)
5. **Generation** → sampling with temperature / top-k / top-p. (`src/generate.py`)
6. **Experiments** → tracked ablations. (`experiments/`)
7. **Writeup** → [[writeup]]: all choices and the *why*.

## Architectural parity with modern models
| Component | "Classic" choice (GPT-2) | Modern choice (Llama/Mistral) | Your choice |
|---|----|----|----|----|
| Positional | Learned absolute | **RoPE** | *to decide* |
| Normalization | Post LayerNorm | **Pre RMSNorm** | *to decide* |
| MLP activation | GELU | **SwiGLU** | *to decide* |
| Attention | MHA | MHA / **GQA** | *to decide* |

Document in the writeup **why** you choose each option — that is the interview question.

## Reference resources
- Sebastian Raschka — *Build a Large Language Model (From Scratch)* + official repo.
- Andrej Karpathy — `nanoGPT`, `minGPT`, `llm.c`; videos *Let's build GPT* and *Let's reproduce GPT-2*.
- Papers for modern choices: RoPE, RMSNorm, SwiGLU, GQA (Llama / Mistral series).

## Definition of "done" (graduation)
- [ ] The pipeline runs end-to-end on your corpus.
- [ ] The model generates **domain-coherent text**.
- [ ] A writeup exists explaining every architectural choice.
- [ ] You can sustain an **oral defense**: "why RMSNorm and not BatchNorm?" → confident answer.

## Hardware
A 1–10M parameter model trains even on CPU/laptop (minutes–hours on TinyShakespeare).
For larger corpora: local GPU or free Colab/Kaggle.
