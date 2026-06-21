---
tags: [portfolio, model-card]
---

# Model Card — micro-LLM

## Model Overview

- **Name**: micro-LLM (from-gradient-to-transformer)
- **Architecture**: Decoder-only Transformer
- **Parameters**: ~10–50M
- **Tokenizer**: BPE / Unigram (vocab size TBD)
- **Language**: Italian (primary), English (baseline comparison)
- **License**: MIT

## Intended Use

Research and educational demonstration of the effect of tokenizer design on language model efficiency for Italian. Not intended for production use.

## Training Data

- PAISÀ corpus (CC-licensed Italian web text, ~250M words)
- Italian Wikipedia (CC BY-SA)
- Clean Italian mC4 subset (ODC-BY)
- English baseline: corresponding English Wikipedia / mC4 subsets

See dataset references in the mini-paper for full details and licenses.

## Factors

- **Language bias**: The model is optimized for Italian and may underperform on other languages.
- **Domain bias**: Training data is primarily web text and Wikipedia; performance on domain-specific Italian (legal, medical, literary) may vary.

## Evaluation

| Benchmark | Task | Metric |
|-----------|------|--------|
| UINAUIL | 6 Italian NLU tasks | Accuracy / F1 |
| ItaCoLA | Italian acceptability | Matthews correlation |

All results reported as mean ± std over ≥3 seeds.

## Limitations

- Micro-scale model (~10–50M params) — capabilities do not match large-scale LLMs.
- Single corpus family (web + Wikipedia) — may not generalize to specialized domains.
- Generative evaluation is limited; focus is on tokenizer effects rather than fluency.
