# MP-92 Premiere Ledger — Atomic Launch Record

**Launch date:** 2026-09-18  
**Commit:** [to be filled at launch]  
**Status:** PRE-DRAFT — URLs to be filled at atomic launch

---

## Five Channels (Same-Sitting Launch)

| Channel | Pre-Draft Location | Live URL | Timestamp |
|---------|-------------------|----------|-----------|
| **Essay** | `portfolio/essay/grokking-dense-attractor.md` | `URL_TBD` | `TBD` |
| **Thread** | `portfolio/threads/mp-92-premiere-thread.md` | `URL_TBD` | `TBD` |
| **Site** | `.github/workflows/pages.yml` → GitHub Pages | `URL_TBD` | `TBD` |
| **Space** | `portfolio/space/mp-92-space.md` | `URL_TBD` | `TBD` |
| **Walkthrough** | `portfolio/walkthrough/mp-92-walkthrough.md` | `URL_TBD` | `TBD` |

---

## Launch Protocol

1. **Single sitting** — all five channels published within 15 minutes
2. **URL receipts** — each URL captured immediately after publish
3. **Single commit** — all five URLs committed in one commit:
   ```
   feat(portfolio): premiere launch — five channels live
   ```
4. **Cross-links** — essay ↔ thread ↔ site ↔ Space/walkthrough
5. **Ledger update** — this file updated with URLs + timestamps
6. **verify-claims=0** — verified after commit

---

## Manifest-Backed Numbers in Premiere

Every quantitative claim in the premiere cites a manifest:

| Claim | Manifest |
|-------|----------|
| Rung 2: val 1.0, k₉₉=111/113 | `results/exp2_grokking.json` |
| Rung 3: 19.67→20/20 features, pentagon | `results/exp3_superposition.json` |
| Rung 1: 52.2% vs 0.05% fixed-vs-fresh | `results/exp1_induction_heads.json` |
| Rung 4: ~0.20 recovery, 0 heads | `results/exp4_circuit_patching.json` |
| Rung 5: 99.97% FVE, 53% L0 (real) | `results/exp5_sae_dashboard.json` |
| Capstone: ind 0.504, mod 0.0047 | `results/probe_capstone_shakedown.json` |
| Retune A/B: NO-MOVE (all < chance) | `results/probe_capstone_ab_*.json` |

---

## Verification

```bash
# Pre-launch
uv run pytest -x -q          # 223 passed
uv run ruff check src/ tests/  # clean
uv run mypy src/results.py src/experiments/runner.py --strict  # clean
uv run python -m src.results verify  # all manifests check out

# Post-launch
curl -I <site-url>           # HTTP 200
git log --oneline -1         # premiere commit present
```

---

## Cross-References

- Paper v20: `portfolio/paper/main.tex`
- Teaching artifact v22: `notebooks/capstone_teaching_artifact_v22.ipynb`
- Results ledger: `portfolio/RESULTS.md`
- Continuum ledger: `docs/adr/0028-continuum-ledger-23.md`
- Release report: `00_meta/92_micro-phase-92-release-report.md` (to be written)

---

**Written:** 2026-09-18  
**Status:** Pre-draft complete — awaiting atomic launch