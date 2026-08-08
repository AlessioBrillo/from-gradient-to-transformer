---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-08
---

# Micro-Phase 19 — The Verdicts, the Publication, the Next Arc (roadmap)

Written as a personal learning log and a public record, like every roadmap before it.
Micro-Phase 18 bound every step to a clocked session and made the Verdict Closure
Ledger ([[docs/adr/0001-verdict-closure-ledger]]) the artifact that turns waiting
into a decision. This phase executes what MP-18 decided: whatever the verdicts are,
they already have pre-committed lanes (6a head / 6b headless / 6c grokked /
6d closed-not-verified) defined in [[16_micro-phase-17-closure-and-release]] and
[[17_micro-phase-18-verdict-window]].

MP-19 adds no new promises. It commits to four verdict-agnostic deliverables:

1. **The paper draft v0.1** — every verdict-independent section written in prose, every
   paragraph citing a file on disk.
2. **The reconciled release** — `make verify-claims` at zero unexpected problems, the
   real clean-clone transcript, the model card rewritten, the release rehearsed.
3. **Rung 6, honestly** — ACDC (Conmy et al., 2023) run for real, compared against the
   hand-found Rung 4 circuit; the deleted placeholder gets a real successor.
4. **Two missing instruments** — attribution patching (written about in the model card,
   never implemented in `src/`), and an SAE-on-a-known-circuit sanity check that tests
   the dictionary against ground truth instead of against nothing.

## Design principle

**Consume, don't re-plan.** MP-18's Sessions S1–S7 remain the execution vehicle; this
phase's Session 0 *starts by verifying the ledger has zero undated rows* — and if it
does not, the phase's first act is the closure sitting itself, not this roadmap.
Verdict-gated writing (paper §3, §5–§7) consumes the lanes instead of guessing them;
verdict-independent writing (Related Work, Methods, Superposition, refined
Limitations) proceeds regardless, because the evidence already exists and is
committed.

## Where this phase starts (state review, verified against the repo)

I checked `git status`, the manifests, the ledger and the CI floor before writing a
single claim here.

- **MP-18 Step 0 is shipped**: the roadmap [[17_micro-phase-18-verdict-window]] and its
  ledger exist, wired into [[00_meta/00_home]]; `dev` pushed and merged contentwise
  (`main` = `dev` + the merge/squash commits of Step 0). Tree clean locally.
- **MP-18 Sessions 1–7 remain unexecuted**: all ten ledger rows are still UNDECIDED —
  the closure decision, the R1 `--standard` run, the P=113 × 3 seeds Colab lane,
  the R3 watchdog regeneration, the clean-clone transcript, the paper spine, the mypy
  de-drift, the model card, the release rehearsal, the verdict lanes themselves.
  Five micro-phases pre-registered the same two flagship runs; the ledger exists
  precisely so this phase either launches them or closes them under a dated reason.
- **Baseline CI floor (re-verified this session)**: 185 tests passing, fully green;
  ruff clean on `src/ tests/`; blocking mypy clean (`src/results.py`,
  `src/experiments/runner.py`); full-tree mypy at 171 (the tracked, non-blocking
  ratchet); `make verify-claims` at its designed 2 problems — Rungs 2 and 5 are still
  manifestless by design; markdownlint is part of the push CI and stays clean.
- **The strongest verified result stands and needs no verdict**: Rung 3's superposition
  phase transition (10/20 → 20/20 features as sparsity drops 0.5 → 0.01; pentagon
  geometry 70.2–73.8° gaps, std ≤ 1.4° vs the ideal 72°), backed by a committed
  multi-seed manifest and curated, tracked figures in `portfolio/figures/`.
- **The committed fallback stands**: the K-composition detector
  (`k_composition_scores` → `plot_composition_diagnostic` in `exp1_induction_heads.py`)
  turns a headless R1 verdict into a figure, not a hole.
- **The instrument set ends short in exactly two places**: attribution patching is the
  one technique named in the model card ("attribution patching can mislead") that has
  no implementation to falsify; and the SAE has never been validated against a circuit
  whose ground truth is known — Rung 5's real-activation numbers are honest but need a
  head-bearing checkpoint to mean more than a density bound.

### Bottleneck analysis (ranked by what blocks what)

1. **The closure decision is the critical path of the critical path.** Five phases
   ended at "launch is next." The ledger is the mechanism and Session 1 is the
   sitting: every row becomes LAUNCHED (date, window, heartbeat) or CLOSED (date, one
   named reason) — there is no third state.
2. **The paper is still ~100% `% TODO`** though four sections are writable today from
   committed evidence. Clocked writing sessions (S3, S6) are the only cure that has
   not been tried for four phases.
