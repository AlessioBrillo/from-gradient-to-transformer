---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-18
---

> **Series**: [StatQuest with Josh Starmer](https://youtube.com/playlist?list=PLblh5JKOoLUIcdlgu78MnlATeyx4cEVeR&si=9Ro_rZjawyoy_Gz_)

## What it is
Probability theory quantifies uncertainty; statistics provides tools to infer properties of populations from samples. Random variables, distributions, expectation, and variance are the vocabulary of every loss function and evaluation metric in machine learning.

## Why it exists / what problem it solves
Machine learning is fundamentally about making decisions under uncertainty. We never see the true data-generating distribution — only finite samples. Probability gives us the language to describe:
- How likely is an outcome? (classification probabilities)
- How much does a quantity vary? (variance in predictions)
- How confident are we in an estimate? (confidence intervals, Bayesian uncertainty)

## How it works

### Random variables
A random variable X maps outcomes of a random process to numbers.

- **Discrete**: takes countable values (e.g., coin flip: {0, 1}).
- **Continuous**: takes values in a continuous range (e.g., height, temperature).

### Probability distributions
For a discrete variable, the probability mass function (PMF) P(X = x) sums to 1.
For a continuous variable, the probability density function (PDF) f(x) integrates to 1.

**Bernoulli**: P(X = 1) = p, P(X = 0) = 1 − p. A single coin flip. The building block of binary classification.

**Binomial**: n independent Bernoulli trials. Count of successes. Used in A/B testing, accuracy metrics.

**Categorical**: generalization of Bernoulli to k categories. The output distribution of a classifier with k classes.

**Gaussian (Normal)** : N(μ, σ²). The most important distribution in statistics. Central Limit Theorem: the sum of many independent random variables is approximately Gaussian, regardless of their individual distributions. This is why the Gaussian appears everywhere — from measurement error to weight initialization.

```python
import numpy as np

# Bernoulli samples
p = 0.7
samples = np.random.binomial(1, p, size=1000)
empirical_p = samples.mean()
print(f"Bernoulli(p={p}): empirical p = {empirical_p:.3f}")

# Gaussian samples
mu, sigma = 0.0, 1.0
samples = np.random.normal(mu, sigma, size=10000)
empirical_mean = samples.mean()
empirical_std = samples.std()
print(f"N({mu}, {sigma}²): empirical mean = {empirical_mean:.3f}, std = {empirical_std:.3f}")
```

### Expectation
The expectation E[X] is the probability-weighted average of all possible values.

- Discrete: E[X] = Σ x · P(X = x)
- Continuous: E[X] = ∫ x · f(x) dx

**Linearity of expectation**: E[aX + bY] = a·E[X] + b·E[Y] — this is true **always**, even if X and Y are dependent. This property is the superpower of expectation.

```python
# Empirical expectation
data = np.array([1, 2, 3, 4, 5])
probabilities = np.array([0.1, 0.2, 0.4, 0.2, 0.1])
expectation = np.sum(data * probabilities)
print(f"E[X] = {expectation}")
```

### Variance and covariance
Variance measures spread: Var(X) = E[(X − E[X])²] = E[X²] − E[X]².

Covariance measures how two variables move together:
Cov(X, Y) = E[(X − E[X])(Y − E[Y])] = E[XY] − E[X]E[Y].

The covariance matrix Σ_ij = Cov(X_i, X_j) is the fundamental object in PCA — its eigenvectors point to directions of maximum variance.

```python
# Covariance matrix
X = np.random.randn(100, 3)  # 100 samples, 3 features
cov = np.cov(X, rowvar=False)
print(f"Covariance matrix shape: {cov.shape}")
```

### Conditional probability and Bayes' theorem
P(A|B) = P(B|A) · P(A) / P(B)

This is the foundation of Bayesian inference: update your belief P(A) after observing evidence B to get P(A|B). In machine learning:
- P(A) is the **prior** — what you believed before seeing data.
- P(B|A) is the **likelihood** — how probable the data is under your hypothesis.
- P(A|B) is the **posterior** — your updated belief after seeing data.

## Links
- [[01_foundations/notes/maximum-likelihood-estimation|Maximum Likelihood Estimation]]
- [[01_foundations/notes/bayesian-thinking-and-regularization|Bayesian Thinking and Regularization]]
- [[01_foundations/notes/entropy-cross-entropy-and-kl-divergence|Entropy, Cross-Entropy, and KL Divergence]]

## Insight
The entire field of deep learning optimization can be framed in probability: minimize cross-entropy loss = maximize log-likelihood of the correct class under a categorical distribution. When you train a classifier with cross-entropy loss, you are implicitly assuming the data follows a categorical distribution and finding the parameters that make the observed data most probable. Every loss function is a negative log-likelihood in disguise.
