---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-11
---

# Micro-Phase 27 — The Unblock: the stack executes

Written as a personal learning log and a public record, like every roadmap before it.

Four roadmaps in a row pre-registered the same two scientific lanes — the P=113 grokking
launch and the standard-scale induction run — and not one of them launched anything. MP-23
opened ADR-0003 and became current, MP-24 pre-registered the synthesis it gates, MP-25
pre-registered the premiere that consumes the paper that consumes the verdicts, MP-26
pre-registered the continuum that consumes the premiere. The log has been naming the
disease since MP-18: *pre-registration without execution is drift by another name.* The
record's deepest law — *a promise can be re-planned forever, but a dated row is answered*
— now stands four deep in undated rows. This phase is where the stack stops stacking: it
executes the oldest dated promises on the shelf, pre-registers nothing new, and ships the
verdicts the next three phases are already waiting for, under their original protocols.

The record's mechanical law was never the problem; the machine it runs on was the
excuse. "Needs a GPU" has been the P=113 lane's recorded reason since MP-8, but the
record itself holds the counter-evidence: exp1's stateful checkpoint/resume (atomic
write, RNG capture, `--resume`, kill-drill-proven bit-identical) has existed since
MP-12, and the probe runs proved the pipeline runs clean on CPU. What has never existed
is that machinery in exp2 — the exact gap MP-26's intake review recorded on its first
day. The unblock is therefore not ambition; it is a port, a clock, and a launch.

## Design decisions

- **The intake is ADR-0003's rows, executed as written.** MP-27 opens no new ledger,
  touches no verdict of ADR-0004/0005/0006, and re-negotiates nothing: the two flagship
  lanes run under the protocols MP-23's Session 0 froze — thresholds, seeds, budgets,
  windows, kill-dates. The only new decision this phase's Session 0 takes is the one
  MP-26 explicitly recorded as belonging there: **the exp2 checkpoint/resume port**,
  which ADR-0003's row-1 disconnect-recovery promise silently presupposes.
- **The hard gate is the machine-budget audit, not the roadmap.** Session 0 opens only
  after a live audit of this machine — cores, RAM, headroom, overnight window — written
  from a real 100-epoch timing probe, with the per-lane wall-time sheet and the kill
  conditions signed before any launch. No audit, no launch: the MP-12 lesson, applied
  to the resource that was available all along.
- **CPU-first ownership.** P=113 × 3 seeds is ~16.5 h serial on the record's own
  estimate, and three small models (d_model=128) on separate cores is one supervised
  overnight (~6 h wall). R1 standard-scale (~17–20 h CPU, fresh batches) is a second
  overnight under `checkpoint-every-250` + resume. Free-tier Colab stays an optional
  accelerator lane with its canary handshake — it is never again load-bearing for a
  verdict this record owes.
- **Launch-then-analyze (the launch reflex, broken mechanically).** Sessions 1–3 exist
  to get both lanes *running with dated rows*; sessions 4–7 analyze whatever lands. A
  session that ends with an undated launch is a failed session by definition — the
  gate is the ledger row, not the prose (inherited from MP-23, now the phase's spine).
- **The continuum law, applied backwards.** Exactly zero new research questions open
  this phase. ADR-0006's candidate set (C1–C4) stays frozen on the shelf, untouched;
  the choice belongs to the phase *after* the stack executes. Science must move before
  the program's next question is chosen — "three open questions is drift" has a twin:
  "four undecided rows is the same drift, re-named."
- **Negative-first, falsification-first.** The scheduled negatives — "P=113 did not
  grok within this budget" and "no head at standard scale" — are drafted in full before
  the long runs finish, printed with the same polish as the wins (the record's public
  signature since MP-23, now load-bearing). Every number this phase will report gets its
  "what would falsify this" column before the number exists (Gelman & Loken, applied at
  the source, always).
- **The one measured line**: `make verify-claims` goes from its designed 2 problems to
  **0** — `results/exp2_grokking.json` and `results/exp5_sae_dashboard.json` land from
  this phase's own runs, and every downstream artifact (paper prose, essay annex, the
  future site) finally has its manifests to cite.
- **The terminus is stamped at Step 0**: release = this roadmap's merge + 14 calendar
  days. On that date the phase ships everything the rows decided — the residue is a
  dated list, never a silence (inherited, applied to the oldest promises first).

## Where this phase starts (state review, verified against the repo 2026-08-11)

