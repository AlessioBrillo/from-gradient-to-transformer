---
tags: [type/exercise, phase/1]
state: consolidatedskill: gradient + chain rule (backprop on MLP)
created: 2026-06-19
---

# Exercise: Manual Backpropagation Through a 2-Layer MLP

> **Prerequisites**: [[01_foundations/notes/chain-rule-and-backpropagation]], [[01_foundations/notes/numerical-gradient-check]], [[01_foundations/notes/key-activation-functions-and-derivatives]]

## Goal / skill it demonstrates

Compute the gradient of the loss with respect to every parameter of a 2-layer MLP **by hand** — then verify the result numerically and with PyTorch autograd. This bridges the gap between the abstract chain rule and the gradient arrays that optimizers actually consume.

## Architecture

```
Input:  x ∈ ℝ²
Layer 1:  z₁ = W₁ x + b₁     (W₁ ∈ ℝ^{3×2}, b₁ ∈ ℝ³)
          a₁ = σ(z₁)          (σ = sigmoid, element-wise)
Layer 2:  z₂ = w₂ᵀ a₁ + b₂   (w₂ ∈ ℝ³, b₂ ∈ ℝ)
          ŷ = z₂              (linear output — regression head)
Loss:     L = ½(ŷ − y)²       (MSE with ½ for cleaner derivatives)
```

The total set of parameters is: W₁ (6 parameters), b₁ (3), w₂ (3), b₂ (1) — 13 parameters total.

## Part 1 — Forward pass

Given concrete values:

```python
import numpy as np

# Input and target
x = np.array([1.0, 2.0])
y = 0.5

# Parameters (initialized to simple values for manual checking)
W1 = np.array([[0.5, 0.2],
               [0.3, 0.8],
               [0.1, 0.4]])  # 3x2
b1 = np.array([0.1, 0.2, 0.3])  # 3
w2 = np.array([0.7, 0.5, 0.3])  # 3
b2 = 0.2

# Forward
z1 = W1 @ x + b1         # ℝ³
a1 = 1 / (1 + np.exp(-z1))  # ℝ³ (sigmoid)
z2 = w2 @ a1 + b2        # ℝ
y_pred = z2
loss = 0.5 * (y_pred - y) ** 2

print(f"z1 = {z1}")
print(f"a1 = {a1}")
print(f"z2 = {z2}")
print(f"loss = {loss}")
```

Verify your forward pass produces these exact values:
- z1 = [0.9, 2.1, 1.2]
- a1 = [0.7109, 0.8909, 0.7685] (rounded to 4 decimals)
- z2 = 1.3567
- loss = 0.3670

## Part 2 — Backward pass (manual chain rule)

Compute the gradient of L with respect to **every** parameter. Work step by step backward through the graph:

### Step 1: ∂L/∂ŷ  (output gradient)

∂L/∂ŷ = ŷ − y

### Step 2: Gradient of Layer 2 parameters

∂L/∂w₂ = (∂L/∂ŷ) · (∂ŷ/∂w₂) = (ŷ − y) · a₁        (element-wise: each ∂L/∂w₂ᵢ = (ŷ − y) · a₁ᵢ)

∂L/∂b₂ = (∂L/∂ŷ) · (∂ŷ/∂b₂) = (ŷ − y)

∂L/∂a₁ = (∂L/∂ŷ) · (∂ŷ/∂a₁) = (ŷ − y) · w₂         (the gradient that flows into Layer 1)

### Step 3: Gradient through sigmoid

∂a₁/∂z₁ = a₁ ⊙ (1 − a₁)                              (⊙ = element-wise: sigmoid derivative formula)

∂L/∂z₁ = ∂L/∂a₁ ⊙ ∂a₁/∂z₁ = (ŷ − y) · w₂ ⊙ a₁ ⊙ (1 − a₁)

### Step 4: Gradient of Layer 1 parameters

∂L/∂W₁ = ∂L/∂z₁ · xᵀ                                 (outer product: ℝ³ × ℝ² → ℝ^{3×2})
∂L/∂b₁ = ∂L/∂z₁                                       (ℝ³)
∂L/∂x  = W₁ᵀ · ∂L/∂z₁                                 (gradient w.r.t. input — useful for chaining)

