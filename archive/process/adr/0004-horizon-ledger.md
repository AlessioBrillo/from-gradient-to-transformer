---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
status: accepted
created: 2026-08-09
---

# ADR-0004 — The Horizon Ledger

## Status

Accepted. Created as the living home of the decision table that
[[00_meta/23_micro-phase-24-the-synthesis]] (Sessions 0–8) fills: one row per
post-capstone decision, each ending `LAUNCHED (date, verdict)` or
`CLOSED (date, one named reason)`.

## Context

The capstone's scientific questions resolve during MP-23's sessions and their
public telling begins in MP-24. What the repository becomes *after* the
verdicts — new experiments (a real ACDC), a scale-up of Rung 1, an external
reader's review, a spoken explainer, or a deliberate stop — is a set of
decisions, and an undecided horizon is drift by another name. ADR-0001 made
the *closure* decision mechanical, ADR-0002 the *publication* decision,
ADR-0003 the *experiment* decision. This ADR makes the *horizon* decision
mechanical under the same rule: rows end `LAUNCHED`-with-a-verdict or
`CLOSED`-with-one-reason, criteria written before the window opens, and a
`"what would falsify it"` column that exists before the data does.

## Decision

- One table, this file, owned by the vault, filled during Micro-Phase 24's
  sessions and maintained through its release.
- Row states are strictly: `LAUNCHED` (with date + window + verdict) or
  `CLOSED` (with date + one named reason). No "awaiting", no "pending", no
  reference without a date.
- The session gate is the same as ADR-0001/0003: a session is not over while
  a row it is responsible for is undated; the phase's Session 8 requires
  zero undated rows.
- Verdict criteria are pre-registered: the window, the deliverable and the
  falsification condition are written into the row's cells **before** the
  window opens and are never edited afterwards; the only allowed
  post-launch edit is "observed".
- Closed-then-reopened is a NEW row, never a revision — the history is the
  audit (inherited from ADR-0002).
- The stranger-review row (row 2) carries a human-dependency rule: if no
  reader answers within the window, the row closes with one reason and the
  recorded self-review substitute — never a silent skip.
- The row is the single source of truth the portfolio README, the site and
  the skill-tree flips cite.

## Consequence

- No post-capstone experiment begins without a dated ledger row and a
  pre-registered protocol: "let's see" is not a row.
- The capstone ends with a dated decision set, not a trailing mood: every
  horizon row is stamped at MP-24's release, so the repository's next state
  is chosen, not inherited.
- The next drift front of this repository is defined: a horizon row that
  says "awaiting window" a second phase in a row is drift in the ledger's
  own terms.

## The ledger (materially empty — filled in the phase's sessions)

| # | Horizon row | State | Date | Window | Verdict criteria (pre-registered) | What would falsify it |
|---|---|---|---|---|---|---|
| 1 | Real ACDC pilot (Rung 6 resurrection, EAP lineage) | UNDECIDED | — | S7 pre-registration; execution beyond release | A pre-registered pilot (sites, metric, negative control, kill-date) that either recovers the target circuit or closes with the trial table | A pilot that starts without a pre-registration → row closes with one reason |
| 2 | The stranger review (first external reader of the paper) | UNDECIDED | — | S6 | The reader's top three friction points fixed with dates in the same sitting as the reading | No answer within the window → row closes with the recorded self-review substitute |
| 3 | Scaled-up R1 (beyond standard scale, conditioned on MP-23's head verdict) | UNDECIDED | — | Opens only on a head; else CLOSED with the no-head reason | A pre-registered scale-up protocol with budget, seeds and detection threshold | The no-head negative at standard scale → scheduled negative (row 3 closes with it) |
| 4 | The 10-minute talk (spoken explainer, scripted twice) | UNDECIDED | — | S7 | The from-memory draft filed beside the paper; the site hosts it | No script by Session 7 → the row closes with one reason |
| 5 | Stop-and-publish (the record releases as-is) | UNDECIDED | — | S8 | The paper, the site and the ledger land together on release day with zero undated rows | Any undated row at Session 8 → the release is blocked, and blocking is a dated reason |

Rule: a row enters `LAUNCHED` or `CLOSED` **in the same sitting** that decides
it; zero `UNDECIDED` rows at Session 8, and the story the portfolio tells is
exactly the rows above, no more and no less.