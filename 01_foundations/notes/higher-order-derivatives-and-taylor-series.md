---
tags: [type/lesson, phase/1, state/review]
state: review
created: 2026-06-18
---

> **Series**: [Essence of Calculus — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&si=UrW_Qk2DDRi0K3PQ) — Chapter 10: *Higher order derivatives* and Chapter 11: *Taylor series*

## What it is
Higher-order derivatives measure curvature and beyond: the second derivative tells you how the slope is changing (concavity). Taylor series approximate any smooth function locally as a polynomial whose coefficients are the derivatives at a point.

## Why it exists / what problem it solves
First derivatives (gradients) tell us which direction to move, but not how far — that is the role of curvature. Second derivatives (Hessian) govern learning rate selection, convergence speed, and the behavior of adaptive optimizers like Adam. Taylor series provide the theoretical foundation for gradient descent itself: gradient descent assumes a linear (first-order Taylor)
  approximation is good enough. Newton's method uses a quadratic (second-order Taylor) approximation for faster convergence.

## How it works

### Second derivative f''(x)
The derivative of the derivative. Measures **concavity**:
- f''(x) > 0 → convex (curving upward, like x²) — minimum.
- f''(x) < 0 → concave (curving downward, like −x²) — maximum.
- f''(x) = 0 → inflection point (transition between convex and concave).

```python
import numpy as np

def second_derivative_numeric(f, x, h=1e-5):
    """f''(x) via central difference of first derivative."""
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)

def f(x):
    return x ** 3 - 3 * x  # inflection at x=0, min at x=1, max at x=-1

for x in [-1.0, 0.0, 1.0]:
    f2 = second_derivative_numeric(f, x)
    label = "convex" if f2 > 0 else ("concave" if f2 < 0 else "inflection")
    print(f"x = {x:+.1f}: f''(x) ≈ {f2:.3f} → {label}")
```

### The Hessian matrix
For a multivariable function f: ℝⁿ → ℝ, the second derivatives form the Hessian H, an n×n symmetric matrix:

H_ij = ∂²f / ∂x_i ∂x_j

The Hessian describes local curvature in every direction. Its eigenvalues tell you:
- All positive → strict local minimum.
- All negative → strict local maximum.
- Mixed signs → saddle point (the most common critical point in high-dimensional loss landscapes).

Gradient descent converges fastest when the Hessian is well-conditioned (all eigenvalues of similar magnitude). Poor conditioning — where some directions have much higher curvature than others — is why adaptive methods like Adam outperform SGD on ill-conditioned problems.

### Taylor series
Any sufficiently smooth function f can be approximated around a point a as:

f(x) = f(a) + f'(a)(x−a) + (1/2) f''(a)(x−a)² + (1/6) f'''(a)(x−a)³ + ...

The n-th term is (1/n!) f^{(n)}(a) (x−a)ⁿ.

**First-order Taylor approximation** (used by gradient descent):
f(x) ≈ f(a) + f'(a)(x−a)

This is a linear approximation — valid only close to a. Gradient descent takes a step in the direction of steepest descent, assuming the linear approximation holds.

**Second-order Taylor approximation** (used by Newton's method):
f(x) ≈ f(a) + f'(a)(x−a) + (1/2) f''(a)(x−a)²

This quadratic approximation captures curvature, allowing Newton's method to take more informed steps. It converges in fewer iterations but each iteration is more expensive (computing and inverting the Hessian).

```python
def taylor_series(f, f_derivatives, a, x, order=3):
    """Evaluate Taylor series of f around a at point x up to given order."""
    result = f(a)
    term = 1.0
    for n in range(1, order + 1):
        term *= (x - a) / n
        result += term * f_derivatives[n](a)
    return result

def f(x):
    return np.sin(x)

# Derivatives of sin(x) at 0 cycle: sin, cos, -sin, -cos, sin, ...
def sin_derivatives(n, x):
    cycle = [np.sin(x), np.cos(x), -np.sin(x), -np.cos(x)]
    return cycle[n % 4]

a = 0.0
x_test = 0.5
true_val = f(x_test)

for order in range(1, 6):
    approx = taylor_series(f, lambda n: (lambda x: sin_derivatives(n, x)), a, x_test, order)
    err = abs(true_val - approx)
    print(f"Order {order}: sin({x_test}) ≈ {approx:.6f}, error = {err:.2e}")
```

### Taylor series in machine learning

| Technique | Taylor order | What it does |
|-----------|-------------|--------------|
| Gradient descent | 1st | Linear approximation of loss |
| Newton's method | 2nd | Quadratic approximation, faster convergence |
| Momentum | 1st + gradient history | Smooths updates, approximates curvature |
| Adam | 1st + gradient variance | Adaptive learning rates per parameter |
| Gradient accumulation | 0th/1st | Approximates full-batch gradient with mini-batches |

```python
# Visualizing Taylor approximations of sin(x) near 0
import matplotlib.pyplot as plt

xs = np.linspace(-np.pi, np.pi, 100)
true = np.sin(xs)

approx_1st = xs  # sin(0) + cos(0)(x-0) = x
approx_3rd = xs - xs ** 3 / 6  # x - x³/3!
approx_5th = xs - xs ** 3 / 6 + xs ** 5 / 120  # x - x³/3! + x⁵/5!

plt.figure(figsize=(10, 6))
plt.plot(xs, true, 'k-', label='sin(x)', linewidth=2)
plt.plot(xs, approx_1st, '--', label='1st order (linear)')
plt.plot(xs, approx_3rd, '--', label='3rd order (cubic)')
plt.plot(xs, approx_5th, '--', label='5th order')
plt.axvline(0, color='gray', alpha=0.3)
plt.axhline(0, color='gray', alpha=0.3)
plt.ylim(-2, 2)
plt.legend()
plt.title('Taylor approximations of sin(x) around x=0')
plt.grid(alpha=0.3)
```

## Links
- [[01_foundations/notes/derivatives-and-gradient-descent|Derivatives and Gradient Descent]]
- [[01_foundations/notes/chain-rule-and-backpropagation|Chain Rule and Backpropagation]]
- [[01_foundations/notes/numerical-gradient-check|Numerical Gradient Check]]

## Insight
In high-dimensional spaces, saddle points vastly outnumber local minima. A point where ∇f = 0 is overwhelmingly likely to be a saddle (mixed curvature) rather than a true minimum. This is why first-order methods (gradient descent) can escape saddle points — they only see the gradient, which is zero at the saddle, but tiny perturbations from mini-batch noise push them away.
  Second-order methods that try to converge directly to a minimum can get stuck at saddles instead. This insight explains why SGD with mini-batches works so well in practice: the noise is a feature, not a bug.
