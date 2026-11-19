---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
status: accepted
created: 2026-08-13
---

# ADR-0009 — The Fourth Continuum Ledger

## Status

Accepted. Created as the living home of the decision table that
[[00_meta/34_micro-phase-35-the-fourth-question]] (Sessions 0–8) fills: one row
per post-premiere decision, each ending `LAUNCHED (date, verdict)` or
`CLOSED (date, one named reason)`.

## Context

ADR-0008 made the continuum's third execution mechanical and MP-34 executes
it now: exactly one new research question opened from the frozen candidate
set C9–C12, the unchosen candidates close with one dated reason each, and the
shelf, the annex, the paper diff, the stranger pipeline and the teaching lane
run as dated rows. ADR-0008 is full and closed at MP-34's release;
closed-then-reopened is a NEW row, never a revision (inherited). What the
program becomes after its third executed continuum — the fourth research
question, the third runnable teaching artifact, the fifth stranger round, the
shelf's third year — is a decision set, and an undecided one is drift by
another name. This ADR makes the fourth execution mechanical under the same
law: exactly one new research question opens per phase, the rest of the
candidate set closes with one dated reason each, and the record's teaching
compounds as a dated row with a runnable receipt, never a mood.

## Decision

- One table, this file, owned by the vault, filled during Micro-Phase 35's
  sessions and maintained through its release; it is the single source of
  truth the essay annex v5, the paper v5 diff, the site's health page and the
  skill-tree flips cite.
- Row states are strictly: `LAUNCHED` (with date + window + verdict/artifact)
  or `CLOSED` (with date + one named reason). No "awaiting", no "pending", no
  reference without a date.
- The session gate is the same as ADR-0001/0003/0004/0005/0006/0007/0008: a
  session is not over while a row it is responsible for is undated; the
  phase's Session 8 requires zero undated rows.
- **The continuum law, fourth execution**: exactly one new research row
  (row 3) opens per phase, chosen at Session 0 from the pre-registered
  candidate set C13–C16 below; the unchosen candidates close with one dated
  reason each, in the same sitting. Verdict criteria are written into the
  row's cells **before** the window opens and are never edited afterwards;
  the only allowed post-launch edit is "observed".
- ADR-0008's executed rows are consumed here as NEW rows carrying MP-34's
  verdicts — the history is the audit (inherited); nothing is re-negotiated.
- Closed-then-reopened is a NEW row, never a revision (inherited).
- The stranger-review human-dependency rule (ADR-0004) extends to round 5: if
  the feedback intake does not happen within the window, the row closes with
  one reason and the recorded self-review substitute — never a silent skip.
- The standing-debt rule is re-verification, never re-doing: a stamped
  closure is re-checked with its transcript; a genuinely new debt cell is a
  NEW row, never a revision. A pending item cannot outlive a ledger.

