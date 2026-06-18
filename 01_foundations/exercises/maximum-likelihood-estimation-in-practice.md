---
tags: [type/exercise, phase/1]
skill: Probability and MLE
created: 2026-06-18
---

> **Series**: [StatQuest — Maximum Likelihood](https://youtu.be/XepXtl9YKwc) | [MLE — Exponential](https://youtu.be/p3T-_LMrvBc) | [MLE — Binomial](https://youtu.be/4KKV9yZCoM4) | [MLE — Normal](https://youtu.be/Dn6b9fCIUpM)

## Goal / skill it demonstrates
Implement Maximum Likelihood Estimation for three common distributions: Gaussian, Bernoulli, and Categorical. Verify that MLE recovers the true parameters from sampled data. Derive the connection between MLE and common loss functions.

## Part 1 — MLE for a Gaussian

Given data x₁, ..., xₙ assumed to come from N(μ, σ²), derive and implement the MLE:

μ̂ = (1/n) Σ x_i
σ̂² = (1/n) Σ (x_i − μ̂)²

```python
import numpy as np

def gaussian_mle(data):
    mu_hat = np.mean(data)
    sigma_hat = np.std(data)  # MLE uses n, not n-1
    return mu_hat, sigma_hat

# Test: recover known parameters
np.random.seed(42)
true_mu, true_sigma = 3.5, 1.2
data = np.random.normal(true_mu, true_sigma, size=10000)

mu_hat, sigma_hat = gaussian_mle(data)
print(f"True:  μ = {true_mu}, σ = {true_sigma}")
print(f"MLE:   μ̂ = {mu_hat:.4f}, σ̂ = {sigma_hat:.4f}")
print(f"Error: Δμ = {abs(mu_hat - true_mu):.4f}, Δσ = {abs(sigma_hat - true_sigma):.4f}")
```

## Part 2 — MLE for a Bernoulli

Given binary data y₁, ..., yₙ ∈ {0, 1} from Bernoulli(p):

p̂ = (1/n) Σ y_i = (number of successes) / (number of trials)

```python
def bernoulli_mle(data):
    return np.mean(data)

# Test
true_p = 0.7
data = np.random.binomial(1, true_p, size=5000)
p_hat = bernoulli_mle(data)
print(f"Bernoulli MLE: p̂ = {p_hat:.4f} (true p = {true_p})")

# Connection to binary cross-entropy:
# NLL = -Σ [y_i log(p̂) + (1-y_i) log(1-p̂)]
def binary_cross_entropy(y_true, y_pred):
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

nll = binary_cross_entropy(data, p_hat * np.ones_like(data))
print(f"NLL at MLE estimate: {nll:.4f}")
```

## Part 3 — MLE for a Categorical (multiclass classification)

Given k classes and counts c₁, ..., cₖ:

p̂_i = c_i / Σ c_j

```python
def categorical_mle(counts):
    counts = np.array(counts)
    return counts / counts.sum()

# Example: 3-class classification
counts = np.array([450, 320, 230])
p_hat = categorical_mle(counts)
print(f"Categorical MLE: p̂ = {p_hat.round(3)}")
print(f"Sum: {p_hat.sum():.3f} (should be 1.0)")

# Connection to cross-entropy loss:
# H(p_true, p_pred) = -Σ one_hot(y) · log(p_pred)
def cross_entropy_loss(y_true_onehot, y_pred):
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.sum(y_true_onehot * np.log(y_pred))

# One sample: true class = 0, predicted from MLE
y_true = np.array([1, 0, 0])
loss = cross_entropy_loss(y_true, p_hat)
print(f"Cross-entropy loss for class 0: {loss:.4f}")
print(f"NLL of correct class: {-np.log(p_hat[0]):.4f}")
```

## Part 4 — Likelihood surface visualization

Plot the negative log-likelihood as a function of μ for the Gaussian case. This shows visually that the MLE estimate is at the minimum of the NLL surface.

```python
import matplotlib.pyplot as plt

def nll_gaussian(data, mu):
    sigma = np.std(data)
    n = len(data)
    # NLL = (n/2) log(2πσ²) + (1/2σ²) Σ (x_i - μ)²
    nll = 0.5 * n * np.log(2 * np.pi * sigma ** 2)
    nll += 0.5 * np.sum((data - mu) ** 2) / (sigma ** 2)
    return nll

mu_range = np.linspace(1, 6, 100)
nll_values = [nll_gaussian(data, mu) for mu in mu_range]

plt.figure(figsize=(8, 4))
plt.plot(mu_range, nll_values)
plt.axvline(mu_hat, color='r', linestyle='--', label=f'MLE μ̂ = {mu_hat:.2f}')
plt.axvline(true_mu, color='g', linestyle=':', label=f'True μ = {true_mu}')
plt.xlabel('μ')
 plt.ylabel('Negative Log-Likelihood')
plt.legend()
plt.title('NLL surface for Gaussian MLE')
plt.grid(alpha=0.3)
```

## What I learned doing it

MLE recovers the true parameters reliably when the model is correctly specified. The NLL surface is convex for the Gaussian mean — a single global minimum at the sample mean.

The critical insight: **cross-entropy loss is exactly NLL under a categorical model**, and **MSE loss is exactly NLL under a Gaussian model**. Every loss function in supervised learning is a negative log-likelihood in disguise. This unifies all of supervised learning under a single probabilistic framework.

## Linked skill
- [[00_meta/02_skill-tree]] → item: Probability and MLE