I checked the tree, the manifests, the ledger rows, the CI floor and the launch
readiness before writing a single claim here.

- **Tree state**: `dev` and `main` tree-identical (reconciled at intake; the #54 wire
  commit is in), working tree clean on `dev`; MP-23 current with ADR-0003's seven rows
  all UNDECIDED; MP-24 (ADR-0004, five rows), MP-25 (ADR-0005, eight rows) and MP-26
  (ADR-0006, eight rows) pre-registered; no session of any of the four has started.
  The intake chain — MP-23 → MP-24 → MP-25 → MP-26 → this phase — is now four deep,
  and this phase's entire science intake is the rows MP-23 froze under its own clock.
- **The CI floor (the recorded baseline; no `src/` change has landed since)**: 185
  tests green; ruff clean on `src/ tests/`; blocking mypy clean (`src/results.py`,
  `src/experiments/runner.py`); full-tree mypy at the tracked 171 ratchet
  (non-blocking, at most one module this phase); `make verify-claims` at its designed
  2 problems — the two never-produced manifests this phase produces; markdownlint 0
  on changed notes.
- **The exp2 gap, verified at the source again today**: `exp2_grokking.py`'s `main()`
  parser exposes `--save-model`, `--seeds`, `--wandb`, `--probe`, `--micro` — and no
  `--resume`, no `--checkpoint-every`, no checkpoint dir. The full stateful system
  (atomic `save_training_checkpoint`, RNG-state capture, `load_training_checkpoint`,
  three falsification tests) exists only in `exp1`. ADR-0003 row 1's
  "checkpoint-every-500 + resume" promise is therefore **not mechanically real** until
  the port lands — this phase's Session 1 exists for exactly that, with the decision
  recorded the day MP-26 opened.
- **The launch readiness, priced honestly**: the Colab notebook is hardened and the
  probe runs de-risked the recipe (P=59 × three drills: dense 59/59 Fourier mass, no
  grok; the named suspects if P=113 fails are the embedding re-normalization and the
  cosine schedule). The only missing launch preconditions are mechanical (the exp2
  port) and temporal (two supervised overnight windows inside the 14-day clock).
- **The R1→R4→R5 domino, unchanged since MP-10**: the fixed-vs-fresh comparison
  (52.2% vs 0.05%, matched 800 epochs) remains the last trustworthy R1 number;
  standard-scale fresh batches has never run; path patching is still validated only by
  its unit tests; the real-activation SAE result (99.97% FVE, 53% L0) still reads from
  a no-head checkpoint. One launched standard run decides all three rows.
- **The public shelf stays gated**: ADR-0002's five rows (essay, thread, site, Space,
  walkthrough) sit UNDECIDED, `portfolio/projects/` holds a `.gitkeep`, and the paper
  is a scaffold — all correct by design: nothing public opens until the science this
  phase launches has manifests to cite.

### Bottleneck analysis (ranked by what blocks what)

1. **The stack itself — the largest single risk in the record.** Four ledgers,
   twenty-eight undecided rows, zero executed sessions since the stack began. The
   treatment is this phase's constitution: execute, don't pre-register — the "dates,
   not plans" law the record invented, turned on its own most recent invention.
2. **The exp2 checkpoint/resume port.** It blocks CPU-first P=113 (a 5.5 h run cannot
   be launched without a resume path) and it blocks the Colab handshake's honest
   claim. The treatment is Session 1: port first, tests first, kill drill second —
   before any long run touches the machine.
3. **The launch reflex.** The record's original disease, still the clock-critical one:
   both lanes must be running with dated rows by Session 3, or sessions 4–7 have no
   data and the 14-day terminus silently becomes the 15th day. The treatment is the
   undated-launch-is-a-failed-session gate, stamped into the session exits below.
4. **The R1→R4→R5 dependency chain.** Path patching and the meaningful SAE re-test
   cannot be verdict-final without a real head. The treatment is the scheduled
   negative in the ledger with the same weight as the positive — the no-head memo is
   drafted before the head decides.
5. **Manifest debt (the measurable CI line).** The two missing manifests are the only
   reason `verify-claims` reports 2; each landing changes the gate baseline and
   unblocks the paper's first prose. The treatment is the phase's one measured line.
6. **Recurring costs** — the mypy ratchet (171) and the CI floor: scheduled,
   non-blocking, at most one module, never chased while a launch or a revision is
   pending (inherited, still true).

<!-- MP27-SECTION-2 -->

