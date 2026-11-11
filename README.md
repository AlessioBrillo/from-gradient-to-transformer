# From Gradient to Transformer to Circuit

<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/commits/main"><img src="https://badgen.net/github/last-commit/AlessioBrillo/from-gradient-to-transformer" alt="GitHub last commit"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/markdown-lint.yml"><img src="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/markdown-lint.yml/badge.svg" alt="Markdown Lint"></a>
<a href="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/python-ci.yml"><img src="https://github.com/AlessioBrillo/from-gradient-to-transformer/actions/workflows/python-ci.yml/badge.svg" alt="Python CI"></a>

> **CI gate**: the repository's gate is the Woodpecker pipeline in `.woodpecker/ci.yml`, run locally with `ci-local`. The GitHub Actions badges above are auxiliary checks, not the merge gate.

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

**Rung 2 is fully reproduced (2026-10-14).** The others are reported as measured, negatives
included:

| Rung | Where it stands |
|------|-----------------|
| 1 Prefix-copying heads | A head **does** form at standard scale (GPU, 3 seeds, 3000 epochs): 2–3 heads per seed, copy-offset mass 0.945, ablation effect 0.44, path-patch effect 0.82 — but the dissociation probe shows the copy follows a **fixed offset**, not the previous occurrence of the same token, so it is a *prefix-copying* head, not an induction head (the repeated-token task is perfectly periodic and hands the model that shortcut). The retracted "0 / 8" was a detector artifact: the detector measured the previous-token offset. The fixed-vs-fresh-batches comparison remains the one solid finding (53.5% vs 0.45% validation accuracy). |
| 1b Content-based induction | The task that removes the shortcut ran on GPU (2026-11-09, 3 seeds × 3000 epochs). **Behaviour: content-based on 3/3 seeds** — copy accuracy 0.9976–1.0000 (non-modal 0.9972–1.0000) against a 15.5–16.5% fixed-offset baseline — and **causally carried by one head on 3/3 seeds** (single-head ablation drop 0.93–0.99). The pre-registered *per-head* rule, however, confirms a head on 1/3 seeds only (content mass 0.09–0.12 < 0.30; K-composition 0.06–0.07 < 0.40), so the pre-registered verdict is **PARTIAL** and the causal addendum's run label is NEGATIVE by the frozen majority rule. Two verdicts, kept apart, with the mechanism report published — see [RESULTS](portfolio/RESULTS.md). |
| 2 Grokking | ✅ **REPRODUCED 2026-10-14**: val accuracy 0.9999 ± 0.0002, sparse circuit (k_energy_90 = 5.7 ± 1.2 of 56) on both the Nanda protocol and the historical repo protocol, 3/3 seeds each. The 2026-08-11 NO-GROK was a metric artifact — retracted. |
| 3 Superposition | Phase transition reproduced (10/20 → 20/20 features represented; pentagon geometry at sparsity ≤ 0.1). |
| 4 Circuit patching | ✅ The cascade ran end to end on Rung 1's own checkpoint: head ablation 0.4445 ± 0.0425, path patching 0.8215 ± 0.1255 — the first end-to-end path-patching result against a real head (a prefix-copying one: it validates the method, not yet an induction circuit). |
| 5 SAE | Synthetic data reproduces; on real activations the dictionary is sparse (L0 3.0% of 512 active) but ~8× wider than the 64-dimensional residual stream, with 78% of its features never firing — the dictionary size, not the sparsity, is the open question. |

The manifests behind that table: Rung 1
<!-- manifest: results/induction_standard.json -->, Rung 2
<!-- manifest: results/grokking_nanda_p113.json -->, Rung 3
<!-- manifest: results/exp3_superposition.json -->, Rung 4
<!-- manifest: results/exp4_standard.json -->, Rung 5
<!-- manifest: results/exp5_real_activations.json -->, Rung 1 fixed-vs-fresh
<!-- manifest: results/exp1_induction_fixed_batches.json -->,
<!-- manifest: results/exp1_induction_fresh_batches.json -->, Rung 1b content task
<!-- manifest: results/induction_content.json -->, Rung 1b causal addendum
<!-- manifest: results/exp4_content.json -->.

Read the Honesty Ledger in [`portfolio/RESULTS.md`](portfolio/RESULTS.md) before citing any
number from this repository: eleven audits have now examined these claims — they found numbers
that were wrong or unbacked, a negative verdict its own metric had manufactured, and a
content-task experiment that could not have produced a verdict until its instrument was fixed
before the GPU run — and, on 2026-11-11, a **published verdict that the code could not
reproduce**.
`make verify-claims` (run in CI) fails if a claim tag has no committed
manifest behind it; `make docs-audit` checks the prose around those tags.

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
- [~] **Phase 5 - LLM Engineering** (instrumentation done: hooks, deterministic inference, activation harvesting, circuit datasets; nnsight pending - not installed, and the capture protocol the repo uses does not need it)
- [~] **Phase 6 - Production AI** (reproducible research infra - pinned env, manifests, `verify-claims` in CI; W&B descoped 2026-09-08, HF Spaces descoped 2026-10-11, the compiled paper PDF ships with the site)
- [~] **Phase 7 — Capstone: train + reverse-engineer** (model built, rungs 1-5 implemented; Rung 2 reproduced on GPU 2026-10-14; the planned 3×20k joint run executed 2026-10-14 — the modular/induction dissociation persists at full budget; the standard-scale induction run landed 2026-10-20 and found a *prefix-copying* head; the content-based task of issue #200 ran on GPU 2026-11-09 — the copy is content-based on 3/3 seeds and causally carried by a single head, but the pre-registered per-head rule confirms a head on 1/3 seeds, so the verdict is PARTIAL and the open question is now *why that head does not put its attention mass on the content key*)

See [03_progress-log](00_meta/03_progress-log.md) for the dated journal and [02_skill-tree](00_meta/02_skill-tree.md) for the complete skill tree.

---

## Quick Setup

```bash
git clone https://github.com/AlessioBrillo/from-gradient-to-transformer
cd from-gradient-to-transformer

# Python environment (recommended: uv, fast and reproducible)
# Tested on Python 3.12 (CI, mypy, ruff target, uv.lock all resolve to 3.12).
pip install uv
uv venv --python 3.12 && source .venv/bin/activate
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
