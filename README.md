# From Gradient to Transformer to Circuit

<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/commits/main"><img src="https://badgen.net/github/last-commit/AlessioBrillo/from-gradient-to-transformer" alt="GitHub last commit"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/markdown-lint.yml"><img src="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/markdown-lint.yml/badge.svg" alt="Markdown Lint"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/python-ci.yml"><img src="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/python-ci.yml/badge.svg" alt="Python CI"></a>

> **Thesis**: I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns. This repository demonstrates end-to-end research capability in mechanistic interpretability — training small models, forming causal hypotheses about their internals, and testing those hypotheses with activation patching, ablations, and sparse dictionary learning.

---

## Headline Result

**Induction heads emerging causally in a 2-layer attention-only transformer**, with their
role verified by activation patching, path patching, and head ablation on
`src/models/decoder_only_transformer.py`. This is the fallback flagship, and currently the
strongest result with re-verified code: **grokking on modular addition is the primary
flagship but is not yet reproduced** — see `portfolio/RESULTS.md` for exactly what is and
isn't confirmed, and why. A validity pass on 2026-08-01 found and fixed real bugs in three
of five rungs' causal claims (wrong ablation site, wrong patch site, an internal metric
that silently disagreed with its own detection threshold); read the Honesty Ledger in
`portfolio/RESULTS.md` before citing any specific number from this repository.

```bash
cd from-gradient-to-transformer
uv sync && make reproduce-quick  # smoke-test every rung in a few minutes
uv sync && make reproduce        # full-scale run, hours
```

*Primary experiment (unreproduced):* `src/experiments/exp2_grokking.py` · *Strongest
verified result:* `src/experiments/exp1_induction_heads.py` +
`src/experiments/exp4_circuit_patching.py`

---

## Overview

This repository is both a **mechanistic interpretability research showcase** with a focused experimental arc and a **structured learning journey** from gradient descent to circuit-level understanding of transformer internals.

It spans seven phases — mathematical foundations, classical ML, deep learning, NLP & Transformers, LLM instrumentation, reproducible research infrastructure, and a capstone that combines training with reverse-engineering — all documented as an Obsidian vault with derivations, exercises, and proofs.

Every concept is marked as verified only after demonstrating it with an exercise and a reconstructed-from-memory proof. The result is a knowledge graph of linked, tested understanding rather than a collection of copied tutorials.

---

## Research Contributions

See `portfolio/RESULTS.md` for the authoritative, actively-maintained status table with
numbers, evidence, and open discrepancies — the table below is a quick pointer, not the
source of truth, because rung status changes faster than two files can be kept in lockstep
by hand.

| Experiment | Question |
|------------|----------|
| Rung 1 — Induction heads | Do induction heads emerge in a 2-layer attention-only transformer, and can I verify them causally? |
| Rung 2 — Grokking modular addition **★** | Can I reproduce the grokking phase transition and reverse-engineer the Fourier multiplication algorithm? |
| Rung 3 — Superposition geometry | How do features organize in a toy ReLU autoencoder under varying sparsity? |
| Rung 4 — Circuit patching | Can I find and causally validate a specific circuit via activation/path patching? |
| Rung 5 — Sparse autoencoder | Can I extract interpretable monosemantic features from a small model's residual stream? |

Rung 6 (automated circuit discovery vs. hand-found circuit) was descoped on 2026-08-01: its
placeholder implementation simulated the comparison with random draws instead of running
ACDC. See `07_capstone/research-plan.md` for the record.

★ — **Primary flagship (not yet reproduced).** See [[portfolio/RESULTS]] for the full table.

---

## Seven-Phase Curriculum

| Phase | Folder | Theme |
|-------|--------|-------|
| 0 | `00_meta/` | Map, roadmap, skill-tree, conventions, journal |
| 1 | `01_foundations/` | Math + Python + Tooling — with MI forward-links (residual stream as vector space, QK/OV as low-rank factorization) |
| 2 | `02_classical_ml/` | Classical ML — PCA as SAE ancestor, SVM margin as circuit intuition |
| 3 | `03_deep_learning/` | Neural networks, training dynamics, grokking-relevant phenomena (delayed generalization, weight decay) |
| 4 | `04_nlp_and_transformers/` | **LOAD-BEARING** — decoder-only transformer from scratch, QK/OV circuits, residual stream, induction heads, activation patching, logit lens |
| 5 | `05_llm_engineering/` | Model instrumentation — hooks, activation caching, deterministic inference, activation harvesting |
| 6 | `06_production_ai/` | Reproducible research infra — pinned environments, W&B tracking, `make reproduce`, CI smoke tests |
| 7 | `07_capstone/` | **Capstone: train + reverse-engineer** — build a decoder-only transformer and reverse-engineer its internals |

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

- [x] **Phase 1 — Foundations** (verified: linear algebra, calculus, probability, information theory, data tools)
- [x] **Phase 2 — Classical ML** (linear/logistic regression, trees/forests, SVM, PCA/k-means, CV/metrics, bias/variance)
- [x] **Phase 3 — Deep Learning** (micrograd, training dynamics, grokking, RNN/CNN breadth)
- [x] **Phase 4 — NLP & Transformers** (LOAD-BEARING for MI — QK/OV circuits, induction heads, activation patching, logit lens, TransformerLens)
- [x] **Phase 5 — LLM Engineering** (model instrumentation: hooks, deterministic inference, activation harvesting, circuit datasets)
- [ ] **Phase 6 — Production AI** (reframed: reproducible research infra)
- [~] **Phase 7 — Capstone: train + reverse-engineer** (model built, experiments implemented, results for rungs 1-5)

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