3. **Rung 6 is a hole in the portfolio where a contribution belongs.** The deleted
   placeholder (fabricated ACDC numbers, removed 2026-08-01) leaves the
   automated-vs-manual question unanswered; a real ACDC run is the highest-value new
   experiment this phase can ship in any verdict lane.
4. **mypy 171 is a scheduled de-drift, not a blocker** — three short sittings at one
   module each, moving exactly one module onto the blocking list as a demonstration of
   the ratchet.
5. **The clean-clone gate has never run once** — one transcript away from a formality,
   and a hard gate for the release and the model card.

## 1. Deep-dive study and research topics (each bound to a session — no topic without a deliverable)

| Topic | Session | The deliverable that proves the reading |
|---|---|---|
| Nanda et al., "Attribution Patching: Activation Patching at Industrial Scale" (2023) | S3 | `attribution_patching` implemented in `src/`, wired into `exp4`, with falsification tests (self-patch = exact no-op; matches activation patching on a textbook case); the new note [[04_nlp_and_transformers/notes/attribution-patching]] written in S3 |
| Conmy et al., "Towards Automated Circuit Discovery for Mechanistic Interpretability" (ICLR 2023) | S4 | Rung 6 returns: an ACDC run on the repeated-token task, automated-vs-manual circuit table, faithfulness per omitted edge — the placeholder's honest successor |
| Zhang & Nanda, "Towards Best Practices of Activation Patching" (ICLR 2024) — read second, after attribution patching exists | S5 | The per-site audit table mapped onto `exp4`, now completed with attribution-patching comparisons; feeds paper Methods |
| Nanda et al., "Progress Measures for Grokking" (ICLR 2023) — re-read with a checkpoint (or a closure) in hand | S6 | The Freq^k sparsity hand-verification protocol; if 6c: the figures; if 6d: the named-suspect analysis table |
| Bricken et al., "Towards Monosemanticity" (2023) + Cunningham et al. (ICLR 2024) | S5 | The SAE-on-known-circuit sanity check: features should align with the ground-truth directions where the circuit is known; where they don't, that is a finding |
| Elhage et al., "Toy Models of Superposition" (2022) | S5 | Cross-check the SAE sanity against the pentagon geometry — the two puzzles must agree |
| Olsson et al., "In-context Learning and Induction Heads" (2022) | S6 | The interpolation commentary for the K-composition "how far" figure, in either lane |
| Pineau et al., "Improving Reproducibility in ML Research" (JMLR 2021) | S3 | The claims audit applied to three headline numbers, written into the paper's Methods as the reproducibility statement |
| Power et al., "Grokking: Generalization Beyond Overfitting" (2022) | S6 | The single-variable retry dials (weight decay / LR / P) pre-set on paper before their budget exists |

The MP-17/MP-18 reading lists are inherited wholesale on top of this — the study
calendar is the same calendar (MP-18 S1–S7) with this phase's additive S3–S6 slots.

## 2. Documentation requirements

- **Progress log**: one dated entry per session; raw pass/fail before interpretation;
  a lane outcome is logged even when the lane never ran (the closure is the outcome).
- **The Verdict Closure Ledger (ADR-0001)**: rows transition from UNDECIDED to
  LAUNCHED or CLOSED in Session 1; no row survives this phase without a date and a
  reason. It remains the public record at release.
- **The paper** (`portfolio/paper/main.tex`): verdict-independent sections become
  prose in Sessions 3–6 (Intro/Setup, Related Work, Methods incl. the reproducibility
  statement, Superposition, refined Limitations), verdict-gated sections (§3
  grokking, §5–§7 induction/patching/SAE) are resolved by lane consumption in
  Session 8. Every paragraph cites a file on disk; the source is the artifact, `make
  paper` just compiles.
- **New notes** (Obsidian, atomic, linked to at least two other notes): the
  attribution-patching note with its proof-style workbook; a proof
  [[05_llm_engineering/proofs/attribution-patching]] (new, S3); the ACDC-experiment
  note + proof; the SAE-sanity note; the mypy-de-drift short record; the "how far"
  interpolation note (contingent); the 300-word honest negative.
- **Skill tree:** flips only via exercises and proofs; the two new instruments get
  their rows; negative outcomes get their own lines.
- **RESULTS.md:** reconciled with every new manifest; a struck claim is a decision
  recorded in the ledger, never a silent absence. This includes the Rung 2 and Rung 5
  unresolved rows — they resolve or they close.
- **Home:** this roadmap is wired as current from the shipping session onward.

## 3. Practical exercises and hands-on challenges

