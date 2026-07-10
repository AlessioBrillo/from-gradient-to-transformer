# Exercise 04 — Gradient Boosting and Naive Bayes

## Objective
Implement gradient boosting manually, train XGBoost/LightGBM, and compare against Naive Bayes on text data. Understand when each method works and why.

## Setup
Use sklearn datasets: `fetch_20newsgroups` (text) for Naive Bayes, and a regression dataset (e.g., California housing) for gradient boosting.

## Tasks

### 1. Naive Bayes from math
Using `sklearn.naive_bayes`, train MultinomialNB and BernoulliNB on 20 Newsgroups:
- Compare accuracy, precision, recall
- Which variant works better? Why?
- Inspect `feature_log_prob_` — what do the most indicative words per class look like?

### 2. Gradient Boosting from scratch
Implement a simple gradient booster on a regression problem:
- Start with mean prediction F₀
- For M = 100 rounds:
  - Compute residuals r_i = y_i − F(x_i)
  - Fit a shallow decision tree (max_depth=3) to residuals
  - F(x) += η · tree(x)  (η = 0.1)
- Plot train/test RMSE vs M

### 3. Compare with XGBoost/LightGBM
Train `xgboost.XGBRegressor` and/or `lightgbm.LGBMRegressor` on the same data:
- Compare RMSE, training time, tree count
- Plot feature importance; compare between manual and library versions

### 4. Bias-variance analysis
For gradient boosting:
- Vary η ∈ {0.01, 0.1, 0.5} — how does learning rate affect optimal tree count?
- Vary max_depth ∈ {2, 4, 8} — when does deep boosting overfit?

### MI Forward Link
Write 2-3 sentences on how gradient boosting's residual correction parallels the iterative refinement of attention head outputs in the residual stream.
