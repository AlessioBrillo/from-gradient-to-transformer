# From Gradient to Transformer

<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/commits/main"><img src="https://img.shields.io/github/last-commit/AlessioBrillo/from-gradient-to-transformer" alt="GitHub last commit"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/markdown-lint.yml"><img src="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/markdown-lint.yml/badge.svg" alt="Markdown Lint"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer"><img src="https://img.shields.io/github/stars/AlessioBrillo/from-gradient-to-transformer?style=social" alt="GitHub Repo stars"></a>

> My documented journey from **zero to AI Engineer / ML Specialist**,
> with a final goal: **building a micro-LLM from scratch** with the same
> architectural foundation as GPT / Claude (decoder-only Transformer).

This is not a collection of copied tutorials. It is an **operational second brain**: every
lesson becomes a Markdown note, every concept a linked node in Obsidian, every skill a box
that is checked **only** after demonstrating it with an exercise and a "proof to myself."

> *"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."* — A. Karpathy.
> The philosophy is the same here: the value is not the note, it is the **graph** that emerges.

---

## How to Navigate

Open this folder as an **Obsidian vault**. The entry point is
[[00_meta/00_home]] (the map of content). From there you reach everything.

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
├── notes/           # lessons converted to .md (one note per concept)
├── exercises/       # "must" exercises solved by me
├── proofs/          # "proofs to myself": reconstruct a concept without looking
└── checklist.md     # phase skills, checked only when verified
```

---

## Progress Dashboard

Global status (update manually or with a Dataview query):

- [ ] **Phase 1 — Foundations**
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
git clone <this-repo> && cd from-gradient-to-transformer
# Python environment (recommended: uv, fast and reproducible)
pip install uv
uv venv && source .venv/bin/activate
# Open the folder as a vault in Obsidian: Open folder as vault
```

Writing conventions, tags, and naming: [[00_meta/04_conventions]].

---

## License

Notes and code released under the MIT License (see `LICENSE`). External resources remain
with their respective authors: this repo contains only **my** notes and **my** code.
