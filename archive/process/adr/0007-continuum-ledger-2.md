---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
status: accepted
created: 2026-08-13
---

# ADR-0007 — The Second Continuum Ledger

## Status

Accepted. Created as the living home of the decision table that
[[00_meta/32_micro-phase-33-the-second-question]] (Sessions 0–8) fills: one row
per post-premiere decision, each ending `LAUNCHED (date, verdict)` or
`CLOSED (date, one named reason)`.

## Context

ADR-0006 made the *continuum* decision mechanical and MP-32 executed it for the
first time: exactly one new research question opened from the frozen candidate
set C1–C4, the unchosen candidates closed with one dated reason each, and the
shelf, the annex, the paper diff and the stranger pipeline ran as dated rows.
ADR-0006 is full and closed at MP-32's release; closed-then-reopened is a NEW
row, never a revision (inherited). What the program becomes after its first
executed continuum — the second research question, the teaching of the record,
the third stranger round, the shelf's second year — is a decision set, and an
undecided one is drift by another name. This ADR makes the second execution
mechanical under the same law: exactly one new research question opens per
phase, the rest of the candidate set closes with one dated reason each, and
the record teaches as a dated row with a runnable receipt, never a mood.

## Decision

- One table, this file, owned by the vault, filled during Micro-Phase 33's
  sessions and maintained through its release; it is the single source of
  truth the essay annex v3, the paper v3 diff, the site's health page and the
  skill-tree flips cite.
- Row states are strictly: `LAUNCHED` (with date + window + verdict/artifact)
  or `CLOSED` (with date + one named reason). No "awaiting", no "pending", no
  reference without a date.
- The session gate is the same as ADR-0001/0003/0004/0005/0006: a session is
  not over while a row it is responsible for is undated; the phase's Session 8
  requires zero undated rows.
- **The continuum law, second execution**: exactly one new research row
  (row 3) opens per phase, chosen at Session 0 from the pre-registered
  candidate set C5–C8 below; the unchosen candidates close with one dated
  reason each, in the same sitting. Verdict criteria are written into the
  row's cells **before** the window opens and are never edited afterwards;
  the only allowed post-launch edit is "observed".
- ADR-0006's executed rows are consumed here as NEW rows carrying MP-32's
  verdicts — the history is the audit (inherited); nothing is re-negotiated.
- Closed-then-reopened is a NEW row, never a revision (inherited).
- The stranger-review human-dependency rule (ADR-0004) extends to round 3: if
  the feedback intake does not happen within the window, the row closes with
  one reason and the recorded self-review substitute — never a silent skip.
- The standing-debt rule is re-verification, never re-doing: a stamped
  closure is re-checked with its transcript; a genuinely new debt cell is a
  NEW row, never a revision.

