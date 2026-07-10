---
tags: [type/lesson, phase/2, state/review]
---

# Naive Bayes

## Core idea
Apply Bayes' theorem with a **strong (naive) independence assumption**: features are conditionally independent given the class label.

```
P(y | x₁,...,xₙ) ∝ P(y) · Π P(xᵢ | y)
```

Despite the naive assumption, works well for:
- Text classification (bag-of-words features are approximately conditionally independent)
- Baseline / sanity check before complex models
- Low-data regimes where variance of a more complex model would dominate

## Variants
| Variant | P(xᵢ|y) distribution | When |
|---------|----------------------|------|
| Gaussian NB | Normal(μᵢy, σ²ᵢy) | Continuous features |
| Multinomial NB | Categorical count | Bag-of-words / TF-IDF |
| Bernoulli NB | Binary indicator | Presence/absence features |
| Complement NB | Multinomial, but on complement class | Imbalanced text data |

## Why it still works
The zero-one loss (classification accuracy) depends on whether the **argmax** is correct, not whether probabilities are well-calibrated. So correlated features don't hurt as long as the ranking P(y₁|x) > P(y₂|x) is preserved. Dependency cancellation: correlated features that push P(y₁|x) up also push P(y₂|x) up → ranking survives.

## Log-space computation
```python
log_posterior = log_prior + Σ log_likelihood(x_i | y)
```
Avoids underflow from multiplying many small probabilities.

## MI forward link
The naive Bayes independence assumption is the opposite of how transformers work: attention mechanisms explicitly model pairwise dependencies between all tokens. The contrast is instructive — where naive Bayes treats all features as independent evidence for a class, attention computes a weighted sum of feature interactions. Sparse autoencoders attempt to recover monosemantic features that behave like approximately independent "evidence" dimensions, a modern version of the naive Bayes factorization.

## References
- Murphy, *Probabilistic Machine Learning* (2022) — Ch. 4
- Ng & Jordan, *On Discriminative vs. Generative Classifiers* (NIPS 2001)
