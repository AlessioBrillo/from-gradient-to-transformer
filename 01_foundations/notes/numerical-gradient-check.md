---
tags: [type/lesson, phase/1, state/review]
state: review
created: 2026-06-18
---

> **Series**: [Essence of Calculus — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&si=UrW_Qk2DDRi0K3PQ) — Chapter 2: *The paradox of the derivative* (limits/finite differences intuition)

## What it is
The numerical gradient check approximates the true gradient using finite differences, providing an independent verification that your analytical gradient (or backpropagation) implementation is correct.

## Why it exists / what problem it solves
When implementing backpropagation by hand, it is easy to make sign errors, miss a term in the chain rule, or transpose a matrix incorrectly. The numerical gradient check catches these errors: compare your analytical gradient against a finite-difference approximation. If the relative error is below 1e-7, your backprop is correct.

## How it works

### Finite difference approximations
**Forward difference:** f'(x) ≈ (f(x + h) − f(x)) / h — O(h) error.

**Central difference (preferred):** f'(x) ≈ (f(x + h) − f(x − h)) / (2h) — O(h²) error. Twice as accurate for the same h.

```python
import numpy as np

def numerical_gradient(f, x, h=1e-5):
    """Compute gradient of f at x using central differences."""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += h
        x_minus = x.copy()
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * h)
    return grad
```

### Relative error
Compute the relative error between analytical and numerical gradients:

error = ‖analytical − numerical‖ / (‖analytical‖ + ‖numerical‖ + ε)

Using the relative error is essential: an absolute error of 1e-10 means different things when gradients are of magnitude 1e-2 vs 1e+6.

```python
def gradient_check(analytical_grad, numerical_grad, eps=1e-12):
    numerator = np.linalg.norm(analytical_grad - numerical_grad)
    denominator = np.linalg.norm(analytical_grad) + np.linalg.norm(numerical_grad) + eps
    return numerator / denominator
```

### Interpreting the error

| Relative error | Meaning |
|----------------|---------|
| < 1e-7 | Perfect — your analytical gradient is correct |
| < 1e-5 | Acceptable for float32 training |
| 1e-3 to 1e-1 | Likely a bug in your backprop |
| > 1e-1 | Almost certainly a bug |

### Choosing h
h = 1e-5 is a safe default for float64. For float32, use h = 1e-3 (float32 has only ~7 decimal digits of precision). Too small h causes catastrophic cancellation; too large h increases truncation error.

### Full example

```python
import numpy as np

def f(x):
    """A composite function for testing."""
    return np.sin(x[0] ** 2) + np.log(1 + x[1] ** 2)

def analytical_gradient(x):
    """Gradient computed via chain rule by hand."""
    grad = np.zeros_like(x)
    grad[0] = 2 * x[0] * np.cos(x[0] ** 2)      # df/dx = 2x · cos(x²)
    grad[1] = 2 * x[1] / (1 + x[1] ** 2)        # df/dy = 2y / (1 + y²)
    return grad

x0 = np.array([1.5, 0.8])
num_grad = numerical_gradient(f, x0)
ana_grad = analytical_gradient(x0)
rel_err = gradient_check(ana_grad, num_grad)

print(f"Analytical gradient: {ana_grad}")
print(f"Numerical gradient:  {num_grad}")
print(f"Relative error:      {rel_err:.2e}")
assert rel_err < 1e-7, f"Gradient check failed: {rel_err:.2e}"
print("Gradient check PASSED ✓")
```

## Links
- [[01_foundations/notes/derivatives-and-gradient-descent|Derivatives and Gradient Descent]]
- [[01_foundations/notes/chain-rule-and-backpropagation|Chain Rule and Backpropagation]]
- [[01_foundations/notes/key-activation-functions-and-derivatives|Key Activation Functions and Their Derivatives]]

## Insight
The numerical gradient check is the unit test for backpropagation. In production deep learning frameworks, it is used during development to verify custom layers (PyTorch's `torch.autograd.gradcheck`). It cannot replace analytical gradients during training (too slow — O(n) forward passes per parameter), but it is the single most effective debugging tool when your model refuses to
  converge and you suspect a gradient bug.
