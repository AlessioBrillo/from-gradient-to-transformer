---
tags: [type/lesson, phase/1, state/consolidated]
state: consolidated
created: 2026-06-18
---

> **Series**: [StatQuest with Josh Starmer](https://youtube.com/playlist?list=PLblh5JKOoLUIcdlgu78MnlATeyx4cEVeR&si=9Ro_rZjawyoy_Gz_)
>
> **Key episodes**: [Bayes' Theorem](https://youtu.be/9wCnvr7Xw4E) | [Regularization Part 1: L2 Ridge](https://youtu.be/Q81RR3yKn30) | [Regularization Part 2: L1 Lasso](https://youtu.be/NGf0voTMlcs) | [Ridge vs Lasso Visualized](https://youtu.be/Xm2C_gTAl8c) | [Regularization Part 3: Elastic Net](https://youtu.be/1dKRdX9bfIo)

## What it is
Bayesian thinking treats parameters as random variables with their own distributions. The prior encodes what we believe before seeing data; the posterior combines prior and data to produce an updated belief. Regularization in ML corresponds exactly to choosing a prior.

## Why it exists / what problem it solves
MLE finds the parameters that best explain the data. But what if we have prior knowledge? What if data is scarce? What if multiple parameter sets explain the data equally well? Bayesian methods address these cases by incorporating a prior distribution over parameters — constraining the solution space and preventing overfitting.

## How it works

### Bayes' theorem for parameter inference
P(θ | D) = P(D | θ) · P(θ) / P(D)

- P(θ) — **prior**: what we believe about θ before seeing data.
- P(D | θ) — **likelihood**: how probable the data is given θ (same as MLE).
- P(θ | D) — **posterior**: our updated belief after seeing data.
- P(D) — **evidence** (marginal likelihood): a normalizing constant.

### Maximum a Posteriori (MAP) estimation
Instead of maximizing likelihood, we maximize the posterior:

θ̂_MAP = argmax_θ P(θ | D) = argmax_θ [ log P(D | θ) + log P(θ) ]

The log-prior log P(θ) acts as a **regularization term** on the MLE objective.

### L2 regularization = Gaussian prior
If we place a Gaussian prior on weights w ~ N(0, 1/λ), then:

log P(w) = −(λ/2) ‖w‖² + constant

The MAP objective becomes: ℓ(w) − (λ/2) ‖w‖²

Maximizing this is equivalent to minimizing: NLL + (λ/2) ‖w‖²

**This is L2 regularization (weight decay).** The strength λ controls how much we trust the prior vs the data.

```python
# L2 regularization as Gaussian prior in linear regression
import numpy as np

def ridge_objective(X, y, w, lam):
    """Negative log-posterior for linear regression with Gaussian prior."""
    n = len(y)
    residuals = y - X @ w
    nll = 0.5 * np.sum(residuals ** 2) / n        # Gaussian MLE
    log_prior = -0.5 * lam * np.sum(w ** 2)       # Gaussian prior
    return -(nll + log_prior)  # return negative for minimization
```

### L1 regularization = Laplace prior
If we place a Laplace prior on weights (double-exponential), the log-prior is:

log P(w) = −(λ/2) · ‖w‖₁ + constant

This gives **L1 regularization (Lasso)** . The Laplace distribution has heavier tails than the Gaussian, placing less certainty that weights are exactly zero — paradoxically, this leads to sparse solutions where many weights become exactly zero.

| Prior | Regularization | Effect |
|-------|---------------|--------|
| Gaussian | L2 (weight decay) | Shrinks weights evenly, no sparsity |
| Laplace | L1 (Lasso) | Drives small weights to zero (sparsity) |

### The Bayesian workflow in practice
1. Start with a prior P(θ). Often uninformative (vague) if you have no strong beliefs.
2. Observe data D.
3. Compute (or approximate) the posterior P(θ | D).
4. Make predictions by averaging over the posterior — this gives **predictive uncertainty**.

Most modern deep learning does not do full Bayesian inference (the posterior over millions of weights is intractable). But the MAP view (= MLE + regularization) is standard practice, and techniques like **dropout as approximate Bayesian inference** (Gal & Ghahramani, 2016) reconnect deep learning to Bayesian principles.

```python
# MAP estimation of a Gaussian mean with conjugate prior
import numpy as np

# Prior: μ ~ N(μ0, σ0²)
# Likelihood: x_i ~ N(μ, σ²), known σ
# Posterior: μ|D ~ N(μ_n, σ_n²)

def gaussian_map(data, mu_prior=0.0, sigma_prior=1.0, sigma_likelihood=1.0):
    n = len(data)
    # Posterior mean: convex combination of prior mean and sample mean
    mu_n = ( (mu_prior / sigma_prior**2) + (data.mean() * n / sigma_likelihood**2) ) / \
           ( (1 / sigma_prior**2) + (n / sigma_likelihood**2) )
    # Posterior variance
    sigma_n = 1 / np.sqrt((1 / sigma_prior**2) + (n / sigma_likelihood**2))
    return mu_n, sigma_n

data = np.array([4.8, 5.2, 5.1, 4.9])
mu_map, sigma_map = gaussian_map(data)
print(f"MAP estimate: μ = {mu_map:.3f} ± {sigma_map:.3f}")
print(f"Sample mean: {data.mean():.3f}")
print(f"Note: MAP is pulled toward prior (0) when data is scarce")
```

## Links
- [[01_foundations/notes/maximum-likelihood-estimation|Maximum Likelihood Estimation]]
- [[01_foundations/notes/probability-basics-for-ml|Probability Basics for ML]]
- [[01_foundations/notes/entropy-cross-entropy-and-kl-divergence|Entropy, Cross-Entropy, and KL Divergence]]

## Insight
The Bayesian view reframes regularization: weight decay is not a hack to prevent overfitting — it is a principled consequence of placing a Gaussian prior on your weights.
L1 and L2 regularization correspond to different assumptions about the distribution of weights (Laplace vs Gaussian).
When you choose a regularizer, you are implicitly choosing a prior belief about how your model should behave.
This is why L2 is the default for deep networks: the Gaussian prior assumes most weights are small but non-zero, which matches the distributed representation hypothesis.
