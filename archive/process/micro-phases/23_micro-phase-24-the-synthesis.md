---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-09
---

# Micro-Phase 24 — The Synthesis: the ledger becomes the story

Written as a personal learning log and a public record, like every roadmap before it.

MP-23 answers the rows; this phase writes the answers down. Whatever MP-23's
release report says — grok or no-grok at P=113, head or no-head at standard
scale — this phase consumes it row by row and converts the dated ledger into
the finished public artifact: the paper in prose (sections opened only for
manifests that exist), the PDF compiling in the CI mirror, RESULTS' trust
order final, the graduation proof answered, and the first stranger's eyes on
the work. The research-return ledger (ADR-0003) is the source of truth this
phase reads; the horizon ledger (ADR-0004) is the machine it turns on to
decide what comes after the capstone.

The record's deepest pattern is the one every roadmap since MP-18 has enacted:
a promise can be re-planned forever, but a dated row is answered. MP-24 is
where that pattern pays out in prose — the paper cannot be postponed by a
missing verdict, because by this phase's Step 0 every verdict is dated one way
or the other. The phase's only honest failure mode left is writer's evasion:
a sentence whose number has no manifest. That failure mode is pre-empted here
with a mechanical gate, not a resolution: the paper's sections open only when
their manifests exist, and the residual is struck with a date, never softened.

## Design decisions

- **The starting artifact is MP-23's release state, row by row.** Step 0 is a
  truthing pass over ADR-0003's seven rows, the essay annex v1.1 (or its
  absence), `verify-claims` at 0 or at its residue, and the CI floor — the
  same discipline MP-21 applied to MP-20, MP-22 to MP-21, MP-23 to MP-22,
  applied to the research return itself. Nothing re-plans MP-23; this phase
  consumes its report.
- **The paper is the flagship artifact, and its sections are manifests-first.**
  `portfolio/paper/main.tex`'s own rule — "do not write this section until
  `results/exp2_grokking.json` exists" — becomes the phase's gate: a section
  opens only for a manifest that exists on disk, and `make paper` (the PDF
  compile) enters the CI mirror in Step 0, so the paper rots loudly or not at
  all. The LaTeX toolchain decision (MiKTeX on this machine) is a Step-0
  item, not a Session-6 surprise.
- **The horizon opens as a new ledger (ADR-0004), never as a mood.** What the
  repo becomes after the capstone — the real ACDC resurrection of Rung 6, a
  scaled-up R1, the stranger review, the 10-minute talk, or stop-and-publish —
  is decided as dated rows under the same two-state rule (LAUNCHED-with-date
  or CLOSED-with-one-reason), written before the phase's sessions begin.
- **The first stranger is a scheduled row, not a hope.** Before release, a
  real human reads the paper; their three highest-friction points become
  dated fixes in the same sitting as the reading. If the stranger does not
  answer within the window, the row closes with one reason and a
  self-review recorded in its place — never a silent skip.
- **The 10-minute talk is a deliverable.** A scripted explainer, written
  twice — once from the paper, once from memory — forcing the paper's
  essence into spoken prose; the second draft is the real one. It is the
  showcase artifact the public arc (MP-22) can host, and it forces the
  argument to survive without code.
- **The annex is absorbed, never re-planned.** Whatever residue MP-23's
  annex leaves (open rows, struck claims, amended numbers) is consumed in
  Session 4 with a dated reconciliation row; the essay is never rewritten.
- **The terminus is stamped at Step 0**: release = this roadmap's merge + 14
  calendar days. On that date the phase ships everything the rows decided —
  the residue is a dated list, never a silence (inherited, still true).

## Where this phase starts (state review, verified against the repo 2026-08-09)

I checked the tree, the manifests, the ledger rows, the CI floor and the gate
states before writing a single claim here.

- **Tree state**: `dev` and `main` tree-identical after MP-23's Step-0 squash
  (merge 2ff35d9); working tree clean; no open PRs. MP-23 is pre-registered
  with its ADR-0003 ledger (seven rows, all UNDECIDED); its sessions 0–8
  have not started. Its release report is this phase's starting artifact —
  this roadmap is written verdict-agnostic, exactly as MP-23 itself was.
