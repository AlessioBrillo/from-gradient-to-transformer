---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-13
---

# Micro-Phase 32 — The Continuation: the continuum law executes for the first time

Written as a personal learning log and a public record, like every roadmap before it.

MP-31 premiares the record — the paper, the site, the Space, the thread and the
walkthrough get addresses a stranger can open, and the horizon lanes MP-30
decided execute or close as dated rows. This phase is the first past the
premiere: the continuum. ADR-0006's eight rows were pre-registered when MP-26
was written (2026-08-10) and never filled; MP-32 is the phase that fills them,
under the law that ledger was built on — the continuum law: exactly one new
research question opens per phase, chosen at Session 0 from the frozen
candidate set C1–C4, and the unchosen candidates close with one dated reason
each, in the same sitting. A phase that opens two questions is drift by
another name.

The executed horizon verdicts become artifacts, never re-opened: the ACDC
pilot's verdict (ADR-0005 row 7) becomes the Rung-6 section or the trial
table; the scaled-up R1's verdict (ADR-0005 row 8) becomes the result
paragraph or the no-head negative. The essay is amended, never rewritten
(annex v2); the paper gets its v2 diff; the shelf is maintained as a dated row
with heartbeats; the stranger round 2 runs with its kill-date and its
pre-built substitute; the standing gate debt — W&B, clean-clone proof,
graduation proof, `reproduce-multiseed` — closes with dates, each cell
LAUNCHED-with-transcript or CLOSED-with-one-reason.

The record's deepest law applies here too: a promise can be re-planned
forever, but a dated row is answered. This roadmap is pre-registered while
MP-31 still stands unexecuted — three phases stacked without execution is the
exact drift the record has named since MP-18 — so this phase's Session 0 is
the mechanical refusal of it: no MP-31 release report (ADR-0005 at zero
UNDECIDED rows, the site live, `verify-claims` at 0), no phase. The gate is a
checklist with receipts, not a paragraph.

## Where this phase starts (state review, verified against the repo 2026-08-13)

The intake is MP-31's release report; below is what the record stands at the
moment of pre-registration, so this roadmap's claims are auditable from day
one. MP-31's Session 8 updates every line; nothing here re-plans a single row
of it.

- **Tree state**: `dev` clean at the MP-31 pre-registration merge (PR #63
  squashed, dev reconciled with main); nothing of MP-29, MP-30 or MP-31 has
  executed yet — three phases stand pre-registered, and their residue rows
  (the positive control's verdict, the paper PDF, the premiere ledger's
  stamps) are this phase's intake, per the record's law that a session is not
  over while a row it owns is undated.