1. **Challenge — the closure session (S1, the phase's Step 1)**: every ledger row
   becomes LAUNCHED (date, window, heartbeat) or CLOSED (one named reason), in one
   sitting, with the pre-registered "evidence that would change my belief, by which
   date" paragraph written first.
2. **Challenge — the R1 supervised launch (S1, same sitting)**: `--standard` on this
   machine under heartbeat + `PYTHONUNBUFFERED`, checkpoint-every 500, a named plan
   for every 3 h of elapsed time, a written fallback if the machine cannot be held.
3. **Launch — the P=113 lane (S1, decision)**: Colab notebook run with
   `pin_colab_run.py` provenance, or a budgeted CPU alternative, or a written closure
   with one named reason — the lane has no silent state.
4. **Challenge — the R3 watchdog regeneration (S2)**: a driver with
   restart-on-abnormal-exit; a deliberate abnormal exit mid-run; the pentagon
   confirmed at full-scale budget; the silent-death class drilled once, for real.
5. **Challenge — the clean-clone dry run (S2)**: `scripts/clean_clone_check.sh` on a
   fresh temp clone; full transcript; zero manual steps. This is the Phase-6 gate
   proof [[06_production_ai/proofs/reproducible-from-clean-clone]] finally going
   green.
6. **Exercise — the claims audit (S3)**: re-derive three headline numbers from
   manifest + code by hand: pentagon gaps 70.2–73.8; fresh-batches 52.2%; one new
   number born this phase.
7. **Challenge — attribution patching, test-first (S3)**: write the falsification
   first (self-attribution on a run patched against itself is an exact no-op; the
   single-position equals the activation-patch on a textbook case), then the
   instrument.
8. **Challenge — Rung 6, honestly (S4)**: real ACDC on the repeated-token circuit;
   automated-vs-manual recovery per edge; a written sentence where they differ.
9. **Exercise — the SAE sanity (S5)**: features vs ground-truth directions comparison
   table; the qualitative "what a dictionary says about a known algorithm" paragraph.
10. **Challenge — the mypy de-drift (S7)**: 171 → ≤160 → ≤150, one module per
    session, exactly one moved onto the blocking allowlist with its errors-at-move
    count recorded.
11. **Habit — the 60-second clock check (every session)**: the ledger's undated rows,
    the heartbeat of any running job, the CI status line — before any planning prose.
12. **Pre-registration — the "how far" estimate (S3)**: expected K-composition
    threshold and the figure that would count as evidence, before any verdict; scored
    in Session 8's lane consumption.
13. **Exercise — the honest negative in 300 words (S6)**: drafted in advance; the
    exact words a lane 6b/6d writeup needs; a skill, not a loss-avoidance drill.

## 4. Strategic tips and architectural best practices

- **The verdict is the least informative part of the show.** The pre-committed lanes
  guarantee the paper has sections, the dashboard has a story, and the release has
  assets, whichever way the runs land (or close). The phase's job is the design under
  the verdict, never the verdict itself.
- **A technique written about without an implementation is a liability.** The model
  card named attribution patching for four phases with nothing to falsify it; this
  phase's instrument-first order (tests before code) is the correction.
- **One variable per retry, one ledger row per verdict.** If P=113 fails, dials change
  one at a time with the pre-set S3 budget, and the row records each turn.
- **The ratchet is a mechanism, not a hope.** One module per session onto the
  blocking allowlist, errors-at-move recorded — small, demonstrated, verifiable.
- **The public record is a table, not a narrative.** The ledger, the manifests, the
  transcripts — they outlive every narrative. Write against them, never around them.
- **A named negative is a contribution.** Rung 5's honest-but-not-sparse reading and
  any closed-not-verified lane are paper-quality when declared as such with the "how
  far" figures.
- **Release discipline: rehearse once, real once.** Every step the release sequence
  needs is first rehearsed on a branch with a transcript (S7), then executed for real
  (S9) — the release becomes a formality before it becomes the deliverable.
- **Session clocks beat roadmaps.** MP-18's calendars bound every step; this phase's
  sessions inherit the same treatment. A step without a session is a plan; the record
  shows plans reproduce themselves.

## 5. Step-by-step execution roadmap

```
SESSION 0 — the pre-flight (this note, ~15–20 min)
  CI green locally (≥185 tests, ruff, blocking mypy, markdownlint); the ledger read
  row-by-row; this roadmap wired into home; pushed to `dev`; CI green on GitHub.
  Exit: a green floor — everything below runs on top of it only.

SESSION 1 — THE CLOSURE DECISION (the phase's Step 1, ~30–45 min, one sitting):
  every ledger row ends LAUNCHED (date, window, heartbeat) or CLOSED (one named
  reason). The R1 `--standard` trigger is decided and possibly launched in the same
  sitting (supervised window, `PYTHONUNBUFFERED=1`, checkpoint-every 500, named
  reschedule rule). The P=113 row is signed. The pre-outcome commitment paragraph is
  written. Exit: the ledger has ZERO undated rows when the sitting ends.

SESSION 2 — Durability and the watch (completes while anything runs, ~2–3 h CPU):
  the watchdog driver around the full-scale R3 `--geometry-check` regeneration with
  a deliberate abnormal-exit drill; the clean-clone dry run with a full transcript;
  the P=113 row settled. Exit: the watchdog provably survives a real death; the
  transcript has zero manual steps; the P=113 row is signed.

SESSION 3 — The instruments and the audit (~2–3 h): attribution patching implemented
  test-first and wired into `exp4`; the claims audit on three headline numbers; the
  "how far" estimate pre-registered; the first two evidence-ordered paper sections
  become prose.

SESSION 4 — Rung 6, honestly (~2–3 h): real ACDC run on the repeated-token task;
  the automated-vs-manual table; the honest difference statement. Exit: a real,
  non-placeholder computational result + figure.

SESSION 5 — The SAE sanity (~2–3 h): SAE trained against a known-circuit checkpoint
  (or a declared bound); features-vs-ground-truth comparison; the 300-word reading.
  Exit: a result or a bound, each with its note.

SESSION 6 — The paper and the negative (two seated sessions of ~2 h each): Related
  Work, Methods (incl. reproducibility statement), Superposition figures, refined
  Limitations into prose, every paragraph citing a file; the 300-word honest
  negative drafted. Exit: four sections as proofed prose.

SESSION 7 — The de-drift and the rehearsal (half-day): full-tree mypy ≤ 150, the
  second module moved to the blocking allowlist with its count; the complete release
  sequence rehearsed on a branch (verify-claims, clean-clone real run, README +
  model-card refresh, `make paper`, PR) — the rehearsal eats the remaining surprises.

SESSION 8 — The verdict lanes (consuming MP-18's decisions wherever S1 left them):
  6a (head):   exp1 manifest; exp4 E2E on the real head; exp5 re-test on the
               head-bearing checkpoint; attribution + path + activation comparisons;
               model card update; skill flips.
  6b (headless): the K-composition "how far" figure and writeup; R4 sensitivity as
               honest negative; paper §5–7 framed as declared bounds.
  6c (grokked): exp2 manifest; Fourier figures; hand-verified frequency product; if
               not on sweep #1, dials change ONE at a time within the set budget.
  6d (closed-not-verified): struck sections and the ledger-visible row re-scoping
               the expected set of `verify-claims`.

SESSION 9 — The release (the phase's Step 9): paper draft v0.1; RESULTS.md
  reconciled; `make verify-claims` at zero unexpected; the real clean-clone transcript; the
  model card and portfolio README refreshed; home wired; PR `dev`→`main` on green
  CI; merge; cleanup; archive this roadmap with its deviations noted.
```

## 6. Gate criteria

1. Session 0: the CI floor is green locally **and** on GitHub before the phase moves.
2. Session 1: the ledger has **zero undated rows** when the sitting ends — every row
   LAUNCHED or CLOSED with a date and a reason.
3. Session 2: the watchdog survives a real abnormal exit; the clean-clone transcript
   shows zero manual steps.
4. Session 3: attribution patching exists in `src/` with its falsifications green; the
   claims audit re-derives three headline numbers.
5. Session 4: an honest ACDC result exists — a real run, no placeholder plots.
6. Session 5: the SAE sanity result — or its declared bound — exists with a note.
7. Session 7: full-tree mypy ≤ 150 and one more module on the blocking allowlist.
8. Sessions 8–9: whichever lanes fire, a verifiable artifact exists; the PR merges on
   green; the release is a formality.

## 7. Showcase note (for the portfolio reader)

This roadmap is the public record of the *finish of the planning arc*: after six
micro-phases that promised the same two launches, the verdicts are decided under
dates — launched with a heartbeat, or closed with one named reason; the two methods
that were written about but never implemented are now instruments that can be
falsified; the circuit-discovery experiment is real after its placeholder; and the
paper that was a `% TODO` scaffold for six phases exists as its first full draft with
a reproducibility statement a reviewer can actually run. The showcase motto:

*"The floor was verified, the clocks were bound, and the verdicts were published
— the paper shipped because the process made waiting a decision."*

## Links

- [[17_micro-phase-18-verdict-window]] — the verdict window this phase executes; its
  Sessions S1–S7 are this phase's inheritance.
- [[16_micro-phase-17-closure-and-release]] — "closure over continuation"; the lane
  definitions and paper-spine rules this phase loads on.
- [[docs/adr/0001-verdict-closure-ledger]] — the artifact Session 1 must finish.
- [[06_production_ai/proofs/reproducible-from-clean-clone]] — the gate proof whose
  transcripts Sessions 2 and 9 produce.
- [[portfolio/RESULTS]] · [[portfolio/README]] · [[07_capstone/research-plan]] — the
  shelf this phase's release reconciles onto.
- [[04_nlp_and_transformers/notes/induction-heads]] and
  [[04_nlp_and_transformers/notes/path-patching]] — the notes that absorb the
  verdicts and the Zhang–Nanda audit.