## 1. Deep-dive study and research topics (bound to a session — no topic without a deliverable)

| Topic | Session | The deliverable that proves the reading |
|---|---|---|
| Power et al., *Grokking: Generalization Beyond Overfitting* (2022) — the canonical setup, weight decay, the small-P story | S1 | The run-record cheat sheet beside the launch: config, the two named suspects, windows, kill conditions — one page a stranger could supervise from |
| Nanda et al., *Progress Measures for Grokking* (ICLR 2023) — Fourier frequency counts, distance-to-solution, the "grokked = sparse frequency" criterion | S4 | The progress-measures analysis written against MY run's log — every number from disk, the criterion applied mechanically, not by eye |
| Varma et al., *Explaining Grokking through Circuit Efficiency* (2023) | S4 | One "why now / why never" paragraph interpreting whatever the curve does |
| Olsson et al., *In-context Learning and Induction Heads* (2022) — the induction protocol, fresh-batches rationale | S2 | My frozen definition of "head formed" (diag+1 mass > 0.3 on ≥ 1 head, sustained ≥ 5 checkpoints) — written once, never re-edited after launch |
| Zhang & Nanda, *Towards Best Practices of Activation Patching* (ICLR 2024) — re-read against a real head if one exists | S5 | The patching checklist re-run against the real-head matrix — or the one-page no-head memo naming the failure mode I now have evidence to cite |
| Bricken et al., *Towards Monosemanticity* (2023) + Cunningham et al. (ICLR 2024) — re-read against the phase's best checkpoint | S6 | The R5 verdict memo: sparsity/FVE table annotated honestly, retry or the dated reason the lane stays closed |
| PyTorch serialization + RNG-state semantics — `torch.random.get_rng_state/set_rng_state`, atomic `os.replace` | S1 | The exp2 port note: what I transported, what I changed, why it stays bit-identical |
| The MP-12 kill-drill transcript + the exp1 resume tests | S1 | The resume protocol v2: cadence (500), heartbeat log format, the deliberate-kill rehearsal, the verification command |
| Gelman & Loken, "The Garden of Forking Paths" (2013) — re-read | S3 | The "what would falsify this" column for every number this phase will report, filled before the number exists |
| The CPU throughput probe — `torch.get_num_threads`, per-epoch wall time, memory headroom | S0 | The machine-budget audit: cores × RAM × overnight window, signed before launch |

Each reading produces a deliverable — the vault's golden rule, extended to the phase
whose sessions finally run.

## 2. Documentation requirements

- **The exp2 checkpoint/resume port note + proof** —
  `06_production_ai/notes/checkpoint-resume-in-exp2` with the proof it names: the
  machinery transported from exp1 (atomic save, RNG capture, rolling path per seed),
  the three falsification tests written first, and a real `Stop-Process -Force` drill
  whose resumed run is bit-identical to the uninterrupted one.
- **The execution transcripts** — one dated heartbeat log per lane (P=113 seeds 0–2,
  R1 standard): launch command, PID, checkpoint events, resume events, wall-clock
  estimate vs. actual; a dropped session or a failed resume is logged, never
  scrubbed — the bad-weather record is the record.
- **The verdict rows** — ADR-0003's seven rows stamped by Session 7, each
  `LAUNCHED (date, verdict)` or `CLOSED (date, one named reason)`; zero UNDECIDED at
  Session 8; the unchosen ADR-0006 candidates stay untouched on the shelf, exactly
  where the continuum law left them.
- **The paper's first prose** (`portfolio/paper/`) — the sections that open for
  manifests that exist on disk: the Rung-2 verdict section (either way), the Rung-1
  finding, the R4/R5 chain; `make paper` compiles in the CI mirror; the paper still
  rots loudly or not at all.
- **The essay annex** — `portfolio/essay-annex-1.md`, drafted from the consumed rows
  only after every number it cites has a manifest tag and a command; the essay itself
  is never rewritten, only amended (the MP-23/24/25/26 inheritance).
- **RESULTS** — the Rung-2 and Rung-5 rows gain their `<!-- manifest: ... -->` tags
  and their tables from the manifests; the trust order at the bottom is rewritten
  only by the data; `make verify-claims` at 0 is the proof, not the prose.
- **Skill tree** — flips only with a dated manifest or a stamped ledger row: grokking
  reproduction [~] → [x] (or the honest negative note), standard-scale R1 [~] → [x]
  (or its memo), R4/R5 chain decided with dates.
