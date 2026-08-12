---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-12
---

# Micro-Phase 30 — The Consumption: the verdicts become the record

Written as a personal learning log and a public record, like every roadmap before it.

MP-29 decides the science: the positive control clears the harness or convicts
it, the microscope's three trials run their budget, the dense solution gets
characterized as a contribution, and the R1/R4/R5 lanes close their rows the
day they are decided. This phase consumes that release — whatever the rows
said — and converts the dated ledger into the finished public artifact:
the paper in prose and PDF with every section gated on a manifest, `make
paper` compiling in the CI mirror, RESULTS.md at its final trust order, the
graduation proof answered from disk, and the first stranger's eyes on the
whole thing. The synthesis MP-24 pre-registered on 2026-08-09 never executed;
this phase is that synthesis, on a new clock, consuming MP-29 instead of
MP-23, under the horizon ledger (ADR-0004) that was its designed instrument.

The record's deepest law applies here as everywhere: a promise can be
re-planned forever, but a dated row is answered. MP-30's only honest failure
mode is writer's evasion — a sentence whose number has no manifest — and that
mode is pre-empted mechanically, not by resolution: a paper section opens only
when its manifest exists on disk, and the residual is struck with a date,
never softened.

## Where this phase starts (state review, verified against the repo 2026-08-12)

The intake is MP-29's release report; below is what the record stands at the
moment of pre-registration, so this roadmap's claims are auditable from day
one. MP-29's Session 8 updates every line; nothing here re-plans a single row
of it.

- **Tree state**: `dev` clean at the MP-29 pre-registration merge (PR #61
  squashed, dev reconciled with main); nothing of MP-29 executed yet — its
  Sessions 0–8 stand as pre-registered, and its residue rows (the R1 verdict,
  the R4/R5 chain, verify-claims → 0, paper prose, release) are this phase's
  intake, per the record's law that a session is not over while a row it owns
  is undated.
- **ADR-0003**: row 1 stamped (LAUNCHED 2026-08-11, NO-GROK, val 1.0, Fourier
  dense, k_99 = 111/113); row 2 in flight (trial 1 `--no-normalize-embeddings`);
  rows 3–7 UNDECIDED. MP-29 stamps 2–7; this phase consumes the stamped set
  exactly as it lands.
- **The manifests**: `results/exp2_grokking.json` exists but carries
  `git_dirty: true` (git_sha d48f9ad, produced mid-phase) and the P=113
  checkpoints were cleaned after the verdict — so re-derivation requires
  MP-29's re-run, which is exactly its Session 0's dated option. The
  standard-scale R1 manifest does not exist (the old `exp1_induction_heads.json`
  is the sub-standard run, d_model=24 / 150 epochs / acc ≈ 0.004).
  `results/exp5_sae_dashboard.json` does not exist.
- **The CI floor**: `make verify-claims` at its current 3 problems (dirty-tree
  exp2 manifest; Rung 2 section tag missing; Rung 5 section tag missing) —
  MP-29's one measured line drives it to 0, and 0 is this phase's
  precondition, not its hope. The tracked 185 tests, ruff, blocking mypy and
  markdownlint baselines were all green at MP-28's release and nothing has
  changed under them since.
- **The synthesis machinery, per MP-24's pre-registration**: the paper
  scaffold (`portfolio/paper/main.tex`) still carries the `% TODO` gate — "do
  not write this section until `results/exp2_grokking.json` exists" — every
  section unopened; `make paper` compiles the PDF when a LaTeX toolchain is
  present; the horizon ledger (ADR-0004) has five rows, all UNDECIDED; the
  premiere ledger (ADR-0005) and the continuum ledger (ADR-0006) are
  pre-registered and frozen — not this phase's rows.
- **The scientific ledger across all runs to date**: no run in this
  repository's history has produced a sparse Fourier solution (P=59 dense,
  P=113 k_99 = 111/113). Whatever MP-29's control says, the story the paper
  tells is the one the dated rows tell — no more, no less.

## Design decisions

- **The paper is the flagship artifact, and its sections are manifests-first
  (inherited from MP-24, now executable).** A section opens only for a
  manifest that exists on disk — Grokking opens on `results/exp2_grokking.json`
  clean, Induction on the standard-scale exp1 manifest, SAE on
  `results/exp5_sae_dashboard.json`; Superposition, Circuit Patching and
  Limitations have live manifests today and open in Session 1, not Session 8.
  `make paper` enters the CI mirror in S0 so the paper rots loudly or not at
  all, and the LaTeX toolchain decision is a Session-0 item, never a
  Session-6 surprise.