- **The ledgers**: ADR-0003 row 1 stamped (LAUNCHED 2026-08-11, NO-GROK, val
  1.0, Fourier dense, k_99 = 111/113, gen epochs 1250/1048/1326); row 2 in
  flight (microscope trial 1); rows 3–7 UNDECIDED (MP-29's rows). ADR-0004's
  five horizon rows UNDECIDED (MP-30 decides them in its Session 4).
  **ADR-0005's eight premiere rows UNDECIDED — MP-31's rows**. **ADR-0006's
  eight continuum rows UNDECIDED — this phase's rows**, filled exactly once,
  under the continuum law.
- **The manifests**: `results/exp2_grokking.json` exists but carries
  `git_dirty: true` (`git_sha d48f9ad`, produced mid-phase) — and the P=113
  final checkpoints ARE on disk (`checkpoints/exp2_checkpoint_seed{0,1,2}.pt`,
  verified 2026-08-13), so the clean-tree re-derivation is a minutes-scale
  producer run (`scripts/exp2_manifest_from_checkpoints.py`), not the ~2 h
  re-run MP-29's S0 text assumed; the decision belongs to MP-29's Session 0,
  recorded here as intake, not re-planning. `results/exp1_induction_heads.json`
  is the old sub-standard run (epochs=150, d_model=24, final acc ≈ 0.004) —
  the standard-scale manifest does NOT exist. `results/exp5_sae_dashboard.json`
  does not exist.
- **The disk truth on the interrupted lanes (verified 2026-08-13)**: the R1
  standard-scale ×3 seeds were interrupted at ~epoch 240 (~1 h 41 m in) and
  **no exp1 checkpoints exist on disk** — the R1 verdict is currently
  underivable from disk and needs a ~17–22 h restart or a dated closure
  (MP-29's row-3 intake). Microscope trial 1 was interrupted at ~3753/5000
  with its rolling checkpoint present
  (`checkpoints/micro_trial1/exp2_checkpoint_seed0.pt`) — its verdict is
  computable now via the kill-drill-verified resume machinery (MP-29's row-2
  intake).
- **The CI floor**: `make verify-claims` at its current 3 problems (dirty-tree
  exp2 manifest; Rung 2 section tag missing; Rung 5 section tag missing) —
  MP-29's one measured line drives it to 0, and 0 is this phase's
  precondition, not its hope. The tracked 185+ tests, ruff, blocking mypy and
  markdownlint baselines were all green at MP-28's release and nothing has
  changed under them since.
- **The toolchains, verified today**: no LaTeX toolchain on this machine
  (`pdflatex`/`latexmk`/`tectonic` all absent — `make paper` is graceful, not
  green); no Pages deploy workflow in `.github/workflows/` (only
  conventional-commits, markdown-lint, python-ci); no `publish:` frontmatter
  policy anywhere in the vault; `portfolio/projects/` empty; the Space engine
  is `src/experiments/exp3_superposition.py` behind verified manifests
  (`results/exp3_*.json` clean). All four are MP-31's Session-0 items,
  recorded here as MP-31's residue, never this phase's re-planning.
- **The showcase corpus**: 12 provenance-guarded figures in
  `portfolio/figures/`; the paper scaffold (`main.tex` + `references.bib`)
  that MP-30 finishes; `portfolio/RESULTS.md`, `README.md` and `model-card.md`
  that MP-30 brings to v-final; `gh` CLI available against
  `github.com/AlessioBrillo/from-gradient-to-transformer`.
- **The scientific ledger across all runs to date**: no run in this
  repository's history has ever produced a sparse Fourier solution (P=59
  dense 59/59; P=113 k_99 = 111/113, val 1.0 — the NO-GROK positive-negative).
  This pre-conditions the C1–C4 adjudication in Session 0: C1's opens-only-if
  is already false, C2 and C4 wait on heads that may never exist, and C3 is
  the only always-CPU-runnable candidate.

## Design decisions

- **The continuum law, first execution.** Exactly one new research row (row 3)
  opens per phase, chosen at Session 0 from the pre-registered candidate set
  C1–C4 below; the unchosen candidates close with one dated reason each, in
  the same sitting. The session gate is the same as ADR-0001/0003/0004/0005: a
  session is not over while a row it is responsible for is undated; Session 8
  requires zero UNDECIDED rows. Verdict criteria are written into the row's
  cells **before** the window opens and are never edited afterwards; the only
  allowed post-launch edit is "observed".
- **Consumption is execution, not memory.** A verdict consumed into an artifact
  in the same sitting that decides it is a result; consumed into a paragraph
  written later it is a memory. The ACDC pilot's verdict (ADR-0005 row 7) →
  Rung-6 artifact (ADR-0006 row 1) and the scaled-up R1's verdict (ADR-0005
  row 8) → scaled-R1 artifact (ADR-0006 row 2) are consumed in the sitting
  that owns them, as MP-30 decided the lanes and MP-31 executed or closed
  them. Both land as dated rows in one sitting, never re-opened.
- **The shelf is a row, not a mood.** Row 6 (shelf maintenance: site + Space
  health, claims gate on every merge) carries a heartbeat, a hostile-webmaster
  walk at zero, and a dated close-or-launch — baseline in S1, rehearsal in S7,
  release in S8. The essay annex v2 (row 4) and paper v2 diff (row 5) are
  first-class artifacts: amended via dated annexes, never rewritten.
- **The stranger's pipeline extends to round 2.** Row 7 (stranger round 2:
  feedback from thread, site, Space) carries the ADR-0004 human-dependency
  rule and the ledger's window — intake at S4, kill-date at S5: if the
  feedback intake does not happen within the window, the row closes with one
  reason and the recorded self-review substitute, written in S2 before the
  window opens. Never a silent skip.
- **The gate-debt row is stamped in one sitting.** Row 8 (standing gate debt:
  W&B, clean-clone proof, graduation proof, `reproduce-multiseed` exp2/exp5)
  ends LAUNCHED (with its transcript/artifact) or CLOSED (with one named
  reason) — all cells decided in S1, the sitting that owns the row.
- **The S0 gate is the mechanical refusal of drift.** Session 0 opens only on
  MP-31's release report (ADR-0005 at zero UNDECIDED rows + the first live URL
  stamped + `verify-claims` at 0). The MP-26 precedent — the first
  continuation pre-registration, gated on MP-25's release, never executed —
  is named and refused: the gate is a checklist with receipts, not a
  paragraph.
