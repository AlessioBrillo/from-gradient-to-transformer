# From Gradient to Transformer to Circuit

<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/commits/main"><img src="https://badgen.net/github/last-commit/AlessioBrillo/from-gradient-to-transformer" alt="GitHub last commit"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/markdown-lint.yml"><img src="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/markdown-lint.yml/badge.svg" alt="Markdown Lint"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/python-ci.yml"><img src="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/python-ci.yml/badge.svg" alt="Python CI"></a>

> **Thesis**: I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns. This repository demonstrates end-to-end research capability in mechanistic interpretability — training small models, forming causal hypotheses about their internals, and testing those hypotheses with activation patching, ablations, and sparse dictionary learning.

---

## Headline Result

**The grokking flagship is reproduced — the sparse Fourier circuit is real (Rung 2,
2026-10-14).** Trained on the Nanda-faithful protocol at P=113 (40k full-batch steps,
3 seeds, GPU), the model reaches **val accuracy 0.9999 ± 0.0002** while its embedding
energy concentrates in **5.7 ± 1.2 of 56 frequencies** — the sparse circuit Nanda et al.
describe, detected by the post-audit energy metric on 3/3 seeds. The repository's
2026-08-11 "NO-GROK" verdict was an artifact of the L1-mass metric the 2026-10-08 audit
had falsified: on the *same embeddings* the old reader still says 109–110 of 113
frequencies. The mechanism was sparse all along; the classifier was wrong.

It is the only rung that is fully reproduced. The others are reported as measured, negatives
included:

| Rung | Where it stands |
|------|-----------------|
| 1 Induction heads | The head counts this repository used to publish are **retracted** (2026-10-19): the detector measured the previous-token offset, so "0/8" was a statement about the detector, not the model. The corrected detector and the standard-scale GPU run (`make remote-run-induction`) are the open work. A matched fixed-vs-fresh-batches comparison is the one solid finding (53.5% vs 0.45% validation accuracy). |
| 2 Grokking | ✅ **REPRODUCED 2026-10-14**: val accuracy 0.9999 ± 0.0002, sparse circuit (k_energy_90 = 5.7 ± 1.2 of 56) on both the Nanda protocol and the historical repo protocol, 3/3 seeds each. The 2026-08-11 NO-GROK was a metric artifact — retracted. |
| 3 Superposition | Phase transition reproduced (10/20 → 20/20 features represented; pentagon geometry at sparsity ≤ 0.1). |
| 4 Circuit patching | Activation patching runs cleanly; path patching is only unit-tested because there is no head to target. Since 2026-10-19 this rung analyses Rung 1's own checkpoint (`--from-checkpoint`) instead of training a second model. |
| 5 SAE | Synthetic data reproduces; on real activations reconstruction is good but dense (53% of features active). |

Read the Honesty Ledger in [`portfolio/RESULTS.md`](portfolio/RESULTS.md) before citing any
number from this repository: seven audits have now examined these claims — six found numbers
that were wrong or unbacked, the seventh reversed a negative verdict its own metric had
manufactured, and the latest (2026-10-19) retracted every head count this repository had
published because the detector behind them measured the wrong attention offset.
`make verify-claims` (run in CI) fails if a public number has no committed
manifest behind it.

**Live site:** <https://alessiobrillo.github.io/from-gradient-to-transformer/>

```bash
git clone https://github.com/AlessioBrillo/from-gradient-to-transformer
cd from-gradient-to-transformer
uv sync && make reproduce-quick  # smoke-test every rung in a few minutes
uv sync && make reproduce        # full-scale run, hours
```

---

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

★ — **Primary flagship, REPRODUCED 2026-10-14** (sparse Fourier circuit, GPU, 3 seeds, both protocols — see [RESULTS](portfolio/RESULTS.md)).

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
- [x] **Phase 6 — Production AI** (reframed: reproducible research infra — pinned env, manifests, `verify-claims` in CI; W&B closed-with-reason, the compiled paper PDF now ships with the site)
- [~] **Phase 7 — Capstone: train + reverse-engineer** (model built, rungs 1-5 implemented; Rung 2 reproduced on GPU 2026-10-14; the planned 3×20k joint run executed 2026-10-14 — the modular/induction dissociation persists at full budget; the standard-scale induction run is in progress)

See [03_progress-log](00_meta/03_progress-log.md) for the dated journal and [02_skill-tree](00_meta/02_skill-tree.md) for the complete skill tree.

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

Writing conventions, tags, and naming: [04_conventions](00_meta/04_conventions.md).

---

## Citation

See [`CITATION.cff`](CITATION.cff) (GitHub's "Cite this repository" button).

---

## License

Notes and code released under the MIT License (see `LICENSE`). External resources remain with their respective authors: this repository contains only the author's notes and code. Dataset licenses are documented inline with each corpus reference.
