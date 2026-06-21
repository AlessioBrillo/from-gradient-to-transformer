---
tags: [type/exercise, phase/1, state/consolidated]
skill: Information theory (entropy, cross-entropy, KL divergence)
state: consolidated
created: 2026-06-18
---

> **Series**: [Oxford Mathematics — Information Theory](https://youtube.com/playlist?list=PL4d5ZtfQonW3iAhXvTYCnoGEeRhxhKHMc&si=7FTfYrBynPzkFEzA)

## Goal / skill it demonstrates
Compute entropy, cross-entropy, and KL divergence by hand for simple distributions, then verify in NumPy. Connect cross-entropy to log-loss in classification. Understand why "minimizing cross-entropy" is the same as "maximizing log-likelihood."

## Part 1 — By hand

Given two distributions over 3 outcomes:

p = [0.5, 0.3, 0.2]
q = [0.4, 0.4, 0.2]

1. Compute H(p) — the entropy of p (in nats).
   H(p) = −0.5·ln(0.5) − 0.3·ln(0.3) − 0.2·ln(0.2)
        = 0.3466 + 0.3612 + 0.3219
        = 1.0297 nats

2. Compute H(p, q) — cross-entropy of q relative to p.
   H(p, q) = −0.5·ln(0.4) − 0.3·ln(0.4) − 0.2·ln(0.2)
           = 0.4581 + 0.2749 + 0.3219
           = 1.0549 nats

3. Compute D_KL(p ‖ q).
   D_KL = H(p, q) − H(p) = 1.0549 − 1.0297 = 0.0252 nats

Or equivalently: D_KL = 0.5·ln(0.5/0.4) + 0.3·ln(0.3/0.4) + 0.2·ln(0.2/0.2)
                     = 0.1116 + (−0.0864) + 0
                     = 0.0252 nats

## Part 2 — Verify in NumPy

```python
import numpy as np

def entropy(p):
    p = np.array(p)
    p = p[p > 0]
    return -np.sum(p * np.log(p))

def cross_entropy(p, q, eps=1e-15):
    p, q = np.array(p), np.array(q)
    q = np.clip(q, eps, 1 - eps)
    return -np.sum(p * np.log(q))

def kl_divergence(p, q, eps=1e-15):
    p, q = np.array(p), np.array(q)
    q = np.clip(q, eps, 1 - eps)
    return np.sum(p * np.log(p / q))

p = np.array([0.5, 0.3, 0.2])
q = np.array([0.4, 0.4, 0.2])

h_p = entropy(p)
ce_pq = cross_entropy(p, q)
kl_pq = kl_divergence(p, q)

print(f"H(p)        = {h_p:.4f} nats")
print(f"H(p, q)     = {ce_pq:.4f} nats")
print(f"D_KL(p||q)  = {kl_pq:.4f} nats")
print(f"Verify: H(p,q) - H(p) = {ce_pq - h_p:.4f} ≈ D_KL = {kl_pq:.4f}")
```

## Part 3 — Connect cross-entropy to classification loss

In a 3-class classification problem with true label y = 0 (one-hot: [1, 0, 0]) and predicted probabilities [0.7, 0.2, 0.1]:

- p = [1, 0, 0]  (true distribution, one-hot vector)
- q = [0.7, 0.2, 0.1]  (predicted distribution)

```python
# Classification setting
p_onehot = np.array([1.0, 0.0, 0.0])
q_pred = np.array([0.7, 0.2, 0.1])

ce_loss = cross_entropy(p_onehot, q_pred)
nll_loss = -np.log(0.7)  # negative log-likelihood of correct class
print(f"Cross-entropy loss:          {ce_loss:.4f}")
print(f"Negative log-likelihood:     {nll_loss:.4f}")
print(f"Match: {abs(ce_loss - nll_loss) < 1e-10}")
```

### Why they match
For a one-hot true distribution p where p(y_correct) = 1:

H(p, q) = −Σ p(x) · log q(x) = −1 · log q(y_correct) − 0 · ...

H(p, q) = −log q(y_correct)

This is exactly the negative log-likelihood of the correct class under the predicted distribution. **Cross-entropy loss = negative log-likelihood of the correct class.**

## Part 4 — Compare classification losses

Simulate two predictions for the same ground truth:

```python
import numpy as np

def classification_report(y_true, pred_probs):
    # pred_probs: shape (n_samples, n_classes)
    n = len(y_true)
    losses = []
    for i in range(n):
        p = np.zeros(pred_probs.shape[1])
        p[y_true[i]] = 1.0
        loss = cross_entropy(p, pred_probs[i])
        losses.append(loss)
    return np.mean(losses)

# Two classifiers on the same data
y_true = np.array([0, 1, 2, 0, 1])

preds_confident = np.array([
    [0.95, 0.03, 0.02],
    [0.02, 0.92, 0.06],
    [0.01, 0.04, 0.95],
    [0.88, 0.10, 0.02],
    [0.05, 0.90, 0.05],
])

preds_uncertain = np.array([
    [0.60, 0.30, 0.10],
    [0.25, 0.50, 0.25],
    [0.20, 0.30, 0.50],
    [0.55, 0.35, 0.10],
    [0.30, 0.55, 0.15],
])

print(f"Confident classifier CE: {classification_report(y_true, preds_confident):.4f}")
print(f"Uncertain classifier CE: {classification_report(y_true, preds_uncertain):.4f}")
print("The confident classifier has lower cross-entropy — better calibrated.")
```

## What I learned doing it

Cross-entropy is not an arbitrary choice for classification — it falls out naturally from information theory:
1. The true label is a one-hot distribution (all probability mass on the correct class).
2. Cross-entropy H(p_true, p_pred) measures how many bits we need to encode the true label using the predicted distribution.
3. Minimizing this forces the predicted distribution to concentrate probability on the correct class.

The equivalence between cross-entropy, negative log-likelihood, and KL divergence (up to a constant) means the same loss function has three interpretations:
- Information theory: minimizing coding inefficiency.
- Statistics: maximizing likelihood of the observed labels.
- Optimization: minimizing divergence between predicted and true distributions.

## Links
- [[01_foundations/notes/entropy-cross-entropy-and-kl-divergence]]
- [[01_foundations/notes/maximum-likelihood-estimation]]

## Linked skill
- [[00_meta/02_skill-tree]] → item: Information theory (entropy, cross-entropy, KL divergence)