- **The terminus is stamped at Step 0**: release = this roadmap's merge + 14
  calendar days. On that date the phase ships everything the rows decided —
  the residue is a dated list, never a silence (inherited, still true).
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED rows
  at Session 8; release = merge + 14 calendar days.

## Session 0 — the gate truthing + the continuum choice (2026-08-13, ~1 h) — next

- **Gate**: MP-31's release report consumed row by row — ADR-0005 at zero
  UNDECIDED rows, the first live URL stamped in the same sitting as MP-31's
  merge, `verify-claims` at its actual count (0 if MP-31 landed its line;
  otherwise the residue is listed with the row that owns it — intake, not
  re-planning). The intake table is committed before a single continuum row
  opens.
- **The continuum choice (the C1–C4 adjudication, decided in this sitting):**
  - **C1 — the P-sweep grokking scaling** (P ∈ {59, 113, 227} at fixed
    budget, one change): opens only if grokking grokked (ADR-0003 row 1
    LAUNCHED). Row 1 stamped NO-GROK — dense at P=113, val 1.0 — so C1's
    condition is already false; S0 records the closure with one dated reason:
    the small-P story is already written as the negative (the dense-solution
    characterization MP-29 produces is its artifact).
  - **C2 — induction scaling at fixed compute** (heads × layers swept at
    standard scale): opens only if a real head exists (ADR-0003 row 3
    LAUNCHED). Row 3's verdict depends on the R1 standard-scale run, whose
    checkpoints are absent from disk (restart or dated closure — MP-29's
    intake). S0 records the conditional: C2 opens if MP-29's row-3 verdict
    meets the head criterion, else closes with the no-head negative.
  - **C3 — heterogeneous-feature superposition** (Elhage et al. ch. 2–3:
    importance/frequency): always runnable on CPU. The only candidate whose
    gate today's record does not already close — the likely survivor of this
    sitting, pending the C2 adjudication.
  - **C4 — SAE monosemanticity on toy features** (Bricken-style dictionary on
    the superposition model): opens only if R5's delta from MP-23/25 warrants
    a retry. R5's manifest does not exist; the dated memo gates it.
  - **S0 exit**: exactly one candidate chosen as row 3 — the first new
    research question; the unchosen close with one dated reason each, stamped
    in the same sitting; the chosen candidate's protocol (site, metric,
    negative control, kill-date) is pre-registered in S5 before the first
    pass, exactly as the ledger's row-3 cell says; the terminus declared.
- **Exit**: the intake table signed; ADR-0006 opened with rows, windows and
  kill-dates; row 3 chosen, three candidates closed with reasons; the
  terminus declared.

## Session 1 — the gate-debt stamping + shelf baseline (~1 h)

- **Row 8 (standing gate debt)**: W&B, clean-clone proof, graduation proof,
  `reproduce-multiseed` exp2/exp5 — each cell ends LAUNCHED (with its
  transcript/artifact) or CLOSED (with one named reason), in the same sitting
  that decides the row. A claimed closure without its transcript stays open.
- **Row 6 (shelf baseline)**: the hostile-webmaster walk of the live site +
  Space health at zero (links, assets, a11y, orphans); the claims gate re-run
  on the live surface — a live public number never exceeds the record. The
  baseline enters LAUNCHED with the transcript at zero, or CLOSED with the
  walk's one reason.
- **Exit**: row 8's cells stamped; row 6's baseline stamped; the gate-debt
  transcript file written (`checklists/`), the hostile-webmaster transcript
  at zero.

## Session 2 — the consumption sitting (rows 1, 5) (~1–2 h)

- **Row 1 (Rung-6 artifact — consumes ADR-0005 row 7, the ACDC pilot's
  verdict)**: the pilot's pre-registered protocol (edges, metric, negative
  control, kill-date) was executed by MP-31 — subgraph recovered, or the
  scheduled negative as the first-class result. This sitting consumes it: the
  Rung-6 section (subgraph recovered) or the trial table (scheduled negative),
  every number manifest-tagged. EAP attribution compared against the
  intervention ground truth if the head existed.
- **Row 5 (paper v2 diff)**: sections open only for manifests on disk; `make
  paper` compiles in the CI mirror; every number manifest-tagged; reverse
  claims audit at zero. The v2 diff skeleton is drafted against the Rung-6
  artifact and the rows MP-29/MP-30 stamped.
