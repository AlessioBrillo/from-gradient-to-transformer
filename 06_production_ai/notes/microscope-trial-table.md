---
tags: [type/lesson, phase/7, research/experiment, state/review]
created: 2026-08-12
---

# Microscope Trial Table — ADR-0003 row 2, pre-registered predictions

The microscope lane exists because the P=113 verdict is NO-GROK: val 1.0 but
Fourier dense (k_99 = 111/113). Its job is to test the named suspects as
**one-change** trials against the frozen ADR-0003 row-1 protocol, each with a
prediction written before the run and a falsification column that exists
before the data does. Three trials maximum (the ledger's budget); the third
is chosen with a one-line justification when 1–2 land. Three failed trials
close the row with one dated reason: *the named suspects were tested and did
not rescue the run.*

Order and content were re-confirmed by the positive-control scan
([[06_production_ai/notes/positive-control-protocol]]) — the control gates
the trials, it does not consume the budget.

## Trial 1 — embedding re-normalization off

| Cell | Pre-registered content |
|---|---|
| Change | `--no-normalize-embeddings` (flag landed in MP-28; default behavior unchanged) |
| Mechanism hypothesis | Unit-norm rows are a nonlinear constraint applied in-place after every optimizer step (exp2 line ~428). It distorts the low-norm, phase-structured embedding rows the sparse Fourier circuit needs (Nanda et al. 2023), pushing the solution toward the dense regime |
| Prediction | k_99 drops below P/2 at P=113 within 5000 epochs, or val-1.0 with a measurably lower k_99 than the 111/113 baseline |
| What would falsify it | k_99 stays ≥ 111/113 at val 1.0 — renormalization is not the suppressor |
| Verdict | **FALSIFIED** 2026-08-13 (observed; manifest `<!-- manifest: exp2_grokking -->` re-derived same sitting): k_99 = 112/113 (≥ 111/113 — the dense solution persisted) and val 0.7176, gen epoch −1 — the run never reached val 1.0 and underperformed the baseline seed-0 (val 1.0 by epoch ~1250). Removing the constraint neither produced sparsity nor helped learning. **Renormalization is not the suppressor.** |

## Trial 2 — constant LR (cosine schedule off)

| Cell | Pre-registered content |
|---|---|
| Change | `--schedule constant` — a small recorded experiment-code change (exp2 currently hardcodes CosineAnnealingLR) |
| Mechanism hypothesis | The late-annealing decay never lets the low-norm sparse solution be reached; the dense solution is found in the regime where LR is still high, and the decay locks it in |
| Prediction | Constant LR groks sparsely (k_99 < P/2 sustained) within 5000 epochs, or val-1.0 with a clear k_99 improvement over baseline |
| What would falsify it | Dense at 5000 epochs under constant LR — the schedule interaction is not the suppressor |
| Verdict | — (date + manifest tag when observed) |

## Trial 3 — weight decay 1.5× (the norm-pressure hypothesis)

| Cell | Pre-registered content |
|---|---|
| Change | `--weight-decay 1.5` — chosen with this one-line justification at trials 1–2: if neither renormalization nor schedule rescues the run, the remaining named suspect is insufficient norm pressure (Gromov 2023's memory-perspective reading), and 1.5× is the smallest change that tests it |
| Mechanism hypothesis | Stronger decay forces the low-norm sparse solution into reach before the dense one settles |
| Prediction | k_99 < P/2 sustained, or a strictly lower k_99 than both trials 1–2 at matched epochs |
| What would falsify it | Dense at 1.5× — the row closes with one reason: the named suspects were tested and did not rescue the run |
| Verdict | — (date + manifest tag when observed) |

## The row's closure rules (ADR-0003, executed)

- A trial enters the table **in the same sitting** that decides it; the only
  post-launch edit is "observed".
- Any trial that groks sparsely re-opens row 1 as a NEW row under a new date
  and window (never a revision of the stamped one).
- Three failures close row 2 `CLOSED (date, named suspects tested, dense at
  P=113 under all three one-change trials)` — and the
  [[06_production_ai/notes/dense-solutions-modular-addition]] characterization
  becomes the phase's headline.

## Links

- [[docs/adr/0003-research-return-ledger]] — row 2, whose budget this table
  spends.
- [[06_production_ai/notes/grokking-verdict-p113]] — the verdict that names
  the suspects.
- [[06_production_ai/notes/positive-control-protocol]] — the gate before
  this table.
- [[00_meta/28_micro-phase-29-the-positive-negative]] — Session 2, the
  roadmap that executes it.
