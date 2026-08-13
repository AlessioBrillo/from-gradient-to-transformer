---
tags: [type/lesson, phase/7, research/experiment, state/review]
created: 2026-08-12
---

# Positive-Control Protocol — does this harness ever go sparse?

## The question

The record holds NO-GROK at P=113 (k_99 = 111/113, val 1.0) and, before that,
dense 59/59 Fourier mass in the P=59 probe drills (MP-27). No run in this
repository's history has ever produced k_99 < P/2. Before the microscope lane
spends its three-trial budget on P=113, the harness itself must be cleared:
**does this codebase ever produce a sparse Fourier solution, at any P, under
any single change?**

A negative that cannot be produced by a positive control in the same harness
is a negative about the harness, not about the phenomenon. The ladder of
attribution — harness → protocol → phenomenon — means the verdict on the
pipeline is dated before any trial is spent.

## The protocol (pre-registered, Session 0, 2026-08-12)

- **Scan**: P = 59, 67, 97 — one seed each. The frozen ADR-0003 row-1 protocol
  (wd=1.0, cosine schedule, 30% train, batch 512, d_model=128, d_mlp=512,
  4 heads, normalize_embeddings=True) minus exactly one variable: the
  renormalization is turned OFF (`--no-normalize-embeddings`), because it is
  the first named suspect and the control must change exactly one thing.
- **Budget**: 2000 epochs per P, checkpoint-every-200, kill condition signed
  before launch — any run past 2000 without k_99 dropping closes as observed,
  not as failed.
- **Threshold**: sparse = k_99 < P/2 sustained across ≥ 3 consecutive
  checkpoints (the frozen ADR-0003 row-1 definition, applied at small P).
- **What would falsify the harness**: the scan comes back all-dense. The
  reading then is code-path root-cause: the renormalization/loss/schedule
  chain read as code, with each suspect's mechanism written down before any
  further run.
- **Decision tree**:
  - Any P goes sparse → the harness is cleared at small P; the microscope
    trial order at P=113 is re-confirmed (or re-ordered with a one-line
    justification).
  - All dense → harness-level negative; the phase pivots to the root-cause
    diagnosis and no P=113 trial is worth its wall time until a sparse
    config exists anywhere in the harness.
  - Borderline (k_99 hovering at P/2) → the scan widens by one seed per P
    before any claim; a borderline is a measurement problem, not a verdict.

## Why a control is not a trial

The scan changes P, not the experiment's intent — it is a property check of
the pipeline under the frozen protocol, and it does not consume any of the
three trial slots the ledger allows the microscope lane. The control's own
prediction is pre-registered here too: **the renormalization is the most
likely suppressor of the sparse solution** (unit-norm rows are a nonlinear
constraint that distorts the low-norm Fourier structure Nanda et al.'s
solution needs), so the control is expected to go sparse at least at P=59. If
it does not, the root-cause reading starts with the weight decay × cosine
interaction, not with renormalization.

## The dated verdict lives here

- [x] Control verdict (P=59/67/97 scan) — **ALL-DENSE, harness-level negative**,
  2026-08-13. P=59: val 0.0000, gen −1, k_99 = 59/59. P=67: val 0.0006, gen −1,
  k_99 = 67/67. P=97: val 0.0002, gen −1, k_99 = 96/97. 2000 epochs, frozen
  protocol minus renormalization, one seed each (logs
  `checkpoints/control_p{59,67,97}.err.log`, 15:17–15:31 local). The
  pre-registered prediction ("expected to go sparse at least at P=59") is
  falsified. Two facts compound the negative: no run went sparse, AND none
  even reached the dense-generalizing regime (val ≈ 0 at every small P,
  matching the pre-frozen-protocol P=59 drills — the only generalizing runs
  in this repository's history remain the P=113 trio, always dense, val 1.0).
- [x] If all-dense: root-cause reading — the weight decay × cosine-schedule
  interaction, NOT renormalization (2026-08-13; the control's own
  pre-registered fallback). Trial 1 (`--no-normalize-embeddings`) is already
  FALSIFIED at P=113, consistent with this reading. The pivot is executed as:
  the phase's trials 2–3 ARE the root-cause instruments (constant LR =
  schedule half of the interaction; wd 1.5× = decay half), at P=113 — the
  only P where the harness generalizes, hence the only lane where a change
  can be observed to matter. Trial order re-confirmed with that one-line
  justification; the trial table's budget (≤ 3) is untouched. Reference:
  [[06_production_ai/notes/microscope-trial-table]].

## Links

- [[00_meta/28_micro-phase-29-the-positive-negative]] — the roadmap that
  pre-registered this protocol (Session 0–1).
- [[06_production_ai/notes/grokking-verdict-p113]] — the NO-GROK verdict this
  control exists to attribute.
- [[docs/adr/0003-research-return-ledger]] — the frozen protocol the scan
  inherits; row 2's trial budget it does not consume.
- [[06_production_ai/notes/microscope-trial-table]] — the trials the control
  gates.