- **Progress log** — one dated entry per session; raw pass/fail before
  interpretation; a failed launch is logged as the note (the MP-12 lesson, still
  true, now load-bearing).
- **New notes (Obsidian, atomic, each linked ≥ 2 others)**: the exp2-port note, the
  CPU-first-execution note, the grokking-verdict note (either way), the
  standard-scale-head-or-no-head note, the one-new-manifest notes, one note per study.

## 3. Practical exercises and hands-on challenges

1. **The machine-budget audit (S0)**: read my own cores/RAM/headroom, derive the
   per-lane wall-time sheet from a real 100-epoch timing probe, and sign the
   overnight schedule with its kill conditions before anything launches.
2. **The exp2 checkpoint port (S1)**: port exp1's machinery into exp2 with the three
   falsification tests written FIRST (red), the port (green), the cleanup (refactor);
   the tests are the port's contract, not its decoration.
3. **The kill drill v2 (S1)**: launch a 200-epoch exp2 run, `Stop-Process -Force` at
   a random epoch, resume, and diff history + weights bit-for-bit against an
   uninterrupted run; the transcript is the proof artifact.
4. **The parallel overnight launch (S2)**: P=113 seeds 0/1/2 on separate cores, one
   supervised night, heartbeat log every wake-up, one deliberate kill + resume
   exercised for real before trusting the night to the machine.
5. **The R1 standard-scale launch (S2–S3)**: fresh-batches, `d_model=64`,
   `seq_len=64`, `vocab_size=2048`, `checkpoint-every-250`, its own supervised
   overnight; the resume path verified once before the night run.
6. **The pre-registered verdicts drill (S3)**: the Falsification column for every
   number the runs will produce — filled while the runs are still computing, then
   never edited; the only allowed post-launch edit is "observed".
7. **The Fourier analysis session (S4)**: frequency counts and progress measures from
   MY log; the "grokked = sparse frequencies" criterion applied mechanically, not by
   eye; the Varma interpretation written from the curve, not from the paper's curves.
8. **The scheduled-negative drafting (S3/S5)**: the no-grok paragraph and the no-head
   memo written in full before the finals — then kept or struck, never rewritten from
   mood; the negative ships with the same polish as the win.
9. **The re-derivation walk (S6)**: every headline number on the phase's verdict
   sheets → command → manifest → figure, walked as a checklist; `verify-claims` at 0
   is the exit gate, and the walk proves it.
10. **Habit — the clock check (every session)**: the ledger's undated rows, the long
    runs' heartbeats, the CI status line — all three before any new prose.

## 4. Strategic tips and architectural best practices

- **Own the clock: CPU-first.** A 24/7 local CPU with tested resume machinery beats a
  fragile free-tier GPU every time; the GPU becomes an accelerator to win, never a
  dependency to wait on. "Needs a GPU" cost this record seven phases of latency — the
  record's own probe runs and kill drill were the counter-evidence all along.
- **Checkpointing is a first-class feature, not a utility.** exp1's machinery was
  earned by a kill drill; it ports with its tests or it does not port. A promise of
  resume without a tested resume is a mood — ADR-0003's row 1 silently made that
  promise, and this phase's Session 1 is the mechanical repayment.
- **Launch at the start, analyze at the end.** The launch reflex is the record's
  original disease: sessions 1–3 exist so that sessions 4–7 have data. An undated
  launch is a failed session; a session's exit gate is the ledger row, not the prose.
- **Parallel seeds = owned nights.** P=113 × 3 seeds on separate cores turns 16.5 h
  into ~6 h of wall time; small experiments are embarrassingly parallel, and the
  machines you own are the truest scheduler. The audit decides the concurrency; the
  audit is Step 0 because the launch is Step 2.
- **Pre-register verdicts, then freeze them.** Thresholds, budgets, and falsification
  columns written before launch, never edited after; the only allowed post-hoc edit
  is "observed" (Gelman & Loken at the source, always — inherited, now executed).
- **The negative is the contribution.** Both flagship lanes may close negative; the
  record's public signature is the polished "not reproduced — here is the date and
  the reason". The negatives are drafted first so the closure is never a silence.
- **One measured line per phase.** This phase's line is `verify-claims` 2 → 0: one
  number, on disk, verifiable by a stranger. The paper's prose, the essay annex and
  the future site all wait on exactly that line, so the line is the phase's spine.
