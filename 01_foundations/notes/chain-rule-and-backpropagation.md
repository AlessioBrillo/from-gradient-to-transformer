---
tags: [type/lesson, phase/1, state/consolidated]
state: consolidated
created: 2026-06-18
---

> **Series**: [Essence of Calculus — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&si=UrW_Qk2DDRi0K3PQ) — Chapter 4: *Visualizing the chain rule and product rule*
>
> **Also**: [StatQuest — The Chain Rule, Clearly Explained](https://youtu.be/wl1myxrtQHQ) | [StatQuest — Gradient Descent, Step-by-Step](https://youtu.be/sDv4f4s2SB8) | [StatQuest — Backpropagation Main Ideas](https://youtu.be/IN2XmBhILt4) | [StatQuest — Backpropagation Details](https://youtu.be/iyn2zdALii8)

## What it is
The chain rule computes the derivative of a composite function. Backpropagation is the chain rule applied efficiently to neural networks — propagating error gradients from the output backward through every parameter.

## Why it exists / what problem it solves
Every neural network is a composition of hundreds or thousands of functions: layer after layer of linear transforms, activations, losses. Computing the gradient of the loss with respect to every parameter by differentiating the full expression symbolically is intractable. The chain rule decomposes the problem: compute local derivatives at each node and multiply them along the path from output to parameter.

## How it works

### Scalar chain rule
For f(x) = g(h(x)):

f'(x) = g'(h(x)) · h'(x)

"Derivative of the outer function, evaluated at the inner function, times the derivative of the inner function."

### Multivariable chain rule
If z = f(g₁(t), g₂(t), ..., gₙ(t)) where each g_i depends on t:

dz/dt = (∂f/∂g₁)·(dg₁/dt) + (∂f/∂g₂)·(dg₂/dt) + ... + (∂f/∂gₙ)·(dgₙ/dt)

This is a dot product of the gradient ∇f with the vector of derivatives dg/dt. Every internal node in a computation graph contributes a term.

### Vector chain rule (Jacobian form)
If f: ℝⁿ → ℝᵐ and g: ℝᵖ → ℝⁿ, then f∘g: ℝᵖ → ℝᵐ:

J_{f∘g}(x) = J_f(g(x)) · J_g(x)

where J is the Jacobian matrix of partial derivatives. The chain rule becomes matrix multiplication.

```python
import numpy as np

# Example: f(x, y) = sigmoid(ax + by + c)
# Let h = ax + by + c, then f = σ(h)
# By chain rule: ∂f/∂a = σ'(h) · x

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

# Forward pass
a, b, c = 0.5, -0.3, 0.1
x, y = 2.0, -1.0
h = a * x + b * y + c
f = sigmoid(h)

# Backward pass (chain rule)
df_dh = sigmoid_derivative(h)
dh_da = x
df_da = df_dh * dh_da  # chain rule: df/da = df/dh · dh/da
dh_db = y
df_db = df_dh * dh_db
dh_dc = 1.0
df_dc = df_dh * dh_dc

print(f"f = {f:.4f}")
print(f"df/da = {df_da:.4f} (via chain rule)")
```

### Backpropagation = chain rule on computation graphs
A computation graph represents the forward pass as a DAG. Backpropagation traverses the graph from output to inputs, computing gradients by:
1. Taking the gradient from the downstream node (closer to output).
2. Multiplying by the local Jacobian of the current node.
3. Passing the result upstream (closer to inputs).

This is **reverse-mode automatic differentiation**: one forward pass computes all values; one backward pass computes all gradients. Compare to forward-mode (which would need n passes for n parameters). Reverse-mode is what makes training deep networks feasible.

## Links
- [[01_foundations/notes/derivatives-and-gradient-descent|Derivatives and Gradient Descent]]
- [[01_foundations/notes/key-activation-functions-and-derivatives|Key Activation Functions and Their Derivatives]]
- [[01_foundations/notes/numerical-gradient-check|Numerical Gradient Check]]

## Insight
The term "backpropagation" is just marketing for "efficiently applying the chain rule." There is no new mathematics — only an engineering insight: compute local gradients during the forward pass (cache them), then multiply in reverse order. This is why frameworks like PyTorch separate `.forward()` (build graph + cache) from `.backward()` (traverse graph in reverse).
