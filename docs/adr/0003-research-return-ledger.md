---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
status: accepted
created: 2026-08-09
---

# ADR-0003 — The Research-Return Ledger

## Status

Accepted. Created as the living home of the research table that
[[00_meta/22_micro-phase-23-the-research-return]] (Sessions 1–8) fills: one row
per research lane, each ending `LAUNCHED (date, verdict)` or
`CLOSED (date, one named reason)`.

## Context

Nine consecutive micro-phases (MP-14 through MP-22) pre-registered the same two
flagship runs — the P=113 grokking lane (×3 seeds, Colab GPU) and the
standard-scale induction-heads lane (fresh batches, supervised CPU) — and none
of them launched them. ADR-0001 made the *closure* decision mechanical; ADR-0002
made the *publication* decision mechanical. The third, oldest open front is the
research itself: rows that are pre-registered in prose forever are not rows at
all. This ADR makes the *experiment* decision mechanical under the same rule:
rows end `LAUNCHED`-with-a-verdict or `CLOSED`-with-one-reason, pre-registered
numbers written before the first launch, and a `"what would falsify this"`
column that exists before the data does (Gelman & Loken's
garden-of-forking-paths countermeasure, applied at the source).

## Decision

- One table, this file, owned by the vault, filled during Micro-Phase 23's
  sessions and maintained through its release.
- Row states are strictly: `LAUNCHED` (with date + window + heartbeat artifact +
  verdict) or `CLOSED` (with date + one named reason). No "awaiting", no
  "pending", no reference without a date.
- The session gate is the same as ADR-0001: a session is not over while a row
  it is responsible for is undated; the phase's Session 8 requires zero undated
  rows.
- Verdict criteria are pre-registered: seeds, budgets, thresholds and success
  criteria are written into the row's cells **before** the run starts and are
  never edited afterwards; the only allowed post-launch edit is "observed".
- Closed-then-reopened is a NEW row, never a revision — the history is the
  audit (inherited from ADR-0002).
- Rows reopen from ADR-0001/ADR-0002 only under new dates and new windows, this
  phase's own.
- The row is the single source of truth the essay's annex, the paper's new
  sections and the skill-tree flips cite.

## Consequence

- No experiment enters the essay or the paper without a dated ledger row and a
  manifest on disk: the annex's numbers re-derive from `results/*.json` via
  `make verify-claims`, which this phase drives from 2 designed problems to 0.
- The negative is a result: a row that closes with a reason is stamped like a
  row that launched — the ledger's honesty is the essay's science.
- The next drift front of this repository is defined: a research row that says
  "awaiting window" a second phase in a row is drift in the ledger's own terms.

## The ledger (materially empty — filled in the phase's sessions)

| # | Research lane (source) | State | Date | Window / heartbeat | Verdict criteria (pre-registered) | What would falsify it |
|---|---|---|---|---|---|---|
| 1 | P=113 grokking, ×3 seeds, CPU-first via this machine's overnight budget (ADR-0003 row 1 frozen protocol; Colab GPU no longer load-bearing) (Rung 2 — primary flagship) | LAUNCHED | 2026-08-11 | Window: S1–S4 · heartbeat: checkpoint-every-500 + resume, `checkpoints/heartbeat.md` | Grok = val acc ≥ 0.95 sustained ≥ 5 checkpoints AND Fourier frequency count < P/2 sustained; generalization epoch reported | No grok by 5000 epochs with wd and cosine as pinned → microscope lane (row 2) |
| 2 | Fallback lane: the one-change microscope (≤ 3 single-variable trials, negative controls) | UNDECIDED | — | Window: S3 · ≤ 3 bullets: embedding re-norm · cosine schedule · my own third | Verdict = the trial that groks, or the dated negative with the trial results table | Third failed trial → row closes with one reason |
| 3 | R1 `--standard` fresh-batches, supervised CPU (domino for R4/R5) | UNDECIDED | — | Window: S1 start, ~17–24 h · heartbeat + every-500 checkpoints | Head formed = diag+1 mass > 0.3 on ≥ 1 head, sustained ≥ 5 checkpoints; seed count reported | No head at 0.3 within the run; the no-head negative is itself a result |
| 4 | R4 validation on a real head (activation + path patching) | UNDECIDED | — | Only after row 3's head exists | Self-patch = exact zero; corrupt-run diff > 0 on the real head | No row-3 head → scheduled negative written as the R4 result |
| 5 | R5 SAE re-run on the confirmed-head checkpoint | UNDECIDED | — | Only after row 3's head exists | L0 and FVE reported vs the no-head 53% baseline; honest delta either way | No row-3 head → scheduled negative |
| 6 | Paper: Grokking + Induction sections; essay annex v1.1 | UNDECIDED | — | S6–S7 | Every number manifest-tagged; `verify-claims` at 0 | Annex numbers without commands → struck with a reason |
| 7 | Graduation proof (capstone gate, `07_capstone`) | UNDECIDED | — | S6 | The Fourier + progress-measures + causal-ablation answer assembled — or closed with its dated reason | Verdict without a manifest |

Rule: a row enters `LAUNCHED` or `CLOSED` **in the same sitting** that decides
it; zero `UNDECIDED` rows at Session 8, and the story the essay's annex tells
is exactly the rows above, no more and no less.