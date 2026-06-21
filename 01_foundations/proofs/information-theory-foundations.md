---
tags: [type/proof, phase/1, state/consolidated]
state: consolidated
created: 2026-06-18
---

# Proof to myself: Information Theory Foundations

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate
1. Define entropy, cross-entropy, and KL divergence from memory.
2. Show their relationships: D_KL = H(p,q) − H(p).
3. Connect cross-entropy to classification loss and log-likelihood.

## What I produced from memory

### 1. Entropy H(p)

Entropy measures the average information content (surprise) of a random variable:

H(p) = −Σ p(x) · log p(x)

It is the lower bound on how many bits (log base 2) or nats (log base e) are needed to encode samples from p. A uniform distribution has maximum entropy (highest uncertainty). A deterministic distribution (one outcome with p = 1) has entropy 0.

### 2. Cross-entropy H(p, q)

Cross-entropy measures the average number of bits needed to encode samples from p using q's encoding:

H(p, q) = −Σ p(x) · log q(x)

By Gibbs' inequality: H(p, q) ≥ H(p) always. Equality only when p = q.

### 3. KL Divergence D_KL(p ‖ q)

KL divergence is the extra bits needed to encode p using q instead of p:

D_KL(p ‖ q) = Σ p(x) · log(p(x) / q(x)) = H(p, q) − H(p)

Properties:
- D_KL ≥ 0 (non-negative)
- D_KL = 0 iff p = q
- Not symmetric: D_KL(p ‖ q) ≠ D_KL(q ‖ p)

### 4. Connection to classification

In classification with one-hot labels (p is all mass on correct class):

H(p, q) = −1 · log(q(correct)) − 0 · log(others) = −log(q(correct))

This is the **negative log-likelihood** of the correct class. Minimizing cross-entropy = maximizing the probability of the correct class = MLE of a categorical distribution.

Since H(p) is constant for fixed data:
minimizing H(p, q) ≡ minimizing D_KL(p_data ‖ p_model)

So classification training is: find the model distribution q that is as close as possible to the empirical data distribution p_data, as measured by KL divergence.

### 5. Code from memory

```python
import numpy as np

def entropy(p):
    p = np.array(p)
    p = p[p > 0]
    return -np.sum(p * np.log(p))

def cross_entropy(p, q):
    p, q = np.array(p), np.array(q)
    q = np.clip(q, 1e-15, 1 - 1e-15)
    return -np.sum(p * np.log(q))

def kl_divergence(p, q):
    return cross_entropy(p, q) - entropy(p)

# Verification
p = np.array([0.7, 0.2, 0.1])
q = np.array([0.6, 0.3, 0.1])

print(f"H(p)      = {entropy(p):.4f}")
print(f"H(p, q)   = {cross_entropy(p, q):.4f}")
print(f"KL(p||q)  = {kl_divergence(p, q):.4f}")
print(f"Verify: H(p,q) - H(p) = {cross_entropy(p, q) - entropy(p):.4f}")

# Classification setting (one-hot)
p_onehot = np.array([1.0, 0.0, 0.0])
q_pred = np.array([0.7, 0.2, 0.1])
ce_loss = cross_entropy(p_onehot, q_pred)
nll = -np.log(0.7)
print(f"\nClassification: CE = {ce_loss:.4f}, NLL = {nll:.4f}")
```

## Links
- [[01_foundations/notes/entropy-cross-entropy-and-kl-divergence]]
- [[01_foundations/notes/mutual-information-and-representation-learning]]

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