- **The stack must move; the shelf is a consequence.** Publication surfaces open only
  for manifests the science produces; until then ADR-0002's rows stay UNDECIDED by
  design, and the scaffold stays a scaffold because honesty is the build.
- **Mypy ratchet and CI upkeep are bounded chores.** At most one module this phase,
  never while a launch or a revision is pending (inherited, still true).
- **Session clocks beat mood clocks** (inherited, still true): every step has a wall
  clock and an exit gate — this phase more than any other, because it is the one
  that finally runs.

<!-- MP27-SECTION-3 -->

## 5. Step-by-step execution roadmap

```
WEEK 1

SESSION 0 — THE PRE-FLIGHT (~1 h)
  Hard gate: the machine-budget audit written live — cores, RAM,
  headroom and the overnight window priced from a real 100-epoch
  timing probe; the four-phase stack's undated rows listed row by
  row; the CI floor re-verified locally (the tracked 185, ruff,
  blocking mypy, markdownlint, `verify-claims` = 2). ADR-0003's
  protocol re-confirmed as frozen — nothing re-planned, nothing
  re-negotiated; the exp2 port decision taken and recorded (the
  decision MP-26's review named). The terminus is declared:
  release = this merge + 14 calendar days. This roadmap wired into
  home; pushed to dev; a green GitHub floor.
  Exit: the audit sheet and the schedule sheet are signed; zero
  launches happen before this sitting.

SESSION 1 — THE EXP2 PORT (~3 h)
  The checkpoint/resume machinery transported from exp1 to exp2 with
  the three falsification tests written FIRST (resume ==
  uninterrupted; resume twice == uninterrupted; missing checkpoint
  starts fresh); the kill drill v2 executed for real on exp2; the
  resume-protocol memo lands (cadence 500, heartbeat format,
  deliberate-kill rehearsal) with the PyTorch-serialization reading.
  Exit: exp2 resume is bit-identical; the drill transcript is
  committed; the port note is written.

SESSION 2 — THE GROKKING OVERNIGHT (~2 h + supervised night)
  P=113 seeds 0/1/2 launched in parallel on separate cores per the
  audit, with `checkpoint-every-500`; the heartbeat log opened; the
  run-record cheat sheet beside the terminals; one deliberate kill +
  resume exercised before the night. The Colab canary stays OPTIONAL:
  a nice-to-have accelerator, never the load-bearing path.
  Exit: three launches live with dates; the kill-condition sheet is
  signed; resume proven once in the live lane.

SESSION 3 — THE R1 OVERNIGHT + THE NEGATIVES PRE-FILLED (~2 h +
  supervised night)
  R1 standard-scale fresh-batches launched with `checkpoint-every-250`
  and its resume path verified once; while it runs: the Falsification
  columns and the two scheduled negatives drafted in full; the
  grokking night's heartbeats walked; the first Fourier pass read as
  data, not as mood.
  Exit: R1 live with a date; both negatives drafted; both lanes have
  survived at least one resume.

WEEK 2

SESSION 4 — THE GROKKING ANALYSIS (~3 h)
  P=113's verdict written from the manifests: Fourier frequency
  counts, progress measures, the generalization epoch (or its honest
  absence), the named suspects answered (embedding re-normalization,
  cosine schedule — each turned into a one-change reading of the
  record); the Nanda and Varma interpretations written from MY log.
  Exit: ADR-0003 row 1 stamped LAUNCHED-with-verdict or
  CLOSED-with-one-reason; every annex-bound number manifest-tagged.

SESSION 5 — THE R1 VERDICT + THE R4 CHAIN (~3 h)
  The standard run's verdict from its manifest: head or no-head,
  named with dates. If head: path patching + head ablation against
  the real head, Zhang & Nanda's checklist applied before the press.
  If no-head: the memo in full, printed as the contribution; the R4
  row closes with its reason in the same sitting.
  Exit: ADR-0003 row 3 stamped; the R4 chain row decided — both with
  dates, either way.

SESSION 6 — THE R5 RE-RUN + VERIFY-CLAIMS 2 → 0 (~3 h)
  The SAE re-test against the phase's best checkpoint (real head if
  one exists, best-available otherwise); the sparsity/FVE verdict
  memo; `results/exp2_grokking.json` and
  `results/exp5_sae_dashboard.json` verified on disk; `make
  verify-claims` at 0; the re-derivation walk end to end; RESULTS
  rows and skill-tree flips stamped with dates.
  Exit: verify-claims = 0; the R5 row LAUNCHED or CLOSED with a date;
  every headline number re-derivable from a walked command.

SESSION 7 — THE PAPER'S FIRST PROSE (~3 h)
  The sections that have manifests, written from disk: the Rung-2
  verdict, the Rung-1 finding, the R4/R5 chain; `make paper` compiles
  in the CI mirror; the essay annex-1 drafted with every number
  manifest-tagged; mypy drift at most one module if the budget
  allows.
  Exit: the paper's first prose lands; the annex cites only disk.

SESSION 8 — THE RELEASE (the fixed terminus date)
  Merge on green; ADR-0003's rows all stamped; home wired; this
  roadmap archived with its deviations — every deviation a dated
  ledger note. ADR-0006's candidate set re-verified untouched on the
  shelf, exactly as the continuum law left it.
  Exit: tree clean, `dev == main`, `verify-claims` = 0, the stack has
  moved, and the four-phase stack is now three ledgers with dates and
  one science that ran.
```

