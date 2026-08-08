---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-08
---

# Micro-Phase 20 — The Execution Arc: Dated Verdicts, Real Instruments, the Paper's First Draft

Written as a personal learning log and a public record, like every roadmap before it.
Micro-Phase 19 defined the four verdict-agnostic deliverables — the paper draft v0.1, the
reconciled release, an honest Rung 6, the two missing instruments — and bound them to
sessions. Its Step 0 is shipped; this phase executes the rest. I add no new promises: I
add the two terms the ledger [[docs/adr/0001-verdict-closure-ledger]] was missing to
ever terminate — a **release date** fixed first, and a **kill-date** stamped on every row
that opens. After five micro-phases that pre-registered the same two launches, the lesson
is formal: a deferral written without a date is instinct; a deferral with a window and a
kill-date is a decision.

## Design decisions

- **The phase ships on a date, not on a verdict.** The terminal date is fixed at Step 0:
  fourteen calendar days after this roadmap merges to `main`. Everything below schedules
  backward from it. On that date the release happens — whichever lanes fired, including
  the lane that fired never again.
- **A row opened without a kill-date is a lie in the ledger's own terms.** Every entry
  that enters `LAUNCHED` in Session 1 carries one named window and one named kill
  condition (the observable that ends the row before the window does). When the condition
  fires, the row transitions to `CLOSED (date, named reason)` in the same sitting that
  observes it. "Kill-date" is the term the two legal states were missing: *terminate*.
- **Consume, don't re-plan.** MP-19's Sessions 0–9 remain the execution vehicle; this
  phase's calendar is that calendar with budgets, kill-conditions and one final date.
- **The pre-outcome commitment stands.** The "evidence that would change my belief, by
  which date" paragraph is written in Session 1, before any verdict exists, and
  re-read at Session 8. No post-hoc leniency: a verdict is scored against the paragraph,
  not against my mood on the day.

## Where this phase starts (state review, verified against the repo)

I checked `git status`, the manifests, the CI floor and the ledger before writing a single
claim here.

- **MP-19 Step 0 is shipped**: the roadmap [[18_micro-phase-19-verdicts-to-publication]]
  is in history, wired into [[00_meta/00_home]], merged to `main` (`dev == main` locally).
  The two `ci(ci)` commits on top (the audit of the commitlint pardon) leave the
  conventional-commit rule intact for every message except the two exact ones.
- **The CI floor, re-verified this session**: **185 tests passing** (76 s), ruff clean on
  `src/ tests/`, blocking mypy clean (`src/results.py`, `src/experiments/runner.py`),
  full-tree mypy at its tracked 171 (exit 1, the non-blocking ratchet), `make
  verify-claims` at exactly its designed 2 problems (Rung 2 and Rung 5 manifestless by
  design — the gate working as designed). markdownlint stays part of push CI and is
  clean.
- **The strongest verified result stands and needs no verdict**: Rung 3's superposition
  phase transition (10/20 → 20/20 features as sparsity drops 0.5 → 0.01; pentagon
  geometry 70.2–73.8° gaps, std ≤ 1.4° vs the ideal 72°) with its committed multi-seed
  manifest and curated figures in `portfolio/figures/`.
- **The committed fallback stands**: the K-composition detector (`k_composition_scores`
  → `plot_composition_diagnostic` in `exp1_induction_heads.py`) turns a headless R1
  verdict into a figure, not a hole.
- **The ledger is still materially empty**: all ten rows in ADR-0001 remain UNDECIDED —
  this is the fifth consecutive phase where "fill the rows" is the honest headline of the
  critical path. Session 1 is the overdue first act.
- **The paper is still a scaffold**: every section of `portfolio/paper/main.tex` is a
  `% TODO`, while four sections are writable today from committed evidence. Clocked
  writing sessions are the only cure that has never been tried in six phases.
- **The instrument set ends short in exactly two places**: attribution patching is the
  one technique named in the model card ("attribution patching can mislead") with no
  implementation to falsify it; and the SAE has never been validated against a circuit
  whose ground truth is known — Rung 5's real-activation numbers are honest but need a
  head-bearing checkpoint to mean more than a density bound.
- **Rung 6 is a hole where a contribution belongs**: the deleted placeholder (fabricated
  ACDC numbers, removed 2026-08-01) leaves the automated-vs-manual question
  unanswered; a real ACDC run is the highest-value new computation this phase can ship
  in any lane.
- **The clean-clone gate has never run once** — one transcript from a formality, and a
  hard gate the release and the model card both depend on.

### Bottleneck analysis (ranked by what blocks what)

