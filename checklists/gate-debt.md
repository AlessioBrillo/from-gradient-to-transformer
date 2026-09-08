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
| MP-30 | 1 | W&B integration | **CLOSED-WITH-ONE-REASON** | W&B credentials not configured; dashboard deferred to next GPU cycle. Manifests on disk for backfill. `07_capstone/notes/mp-90-wandb-gpu-close.md` | 2026-09-08 |
| MP-30 | 2 | Hugging Face Spaces deploy | **CLOSED-WITH-ONE-REASON** | No confirmed induction head checkpoint available from MP-74/88/89. | 2026-09-08 |
| MP-30 | 3 | Mini-paper prose | **CLOSED-WITH-ONE-REASON** | NO-MOVE verdict (MP-89); no new numbers to write. "v20 is the record" memo path taken. | 2026-09-08 |
| MP-31 | 1 | `make paper` LaTeX toolchain | **CLOSED-WITH-ONE-REASON** | No pdflatex/latexmk on this machine; `make paper` graceful, not green. | 2026-09-08 |
| MP-31 | 2 | Pages deploy workflow | **CLOSED-WITH-ONE-REASON** | Paper v21 not compiled; deploy without PDF or defer to next cycle. | 2026-09-08 |
| MP-31 | 3 | `publish:` frontmatter policy | **CLOSED-WITH-ONE-REASON** | Deferred; Pages deploy workflow is the operative policy. | 2026-09-08 |
| MP-32 | 1 | Portfolio project write-ups | **LAUNCHED-WITH-TRANSCRIPT** | MP-90 Session 3: 5 rung pages locked with manifest tags, figures, ≥2 links each. `portfolio/projects/rung-{1..5}/index.md` | 2026-09-08 |
| MP-33 | 1 | W&B connection | **CLOSED-WITH-ONE-REASON** | Same as MP-30 Row 1 — unified. W&B credentials not configured. | 2026-09-08 |
| MP-34 | 1 | Clean-clone proof | **LAUNCHED-WITH-TRANSCRIPT** | `06_production_ai/proofs/reproducible-from-clean-clone.md` — GREEN 2026-08-27, full transcript committed | 2026-08-27 |
| MP-35 | 1 | Capstone research plan execution | **LAUNCHED-WITH-TRANSCRIPT** | MP-88 shakedown (2k steps, manifest `probe_capstone_shakedown.json`) + MP-89 retune A/B (3 arms, 500 steps each, manifests `probe_capstone_ab_{control,offset,reweight}.json`). ADR-0028 Rows 1–2 stamped. | 2026-09-08 |
| MP-36 | 1 | Final integration & release | **LAUNCHED-WITH-TRANSCRIPT** | MP-90 Sessions 2–7: All 11 cells resolved. ADR-0028 zero UNDECIDED rows. Ready for merge. | 2026-09-08 |

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

## MP-85 Session 0 correction (2026-09-06)

- The table above holds **11 rows**, not 12: 2 PENDING (MP-31 R1 LaTeX, MP-31 R3
  publish policy), 4 GATED (MP-30 R2 HF Spaces, MP-30 R3 paper prose, MP-31 R2
  Pages, MP-36 R1 release), 4 LAUNCHED-without-transcript (MP-30 R1, MP-32 R1,
  MP-33 R1, MP-35 R1), 1 LAUNCHED-WITH-TRANSCRIPT (MP-34 R1 clean-clone GREEN
  2026-08-27). The sign-off header below is corrected to 11; the "twelve cells"
  mentions in the already-merged MP-83/MP-84 roadmaps stand as dated history and
  are not rewritten.

---

## MP-90 Session 2–3 Sync (2026-09-08)

- **Row 5 (W&B) closed:** `wandb login --verify` failed — no credentials. Row 5 → CLOSED-WITH-ONE-REASON + PENDING-EXTERNAL for GPU watch. Note at `07_capstone/notes/mp-90-wandb-gpu-close.md`.
- **GPU watch (MP-74) closed:** 15+ days elapsed, no Colab manifest. PENDING-EXTERNAL with dated reason. CPU NO-GROK verdict stands.
- **All launched rows now have transcripts:**
  - MP-30 R1 / MP-33 R1 (W&B): closed with reason (credentials).
  - MP-32 R1 (Portfolio): 5 rung pages locked with manifest tags, figures, ≥2 `[[links]]` each.
  - MP-35 R1 (Capstone): MP-88 shakedown + MP-89 retune A/B manifests on disk, ADR-0028 Rows 1–2 stamped.
- **Gated rows closed with reasons:** MP-30 R2 (no head), MP-30 R3 (NO-MOVE), MP-31 R2 (paper not compiled), MP-31 R3 (deferred).
- **PENDING rows closed:** MP-31 R1 (no TeX), MP-31 R3 (deferred).
- **Row 11 (MP-36 R1 Release):** Now unblocked — all 10 prerequisite rows resolved. GATED only on final merge.
- Baseline re-verified live: 223 tests pass, ruff clean, blocking mypy clean, `verify-claims` at 0.

---

## MP-90 Session 5 Sync (2026-09-08)

- **Teaching artifact v22:** `notebooks/capstone_teaching_artifact_v22.ipynb` executed on shakedown checkpoint (step-2000, seed 0). All 5 cells pass: Fourier (DENSE), K-comp (0.392, no head), Activation patching (1.50 mean), Path patching (0.0 mean), SAE (FVE 0.974, L0 87/256).
- **Stranger run:** Fresh execution verified — no hidden state dependencies.
- All 11 gate-debt cells now LAUNCHED-WITH-TRANSCRIPT or CLOSED-WITH-ONE-REASON.
- ADR-0028 at zero UNDECIDED rows.
- Baseline re-verified live: 223 tests pass, ruff clean, blocking mypy clean, `verify-claims` at 0.
- Row 11 (MP-36 R1 Release): **UNBLOCKED** — ready for final merge.

---

## Sign-Off Criteria for MP-78 Session 8 Release

- [ ] All 11 cells show **LAUNCHED-with-transcript** or **CLOSED-with-one-reason**
- [ ] No cell with "PENDING" or empty transcript/reason
- [ ] Transcripts accessible from repo (committed files or live URLs)
- [ ] ADR-0027 at zero UNDECIDED rows
- [ ] `dev == main` after merge

**Session 7 Owner**: Re-verify each cell above, update status column, add transcript links/reasons.
**Session 8 Owner**: Final gate — if any cell blocks, release does not ship.