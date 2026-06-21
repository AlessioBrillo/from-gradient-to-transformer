---
tags: [type/lesson, phase/1]
state: consolidated
created: 2026-06-19
---

# Bias-Variance Decomposition

> **Resources**: *Mathematics for Machine Learning* — Deisenroth, Faisal, Ong, Ch. 8.4 | [StatQuest — Bias and Variance](https://youtu.be/EuBBz3bI-aA) | [Bias-Variance Decomposition — scikit-learn docs](https://scikit-learn.org/stable/modules/learning_curve.html) | [Gareth James et al. — *An Introduction to Statistical Learning*](https://www.statlearning.com/) (Ch. 2.2.2)

## What it is

The bias-variance decomposition breaks the expected prediction error of a model into three fundamental sources: bias (error from overly simplistic assumptions), variance (error from sensitivity to training data fluctuations), and irreducible error (noise inherent in the data). Mathematically:

E[(y − ŷ)²] = Bias[ŷ]² + Var[ŷ] + σ²

where ŷ = ŷ(x) is the model prediction, y is the true value, and σ² = Var[y | x] is the irreducible noise.

## Why it exists / what problem it solves

Every modeling decision — choosing between linear regression and a neural network, adjusting the regularization strength, adding or removing features — is a tradeoff between bias and variance:

- **High bias**: the model is too simple to capture the true pattern. It systematically underfits. Training error is high, and test error is similarly high.
- **High variance**: the model is so flexible that it memorizes the training noise. It overfits. Training error is near zero, but test error is high.

The decomposition explains why the best model is not the most complex model, nor the simplest, but the one that optimally balances bias and variance for the available data.

## How it works

### Derivation

Let y = f(x) + ε, where ε ∼ (0, σ²) is zero-mean noise independent of x. Let ŷ(x) be the prediction of a model trained on a random training set D.

The expected squared error at a fixed test point x decomposes as:

E[(y − ŷ)²] = E[(f + ε − ŷ)²]
            = E[(f − ŷ)²] + 2E[(f − ŷ)ε] + E[ε²]
            = E[(f − ŷ)²] + σ²                        (since ε independent of ŷ)

Now expand E[(f − ŷ)²]:

E[(f − ŷ)²] = E[(f − E[ŷ] + E[ŷ] − ŷ)²]
            = (f − E[ŷ])² + E[(ŷ − E[ŷ])²] + 2E[(f − E[ŷ])(E[ŷ] − ŷ)]
            = Bias[ŷ]² + Var[ŷ]                       (cross-term vanishes: E[ŷ − E[ŷ]] = 0)

Therefore:

**Expected Test Error = Bias² + Variance + Irreducible Error**

where:
- **Bias[ŷ]²** = (f(x) − E_D[ŷ_D(x)])² — how far the average prediction is from the true value.
- **Var[ŷ]** = E_D[(ŷ_D(x) − E_D[ŷ_D(x)])²] — how much predictions fluctuate across different training sets.
- **σ²** = Var[y | x] — the noise floor that no model can reduce.

### The tradeoff visualized (target diagram)

Interpret each "shot" as the model's prediction on a fixed test point, trained on different instantiations of the training set:

```
Low bias, low variance     Low bias, high variance
  🎯 🎯 🎯                  ↖ ↗ ↙ ↘
  🎯 🎯 🎯                  ↗ ↖ ↘ ↙
  (ideal)                   (overfit)

High bias, low variance     High bias, high variance
  😢 😢 😢                  😢 😢 😢
  😢 😢 😢                  😢 😢 😢
  (underfit)                (worst of both)
```

The expected error is the average squared distance from the center of the target. Low bias centers the cluster on the bullseye. Low variance keeps the cluster tight.

### Bias-variance and model complexity

```
Error
  ▲
  │   ┌────────── Test error (Bias² + Variance)
  │  ╱│╲
  │ ╱ │ ╲
  │╱  │  ╲
  │    │   ╲  ←─── Irreducible error
  │           ╲
  │            ╲─────────────────── Training error
  └──────────────────────────────→ Model complexity
               ↑
          Optimal complexity
          (sweet spot)
```

Training error decreases monotonically with complexity (a polynomial of degree N+1 fits N points perfectly). Test error is U-shaped: decreasing initially as bias drops, then increasing as variance dominates.

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

np.random.seed(42)

# True function: sin(x)
def f_true(x):
    return np.sin(x)

# Generate multiple training sets to estimate bias and variance
n_repeats = 200
n_samples = 30
degrees = [1, 3, 9, 15]
x_test = np.linspace(-3, 3, 100)

fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharey=True)