1. **The closure decision — the critical path of the critical path.** The ledger is the
   mechanism and Session 1 is the sitting; what the ledger has lacked is the causal
   *term*: a terminal date that ends deferral, and a kill-date per row that ends
   ambiguity. This phase's Step 1 stamps both. Not a re-plan — the missing verb.
2. **The launch windows themselves** — R1 `--standard` (~17–20 h supervised CPU) and
   P=113 (one named GPU window, or a bounded CPU lane). They schedule under the wall
   clock: S2–S6 are compute-light and file-based, so nothing waits on them except the
   verdicts themselves.
3. **The paper's prose** — the only cure never tried for six phases: seated writing
   sessions with a per-paragraph file-citation rule.
4. **Rung 6** — the honest successor to the placeholder, automatable in one session and
   valuable in every verdict lane.
5. **The mypy ratchet (171)** — scheduled, not blocking: three short sittings, one
   module per sitting, exactly one moved onto the blocking allowlist with its
   errors-at-move count.
6. **The clean-clone gate** — one dry run, zero manual steps, full transcript; the
   Phase-6 gate proof [[06_production_ai/proofs/reproducible-from-clean-clone]] finally
   going green.

## 1. Deep-dive study and research topics (bound to a session — no topic without a deliverable)

| Topic | Session | The deliverable that proves the reading |
|---|---|---|
| Conmy et al., "Towards Automated Circuit Discovery for Mechanistic Interpretability" (ICLR 2023) | S4 | Rung 6 returns: a real ACDC run on the repeated-token task; automated-vs-manual recovery per edge; faithfulness per omitted edge; one written sentence where the two differ. The placeholder's honest successor |
| Nanda et al., "Attribution Patching: Activation Patching at Industrial Scale" (2023) | S3 | `attribution_patching` implemented in `src/`, wired into `exp4`, with falsification tests (self-patch = exact no-op; single-position = activation patch on a textbook case); the note [[04_nlp_and_transformers/notes/attribution-patching]] (new, S3) |
| Zhang & Nanda, "Best Practices of Activation Patching" (ICLR 2024) — read second, after the instrument exists | S4 | The per-site audit table mapped onto `exp4`, now with attribution-vs-path comparisons; feeds paper Methods |
| Nanda et al., "Progress Measures for Grokking" (ICLR 2023) — re-read with a checkpoint (or a closure) in hand | S5/S6 | The Freq^k sparsity hand-verification protocol; if 6c (grokked): the figures; if 6d (closed): the named-suspect analysis table |
| Bricken et al., "Towards Monosemanticity" (2023) + Cunningham et al. (ICLR 2024) | S5 | The SAE-on-known-circuit sanity check: features should align with the ground-truth directions where the circuit is known; where they don't, that is a finding — not a bug |
| Elhage et al., "Toy Models of Superposition" (2022) | S5 | Cross-check the SAE sanity against the pentagon geometry — the two puzzles must agree |
| Olsson et al., "In-Context Learning and Induction Heads" (2022) | S6 | The interpolation commentary for the K-composition "how far" figure, in either lane |
| Pineau et al., "Improving Reproducibility in ML Research" (JMLR 2021) | S6 | The claims audit applied to three headline numbers, written into the paper's Methods as the reproducibility statement |
| Power et al., "Grokking: Generalization Beyond Overfitting" (2022) | S5 | The one-variable retry dials (weight decay / LR / P) pre-set on paper before the budget exists |

The MP-17/MP-18/MP-19 reading lists are inherited wholesale on top of this — my study
calendar is the same calendar, with this phase's S3–S6 slots bound to instruments.

## 2. Documentation requirements

- **Progress log**: one dated entry per session; raw pass/fail before interpretation; a
  lane outcome is logged even when the lane never ran — the closure is the outcome.
- **The Verdict Closure Ledger (ADR-0001)**: rows transition UNDECIDED → LAUNCHED or
  CLOSED in Session 1, each with date, window, **kill-date**; zero undated rows gates
  the sitting. A row closed and later re-opened is a NEW row, never a revision of the
  old one — the history is the audit. It remains the public record at release.
- **The paper** (`portfolio/paper/main.tex`): the verdict-independent sections (Intro,
  Related Work, Methods incl. the reproducibility statement, Superposition, refined
  Limitations) become prose in Sessions 3–6; the verdict-gated sections (§3 grokking,
  §5–7 induction/patching/SAE) are resolved by lane consumption in Session 8. Every
  paragraph cites a file on disk; the source is the artifact, `make paper` just
  compiles.
