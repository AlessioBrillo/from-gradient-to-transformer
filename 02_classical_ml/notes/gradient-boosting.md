---
tags: [type/lesson, phase/2, state/review]
---

# Gradient Boosting

## Core idea
Sequential ensemble: each new tree corrects the **residuals** of the previous ensemble. Unlike bagging (parallel independent trees), boosting is additive and greedy.

- **Weak learner**: shallow tree (stump or depth 2–5)
- **Loss**: squared error → fit residuals; logistic → fit pseudo-residuals (gradient of log loss)
- **Shrinkage**: scale each tree by learning rate η < 1 — reduces overfit, needs more trees

## Algorithm sketch
```
F_0(x) = argmin_γ Σ L(y_i, γ)
for m = 1..M:
  r_im = -[∂L(y_i, F(x_i)) / ∂F(x_i)]      ← gradients (pseudo-residuals)
  fit tree h_m on {(x_i, r_im)}
  ρ_m = line search (or fixed η)
  F_m(x) = F_{m-1}(x) + η · h_m(x)
```

## XGBoost innovations
- **Second-order** Taylor expansion of loss (Newton boosting)
- **Regularized** objective: γT + ½λΣwⱼ² (T = leaves)
- **Column/row subsampling** (like RF)
- Built-in missing-value handling, quantile-based split finding

## LightGBM
- **GOSS**: Gradient-based One-Side Sampling — keep large-gradient instances, randomly sample small-gradient ones
- **EFB**: Exclusive Feature Bundling — one-hot features rarely co-occur → bundle into one
- Histogram-based splits (discretize continuous → 256 bins) — much faster

## MI forward link
Gradient boosting's additive correction of residuals parallels how attention heads iteratively refine representations: each head corrects the residual stream, and the ensemble of heads across layers builds up the final prediction. The "shallow trees + shrinkage" pattern maps to "shallow attention heads + layer norm scaling."

## References
- Friedman, *Greedy Function Approximation: A Gradient Boosting Machine* (2001)
- Chen & Guestrin, *XGBoost* (KDD 2016)
- Ke et al., *LightGBM* (NIPS 2017)
