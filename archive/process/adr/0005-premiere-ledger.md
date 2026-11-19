---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
status: accepted
created: 2026-08-10
---

# ADR-0005 — The Premiere Ledger

## Status

Accepted. Created as the living home of the public-release table that
[[00_meta/24_micro-phase-25-the-premiere]] (Sessions 0–8) fills: one row per
public surface and per executed horizon lane, each ending
`LAUNCHED (date, URL)` or `CLOSED (date, one named reason)`.

## Context

ADR-0001 made the *closure* decision mechanical, ADR-0002 the *publication*
decision, ADR-0003 the *experiment* decision, ADR-0004 the *horizon* decision.
The record still has no address: MP-22 pre-registered the public arc and none
of its rows ever launched — the essay, thread, site, Space and walkthrough
exist nowhere on disk or the web. ADR-0002's rows were never filled because
the phase that owned them never executed; they reopen here as NEW rows under
MP-25's own dates, windows and kill-dates, with the added rule the science
already learned: nothing launches before its artifact and its manifest exist.
This ADR makes the *premiere* decision mechanical under the same law — a row
ends `LAUNCHED`-with-a-URL or `CLOSED`-with-one-reason, and a surface with no
artifact merged on disk is not a surface at all.

## Decision

- One table, this file, owned by the vault, filled during Micro-Phase 25's
  sessions and maintained through its release; it is the single source of
  truth the site's footer, the essay's "how far" sentence and the skill-tree
  publication rows cite.
- Row states are strictly: `LAUNCHED` (with date + working URL/artifact) or
  `CLOSED` (with date + one named reason). No "awaiting", no "pending", no
  reference without a date.
- The session gate is the same as ADR-0001/0003/0004: a session is not over
  while a row it is responsible for is undated; the phase's Session 8
  requires zero undated rows.
- The same-sitting rule: a row enters `LAUNCHED` **in the same sitting** that
  merges its artifact and stamps its URL — a plan with a date is a promise by
  another name. The premiere drill (S1, S7) precedes every real launch.
- The manifest rule extends to the web: no public page cites a number the
  claims gate (`make verify-claims`) cannot re-derive; the site build runs
  the gate in the local CI mirror.
- ADR-0002's five surfaces reopen here as NEW rows — the history is the audit
  (inherited). ADR-0004's rows are consumed as decided, never re-negotiated:
  they enter MP-25 with their verdicts and get their execution here.
- Closed-then-reopened is a NEW row, never a revision (inherited).
- The stranger-review human dependency rule (ADR-0004) extends to the revision
  cycle: if the re-read does not happen within the window, the row closes with
  one reason and the recorded self-review substitute — never a silent skip.

## Consequence

- No public surface exists without a dated ledger row and an artifact on disk:
  the URL is the receipt, and the release is exactly the set of rows stamped
  `LAUNCHED` with dates.
- The capstone's public premiere is a sequence of decisions, not prose: a
  reviewer opens this table to see that publishing was dated work, exactly
  like the science before it.
- The next drift front of this repository is defined: a premiere row that
  says "awaiting window" a second phase in a row is drift in the ledger's own
  terms.

## The ledger (materially empty — filled in the phase's sessions)

| # | Premiere lane (source) | State | Date | URL / window | Verdict criteria (pre-registered) | What would falsify it |
|---|---|---|---|---|---|---|
| 1 | The essay — `portfolio/essay.md` (reopens ADR-0002 row 1 as NEW) | UNDECIDED | — | S3 draft · S8 launch | Every number manifest-tagged; reverse claims audit at zero | An essay sentence without a manifest-tagged number → struck with a reason |
| 2 | The thread — six-post arc (reopens ADR-0002 row 2 as NEW) | UNDECIDED | — | S6 draft ×3 · S8 launch | Each post cites its manifest; three drafts, the second and third the real ones | A post citing a number the claims gate cannot re-derive → post struck, row closed with the reason |
| 3 | The site — Quartz v4 on GitHub Pages (reopens ADR-0002 row 3 as NEW) | UNDECIDED | — | S1 pin + smoke · S7 rehearsal · S8 live | Build runs the claims gate in the mirror; hostile-webmaster audit at zero | A public number `verify-claims` cannot re-derive → build fails loudly, row blocked |
| 4 | The Space — CPU Superposition Explorer, Gradio (reopens ADR-0002 row 4 as NEW) | UNDECIDED | — | S6 rebuild · S8 launch | Rung 3 engine behind the demo; engine health check live | Demo without the verified engine → row closes with one reason |
| 5 | The walkthrough — clean-clone-to-release transcript (reopens ADR-0002 row 5 as NEW) | UNDECIDED | — | S7 rehearsal · S8 transcript | One command line: clone → sync → suite → verify-claims → paper → site | Any step unexecuted in the transcript → the row closes with that step's reason |
| 6 | The revision cycle (consumes ADR-0004 row 2's stranger notes) | UNDECIDED | — | S3 fixes · S3 re-read | Three friction points → three dated fixes → re-read row stamped same sitting | No re-read within the window → row closes with the self-review substitute |
| 7 | The ACDC pilot execution (consumes ADR-0004 row 1) | UNDECIDED | — | Pre-registration S2 · run S5 | Pre-registered protocol (edges, metric, negative control, kill-date); subgraph recovered or trial table | Pilot starting without its pre-registration → row closes with one reason |
| 8 | The scaled-up R1 execution (consumes ADR-0004 row 3) | UNDECIDED | — | Decided S5 · opens only on a head | Pre-registered scale-up protocol; or the scheduled no-head negative from MP-23's verdict | Scale-up without a protocol → row closes, the negative is the result |

Rule: a row enters `LAUNCHED` or `CLOSED` **in the same sitting** that decides
it; zero `UNDECIDED` rows at Session 8, and the story the premiere tells is
exactly the rows above, no more and no less.