---
tags: [type/lesson, phase/1]
state: consolidated
created: 2026-06-19
---

# Convex Optimization Basics

> **Resources**: *Mathematics for Machine Learning* — Deisenroth, Faisal, Ong, Ch. 7 | [Convex Optimization — Boyd & Vandenberghe](https://web.stanford.edu/~boyd/cvxbook/) (Ch. 2–3 for definitions)

## What it is

Convex optimization studies minimizing convex functions over convex sets. A function is convex if the line segment between any two points on its graph lies **above** the graph — equivalently, its Hessian is positive semidefinite everywhere. A set is convex if the line segment connecting any two points in the set lies entirely inside the set.

## Why it exists / what problem it solves

Not every optimization problem is equally hard. Convex problems have a **single global minimum**
with no spurious local minima or saddle points. Gradient descent provably converges to the
global optimum for convex losses — no matter where you start. This is why logistic regression
and linear SVMs (both convex) have clean convergence guarantees, while neural networks
(non-convex) require careful initialization and tuning.

## How it works

### Convex sets

A set C is convex if for any x, y ∈ C and θ ∈ [0, 1]:

θx + (1 − θ)y ∈ C

Examples of convex sets: ℜⁿ itself, any affine subspace (lines, planes), norm balls {x : ‖x‖ ≤ r}, the set of probability distributions (simplex), the set of positive semidefinite matrices.

Non-examples: the set of integers, the set of matrices with determinant = 1, the set of vectors with exactly k non-zero entries (sparsity constraint).

### Convex functions

A function f : ℜⁿ → ℜ is convex if:

1. Its domain is a convex set.
2. For all x, y in the domain and θ ∈ [0, 1]:

   f(θx + (1 − θ)y) ≤ θf(x) + (1 − θ)f(y)

   *The function at any convex combination is at most the convex combination of the function values.*

**First-order condition** (for differentiable f):

   f(y) ≥ f(x) + ∇f(x)ᵀ(y − x)

   *The linear (first-order Taylor) approximation is a global lower bound. This is why gradient descent never overshoots on a convex function — the true function is always above the linear approximation used by the update step.*

**Second-order condition** (for twice-differentiable f):

   ∇²f(x) ⪰ 0   (Hessian is positive semidefinite for all x)

   *All eigenvalues of the Hessian are non-negative everywhere.*

```python
import numpy as np

def is_convex_numeric(f, x_range, grid=101):
    """Heuristic: check if the second derivative is non-negative
    on a dense grid. For 1D functions only — a true check needs
    the Hessian everywhere."""
    xs = np.linspace(x_range[0], x_range[1], grid)
    h = xs[1] - xs[0]
    second_deriv = (f(xs[:-2]) - 2 * f(xs[1:-1]) + f(xs[2:])) / (h ** 2)
    return np.all(second_deriv >= -1e-8)

f_mse = lambda x: (x - 3) ** 2               # convex everywhere
f_nonconvex = lambda x: x ** 3 - 3 * x        # not convex (inflection at 0)

print(is_convex_numeric(f_mse, (-5, 5)))          # True
print(is_convex_numeric(f_nonconvex, (-5, 5)))    # False
```

### Convexity of common ML loss functions

| Loss | Function | Convex? | Hessian (or second derivative) |
|------|----------|---------|--------------------------------|
| MSE | (y − ŷ)² | **Yes**, everywhere | 2 (positive constant) |
| MAE | \|y − ŷ\| | **Yes**, but not strictly | 0 (except at ŷ=y where undefined) |
| Cross-entropy (logistic) | −y log σ(ŷ) − (1−y) log(1−σ(ŷ)) | **Yes**, in the logit space | σ(ŷ)(1−σ(ŷ)) > 0 (positive semidef gradient of sigmoid) |
| Hinge loss | max(0, 1 − yŷ) | **Yes** | 0 or undefined (piecewise linear) |
| Neural net with hidden layers | f(x; W₁, W₂) | **No** | Non-convex (product of parameters creates saddle points) |
| Cross-entropy in a neural net | CE(f(x; θ), y) | **No** | Hessian has both positive and negative eigenvalues |

The key boundary: **when the model is a linear function of the parameters** (linear regression, logistic regression, linear SVM), the optimization is convex. **When the model is a non-linear function of parameters** (neural networks with hidden layers), it is non-convex.

### Why convexity guarantees global optimization

For a convex loss L(θ), gradient descent satisfies:

L(θ_{t+1}) − L(θ*) ≤ (1 − 2ημ)(L(θ_t) − L(θ*))

where μ is the strong convexity parameter (minimum eigenvalue of the Hessian). This is **linear convergence**: the suboptimality shrinks by a constant fraction each step. Non-convex optimization cannot provide such guarantees — you rely on heuristics like learning rate schedules, momentum, and batch normalization to navigate saddle points.

## Links
- [[01_foundations/notes/derivatives-and-gradient-descent]]
- [[01_foundations/notes/higher-order-derivatives-and-taylor-series]]
- [[01_foundations/notes/positive-definite-matrices]]
- [[01_foundations/notes/lagrange-multipliers]]

## Insight
Convexity is not about the shape of the loss landscape in the data space — it is about the shape
in **parameter space**. MSE as a function of the residual is a parabola (convex), but MSE as a
function of neural network weights is not. The distinction is invisible until you derive the
second derivative with respect to the actual parameters. This is why feature engineering (making
the problem more linearly separable) is often easier than making the model more powerful.
