---
tags: [type/proof, phase/2]
created: 2026-07-05
---

# Proof to myself: Linear and Logistic Regression

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate

1. Derive the closed-form solution for linear regression (normal equations).
2. Derive the gradient of the logistic regression loss.
3. Explain why sigmoid + cross-entropy is used instead of sigmoid + MSE.
4. Connect the linear decision boundary geometry to the QK circuit in transformer attention.

## What I produced from memory

### 1. Linear regression — closed-form

Loss: L(w) = (1/n) ||Xw - y||² = (1/n)(Xw - y)ᵀ(Xw - y)

Gradient: ∇_w L = (2/n) Xᵀ(Xw - y)

Set to zero: XᵀXw = Xᵀy → w = (XᵀX)⁻¹ Xᵀy

In practice, don't invert XᵀX directly — use SVD: X = UΣVᵀ → w = VΣ⁺Uᵀy where Σ⁺ inverts nonzero singular values.

### 2. Logistic regression gradient

Loss: L = -(1/n) Σ [y_i log(σ(X_i w)) + (1-y_i) log(1 - σ(X_i w))]

Gradient: ∇_w L = (1/n) Xᵀ(σ(Xw) - y)

Proof sketch: derivative of σ is σ(1-σ), chain rule gives cancellation that leaves the simple form.

### 3. Why sigmoid + cross-entropy?

Sigmoid + MSE produces a non-convex loss with vanishing gradients when σ(z) ≈ 0 or 1 (which is exactly where you want the strongest gradient, because the model is wrong). Cross-entropy + sigmoid = convex loss with gradient proportional to the error (σ(Xw) - y) — the gradient is large when the model is wrong and confident.

### 4. Connection to attention QK circuit

The logistic regression decision function f(X) = Xw + b defines a linear boundary.
A transformer's QK circuit computes QKᵀ — a matrix of dot products between queries and keys.
Each query position "decides" which keys to attend to via this dot product,
which is exactly a binary separation problem (softmax replaces sigmoid).
The weight direction in input space is analogous to the projection direction
defined by the Q and K weight matrices.

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
