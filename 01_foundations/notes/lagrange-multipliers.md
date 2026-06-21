---
tags: [type/lesson, phase/1]
state: consolidated
created: 2026-06-19
---

# Lagrange Multipliers and KKT Conditions

> **Resources**: [3Blue1Brown — Lagrange Multipliers](https://youtu.be/yuqB-d5MjZA) (the geometric intuition is irreplaceable) | *Mathematics for Machine Learning* — Deisenroth, Faisal, Ong, Ch. 7.4 | [Boyd & Vandenberghe Ch. 5](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf) — Duality (advanced)

## What it is

Lagrange multipliers are a method for finding the local extrema of a function subject to equality constraints. Given f(x) to minimize and g(x) = 0 the constraint, the Lagrangian is L(x, λ) = f(x) − λg(x). The solution is a stationary point of L: ∇L = 0 simultaneously satisfies ∇f = λ∇g and g(x) = 0. The KKT (Karush–Kuhn–Tucker) conditions extend this to inequality constraints.

## Why it exists / what problem it solves

Most ML problems are constrained optimizations, even when they do not look like one:

- **SVM**: maximize the margin subject to every training point being correctly classified (or within a slack margin): yᵢ(w·xᵢ + b) ≥ 1.
- **Regularization**: minimize training loss subject to ‖w‖ ≤ c (weight budget). The Lagrangian of this problem is L = loss + λ(‖w‖ − c), and minimizing L is equivalent to adding a penalty term.
- **Maximum entropy models**: maximize entropy H(p) subject to expected feature counts matching the empirical distribution.

Understanding Lagrange multipliers makes these connections explicit: **every penalty method is a Lagrangian, and every Lagrangian implies a constraint.**

## How it works

### Equality constraints: geometric intuition

Minimize f(x) subject to g(x) = 0.

At the optimum x*, moving along the constraint surface (where g(x) = 0) cannot decrease f — otherwise you would not be at an optimum. This means ∇f(x*) has no component tangent to the constraint surface, so ∇f(x*) must be parallel to ∇g(x*):

∇f(x*) = λ ∇g(x*)

The scalar λ is the **Lagrange multiplier**. Its sign encodes whether relaxing the constraint (allowing g(x) = ε) would increase or decrease f.

General solution: solve the system of n + 1 equations (n from ∇f = λ∇g, 1 from g(x) = 0) for x and λ.

```python
import numpy as np

# Example: minimize f(x, y) = x² + y² subject to x + y = 1
# Lagrangian: L = x² + y² - λ(x + y - 1)
# ∂L/∂x = 2x - λ = 0  →  x = λ/2
# ∂L/∂y = 2y - λ = 0  →  y = λ/2
# ∂L/∂λ = -(x + y - 1) = 0  →  λ/2 + λ/2 = 1  →  λ = 1
# Solution: x = 0.5, y = 0.5, f_min = 0.5

lam = 1.0
x_opt = lam / 2
y_opt = lam / 2
print(f"Optimum at x={x_opt}, y={y_opt}, f={x_opt**2 + y_opt**2}")
```

### Inequality constraints: KKT conditions

Minimize f(x) subject to g(x) ≤ 0.

The Lagrangian is: L(x, λ) = f(x) + λg(x) with λ ≥ 0.

The KKT necessary conditions (for convex problems, also sufficient) are:

| Condition | Equation | Meaning |
|-----------|----------|---------|
| Stationarity | ∇f(x) + λ∇g(x) = 0 | No direction can improve f without violating the constraint |
| Primal feasibility | g(x) ≤ 0 | The constraint is satisfied |
| Dual feasibility | λ ≥ 0 | The Lagrange multiplier is non-negative |
| Complementary slackness | λg(x) = 0 | Either the constraint is inactive (g < 0, λ = 0) or binding (g = 0, λ > 0) |

Complementary slackness is the most important condition: it says that if the constraint is not touching the optimum (g(x) < 0), then the multiplier λ is zero and the constraint can be ignored. Only **active constraints** — those where g(x) = 0 — affect the solution.

### Connection to regularization

Consider L2-regularized linear regression:

min_w MSE(w) + λ‖w‖₂²

This solves the constrained problem:

min_w MSE(w)  subject to  ‖w‖₂² ≤ c

The Lagrangian is L = MSE(w) + λ(‖w‖₂² − c). Minimizing L over w with λ fixed (and then optimizing λ) recovers the penalty formulation. The connection is exact:

- **λ small** (weak penalty) ↔ c large (big weight budget) — the model uses large weights.
- **λ large** (strong penalty) ↔ c small (tight budget) — the model shrinks weights.

| Penalty | Implicit prior (Bayesian) | Effective constraint |
|---------|--------------------------|---------------------|
| L2 ‖w‖₂² | Gaussian prior on w | ‖w‖₂² ≤ c |
| L1 ‖w‖₁ | Laplace prior on w | ‖w‖₁ ≤ c |
| Elastic Net | αL2 + (1−α)L1 | ‖w‖₂² ≤ c₁ and ‖w‖₁ ≤ c₂ |

### Application preview: SVM (Phase 2)

The SVM primal problem is:

min_{w, b} ‖w‖²  subject to  yᵢ(w·xᵢ + b) ≥ 1 for all i

The Lagrangian is L = ‖w‖² − Σ αᵢ[yᵢ(w·xᵢ + b) − 1] with αᵢ ≥ 0.

KKT stationarity gives w = Σ αᵢ yᵢ xᵢ — the weight vector is a linear combination of **support vectors** (those with αᵢ > 0). The complementary slackness condition αᵢ(yᵢ(w·xᵢ + b) − 1) = 0 ensures that only points on the margin boundary contribute to the solution. This is why SVMs are sparse: most training points have αᵢ = 0 and can be discarded after training.

## Links
- [[01_foundations/notes/convex-optimization-basics]]
- [[01_foundations/notes/bayesian-thinking-and-regularization]]
- [[01_foundations/notes/maximum-likelihood-estimation]]

## Insight
The Lagrange multiplier λ in a regularized objective is not a free hyperparameter to tune by guesswork — it is the dual variable of a budget constraint. Cross-validation over λ is implicitly searching for the tightest budget that still achieves low training error. This dual perspective (primal: constraint on weights; dual: penalty on loss) is the foundation of the SVM, Lasso, and every regularized estimator. Understanding it now saves you from treating regularization as a hack.
