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

## Solution

The full `Value` class is implemented at `src/training/micrograd.py` (161 lines). Key design:

- **`__add__` / `__mul__`**: store `(self, other)` as children, define `_backward` closures that accumulate gradients via `self.grad += out.grad * (∂out/∂self)`.
- **`tanh` / `relu` / `exp` / `log` / `sigmoid`**: unary operations with analytic derivative in `_backward`.
- **`backward()`**: topological sort via DFS, then processes nodes in reverse order calling `_backward()`.

### Usage: Train a Binary Classifier
```python
from src.training.micrograd import Value
import random, math

# Synthetic circular data
def make_circular_data(n=100):
    xs, ys = [], []
    for _ in range(n):
        angle = random.random() * 2 * math.pi
        radius = random.random()
        x1, x2 = radius * math.cos(angle), radius * math.sin(angle)
        label = 1 if radius > 0.5 else -1
        xs.append([x1, x2]); ys.append(label)
    return xs, ys

data, labels = make_circular_data(100)

# Neuron: w1*x1 + w2*x2 + b → tanh
w1 = Value(random.uniform(-1, 1), label="w1")
w2 = Value(random.uniform(-1, 1), label="w2")
b = Value(0.0, label="b")

for step in range(100):
    total_loss = Value(0.0)
    for xi, yi in zip(data, labels):
        pred = (w1 * xi[0] + w2 * xi[1] + b).tanh()
        loss = (pred - yi) ** 2
        total_loss = total_loss + loss
    total_loss.backward()
    for p in [w1, w2, b]:
        p.data -= 0.1 * p.grad
        p.grad = 0.0
    if step % 20 == 0:
        print(f"step {step}: loss = {total_loss.data:.4f}")
```

### Numerical Gradient Verification
```python
def numerical_grad(f, x, eps=1e-6):
    return (f(x + eps) - f(x - eps)) / (2 * eps)

# Verifies that autograd matches finite differences to < 1e-4
```

Expected result: `|autograd_grad - numerical_grad| < 1e-4` for all parameters.

## Deliverables
- `Value` class implementation (in a file or notebook)
- Trained binary classifier with loss curve
- Numerical gradient verification (< 1e-4 error)
- Computation graph drawing for `3*x + 2*y + 1`

## Links

- [[03_deep_learning/notes/backpropagation-from-scratch]] — the theory note that this exercise builds as a code implementation.
- [[01_foundations/proofs/chain-rule-and-gradient-check]] — the chain rule derivation that micrograd's autograd engine implements in practice.