- **Exit**: row 1 dated (section or trial table, manifest-tagged); row 5's
  diff skeleton drafted; the paper's section table written against disk.

## Session 3 — the essay annex v2 (~2–3 h)

- **Row 4 (`portfolio/essay-annex-2.md`)**: the two verdict sets (the
  positive-negative science and the premiere's public arc) distilled into one
  dated annex — every number manifest-tagged; the reverse claims audit at
  zero (prose → manifest → command); each claim's "what would falsify this"
  column filled at writing time (Gelman & Loken, applied to stranger-facing
  prose). The annex is never rewritten afterwards, only amended via dated
  annexes (the MP-23/24 inheritance).
- **Exit**: row 4 dated; the annex exists with the reverse claims audit at
  zero; the essay cites only disk.

## Session 4 — the stranger round 2 intake (~1 h)

- **Row 7's window opens** (the ledger's window: intake S4, kill-date S5).
  The feedback-to-fixes matrix is pre-stamped: friction point → cause → dated
  fix → re-check row. The self-review substitute — written in S2, from the
  stranger's chair — is filed before the window closes, so a silent window
  can never close the row with a skip.
- **Exit**: row 7's window open with its kill-date declared; the substitute
  filed; the matrix's column headers committed.

## Session 5 — the research row pre-registration + launch (~2–3 h)

- **Row 3 (the first new research question)**: the chosen candidate's protocol
  written before the first pass — site, metric, negative control, kill-date,
  the "what would falsify this" column at writing time — and the run launched
  under a heartbeat while it is live. The verdict (or the scheduled negative
  from the manifest) is the row's result, manifest-tagged.
  - If C3 was chosen: heterogeneous-feature superposition (Elhage et al.
    ch. 2–3) — features with varying importance/frequency trained into the
    Rung-3 superposition model; the metric is the phase-transition point and
    superposition ratio per feature class; the negative control is the
    uniform-importance baseline; kill-date pre-registered.
  - If C2 was chosen: the standard-scale head sweep with its pre-registered
    budget, seeds and detection threshold; the same protocol machinery.
- **Row 2 (scaled-R1 artifact — consumes ADR-0005 row 8's verdict)**: the
  scale-up result paragraph, or the no-head negative from MP-29's verdict as
  the row's first-class result; manifest-tagged.
- **Row 7's kill-date (the ledger's window)**: no feedback by this sitting →
  row 7 closes with the S2 substitute; feedback present → the matrix is
  drafted here and the fixes land with dates.
- **Exit**: row 3 pre-registered and launched with its heartbeat live; row 2
  dated; row 7 closed or drafted at its kill-date.

## Session 6 — the research verdict sitting (~1–2 h)

- **Row 3's verdict**: read from the manifest — the run completed and the
  verdict is dated, or the window closed and the scheduled negative is the
  result. Either way the row is stamped in this sitting, and the unchosen
  candidates stay closed (a closed row is never re-opened without a NEW row).
- **Row 5 complete**: the paper v2 diff finished — every section open only
  for its manifest, `make paper` green in the CI mirror.
- **Exit**: row 3 dated either way; row 5's diff complete.

## Session 7 — the shelf rehearsal + the re-check row (~2–3 h)

- **Row 6 rehearsal**: the hostile-webmaster walk at zero on the live site +
  the Space health check (links, assets, a11y, orphans, dead figures) — the
  claims gate re-run beside the browser, every public number clicked back to
  disk.
- **Row 7's re-check row**: the fixes matrix re-read in the same sitting as
  the fixes (feedback present), or the substitute's closure re-confirmed
  (silent window) — row 7 dated either way.
- **Exit**: row 6 dated or closed; row 7's re-check row dated; the
  hostile-webmaster transcript at zero.

## Session 8 — the release (~1 h)

- ADR-0006 at **zero UNDECIDED rows** — each LAUNCHED-with-date or
  CLOSED-with-one-reason; the continuum law honored (exactly one research row
  opened, its verdict or scheduled negative in the ledger); the merge green
  locally and on GitHub; `dev == main`; home wired; this roadmap archived with
  its deviations — every deviation a dated ledger note.
- **Exit**: the merge; `dev == main`; the ledger is the phase's after-the-fact
  truth; the program has a chosen direction, not a trailing mood.

## Gate criteria (pre-registered, from the sessions above)

1. S0: intake table signed (MP-31's release: ADR-0005 zero UNDECIDED + first
   live URL stamped + `verify-claims` at its actual count); the continuum
   choice made — exactly one row 3 opened, three candidates closed with dated
   reasons in the same sitting; ADR-0006 opened; the terminus declared.