- **New notes** (Obsidian, atomic, each linked to at least two other notes): the
  attribution-patching note with its proof-style workbook + proof
[[05_llm_engineering/proofs/attribution-patching]] (new, S3); the ACDC-experiment note
  with its proof (S4); the SAE-sanity note (S5); the mypy de-drift short record (S7); the
  "how far" interpolation note (contingent, S6); the 300-word honest negative (S6).
- **Skill tree**: flips only via exercises and proofs; the two new instruments get their
  rows; negative outcomes get their own lines.
- **RESULTS.md**: reconciled with every new manifest via `verify-claims`; a struck claim
  is a decision recorded in the ledger, never a silent absence. The Rung 2 and Rung 5
  unresolved rows resolve into the re-scoped expected set — they resolve or they close.
- **Home**: this roadmap is wired as current from the shipping session onward; MP-19
  stays linked as the roadmap this phase executes.

## 3. Practical exercises and hands-on challenges

1. **The closure session (S1 — the phase's Step 1)**: every ledger row becomes LAUNCHED
   (date, window, kill-date) or CLOSED (one named reason), in one sitting, with the
   pre-registered "evidence that would change my belief, by which date" paragraph
   written FIRST. Exit: zero undated rows AND zero rows without a kill-date.
2. **The 20-minute launch rehearsal (S1)**: the entire R1 supervision loop at `--quick`
   scale — launch, heartbeat, one checkpoint, `Stop-Process`, `--resume`, diff
   bit-identical. Make the boring drill boring before the 17–20 h launch is real.
3. **The heartbeat journal (S1–S2)**: under the running R1, the wall-clock R3
   regeneration: a logged heartbeat per checkpoint; I can truth-report "the job is
   alive" from records alone, at any check. (Python buffers stdout when not a TTY —
   `PYTHONUNBUFFERED=1` and the heartbeat are the anti-silent-death pair.)
4. **The P=113 lane, without a silent state (S1)**: one named GPU window on the date;
   else, by Day 4 the pre-committed tie-break fires: the budgeted CPU lane (see
   Session 1's record: P=113 progress-measure witnesses at four checkpoints within the
   budget — the Freq^k readout is the deliverable even without the crossover); else the
   row closes under one named reason. Whatever fires, a dated row and a manifest exist.
5. **The watchdog kill drill (S2)**: a driver with restart-on-abnormal-exit around the
   full-scale R3 `--geometry-check` regeneration; ONE deliberate abnormal exit mid-run;
   the pentagon confirmed at full-scale budget; the silent-death class rehearsed once,
   for real.
6. **The clean-clone dry run (S2)**: `scripts/clean_clone_check.sh` on a fresh temp
   clone; full transcript; zero manual steps. The Phase-6 gate proof
   [[06_production_ai/proofs/reproducible-from-clean-clone]] green.
7. **The claims audit by hand (S3)**: re-derive three headline numbers from manifest +
   code, not from my own prose — pentagon gaps 70.2–73.8°; fresh-batches 52.2%; one
   number born this phase.
8. **Attribution patching, test-first (S3)**: the falsifications written before the
   instrument — self-patching a run against itself is an exact no-op; the
   single-position attribution equals the activation patch on a textbook case.
9. **Rung 6, honestly (S4)**: a one-layer toy circuit first (recurse the pruning loop
   by hand and match my answer), then the real ACDC run on the repeated-token circuit;
   automated-vs-manual recovery per edge; the honest difference sentence.
10. **The SAE sanity (S5)**: the features-vs-ground-truth directions comparison table; a
    qualitative paragraph: "what a dictionary says about a known algorithm". If the
    head-bearing checkpoint does not exist, the declared bound is the deliverable.
11. **The adversarial reader pass (S6)**: I read the draft as three hypothetical
    reviewers who want to *disprove* me; the five strongest attack sentences are
    written and fixed before Session 8. The showcase's best insurance.
12. **The mypy de-drift (S7)**: 171 → ≤160 → ≤150, one short sitting per module, exactly
    one module moved onto the blocking allowlist with its errors-at-move count. The
    ratchet is a mechanism, not a promise.
13. **The 300-word honest negative (S6)**: drafted in advance; the exact words a lane
    6b/6d writeup needs; a skill, not a loss-avoidance drill.
14. **Habit — the 60-second clock check (every session)**: the ledger's undated rows,
    the heartbeat of any running job, the CI status line — before any planning prose.

## 4. Strategic tips and architectural best practices