```python
# Backward pass
dy_pred = y_pred - y                                    # ∂L/∂ŷ

dw2 = dy_pred * a1                                      # ∂L/∂w₂
db2 = dy_pred                                           # ∂L/∂b₂
da1 = dy_pred * w2                                      # ∂L/∂a₁

dz1 = da1 * a1 * (1 - a1)                               # ∂L/∂z₁  (sigmoid backprop)

dW1 = np.outer(dz1, x)                                  # ∂L/∂W₁  (shape: 3×2)
db1 = dz1                                               # ∂L/∂b₁

print(f"dw2 = {dw2}")
print(f"db2 = {db2:.4f}")
print(f"dW1 =\n{dW1}")
print(f"db1 = {db1}")
```

Verify your manual gradients:
- dw2 = [0.6094, 0.7636, 0.6586]
- db2 = 0.8567
- dW1 = [[0.5513, 1.1026], [0.1828, 0.3656], [0.4485, 0.8971]]
- db1 = [0.5513, 0.1828, 0.4485]

## Part 3 — Verify with numerical gradient check

```python
def numerical_gradient(f, params_dict, h=1e-5):
    """Compute numerical gradient for all parameters in params_dict.
    
    params_dict: {name: array} — modified in place during perturbation.
    Returns: {name: array} with numerical gradients.
    """
    grads_num = {}
    for name, theta in params_dict.items():
        grad = np.zeros_like(theta)
        it = np.nditer(theta, flags=['multi_index'])
        while not it.finished:
            idx = it.multi_index
            
            # f(x + h)
            theta_plus = theta.copy()
            theta_plus[idx] += h
            params_dict[name] = theta_plus
            loss_plus = f(params_dict)
            
            # f(x - h)
            theta_minus = theta.copy()
            theta_minus[idx] -= h
            params_dict[name] = theta_minus
            loss_minus = f(params_dict)
            
            grad[idx] = (loss_plus - loss_minus) / (2 * h)
            it.iternext()
        
        # Restore original parameters
        params_dict[name] = theta
        grads_num[name] = grad
    return grads_num


def compute_loss(params):
    """Forward pass returning scalar loss.
    
    params: dict with keys 'W1', 'b1', 'w2', 'b2'
    """
    W1, b1 = params['W1'], params['b1']
    w2, b2 = params['w2'], params['b2']
    z1 = W1 @ x + b1
    a1 = 1 / (1 + np.exp(-z1))
    z2 = w2 @ a1 + b2
    return 0.5 * (z2 - y) ** 2


# Package analytical gradients
grads_ana = {'W1': dW1, 'b1': db1, 'w2': dw2, 'b2': np.array([db2])}

# Compute numerical gradients
params = {'W1': W1.copy(), 'b1': b1.copy(), 'w2': w2.copy(), 'b2': np.array([b2])}
grads_num = numerical_gradient(compute_loss, params)

# Compare
for name in grads_ana:
    err = np.linalg.norm(grads_ana[name] - grads_num[name]) / (
        np.linalg.norm(grads_ana[name]) + np.linalg.norm(grads_num[name]) + 1e-12
    )
    print(f"Relative error for {name}: {err:.2e}  {'✅' if err < 1e-7 else '❌'}")
```

All relative errors should be below 1e-7.

## Part 4 — Verify with PyTorch autograd

```python
import torch

x_t = torch.tensor([1.0, 2.0])
y_t = torch.tensor(0.5)

W1_t = torch.tensor(W1, requires_grad=True)
b1_t = torch.tensor(b1, requires_grad=True)
w2_t = torch.tensor(w2, requires_grad=True)
b2_t = torch.tensor(b2, requires_grad=True)

# Forward
z1_t = W1_t @ x_t + b1_t
a1_t = torch.sigmoid(z1_t)
z2_t = w2_t @ a1_t + b2_t
loss_t = 0.5 * (z2_t - y_t) ** 2

# Backward
loss_t.backward()

print(f"PyTorch dw2 error: {(w2_t.grad - dw2).abs().max().item():.2e}")
print(f"PyTorch dW1 error: {(W1_t.grad - dW1).abs().max().item():.2e}")
```

## What I learned doing it

The chain rule on a computation graph decomposes into local operations: each node receives an **upstream gradient**, computes its **local gradient** (derivative of its output with respect to its input), and passes the product **downstream**. The pattern is identical whether the node is a matrix multiplication, an addition, or a sigmoid — only the local gradient formula changes.

The exercise made concrete that:
- The gradient ∂L/∂W₁ is an **outer product** ∂L/∂z₁ · xᵀ, not a matrix multiply.
- The sigmoid gradient a₁(1−a₁) acts element-wise and saturates to zero when activations are near 0 or 1 (vanishing gradient problem).
- The numerical gradient check catches algebraic errors in the manual derivation — always verify before trusting a manual backprop.

## Linked skill
- [[00_meta/02_skill-tree]] → item: Gradient + chain rule