2. S1: row 8 stamped (LAUNCHED with transcript or CLOSED with reason); row 6's
   baseline stamped; the hostile-webmaster transcript at zero.
3. S2: row 1 dated (Rung-6 section or trial table, manifest-tagged); row 5's
   v2 diff skeleton drafted.
4. S3: row 4 dated (essay annex v2; reverse claims audit at zero).
5. S4: row 7's window open with its kill-date declared; the substitute filed.
6. S5: row 3 pre-registered + launched (protocol before the first pass,
   heartbeat live); row 2 dated; row 7 closed or drafted at its kill-date.
7. S6: row 3's verdict dated or closed; row 5's v2 diff complete (`make paper`
   green in the mirror).
8. S7: row 6 dated or closed; row 7's re-check row dated; the walk at zero.
9. S8: ADR-0006 zero UNDECIDED rows; the merge green; `dev == main`; home
   wired; this roadmap archived with its deviations.

## The one measured line (status)

ADR-0006 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row (row 3) whose verdict (or scheduled negative) re-derives from a
manifest; the hostile-webmaster walk at zero on the live shelf; `dev == main`
and the program's chosen direction, stamped in the same sitting as the merge.

## Deep-dive study plan

1. **Elhage et al. 2022, ch. 2–3 — Heterogeneous-feature superposition:
   importance and frequency as the two axes of superposition, and what a
   pre-registered C3 protocol must measure** (the phase-transition point, the
   superposition ratio per feature class, the uniform-importance negative
   control). The reading that makes the S0 choice a decision, not a mood; read
   before S5's protocol is written.
2. **Conmy et al. 2023; Hanna et al. 2024 — ACDC and the EAP lineage: edge
   sets, attribution metrics, negative controls, the failure modes EAP names.**
   The Rung-6 artifact (row 1) consumes MP-31's executed pilot — this reading
   is what makes the consumption a verdict read correctly, not a re-run.
3. **Nanda et al. 2023; Power et al. 2022 — Grokking scaling: the P-sweep
   story and the C1 closure memo's canon.** C1's opens-only-if is already
   false; the reading is what makes the S0 closure a decision, and the
   dense-solution characterization MP-29 produces is its artifact.
4. **Bricken et al. 2023 — SAE monosemanticity on toy features: dictionary
   learning on the superposition model, L0 and FVE vs the no-head baseline.**
   For the C4 memo and R5's dated gate; if row 8's SAE debt is open, read
   before S0's adjudication.
5. **Shelf engineering: Quartz v4 health, Gradio CPU packaging, the claims
   gate in the site build.** The maintenance row (row 6) as a build system:
   the hostile-webmaster walk, a live public number that never exceeds the
   record, the gate re-run on every merge.
6. **The annex craft: writing for strangers.** Distilling two verdict sets
   into one dated annex — every number manifest-tagged, the reverse claims
   audit at zero, the negative as the signature rather than the gap, and the
   30-second spoken claim that survives without code.

## Documentation contract

- This roadmap, pre-registered (the file you are reading).
- ADR-0006's eight rows stamped with dates and verdicts — LAUNCHED or CLOSED,
  nothing "awaiting"; rows 1–2 consumed from ADR-0005's verdicts; row 3 the
  first new research question with its protocol note and heartbeat; rows 4–8
  the continuum law's decisions.
- `portfolio/essay-annex-2.md` — the v2 annex, manifest-tagged, never
  rewritten after release, only amended via dated annexes.
- The paper v2 diff (`portfolio/paper/main.tex` v2 + diff log): sections open
  only for manifests on disk; `make paper` green in the CI mirror.
- The shelf health sheet + hostile-webmaster transcript (site + Space at
  zero); the claims gate re-run on every merge.
- The gate-debt transcript file (`checklists/gate-debt.md`): each cell's
  transcript or one-line reason, dated in S1.
- The research row's pre-registration note (site, metric, negative control,
  kill-date) in `06_production_ai/notes/` + the heartbeat artifact.
- `00_meta/03-progress-log`: one dated entry per session; this roadmap wired
  into home on release; the continuum ledger's rows cited by the skill tree's
  publication flips.

## Practical exercises and challenges

1. **Ex-A · The C1–C4 adjudication drill (S0):** write each candidate's
   opening-or-closure memo in three sentences with a falsifier, then decide
   exactly one to open; the unchosen close with one dated reason, stamped in
   the same sitting.