- **Every number is manifest-tagged before it is typed.** A sentence whose
  number has no `<!-- manifest: results/*.json -->` tag is opinion; the
  hostile-webmaster audit (the reverse pass: from prose to manifest to
  command) is a session, not a mood. `verify-claims` at 0 is the paper's
  visa, and the visa is checked twice — once at S0 intake, once on the
  clean-clone rehearsal in S7.
- **The horizon opens as dated rows (ADR-0004), never as a mood.** The five
  horizon rows — the ACDC pilot pre-registering in S4 or closing with its
  reason, the stranger review with its human-dependency rule, scaled-up R1
  opening only on MP-29's head verdict, the 10-minute talk scripted twice,
  stop-and-publish — are decided in the same sitting that decides them, under
  the record's two-state law. What MP-29's R1 verdict was decides rows 1 and
  3; nothing else does.
- **The stranger review is a scheduled row with a pre-built substitute
  (inherited from ADR-0004, now executed).** A real human reads the paper
  within the window; their top three friction points become dated fixes in
  the same sitting as the reading. If no reader answers, the row closes with
  one reason and the recorded self-review substitute — written in S2, before
  the window opens, from the stranger's chair. Never a silent skip.
- **The 10-minute talk is a deliverable, written twice.** Draft one is
  distilled from the paper; draft two is written from memory — the second is
  the real one, and the gap between them is the paper's weak argument made
  visible. It is the showcase artifact the public arc can host, and it forces
  the argument to survive without code.
- **The one measured line**: `make verify-claims` at **0**, held across the
  phase, and `make paper` green on a clean clone — the PDF that exists, from
  disk, with zero numbers the claims gate cannot re-derive. Prose is the
  witness; the manifest is the referee.
- **The premiere and the continuum stay frozen (inherited laws, reapplied).**
  ADR-0005's eight rows and ADR-0006's candidate set are not this phase's
  rows; zero new research questions open here. The premiere's own gate — no
  PDF, no phase — is exactly what this phase is for: its roadmap is written
  by the phase that owns it, on the cadence the record has kept since MP-27:
  pre-registration when the phase before it is executing, never stacked.
- **The terminus is stamped at Step 0**: release = this roadmap's merge + 14
  calendar days. On that date the phase ships everything the rows decided —
  the residue is a dated list, never a silence (inherited, still true).

## Session 0 — the disk truth + the toolchain (2026-08-12, ~1 h) — next

- MP-29's release consumed row by row into an intake table: ADR-0003 rows 1–7
  as stamped (dates, verdicts, manifest tags), `make verify-claims` at its
  actual count (0 if MP-29 landed its line; otherwise the residue is listed
  with the row that owns it — intake, not re-planning).
- The LaTeX toolchain decided and proven: `make paper` on the empty scaffold
  either produces the PDF or names the blocker with the install line — the
  same S0 honesty the machine-budget audit taught MP-27.
- The paper's section table written against disk: which sections open now
  (their manifests exist), which open on MP-29's rows (their manifests are
  promised), which stay struck with a date. The table is this phase's map and
  its seal.
- The CI floor re-verified locally: tracked tests green, ruff clean, blocking
  mypy clean, markdownlint 0 on changed notes.
- **Exit**: the intake table signed; `make paper` green or dated; the section
  table committed to the roadmap's linked notes.

## Session 1 — the paper, part I: the sections whose manifests exist (next)

- Superposition (manifest live), Circuit Patching (manifest live), Limitations
  and Related Work written first — the sections nothing can take away — every
  number manifest-tagged, each claim's "what would falsify this" column filled
  at writing time (Gelman & Loken, applied to prose the way the ledger always
  applied it to data).
- Related Work also carries the paper's honest spine: the NO-GROK verdict
  written as the record's own result, not a confession — "grokking modular
  addition at P=113 was not reproduced under this protocol on this machine
  within this window; here is the algorithm the model found instead" (the
  sentence MP-29's characterization exists to support).
