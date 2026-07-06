---
tags: [type/lesson, phase/2]
state: review
created: 2026-07-05
---

# Logistic Regression

## What it is
A linear model for binary classification that outputs a probability via the sigmoid function: P(y=1|X) = σ(Xw + b).

## Why it exists
Linear regression on binary labels produces unconstrained outputs. Logistic regression maps the linear output to [0, 1] and interprets it as a probability — the standard building block for classification.

## How it works

**Sigmoid function:**
σ(z) = 1 / (1 + e^(-z))

Transforms the real-valued decision function z = Xw + b into a probability.

**Cross-entropy loss:**
L = -y log(ŷ) - (1 - y) log(1 - ŷ)

Not MSE. Why? Because the sigmoid + MSE creates a non-convex loss with flat gradients. Cross-entropy + sigmoid = convex, with gradients proportional to the error (pred - true).

**Gradient:**
∇_w L = (1/n) Xᵀ(σ(Xw) - y)

Same form as linear regression, but with σ(Xw) instead of Xw — which means the gradient *automatically downweights* samples where the model is confident.

**Training in practice:**
```python
model = LogisticRegression(C=1.0)
model.fit(X, y, lr=0.1, epochs=2000)
```

## Decision boundary
The boundary σ(Xw + b) = 0.5 corresponds to Xw + b = 0 — a linear hyperplane in feature space. This is why "logistic regression" is a linear classifier despite its name.

## Regularization
L2 penalty (controlled by `C`, inverse of regularization strength) prevents coefficients from exploding on perfectly separable data — critical for numerical stability and generalization.

## MI Forward Link: classification geometry in attention

| LR Concept | MI Analogue |
|------------|-------------|
| Linear decision boundary | Attention separates token positions via linear QK/OV operations |
| Sigmoid probability | Softmax over vocabulary in the unembedding layer |
| Cross-entropy loss | Language modeling loss (identical functional form) |
| L2 regularization | Weight decay in transformers (same math, different name) |
| Feature weight magnitude | Logit lens projection magnitude per vocabulary token |

The key insight: **attention heads compute a linear separation in the residual stream**, analogous to how logistic regression separates classes. The QK circuit computes "which positions matter" (a separation problem), and the OV circuit computes "what to copy from those positions" (a regression problem). This is the core of the Elhage et al. QK/OV decomposition — see [[04_nlp_and_transformers/_MOC|Transformer Circuits]].

## Code reference
- [[../../../src/models/linear_model.py|src/models/linear_model.py]] — `LogisticRegression` class

## Links
- [[02_classical_ml/notes/linear-regression|Linear Regression]]
- [[01_foundations/notes/entropy-cross-entropy-and-kl-divergence|Cross-Entropy]]
- [[04_nlp_and_transformers/_MOC|Transformer Circuits (Phase 4)]]

## Open questions
- What happens with class imbalance? How should the loss change? (#question)
