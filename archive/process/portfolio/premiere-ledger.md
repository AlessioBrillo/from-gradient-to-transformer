# MP-92 Premiere Ledger — Atomic Launch Record

**Launch date:** 2026-09-18 (site and paper) — updated 2026-10-20 with the
receipts that were actually observed
**Commit:** the live site is built from `main` by `.github/workflows/pages.yml`
**Status:** **PARTIALLY LAUNCHED** — three of the five channels are live, two
were never published. The pre-draft below is kept, with the outcome recorded
next to it, because the difference between "planned" and "shipped" is exactly
the kind of thing this repository's ledger exists to keep visible.

---

## Five Channels (Same-Sitting Launch)

| Channel | Pre-Draft Location | Live URL | Status |
|---------|-------------------|----------|--------|
| **Essay** | `portfolio/essay/grokking-dense-attractor.md` | <https://alessiobrillo.github.io/from-gradient-to-transformer/portfolio/essay/grokking-dense-attractor.html> | **LIVE** (verified 2026-10-20, HTTP 200) |
| **Thread** | `portfolio/threads/mp-92-premiere-thread.md` | — | **NOT PUBLISHED**: a launch draft, kept in the repository and deliberately excluded from the site build (`scripts/build_site.py` publishes README, RESULTS, the model card, the project pages and the essay — not the threads) |
| **Site** | `.github/workflows/pages.yml` → GitHub Pages | <https://alessiobrillo.github.io/from-gradient-to-transformer/> | **LIVE** (verified 2026-10-20, HTTP 200) |
| **Space** | `portfolio/space/mp-92-space.md` | — | **NOT PUBLISHED**: the HF Spaces demo was descoped on 2026-10-11 (no browsable artifact exists to host) |
| **Walkthrough** | `portfolio/walkthrough/mp-92-walkthrough.md` | — | **NOT PUBLISHED**: a launch draft, excluded from the site build like the thread |

**Also live** (not one of the five channels, but part of the same public
surface): the mini-paper PDF,
<https://alessiobrillo.github.io/from-gradient-to-transformer/paper.pdf>, and
the per-rung project pages under `portfolio/projects/`.

---

## Launch Protocol

1. **Single sitting** — all five channels published within 15 minutes
2. **URL receipts** — each URL captured immediately after publish
3. **Single commit** — all five URLs committed in one commit:
   ```
   feat(portfolio): premiere launch — five channels live
   ```
4. **Cross-links** — essay ↔ thread ↔ site ↔ Space/walkthrough
5. **Release** — tag, then the announcement

## What actually happened (2026-10-20 audit)

The five-channel launch **did not happen as one sitting**, and the record says
so rather than pretending otherwise:

- steps 1–3 were never executed: there is no "premiere launch" commit, because
  the three unpublished channels were never published;
- the site, the essay and the paper PDF are live and are rebuilt from `main` by
  the Pages workflow;
- the thread and the walkthrough remain drafts in the repository, and the Space
  was descoped with the dashboard (2026-10-11) — the three of them are
  excluded from the site build on purpose, not by accident;
- **the published essay is current**: it was rewritten on 2026-10-16 against
  the post-audit manifests (val accuracy 0.9999 ± 0.0002, k_energy_90 = 5.7 of
  56, 3/3 seeds) and it even names the content-based induction task as the
  next step. The two *unpublished* drafts (the thread and the walkthrough) are
  the ones that still carry the 2026-09-18 numbers — the pre-fix "0 heads" and
  the pre-audit "dense" readings. They are not on the site, so they mislead
  nobody, and they are rewritten or deleted as part of the closure pass rather
  than left to rot in the repository.

## Links

- [[portfolio/RESULTS]] — the authority on what is true; the essay is written
  against it, the two unpublished drafts are not.
- [[07_capstone/execution-log]] — the runs that rewrote the essay.
