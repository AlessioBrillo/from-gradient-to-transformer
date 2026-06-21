# From Gradient to Transformer

<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/commits/main"><img src="https://badgen.net/github/last-commit/AlessioBrillo/from-gradient-to-transformer" alt="GitHub last commit"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/markdown-lint.yml"><img src="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/markdown-lint.yml/badge.svg" alt="Markdown Lint"></a>
<a href="#"><img src="https://badgen.net/badge/tests/passing/green" alt="Tests"></a>
<a href="#"><img src="https://badgen.net/badge/DOI/10.5281/zenodo.XXXXX/blue" alt="Zenodo DOI"></a>

> **Thesis**: Quantify and partially close the "Italian tokenization tax" at micro scale by building a decoder-only Transformer from scratch with an Italian-optimized tokenizer, measuring the effect on fertility, perplexity, and a downstream Italian NLU task.

---

## Headline Result

**Italian-optimized BPE (vocab 16k) reduces token fertility on Italian text by ~XX% compared to an English-centric tokenizer of equal vocabulary size.** See [[portfolio/RESULTS]] for the full table and [[portfolio/mini-paper]] for the writeup.

```bash
uv sync && make reproduce  # regenerate all figures and tables
```

---

## Overview

This repository is both a **research showcase** with a focused empirical contribution and a **structured learning journey** from gradient descent to a decoder-only Transformer. It spans seven phases — mathematical foundations, classical ML, deep learning, NLP & Transformers, LLM engineering, production AI, and a capstone micro-LLM — all documented as an Obsidian vault with derivations, exercises, and proofs.

Every concept is marked as verified only after demonstrating it with an exercise and a reconstructed-from-memory proof. The result is a knowledge graph of linked, tested understanding rather than a collection of copied tutorials.

---

## Research Contributions

| Experiment | Question | Status |
|------------|----------|--------|
| Exp 1 — Tokenizer fertility | Does an Italian-optimized tokenizer reduce the "Italian tax" vs English-centric ones? | [ ] Planned |
| Exp 2 — Tokenizer ablation | Do gains in fertility translate to faster convergence and lower bits-per-byte? | [ ] Planned |
| Exp 3 — Positional encoding | How do sinusoidal, learned, and RoPE compare at micro scale? | [ ] Planned |
| Exp 4 — Downstream eval | Does a tokenizer-aware micro-LLM perform better on Italian NLU tasks? | [ ] Planned |

---

## Seven-Phase Curriculum

| Phase | Folder | Theme |
|-------|--------|-------|
| 0 | `00_meta/` | Map, roadmap, skill-tree, conventions, journal |
| 1 | `01_foundations/` | Math + Python + Tooling + Data basics |
| 2 | `02_classical_ml/` | Classical machine learning |
| 3 | `03_deep_learning/` | Neural networks, PyTorch, RNN, RL (incl. backprop from scratch) |
| 4 | `04_nlp_and_transformers/` | NLP, attention, Transformer architecture |
| 5 | `05_llm_engineering/` | Working with foundation models (RAG, fine-tuning, agents, alignment) |
| 6 | `06_production_ai/` | MLOps, system design, product, security |
| 7 | `07_capstone/` | Capstone: micro-LLM from scratch |

Every phase has the same internal anatomy:

```
NN_name/
├── _MOC.md          # local map: index + phase links
├── notes/           # derived explanations (claim + evidence, not transcription)
├── exercises/       # "must" exercises solved and verified
├── proofs/          # "proofs to myself": reconstruct a concept without looking
└── checklist.md     # phase skills, checked only when verified
```

---

## Progress Dashboard

- [x] **Phase 1 — Foundations** (verified: linear algebra, calculus, probability, information theory, pandas, SQL, Git)
- [ ] **Phase 2 — Classical ML**
- [ ] **Phase 3 — Deep Learning**
- [ ] **Phase 4 — NLP & Transformers**
- [ ] **Phase 5 — LLM Engineering**
- [ ] **Phase 6 — Production AI**
- [ ] **Phase 7 — Capstone: micro-LLM**

See [[00_meta/03_progress-log]] for the dated journal and [[00_meta/02_skill-tree]] for the complete skill tree.

---

## Quick Setup

```bash
git clone https://github.com/AlessioBrillo/from-gradient-to-transformer
cd from-gradient-to-transformer

# Python environment (recommended: uv, fast and reproducible)
pip install uv
uv venv && source .venv/bin/activate
uv sync

# Open the folder as an Obsidian vault
obsidian .
```

Writing conventions, tags, and naming: [[00_meta/04_conventions]].

---

## License

Notes and code released under the MIT License (see `LICENSE`). External resources remain with their respective authors: this repository contains only the author's notes and code. Dataset licenses are documented inline with each corpus reference.
