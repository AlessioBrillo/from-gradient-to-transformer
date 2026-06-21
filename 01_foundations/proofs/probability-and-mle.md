---
tags: [type/proof, phase/1, state/consolidated]
state: consolidated
created: 2026-06-18
---

# Proof to myself: Probability, MLE, and Bayesian Thinking

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate
1. Explain Maximum Likelihood Estimation and derive MLE for a Gaussian.
2. Explain the connection between MLE and common loss functions (MSE, cross-entropy).
3. Explain Bayesian thinking and how regularization emerges from a prior.

## What I produced from memory

### 1. What is MLE?

MLE finds the parameters θ that maximize the probability of observing the data:

θ̂ = argmax_θ P(data | θ) = argmax_θ ∏_{i=1}^{n} P(x_i | θ)

In practice, we maximize the log-likelihood (product becomes sum, monotonic transform):

ℓ(θ) = Σ log P(x_i | θ)

Equivalently, minimize the negative log-likelihood (NLL).

### 2. MLE for a Gaussian

Assume x_i ~ N(μ, σ²). The log-likelihood is:

ℓ(μ, σ²) = Σ log [ 1 / √(2πσ²) · exp(−(x_i − μ)² / (2σ²)) ]
         = −(n/2) log(2πσ²) − (1 / 2σ²) Σ (x_i − μ)²

Maximize w.r.t. μ: set derivative to 0 → μ̂ = (1/n) Σ x_i (sample mean)
Maximize w.r.t. σ²: σ̂² = (1/n) Σ (x_i − μ̂)² (sample variance, with n not n-1)

If σ is fixed, maximizing ℓ is equivalent to minimizing Σ (x_i − μ)² — **MSE loss**.

### 3. MLE for classification (Categorical)

Assume y_i ~ Categorical(p₁, ..., pₖ). The NLL is:

−ℓ = −Σ Σ one_hot(y_i)_j · log(p_j) = cross-entropy loss

This is the same as the information theory perspective: cross-entropy H(p, q) measures the coding inefficiency of using q to encode p.

### 4. Bayesian thinking

Bayes' theorem: P(θ | D) = P(D | θ) · P(θ) / P(D)

- P(θ) is the prior (what I believe before seeing data).
- P(D | θ) is the likelihood (same as MLE).
- P(θ | D) is the posterior (updated belief after data).

MAP estimation: maximize the posterior instead of just the likelihood:

θ̂_MAP = argmax_θ [log P(D | θ) + log P(θ)]

The log-prior is a regularization term:
- Gaussian prior on w → log P(w) = −(λ/2) ‖w‖² → L2 regularization (weight decay).
- Laplace prior on w → log P(w) = −(λ/2) ‖w‖₁ → L1 regularization (sparsity).

So weight decay is not a hack — it is the consequence of assuming weights are Gaussian-distributed around zero.

### 5. Code from memory

```python
import numpy as np

def gaussian_mle(data):
    mu = np.mean(data)
    sigma = np.std(data)  # MLE
    return mu, sigma

def bernoulli_mle(data):
    return np.mean(data)

def binary_cross_entropy(y_true, y_pred):
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

# Verify: MLE minimizes cross-entropy
y = np.random.binomial(1, 0.7, 1000)
p_mle = bernoulli_mle(y)
loss_at_mle = binary_cross_entropy(y, p_mle)
loss_at_wrong = binary_cross_entropy(y, 0.5)
print(f"MLE p̂ = {p_mle:.3f}, CE = {loss_at_mle:.4f}")
print(f"Wrong p = 0.5, CE = {loss_at_wrong:.4f}")
# The MLE estimate gives LOWER cross-entropy (better)
```

## Links
- [[01_foundations/notes/probability-basics-for-ml]]
- [[01_foundations/notes/maximum-likelihood-estimation]]

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