## 6. Gate criteria

1. Session 0: the machine-budget audit and the schedule sheet signed and committed;
   the CI floor green locally AND on GitHub; ADR-0003's protocol re-confirmed frozen;
   the exp2 port decision recorded.
2. Session 1: exp2's three falsification tests green, including the kill-drill v2
   bit-identical result; the drill transcript and the port note committed.
3. Sessions 2–3: both lanes live with dated rows and heartbeats; a real resume has
   happened in each lane; the scheduled negatives are drafted before the finals.
4. Session 4: ADR-0003 row 1 stamped LAUNCHED-with-verdict or CLOSED-with-one-reason;
   every annex-bound number manifest-tagged.
5. Session 5: the R1 row and the R4-chain row both stamped with dates, either way;
   the no-head memo printed as a contribution if it came.
6. Session 6: `make verify-claims` at 0 — the phase's one measured line, on disk;
   the R5 row LAUNCHED or CLOSED with a date; the re-derivation walk complete.
7. Session 7: paper sections cite only manifests; `make paper` compiles in the mirror;
   the annex cites only disk.
8. Session 8: the merge is green; ADR-0003's rows are all stamped; ADR-0006's
   candidate set untouched — zero new research questions opened this phase.
9. The record-sanity gate: nothing on any public surface exceeds the record — every
   sentence survives `verify-claims` or is struck with a date (inherited, now
   enforceable because the manifests exist).

## 7. Showcase note (for the portfolio reader)

Four roadmaps had been pre-registered in a row while the science that gates them all
sat unexecuted — my own ledger's deepest pattern, momentarily inverted. This phase is
where the stack stopped stacking: I ported the resume machinery that made long runs
survivable into the experiment that owed them, launched both flagship lanes on my own
machine's overnight budget under their own frozen protocols, drafted the negatives
before the runs finished, analyzed whatever the data decided, and moved
`verify-claims` from its designed 2 problems to 0. The paper's first prose is now
written strictly from disk, the essay annex cites only manifests, and the program's
next research question stayed frozen until the record's oldest promises carried
dates. A stranger can now watch the discipline compound in its intended order:
execute first, question later, dates always.

> "The phase where the promises finally became rows: two flagships launched under
> their own clocks, verdicts dated either way, and the record's oldest debt — the run
> that would not start — quietly became the run that would not stop."

## Links

- [[docs/adr/0003-research-return-ledger]] — the intake this phase executes: the
  seven rows whose protocols were frozen before this roadmap existed.
- [[00_meta/22_micro-phase-23-the-research-return]] — the current phase whose
  sessions this phase's clock runs under; its Session 0 decisions are this intake.
- [[docs/adr/0004-horizon-ledger]] · [[docs/adr/0005-premiere-ledger]] ·
  [[docs/adr/0006-continuum-ledger]] — frozen by design: their gates are the verdicts
  this phase produces, and MP-27 touches none of their rows.
- [[00_meta/25_micro-phase-26-the-continuation]] — the roadmap whose intake review
  recorded the exp2 gap this phase's Session 1 closes.
- [[portfolio/RESULTS]] · [[portfolio/essay-annex-1]] · [[portfolio/paper/main]] —
  the artifacts this phase's manifests unblock.
- [[06_production_ai/proofs/kill-drill-checkpoint-resume]] — the machinery the exp2
  port inherits, and the drill the port's proof must repeat.
