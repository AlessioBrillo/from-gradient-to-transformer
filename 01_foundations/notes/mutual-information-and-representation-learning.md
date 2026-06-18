---
tags: [type/lesson, phase/1, state/review]
state: review
created: 2026-06-18
---

> **Series**: [Oxford Mathematics — Information Theory](https://youtube.com/playlist?list=PL4d5ZtfQonW3iAhXvTYCnoGEeRhxhKHMc&si=7FTfYrBynPzkFEzA) — Lecture 2: *Basic Properties of Information*
>
> **Also**: [StatQuest — Mutual Information, Clearly Explained](https://youtu.be/eJIp_mgVLwE) | [StatQuest — Entropy, Clearly Explained](https://youtu.be/YtebGVx-Fxw)

## What it is
Mutual information I(X; Y) measures how much knowing X reduces uncertainty about Y — the amount of information one variable contains about another. It is the KL divergence between the joint distribution and the product of marginals.

## Why it exists / what problem it solves
Correlation (Pearson's r) only captures linear relationships. Mutual information captures any kind of dependence — linear, nonlinear, periodic, categorical. It is the general-purpose measure of dependence, and it underpins modern representation learning objectives like the InfoNCE loss used in CLIP and contrastive learning.

## How it works

### Definition
I(X; Y) = D_KL(P(x, y) ‖ P(x)P(y)) = ΣΣ P(x, y) · log( P(x, y) / (P(x)P(y)) )

- I(X; Y) ≥ 0 — always non-negative, zero only when X and Y are independent.
- I(X; Y) = H(X) − H(X | Y) = H(Y) − H(Y | X) — reduction in uncertainty.
- Symmetric: I(X; Y) = I(Y; X).
- I(X; X) = H(X) — a variable contains all information about itself.

```python
import numpy as np

def mutual_information(x, y, bins=10):
    """Estimate MI between two continuous variables using binning."""
    # Discretize
    x_bins = np.digitize(x, np.histogram_bin_edges(x, bins=bins)[:-1])
    y_bins = np.digitize(y, np.histogram_bin_edges(y, bins=bins)[:-1])
    
    # Joint and marginal distributions
    c_xy = np.histogram2d(x_bins, y_bins, bins=bins)[0] + 1e-12
    p_xy = c_xy / c_xy.sum()
    p_x = p_xy.sum(axis=1, keepdims=True)
    p_y = p_xy.sum(axis=0, keepdims=True)
    
    # MI = KL( joint || product of marginals )
    mi = np.sum(p_xy * np.log(p_xy / (p_x @ p_y)))
    return mi

# Test: independent vs dependent
np.random.seed(42)
n = 1000
x = np.random.randn(n)
y_independent = np.random.randn(n)
y_dependent = x + np.random.randn(n) * 0.1  # noisy linear

print(f"MI(independent): {mutual_information(x, y_independent):.4f}")
print(f"MI(dependent):   {mutual_information(x, y_dependent):.4f}")
```

### MI vs Correlation
Correlation only captures linear dependence. Two variables can have correlation near zero but high mutual information (e.g., y = x² with x symmetric around 0).

```python
x = np.random.randn(1000)
y = x ** 2
print(f"Pearson r(x, x²): {np.corrcoef(x, y)[0, 1]:.4f}")
print(f"MI(x, x²):        {mutual_information(x, y):.4f}")
```

### Connection to representation learning (InfoNCE)
Modern contrastive learning methods learn representations by maximizing mutual information between views of the same data. The InfoNCE loss is a lower bound on MI:

L_InfoNCE = −log( exp(sim(z_i, z_j)) / Σ_k exp(sim(z_i, z_k)) )

where sim is cosine similarity. Maximizing this lower bound increases MI between positive pairs (augmented views of the same image, paired text-image in CLIP). This is why contrastive learning produces such good representations — it forces the model to preserve information that is shared across views while discarding instance-specific noise.

### The data processing inequality
If X → Y → Z (Markov chain), then I(X; Z) ≤ I(X; Y). Processing cannot create information — it can only preserve or destroy it. This has a sobering implication for deep learning: each layer of processing can only reduce the mutual information between the input and the final representation. Good architectures minimize this loss.

## Links
- [[01_foundations/notes/entropy-cross-entropy-and-kl-divergence|Entropy, Cross-Entropy, and KL Divergence]]
- [[01_foundations/notes/probability-basics-for-ml|Probability Basics for ML]]

## Insight
The InfoNCE loss — used in CLIP, SimCLR, and virtually every modern contrastive learning framework — is explicitly derived from mutual information maximization. When people say "CLIP learns aligned text-image representations by maximizing MI," they literally mean the loss function is a tractable lower bound on I(image; caption). The information theory foundations of modern deep
  learning are not theoretical abstraction — they are the actual loss functions running in production systems.