- **The verdict is the least informative part of the show.** The pre-committed lanes 6a
  (head) / 6b (headless) / 6c (grokked) / 6d (closed-not-verified) guarantee the paper
  has sections, the dashboard has a story and the release has assets whichever way the
  runs land — or close. The phase's design is under the verdict, never the verdict.
- **Deferral-with-a-kill-date is a decision; deferral without one is instinct.** Every
  row stamped, no exceptions. Five phases of "launch is next" end not with more prose
  but with one mechanism: the row names the condition that ends it. A window that
  survives its own kill-date is a lie in the ledger's own terms: it is auto-CLOSED the
  day the date passes, with the date as the reason.
- **Ship on a date, not on a verdict.** Fourteen days from Step 0; the paper is first
  draft or a closed lane, but the release is *on the calendar* before the verdicts are
  opinions.
- **A technique written about without an implementation is a liability.** The model card
  named attribution patching for five phases with nothing to falsify it; the
  instrument-first order (tests before code) is the correction.
- **One variable per retry, one ledger row per verdict.** If P=113 fails, the dials
  change one at a time within the budget pre-registered in Session 1; each turn is a
  row edit, never a paragraph.
- **The ratchet is a mechanism, not a hope.** One module onto the blocking allowlist per
  session, errors-at-move recorded — small, demonstrated, verifiable.
- **The public record is a table, not a narrative.** The ledger, the manifests, the
  transcripts outlive every narrative. Write against them, never around them.
- **A named negative is a contribution.** Rung 5's honest-but-not-yet-dense reading and
  any closed-not-verified lane are paper-quality when declared with the "how far"
  figures — numbers, not adjectives.
- **Reproduce one claim at a time.** The Methods reproducibility statement is the
  paragraph a reviewer uses to decide "can I run this?" — its every citation is a
  transcript or a manifest, never a memory.
- **Rehearse the release once, then release once.** The full release sequence (S9) runs
  verbatim on a branch first (S7); by release day it is a formality, by design.
- **Session clocks beat re-clocks.** Every step in the calendar below has a wall-clock
  budget and an exit gate. A step without a session is a plan — the vault's record
  shows exactly how plans reproduce themselves.

## 5. Step-by-step execution roadmap

```
WEEK 1

SESSION 0 — the pre-flight (this note, ~15–20 min)
  CI green locally AND on GitHub (185 tests, ruff, blocking mypy, markdownlint);
  the ledger re-read row-by-row; this roadmap wired into home; pushed to `dev`; CI
  green on GitHub. Exit: a green floor — everything below runs on top of it only.
  [The fixed terminus: release = this merge + 14 calendar days.]

SESSION 1 — THE CLOSURE (the phase's Step 1, ~45–60 min, one sitting)
  Every ledger row ends LAUNCHED (date, window, kill-date) or CLOSED (one named
  reason); the pre-outcome "evidence that would change my belief" paragraph is
  written FIRST. R1 `--standard` signs its supervised window with its heartbeat and
  checklist; the P=113 row signs its lane (GPU date, or the CPU budget lane with its
  Day-4 tie-break, or a one-reason closure). Exit: ZERO undated rows and ZERO
  rows without a kill-condition when the sitting ends.

SESSION 2 — Durability and the watch (completes while anything runs; ~2–3 h CPU)
  The watchdog around the full-scale R3 `--geometry-check` regeneration with a real
  abnormal-exit drill; the clean-clone dry run with a full transcript. Exit: the
  watchdog provably survives a real death; the transcript has zero manual steps.

SESSION 3 — The instruments and the audit (~2–3 h)
  Attribution patching, test-first: falsifications before code, then wired into the
  patching experiment. The claims audit re-derives three headline numbers. The
  "how far" estimate pre-registered. First paper prose: Intro/Setup drafts.
  Exit: the instrument exists in `src/` and its falsifications are green.

SESSION 4 — Rung 6, honestly (~2–3 h)
  Toy-circuit drill first, then the real ACDC run on the repeated-token task;
  automated-vs-manual recovery per task; the honest difference sentence. Exit: a
  real, non-placeholder computational result + figure + manifest.

SESSION 5 — The SAE sanity (~2–3 h)
  SAE trained against a known-circuit checkpoint (or a declared bound); the
  features-vs-ground-truth alignment table acquires its note; the pentagon
  cross-check written. Exit: a result or a bound, each with its note; the open
  question for the P=113/6c lane exists in the ledger.

WEEK 2

SESSION 6 — The paper and the negative (two seated hours ×2)
  Related Work, Methods (incl. the reproducibility statement), Superposition
  figures, refined Limitations into prose: every paragraph cites a file in the
  repo. The 300-word honest negative drafted. The adversarial-reader pass produces
  the five attack sentences the next sitting will fix. Exit: four/more sections as
  proofed prose; the attack list emitted.

SESSION 7 — The de-drift and the rehearsal (half-day)
  Full-tree mypy ≤ 150 with the second module moved onto the blocking allowlist
  (errors-at-move recorded). The COMPLETE release sequence rehearsed on a branch
  (verify-claims expected-set settled, clean-clone real run, README + model-card
  refresh, `make paper`, PR) — the rehearsal eats the remaining surprises.

SESSION 8 — The verdict lanes (consumes MP-19's decisions wherever S1 left them)
  6a (head):     exp1 manifest; exp4 end-to-end on the real head; exp5 re-test on
                 the head-bearing checkpoint; attribution + path + activation
                 comparisons; model card update; skill flips.
  6b (headless): the K-composition "how far" figure and writeup; R4 sensitivity as
                 honest negative; paper §5–7 framed as declared bounds.
6c (grokked):  exp2 manifest; Fourier figures; hand-verified frequency product;
                  if not on sweep #1, dials change ONE at a time within the
                  pre-registered budget.
  6d (closed):   struck sections; the ledger-visible row re-scoping the expected
                 `verify-claims` set. The 300-word negative is its voice.
  Every row of §6's ledger must match a row in ADR-0001 — no orphan artifact.

SESSION 9 — THE RELEASE (the fixed terminus date)
  Paper draft v0.1; RESULTS reconciled; `make verify-claims` at zero unexpected;
  the real clean-clone transcript; model card + portfolio README refreshed; home
  wired; PR `dev`→`main` on green CI; merge; cleanup; this roadmap archived with
  its deviations — every deviation a dated ledger note.
```

