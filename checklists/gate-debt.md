---
tags: [checklist, gate-debt, phase/6, phase/7]
created: 2026-08-24
updated: 2026-09-05
---

# Gate-Debt Ledger — MP-30 through MP-36 Row Closures

**Protocol**: Re-verify all MP-30–MP-36 row closures with transcripts. Each cell: LAUNCHED-with-transcript or CLOSED-with-one-reason. A claimed closure without its transcript stays open and blocks Session 8. This file's absence, if still absent, recorded with a date.

**Session 1 (Initial) — 2026-08-24**: Initial audit. **Session 7**: Re-verification. **MP-78 Session 0**: Status sync from ADR-0027 adjudication.

---

## MP-30 through MP-36 Row Status (Current as of MP-78 Session 0)

| Phase | Row | Description | Status | Transcript / Reason | Date |
|-------|-----|-------------|--------|---------------------|------|
| MP-30 | 1 | W&B integration | **LAUNCHED** | MP-78 Row 3: W&B logging added to runner.py, capstone runs connected, MP-74 backfill in progress | 2026-09-01 |
| MP-30 | 2 | Hugging Face Spaces deploy | **GATED** | MP-78 Row 4: Opens only if MP-74 R5 produces confirmed head | 2026-09-01 |
| MP-30 | 3 | Mini-paper prose | **GATED** | MP-78 Row 2: Opens only if MP-74 produces new numbers | 2026-09-01 |
| MP-31 | 1 | `make paper` LaTeX toolchain | **PENDING** | No TeX on this machine — `make paper` graceful, not green | 2026-08-23 |
| MP-31 | 2 | Pages deploy workflow | **GATED** | MP-78 Row 6: Opens only if paper v21 compiles | 2026-09-01 |
| MP-31 | 3 | `publish:` frontmatter policy | **PENDING** | Not yet defined | 2026-08-23 |
| MP-32 | 1 | Portfolio project write-ups | **LAUNCHED** | MP-78 Row 5: Figures exist for all 5 rungs; write-ups Sessions 3-4 | 2026-09-01 |
| MP-33 | 1 | W&B connection | **LAUNCHED** | Same as MP-30 Row 1 — unified | 2026-09-01 |
| MP-34 | 1 | Clean-clone proof | **LAUNCHED-WITH-TRANSCRIPT** | `06_production_ai/proofs/reproducible-from-clean-clone.md` — GREEN 2026-08-27, full transcript committed | 2026-08-27 |
| MP-35 | 1 | Capstone research plan execution | **LAUNCHED** | MP-78 Row 1: Clean-clone proof GREEN unblocks; config ready, training Session 1 | 2026-09-01 |
| MP-36 | 1 | Final integration & release | **GATED** | MP-78 Row 8: Gated on Rows 1–6 complete | 2026-09-01 |

---

## Session 1 Audit Notes (2026-08-24)

All MP-30–MP-36 rows remain **PENDING** — they are the documented residue from the MP-30 through MP-36 cap that was never executed, not new work. Each row is owned by its respective phase and will be resolved when that phase executes. This ledger exists to ensure they are not forgotten and that the Phase 6 gate (clean-clone proof) is the only blocker this phase (MP-74) must directly address.

**Clean-clone proof (MP-34 Row 1)** is the only row MP-74 must execute directly (ADR-0024 Row 4). All other rows are tracked here for completeness and will be addressed in their respective phases.

---

## Session 7 Re-verification Notes (MP-78 Session 7)

To be completed at MP-78 Session 7. Each row must show:
- LAUNCHED-with-transcript (link to execution artifact/transcript)
- CLOSED-with-one-reason (single dated sentence explaining why not launched)

Any cell without transcript/reason blocks Session 8 release.

---

## MP-78 Session 0 Status Sync (2026-09-01)

Updated from ADR-0027 adjudication at MP-78 Session 0:

**Resolved since MP-74**:
- MP-34 Row 1 (Clean-clone proof): **GREEN 2026-08-27** — transcript at `06_production_ai/proofs/reproducible-from-clean-clone.md`
- MP-35 Row 1 (Capstone execution): **UNBLOCKED** — clean-clone proof GREEN removes Phase 6 gate

**Launched in MP-78**:
- MP-30 Row 1 / MP-33 Row 1 (W&B): Row 3 of ADR-0027
- MP-32 Row 1 (Portfolio): Row 5 of ADR-0027

**Gated in MP-78** (depend on MP-74 verdicts):
- MP-30 Row 2 (HF Spaces): ADR-0027 Row 4 — needs confirmed head
- MP-30 Row 3 (Paper prose): ADR-0027 Row 2 — needs new numbers
- MP-31 Row 2 (Pages): ADR-0027 Row 6 — needs paper compile

**Still Pending** (Phase 6/7 residue):
- MP-31 Row 1 (LaTeX): No TeX toolchain — re-verified 2026-09-05 (no pdflatex/latexmk on this machine; `make paper` graceful, not green)
- MP-31 Row 3 (Publish policy): Not yet defined (unchanged 2026-09-05)
- MP-36 Row 1 (Final release): Gated on Rows 1-6

## MP-80 Sync (2026-09-05)

- Portfolio click-through blockers repaired: 5 rung pages now carry >=2 `[[links]]`, correct `../../figures/` prefix, and real filenames (dangling refs struck with reasons).
- `portfolio/RESULTS.md` Rung-2 summary (NO-GROK 2026-08-11) and Phase-6 gate cell (GREEN 2026-08-27) truthed against the body and this ledger.
- Exp6 probe guardrail (`--manifest-path`) and real K-comp port landed test-first; shakedown may proceed without flagship-clobber risk.
- Toolchains pinned: pdflatex/latexmk absent, wandb 0.28.0 present, hf 1.28.0 present, `pages.yml` exists.

---

## Sign-Off Criteria for MP-78 Session 8 Release

- [ ] All 12 cells show **LAUNCHED-with-transcript** or **CLOSED-with-one-reason**
- [ ] No cell with "PENDING" or empty transcript/reason
- [ ] Transcripts accessible from repo (committed files or live URLs)
- [ ] ADR-0027 at zero UNDECIDED rows
- [ ] `dev == main` after merge

**Session 7 Owner**: Re-verify each cell above, update status column, add transcript links/reasons.
**Session 8 Owner**: Final gate — if any cell blocks, release does not ship.