- `make paper` runs in the local CI mirror; the PDF is born ugly but alive.
- **Exit**: Part I compiles; every Part-I number re-derives via
  `make verify-claims` from disk.

## Session 2 — the paper, part II: the sections the rows opened (next)

- Grokking opens on MP-29's clean exp2 manifest (the re-run or the recorded
  decision); Induction opens on the standard-scale exp1 manifest; SAE opens
  on exp5 — each only if it exists, each with its falsification column, the
  struck sections dated, not softened.
- The stranger's-chair self-review drafted (before the real window opens):
  the three friction points I would raise as a first reader, with the dated
  fixes I would accept.
- **Exit**: the full PDF compiles; the stranger's-chair document filed; the
  section table reconciled to disk — nothing open that no manifest opened.

## Session 3 — RESULTS v-final + the portfolio (next)

- `portfolio/RESULTS.md` at its final trust order: every rung row
  manifest-tagged, the trust list rewritten from the dated verdicts, the
  home page's headline line updated to the record's own sentence — MP-29's
  release report, not a second draft of it.
- The portfolio's public surfaces reconciled to disk: `portfolio/README.md`
  (the "how far" sentence), `portfolio/model-card.md`, `portfolio/projects/`,
  the figures that exist — every link that resolves, every figure that a
  manifest's command actually produced.
- **Exit**: the hostile-webmaster pass over the portfolio at zero (broken
  links, dangling figures, orphan claims); RESULTS' trust order finalized.

## Session 4 — the horizon decided (next)

- ADR-0004 rows decided in the sitting that decides them: row 1 — the ACDC
  pilot's pre-registration written (sites, metric, negative control, kill-date)
  or closed with its one reason; row 3 — the scaled-up R1 protocol or the
  scheduled no-head negative from MP-29's verdict; rows 2, 4, 5 — dispatched,
  drafted, or declared, each in the same sitting.
- The stranger review dispatched with the paper attached and the window
  stated; the 10-minute talk's draft one written from the paper.
- **Exit**: ADR-0004's rows LAUNCHED or CLOSED with dates; nothing "awaiting";
  the premiere ledger (ADR-0005) still unopened — by design.

## Session 5 — the stranger's eyes + the talk from memory (next)

- The stranger's friction points (or the self-review substitute, if the
  window closed silent): three points → three dated fixes → the re-read row
  stamped in the same sitting.
- The 10-minute talk, draft two, from memory — timed once, cut to the paper's
  one claim, no code on the slide.
- **Exit**: ADR-0004 row 2 stamped either way; draft two exists and runs
  under 11 minutes.

## Session 6 — the graduation proof + the paper's final pass (next)

- The capstone gate answered from the phase's own numbers: the Fourier +
  progress-measures + causal-ablation assembly with the dense reading as the
  honest answer — or closed with its dated reason. The proof lands whatever
  MP-29's rows decided; a verdict without a manifest is not a verdict.
- The paper's final pass: abstract, conclusion, one 30-second version of the
  record's claim; the stranger's fixes folded in.
- **Exit**: ADR-0003 row 7's residue closed; the PDF compiles with the
  abstract's every number tagged.

## Session 7 — the clean-clone rehearsal (next)

- The one-commandline transcript, executed from a fresh clone: sync → suite →
  verify-claims → paper → PDF — every step logged with its output line; the
  walkthrough ADR-0005 row 5 pre-registered, this phase's only touch with the
  premiere ledger's material.
- The hostile-webmaster pass again, this time over the whole portfolio + paper
  build, at zero.
- **Exit**: the transcript saved; no hidden hand — the clone is the referee.

## Session 8 — the release (the fixed terminus date)

- ADR-0004 at zero UNDECIDED rows; the merge green locally and on GitHub;
  the premiere and continuum ledgers untouched — this phase opened zero new
  research questions; the residue is a dated list.
- **Exit**: the merge; this roadmap wired into home as the executed record;
  the next phase's pre-registration seeded only from what actually happened.

## Gate criteria (pre-registered, from the sessions above)

