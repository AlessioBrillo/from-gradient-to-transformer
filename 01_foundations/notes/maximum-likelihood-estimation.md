---
tags: [type/lesson, phase/1, state/review]
state: review
created: 2026-06-18
---

> **Series**: [StatQuest with Josh Starmer](https://youtube.com/playlist?list=PLblh5JKOoLUIcdlgu78MnlATeyx4cEVeR&si=9Ro_rZjawyoy_Gz_)
>
> **Key episodes**: [Probability vs Likelihood](https://youtu.be/pYxNSUDSFH4) | [Maximum Likelihood](https://youtu.be/XepXtl9YKwc) | [MLE — Exponential Distribution](https://youtu.be/p3T-_LMrvBc) | [MLE — Binomial](https://youtu.be/4KKV9yZCoM4) | [MLE — Normal Distribution](https://youtu.be/Dn6b9fCIUpM) | [R-squared Explained](https://youtu.be/2AQKmw14mHM)

## What it is
Maximum Likelihood Estimation (MLE) is a method for finding the parameters θ that make the observed data most probable under a chosen model: θ̂ = argmax_θ P(data | θ).

## Why it exists / what problem it solves
Given data and a parametric model (e.g., a Gaussian with unknown μ, σ, or a linear classifier with unknown weights w), how do we choose the parameters? MLE provides a principled, general-purpose answer: pick the parameters that assign the highest probability to the data you actually observed.

## How it works

### The likelihood function
Given i.i.d. data D = {x₁, ..., xₙ} and a parametric model P(x | θ), the likelihood is:

L(θ) = P(D | θ) = ∏_{i=1}^{n} P(x_i | θ)

We take the product because each data point is independent. In practice we maximize the **log-likelihood** (monotonic transform, turns product into sum):

ℓ(θ) = log L(θ) = Σ_{i=1}^{n} log P(x_i | θ)

### MLE for a Gaussian
Suppose x_i ~ N(μ, σ²). Then:

ℓ(μ, σ²) = Σ log [ (1 / √(2πσ²)) · exp(−(x_i − μ)² / (2σ²)) ]

Maximizing ℓ w.r.t. μ gives μ̂ = (1/n) Σ x_i — the sample mean.
Maximizing ℓ w.r.t. σ² gives σ̂² = (1/n) Σ (x_i − μ̂)² — the sample variance.

```python
import numpy as np

# Generate data from a known Gaussian
np.random.seed(42)
true_mu, true_sigma = 5.0, 2.0
data = np.random.normal(true_mu, true_sigma, size=1000)

# MLE estimates
mu_mle = data.mean()
sigma_mle = data.std()  # note: np.std uses n, not n-1 — this is MLE
print(f"True: μ={true_mu}, σ={true_sigma}")
print(f"MLE:  μ̂={mu_mle:.3f}, σ̂={sigma_mle:.3f}")
```

### MLE = minimizing negative log-likelihood
In optimization terms, we minimize the negative log-likelihood (NLL):

θ̂ = argmin_θ [−ℓ(θ)]

This is the bridge to loss functions. For Gaussian NLL:

−ℓ(μ, σ²) = (n/2) log(2πσ²) + (1 / 2σ²) Σ (x_i − μ)²

If σ² is constant, minimizing NLL is equivalent to minimizing Σ (x_i − μ)² — **mean squared error**.

For Categorical (classification) NLL:

−ℓ = −Σ y_i · log(p_i) — **cross-entropy loss**.

### MLE for linear regression
In linear regression, we assume y | x ~ N(w·x, σ²). The NLL becomes:

−ℓ(w) = (1/2σ²) Σ (y_i − w·x_i)² + constant

Minimizing this w.r.t. w is ordinary least squares. **Regression with MSE loss = MLE under Gaussian noise assumption.**

### MLE for classification (logistic regression)
We assume y | x ~ Bernoulli(σ(w·x)). The NLL is:

−ℓ(w) = −Σ [y_i log(σ(w·x_i)) + (1−y_i) log(1 − σ(w·x_i))]

This is **binary cross-entropy loss**. **Classification with cross-entropy loss = MLE under Bernoulli/Categorical assumption.**

```python
def negative_log_likelihood_binary(y_true, y_pred):
    """Binary cross-entropy = NLL of Bernoulli model."""
    return -np.mean(y_true * np.log(y_pred + 1e-15) + (1 - y_true) * np.log(1 - y_pred + 1e-15))
```

## Links
- [[01_foundations/notes/probability-basics-for-ml|Probability Basics for ML]]
- [[01_foundations/notes/bayesian-thinking-and-regularization|Bayesian Thinking and Regularization]]
- [[01_foundations/notes/entropy-cross-entropy-and-kl-divergence|Entropy, Cross-Entropy, and KL Divergence]]

## Insight
MLE unifies virtually every supervised learning loss function:
- MSE loss → Gaussian MLE
- Binary cross-entropy → Bernoulli MLE
- Categorical cross-entropy → Categorical MLE
- Poisson regression → Poisson MLE
- MAE (L1 loss) → Laplace MLE (more robust to outliers)

Understanding this connection means you never have to "memorize" loss functions again — you derive them from the distributional assumption of your choice.
