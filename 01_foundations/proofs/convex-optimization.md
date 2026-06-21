---
tags: [type/proof, phase/1]
state: consolidated
created: 2026-06-19
---

# Proof to myself: Convex Optimization Basics

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate

1. Define convex sets and convex functions precisely.
2. State the second-order (Hessian) condition for convexity.
3. Verify whether MSE, cross-entropy, and a neural network loss are convex — and explain why the answer matters.
4. Write a numerical convexity check from memory.

## What I produced from memory

### 1. Definitions

**Convex set:** A set C is convex if for any x, y ∈ C and θ ∈ [0, 1], the point θx + (1 − θ)y is also in C. The line segment between any two points stays inside the set.

**Convex function:** A function f is convex if for any x, y in its domain and θ ∈ [0, 1]:

f(θx + (1 − θ)y) ≤ θf(x) + (1 − θ)f(y)

The function at any interpolation of inputs is less than or equal to the interpolation of outputs — the function always lies below the chord.

**Second-order condition:** If f is twice differentiable, convexity is equivalent to the Hessian being positive semidefinite everywhere:

∇²f(x) ⪰ 0  for all x in the domain

A matrix is positive semidefinite if all its eigenvalues are ≥ 0. For a 1D function, this reduces to f''(x) ≥ 0 everywhere.

### 2. Convexity of ML losses

**MSE:** f(ŷ) = (ŷ − y)². The second derivative f''(ŷ) = 2 > 0 everywhere. Convex.

**Binary cross-entropy** (as a function of logit z): L(z) = −y log σ(z) − (1−y) log(1 − σ(z)). The second derivative L''(z) = σ(z)(1 − σ(z)) > 0 for all finite z. Convex in the logit space.

**Neural network loss** (two hidden layers): L(W₁, W₂) = (σ(W₂σ(W₁x)) − y)². The Hessian contains terms proportional to W₁W₂ and products of activations — it is indefinite (has both positive and negative eigenvalues). Not convex.

The practical consequence: for linear models (logistic regression, linear SVM), gradient descent converges to the global minimum regardless of initialization. For neural networks, initialization, learning rate, and architecture choices determine which local minimum you land in.

### 3. Code from memory

```python
import numpy as np

def hessian_convex_check(f, x, eps=1e-5):
    """Check convexity at point x by examining Hessian eigenvalues."""
    n = len(x)
    H = np.zeros((n, n))
    f0 = f(x)
    for i in range(n):
        for j in range(i, n):
            x_pp, x_pm = x.copy(), x.copy()
            x_mp, x_mm = x.copy(), x.copy()
            x_pp[i] += eps; x_pp[j] += eps
            x_pm[i] += eps; x_pm[j] -= eps
            x_mp[i] -= eps; x_mp[j] += eps
            x_mm[i] -= eps; x_mm[j] -= eps
            H[i, j] = (f(x_pp) + f(x_mm) - f(x_pm) - f(x_mp)) / (4 * eps ** 2)
            H[j, i] = H[i, j]
    eigvals = np.linalg.eigvalsh(H)
    is_convex = np.all(eigvals >= -1e-8)
    return is_convex, eigvals

# Test: MSE loss for simple linear regression
def mse_at(w):
    x = np.array([1, 2, 3])
    y = np.array([2, 4, 6])
    pred = w[0] * x + w[1]
    return np.mean((pred - y) ** 2)

convex, ev = hessian_convex_check(mse_at, np.array([1.0, 0.0]))
print(f"MSE convex at this point: {convex}")     # True
print(f"Hessian eigenvalues: {ev}")
```

## Links
- [[01_foundations/notes/convex-optimization-basics]]
- [[01_foundations/notes/higher-order-derivatives-and-taylor-series]]
- [[01_foundations/notes/lagrange-multipliers]]

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
