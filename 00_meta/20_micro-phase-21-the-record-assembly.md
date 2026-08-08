---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-08
---

# Micro-Phase 21 — The Record Assembly: Consume the Release, Publish the Gates, Graduate

Written as a personal learning log and a public record, like every roadmap before it.
Micro-Phase 20 shipped its Step 0 and with it the two terms the verdict ledger
[[docs/adr/0001-verdict-closure-ledger]] was missing — a release date fixed first, and a
kill-date on every row. By the time this phase starts, MP-20 has either released (on its
14-day terminus) or the ledger's own rules have auto-CLOSED the rows whose dates passed.
Either way, the repository has a *release state* — and this phase's job is to consume it:
the paper compiles, the gates close under dates, and the graduation proof is asked and
answered honestly. I add no new promises: the record is the paper, whatever the verdicts
are.

## Design decisions

- **The starting artifact is the release state, not the promise.** This phase's Step 0 is
  a truthing pass: I read what MP-20 actually shipped — ledger rows, manifests, paper
  prose, transcripts — and write the *actual-state sheet*: one row per promise, each
  ending as SHIPPED (artifact tagged), RE-SCOPED (dated lane), or STRUCK (dated reason).
  A claim with no file is struck. This is "consume, don't re-plan" made literal.
- **The record is the paper.** Whatever lanes fired (or closed), `portfolio/paper/main.tex`
  compiles to a first draft by S6. Every sentence that carries a number cites a manifest,
  a figure, or a ledger row on disk — `make paper` just compiles the repo.
- **Gates close under dates, not moods.** The five `[~]` rows of the skill tree / RESULTS
  (nnsight, W&B, HF Spaces, clean-clone proof, graduation) each end in one sitting as
  LAUNCHED or CLOSED-with-one-reason — the ledger mechanism, applied to gate boxes.
- **The terminus is stamped at Step 0**: release = this roadmap's merge + 14 calendar
  days. On that date the phase ships — whichever rows are left, the paper and the release
  are the deliverables, and the honest residue is a dated list, not a silence.

## Where this phase starts (state review, verified against the repo)

I checked `git status`, the manifests, the ledger, the CI floor and the paper scaffold
before writing a single claim here.

- **Tree state**: `dev` and `main` are tree-identical (MP-20's Step 0 was squash-merged
  via PR #45; the six repair commits that followed on `dev` are history-only — a
  normal squash-merge artifact, no content divergence). Working tree clean. No open PRs.
- **The CI floor, re-verified this session**: **185 tests passing** (78.8 s locally),
  ruff clean on `src/ tests/`, blocking mypy clean (`src/results.py`,
  `src/experiments/runner.py`), full-tree mypy at its tracked **171** (exit 1, the
  non-blocking ratchet), `make verify-claims` at exactly its designed 2 problems (Rung 2
  and Rung 5 manifestless by design), markdownlint 0 issues on 178 files.