## 6. Gate criteria

1. Session 0: the CI floor is green locally AND on GitHub — before the phase evicts a
   step.
2. Session 1: the ledger has zero undated rows AND zero rows without a kill-date when
   the sitting ends — every row LAUNCHED or CLOSED under a date.
3. Session 2: the watchdog survives one real abnormal exit; the clean-clone transcript
   shows zero manual steps.
4. Session 3: attribution patching exists in `src/` with its falsifications green; the
   claims audit re-derives three headline numbers from manifest + code.
5. Session 4: an honest ACDC result exists — a real run, no placeholder plots.
6. Session 5: the SAE sanity result — or its declared bound — exists with a note.
7. Session 6: the evidence-ordered sections are prose, every paragraph citing a source
   file; the adversarial-reader attack list is closed.
8. Session 7: full-tree mypy ≤ 150 and one more module on the blocking allowlist; the
   release rehearsal transcript complete.
9. Sessions 8–9: whichever lanes fire, a verifiable artifact exists and a ledger row
   names it; the PR merges on green; the release date is kept — the phase ends on it
   whether every lane ran or closed.

## 7. Showcase note (for the portfolio reader)

This is the record of the execution of the planning arc — the phase where the ledger's
rows stop being UNDECIDED. After six micro-phases that promised the same two launches,
the closure sitting stamps dates, windows and **kill-conditions**, so the repository
accepted deferral as a decision or rejected it as instinct. The two methods that were
written about for five phases without implementation are instruments with
falsification tests; the circuit-discovery experiment is real after its placeholder;
and the paper scaffold becomes a first draft in which every sentence a reviewer would
try to re-derive is one manifest or one transcript away from a file on disk. The
showcase motto:

*"The floor was verified, the dates were stamped, and the verdicts were decided under a
kill-condition — the phase that said it would execute actually did."*

## Links

- [[18_micro-phase-19-verdicts-to-publication]] — the roadmap this phase executes; its
  Sessions 0–9 become this calendar's sessions.
- [[17_micro-phase-18-verdict-window]] — the calendars and the inheritance; its S1–S7
  are what Session 1 here signs off on.
- [[docs/adr/0001-verdict-closure-ledger]] — the artifact Session 1 completes; the
  public record of every decision this phase makes.
- [[06_production_ai/proofs/reproducible-from-clean-clone]] — the gate proof whose
  transcripts Sessions 2 and 9 produce.
- [[portfolio/RESULTS]] · [[portfolio/README]] · [[07_capstone/research-plan]] — the
  shelf this phase's release reconciles onto.
- [[04_nlp_and_transformers/notes/induction-heads]] and
  [[04_nlp_and_transformers/notes/attribution-patching]] — the notes that absorb the
  verdicts and the new instrument (the latter written in Session 3).
- [[05_llm_engineering/proofs/intervention-validity]] — the sister proof the S3
  falsifications extend.