1. S0: intake table signed; `make paper` green or dated; section table written.
2. S1: Part I compiles; every Part-I number re-derived from disk.
3. S2: the full PDF compiles; the stranger's-chair document filed.
4. S3: hostile-webmaster pass at zero; RESULTS' trust order final.
5. S4: ADR-0004 rows stamped the same sitting; nothing "awaiting".
6. S5: row 2 stamped either way; the talk's draft two under 11 minutes.
7. S6: the capstone proof answered from disk; the PDF compiles final.
8. S7: the clean-clone transcript executed, every step logged; S8: zero
   UNDECIDED rows; the merge green; the phase wired into home.

## The one measured line (status)

`make verify-claims` at **0** — currently 3, owned by MP-29's line (3 → 2 in
its S0, 2 → 0 by its S6). This phase does not inherit problems it did not
cause: at S0 the count is re-derived and the residue is owned by a row; from
S1 onward, 0 is the paper's visa and every session re-checks it.
`make paper` on a clean clone, green, is the second half of the line — the
PDF is this phase's ship date, the same one MP-24 always owed.

## Deep-dive study plan

1. **The negative as scholarship** — how the MI/ML literature ships negatives:
   the structure of a "not reproduced under this protocol" claim (protocol,
   window, machine, criterion), what makes it citable, and the honest-paragraph
   canon the paper's Grokking section must match. The phase's spine is also
   its study topic (inherited from MP-29, now written as prose).
2. **The paper's own canon, read as Related Work** — Nanda et al. 2023
   (progress measures, the ~√P dictionary), Power et al. 2022 (grokking the
   phenomenon), Elhage et al. 2021/2022 (circuits, superposition), Olsson et
   al. 2022 (induction heads), Bricken et al. 2023 and Zhang & Nanda 2024
   (SAEs, patching best practices): each section's claims positioned against
   the paper's real references, with the dense-solution reading as the
   delta, not the echo.
3. **Circuit figures as arguments** — the Transformer Circuits visual
   language (heads as lookup tables, residual streams as highways, the
   DFT-as-clock pictures): what a TikZ/Matplotlib circuit figure must prove
   to be worth a page, and how the dense solution's per-head dictionary gets
   drawn without inventing structure.
4. **Epistemic writing** — Gelman & Loken's garden of forking paths applied
   to prose: a pre-registered number cannot be re-forked later, so the
   manifest tag is the fork's lock; the essay annex's reverse claims audit
   as the second reader every crafted sentence must survive.
5. **The talk that survives without code** — spoken-explainer craft: the one
   sentence, the one picture, the one analogy; what a 10-minute version of
   the dense-solution story loses from the paper, and what it must keep to
   stay honest (the falsification column travels with the talk).
