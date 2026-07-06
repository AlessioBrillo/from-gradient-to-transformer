---
tags: [type/lesson, phase/2]
state: review
created: 2026-07-05
---

# Linear Regression

## What it is
Models a scalar target y as a linear combination of features X: y = Xw + b. The simplest supervised learning model.

## Why it exists
It is the building block of all regression. The solution is interpretable (coefficients = feature weights), analytically tractable (closed-form via SVD), and extends naturally to regularization (Ridge, Lasso) and nonlinearity (basis expansion).

## How it works

**Closed-form (normal equations / SVD):**
Minimize MSE loss L = (1/n) ||Xw - y||². Setting gradient to zero gives the normal equations: XᵀXw = Xᵀy. Solved via SVD for numerical stability:

```
U, s, Vt = svd(X)
w = V @ diag(1/s) @ Uᵀ @ y
```

**Gradient descent:**
When n or d is large, use mini-batch SGD:

```
w = w - lr * (1/b) * X_bᵀ(X_b w - y_b)
```

Our implementation in `src/models/linear_model.py` supports both solvers with a scikit-learn-compatible API.

## Key properties

- **Linearity**: assumes linear relationship between X and y
- **Homoscedasticity**: constant variance of residuals
- **No multicollinearity**: correlated features inflate coefficient variance
- **SVD degeneracy**: when X is rank-deficient, SVD handles it gracefully (zero singular values → no contribution)

## Regularized variants (forward link)
Ridge = L2 penalty, Lasso = L1 penalty (sparsity). Lasso connects directly to the sparsity prior we use in sparse autoencoders — see [[04_nlp_and_transformers/_MOC|SAE connection]].

## MI Forward Link: what linear regression teaches about circuits

| Concept | MI analogue |
|---------|-------------|
| Feature weight w_i | Attention head contribution to the residual stream |
| MSE loss landscape | Cross-entropy landscape in language modeling |
| SVD solution | Low-rank factorization of QK/OV circuits (Elhage et al., 2021) |
| Regularization (Ridge) | Weight decay in transformers (critical for grokking) |

## Code reference
- [[../../../src/models/linear_model.py|src/models/linear_model.py]] — `LinearRegression` class with SVD + SGD solvers

## Links
- [[02_classical_ml/notes/logistic-regression|Logistic Regression]]
- [[02_classical_ml/notes/scikit-learn-ecosystem|scikit-learn Ecosystem]]
- [[01_foundations/notes/singular-value-decomposition|SVD]]

## Open questions
- When does the SVD solver fail vs. the SGD solver in practice? (#question)