for idx, degree in enumerate(degrees):
    predictions = np.zeros((n_repeats, len(x_test)))

    for rep in range(n_repeats):
        x_train = np.random.uniform(-3, 3, n_samples)
        y_train = f_true(x_train) + np.random.randn(n_samples) * 0.25

        model = make_pipeline(
            PolynomialFeatures(degree), LinearRegression()
        )
        model.fit(x_train.reshape(-1, 1), y_train)
        predictions[rep, :] = model.predict(x_test.reshape(-1, 1))

    # Estimate bias², variance, and MSE
    y_true = f_true(x_test)
    avg_prediction = predictions.mean(axis=0)
    bias_sq = (avg_prediction - y_true) ** 2
    variance = predictions.var(axis=0)
    mse = bias_sq + variance + 0.25**2  # σ² = noise^2

    axes[idx].plot(x_test, y_true, "k--", label="True f(x)")
    axes[idx].plot(x_test, avg_prediction, "r-", label="Avg prediction")
    axes[idx].fill_between(
        x_test,
        avg_prediction - np.sqrt(variance),
        avg_prediction + np.sqrt(variance),
        alpha=0.3,
        label="±1 std (variance)",
    )
    axes[idx].set_title(f"Degree {degree}")
    axes[idx].legend(fontsize=8)
    axes[idx].set_ylim(-2, 2)

plt.tight_layout()
print(f"Degree {degree}: avg bias² = {bias_sq.mean():.3f}, "
      f"avg variance = {variance.mean():.3f}, "
      f"avg MSE = {mse.mean():.3f}")
```

### How methods affect the tradeoff

| Method | Effect on bias | Effect on variance |
|--------|---------------|-------------------|
| More features (complexity) | ↓ decreases | ↑ increases |
| L2 regularization | ↑ increases (shrinks weights) | ↓ decreases |
| L1 regularization | ↑ increases (zeroes out weights) | ↓ decreases (model selection) |
| More training data | ↔ no change for well-specified model | ↓ decreases (1/n) |
| Bagging (e.g., Random Forest) | ↔ slight increase possible | ↓ decreases (averaging) |
| Boosting (e.g., XGBoost) | ↓ decreases (focus on residuals) | ↑ increases (overfits to noise) |
| Feature selection | ↑ may increase (loses signal) | ↓ decreases (fewer parameters) |

### Relationship to MLE and regularization (from [[01_foundations/notes/bayesian-thinking-and-regularization]])

- MLE finds the parameters that best fit the training data (minimum bias, potentially high variance).
- MAP with a prior (regularization) introduces bias toward zero but reduces variance.
- The optimal λ in L2 regularization is the one that minimizes E[(y − ŷ)²] on unseen data — i.e., the λ that achieves the best bias-variance tradeoff.

## Links
- [[01_foundations/notes/bayesian-thinking-and-regularization]]
- [[01_foundations/notes/maximum-likelihood-estimation]]
- [[01_foundations/notes/derivatives-and-gradient-descent]]

## Insight
The bias-variance decomposition is not just a theoretical curiosity — it is a **diagnostic tool**. If your model is underfitting (high training error), you are in the high-bias regime: add features, reduce regularization, use a more flexible model. If your model is overfitting (low training error, high validation error), you are in the high-variance regime: add regularization, reduce features, get more data. The decomposition tells you which lever to pull, not just that something is wrong.