2. **Ex-B · The consumed-verdicts reverse audit (S2):** every number from
   ADR-0005 rows 7–8 traced to its manifest and its command; the rest struck
   with a reason — the hostile-webmaster test of my own prose.
3. **Ex-C · The annex distillation (S3):** the two verdict sets distilled into
   one dated annex — same facts, three registers (the paper's sentence, the
   annex's sentence, the 30-second spoken claim); the delta between them is
   where my understanding leaks.
4. **Ex-D · The research pre-registration hand-roll (S5):** the protocol
   (site, metric, negative control, kill-date) written before the first pass,
   the "what would falsify this" column filled at writing time, the heartbeat
   live while the run is live.
5. **Ex-E · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
6. **Ex-F · The hostile-webmaster walk v2 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript.
7. **Ex-G · The gate-debt closure stamping (S1):** W&B, clean-clone proof,
   graduation proof, `reproduce-multiseed` — each ends
   LAUNCHED-with-transcript or CLOSED-with-reason in one sitting; a claimed
   closure without its transcript stays open.
8. **Ex-H · The stranger substitute from the visitor's chair (S2, before the
   window opens):** the self-review written from the chair a stranger would
   occupy — friction points → fixes → re-check row — filed before S4, so the
   S5 kill-date can never close the row with a skip.
9. **Habit · The clock check (every session):** ADR-0006's undated rows, the
   open PR's CI status line, the site's build status — all three before any
   new prose.

## Strategic tips and architectural best practices

- **The one-question law.** A phase that opens two research questions is drift
  by another name; the unchosen candidates close in the same sitting as the
  choice. The continuum law is the mechanical refusal of this drift.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Rows 1–2 are consumed in the sitting that owns them, exactly as
  ADR-0005 executed or closed them.
- **The shelf is a row, not a mood.** Maintenance has dates, heartbeats and a
  hostile-webmaster transcript; a live public number that exceeds the record
  is a blocked row, not a to-do.
- **Annexes are amended, never rewritten.** The essay annex v2 inherits the
  annex doctrine the record built at MP-23/24: a new annex appears via a dated
  fork, the original preserved — the science's negative-amendment discipline,
  applied to prose.
- **The S0 gate is a checklist with receipts.** MP-31's release report (zero
  UNDECIDED premiere rows, the live URL, `verify-claims` at 0) is a condition
  with artifacts, not a paragraph — the MP-26 precedent (a continuation
  gated on a release that never landed) is the permanent warning.
- **The pre-registration cadence is the record's discipline.** This roadmap is
  pre-registered while MP-31 stands unexecuted — three phases stacked without
  execution is the drift the record has named since MP-18, and Session 0 is
  the mechanical refusal of it: no release, no phase.
- **The negative stays the signature.** The row that closes with one reason is
  stamped like the row that launched; the continuum's first question earns
  its verdict or its scheduled negative with equal polish.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED rows
  at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story**: *the capstone premiered and the program
  continues — one pre-registered question, one dated verdict, the shelf
  health-checked with receipts, and every public number still re-deriving
  from one command line.* Every artifact this phase launches is written to
  that standard.

## Links

- [[00_meta/30_micro-phase-31-the-premiere]] — the roadmap this phase
  consumes; its release report and ADR-0005 stamps are Session 0's starting
  artifact.
- [[00_meta/29_micro-phase-30-the-consumption]] ·
  [[00_meta/28_micro-phase-29-the-positive-negative]] — the paper and science
  lanes whose residue (the PDF, the verdicts, the manifests) is this phase's
  intake.
- [[00_meta/25_micro-phase-26-the-continuation]] — the original continuation
  pre-registration, gated on a release that never landed; ADR-0006 was built
  for it, and this phase executes that ledger under the same law.
- [[docs/adr/0006-continuum-ledger]] — this phase's ledger: the eight rows it
  stamps LAUNCHED-with-date or CLOSED-with-one-reason, and the frozen
  candidate set C1–C4.
- [[docs/adr/0005-premiere-ledger]] · [[docs/adr/0004-horizon-ledger]] ·
  [[docs/adr/0003-research-return-ledger]] — the intake and the machines
  whose rows reopen here as NEW rows under this phase's dates.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[07_capstone/research-plan]] — the research plan the paper and the essay
  distill.
- [[00_meta/03-progress-log]] — the dated journal entries per session,
  including the rows that closed and the launches that failed (the MP-12
  lesson, applied to URLs).
