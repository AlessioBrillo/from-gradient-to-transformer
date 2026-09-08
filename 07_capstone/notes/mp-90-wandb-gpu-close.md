---
tags: [phase/7, research/experiment, type/note]
created: 2026-09-08
consumes: [ADR-0028, 89_micro-phase-89-from-retune-to-signal]
---

# MP-90 Session 2 — W&B Verdict + GPU-Watch Hard Close

## W&B Login Attempt

**Command:** `uv run wandb login --verify`

**Result:** FAIL — No API key configured.
- No `~/.netrc` with wandb entry
- No `WANDB_API_KEY` environment variable
- `wandb` CLI installed (0.28.0 via uv) but not authenticated

**Decision:** Row 5 → **CLOSED-WITH-ONE-REASON**
> "W&B credentials not configured; dashboard deferred to next GPU cycle. All committed manifests (exp1–exp5, exp6 probes) remain on disk and can be backfilled when credentials are available."

## GPU Watch Consumption (MP-74 Colab)

**MP-74 Launch Date:** 2026-08-24 (Colab GPU Grokking 3-seed P=113)
**Days Elapsed:** 15+ days (as of 2026-09-08)
**Expected Manifest:** `results/exp2_grokking_gpu_manifest.json` or equivalent

**Check:** No GPU manifest found in `results/` directory. Only CPU manifests present:
- `exp2_grokking.json` (CPU 3-seed P=113, 2026-08-13)
- `probe_capstone_shakedown.json` (joint shakedown, 2026-09-07)
- Three A/B probe manifests (2026-09-07)

**Decision:** Row 5 note updated with **PENDING-EXTERNAL**
> "MP-74 Colab manifest not landed after 15+ days; closed as external dependency. Next GPU cycle owns this question. The CPU NO-GROK verdict (2026-08-11, 3 seeds, val 1.0 + dense Fourier k_99=111/113) stands as the recorded measurement."

## Row 5 Status: STAMPED

ADR-0028 Row 5 (W&B live dashboard or dated close) — **CLOSED-WITH-ONE-REASON + PENDING-EXTERNAL** as of 2026-09-08.

## Next: Session 3 — Portfolio Repair + Ledger Truthing

Row 3 (portfolio repair) and Row 4 (RESULTS + progress-log + gate-debt truthing) now unblocked.

---

**Written:** 2026-09-08
**Perspective:** Personal study notes, learning log, portfolio showcase
**Status:** Session 2 complete — Row 5 stamped