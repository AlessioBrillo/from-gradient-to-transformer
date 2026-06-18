---
tags: [type/exercise, phase/1, state/review]
skill: Probability and MLE
state: review
created: 2026-06-18
---

> **Series**: [StatQuest — Probability Distributions](https://youtu.be/oI3hZJqXJuc) | [Expected Values (Discrete)](https://youtu.be/KLs_7b7SKi4) | [Expected Values (Continuous)](https://youtu.be/OSPr6G6Ka-U)

## Goal / skill it demonstrates
Sample from common distributions, estimate expectations and covariances, and verify the law of large numbers and central limit theorem empirically. Build intuition for what probability concepts mean in code.

## Part 1 — Sampling and the Law of Large Numbers

Show that the sample mean converges to the true expectation as sample size increases.

```python
import numpy as np

def law_of_large_numbers_demo(distribution, true_mean, max_n=10000):
    sample_sizes = np.logspace(1, np.log10(max_n), 20).astype(int)
    errors = []
    for n in sample_sizes:
        sample = distribution(n)
        estimated_mean = np.mean(sample)
        errors.append(abs(estimated_mean - true_mean))
    return sample_sizes, errors

# Test with three distributions
np.random.seed(42)

# Standard normal: E[X] = 0
sizes, errors_normal = law_of_large_numbers_demo(
    lambda n: np.random.normal(0, 1, n), true_mean=0)

# Exponential(1): E[X] = 1
sizes, errors_exp = law_of_large_numbers_demo(
    lambda n: np.random.exponential(1, n), true_mean=1)

# Bernoulli(0.3): E[X] = 0.3
sizes, errors_bern = law_of_large_numbers_demo(
    lambda n: np.random.binomial(1, 0.3, n), true_mean=0.3)

print("Sample size vs estimation error:")
for i, s in enumerate(sizes):
    print(f"  n={s:5d}: normal err={errors_normal[i]:.5f}, "
          f"exp err={errors_exp[i]:.5f}, bern err={errors_bern[i]:.5f}")

# Verify: error ~ 1/√n
print(f"\nerror * sqrt(n) at n={sizes[-1]}:")
print(f"  Normal: {errors_normal[-1] * np.sqrt(sizes[-1]):.4f} (should be ~σ=1)")
```

## Part 2 — Central Limit Theorem

Sample means from any distribution are approximately normal. Verify visually.

```python
def central_limit_theorem_demo(pop_distribution, n_samples=1000, sample_size=30):
    """Draw sample_size samples, compute mean, repeat n_samples times."""
    means = np.array([np.mean(pop_distribution(sample_size)) for _ in range(n_samples)])
    return means

# CLT with exponential distribution (exponential is very non-normal)
np.random.seed(42)
exponential_means = central_limit_theorem_demo(
    lambda n: np.random.exponential(1, n),
    n_samples=5000, sample_size=30)

print(f"CLT demo: mean of sample means = {np.mean(exponential_means):.4f} (expected 1.0)")
print(f"CLT demo: std of sample means = {np.std(exponential_means):.4f} (expected 1/√30 ≈ 0.1826)")
```

## Part 3 — Covariance and correlation

Generate data with known covariance structure and verify that the empirical covariance matrix converges to the true one.

```python
def sample_covariance_demo(true_cov, n_samples=5000):
    """Sample from N(0, Σ) and estimate Σ."""
    mean = np.zeros(true_cov.shape[0])
    samples = np.random.multivariate_normal(mean, true_cov, size=n_samples)
    estimated_cov = np.cov(samples, rowvar=False)
    error = np.linalg.norm(estimated_cov - true_cov) / np.linalg.norm(true_cov)
    return estimated_cov, error

true_cov = np.array([[2.0, 0.8], [0.8, 1.0]])
est_cov, err = sample_covariance_demo(true_cov)
print(f"True covariance:\n{true_cov}")
print(f"Estimated covariance:\n{est_cov.round(3)}")
print(f"Relative error: {err:.4f}")
```

## Part 4 — Empirical expectation and variance

For a discrete random variable, compute expectation directly from the PMF and verify via sampling.

```python
def discrete_expectation(values, probs):
    """E[X] = Σ x · P(X=x)"""
    return np.sum(values * probs)

def discrete_variance(values, probs):
    """Var(X) = E[X²] - E[X]²"""
    e_x = discrete_expectation(values, probs)
    e_x2 = discrete_expectation(values ** 2, probs)
    return e_x2 - e_x ** 2

# Fair die
values = np.array([1, 2, 3, 4, 5, 6])
probs = np.ones(6) / 6

e_x = discrete_expectation(values, probs)
var_x = discrete_variance(values, probs)
print(f"Fair die: E[X] = {e_x}, Var[X] = {var_x:.4f}")

# Empirical verification
samples = np.random.choice(values, size=100000, p=probs)
print(f"Empirical: E[X] ≈ {np.mean(samples):.4f}, Var[X] ≈ {np.var(samples):.4f}")
```

## What I learned doing it

The Law of Large Numbers is not just theory — it's why training on more data gives better estimates. The Central Limit Theorem explains why Gaussian noise assumptions are often reasonable even when the underlying data is not Gaussian.

The covariance matrix estimation exercise clarifies why PCA needs enough samples: with n < p (more features than samples), the sample covariance matrix is rank-deficient and the eigenvalues are unreliable.

## Links
- [[01_foundations/notes/probability-basics-for-ml]]
- [[01_foundations/notes/bayesian-thinking-and-regularization]]

## Linked skill
- [[00_meta/02_skill-tree]] → item: Probability and MLE
