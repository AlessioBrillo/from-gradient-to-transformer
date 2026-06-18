---
tags: [type/exercise, phase/1, state/review]
skill: Gradient + chain rule (gradient check)
state: review
created: 2026-06-18
---

> **Series**: [Essence of Calculus — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&si=UrW_Qk2DDRi0K3PQ)

## Goal / skill it demonstrates
Derive gradients analytically using the chain rule, then verify them numerically. This is the debugging skill that every deep learning practitioner uses when their model refuses to train — if you can gradient-check your implementation, you can find the bug.

## Setup

```python
import numpy as np
```

## Part 1 — Derive and verify a scalar function

Given f(x) = sin(x²) + ln(1 + x²):

1. Derive f'(x) using the chain rule.
   - Term 1: d/dx sin(x²) = cos(x²) · 2x
   - Term 2: d/dx ln(1 + x²) = 2x / (1 + x²)
   - f'(x) = 2x · cos(x²) + 2x / (1 + x²)

2. Implement f(x) and f'_analytic(x).

3. Implement f'_numeric(x) using central differences.

4. Compare at several values of x.

```python
def f_scalar(x):
    return np.sin(x ** 2) + np.log(1 + x ** 2)

def f_scalar_grad_analytic(x):
    return 2 * x * np.cos(x ** 2) + 2 * x / (1 + x ** 2)

def central_difference(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

# Test across multiple values
test_points = np.array([-2.0, -0.5, 0.0, 1.0, 3.0])
for x in test_points:
    analytic = f_scalar_grad_analytic(x)
    numeric = central_difference(f_scalar, x)
    err = abs(analytic - numeric) / (abs(analytic) + abs(numeric) + 1e-12)
    print(f"x = {x:+.1f}: analytic = {analytic:.8f}, numeric = {numeric:.8f}, rel_err = {err:.2e}")
    assert err < 1e-7, f"Failed at x={x}"
print("Part 1 PASSED ✓")
```

## Part 2 — Derive and verify a multivariable function

Given f(x, y) = (x² + y²) · sin(x) · e^{-y}:

1. Derive ∂f/∂x and ∂f/∂y by hand.

   ∂f/∂x = 2x · sin(x) · e^{-y} + (x² + y²) · cos(x) · e^{-y}

   ∂f/∂y = 2y · sin(x) · e^{-y} - (x² + y²) · sin(x) · e^{-y}

2. Implement and verify.

```python
def f_multi(v):
    x, y = v
    return (x ** 2 + y ** 2) * np.sin(x) * np.exp(-y)

def f_multi_grad_analytic(v):
    x, y = v
    ex = (x ** 2 + y ** 2) * np.exp(-y)
    df_dx = 2 * x * np.sin(x) * np.exp(-y) + ex * np.cos(x)
    df_dy = 2 * y * np.sin(x) * np.exp(-y) - ex * np.sin(x)
    return np.array([df_dx, df_dy])

def numerical_gradient(f, x, h=1e-5):
    """Gradient of f at d-dimensional point x using central differences."""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += h
        x_minus = x.copy()
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * h)
    return grad

def relative_error(analytic, numeric, eps=1e-12):
    return np.linalg.norm(analytic - numeric) / (np.linalg.norm(analytic) + np.linalg.norm(numeric) + eps)

# Test at several 2D points
test_2d = [np.array([0.5, 0.5]), np.array([1.0, 0.0]), np.array([-0.3, 2.0])]
for x in test_2d:
    ana = f_multi_grad_analytic(x)
    num = numerical_gradient(f_multi, x)
    err = relative_error(ana, num)
    print(f"x = {x}: rel_err = {err:.2e}")
    assert err < 1e-7, f"Failed at x={x}"
print("Part 2 PASSED ✓")
```

## Part 3 — Verify a softmax + cross-entropy gradient

Given logits z ∈ ℝᵏ and a true class index y, the cross-entropy loss is:

