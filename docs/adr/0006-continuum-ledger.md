---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
status: accepted
created: 2026-08-10
---

# ADR-0006 — The Continuum Ledger

## Status

Accepted. Created as the living home of the decision table that
[[00_meta/25_micro-phase-26-the-continuation]] (Sessions 0–8) fills: one row per
post-premiere decision, each ending `LAUNCHED (date, verdict)` or
`CLOSED (date, one named reason)`.

## Context

ADR-0001 made the *closure* decision mechanical, ADR-0002 the *publication*,
ADR-0003 the *experiment*, ADR-0004 the *horizon*, ADR-0005 the *premiere*.
The record now has an address and the capstone has a release; what the program
becomes after the premiere — which verdicts the executed horizon lanes convert
into artifacts, what the first new research question is, how the shelf is
maintained — is a decision set, and an undecided one is drift by another name.
This ADR makes the *continuum* decision mechanical under the same law: exactly
one new research question opens per phase, the rest of the candidate set closes
with one dated reason each, and maintenance is a dated row with a heartbeat,
never a mood.

## Decision

- One table, this file, owned by the vault, filled during Micro-Phase 26's
  sessions and maintained through its release; it is the single source of
  truth the essay annex, the paper's v2 diff, the site's health page and the
  skill-tree flips cite.
- Row states are strictly: `LAUNCHED` (with date + window + verdict/artifact)
  or `CLOSED` (with date + one named reason). No "awaiting", no "pending", no
  reference without a date.
- The session gate is the same as ADR-0001/0003/0004/0005: a session is not
  over while a row it is responsible for is undated; the phase's Session 8
  requires zero undated rows.
- **The continuum law**: exactly one new research row (row 3) opens per phase,
  chosen at Session 0 from the pre-registered candidate set below; the
  unchosen candidates close with one dated reason each, in the same sitting.
  Verdict criteria are written into the row's cells **before** the window
  opens and are never edited afterwards; the only allowed post-launch edit is
  "observed".
- ADR-0005's executed horizon rows are consumed here as NEW rows carrying
  MP-25's verdicts — the history is the audit (inherited); nothing is
  re-negotiated.
- Closed-then-reopened is a NEW row, never a revision (inherited).
- The stranger-review human-dependency rule (ADR-0004) extends to round 2: if
  the feedback intake does not happen within the window, the row closes with
  one reason and the recorded self-review substitute — never a silent skip.

## The candidate set for the first new research question (chosen at Session 0)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C1 | The P-sweep grokking scaling: P ∈ {59, 113, 227} at fixed budget, one change | Grokking grokked (ADR-0003 row 1 LAUNCHED) | Not grokked → the small-P story is already written as the negative |
| C2 | Induction scaling at fixed compute: heads × layers swept at standard scale | A real head exists (ADR-0003 row 3 LAUNCHED) | No head → the no-head negative is the result |
| C3 | Heterogeneous-feature superposition (Elhage et al. ch. 2–3: importance/frequency) | Always runnable on CPU | Row 3 already opened by another candidate → one question per phase |
| C4 | SAE monosemanticity on toy features (Bricken-style dictionary on the superposition model) | R5's delta from MP-23/25 warrants a retry | Delta thin → the dated memo says so |

## Consequence

- No post-premiere experiment begins without a dated ledger row and a
  pre-registered protocol: "let's see" is not a row (inherited).
- The capstone ends with a chosen program, not a trailing mood: at any release,
  the ledger states exactly which question is open, which closed with a reason,
  and which surface was maintained — the record compounds one number at a
  time.
- The next drift front of this repository is defined: a continuum row that
  says "awaiting window" a second phase in a row is drift in the ledger's own
  terms.

## The ledger (materially empty — filled in the phase's sessions)

| # | Continuum row (source) | State | Date | Window / heartbeat | Verdict criteria (pre-registered) | What would falsify it |
|---|---|---|---|---|---|---|
| 1 | Rung-6 artifact — consumes ADR-0005 row 7 (the ACDC pilot verdict) | UNDECIDED | — | S2 consume · S8 release | The pilot's verdict becomes the paper-v2 section (subgraph recovered) or the scheduled-negative trial table; every number manifest-tagged | A section written without the pilot's manifest → struck with a reason |
| 2 | Scaled-R1 artifact — consumes ADR-0005 row 8 | UNDECIDED | — | S5 paragraph · S8 release | The scale-up verdict's result paragraph from my log, or the no-head negative from MP-23's verdict | A paragraph number without a command → struck with a reason |
| 3 | The first new research question (the continuum row, candidate set above) | UNDECIDED | — | S5 pre-registration + launch · S6 verdict · heartbeat while the run is live | One candidate chosen at S0; protocol (site, metric, negative control, kill-date) written before the first pass; verdict or scheduled negative from the manifest | A run that starts without its pre-registration → row closes with one reason; the unchosen candidates close with reasons at S0 |
| 4 | The essay annex v2 — `portfolio/essay-annex-2.md` | UNDECIDED | — | S3 draft · S8 release | Distilled from the consumed rows; every number manifest-tagged; reverse claims audit at zero | An annex sentence without a manifest-tagged number → struck with a reason |
| 5 | The paper v2 diff | UNDECIDED | — | S2–S8 | Sections open only for manifests on disk; `make paper` compiles in the CI mirror | The PDF cites a number `verify-claims` cannot re-derive → the build fails loudly |
| 6 | The shelf maintenance — site + Space health, claims gate on every merge | UNDECIDED | — | S1 baseline · S7 rehearsal · S8 release | Hostile-webmaster walk at zero (links, assets, a11y, orphans); a live public number never exceeds the record | A live page number `verify-claims` cannot re-derive → the page is blocked, row blocked |
| 7 | The stranger round 2 — feedback from thread, site, Space | UNDECIDED | — | S4 intake · kill-date at S5 | Feedback-to-fixes matrix stamped: friction point → cause → dated fix → re-check row | No feedback within the window → row closes with the recorded self-review substitute |
| 8 | The standing gate debt — W&B, clean-clone proof, graduation proof, `reproduce-multiseed` exp2/exp5 | UNDECIDED | — | S1 stamping | Each cell ends LAUNCHED (with its transcript/artifact) or CLOSED (with one named reason) | A claimed closure without its transcript → the row stays open and blocks Session 8 |

Rule: a row enters `LAUNCHED` or `CLOSED` **in the same sitting** that decides
it; zero `UNDECIDED` rows at Session 8, and the story the program tells is
exactly the rows above, no more and no less.