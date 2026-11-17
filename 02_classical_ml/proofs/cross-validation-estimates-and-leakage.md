---
tags: [type/proof, phase/2, state/review]
authorship: claude
created: 2026-11-17
---

# Proof: when cross-validation is an honest estimate, and why leakage breaks it

> **Authorship.** Written by Claude on 2026-11-17, not reconstructed from memory by the
> repository owner. Companion exercise:
> [[02_classical_ml/exercises/ex-05-metrics-cross-validation-and-leakage]]; the
> end-to-end pipeline is in [[02_classical_ml/proofs/complete-ml-pipeline]].

## Claim

K-fold cross-validation estimates a *procedure's* generalisation error only if the whole
procedure, every data-dependent step included, is refit inside each training fold. A step
fit on all the data, a feature selector for example, makes the estimate optimistic, and
the optimism can be arbitrarily large.

## Proof

**What the estimate is.** For fold `i`, let `A(D_train^i)` be the model produced by the
procedure `A` on the training rows, and `L_i` its error on the held-out rows `D_val^i`.
The cross-validation estimate is `mean_i L_i`. Because `D_val^i` plays no part in
producing `A(D_train^i)`, `L_i` is an unbiased estimate of that model's error on new
data, and the mean estimates the error of the *procedure* (up to the small bias of using
`(K-1)/K` of the data).

**Where the argument breaks.** Suppose a step `S` chooses the 20 features most
correlated with the label and is run on the whole of `D` before splitting. Then the
model in fold `i` depends on `D_val^i` through `S`, and `L_i` is no longer a held-out
error: the held-out labels have already influenced which features the model sees.

**Why the damage is large here.** With `p = 2000` independent noise features and `n =
50` samples, the sample correlation of each feature with the label is about `N(0, 1/n)`.
The largest of 2000 such values is bounded by about `sqrt(2 ln 2000 / 50)`, 0.55, and sits near 0.49 in practice; the 20th largest is near 0.36. So the chosen features correlate with the label at roughly 0.36 to 0.49 *by chance alone*, and they do so on every row, validation rows included. A classifier built on them looks
accurate on rows whose labels chose them. The exercise measures 0.959 mean accuracy
against a true 0.5.

**Why the fix works.** Selecting inside each training fold re-establishes the independence
in the first paragraph: `S` sees only `D_train^i`, so the chosen features are noise
relative to `D_val^i`, and the estimate returns to 0.479 (a mean over 20 seeds whose
range, 0.32 to 0.64, shows how noisy a 10-row fold is).

## Consequences

- Every data-dependent preprocessing step belongs inside the fold: imputation, scaling,
  feature selection, target encoding, dimensionality reduction.
- A very high score on a problem with many features and few samples is a reason to look
  for a leak before celebrating.
- Cross-validation on a leaked pipeline can rank models *wrongly*, not just score them
  too high, because models that exploit the leak the most win.

## What is backed here

The 0.959 and 0.479 are measured by `tests/test_leakage.py`'s helper over 20 seeds. The
extreme-value estimate in the third paragraph is a back-of-envelope bound, not a test.
Scaling and imputation leakage, which is usually milder, is not measured here.

## Outcome

- [x] Argument written; the central effect reproduced by a test.
- [ ] Reconstructed from memory by the repository owner. Not done.
