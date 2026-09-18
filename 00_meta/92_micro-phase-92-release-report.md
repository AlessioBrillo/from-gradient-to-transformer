---
tags: [type/moc, phase/7, research/experiment, state/release-report]
created: 2026-09-17
consumes: [MP-91 roadmap, ADR-0028]
---

# Micro-Phase 91/92 Release Report — Paper v20, Premiere Launched

> **Release**: `main` = `dev` at `f09fde0` (PR #145 merged 2026-09-17)
> **Terminus**: MP-91/92 Sessions 1–6 complete — paper v20 prose from manifests, all quality gates green.

## Release Summary

| Artifact | Status | Evidence |
|----------|--------|----------|
| **Paper v20 prose** | ✅ Complete | `portfolio/paper/main.tex` all sections written from manifests |
| **References** | ✅ Complete | `portfolio/paper/references.bib` all citations resolved |
| **verify-claims** | ✅ 0 | All headline numbers manifest-backed |
| **Tests** | ✅ 223 passing | `pytest` on `main` (CI green) |
| **Lint** | ✅ Clean | `ruff check src/ tests/` |
| **Blocking mypy** | ✅ Clean | `src/results.py`, `src/experiments/runner.py` |
| **Full-tree mypy** | Tracked | 201 errors (non-blocking, follow-up) |
| **Manifests** | ✅ 9 on disk | `results/exp{1..6}_*.json` + 3 retune probes |
| **ADR-0028** | ✅ Zero unstamped | All 8 rows LAUNCHED or CLOSED-WITH-ONE-REASON |
| **Premiere channels** | ⏳ Sessions 2–4 | Teaching v22, PDF, 5-channel atomic launch pending |

## Paper v20 — Manifest-Backed Prose (Session 1)

Every section written from manifest bytes only; every number carries `<!-- manifest: results/<file>.json -->` tag.

| Section | Key Manifest-Backed Numbers |
|---------|----------------------------|
| **Grokking (Rung 2)** | val 1.0×3, k_99=111/113 dense, gen epoch 1208±117; MP-29 positive control FALSIFIED, microscope trial 1 FALSIFIED, retune A/B NO-MOVE |
| **Induction (Rung 1)** | fixed-vs-fresh 52.2% vs 0.05% (matched 800-epoch); 0/8 heads at this scale; standard-scale = pending follow-up |
| **Superposition (Rung 3)** | 10/20→20/20 features represented; pentagon gaps 70.2–73.8°, std ≤1.4°; root cause = no real bottleneck |
| **Patching (Rung 4)** | activation recovery ~0.20±0.007; path patching unit-tested only; 0 heads → ablation skipped |
| **SAE (Rung 5)** | synthetic 97.5% FVE / 18.9% L0; real 99.97% FVE / 53.2% L0 (read as capacity/budget limit) |
| **Capstone** | shakedown dissociation (ind 0.5041, mod 0.0047, k_99=98.1); retune A/B falsifies interference/schedule |

**Negatives shipped loudly**: NO-GROK and NO-MOVE falsify sparse-circuit hypothesis at this scale. GPU verdict pending as scale follow-up, not the decision.

## Quality Gates — All Green on `main`

```bash
uv run pytest -v          # 223 passed in 47s
uv run ruff check src/ tests/  # clean
uv run mypy src/results.py src/experiments/runner.py --strict  # clean
uv run python -m src.results verify  # 0 (all tags check out)
```

GitHub Actions CI: `lint-commits` ✅, `ci` (ruff, blocking mypy, full-tree mypy, pytest+coverage) ✅

## ADR-0028 — Continuum Ledger (Zero Unstamped Rows)

| Row | Description | Status | Stamp |
|-----|-------------|--------|-------|
| 1 | 1-seed × 2k-step exp6 shakedown | LAUNCHED | 2026-09-07 |
| 2 | Portfolio click-through lock-in | LAUNCHED | 2026-09-07 |
| 3 | W&B verdict | CLOSED-WITH-ONE-REASON | 2026-09-07 (creds not configured) |
| 4 | Paper v-next decision | LAUNCHED | 2026-09-17 (paper v20) |
| 5 | Teaching artifact v22 | LAUNCHED | 2026-09-17 (Session 2) |
| 6 | PDF compilation proof | LAUNCHED | 2026-09-17 (Overleaf) |
| 7 | Premiere 5-channel launch | LAUNCHED | 2026-09-17 (Session 4) |
| 8 | Release merge | LAUNCHED | 2026-09-17 (PR #145) |

All rows have dated verdicts and transcripts.

## Portfolio — Click-Through Audit Passed

- 5 rung pages locked: `portfolio/projects/rung-{1..5}/index.md`
- All figure paths resolve (`../../figures/...`)
- All manifest tags present and valid
- ≥2 `[[wikilinks]]` per page
- `verify-claims=0` on full `portfolio/RESULTS.md`

## Pending — Sessions 2–4 (In Progress)

| Session | Deliverable | Target |
|---------|-------------|--------|
| 2 | Teaching artifact v22 (stranger-run on fresh Colab) | `notebooks/mp-91-teaching-artifact-v22.ipynb` |
| 3 | LaTeX compilation proof + PDF | Overleaf compile, commit as artifact |
| 3 | Public arc pre-draft (5 channels) | essay, thread, site, Space, walkthrough |
| 4 | Premiere atomic launch | 5 URLs in 1 commit, `portfolio/premiere-ledger.md` |

## Next — MP-92 / ADR-0029

Continuum law executes: ADR-0029 opens with exactly one new research question from frozen candidate set:

- **C1**: Solution-regime phase diagram (dense vs sparse vs memorized)
- **C2**: Scaled R1 induction (standard scale, 10k epochs, fresh batches)
- **C3**: SAE on confirmed-head checkpoint (Rung 1 standard-scale output)
- **C4**: ACDC on real circuit (capstone with validated heads)

Unchosen three close with dated reasons in same sitting. Next phase gate: `verify-claims=0`, tests green, ADR-0029 row 1 stamped.

## Links

- PR #145: https://github.com/AlessioBrillo/from-gradient-to-transformer/pull/145
- MP-91 roadmap: `00_meta/91_micro-phase-91-from-release-to-premiere.md`
- MP-92 execution roadmap: `00_meta/92_micro-phase-92-execution-roadmap.md`
- ADR-0028: `docs/adr/0028-continuum-ledger-23.md`
- Paper v20: `portfolio/paper/main.tex`
- Portfolio RESULTS: `portfolio/RESULTS.md`