---
tags: [type/lesson, phase/1, state/review]
state: review
created: 2026-06-18
---

> **Series**: [Essence of Calculus — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&si=UrW_Qk2DDRi0K3PQ) — Chapter 5: *What's so special about Euler's number e?*

## What it is
Euler's number e ≈ 2.71828 is the unique real number such that the exponential function f(x) = eˣ is its own derivative: d/dx eˣ = eˣ. This self-derivative property makes e the natural base for continuous growth, decay, and probability.

## Why it exists / what problem it solves
Every exponential function aˣ has a derivative proportional to itself: d/dx aˣ = aˣ · ln(a). The constant ln(a) is a scaling factor. The number e is special because ln(e) = 1, eliminating the scaling factor and making eˣ the "purest" exponential — the one whose rate of change equals its value at every point. This property is why e appears in the sigmoid, softmax, cross-entropy,
  Gaussian distribution, and every continuous probability model.

## How it works

### The defining property
d/dx eˣ = eˣ

This means: at every point x, the slope of eˣ equals its current value. If you are at eˣ = 5, the slope is 5. If you are at eˣ = 100, the slope is 100. The function grows faster the larger it gets.

### Derivation from compound interest
e emerges from the limit of compound interest:

e = lim_{n→∞} (1 + 1/n)ⁿ

More generally:
eˣ = lim_{n→∞} (1 + x/n)ⁿ

This limit connects discrete compounding to continuous exponential growth — the same idea that underlies how interest accumulates, how populations grow, and how probabilities compound in sequence models.

```python
import numpy as np

def approximate_e(n_terms=100):
    """Approximate e using the series sum: Σ 1/n!"""
    e = 0.0
    fact = 1.0
    for n in range(n_terms):
        e += 1.0 / fact
        fact *= (n + 1)
    return e

print(f"e ≈ {approximate_e(20):.10f}")
print(f"e (NumPy) = {np.e:.10f}")
```

### Why e appears everywhere in ML

**Sigmoid:** σ(x) = 1 / (1 + e^{−x}) — the logistic function uses e because its derivative has the elegant form σ(x)(1 − σ(x)).

**Softmax:** softmax(z)_i = e^{z_i} / Σ e^{z_j} — the exponential turns logits into positive numbers that sum to 1. The choice of e vs any other base is absorbed by the scale of the logits.

**Gaussian:** N(x | μ, σ²) = 1 / √(2πσ²) · exp(−(x−μ)² / 2σ²) — the exponential of a quadratic form.

**Cross-entropy gradient:** ∂L/∂z_i = p_i − 1(i == y) — this simplification depends on the exponential in softmax canceling with the log in cross-entropy.

```python
# Verify the defining property numerically
def exp_derivative_numeric(x, h=1e-7):
    return (np.exp(x + h) - np.exp(x - h)) / (2 * h)

x_test = np.array([0.0, 1.0, 2.0, -1.0])
for x in x_test:
    analytic = np.exp(x)
    numeric = exp_derivative_numeric(x)
    print(f"x = {x:+.1f}: eˣ = {analytic:.6f}, numeric derivative = {numeric:.6f}, match = {np.isclose(analytic, numeric)}")
```

## Links
- [[01_foundations/notes/key-activation-functions-and-derivatives|Key Activation Functions and Their Derivatives]]
- [[01_foundations/notes/derivatives-and-gradient-descent|Derivatives and Gradient Descent]]

## Insight
The fact that eˣ is its own derivative is the hidden reason why softmax + cross-entropy produces such a clean gradient. In the chain rule for d/dz_i log(softmax(z)_i), the exponential function's self-derivative property makes terms cancel perfectly, leaving just (p_i − 1). If we used any other base b, the gradient would have an extra factor of ln(b) — absorbed by learned weights
  anyway, but mathematically less elegant.