- **Environment incident, recorded honestly**: `make` had vanished from this machine
  entirely (the same class of silent environment rot as MP-14's disappearing `uv`).
  Restored with GNU Make 4.4.1 (winget, ezwinports) — user-scope, no admin, `make
  ci-check` works again from any shell with Git's `bin/` on PATH. The vault's documented
  gate is the interface; the incident gets the same honest treatment as MP-14's.
- **The ledger is still materially empty**: all ten rows in ADR-0001 remain UNDECIDED.
  MP-20's Session 1 (the closure sitting) owns that; this phase starts by reading
  whatever state the sitting produced — launched-with-heartbeat, closed-with-reason, or
  (if the sitting never fired) the rows auto-CLOSED by their own kill-dates.
- **The paper is still a scaffold**: every section of `portfolio/paper/main.tex` is a
  `% TODO`, while four sections are writable today from committed evidence. The abstract
  exists only as a pre-filled placeholder. `make paper` works when a LaTeX toolchain is
  present; the clean-clone transcript must now include the LaTeX install and a compile.
- **The strongest verified result stands**: Rung 3's superposition phase transition
  (10/20 → 20/20 features as sparsity drops 0.5 → 0.01; pentagon geometry 70.2–73.8°
  gaps, std ≤ 1.4° vs the ideal 72°) with its committed multi-seed manifest and curated
  figures in `portfolio/figures/`.
- **The instrument set ends short in exactly two places**: attribution patching is the
  one technique named in the model card with no implementation to falsify it; and the SAE
  has never been validated against a circuit whose ground truth is known. Rung 6 (ACDC)
  has no honest successor since the placeholder's deletion.
- **`checkpoints/` holds only the kill-drill artifacts** — no head-bearing checkpoint
  has ever existed, which is why Rung 4's path patching and Rung 5's real-activation
  numbers stay bounds rather than findings.

### Bottleneck analysis (ranked by what blocks what)

1. **The release state itself.** MP-20's Session 1 decides whether the two flagship rows
   carry verdicts or closures. This phase consumes either — but the *paper's* §3 and
   §5–7 are written from the row outcomes, so Step 0's actual-state sheet is the
   critical path. It is a 20-minute truthing, not a re-plan.
2. **The paper's prose.** Six phases of scaffold. Seated writing sessions with a
   per-paragraph file-citation rule remain the only cure never fully tried.
3. **The five gate rows.** Each is a decision with a date: nnsight (run the toy probe or
   close with one reason — no GPU), W&B (wire or close; manifests already cover its role),
   HF Spaces (re-scope "browsable artifact" to the regenerated figure set, or ship a
   Space), clean-clone proof (the transcript, now including LaTeX), graduation (the
   written answer to "how does your transformer compute?").
4. **The instruments** (attribution patching, ACDC successor, SAE sanity) — three
   sessions of real work in any verdict lane; two of them are already bound in MP-20's
   calendar, so this phase inherits rather than re-plans them.
5. **The mypy ratchet (171)** — scheduled, not blocking: the same three-short-sittings
   mechanism as MP-20, one module per sitting.

## 1. Deep-dive study and research topics (bound to a session — no topic without a deliverable)

| Topic | Session | The deliverable that proves the reading |
|---|---|---|
| Booth, Colomb & Williams, *The Craft of Research* (4th ed.) | S1 | The paper's argument skeleton on paper: claims → evidence → warrants, mapped one-to-one onto `main.tex`'s sections before any prose |
| Nanda et al., "Attribution Patching: Activation Patching at Industrial Scale" (2023) | S1 | `attribution_patching` in `src/`, wired into `exp4`, falsifications green — or the row closes with one dated reason (the model card's "attribution patching can mislead" line finally has something to be true of, either way) |
| Conmy et al., "Towards Automated Circuit Discovery for Mechanistic Interpretability" (ICLR 2023) | S2 | A real ACDC run on the repeated-token task, automated-vs-manual recovery per edge, the honest difference sentence — the placeholder's real successor |
| Nosek et al., "Promoting an Open Research Culture" (Science 2015) | S2 | The pre-registration paragraph that turns whichever Rung 2 outcome exists into a contribution clause, not an apology |
| Zhang & Nanda, "Best Practices of Activation Patching" (ICLR 2024) — read after the instruments exist | S3 | The per-site audit table mapped onto the instrumented `exp4`; feeds paper Methods |
| Nanda et al., "Progress Measures for Grokking" (ICLR 2023) — re-read with the manifests, not the memory | S4 | The Freq^k sparsity hand-verification protocol executed against the committed record; if the lane never fired, the named-suspect table |
| Elhage et al., "Toy Models of Superposition" (2022) — re-read against the committed geometry | S4 | The pentagon-to-circuit bridge paragraph: what the geometry data licenses, written with file citations |
| Bricken et al., "Towards Monosemanticity" (2023) + Cunningham et al. (ICLR 2024) | S5 | The SAE-sanity table: features vs ground-truth directions where the circuit is known; where they don't align, that is a finding |
| Olsson et al., "In-Context Learning and Induction Heads" (2022) | S5 | The interpolation commentary for the K-composition figure, in whatever lane stands |
| Pineau et al., "Improving Reproducibility in ML Research" (JMLR 2021) | S5 | The reproducibility statement in paper Methods, every citation a transcript or a manifest |
| Power et al., "Grokking: Generalization Beyond Overfitting" (2022) — final re-read | S6 | The single-variable retry record (weight decay / LR / P) as a ledger appendix, one row per turn |

The MP-18/19/20 reading lists are inherited wholesale — my study calendar is the same
calendar with this phase's S1–S5 slots bound to instruments and the paper.

## 2. Documentation requirements

- **Progress log**: one dated entry per session; raw pass/fail before interpretation; a
  lane outcome is logged even when the lane never ran — the closure is the outcome.
- **The actual-state sheet (S0, this phase's Step 0)**: one page, one row per MP-20
  promise: SHIPPED (file tag) / RE-SCOPED (dated lane) / STRUCK (dated reason). It is the
  working plan of the phase — anything that survives as prose but has no row is drift.
- **The Verdict Closure Ledger (ADR-0001)**: MP-20's rows are consumed (final states
  recorded); this phase's own new rows (the five gate decisions, the instruments) open
  with date, window and kill-date, under the same rules. Closed-then-reopened is a NEW
  row, never a revision — the history is the audit.
- **The paper** (`portfolio/paper/main.tex`): the argument skeleton (S1) first, then
  prose in evidence order — the verdict-independent sections (Intro/Setup, Related Work,
  Methods incl. the reproducibility statement, Superposition, refined Limitations)
  regardless of lanes; §3 grokking, §5–7 induction/patching/SAE per the actual-state
  sheet. Every paragraph cites a file on disk. `make paper` compiles by S4, zero errors.
- **RESULTS.md**: reconciled with every manifest via `verify-claims`; a struck claim
  carries the ledger row that struck it. The Rung 2 and Rung 5 unresolved rows resolve
  or close — no third state.
- **Skill tree**: the five gate rows each end LAUNCHED or CLOSED-with-a-line in one
  sitting; boxes flip only via exercises and proofs; negative outcomes get their own
  lines, never a silent absence.
- **New notes** (Obsidian, atomic, each linked to at least two other notes): the
  attribution-patching note + proof (contingent on S1's instrument lane); the ACDC note +
  proof (S2); the SAE-sanity note (S5); the "how far" interpolation note (contingent,
  S5); the graduation proof note (S6); the paper-argument note (S1) that records how the
  skeleton was built.
- **Home**: this roadmap wired as current from the shipping session onward; MP-20 stays
  linked as the roadmap this phase consumes.

## 3. Practical exercises and hands-on challenges

1. **The truthing pass (S0 — the phase's Step 0)**: read the ledger, the manifests, the
   paper's prose %, the transcripts; write the actual-state sheet. Exit: zero promises
   without a row, zero rows without a status.
2. **The argument skeleton (S1)**: the paper's claims→evidence→warrants map written by
   hand first; the abstract rewritten so every sentence names a file. The skeleton is the
   scaffold the prose fills.
3. **The compile drill (S1–S6)**: after every writing session, `make paper` must compile;
   the first compile failure of a session is a finding logged in the progress log, not a
   frustration.
4. **Attribution patching, test-first (S1)**: falsifications before the instrument —
   self-attribution is an exact no-op; single-position equals the activation patch on a
   textbook case. If the row closes instead, the closure IS the exercise.
5. **Rung 6, honestly (S2)**: a toy-circuit recursion drill first (prune by hand, match
   my answer), then the real ACDC run; automated-vs-manual recovery per edge; the honest
   difference sentence.
6. **The claims audit by hand (S3)**: re-derive three headline numbers from manifest +
   code, not from my own prose — pentagon gaps 70.2–73.8°; fresh-batches 52.2%; one number
   born this phase. Each lands in the paper Methods as the reproducibility trio.
7. **The gate-closing sitting (S3)**: the five `[~]` rows decided in one sitting —
   each LAUNCHED with a date or CLOSED with one named reason. Exit: the skill tree's
   `[~]` count is zero or every remaining row has a date.
8. **The SAE sanity (S5)**: features vs ground-truth directions table; the qualitative
   "what a dictionary says about a known algorithm" paragraph. If the head-bearing
   checkpoint does not exist, the declared bound is the deliverable.
9. **The adversarial reader pass (S6)**: the whole draft read as three hypothetical
   reviewers who want to disprove me; the five strongest attack sentences per major
   section are written and fixed before the release.
10. **The 300-word honest negative (S6)**: the exact words any closed-not-verified lane
    needs; drafted in advance, a skill rather than a loss-avoidance drill.
11. **The mypy de-drift (S7)**: 171 → ≤160 → ≤150, one short sitting per module, exactly
    one module moved onto the blocking allowlist with its errors-at-move count.
12. **The graduation proof (S7)**: the Phase-7 gate question answered in writing —
    "how does your transformer implement modular addition?" — scoped to the actual
    record: the Fourier algorithm, the progress measures, the causal confirmation, each
    with its manifest; where the record closes, the closure is part of the answer.
13. **The clean-room run (S8)**: fresh clone, `uv sync`, full suite, `make paper` with
    the LaTeX toolchain, `verify-claims` — one transcript, zero manual steps. The Phase-6
    gate proof [[06_production_ai/proofs/reproducible-from-clean-clone]] green for real.
14. **Habit — the 60-second clock check (every session)**: the ledger's undated rows,
    the heartbeat of any running job, the CI status line — before any planning prose.

## 4. Strategic tips and architectural best practices

- **The verdict is the least informative part of the show** — inherited, still load
  bearing: the record is designed so the paper and the release exist in every lane,
  including the lane that fired never again.
- **A claim with no file is struck.** The actual-state sheet and the paper's citation
  rule are the same discipline at two scales: the record is tables and manifests, not
  narrative.
- **The paper is an argument, not a dump.** The skeleton (claims → evidence → warrants)
  comes before prose; every section's last paragraph is a warrant for the next section's
  first claim.
- **A gate box without a date is a lie.** The five `[~]` rows each end in one sitting;
  "decided, evidence here" and "closed, reason here" are both completions. The skill
  tree's own rule — a checked box without proof is a lie you tell yourself — applies to
  unchecked boxes too.
- **Deferral-with-a-kill-date is a decision; deferral without one is instinct** —
  inherited, applied to this phase's own rows without exception.
- **Instrument first, then read.** Zhang & Nanda's audit means nothing until the
  instrument exists to audit; the instrument-first order (tests before code) is the
  correction, not the reading order.
- **A named negative is a contribution** — inherited: Rung 2's pre-registered negative
  protocol and any closed lane are paper-quality when declared with the "how far"
  figures.
- **The ratchet is a mechanism, not a hope** — inherited: one module per sitting onto
  the blocking allowlist, errors-at-move recorded.
- **Session clocks beat re-clocks** — inherited: every step below has a wall-clock
  budget and an exit gate.
- **Rehearse the release once, then release once** — inherited: the clean-room run (S8)
  is rehearsed on a branch first (S7); by release day it is a formality, by design.

## 5. Step-by-step execution roadmap

```
WEEK 1

SESSION 0 — the pre-flight (this note, ~15–20 min)
  CI green locally AND on GitHub (185 tests, ruff, blocking mypy, markdownlint);
  the ledger re-read row-by-row; this roadmap wired into home; pushed to `dev`; CI
  green on GitHub. Exit: a green floor — everything below runs on top of it only.
  [The fixed terminus: release = this merge + 14 calendar days.]

SESSION 1 — THE TRUTHING and the skeleton (the phase's Step 1, ~2 h, one sitting)
  The actual-state sheet: every MP-20 promise ends SHIPPED / RE-SCOPED / STRUCK.
  The paper's argument skeleton written by hand. Attribution patching: instrument
  test-first, or the row closes with one dated reason. Exit: zero promises without
  a row; the skeleton exists; the attribution row is INSTRUMENT or CLOSED.

SESSION 2 — Rung 6, honestly, and the pre-registration (~2–3 h)
  Toy-circuit ACDC drill, then the real run on the repeated-token task; the
  automated-vs-manual table; the pre-registration paragraph for the Rung 2 outcome.
  Exit: a real, non-placeholder computational result + figure + manifest.

SESSION 3 — The instruments, the audit and the gates (~2–3 h)
  The claims audit re-derives three headline numbers from manifest + code. The
  gate-closing sitting: nnsight, W&B, HF Spaces each LAUNCHED or CLOSED with one
  reason. Zhang & Nanda's per-site audit table mapped onto the instrumented `exp4`.
  First paper prose: Intro/Setup + Methods (incl. the reproducibility trio).
  Exit: the three gate rows are stamped; Methods is prose.

SESSION 4 — The evidence sections (~2–3 h)
  §3 grokking and §6 induction per the actual-state sheet (verdict lane or closure
  lane, each with its figure or its negative). The Freq^k hand-verification protocol
  against the committed record. `make paper` compiles by the end of this session.
  Exit: §3 and §6 exist as prose with file citations; the paper compiles.

SESSION 5 — The SAE sanity and the cross-checks (~2–3 h)
  SAE trained against a known-circuit checkpoint (or a declared bound); the
  features-vs-ground-truth table; the pentagon cross-check written; the "how far"
  interpolation note (contingent). Exit: a result or a bound, each with its note.

WEEK 2

SESSION 6 — The paper endgame (two seated hours ×2)
  Related Work, Superposition, refined Limitations, Conclusion into prose; every
  paragraph cites a file. The 300-word honest negative drafted. The adversarial-reader
  pass produces the attack list the next sitting will fix. Exit: all sections exist
  as proofed prose; the attack list is emitted.

SESSION 7 — The de-drift, the proof and the rehearsal (half-day)
  Full-tree mypy ≤ 150 with one more module on the blocking allowlist (errors-at-move
  recorded). The graduation proof written, scoped to the actual record. The COMPLETE
  release sequence rehearsed on a branch (verify-claims expected-set settled,
  clean-room run, README + model-card refresh, `make paper`, PR) — the rehearsal eats
  the remaining surprises.

SESSION 8 — THE RELEASE (the fixed terminus date)
  Paper draft v1.0; RESULTS reconciled; `make verify-claims` at zero unexpected; the
  real clean-room transcript (fresh clone + LaTeX compile); model card + portfolio
  README refreshed; home wired; PR `dev`→`main` on green CI; merge; cleanup; this
  roadmap archived with its deviations — every deviation a dated ledger note.
```

## 6. Gate criteria

1. Session 0: the CI floor is green locally AND on GitHub — before the phase evicts a
   step.
2. Session 1: the actual-state sheet has zero promises without a row; the paper's
   argument skeleton exists; the attribution row is INSTRUMENT or CLOSED under a date.
3. Session 2: an honest ACDC result exists — a real run, no placeholder plots — or the
   row closes under the kill-date with the negative written.
4. Session 3: the claims audit re-derives three headline numbers; the three gate rows
   (nnsight, W&B, HF Spaces) are stamped LAUNCHED or CLOSED.
5. Session 4: §3 and §6 are prose, every paragraph citing a source file; `make paper`
   compiles with zero errors.
6. Session 5: the SAE sanity result — or its declared bound — exists with a note.
7. Session 7: full-tree mypy ≤ 150 and one more module on the blocking allowlist; the
   graduation proof exists; the release rehearsal transcript is complete.
8. Session 8: whichever lanes fired, a verifiable artifact exists and a ledger row names
   it; `verify-claims` is at zero unexpected; the PR merges on green; the release date
   is kept — the phase ends on it whether every lane ran or closed.

## 7. Showcase note (for the portfolio reader)

This is the record of the *consumption* of the planning arc: where MP-20 executed, this
phase converts the release into the publication. The paper stops being a `% TODO`
scaffold and becomes a first draft whose every number is one manifest away from a file
on disk; the five gate boxes that sat `[~]` for phases each end as a dated decision; and
the graduation question — "how does your transformer implement modular addition?" — is
asked of the actual record and answered honestly, including where the record closes. The
showcase motto:

*"The release was consumed, the gates closed as dates, and the record was published —
the roadmap became the runnable story."*

## Links

- [[19_micro-phase-20-execution-arc]] — the roadmap this phase consumes; its Sessions
  0–9 and its release state are this phase's starting artifact.
- [[18_micro-phase-19-verdicts-to-publication]] — the deliverables this phase inherits;
  its four verdict-agnostic commitments are the paper's spine here.
- [[docs/adr/0001-verdict-closure-ledger]] — the artifact whose rows this phase consumes
  and extends; the public record of every decision.
- [[06_production_ai/proofs/reproducible-from-clean-clone]] — the gate proof whose
  transcripts Sessions 7 and 8 produce, now including the LaTeX compile.
- [[portfolio/RESULTS]] · [[portfolio/README]] · [[07_capstone/research-plan]] — the
  shelf this phase's release reconciles onto.
- [[04_nlp_and_transformers/notes/attribution-patching]] (new, S1) and
  [[05_llm_engineering/proofs/intervention-validity]] — the notes that absorb the new
  instrument and its falsifications.
- [[00_meta/02_skill-tree]] — the five gate rows this phase stamps; the graduation proof
  lands its Phase-7 line.
- [[03_progress-log]] — this phase's dated record, including the make-restore incident
  of Step 0.
