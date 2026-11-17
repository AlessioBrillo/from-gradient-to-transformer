---
tags: [type/exercise, phase/2, state/review]
authorship: claude
created: 2026-11-17
---

# Exercise 05 — Metrics by hand, cross-validation, and leakage you can measure

> **Authorship.** Written by Claude on 2026-11-17 to close a gap the vault's own rule
> exposed (see [[00_meta/02_skill-tree]]). The code and tests are real; this is not the
> repository owner's own solution.

## Goal / skill it demonstrates

Compute the classification metrics from their definitions, cross-validate correctly,
and *see* data leakage inflate a score rather than only read about it.

## Task

1. Verify precision, recall, F1 and accuracy against a hand-built confusion matrix.
2. Show where accuracy misleads (class imbalance) and what ROC-AUC does with ties.
3. Make k-fold cross-validation reproducible.
4. Reproduce the leakage of Hastie, Tibshirani & Friedman (ESL, §7.10.2): on labels
   that are pure noise, select features before cross-validating and watch the score
   rise far above chance.

## Solution

Code: `src/evaluation/metrics.py`, `src/evaluation/leakage.py`. Tests:
`tests/test_leakage.py`, `tests/test_metrics.py`.

**Metrics.** Ten samples, four positives; the classifier finds three and raises one
false alarm: accuracy 0.8, precision 0.75, recall 0.75, F1 0.75, all asserted. A
classifier that always answers "negative" on a 1%-positive set scores accuracy 0.99
and recall 0.0.

**Leakage.** 50 samples, 2000 Gaussian features, random binary labels, nearest-centroid
classifier, 5-fold cross-validation, the 20 features most correlated with the label.
The truth is 0.5. Over 20 seeds:

| Where the feature selection happens | Mean CV accuracy | Range |
|---|---|---|
| on all the data, before splitting (leaks) | **0.959** | 0.90 to 1.00 |
| inside each training fold (correct) | **0.479** | 0.32 to 0.64 |

The leaky pipeline "discovers" an almost perfect classifier of noise. Nothing in the
code looks wrong: every fold trains on its training rows and is scored on its held-out
rows. The leak is that the *selection* already used the held-out labels.

## Two defects this exercise found

- **`roc_auc_score` mishandled tied scores.** It emitted one ROC point per sample, so
  tied scores were ranked in whatever order they appeared: a constant scorer got AUC
  1.0 or 0.0 depending on the label order, instead of 0.5. Fixed to emit a point only
  where the threshold changes. No experiment uses it, so no published number moves.
- **`cross_val_score` could not be made reproducible.** It shuffled with numpy's global
  RNG. It now takes an optional `seed`. It is still not stratified, which is noted in
  its docstring rather than changed.

## Linked skill

- [[00_meta/02_skill-tree]] → Cross-validation + correct metrics; data leakage
- Proof: [[02_classical_ml/proofs/cross-validation-estimates-and-leakage]]
