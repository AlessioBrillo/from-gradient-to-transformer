---
tags: [moc, phase/7, capstone]
---

# Capstone — micro-LLM from Scratch (Italian Corpus)

The capstone converges everything from Phases 1–6 into a trained, evaluated decoder-only Transformer on an Italian corpus. This is the primary research vehicle for the thesis: **quantifying the Italian tokenization tax at micro scale.**

## Thesis (one sentence)

> Quantify and partially close the "Italian tokenization tax" at micro scale by building a decoder-only Transformer from scratch with an Italian-optimized tokenizer, and measure the effect on fertility, perplexity, and a downstream Italian NLU task.

## Experiment Ladder

Do in order; each produces a defensible result:

1. **Tokenizer fertility study** — Train Italian BPE/Unigram tokenizers at several vocab sizes (8k/16k/32k); measure fertility, Rényi efficiency, and compression ratio on Italian vs English; compare to GPT-2/Mistral/Gemma tokenizers. This is the headline result.

2. **Micro-LM pretraining with tokenizer ablation** — Train two identical decoder-only models (~10–50M params) on the same Italian corpus, differing only in tokenizer; compare bits-per-byte and tokens-to-convergence.

3. **Positional encoding ablation** — Sinusoidal vs learned vs RoPE on the same micro-LM.

4. **Downstream evaluation** — Fine-tune/probe on one Italian NLU task (UINAUIL or ItaCoLA); report mean ± std over seeds.

## Pipeline

```
07_capstone/
├── data/          ← corpus selection, train/val split
├── src/
│   ├── tokenizer.py   ← BPE tokenizer
│   ├── model.py       ← decoder-only Transformer
│   ├── train.py       ← training loop
│   └── generate.py    ← sampling
├── experiments/   ← tracked ablations
├── notebooks/     ← exploratory analysis
└── writeup.md     ← architectural decisions and final report
```

Shared research code lives in `src/` at the repository root (models, experiments, training, generation, reproducibility). Capstone-specific code and notebooks live here.

## Architectural Decisions

| Component | Available Options | Selection (to decide) |
|-----------|------------------|----------------------|
| Positional encoding | Sinusoidal / Learned / RoPE | — |
| Normalization | Post LayerNorm / Pre RMSNorm | — |
| MLP activation | GELU / SwiGLU | — |
| Attention | MHA / MQA / GQA | — |

Each choice must be justified in the writeup. The positional encoding ablation (Exp 3) will inform the final decision.

## Definition of "Done"

- [ ] Pipeline runs end-to-end on an Italian corpus
- [ ] Model generates coherent Italian text
- [ ] Exp 1–4 completed and results documented in [[portfolio/RESULTS]]
- [ ] Mini-paper (LaTeX) written with abstract, method, experiments, ablations, limitations, references
- [ ] Reproducibility harness: `uv sync && make reproduce` regenerates all figures
- [ ] Oral defense ready: "why RMSNorm and not BatchNorm?" → confident answer

## Datasets (primary candidates)

| Dataset | Language | License | Size |
|---------|----------|---------|------|
| PAISÀ (Lyding et al., 2014) | Italian | CC-BY / CC-BY-SA / NC variants | ~250M words |
| Italian Wikipedia | Italian | CC BY-SA | ~variable subset |
| Clean Italian mC4 (Sarti & Nissim, 2024) | Italian | ODC-BY | ~215 GB raw (subset) |
| CulturaX (Italian) | Italian | — | used by Minerva |

All licenses are explicitly stated in dataset references. Only subsets are used.

## Hardware

~10–50M parameter model: trains on a single GPU (Colab / local) in hours. Tokenizer experiments run on CPU.

## Reference Resources

- Karpathy — `nanoGPT`, `minGPT`, `llm.c`; videos *Let's build GPT* and *Let's reproduce GPT-2*
- Raschka — *Build a Large Language Model (From Scratch)*
- Vaswani et al., *Attention Is All You Need* (NeurIPS 2017)
- Su et al., *RoFormer: Enhanced Transformer with Rotary Position Embedding* (2024)
- Orlando et al., *Minerva LLMs* (CLiC-it 2024) — Italian LLM reference point
- Moroni et al., *Optimizing LLMs for Italian* (Findings of NAACL 2025) — tokenizer adaptation
- Eldan & Li, *TinyStories* (2023) — micro-scale LM methodology
