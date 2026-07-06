---
tags: [type/exercise, phase/2]
skill: Linear/logistic regression
created: 2026-07-05
---

# Exercise: Linear and Logistic Regression

## Goal / skill it demonstrates
Implement linear regression and logistic regression from scratch, verify correctness against scikit-learn, visualize decision boundaries, and connect the geometry to attention-based separation in transformers.

## Instructions

### Part 1 — Linear Regression (SVD vs SGD)

1. Generate a synthetic regression dataset: `X, y = make_regression(n_samples=200, n_features=5, noise=2.0, seed=42)` from `src.data.datasets`.
2. Fit `LinearRegression(solver="svd")` from `src.models.linear_model` and compare coefficients with `sklearn.linear_model.LinearRegression`.
3. Fit `LinearRegression(solver="sgd")` with `lr=0.01, epochs=500`. Plot the training loss curve. Does it converge to the SVD solution? Within what tolerance?
4. **Question:** one sample has 3 features with values [0.1, -2.5, 4.0]. Predict its target using all three solvers. Do they agree?

### Part 2 — Logistic Regression on Moons

1. Generate: `X, y = make_moons(n_samples=300, noise=0.2, seed=42)`.
2. Train `LogisticRegression(C=1.0)` from our implementation. Plot the decision boundary (hint: contour of `decision_function(X) = 0`). Mark the support vectors — which points are closest to the boundary?
3. Same with `LogisticRegression(C=100.0)`. How does the boundary change? Why?
4. Compare our accuracy and F1 score with `sklearn.linear_model.LogisticRegression` on a held-out test set.

### Part 3 — Feature Weights & Decision Geometry

For the moon dataset, inspect the learned coefficients `model.coef_`. Which feature contributes more to the decision? Visualize the projection of data onto the weight direction — this is analogous to how an **attention head projects queries onto a key direction** in the QK circuit.

In your own words: **"If the feature weights w define a direction in input space that separates classes, what is the analogous direction in a transformer attention head?"** (Hint: the QK circuit computes a dot product between query and key — what does that dot product "separate"?)

## Solution

```python
from src.data.datasets import make_regression, make_moons, train_test_split
from src.models.linear_model import LinearRegression, LogisticRegression
from src.evaluation.metrics import accuracy_score, f1_score
import matplotlib.pyplot as plt
import numpy as np

# Part 1
X, y = make_regression(n_samples=200, n_features=5, noise=2.0, seed=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, seed=42)

lin_svd = LinearRegression(solver="svd").fit(X_train, y_train)
lin_sgd = LinearRegression(solver="sgd").fit(X_train, y_train, lr=0.01, epochs=500, seed=42)

# Compare coefficients
print("SVD coef:", lin_svd.coef_)
print("SGD coef:", lin_sgd.coef_)
print("Max diff:", np.max(np.abs(lin_svd.coef_ - lin_sgd.coef_)))

# Part 2
X, y = make_moons(n_samples=300, noise=0.2, seed=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, seed=42)

log_reg = LogisticRegression(C=1.0).fit(X_train, y_train, lr=0.1, epochs=2000, seed=42)
preds = log_reg.predict(X_test)
acc = accuracy_score(y_test, preds)
f1 = f1_score(y_test, preds)
print(f"LogReg on moons: acc={acc:.3f}, f1={f1:.3f}")
print(f"Weights: {log_reg.coef_}, intercept: {log_reg.intercept_:.3f}")

# Part 3 — Decision boundary plot
xx, yy = np.meshgrid(np.linspace(X[:, 0].min()-0.5, X[:, 0].max()+0.5, 200),
                     np.linspace(X[:, 1].min()-0.5, X[:, 1].max()+0.5, 200))
Z = log_reg.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
plt.contourf(xx, yy, Z, levels=20, cmap="RdBu", alpha=0.6)
plt.contour(xx, yy, Z, levels=[0], colors="k", linewidths=2)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap="bwr", edgecolors="k", s=20)
plt.title("Logistic Regression Decision Boundary on Moons")
plt.savefig("figures/ex01_logreg_moons.png", dpi=150)
plt.close()
```

## MI Forward Link: My Answer

The feature weight vector w in logistic regression defines a direction in input space. The signed distance from a point to the decision boundary is X · w + b. This is **mathematically identical** to what an attention head's QK circuit computes: the dot product between a query and a key determines which positions to attend to. The "decision boundary" in attention is the threshold at which one token is preferred over another — the attention probability softmax replaces the logistic sigmoid.

This isomorphism is the core insight of Elhage et al.'s QK/OV decomposition: **QK is a binary separation problem (attend vs. not-attend), and OV is a regression problem (what value to copy)**.

## What I learned doing it
- SVD solver is exact but costs O(n d²) memory; SGD scales to large data
- Logistic regression without enough regularization overfits on separable data (weights explode)
- The geometry of a linear decision boundary is the same geometry that governs attention — same math, different names

## Linked skill
- [[00_meta/02_skill-tree]] → Linear/logistic regression
- [[04_nlp_and_transformers/_MOC|Phase 4 — QK/OV connection]]
