---
tags: [type/lesson, phase/1, state/review]
state: review
created: 2026-06-18
---

> **Series**: [Essence of Calculus — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&si=UrW_Qk2DDRi0K3PQ) — Chapter 8: *Integration and the fundamental theorem of calculus*

## What it is
Integration computes the accumulated area under a curve. The Fundamental Theorem of Calculus (FTC) states that integration and differentiation are inverse operations: the derivative of an accumulated area function gives back the original curve.

## Why it exists / what problem it solves
Integration answers questions of accumulation: total distance from velocity, total probability from a density, expected value from a PDF. In machine learning, the most common integral is the expected value E[X] = ∫ x · f(x) dx — the center of every distribution. The FTC is why we can compute probabilities from PDFs using cumulative distribution functions (CDFs).

## How it works

### The definite integral
∫_a^b f(x) dx represents the signed area under f(x) from x = a to x = b. It is defined as the limit of a Riemann sum: sum of rectangle areas as the width approaches zero.

```python
import numpy as np

def riemann_sum(f, a, b, n=1000):
    """Approximate ∫_a^b f(x) dx using the midpoint rule."""
    xs = np.linspace(a, b, n, endpoint=False)
    dx = (b - a) / n
    return np.sum(f(xs + dx / 2)) * dx

# Example: ∫_0^1 x² dx = 1/3 ≈ 0.3333
area = riemann_sum(lambda x: x ** 2, 0, 1)
print(f"∫_0^1 x² dx ≈ {area:.6f} (expected 0.333333)")
```

### The Fundamental Theorem of Calculus (Part 1)
If F(x) = ∫_a^x f(t) dt, then F'(x) = f(x).

The derivative of the accumulated area function gives back the original function. This is why differentiation and integration are inverses.

### The Fundamental Theorem of Calculus (Part 2)
∫_a^b f(x) dx = F(b) − F(a), where F'(x) = f(x).

This is how we compute definite integrals: find an antiderivative F, evaluate at the endpoints, and subtract.

```python
from scipy.integrate import quad

# Numerical integration of a Gaussian PDF
mu, sigma = 0.0, 1.0
def gaussian(x):
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))

# Probability that x lies in [-1, 1]
prob, error = quad(gaussian, -1, 1)
print(f"P(-1 ≤ X ≤ 1) ≈ {prob:.4f} (expected ~0.6827 for standard normal)")
```

### Connection to probability
A probability density function f(x) must satisfy ∫_{-∞}^{∞} f(x) dx = 1.

The cumulative distribution function F(x) = ∫_{-∞}^{x} f(t) dt gives the probability that a random sample is ≤ x.

The expected value of a function g under the distribution f is:
E[g(X)] = ∫ g(x) · f(x) dx

This integral cannot always be computed analytically — which is why we use Monte Carlo estimation (sample and average).

```python
# Monte Carlo estimation of expectation
np.random.seed(42)
samples = np.random.normal(0, 1, size=100000)
# E[X²] for standard normal = 1 (variance)
estimate = np.mean(samples ** 2)
print(f"E[X²] ≈ {estimate:.4f} (expected 1.0)")
```

### Numerical integration in practice
In ML, most integrals are either:
- **Analytically tractable** (Gaussian expectation, linear models) — we have closed forms.
- **Estimated via Monte Carlo** (Bayesian inference, reinforcement learning) — sample from the distribution and average.
- **Replaced by sums** (empirical risk minimization) — the integral over the true data distribution is approximated by a sum over training samples: (1/n) Σ loss(x_i, y_i).

This last point is crucial: **every training loss is a Monte Carlo estimate of an integral over the true data distribution.**

## Links
- [[01_foundations/notes/probability-basics-for-ml|Probability Basics for ML]]
- [[01_foundations/notes/derivatives-and-gradient-descent|Derivatives and Gradient Descent]]
- [[01_foundations/notes/eulers-number-and-exponential|Euler's Number and the Exponential Function]]

## Insight
The training loss (1/n) Σ L(x_i, y_i) is a Monte Carlo approximation of the true risk R(θ) = E_{(x,y)∼p_data}[L(x, y; θ)]. This is why larger datasets give better models — they provide a more accurate estimate of the integral over the true distribution. The Fundamental Theorem of Calculus connects the two: differentiation tells us how to improve our model (gradient descent), and
  integration tells us how to evaluate it (expected loss).
