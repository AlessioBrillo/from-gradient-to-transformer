---
tags: [type/exercise, phase/3, state/review]
---

# Exercise 01 — Build micrograd: Autograd from Scratch

## Objective
Implement a minimal automatic differentiation engine in pure Python (no NumPy, no PyTorch). This is Karpathy's micrograd exercise — the single best way to understand backpropagation.

## Core Implementation
Build a `Value` class that supports:
- Construction: `Value(data, label="")`
- Arithmetic: `+`, `*`, `**`, `-`, `/`
- Activation: `tanh()`, `relu()`, `exp()`, `log()`
- Backward: `.backward()` computes gradients via reverse-mode autograd
- Graph visualization: `.draw()` to see the computation graph

## Key Operations to Implement

### Addition: z = a + b
```
z._op = '+'
z._prev = {a, b}
z._backward = lambda: (a.grad += z.grad, b.grad += z.grad)
```

### Multiplication: z = a * b
```
z._op = '*'
z._prev = {a, b}
z._backward = lambda: (a.grad += b.data * z.grad, b.grad += a.data * z.grad)
```

### Tanh: z = tanh(a)
```
z._op = 'tanh'
z._prev = {a}
z._backward = lambda: a.grad += (1 - z.data**2) * z.grad
```

## Test: Train a Neuron
Use your Value class to implement:
1. A single neuron: `w1*x1 + w2*x2 + b` → `tanh(output)`
2. Binary classification on synthetic circular data
3. Verify gradients match numerical gradient check (finite differences)

## Verification
```
# Numerical gradient check
def numerical_grad(f, x, eps=1e-6):
    return (f(x + eps) - f(x - eps)) / (2 * eps)
```

## Deliverables
- `Value` class implementation (in a file or notebook)
- Trained binary classifier with loss curve
- Numerical gradient verification (< 1e-4 error)
- Computation graph drawing for `3*x + 2*y + 1`

## Links

- [[03_deep_learning/notes/backpropagation-from-scratch]] — the theory note that this exercise builds as a code implementation.
- [[01_foundations/proofs/chain-rule-and-gradient-check]] — the chain rule derivation that micrograd's autograd engine implements in practice.


## Links

- [[03_deep_learning/notes/backpropagation-from-scratch]] — the theory behind the Value class you are building
- [[01_foundations/proofs/chain-rule-and-gradient-check]] — the numerical gradient check that verifies your autograd implementation
