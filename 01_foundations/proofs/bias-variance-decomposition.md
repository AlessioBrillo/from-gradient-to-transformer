---
tags: [type/proof, phase/1]
state: consolidated
created: 2026-06-19
---

# Proof to myself: Bias-Variance Decomposition

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate

1. Derive the bias-variance decomposition formula from first principles.
2. Explain the tradeoff: how bias and variance change with model complexity, and why the test error is U-shaped.
3. Simulate bias and variance empirically for polynomial regression models of varying degrees.
4. Connect the decomposition to regularization and the MLE/MAP distinction.

## What I produced from memory

### 1. Derivation

Assume y = f(x) + ε, with E[ε] = 0 and Var[ε] = σ². Let ŷ = ŷ_D(x) be the prediction of a model trained on dataset D.

At a fixed test point x:

E[(y − ŷ)²] = E[(f + ε − ŷ)²]
            = E[(f − ŷ)²] + 2E[(f − ŷ)ε] + E[ε²]
            = E[(f − ŷ)²] + σ²                    (since ε ⟂ D, E[ε] = 0)

Now write ŷ − f = (ŷ − E[ŷ]) + (E[ŷ] − f) and expand:

E[(ŷ − f)²] = E[(ŷ − E[ŷ])²] + 2E[(ŷ − E[ŷ])(E[ŷ] − f)] + (E[ŷ] − f)²
            = Var[ŷ] + 0 + Bias[ŷ]²

Therefore:

**Expected Test Error = Bias² + Variance + σ²**

where:
- Bias[ŷ] = E[ŷ] − f(x) — systematic error (underfitting).
- Var[ŷ] = E[(ŷ − E[ŷ])²] — sensitivity to training data (overfitting).
- σ² = Var[y | x] — irreducible noise.

### 2. The U-shape of test error vs. model complexity

- Simple model (e.g., linear regression with few features): **High bias** (cannot capture pattern), **low variance** (unstable features are excluded). Test error is dominated by bias.
- Complex model (e.g., high-degree polynomial): **Low bias** (flexible enough to fit the pattern), **high variance** (also fits the noise). Test error is dominated by variance.
- The optimal model sits at the bottom of the U-curve, where the marginal decrease in bias equals the marginal increase in variance.

Regularization shifts the curve: L2 adds bias (shrinks weights toward zero) but reduces variance (less sensitivity to individual training points). Increasing λ moves the model left along the complexity axis; decreasing λ moves it right.

### 3. Code from memory

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def estimate_bias_variance(degree, n_samples=30, n_repeats=200, noise=0.25):
    """Estimate bias² and variance for polynomial regression of given degree."""
    x_test = np.linspace(-3, 3, 100)
    y_true = np.sin(x_test)
    predictions = np.zeros((n_repeats, len(x_test)))

    for rep in range(n_repeats):
        x_tr = np.random.uniform(-3, 3, n_samples)
        y_tr = np.sin(x_tr) + np.random.randn(n_samples) * noise
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
        model.fit(x_tr.reshape(-1, 1), y_tr)
        predictions[rep] = model.predict(x_test.reshape(-1, 1))

    avg_pred = predictions.mean(axis=0)
    bias_sq = ((avg_pred - y_true) ** 2).mean()
    variance = predictions.var(axis=0).mean()
    return bias_sq, variance

for deg in [1, 3, 5, 9, 15]:
    b, v = estimate_bias_variance(deg)
    print(f"Degree {deg:2d}: bias² = {b:.4f}, variance = {v:.4f}, "
          f"total (excl noise) = {b+v:.4f}")
```

## Links
- [[01_foundations/notes/bias-variance-decomposition]]
- [[01_foundations/notes/bayesian-thinking-and-regularization]]
- [[01_foundations/notes/convex-optimization-basics]]

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
