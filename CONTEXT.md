# CONTEXT — From Gradient to Transformer to Circuit

Single-context domain map for this repo. Read this before touching `src/`, the
capstone, or any portfolio number. Vocabulary here is canonical: use these terms,
not synonyms.

## What this repo is

An Obsidian learning vault bolted to a working mechanistic-interpretability
research codebase. The thesis: train a small decoder-only transformer from
scratch, then reverse-engineer what it actually learned, with **every public
number traced to a committed run manifest**.

## Vocabulary

| Term | Meaning here |
|---|---|
| **Rung** | One experiment on the capstone ladder (1–5; Rung 6 descoped 2026-08-01). Lives in `src/experiments/expN_*.py`. |
| **Manifest** | `results/<experiment>.json` written by `src/results.py::ResultsManifest`. Carries seeds, args, per-seed metrics, aggregate (mean/std/min/max/n), wall clock, git SHA + dirty flag, device, param count. |
| **Ledger** | `portfolio/RESULTS.md` — the Honesty Ledger. Audit findings, retractions, and pending items. The authority on what is true. |
| **Claim** | Any public number. A claim is *backed* only if a `<!-- manifest: ... -->` tag in a tracked document resolves to a tracked, non-empty manifest. `make verify-claims` enforces this. |
| **verify-claims** | `python -m src.results verify`. Enforces: tag resolves, manifest seeded, aggregate non-empty, figures exist and are tracked, every manifest is cited, numbers do not drift from their manifest. |
| **Quick / Standard scale** | `--quick` is a smoke config (minutes, CPU). `--standard` is the canonical config recorded in the Makefile — the single source of truth for "standard scale". |
| **Grokking (REPRODUCED)** | A run reaching val accuracy ~1.0 with a **sparse** Fourier embedding (the Nanda et al. circuit). The Rung 2 verdict since 2026-10-14, measured by the energy metric. The 2026-08-11 NO-GROK label was an L1-metric artifact — retracted; see the Honesty Ledger. |
| **energy_sparse** | The post-audit sparsity criterion: whether the frequencies holding 90% of the embedding *energy* number < P/2. Replaces the L1-mass k99, which misclassifies noisy sparse embeddings as dense (audit 2026-10-08; reversal 2026-10-14). |
| **Induction head** | An attention head attending from the current query `q` to the token **after the previous occurrence of the current token** — on this repo's `prefix + prefix` task, the key `q-(L-1)`. Detected by the shared detector (`src/experiments/induction_detection.py`): induction mass ≥ 0.3 **and** a K-composition score ≥ 0.4 with an earlier layer. The previous "diag+1" detector measured `q-1` (the previous token) and the "0/8" counts it produced were retracted on 2026-10-19 — see the Honesty Ledger. |
| **Prefix-copying head** | What the standard-scale run actually found (2026-10-20): 2–3 heads per seed with a copy-offset mass of 0.95, all in the first layer, K-composition 0.05 — and the dissociation probe puts the copy on the **fixed offset**, not on the previous occurrence of the same token. On a perfectly periodic task the two are the same function in-distribution; only the probe (a second half that is a permuted copy of the prefix) can tell them apart, and it says the copy is positional. |
| **Variable-distance task** | The content-based task of ADR-0033: a key of distinct tokens, verbatim copy blocks whose source windows and positions are resampled per sequence, so the distance between a token and its previous occurrence changes from block to block. The best single fixed offset explains 17.6% of its copy queries, so a fixed-offset head cannot solve it and the content hypothesis is testable. `src/experiments/induction_tasks.py`. |
| **Copy query** | A position `q` where "copy the token that followed the previous occurrence" is the right answer: `tokens[q+1] == tokens[prev(q)+1]`. Derived from the tokens alone, so the detector never has to trust the generator. |
| **Superposition** | More features than dimensions, represented as non-orthogonal directions. Rung 3 is the only fully reproduced rung. |
| **k₉₀ / k₉₉** | Number of Fourier frequencies needed to hold 90% / 99% of embedding energy. `k₉₉ < P/2` is the sparsity criterion. |
| **P** | Modulus of the modular-addition task (P=113 is the flagship scale). |

## Rung → module map

| Rung | Module | Status |
|---|---|---|
| 1 Prefix-copying heads | `src/experiments/exp1_induction_heads.py` | **A head forms at standard scale (GPU, 3 seeds, 2026-10-20)** and the causal interventions land (ablation 0.44, path patching 0.82) — but the copy is *positional*, not content-based: the periodic task admits the shortcut. The content-based task that removes it is pre-registered (ADR-0033); its run is the open item of issue #200 |
| 2 Grokking (flagship) | `src/experiments/exp2_grokking.py` | **REPRODUCED 2026-10-14**: sparse circuit on the Nanda protocol and the repo protocol, GPU, 3 seeds each |
| 3 Superposition | `src/experiments/exp3_superposition.py` | **Fully reproduced** (the first rung to be; Rung 2 followed on 2026-10-14) |
| 4 Circuit patching | `src/experiments/exp4_circuit_patching.py` | **The cascade ran end to end on Rung 1's own checkpoint**: head ablation 0.4445 ± 0.0425, path patching 0.8215 ± 0.1255 — on a prefix-copying head, so it validates the method, not yet an induction circuit |
| 5 SAE dashboard | `src/experiments/exp5_sae_dashboard.py` | Synthetic reproduces; on real activations the dictionary is sparse (L0 3.0%) but ~8× too wide, with 78% of its features dead |
| 6 Automated circuits | — | **Descoped 2026-08-01** |

The manifests behind that table, one per rung: Rung 1
<!-- manifest: results/induction_standard.json -->, Rung 2
<!-- manifest: results/grokking_nanda_p113.json -->, Rung 3
<!-- manifest: results/exp3_superposition.json -->, Rung 4
<!-- manifest: results/exp4_standard.json -->, Rung 5
<!-- manifest: results/exp5_real_activations.json -->.

Shared model: `src/models/decoder_only_transformer.py` (RMSNorm + RoPE + causal
multi-head attention + KV cache). Experiments `exp1`–`exp5` use their own local
model classes; `exp6` (capstone) uses the shared one.

## Repo map

```
CONTEXT.md            ← this file
docs/adr/             ← dated architecture/research decisions (0001–0033)
portfolio/RESULTS.md  ← Honesty Ledger: the authority on what is true
src/results.py        ← manifests + verify-claims
src/experiments/      ← one module per rung
scripts/              ← plotting, site build, external-run pinning, vault checks
configs/              ← YAML configs for exp6 and the phase-diagram sweep
checklists/           ← reproducibility checklist, gate debt
07_capstone/          ← capstone plan, execution log, writeup, notes
```

## Conventions that bite

- **Everything runs from the repo root.** `FIGURES_DIR`, `RESULTS_DIR`, `CHECKPOINTS_DIR` are CWD-relative (`Path("figures")`, `Path("results")`, …). Run experiments as `uv run python -m src.experiments.expN_*` from the root.
- **`scripts/` is first-class and is linted.** It exports no package; tests import it as an implicit namespace package.
- **This is not a distributable package.** `pyproject.toml` has no `[build-system]`; the code is used in-place via `uv run`.
- **Never push to `main`.** Work on `dev`, merge by PR with CI green.

## Open decisions

Current status lives in `portfolio/RESULTS.md` and the `v1.0` GitHub milestone.
Do not re-derive status from the ADR ledgers (0001–0030 are historical and closed,
see `docs/adr/0031-closure.md`).
