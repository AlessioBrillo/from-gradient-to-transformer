---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-18
---

> **Series**: [Oxford Mathematics — Information Theory](https://youtube.com/playlist?list=PL4d5ZtfQonW3iAhXvTYCnoGEeRhxhKHMc&si=7FTfYrBynPzkFEzA) — Lecture 1: *Defining Entropy and Information*
>
> **Also**: [StatQuest — Entropy, Clearly Explained](https://youtu.be/YtebGVx-Fxw) | [StatQuest — Mutual Information](https://youtu.be/eJIp_mgVLwE) | [StatQuest — Cross Entropy (Neural Networks Pt. 6)](https://youtu.be/6ArSys5qHAU) | [StatQuest — Cross Entropy Derivatives (NN Pt. 7)](https://youtu.be/xBEh66V9gZo)

## What it is
Entropy measures the average information content of a random variable — how many bits you need on average to encode a sample from its distribution. Cross-entropy and KL divergence extend this to compare two distributions, forming the foundation of every classification loss function in machine learning.

## Why it exists / what problem it solves
When building a classifier, we need a way to measure how different the predicted distribution is from the true distribution. Cross-entropy is exactly this measure. Understanding information theory explains:
- Why cross-entropy is the default loss for classification.
- Why minimizing cross-entropy is equivalent to minimizing KL divergence.
- Why "surprise" (negative log-probability) is the natural unit for loss.

## How it works

### Self-information (surprise)
An event with probability p has information content:

I(x) = −log₂(p)  (in bits) or I(x) = −ln(p)  (in nats)

A certain event (p = 1) carries 0 information. A rare event (p → 0) carries infinite information.

### Entropy
The entropy H(p) is the expected (average) self-information:

H(p) = E_p [−log p(x)] = −Σ p(x) · log p(x)

H(p) is the **lower bound** on how many bits are needed to encode samples from p optimally. A fair coin has H = 1 bit. A biased coin (p = 0.9) has H ≈ 0.47 bits — less uncertainty, fewer bits needed.

```python
import numpy as np

def entropy(p, base=np.e):
    """Compute entropy of a discrete distribution p."""
    p = np.array(p)
    p = p[p > 0]  # avoid log(0)
    return -np.sum(p * np.log(p)) / np.log(base)

# Uniform distribution: maximum entropy
uniform = np.ones(4) / 4
print(f"Uniform (4 outcomes): H = {entropy(uniform, base=2):.2f} bits")

# Skewed distribution: lower entropy
skewed = np.array([0.9, 0.05, 0.03, 0.02])
print(f"Skewed: H = {entropy(skewed, base=2):.2f} bits")
```

### Cross-Entropy
Cross-entropy measures the average number of bits needed to encode samples from p using a code optimized for q:

H(p, q) = −Σ p(x) · log q(x)

By definition: H(p, q) ≥ H(p). You always need at least as many bits using the wrong distribution. Equality holds only when p = q.

**This is the classification loss.** In a k-class classifier:
- p = true distribution (one-hot: 1 for the correct class, 0 otherwise).
- q = predicted probabilities.

H(p, q) = −log q(y_correct)

Minimizing cross-entropy = maximizing the predicted probability of the correct class.

```python
def cross_entropy(p, q, eps=1e-15):
    """Cross-entropy H(p, q)."""
    p, q = np.array(p), np.array(q)
    q = np.clip(q, eps, 1 - eps)
    return -np.sum(p * np.log(q))
```

### KL Divergence
KL divergence measures the "distance" from q to p:

D_KL(p ‖ q) = Σ p(x) · log(p(x) / q(x)) = H(p, q) − H(p)

It is the extra bits needed to encode samples from p using q instead of p. KL divergence is:
- **Non-negative**: D_KL ≥ 0 (Gibbs' inequality).
- **Zero only when p = q**.
- **Not symmetric**: D_KL(p ‖ q) ≠ D_KL(q ‖ p) — it is not a true metric.

In machine learning, we almost always minimize D_KL(p_data ‖ p_model), which is equivalent to minimizing cross-entropy (since H(p_data) is constant for fixed data).

```python
def kl_divergence(p, q, eps=1e-15):
    """D_KL(p || q)."""
    p, q = np.array(p), np.array(q)
    q = np.clip(q, eps, 1 - eps)
    return np.sum(p * np.log(p / q))
```

### The chain of relationships

D_KL(p ‖ q) = H(p, q) − H(p)

Since H(p) is fixed by the data: **minimizing cross-entropy ≡ minimizing KL divergence**.

Since D_KL ≥ 0: H(p) ≤ H(p, q). You can never beat the true entropy.

### Example by hand
Let p = [0.7, 0.2, 0.1] and q₁ = [0.6, 0.3, 0.1] and q₂ = [0.4, 0.4, 0.2].

- H(p) = −0.7·log(0.7) − 0.2·log(0.2) − 0.1·log(0.1) ≈ 0.356 nats (using base e)
- H(p, q₁) = −0.7·log(0.6) − 0.2·log(0.3) − 0.1·log(0.1) ≈ 0.381 nats
- H(p, q₂) = −0.7·log(0.4) − 0.2·log(0.4) − 0.1·log(0.2) ≈ 0.494 nats

q₁ is closer to p than q₂ (lower cross-entropy, lower KL divergence).

## Links
- [[01_foundations/notes/mutual-information-and-representation-learning|Mutual Information and Representation Learning]]
- [[01_foundations/notes/maximum-likelihood-estimation|Maximum Likelihood Estimation]]
- [[01_foundations/notes/probability-basics-for-ml|Probability Basics for ML]]

## Insight
Cross-entropy loss = negative log-likelihood of a categorical distribution = D_KL(one-hot ‖ predictions) + constant. Three different perspectives on exactly the same objective. Understanding this equivalence means you understand why classification works: you are measuring the "coding inefficiency" of using your predicted distribution q to represent the true distribution p, and minimizing that inefficiency forces q to match p.
