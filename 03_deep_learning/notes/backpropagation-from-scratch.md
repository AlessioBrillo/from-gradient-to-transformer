---
tags: [phase/3, note, state/review]
---

# Backpropagation from Scratch — Notes

## The Chain Rule (Scalar Case)
If z = f(y) and y = g(x), then dz/dx = dz/dy · dy/dx.

## The Chain Rule (Vector Case)
If z = f(y) and y = g(x) where y ∈ ℝᵐ, x ∈ ℝⁿ:
- ∂z/∂xⱼ = Σᵢ (∂z/∂yᵢ)(∂yᵢ/∂xⱼ)
- In matrix form: ∂z/∂x = (∂y/∂x)ᵀ · ∂z/∂y

## Reverse-Mode Autograd
The computation graph is built during the forward pass. Each node stores:
- Its value (`data`)
- Its children (`_prev`)
- The operation that produced it (`_op`)
- A local gradient function (`_backward`)

During backward pass:
1. Topologically sort the graph (children before parents)
2. Set output gradient = 1.0
3. Traverse in reverse topological order, calling each node's `_backward`

## Gradient of Common Operations

**Addition (z = a + b):** ∂z/∂a = 1, ∂z/∂b = 1
→ The backward function adds to both a.grad and b.grad

**Multiplication (z = a * b):** ∂z/∂a = b, ∂z/∂b = a
→ a.grad += b.data * out.grad; b.grad += a.data * out.grad

**Tanh (z = tanh(a)):** ∂z/∂a = 1 - tanh²(a)
→ a.grad += (1 - z²) * out.grad

**ReLU (z = max(0, a)):** ∂z/∂a = 1 if a > 0 else 0
→ a.grad += (out.data > 0) * out.grad

## Implementing a Neuron with Value
```python
# Neuron: w1*x1 + w2*x2 + b → tanh
w1 = Value(0.5); w2 = Value(-0.3); b = Value(0.1)
x1 = Value(2.0); x2 = Value(1.0)

output = (w1 * x1 + w2 * x2 + b).tanh()
output.backward()
print(w1.grad, w2.grad, b.grad)  # gradients for the optimizer
```

This is exactly what PyTorch does, scaled to millions of parameters.

## Links

- [[01_foundations/notes/chain-rule-and-backpropagation]] — the scalar and vector chain rule that underlies all of backprop
- [[03_deep_learning/exercises/ex-01-micrograd]] — build your own autograd engine (micrograd exercise)
- [[04_nlp_and_transformers/notes/qk-ov-circuits]] — how gradient flow through attention circuits enables the transformer