L(z) = −log( softmax(z)_y )

The gradient simplifies beautifully:

∂L/∂z_i = softmax(z)_i − 1(y == i)

i.e., the gradient is (predicted probability − true probability). Verify this numerically.

```python
def softmax(z):
    z = z - np.max(z)  # numerical stability
    e = np.exp(z)
    return e / np.sum(e)

def cross_entropy_loss(z, y):
    return -np.log(softmax(z)[y])

def ce_grad_analytic(z, y):
    p = softmax(z)
    grad = p.copy()
    grad[y] -= 1
    return grad

def ce_grad_numeric(z, y, h=1e-5):
    grad = np.zeros_like(z)
    for i in range(len(z)):
        z_plus = z.copy()
        z_plus[i] += h
        z_minus = z.copy()
        z_minus[i] -= h
        grad[i] = (cross_entropy_loss(z_plus, y) - cross_entropy_loss(z_minus, y)) / (2 * h)
    return grad

# Random test
np.random.seed(42)
for _ in range(5):
    z = np.random.randn(5)
    y = np.random.randint(0, 5)
    ana = ce_grad_analytic(z, y)
    num = ce_grad_numeric(z, y)
    err = relative_error(ana, num)
    print(f"z = {z.round(2)}, y = {y}: rel_err = {err:.2e}")
    assert err < 1e-7, f"CE gradient check failed"
print("Part 3 PASSED ✓")
```

## Part 4 — End-to-end gradient check (the Phase 1 gate pattern)

Write a single function `gradient_check(f, grad_analytic, x)` that:
1. Computes the numerical gradient using central differences.
2. Computes the analytical gradient.
3. Returns the relative error.
4. Asserts the error is below 1e-7.

This is the pattern you will reproduce from memory in the proof.

```python
def gradient_check(f, grad_analytic, x, h=1e-5, eps=1e-12):
    # Numerical gradient
    grad_num = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += h
        x_minus = x.copy()
        x_minus[i] -= h
        grad_num[i] = (f(x_plus) - f(x_minus)) / (2 * h)

    # Analytical gradient
    grad_ana = grad_analytic(x)

    # Relative error
    error = np.linalg.norm(grad_ana - grad_num) / (np.linalg.norm(grad_ana) + np.linalg.norm(grad_num) + eps)
    return error

# Verify on all functions from Parts 1-3
assert gradient_check(f_scalar, lambda x: np.array([f_scalar_grad_analytic(x[0])]), np.array([1.5])) < 1e-7
assert gradient_check(f_multi, f_multi_grad_analytic, np.array([1.0, 0.5])) < 1e-7

# The softmax+CE gradient
z_test = np.array([1.0, 2.0, 3.0])
y_test = 0
ce_loss = lambda z: cross_entropy_loss(z, y_test)
ce_grad = lambda z: ce_grad_analytic(z, y_test)
assert gradient_check(ce_loss, ce_grad, z_test) < 1e-7

print("All checks PASSED ✓ — gradient verification complete")
```

## What I learned doing it

The central-difference gradient check is surprisingly accurate — with h=1e-5, relative errors below 1e-7 are routine for well-implemented analytic gradients. The most common failure mode is a sign error in the chain rule.

The softmax + cross-entropy gradient is the most beautiful simplification in deep learning:
∂L/∂z_i = p_i − 1(i == y). One subtraction for the entire gradient. No complex derivative computation needed at the final layer — which is why every framework implements this fused operation (`CrossEntropyLoss` in PyTorch combines log-softmax + NLL loss).

The gradient check pattern (finite-difference approximation + relative error comparison) is the standard verification technique used by library authors themselves — PyTorch's `torch.autograd.gradcheck` does exactly this.

## Links
- [[01_foundations/notes/chain-rule-and-backpropagation]]
- [[01_foundations/notes/numerical-gradient-check]]

## Linked skill
- [[00_meta/02_skill-tree]] → item: Gradient + chain rule (gradient check)
