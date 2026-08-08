---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
status: accepted
created: 2026-08-08
---

# ADR-0001 — The Verdict Closure Ledger

## Status

Accepted. Created as the living home of the closure table that
[[00_meta/16_micro-phase-17-closure-and-release]] (Step 1) and
[[00_meta/17_micro-phase-18-verdict-window]] (Session 1) must fill.

## Context

Five consecutive micro-phases (MP-13 through MP-17) pre-registered the same two
flagship runs — R1 `--standard` induction-heads (~17–20 h supervised CPU) and P=113
grokking ×3 seeds (Colab GPU) — and none of them launched anything. The bottleneck was
not instrumentation (MP-10/11 finished the CPU-side de-risking; everything the runs
need is pinned and provenance-guarded). The bottleneck is *launch discipline*: a
deferral that is written in prose can be repeated forever without ever being a
decision. This ADR makes the decision mechanical: every open item exists as a **row**
with exactly two legal states — `launched (date, window, heartbeat)` or
`closed (date, one named reason)` — where `closed-not-verified` is one of the legal
reasons. A row in any other state is a lie in the ledger's own terms and is flagged
as drift.

## Decision

- One table, this file, owned by the vault, filled during Session 1 of Micro-Phase 18
  (the closure session) and maintained through the release.
- Row states are strictly: `LAUNCHED` (with date + supervised window + heartbeat
  artifact) or `CLOSED` (with date + one named reason). No "awaiting", no "TBD",
  no reference without a date.
- The gate is session-scoped: the closure session is not over while any row is
  undated.
- Closure re-scopes `make verify-claims`' expected set: a struck claim is a decision
  visible in this file, never a silent absence.
- The ledger outlives the phase: it remains the public record of what was real, what
  was deferred — and what was decided.

## Consequence

- Merges pass `verify-claims` with an explicit expected-set re-scoped by this file —
  no fabricated manifests, no dangling claims.
- The roadmap itself is a document; this table is the artifact a reviewer can open to
  see that waiting was a *decision*, not drift.
- The ledger outlives the phase: at release time the roadmap is archived, but the
  public record remains a table, not a narrative.
- The next drift front of this repository is defined: a row that says "awaiting
  window" a second phase in a row is drift in the ledger's own terms.

## The ledger (filled in Session 1 — until then, materially empty)

| # | Open item (source) | State | Date | Window / reason | Heartbeat / artifacts |
|---|---|---|---|---|---|
| 1 | R1 `--standard` supervised run — the domino for R4, R5, paper §5–7 (MP-13..17) | UNDECIDED | — | — | — |
| 2 | P=113 ×3 seeds grokking run via Colab notebook (MP-13..17) | UNDECIDED | — | — | — |
| 3 | P=113 fallback lane: budgeted CPU alternative or written closure (MP-17 §6d) | UNDECIDED | — | — | — |
| 4 | R3 full-scale geometry re-run under watchdog (MP-17 S2) | UNDECIDED | — | — | — |
| 5 | Clean-clone dry run transcript (MP-17 S2) | UNDECIDED | — | — | — |
| 6 | Paper spine: Related Work, Methods, Superposition, Limitations prose (MP-17 S4) | UNDECIDED | — | — | — |
| 7 | Full-tree mypy de-drift 171 → ≤160 + new blocking module (MP-17 S5) | UNDECIDED | — | — | — |
| 8 | Model card rewrite vs the multi-seed harness (MP-17 S7) | UNDECIDED | — | — | — |
| 9 | Verdict lanes 6a/6b/6c/6d — whichever fires, an artifact must exist (MP-17 S6) | UNDECIDED | — | — | — |
| 10 | Release rehearsal on a branch (MP-17 Challenge 11) | UNDECIDED | — | — | — |

Rule: a row enters `LAUNCHED` or `CLOSED` **in the same sitting** that decides it; an
`UNDECIDED` state after the Session-1 gate is a failed gate.