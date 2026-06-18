---
tags: [type/proof, phase/1]
created: 2026-06-18
---

# Proof to myself: Chain Rule and Gradient Check

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate
1. Explain the chain rule on paper and show how it applies to a composition of 3 functions.
2. Implement a numerical gradient check in ≤15 lines of NumPy.

## What I produced from memory

### 1. Explain the chain rule in plain English

The chain rule says: the derivative of a composition is the product of the derivatives of each constituent function, evaluated at the correct intermediate points.

Given f(x) = g(h(x)), the derivative is:
f'(x) = g'(h(x)) · h'(x)

"Derivative of outer, evaluated at inner, times derivative of inner."

For a composition of three functions f(x) = a(b(c(x))):
f'(x) = a'(b(c(x))) · b'(c(x)) · c'(x)

The pattern is recursive: start at the outermost function, differentiate it at its input (which is the result of everything inside), then multiply by the derivative of the next inner function, and so on until you reach x.

**Visual computation graph:**
```
x → c → c(x) → b → b(c(x)) → a → a(b(c(x)))
           ↑            ↑            ↑
         c'(x)       b'(c(x))      a'(b(c(x)))
                              ↓
                    Chain: a' · b' · c'
```

This is exactly backpropagation: the gradient flows backward through the graph, multiplying by the local derivative at each node.

### 2. Numerical gradient check from memory (≤15 lines of NumPy)

```python
import numpy as np

def numerical_gradient(f, x, h=1e-5):
    """Gradient of f at x via central differences."""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += h
        x_minus = x.copy()
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * h)
    return grad

def check_gradient(f, grad_analytic, x, eps=1e-12):
    grad_num = numerical_gradient(f, x)
    grad_ana = grad_analytic(x)
    err = np.linalg.norm(grad_ana - grad_num) / (np.linalg.norm(grad_ana) + np.linalg.norm(grad_num) + eps)
    return err

# Test on f(x) = x³sin(x²)
def f(x):
    return x[0]**3 * np.sin(x[0]**2)

def f_prime(x):
    return np.array([3*x[0]**2 * np.sin(x[0]**2) + x[0]**3 * 2*x[0] * np.cos(x[0]**2)])

x_test = np.array([1.5])
rel_err = check_gradient(f, f_prime, x_test)
assert rel_err < 1e-7, f"Gradient check failed: {rel_err:.2e}"
print(f"Gradient check PASSED (relative error = {rel_err:.2e})")
```
**(13 lines of NumPy code — inside the function bodies)**

The central difference formula (f(x+h) − f(x−h)) / (2h) is O(h²) accurate — much better than forward difference O(h). The relative error normalization ensures the check works for both tiny and huge gradient magnitudes.

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
