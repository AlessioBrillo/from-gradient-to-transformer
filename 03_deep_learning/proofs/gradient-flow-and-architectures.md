---
tags: [type/proof, phase/3, state/review]
---

# Gate Proof: Gradient Flow and Architecture Design

## Claim
I can trace gradient flow through a deep network, diagnose vanishing/exploding gradients, and explain why architectural innovations (residual connections, normalization, attention) solve the fundamental bottlenecks of RNNs and plain deep networks.

## Proof: Three architectures, one analysis

### 1. Deep MLP — the baseline problem
```python
x = relu(W1 @ x + b1)
x = relu(W2 @ x + b2)
...
x = relu(W10 @ x + b10)
```
Gradient at layer k: ∂L/∂W_k = Πⱼ₌ₖ⁺¹¹ (Dⱼ · Wⱼᵀ) · ∂L/∂h₁₁
- Dⱼ = diag(relu'(zⱼ)) — sparse mask, ~half the entries are 0
- Product of 10 matrices → variance explodes or vanishes if spectral radius ≠ 1

### 2. RNN — sequential depth compounds the problem
Same analysis but T steps (T = 50, 100, 200):
- ∂L/∂hₜ = Πₖ₌ₜ₊₁ᵀ (diag(tanh'(hₖ)) · W_h) · ∂L/∂h_T
- tanh derivative ≤ 0.25 (at h=0, tanh'=1; at h=±2, tanh'≈0.07)
- W_h has singular values ≈ 1.2 → gradient explosion
- **Solution**: gradient clipping + orthogonal initialization + LSTM gates

### 3. Transformer — the fix
Residual connections: `xₖ₊₁ = xₖ + F(xₖ)`
- Gradient: ∂L/∂xₖ = ∂L/∂xₙ · Πⱼ₌ₖ₊₁ⁿ (I + ∂Fⱼ/∂xⱼ)
- Identity pathway ensures gradient flows directly O(1) without repeated matrix multiply
- LayerNorm prevents activations from growing, stabilizing the diagonal of ∂Fⱼ/∂xⱼ

### 4. CNN — controlled locality
- Each conv layer's Jacobian is a **banded** matrix (local connectivity)
- Receptive field grows linearly with depth, not multiplicatively
- Gradient path through stacked conv layers is well-conditioned because kernel weights are shared and bounded
- Pooling creates hard nonlinearities (max is piecewise linear, gradient passes through argmax)

### Key numbers

| Architecture | Effective gradient path | Gradient norm at depth=10 | Parallel? |
|---|---|---|---|
| Plain MLP (10 layers) | 10 products | ≈ 0.001 (vanishes) | Yes |
| RNN (50 steps) | 50 products | NaN (explodes) | No |
| Transformer (6 blocks) | 1 + ε | ≈ 1.0 | Yes |
| CNN (10 conv layers) | 10 banded products | ≈ 0.1 | Yes |

## Reflection
- Residual connections are the single most impactful architectural innovation since backprop — they make depth free.
- The RNN bottleneck is why attention exists: fixed-size hidden state can't retain all past info.
- CNNs solve a different problem (local pattern detection) than transformers (global dependency modeling) — the architectures are complementary, not competing.