6. **The horizon's science, read ahead of its decision** — ACDC and the
   EAP/attribution-patching lineage (Conmy et al. 2023) as the Rung-6
   resurrection candidates, and the induction-head scaling literature
   (Olsson's reported d_model ≈ 128 formation floor) for the scaled-R1 row:
   the S4 decisions are made with the papers open, not from memory.
7. **The stranger's chair** — the craft of self-review as first-reader: what
   an external review needs to falsify (the self-patch test of prose: would
   an honest reader with no stake in the record believe the negative?).

## Documentation contract

- This roadmap, pre-registered (the file you are reading).
- ADR-0004's five rows stamped with dates and one-line reasons; ADR-0003's
  rows consumed as decided; ADR-0005/0006 untouched — zero new research
  questions opened.
- `portfolio/paper/main.tex`: sections opened only for manifests, every
  number manifest-tagged; the PDF compiles via `make paper` in the CI mirror;
  the abstract carries the record's one sentence.
- `portfolio/RESULTS.md`: v-final — rung tables manifest-tagged, trust order
  rewritten from dated verdicts; `portfolio/README.md` and
  `portfolio/model-card.md` reconciled to disk.
- The stranger-review dispatch + the stranger's-chair substitute; the
  10-minute talk drafts 1 and 2; the clean-clone transcript.
- `00_meta/03_progress-log`: one dated entry per session; this roadmap wired
  into home on release.

## Practical exercises and challenges

1. **Ex-A · The number-tracing drill**: take every headline number in
   RESULTS.md and the paper, and trace it to its manifest and its command —
   the reverse claims audit as a table, every row a command that runs. The
   hostile-webmaster test of my own prose.
2. **Ex-B · The stranger's chair, before the stranger**: write the three
   friction points as an external first reader — before the dispatch window
   opens — with the fixes I would accept. The substitute review is built
   before it is needed, so the human dependency can never strike a silent
   row.
3. **Ex-C · Three registers, one verdict**: the NO-GROK/dense-solution story
   written as (1) the paper's Methods-and-Results paragraph, (2) the essay's
   one-line sentence, (3) the 30-second spoken claim. Same facts, three
   audiences; the delta between them is where my understanding leaks.
4. **Ex-D · The 10-minute talk from memory**: draft one from the paper,
   draft two from memory, both timed; the gap between them is the paper's
   weakest argument — fixed in the paper, not rehearsal'd around.
5. **Ex-E · The clean-clone rehearsal**: one commandline from a fresh clone to
   a compiled PDF, executed and logged — the transcript is the deliverable,
   and any step that needs a hidden hand is a claim that fails its audit.
6. **Ex-F · The horizon drill**: the 5-column decision table for ACDC
   (fire-with-protocol vs close-with-reason) and for scaled-R1 (open-with-
   protocol vs scheduled-negative), written before the data this phase
   consumes exists — the fork's lock, applied to the post-capstone set.
7. **Ex-G · The abstract in 30 words**: the record's whole journey — from
   gradient to transformer to circuit, the negative that became the
   contribution — compressed to one sentence that survives contact with
   strangers.

## Strategic tips and architectural best practices

- **The manifest is the referee; prose is the witness.** A section does not
  open without its manifest; a number does not get typed without its tag;
  `verify-claims` at 0 is checked at intake, at S6, and again on the clean
  clone. The paper cannot be postponed by a missing verdict, and it cannot
  be padded by one either.
- **The dated negative outlives the positive.** The NO-GROK verdict, the
  no-head negative, the dense reading — shipped with the same polish as the
  win — are this record's signature, and the paper's Grokking section is
  where the signature is witnessed by the widest audience.
- **One measured line per phase.** This phase's line is the compiled PDF on a
  clean clone with the claims gate at zero — every gate above is a row stamp
  or a compile, never prose.
- **Decide the horizon in the sitting that decides it.** ADR-0004's rows are
  stamped the day they are decided — LAUNCHED with a window or CLOSED with
  one reason; "awaiting" is not a row state, a second phase of it is drift in
  the ledger's own terms.
- **The stranger is a law, and the substitute is built first.** The
  self-review exists before the window opens; the human dependency can fail
  safely, which is how a schedule-dependent row stays honest.
- **The talk survives without code, or it does not survive at all.** The
  from-memory draft is the real one; if the argument needs the repository to
  stand, it is not an argument yet.
- **Architecture laws, unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(paper)`, `(infra)` scopes; CI green before any
  merge — the floor re-verified locally before every push; zero UNDECIDED
  rows at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story**: *the pipeline worked perfectly and
  produced a genuine negative; I characterized the algorithm it found instead;
  then I wrote it down so a stranger could check every number.* Every artifact
  this phase writes — the paper, the RESULTS trust order, the talk, the
  transcript — is written to that standard.

## Links

- [[00_meta/28_micro-phase-29-the-positive-negative]] — the roadmap this
  phase consumes; its release report is the intake this roadmap is written
  to receive.
- [[docs/adr/0003-research-return-ledger]] — the rows this phase consumes as
  decided; zero re-negotiation.
- [[docs/adr/0004-horizon-ledger]] — the rows this phase decides: the ACDC
  pilot, the stranger review, scaled-up R1, the 10-minute talk,
  stop-and-publish.
- [[docs/adr/0005-premiere-ledger]] · [[docs/adr/0006-continuum-ledger]] —
  frozen by design; the premiere opens only on this phase's release (no PDF,
  no phase), the continuum stays at zero new questions.
- [[00_meta/23_micro-phase-24-the-synthesis]] — the synthesis this phase
  executes on a new clock; its pre-registered decisions are inherited as
  written, its session list re-clocked to MP-29's intake.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/grokking-verdict-p113]] · the support notes the
  paper's Grokking section cites.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every number cites, every section opens on.
- [[portfolio/RESULTS]] · [[portfolio/paper/main]] · [[portfolio/README]] ·
  [[portfolio/model-card]] — the artifacts this phase finishes.
- [[07_capstone/research-plan]] — the graduation proof's gate, answered from
  this phase's own numbers.
- [[00_meta/03_progress-log]] — the dated journal entries per session.