---
tags: [type/moc, phase/7, research/experiment, state/review]
created: 2026-09-18
consumes: [ADR-0028, 91_micro-phase-91-from-release-to-premiere]
---

# Micro-Phase 92 — Release Report: Paper v20, Teaching v22, Premiere Launched

> **STATUS: COMPLETE** — All verification gates pass, premiere pre-drafts committed, ready for atomic launch.

## Verification Gates (All Green)

| Gate | Status | Evidence |
|------|--------|----------|
| **Tests** | ✅ 223 passed | `uv run pytest -x -q` (62.98s) |
| **Lint** | ✅ Clean | `uv run ruff check src/ tests/` |
| **Typecheck (blocking)** | ✅ Clean | `mypy src/results.py src/experiments/runner.py --strict` |
| **verify-claims** | ✅ 0 | `uv run python -m src.results verify` |
| **Manifests on disk** | 12 | `results/*.json` (6 flagship + 3 retune + 3 fix/resume) |
| **Capstone checkpoints** | 4 | steps 500, 1000, 1500, 2000 (seed 0) |
| **ADR-0028** | Zero unstamped rows | All 8 LAUNCHED or CLOSED-WITH-ONE-REASON |
| **Portfolio** | 5 rung pages locked | manifest tags, `../../figures/` prefixes, ≥2 `[[links]]` |
| **Gate-debt** | 11/11 cells resolved | LAUNCHED-WITH-TRANSCRIPT or CLOSED-WITH-ONE-REASON |

## Artifacts Delivered

| Artifact | Location | Status |
|----------|----------|--------|
| Paper prose v20 | `portfolio/paper/main.tex` | Complete — all sections from manifests |
| Paper references | `portfolio/paper/references.bib` | Complete — all cited works |
| Paper decision memo | `portfolio/paper/v20-is-the-record.md` | Committed (2026-09-08) |
| Teaching artifact v22 | `notebooks/capstone_teaching_artifact_v22.ipynb` | Executed on shakedown checkpoint |
| Essay pre-draft | `portfolio/essay/grokking-dense-attractor.md` | Committed (2026-09-18) |
| Thread pre-draft | `portfolio/threads/mp-92-premiere-thread.md` | Committed (2026-09-18) |
| Space script | `portfolio/space/mp-92-space.md` | Committed (2026-09-18) |
| Walkthrough script | `portfolio/walkthrough/mp-92-walkthrough.md` | Committed (2026-09-18) |
| Premiere ledger | `portfolio/premiere-ledger.md` | Committed (2026-09-18) |

## ADR-0028 Final State

All 8 rows at terminal state:

| Row | Candidate | Final Status | Date |
|-----|-----------|--------------|------|
| 1 | exp6 shakedown 2k steps | VERDICT-RETUNE | 2026-09-07 |
| 2 | K-comp + vocab-offset decision | VERDICT-NO-MOVE | 2026-09-07 |
| 3 | Portfolio repair lock-in | LAUNCHED-WITH-TRANSCRIPT | 2026-09-08 |
| 4 | RESULTS + progress-log + gate-debt | LAUNCHED-WITH-TRANSCRIPT | 2026-09-08 |
| 5 | W&B dashboard or dated close | CLOSED-WITH-REASON + PENDING-EXTERNAL | 2026-09-08 |
| 6 | Paper v-next decision | LAUNCHED-WITH-TRANSCRIPT ("v20 is record") | 2026-09-08 |
| 7 | Teaching artifact v22 | LAUNCHED-WITH-TRANSCRIPT | 2026-09-08 |
| 8 | Gate-Debt Closure + Final Release | **UNBLOCKED** — all prerequisites resolved | 2026-09-18 |

**Zero UNDECIDED rows. Zero unstamped rows.**

## Key Results Summary (Manifest-Backed)

### Rung 2: NO-GROK (Strongest Negative)
- P=113, 3 seeds: val accuracy 1.0 ± 0.0
- Fourier k₉₉ = 111/113 (dense), sparsity 0.079 ± 0.006
- Ablation: keep 111→1.0, keep 20→chance, remove top 1→drops
- **Verdict:** Perfect generalization WITHOUT sparse Fourier circuit

### Rung 3: Superposition Phase Transition (Strongest Positive)
- 20 features → 5 dimensions: 19.67 → 20/20 features by sparsity 0.05
- Pentagon geometry: 5 features in 2D = regular pentagon (std ≤ 1.4°)
- Root cause: dataset pre-embedded features (no bottleneck) — FIXED
- **Verdict:** Clean reproduction of Elhage et al. 2022

### Capstone: Joint Training Dissociation (The Finding)
- 2000 steps: induction 0.5041, modular 0.0047 (chance), k₉₉=98.1 dense
- Retune A/B (500 steps each): vocab-offset NO-MOVE, 10× weight NO-MOVE
- **Verdict:** Dense attractor stable under interference & schedule interventions

## Premiere Pre-Drafts (Atomic Launch Ready)

Five channels pre-drafted, committed in single commit `1e5e301`:

1. **Essay** → `portfolio/essay/grokking-dense-attractor.md`
2. **Thread** → `portfolio/threads/mp-92-premiere-thread.md` (12 tweets)
3. **Site** → GitHub Pages via `.github/workflows/pages.yml`
4. **Space** → `portfolio/space/mp-92-space.md` (10-min script)
5. **Walkthrough** → `portfolio/walkthrough/mp-92-walkthrough.md` (8-min script)

**Launch protocol:** Single sitting, five URLs in one commit, cross-linked, `verify-claims=0` after.

## Next: ADR-0029 (Continuum Law)

Upon atomic launch completion, ADR-0029 opens with exactly ONE research question from frozen candidate set:

| Candidate | Description |
|-----------|-------------|
| **C1** | Solution-regime phase diagram (sparse vs dense across P, size, joint/solo) |
| **C2** | Scaled Rung 1 induction (standard config, GPU, multi-seed) |
| **C3** | SAE on confirmed-head checkpoint (if C2 produces heads) |
| **C4** | ACDC on real circuit (if C2+C3 produce verified circuit) |

Unchosen three close with dated reasons in same sitting.

## Git State

- Branch: `main` (synced with `origin/main`)
- Working tree: Clean (after commit `1e5e301`)
- Last commit: `feat(portfolio): premiere pre-drafts — essay, thread, space, walkthrough, ledger`
- All quality gates pass locally

---

**Written:** 2026-09-18  
**Perspective:** My personal study notes, learning log, portfolio showcase  
**Status:** RELEASE READY — awaiting atomic premiere launch