- **The CI floor, re-verified in this session**: ruff clean on `src/ tests/`;
  blocking mypy clean (`src/results.py`, `src/experiments/runner.py`);
  full-tree mypy at its tracked **171** (exit 1, the non-blocking ratchet);
  the full suite green in the mirror (the tracked 185 tests); `make
  verify-claims` at exactly its designed **2 problems** — Rung 2 and Rung 5
  manifestless by design. The mirror's `commitlint-head` step flags
  `bcd0d52` (MP-23's pre-squash step-0 commit, body line > 200 chars) through
  the reconcile merge's second-parent span — the recorded artifact class,
  not a message of this phase; the phase's own commit is linted on a clean
  range before leaving the machine.
- **The research-return ledger (ADR-0003) is the phase's intake**: its seven
  rows (P=113 ×3 seeds, the one-change microscope, R1 standard, R4-on-head,
  R5 re-run, paper/annex, graduation proof) will each end LAUNCHED-with-verdict
  or CLOSED-with-reason before this phase's Step 0 truthing; the paper
  section for a rung opens only if that rung's row carries a manifest.
- **The claim-vs-code pass is Step 0's second instrument.** The paper will
  only carry numbers that survive it. The known candidate list, verified
  this session: the P=113 resume promise vs `exp2_grokking.py`'s actual
  machinery (stateful checkpoint/resume exists only in
  `exp1_induction_heads.py` — `save_training_checkpoint`, RNG-state capture,
  `--resume` — while `exp2_grokking.py` has only `--save-model`); the
  52.2%-vs-0.05% fresh-vs-fixed comparison; the SAE 99.97% FVE at 53% L0
  no-head baseline. Every one of them re-derives from a command or is struck.
- **The horizon (ADR-0004) is written before the sessions**, rows with
  windows and kill-dates, so the capstone's end is a decision, not a drift.

### Bottleneck analysis (ranked by what blocks what)

1. **MP-23's release report — everything consumes it.** The phase cannot
   write a section for a rung whose row is still undated; the treatment is
   the intake table written in Session 0 and the manifests-first rule: a
   section opens only for a manifest on disk. If MP-23's release leaves
   residue, this phase's Session 4 absorbs it with a dated reconciliation
   row — never by inventing prose for missing receipts.
2. **The paper's compile gate.** `make paper` in the CI mirror is decided in
   Step 0 (MiKTeX), not discovered at Session 6 — a missing toolchain on
   release day is a plan failure, not an environment accident.
3. **The prose-vs-manifest discipline.** The paper's only internal failure
   mode is a sentence whose number has no manifest; the phase inscribes the
   negative — a section without its manifest stays a `% TODO` scaffold, and
   the release rehearsal walks the paper with `verify-claims` open.
4. **The stranger-review row is a human dependency.** A dated window with a
   kill-date; if no answer arrives, the row closes with one reason and the
   self-review substitute is recorded — the schedule never absorbs a silent
   wait.
5. **The mypy ratchet (171)** — scheduled, non-blocking, at most one module
   in this phase; it must never be chased while the paper or the release is
   pending.

## 1. Deep-dive study and research topics (bound to a session — no topic without a deliverable)

| Topic | Session | The deliverable that proves the reading |
|---|---|---|
| Whatever MP-23's grokking lane decided: Nanda et al. (ICLR 2023) re-read *against my own Fourier counts* — support measures, the "grokked = sparse" criterion | S2 | The paper's Grokking section written from my log, not from the paper's curves |
| If grokked: Varma et al., *Explaining Grokking through Circuit Efficiency* — the "why now / why never" sentence | S2 | The interpretability paragraph: my learning dynamics told through efficiency, not vibes |
| If not grokked: the microscope's trial table read as a *compression study* — what changed in the train/val gap, not just accuracy | S2 | A one-page compression-dynamics addendum for the paper's honest-negatives appendix |
| Zhang & Nanda, *Best Practices of Activation Patching* — the second re-read, now against the matrix I actually ran | S4 | The "what I did differently from best practice" memo — the reviewer apology drafted before the review |
| If the horizon row opens: the attribution-vs-intervention line (the EAP lineage behind ACDC) | S7 | The real-ACDC pilot's pre-registration: sites, metric, negative control, kill-date |
| One SAE paper chosen by R5's delta: JumpReLU SAEs (Rajamanoharan et al.) if sparsity still disappoints; the monotonicity line otherwise | S5 | A dated decision memo: retry or strike, with the L0/FVE numbers that decide it |
| The distinctiveness gate re-read: the original rungs' own ablations, compared claim-by-claim with mine | S6 | The "what did I add beyond the original" paragraph — the paper's contribution sentence |
| Gelman & Loken, *The Garden of Forking Paths* — final re-read, as the write-up lens | S6 | The paper's Methods oath: every number's fork-tree acknowledged or excluded |

Each reading produces a deliverable — the vault's rule: no topic without an artifact.

## 2. Documentation requirements

- **The horizon ledger (ADR-0004)** — *new*: rows for the real-ACDC pilot,
  the stranger review, the scaled-up R1, the 10-minute talk, and
  stop-and-publish — each with a window, a heartbeat where a run exists, and
  a kill-date, under the ADR-0001 rules; rows end LAUNCHED or CLOSED, never
  "awaiting".
- **The paper in prose** — `portfolio/paper/main.tex` leaves scaffold:
  intro, related work, grokking (whichever way), induction, superposition,
  patching, SAE, discussion, and the honest-negatives appendix. A section
  opens only for the manifest that names it; `make paper` compiles in the
  CI mirror.
- **RESULTS.md v-final** — the "what to trust, in order" summary rewritten
  as the definitive trust order; every Rung table carries its manifest tag
  or a struck note; the Honesty Ledger stays open as the record's spine.
- **The model card** — completed with the final known-limitations list:
  what micro-scale allows and forbids, stated once, dated.
- **The stranger-review row** — the reader's notes kept verbatim in the
  ledger; my three dated fixes beside them.
- **The 10-minute talk script** — one page of spoken prose, filed beside
  the paper; the second (from-memory) draft is the deliverable.
- **New notes (Obsidian, atomic, each linked ≥ 2 others)**: the
  Fourier-algorithm note (if grokked — expanded from MP-23's progress
  measures), the patching-on-a-real-head note (or its negative), the
  SAE-delta note, the adversarial-self-review method note, the
  horizon-decision note.
- **Skill tree** — flips only with a dated manifest behind them: grokking
  [~] → [x] or stays [~] with the reason cited; SAE [~] likewise; the
  horizon rows end LAUNCHED or CLOSED with dates.
- **Progress log** — one dated entry per session; raw pass/fail before
  interpretation; the stranger's verdict logged exactly as given.

## 3. Practical exercises and hands-on challenges

1. **The truthing pass (S0)**: read MP-23's release row by row; the one-page
   scope: what the record can now claim, in trust order. Exit: zero
   unsupported claims in the scope sheet.
2. **The intake table (S0)**: ADR-0003's rows mapped to paper sections —
   which section opens for which manifest, and what the scheduled negative
   is for each rung that closed without one.
3. **The paper sprint (S2–S4)**: eight sections from manifests; two full
   revision passes, the second against the claims → evidence → warrants
   argument skeleton.
4. **The three-hostile-reviewers pass (S5)**: the full paper read as an
   experimentalist, a theorist, and a skeptic; five attack sentences fixed
   per section.
5. **The stranger test (S6)**: a real human reads the paper; I record where
   they stalled and fix their top three points in one sitting, dated.
6. **The re-derivation game (S6)**: every headline number → command →
   manifest → figure, walked as a checklist — `verify-claims` for the whole
   portfolio, not just the automated gate.
7. **The clean-clone closure (S7)**: bare checkout → `uv sync` → full suite
   → `verify-claims` at 0 → `make paper` → site build — one transcript.
8. **The 10-minute talk (S7)**: scripted twice — once from the paper, once
   from memory; the second draft is the real one.
9. **The horizon pilot (S7, if opened)**: the real-ACDC pre-registration —
   EAP on the real circuit with its own negative control and kill-date,
   never a "let's see".
10. **Habit — the clock check (every session)**: the ledger's undated rows,
    the open PR's CI status line, the paper's compile status — all three
    before any new prose.

## 4. Strategic tips and architectural best practices

- **The roadmap is written before the results exist.** Every row here is
  verdict-agnostic; MP-23's data fills cells, never redraws the table.
- **Prose is a distillation, not a recapitulation.** The paper argues from
  wrapped claims; if a sentence needs a manifest to survive, the manifest
  comes first — a section without its receipt stays a scaffold.
- **One stranger, one month.** External review is the cheapest validation
  the record can buy; it is a scheduled row with a kill-date, not a hope.
- **The negative is the contribution** (inherited, now load-bearing): by
  MP-24 the honest negatives are the paper's distinguishing feature — the
  essay's annex was never a confession.
- **Compile early, compile often.** `make paper` in the CI mirror means the
  paper rots loudly or not at all.
- **The demo is the proof.** The 10-minute talk forces the argument into
  spoken prose; the site already exists to host it.
- **The horizon is chosen, not inherited.** ACDC, scale-up, or stop — each
  is a dated row; an undecided horizon is drift by another name.
- **Session clocks beat mood clocks** (inherited, still true): every step
  has a wall clock and an exit gate.
- **No topic without an artifact** (inherited, still the vault's golden
  rule): every reading in Section 1 names its deliverable.

## 5. Step-by-step execution roadmap

```
WEEK 1

SESSION 0 — THE PRE-FLIGHT (~30–60 min)
  CI green locally AND on GitHub (185 tests, ruff, blocking mypy,
  markdownlint); MP-23's release truthing done row by row; the intake
  table written (rows → sections); ADR-0004 opened with its rows and
  windows; the LaTeX toolchain pinned (`make paper` compiles here);
  this roadmap wired into home; pushed to dev; a green GitHub floor.
  Exit: the terminus is declared (release = this merge + 14 calendar
  days); `make paper` is part of the mirror.

SESSION 1 — THE ARGUMENT SKELETON (~2 h)
  The paper's claims → evidence → warrants skeleton for all eight
  sections, written before any prose; each section names its manifest
  or its scheduled negative. Exit: zero prose exists, zero sections
  lack a receipt plan.

SESSION 2 — THE GROKKING + SUPERPOSITION PROSE (~3 h)
  The two sections whose manifests are oldest (Rung 3's is on disk
  since MP-8; Rung 2's, whatever MP-23 decided); the study slot's
  deliverable lands with it. Exit: both sections cite only disk.

SESSION 3 — THE INDUCTION + PATCHING PROSE (~2–3 h)
  The R1 section written from MP-23's verdict — the head at standard
  scale, or the no-head negative as a first-class result; the R4
  section from the real-head validation or its scheduled negative.
  Exit: the patching best-practice memo exists.

WEEK 2

SESSION 4 — THE ANNEX ABSORPTION + REVISION PASS 1 (~3 h)
  Whatever MP-23's annex left open is consumed with a dated
  reconciliation row; SAE + related work + discussion in prose;
  revision pass 1. Exit: all sections exist; residue is a dated list.

SESSION 5 — THE ADVERSARIAL PASS + THE COMPILE (~3 h)
  The three-hostile-reviewers pass over the full paper; five attack
  sentences fixed per section; `make paper` compiles clean in the
  mirror for the first time. Exit: the PDF exists from the source.

SESSION 6 — THE STRANGER + THE RE-DERIVATION (~3 h)
  The stranger reads; their top three points fixed, dated; the
  re-derivation game walked end to end; RESULTS v-final and the model
  card completed; the skill-tree flips stamped. Exit: every headline
  number re-derivable from a walked command.

SESSION 7 — THE REHEARSAL (~3 h)
  The clean-clone closure transcript from a bare checkout; the
  10-minute talk scripted twice; the horizon rows decided with dates
  (ACDC pilot pre-registered or closed with one reason); mypy drift
  at most one module if the budget allows. Exit: the landing plan has
  been walked on a branch.

SESSION 8 — THE RELEASE (the fixed terminus date)
  Merge on green; the paper lands with its date; the horizon rows
  LAUNCHED or CLOSED under dates; home wired; this roadmap archived
  with its deviations — every deviation a dated ledger note. Exit:
  tree clean, `dev == main`, the ledger is the phase's after-the-fact
  truth.
```

## 6. Gate criteria

1. Session 0: the CI floor is green locally AND on GitHub — before the phase
   evicts a single step; MP-23's release truthing done; `make paper` compiles
   and is in the mirror.
2. Session 1: the argument skeleton exists with a receipt plan per section —
   a manifest or a scheduled negative; zero prose without one.
3. Sessions 2–3: prose exists only for manifests on disk; no section cites a
   number the claim-vs-code pass cannot re-derive.
4. Session 5: the PDF compiles from source; the hostile pass produced ≥ 5
   fixed attack sentences per section.
5. Session 6: the stranger read; their top three points fixed with dates;
   every headline number re-derivable from a walked command.
6. Session 7: the talk script exists; the horizon rows are dated; the
   clean-clone transcript is one command line.
7. Session 8: the merge is green; the ledger shows zero undated rows; the
   progress log closes the loop.
8. The record-sanity gate: nothing in the paper or the site exceeds the
   record — every public sentence is verified on disk or struck with a date.

## 7. Showcase note (for the portfolio reader)

The journey's shape is legible to a stranger now: I built a transformer from
nothing, asked it the smallest honest questions, caught real bugs in my own
claims three times and published the catches, answered the two flagship
questions one way or the other under pre-registered clocks — and then wrote
it all down, in the order the evidence allowed: paper, talk, site, a real
reader's notes.

> "The phase that stopped planning and started answering: every row dated,
> every number file-cited, every negative printed as a contribution — and
> for the first time, the record survived a stranger's eyes."

## Links

- [[00_meta/22_micro-phase-23-the-research-return]] — the roadmap this phase
  consumes; its release report and ADR-0003 rows are Step 0's starting
  artifact.
- [[docs/adr/0003-research-return-ledger]] — the intake: the rows this
  phase maps to paper sections.
- [[docs/adr/0004-horizon-ledger]] — this phase's new ledger: the rows that
  decide what the repo becomes after the capstone.
- [[docs/adr/0001-verdict-closure-ledger]] · [[docs/adr/0002-public-arc-ledger]] —
  the two ledger machines the horizon rows inherit.
- [[portfolio/RESULTS]] · [[portfolio/README]] — the results sheet this
  phase writes final; the public shelf the paper lands on.
- [[00_meta/03-progress-log]] — the dated record of every session, including
  the rows that closed.
