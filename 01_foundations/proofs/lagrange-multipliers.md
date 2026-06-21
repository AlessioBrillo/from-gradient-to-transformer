---
tags: [type/proof, phase/1]
state: consolidated
created: 2026-06-19
---

# Proof to myself: Lagrange Multipliers and KKT Conditions

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate

1. Derive the Lagrange multiplier condition from geometric reasoning.
2. State all four KKT conditions for inequality-constrained optimization and explain complementary slackness.
3. Show how L2 regularization emerges as the Lagrangian of a constrained MSE problem.
4. Write a Lagrange multiplier solution from memory.

## What I produced from memory

### 1. Geometric derivation for equality constraints

Minimize f(x) subject to g(x) = 0.

At the optimum x*, the gradient of f along the constraint surface must be zero, otherwise we could move along the surface to decrease f. The component of ∇f tangent to g(x) = 0 is the projection onto the tangent space of g. For this to vanish, ∇f must be normal to the constraint surface — i.e., parallel to ∇g:

∇f(x*) = λ ∇g(x*)   for some scalar λ.

The Lagrangian L(x, λ) = f(x) − λg(x) encodes both the gradient condition (∂L/∂x = 0 → ∇f = λ∇g) and the constraint (∂L/∂λ = 0 → g(x) = 0).

### 2. KKT conditions for g(x) ≤ 0

1. **Stationarity**: ∇f(x) + λ∇g(x) = 0
2. **Primal feasibility**: g(x) ≤ 0
3. **Dual feasibility**: λ ≥ 0
4. **Complementary slackness**: λg(x) = 0

Complementary slackness is the key insight: if the constraint does not bind (g(x) < 0), then λ = 0 and the constraint is irrelevant. If λ > 0, the constraint is active (g(x) = 0) and the optimum lies exactly on the boundary.

### 3. L2 regularization as a Lagrangian

Constrained problem: min_w MSE(w) subject to ‖w‖₂² ≤ c

Lagrangian: L(w, λ) = MSE(w) + λ(‖w‖₂² − c), with λ ≥ 0

For any fixed λ, minimizing L over w is equivalent to minimizing MSE(w) + λ‖w‖₂² — which is exactly L2-regularized regression. The dual approach would solve max_{λ ≥ 0} min_w L(w, λ), which recovers the functional relationship between the budget c and the penalty λ.

### 4. Code from memory

```python
import numpy as np

# Minimize f(x,y) = x² + y² subject to g(x,y) = x + y - 2 = 0
# Lagrangian: L = x² + y² - λ(x + y - 2)
# Stationarity:
#   ∂L/∂x = 2x - λ = 0  →  x = λ/2
#   ∂L/∂y = 2y - λ = 0  →  y = λ/2
#   ∂L/∂λ = -(x + y - 2) = 0  →  λ/2 + λ/2 = 2  →  λ = 2
# Solution: x = 1, y = 1, f_min = 2

def solve_lagrange_2d(f, grad_f, g, grad_g):
    """
    Solve ∇f = λ∇g and g=0 for a 2D problem.
    f: ℜ² → ℜ
    g: ℜ² → ℜ (constraint, must be 0)
    Returns x*, y*, λ.
    """
    # Analytical solution: specific to this problem
    # General case would need a nonlinear solver
    pass

# Numerical verification with gradient descent on the Lagrangian
x, y, lam = 0.0, 0.0, 0.0
lr = 0.01
for _ in range(1000):
    L_x = 2 * x - lam
    L_y = 2 * y - lam
    L_lam = -(x + y - 2)
    x -= lr * L_x
    y -= lr * L_y
    lam -= lr * L_lam

print(f"x = {x:.6f}, y = {y:.6f}, λ = {lam:.6f}, f = {x**2 + y**2:.6f}")
```

## Links
- [[01_foundations/notes/lagrange-multipliers]]
- [[01_foundations/notes/convex-optimization-basics]]
- [[01_foundations/notes/bayesian-thinking-and-regularization]]

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