## The candidate set for the second research question (chosen at Session 0)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C5 | The weight-decay frontier at P=113: wd ∈ {0.5, 1.5, 2.0, 3.0}, one seed each, frozen protocol, checkpoint-every-500 (the microscope's successor — the record's deepest open question: does ANY config in this harness produce k_99 < P/2?) | ADR-0003 row 2 closes negative (the ≤ 3 trials exhausted) — the most likely state | A trial groks sparsely → the question is answered by the ledger, closed with that verdict |
| C6 | The head-formation floor: R1 scale-up at d_model ∈ {128, 256} at fixed compute (Olsson's formation-floor question, the no-head negative's successor) | ADR-0003 row 3 closes NO-HEAD | A head formed → the question is answered, closed with that verdict |
| C7 | SAE on the dense residual stream as a research row (MP-29 S3's prediction: "sparse autoencoders struggle exactly where the circuit is dense" — L0/FVE/dead-features on the P=113 dense stream vs. synthetic + any sparse solution found) | Always runnable on CPU — the checkpoints exist on disk | Row 3 already opened by another candidate → one question per phase |
| C8 | The ACDC/EAP successor: attribution-scale circuit recovery on the capstone model's confirmed circuits (the Rung-6 line, scaled) | ADR-0005 row 7's pilot recovered a subgraph | The pilot's scheduled negative → the Rung-6 artifact is the trial table, this closes with that verdict |

## Consequence

- No post-premiere experiment begins without a dated ledger row and a
  pre-registered protocol: "let's see" is not a row (inherited).
- The record teaches: the teaching lane (row 7) ships one public artifact a
  stranger can run, with the run-transcript as its receipt — the capstone's
  showcase compounds a runnable claim, not just a readable one.
- The capstone ends with a chosen program, not a trailing mood: at any
  release, the ledger states exactly which question is open, which closed with
  a reason, and which surface was maintained — the record compounds one number
  at a time (inherited).
- The next drift front of this repository is defined: a continuum row that
  says "awaiting window" a second phase in a row is drift in the ledger's own
  terms (inherited).

## The ledger (materially empty — filled in the phase's sessions)

| # | Continuum row (source) | State | Date | Window / heartbeat | Verdict criteria (pre-registered) | What would falsify it |
|---|---|---|---|---|---|---|
| 1 | The first research question consumed as artifact — consumes ADR-0006 row 3's verdict | UNDECIDED | — | S2 consume · S8 release | The executed question's verdict (or its scheduled negative) becomes the paper-v3 section, the annex table or the results-page row; every number manifest-tagged | An artifact written without the verdict's manifest → struck with a reason |
| 2 | The paper v3 rule | UNDECIDED | — | S2 decide · S8 release | v3 opens only if row 1 lands new numbers; else the row closes with the dated reason "the v2 is the record" and `make paper` re-verified green in the CI mirror against v2 | A v3 section without a new manifest → the build fails loudly |
| 3 | The second research question (the continuum row, candidate set C5–C8 above) | UNDECIDED | — | S5 pre-registration + launch · S6 verdict · heartbeat while the run is live | One candidate chosen at S0; protocol (site, metric, negative control, kill-date) written before the first pass; verdict or scheduled negative from the manifest | A run that starts without its pre-registration → row closes with one reason; the unchosen candidates close with reasons at S0 |
| 4 | The essay annex v3 — `portfolio/essay-annex-3.md` | UNDECIDED | — | S3 draft · S8 release | Distilled from the consumed rows; every number manifest-tagged; reverse claims audit at zero | An annex sentence without a manifest-tagged number → struck with a reason |
| 5 | The shelf maintenance — site + Space health, claims gate on every merge | UNDECIDED | — | S1 baseline · S7 rehearsal · S8 release | Hostile-webmaster walk at zero (links, assets, a11y, orphans); a live public number never exceeds the record | A live page number `verify-claims` cannot re-derive → the page is blocked, row blocked |
| 6 | The stranger round 3 — feedback from thread, site, Space | UNDECIDED | — | S4 intake · kill-date at S5 | Feedback-to-fixes matrix stamped: friction point → cause → dated fix → re-check row | No feedback within the window → row closes with the recorded self-review substitute |
| 7 | The teaching lane — one public artifact a stranger can run (Colab grokking notebook / walkthrough v2 / 10-minute talk v2) | UNDECIDED | — | S5 kickoff · S7 ship · S8 release | The artifact runs end to end on a stranger's machine (fresh clone / Colab session); the run-transcript is the receipt | A shipped artifact without its run-transcript → the row stays open and blocks Session 8 |
| 8 | The standing debt re-verification — W&B, clean-clone proof, graduation proof, `reproduce-multiseed` exp2/exp5 | UNDECIDED | — | S1 stamping | Each cell re-verified LAUNCHED (with its transcript re-checked) or CLOSED (with one named reason); a claimed closure without its transcript stays open | A re-verified closure without its transcript → the row stays open and blocks Session 8 |

Rule: a row enters `LAUNCHED` or `CLOSED` **in the same sitting** that decides
it; zero `UNDECIDED` rows at Session 8, and the story the program tells is
exactly the rows above, no more and no less.