## The candidate set for the fourth research question (chosen at Session 0)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C13 | The dense algorithm, identified: whatever C10 decided, spell out the computation the dense solution actually performs — per-head Fourier dictionary → the function each head computes → QK/OV composition → why it generalizes (the C10 verdict becomes the framing: shortcut mechanism or alternative algorithm) | ADR-0008 row 3 lands (either verdict) | The record already answers it — MP-29 S3's characterization plus C10's theory note together spell out the computation; then this closes with "the record answers it," consumed as an artifact in the same sitting |
| C14 | The solution-regime phase diagram: a bounded wd × LR-schedule × embedding-norm sweep at P=113 (plus one small-P slice) mapping where the sparse / dense / memorized regimes live — the systematic successor to the microscope's three-trial budget, and the only candidate that converts the record's deepest open fact (no run ever produced k_99 < P/2) into a **mapped, dated answer** instead of a point negative | ADR-0003 row 2 closes with all three trials dense (the most likely state) | A sparse solution found anywhere in the sweep → the harness is cleared; the sweep becomes the positive's context and this row closes with that verdict |
| C15 | The head-formation floor at scale (C11's successor): R1 scale-up at d_model ∈ {128, 256} at fixed compute — Olsson's formation-floor question, the no-head negative's successor | ADR-0003 row 3 closes NO-HEAD | A head formed → the question is answered by the ledger, closed with that verdict |
| C16 | The induction-head portrait on a confirmed head (the Olah-style deep dive): QK/OV decomposition, K-composition, logit lens, head-role map — the payoff of the R4/R5 chain | ADR-0003 row 3 closes WITH a head | No head → the no-head negative is the Rung-1 artifact, this closes with that verdict |

## Consequence

- No post-premiere experiment begins without a dated ledger row and a
  pre-registered protocol: "let's see" is not a row (inherited).
- The record's teaching compounds a third time: the teaching lane (row 7)
  ships a third public artifact a stranger can run, with the run-transcript
  as its receipt — the showcase's story is "read it, run it, watch me be
  wrong on the record," three receipts deep.
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
| 1 | The third research question consumed as artifact — consumes ADR-0008 row 3's verdict | UNDECIDED | — | S2 consume · S8 release | The executed question's verdict (or its scheduled negative) becomes the paper-v5 section, the annex table or the results-page row; every number manifest-tagged | An artifact written without the verdict's manifest → struck with a reason |
| 2 | The paper v5 rule | UNDECIDED | — | S2 decide · S8 release | v5 opens only if row 1 lands new numbers; else the row closes with the dated reason "the v4 is the record" and `make paper` re-verified green in the CI mirror against v4 | A v5 section without a new manifest → the build fails loudly |
| 3 | The fourth research question (the continuum row, candidate set C13–C16 above) | UNDECIDED | — | S5 pre-registration + launch · S6 verdict · heartbeat while the run is live | One candidate chosen at S0; protocol (site, metric, negative control, kill-date) written before the first pass; verdict or scheduled negative from the manifest | A run that starts without its pre-registration → row closes with one reason; the unchosen candidates close with reasons at S0 |
| 4 | The essay annex v5 — `portfolio/essay-annex-5.md` | UNDECIDED | — | S3 draft · S8 release | Distilled from the consumed rows; every number manifest-tagged; reverse claims audit at zero | An annex sentence without a manifest-tagged number → struck with a reason |
| 5 | The shelf maintenance, year three — site + Space health, claims gate on every merge | UNDECIDED | — | S1 baseline · S7 rehearsal · S8 release | Hostile-webmaster walk at zero (links, assets, a11y, orphans); a live public number never exceeds the record | A live page number `verify-claims` cannot re-derive → the page is blocked, row blocked |
| 6 | The stranger round 5 — feedback from thread, site, Space | UNDECIDED | — | S4 intake · kill-date at S5 | Feedback-to-fixes matrix stamped: friction point → cause → dated fix → re-check row | No feedback within the window → row closes with the recorded self-review substitute |
| 7 | The teaching lane, round three — a third public artifact a stranger can run (walkthrough v3 / 10-minute talk v3) | UNDECIDED | — | S5 kickoff · S7 ship · S8 release | The artifact runs end to end on a stranger's machine (fresh clone / Colab session); the run-transcript is the receipt | A shipped artifact without its run-transcript → the row stays open and blocks Session 8 |
| 8 | The standing debt re-verification — W&B, clean-clone proof, graduation proof, `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch ×3-seed resolution (which ADR-0008 row 8 is obligated to date) | UNDECIDED | — | S1 stamping | Each cell re-verified LAUNCHED (with its transcript re-checked) or CLOSED (with one named reason); a claimed closure without its transcript stays open | A re-verified closure without its transcript → the row stays open and blocks Session 8 |

Rule: a row enters `LAUNCHED` or `CLOSED` **in the same sitting** that decides
it; zero `UNDECIDED` rows at Session 8, and the story the program tells is
exactly the rows above, no more and no less.