---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
status: accepted
created: 2026-08-09
---

# ADR-0002 — The Public Arc Ledger

## Status

Accepted. Created as the living home of the publication table that
[[00_meta/21_micro-phase-22-the-public-arc]] (Session 1) must fill: one row per public
surface, each ending `LAUNCHED (date, URL)` or `CLOSED (date, one named reason)`.

## Context

The record — manifests, figures, a compiling paper, a verified superposition
transition — has never had an address. Six consecutive micro-phases pre-registered
verdicts; none published a word of prose to a public surface. The bottleneck is not
content (everything publication-ready is committed and provenance-guarded); the
bottleneck is *publication discipline*: a publishable result with no dated publication
row stays a private notebook forever. This ADR makes the publication decision
mechanical, under the same rule as ADR-0001: a row exists with exactly two legal
states — `LAUNCHED (date, URL/artifact)` or `CLOSED (date, one named reason)` — and no
third state.

## Decision

- One table, this file, owned by the vault, filled during Session 1 of Micro-Phase 22
  and maintained through the release.
- Row states are strictly: `LAUNCHED` (with date + working URL/artifact) or `CLOSED`
  (with date + one named reason). No "planned", no "TBD", no reference without a date.
- The gate is session-scoped: Session 6 of MP-22 is not over while any row is undated.
- Closed-then-reopened is a NEW row, never a revision — the history is the audit.
- The HF Space row reopens here as a NEW row scoped to CPU, whatever the MP-21 gate
  row decided; GPU-scoped lanes stay closed.
- The ledger row is the single source of truth the essay's "how far" sentence and the
  skill-tree publication rows cite.

## Consequence

- The essay's links are only as honest as this table: a public address that is not in
  a LAUNCHED row does not exist.
- The release is exactly the set of rows stamped `LAUNCHED` with dates — the roadmap
  is a document, this table is the artifact a reviewer opens to see that publishing
  was a sequence of decisions, not prose.
- The next drift front of the publication arc is defined: a row that says "planned" a
  second phase in a row is drift in the ledger's own terms.

## The ledger (filled in Session 1 — until then, materially empty)

| # | Public surface (source) | State | Date | URL / window | Heartbeat / artifacts |
|---|---|---|---|---|---|
| 1 | The essay — `portfolio/essay.md` (MP-22 S2–S3) | UNDECIDED | — | — | — |
| 2 | The thread — six-post arc (MP-22 S6) | UNDECIDED | — | — | — |
| 3 | The site — Quartz v4 on GitHub Pages (MP-22 S5) | UNDECIDED | — | — | — |
| 4 | The Space — CPU Superposition Explorer (MP-22 S4; reopens as NEW row) | UNDECIDED | — | — | — |
| 5 | The walkthrough — clean-clone-to-release transcript (MP-22 S7) | UNDECIDED | — | — | — |

Rule: a row enters `LAUNCHED` or `CLOSED` **in the same sitting** that decides it; an
`UNDECIDED` state after the Session-1 gate is a failed gate — and the ledger rows with
dates are the release's receipt.