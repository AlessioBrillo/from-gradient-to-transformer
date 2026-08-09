---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-09
---

# Micro-Phase 23 — The Research Return: the flagships stop being pre-registered

Written as a personal learning log and a public record, like every roadmap before it.

Nine roadmaps since MP-14 pre-registered the same two scientific lanes — the
induction-heads standard run and the P=113 grokking launch — and none of them
launched anything. The progress log named the disease before this phase existed:
"Five consecutive phases pre-registered the same two flagship verdicts; the
bottleneck is launch discipline, and the treatment has to be mechanical, not
rhetorical." MP-18 built the clocked-window treatment, MP-20 added the kill-date
terminator, MP-21 and MP-22 proved the ledger discipline on the release and the
publication. This phase is where the scientific record itself absorbs the lesson:
the two flagship lanes OPEN as ledger rows with launch windows, checkpoint
cadence, heartbeats and kill-dates — and whatever the data says, each row ends
in a dated verdict, never in a promise.

The record this phase works on has a verified spine (Rung 3's superposition
phase transition and pentagon geometry, Rung 5's synthetic baseline), an honest
set of open questions (Rung 2 grokking never reproduced, Rung 1 no head seen
above quick scale, Rung 4's path patching validated only by unit tests because
no real head has ever existed to point it at) and, as of MP-22's release, an
address — the essay, the thread, the site, the demo. This phase does not
re-plan the publication and does not rewrite the essay: it runs the two
experiments the essay honestly names as unverified, and whatever happens, the
public record absorbs the outcome through a dated annex — never a silent edit.

## Design decisions

- **The starting artifact is MP-22's release state, row by row.** Step 0 is a
  truthing pass over the public-arc ledger and the essay's claims — the same
  discipline MP-21 applied to MP-20's release, applied to the public record.
  Nothing in this roadmap re-plans the public arc; it consumes its verdicts.
- **Research lanes reopen as NEW rows in a new ledger (ADR-0003), never as
  revisions of the old ones.** The MP-18..21 verdict ledger's rows carry their
  dates and reasons; this phase's rows are new decisions with new dates, under
  the same two-state rule (LAUNCHED-with-date or CLOSED-with-one-reason).
- **GPU work happens only under the Colab handshake.** A minutes-scale canary
  run of the exact pinned notebook cells on the exact free-tier runtime
  precedes every long launch; the checkpoint/resume mechanism that passed the
  MP-12 kill drill (bit-identical resume across a real process kill) is the
  resume path when Colab disconnects mid-run.
- **Pre-registered verdicts are frozen before the first launch.** The
  thresholds, the seeds, the budgets, the generalization epoch bound and the
  "what would falsify this" column are written into ADR-0003's ledger tables in
  the phase's Session 0 and never edited again — the garden-of-forking-paths
  countermeasure (Gelman & Loken) applied at the source, not at the report.
- **R4 and R5 chain off R1's verdict — with a scheduled negative as the
  default fallback.** Path-patching validation and the real-activation SAE
  re-test open only if a real induction head exists; if the head never comes,
  the "no head at standard scale" result is the paper's honest Rung-1/4 line.
- **The essay is never rewritten; it is amended.** New verified findings land
  in a dated annex (`portfolio/essay-annex-1.md` visible from the essay), and
  the public-arc ledger records the supersession as a NEW row — the record
  stays the artifact a stranger can audit.
- **The terminus is stamped at Step 0**: release = this roadmap's merge + 14
  calendar days. On that date the phase ships everything the rows decided —
  the residue is a dated list, never a silence.

## Where this phase starts (state review, verified against the repo 2026-08-09)

I checked the tree, the manifests, the ledger rows, the CI floor and the gate
states before writing a single claim here.

- **Tree state**: `dev` and `main` tree-identical after MP-22's Step-0 squash;
  working tree clean; no open PRs.
- **The CI floor, re-verified in this session**: **185 tests passing**, ruff
  clean on `src/ tests/`, blocking mypy clean (`src/results.py`,
  `src/experiments/runner.py`), full-tree mypy at its tracked **171** (exit 1,
  the non-blocking ratchet), `make verify-claims` at exactly its designed **2
  problems** — Rung 2 and Rung 5 manifestless by design — markdownlint 0 issues
  on the changed notes.
- **The public arc (MP-22) is pre-registered, not executed**: its rows (essay,
  thread, site, Space, walkthrough) sit in ADR-0002 UNDECIDED until its own
  session 1. This phase consumes whatever its report says; the research lanes
  here are orthogonal to it by design: they can run even if publication rows
  close, and they feed the annex when they land.
- **The scientific ledger (ADR-0001) is fully stamped by MP-21/22's release**:
  every verdict row is LAUNCHED or CLOSED with a date. The two rows this phase
  reopens — the P=113 grokking lane and the induction standard lane — come
  back as NEW rows carrying this phase's windows.
- **Manifest debt, quantified**: `results/exp_2_grokking.json` has never
  existed; `results/exp5_sae_dashboard.json` has never existed. Rung 3 and
  Rung 1's quick manifests are on disk and cited. Closing this debt is a
  measurable CI line this phase owns: `make verify-claims` goes from its
  designed 2 problems to 0.
- **The two named suspects if P=113 fails**: the embedding re-normalization
  and the cosine schedule — the notebook's own comments name them; this
  phase's fallback lane stops trusting them and turns each into a one-change
  trial with its own negative control.
- **The R1 standard-scale gap has not moved since MP-10**: the fixed-vs-fresh
  comparison (52.2% val acc vs 0.05%, matched 800-epoch) was the last
  trustworthy number; standard-scale fresh batches (d_model=64, seq_len=64,
  vocab 2048, ~17–20 h CPU) has never run. That is the domino for R4 and R5.

### Bottleneck analysis (ranked by what blocks what)

1. **The launch reflex — the first bottleneck to break.** The whole phase
   hangs off Session 1: the two launches have to be *running* before anything
   else can be analyzed. The treatment is the ledger's undated-rows gate: the
   session ends when the launches are live with dates, not when the roadmap is
   written. No prose survives the session if a row is still undated.
2. **Colab's session fragility.** A free-tier run can die at any moment: the
   handshake canary and checkpoint-every-500 + resume policy are what make the
   P=113 lane *executable* rather than aspirational. Without the resume path a
   disconnected 3-seed run becomes a two-week redo — the recorded failure mode
   of the MP-9 era.
3. **The R1→R4→R5 dependency chain.** Path patching remains unit-test-validated,
   the real-activation SAE result (99.97% FVE at 53% L0) remains a no-head
   checkpoint artifact. Everything downstream of a nonexistent head is a
   delayed verdict, so the phase inscribes the negative path into the ledger
   with the same weight as the positive one.
4. **Manifest debt (the measurable CI line).** The two missing manifests are
   the only reason `verify-claims` reports its designed 2 problems; each rung
   that lands a manifest changes the gate baseline — and the essay's annex
   cannot cite data with no manifest.
5. **The mypy ratchet (171)** — scheduled, non-blocking, at most one module in
   this phase; it must never be chased while a launch is pending.

## 1. Deep-dive study and research topics (bound to a session — no topic without a deliverable)

| Topic | Session | The deliverable that proves the reading |
|---|---|---|
| Nanda et al., *Progress Measures for Grokking* (ICLR 2023) — the Fourier recipe: frequency counts, the "grokked solution = sparse frequency" criterion, the distance-to-solution / period measures | S1 | The progress-measures section of the paper written against the exact functions the run's log records, before the log is read |
| Power et al., *Grokking: Generalization Beyond Overfitting* (2022) — the canonical setup, weight decay, the small-math differences in norms | S1 | The run-record cheat sheet: one page beside the supervised launch — config, suspects, windows, kill conditions |
| Olsson et al., *In-context Learning and Induction Heads* (2022) — induction-head protocol as commonly defined, fresh-batches rationale | S1 | My written definition of "head formed" (diag+1 mass > 0.3 on ≥ 1 head, sustained ≥ 5 checkpoints) — fixed before the run, not after |
| Varma et al., *Explaining Grokking through Circuit Efficiency* (2023) | S2 | One paragraph interpreting whatever the curve does — the "why now / why never" sentence the paper will carry |
| Gelman & Loken, "The Garden of Forking Paths" (2013) — re-read | S2 | The "what would falsify this" column for every new number I am about to report, filled before the number exists |
| Zhang & Nanda, "Towards Best Practices of Activation Patching" (ICLR 2024) | S4 | The patching session's checklist: site choice, logit-diff definition, the before-the-press sanity table |
| Bricken et al., *Towards Monosemanticity* (2023) + Cunningham et al. (ICLR 2024) — re-read | S5 | The SAE real-checkpoint result table annotated with the expected sparsity/FVE trade-off — honest reading before the run |
| The MP-12 kill drill transcript (bit-identical resume) | S1 | The Colab-resume protocol written from it: checkpoint cadence, resume verification, heartbeat log format |
| The essay's own claims audit table (MP-22 S1) | S6 | The annex's evidence sheet: every annex number carrying its manifest tag and command |

Each reading produces a deliverable — the vault's rule: no topic without an artifact.

## 2. Documentation requirements

- **The research-return ledger (ADR-0003)** — *new*: one row per research lane
  (grokking P=113, fallback microscope, R1 standard, R4-on-head, R5 re-run,
  paper section, graduation proof), each with launch window, heartbeat, and
  kill-date, under the ADR-0001 rules; closed-then-reopened rows are new rows.
- **The frozen protocol**: the pre-registered numbers (seeds, epochs, budget,
  thresholds, success criteria, falsification column) written into the ADR in
  Session 0 and never edited.
- **The essay annex** (`portfolio/essay-annex-1.md`, drafted S6): five numbered
  additions — (1) the R2 verdict whichever way, (2) the R1 finding, (3) the R4
  validation or its negative, (4) the R5 re-run or its negative, (5) the
  verify-claims 2 → 0 line. Every claim file-cited.
- **RESULTS.md**: Rung 2 and Rung 5 tables updated to dated verdicts with
  manifest tags; the summary table's trust-order re-written if warranted.
- **Progress log**: one dated entry per session; raw pass/fail before
  interpretation; a launch row is logged even if it fails — the failure is the
  note.
- **New notes (Obsidian, atomic, each linked ≥ 2 others)**: the grokking
  progress-measures note (S1/S3), the induction-head-formation note (S1/S5),
  the patching-on-a-real-head note (S4), the SAE-on-confirmed-features note
  (S5).
- **Skill tree**: flips only with a dated manifest behind them: grokking [~]
  → [x] or stays [~] with the reason cited; SAE [~] likewise; the new
  publication rows (annex) end LAUNCHED or CLOSED with dates.
- **The graduation proof row**: `07_capstone/`'s proof-to-myself ("explain the
  Fourier algorithm, show the model's actual progress, demonstrate the causal
  ablation") — either assembled from the real run or closed with its dated
  reason, never absent.

## 3. Practical exercises and hands-on challenges

1. **The truthing pass (S0)**: read the current state row-by-row — public-arc
   ledger, manifests, CI floor — and write the one-page scope: what the essay
   can claim today. Exit: zero unsupported claims in the scope sheet.
2. **The Colab handshake (S1)**: under-five-minute canary of the pinned
   notebook's exact cells on the free tier; the run passes the canary or the
   notebook is fixed before any P=113 hour is burned.
3. **The three-seed stampede (S1)**: P=113 × 3 with pre-committed seeds,
   weight-decay and cosine knobs as frozen; heartbeat log; tick. Exit: all
   three lanes live, resume path proven on the first Colab disconnect.
4. **The supervised standard-scale R1 (S1/S2)**: the 17–24 h fresh-batches
   run with heartbeat and every-500 checkpoints; the machine is left alone
   exactly as a supervised run should be — logs, no micromanagement.
5. **The one-change microscope (S3, only if P=113 misses)**: the two named
   suspects (embedding re-normalization, cosine schedule) plus one hypothesis
   of mine = ≤ 3 single-variable trials, each with a negative control and a
   canary; after the third trial the row closes with its reason.
6. **The progress-measures sitting (S2/S3, whichever way)**: decompose the
   run's own log — frequency counts, S1/S2 gap, spike behavior — and compare
   against Nanda's published curves *before* touching any ablation.
7. **The Fourier ablation (S4, if grokked)**: zero the top-K frequencies and
   watch val accuracy collapse; the ablation curve is the causal proof of the
   trigonometric algorithm.
8. **Patching's first press on a real head (S5, if the head exists)**: the R4
   matrix — path patching + activation patching on 2–3 heads, with the
   self-patch-is-zero and corrupt-run-moves-the-diff tests re-run against the
   real head.
9. **The SAE re-run reprise (S5/6)**: real activations from the new
   confirmed-head checkpoint — L0 vs FVE trade-off against the 53%-L0 no-head
   baseline; the honest delta, whichever way.
10. **The adversarial-reader pass (S7)**: paper's grokking/induction sections
    read as three hostile reviewers; five attack sentences per section fixed
    before release.
11. **The clean-clone closure (S7)**: fresh clone → `uv sync` → full suite →
    `make verify-claims` (2 → 0) → annex + paper build — one transcript.
12. **Habit — the clock check (every session)**: the ledger's undated rows,
    the open PR's CI status line, the essay's annex status — all three before
    any new prose.

## 4. Strategic tips and architectural best practices

- **A row with a launch clock is science; a row without one is hope.** Every
  > 1 h run attaches to a session with a window, a heartbeat and a resume path
  before it starts.
- **The handshake precedes the flight, always.** A free-tier Colab runtime is
  a fresh machine every time; the five-minute canary is cheaper than one
  mid-run surprise.
- **Pre-register, then never move the line.** Thresholds, seeds, budgets and
  the falsification column live in ADR-0003 from Session 0; after the first
  launch the only allowed edit is "observed".
- **One variable per bullet.** Post-failure hypotheses are separate
  single-variable mini-runs, each with a negative control — never a
  three-knob "let's see".
- **Manifests are the only currency.** Prose is the narrative; `json` is the
  receipt. No number enters the essay or the paper without a command that
  reproduces it (`verify-claims` 2 → 0 is the phase's measurable gate).
- **Design the negative as a deliverable.** The no-head-at-standard-scale
  result and the no-grok-at-P=113 result are contribution claims with
  pre-registered protocols; publishing them is a win, deferring them is the
  loss.
- **The annex beats the rewrite.** Public record mutates only through dated
  annexes; a review observes the record over time, never through a silent retroactive edit.
- **Session clocks beat mood clocks** (inherited, still true): every step has
  a wall clock and an exit gate.
- **The record's honest spine is what the phase feeds** (inherited): every
  number in the essay's annex must be re-derivable from command + manifest, or
  it is struck with a reason — not softened.

## 5. Step-by-step execution roadmap

```
WEEK 1

SESSION 0 — the pre-flight (~15–30 min)
  CI green locally AND on GitHub (185 tests, ruff, blocking mypy,
  markdownlint); the research-ready ledger (ADR-0003) opened with its rows and
  windows; the frozen protocol written into it; this roadmap wired into
  home; pushed to dev; a green GitHub floor. Exit: the terminus is declared
  (release = this merge + 14 calendar days).

SESSION 1 — THE HAND SHAKES (the phase's Step 1, ~2 h)
  Read MP-22's report row-by-row; write the one-page scope. The Colab
  handshake passes. The three-seed P=113 stampede launches with its
  heartbeat; the R1 standard fresh-batches launch is scheduled (S1 evening,
  ~17–20 h). Exit: both rows LAUNCHED with dates — the session is not over
  while a row is undated.

SESSION 2 — THE RESUME CHECK (~2 h)
  First overnight checkpoint verified via the resume path; the study slots
  bound to it (Power, Olsson) produce their cheat sheets; heartbeat logged.
  Exit: each run's first checkpoint exists and resume is proven.

SESSION 3 — THE WAITING HOUR THAT EARNED ITS KEEP (~3 h)
  The P=113 lane resolves (grok / fail): if grok — the progress-measures
  reading and the frequency-count pencil the paper's section; if fail — the
  one-change microscope runs its ≤ 3 trials with negative controls. The R1
  lane at ≥ 50% despite heartbeat. Exit: the P=113 row is (LAUNCHED,
  continued) or (CLOSED, one reason).

WEEK 2

SESSION 4 — THE VERDICT WINDOW 1 (~3–4 h)
  R2's row concludes: grok → the Fourier ablation runs and its curve lands
  in the paper draft; fail → the honest section is written from the frozen
  protocol. R1 concludes: head/no head-and-why, from the run's own metrics.
  Exit: both verdict lines exist in the ledger with dates.

SESSION 5 — THE CHAIN OPEN OR ITS NEGATIVE (~3 h)
  With a head: the patching matrix on 2–3 real heads (self-patch = zero,
  corrupt = diff) and the SAE re-run on the real checkpoint. Without a head:
  the scheduled negative is written as the R4/R5 result. Paper's grokking
  and induction sections in prose; skill-tree rows flipped or dated. Exit:
  an honest R4/R5 row (LAUNCHED-with-verdict or CLOSED-with-reason).

SESSION 6 — THE ASSEMBLY (~2–3 h)
  R2/R3-style progress: the graduation proof assembled from the real run
  (or closed with its reason); the essay annex v1.1 drafted and cited;
  `verify-claims` runs at 0; RESULTS and the model card reconciled.
  Exit: annex + paper numbers all carry manifest tags.

SESSION 7 — THE ADVERSARIAL PASS + THE REHEARSAL (~3 h)
  Attack pass on the paper's new sections and the annex; the clean-clone
  closure transcript from a bare checkout; the ledger read row-by-row with
  zero undated rows; mypy drift (at most one module) if the budget allows.
  Exit: the release rehearsal on a branch — the landing plan has been walked.

SESSION 8 — THE RELEASE (the fixed terminus date)
  Merge on green; the essay-annex amendment lands with its date; the public
  rows LAUNCHED or CLOSED under dates; home wired; this roadmap archived
  with its deviations — every deviation a dated ledger note. Exit: tree
  clean, `dev == main`, the ledger is the phase's after-the-fact truth.
```

## 6. Gate criteria

1. Session 0: the CI floor is green locally AND on GitHub — before the phase
   evicts a single step; the protocol is frozen in the ledger.
2. Session 1: the P=113 run and the R1 run are LAUNCHED with dates after a
   passed Colab handshake — zero undated rows at session end.
3. Session 4: the R2 and R1 rows end with verdicts — LAUNCHED-with-result or
   CLOSED-with-one-reason; no run leaves the window in "unsure".
4. Session 5: the R4/R5 rows are dated — either the real-head validation or
   the scheduled negative, both artifact-backed.
5. Session 7: `make verify-claims` reports zero unexpected problems; the
   ledger shows zero undated rows; the rehearsal transcript exists.
6. Session 8: the merge is green; the annex is live with numbers re-derivable
   from disk; the progress log closes the loop.
7. The record-sanity gate: nothing in the essay's annex exceeds the record —
   every public sentence is verified on disk or struck with a date.

## 7. Showcase note (for the portfolio reader)

The project's deepest lesson is the one this phase enacts: a promise can be
re-planned forever, but a dated row is answered. The scientific record ends
with the essay's two open lanes — Rung 2 and Rung 1 — resolved exactly one
way or the other, entry by entry, with manifests on the shelf and the negative
results printed as contributions, not as confessions:

> "The phase that answered rather than planned. Rung 2 and Rung 1 ran their
> clocks, the chain followed the head, and the annex told the stranger exactly
> what the record now claims — because every claim had a file."

## Links

- [[00_meta/21_micro-phase-22-the-public-arc]] — the roadmap this phase
  consumes; its report and public-arc rows are Step 0's starting artifact.
- [[docs/adr/0003-research-return-ledger]] — this phase's ledger: the new
  rows, windows and frozen protocols.
- [[docs/adr/0001-verdict-closure-ledger]] · [[docs/adr/0002-public-arc-ledger]] —
  the two ledger machines this phase's rows inherit and amend.
- [[portfolio/RESULTS]] · [[portfolio/README]] — the results sheet the new
  rows update; the shelf the annex lands on.
- [[00_meta/03-progress-log]] — the dated record of every session, including
  the rows that closed.