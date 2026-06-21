---
tags: [type/exercise, phase/1]
state: consolidatedskill: singular value decomposition
created: 2026-06-19
---

# Exercise: SVD Image Compression

> **Prerequisites**: [[01_foundations/notes/singular-value-decomposition]], [[01_foundations/notes/numpy-basics-for-linear-algebra]]

## Goal / skill it demonstrates

Apply SVD to compress a grayscale image, demonstrating the Eckart–Young theorem in practice: the best rank-k approximation of the image matrix, the tradeoff between compression ratio and reconstruction error, and the visual effect of discarding singular values. This connects linear algebra (SVD) to a concrete engineering application.

## Setup

```python
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO
```

## Part 1 — Load image as grayscale matrix

```python
# Load a test image (you can substitute any image URL or local path)
url = "https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content)).convert("L")  # grayscale
A = np.array(img, dtype=float)
m, n = A.shape
print(f"Image shape: {A.shape}")  # typically 512×512
print(f"Total pixels: {m * n}")
```

If you prefer a local image, load with:
```python
from PIL import Image
img = Image.open("path/to/your/image.jpg").convert("L")
A = np.array(img, dtype=float)
```

## Part 2 — Compute SVD and examine singular values

```python
U, S, Vt = np.linalg.svd(A, full_matrices=False)
print(f"U shape: {U.shape}")
print(f"S length: {len(S)}")
print(f"Vt shape: {Vt.shape}")

# Plot singular values
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(S, marker='.')
plt.yscale('log')
plt.title("Singular values (log scale)")
plt.xlabel("Index")
plt.ylabel("σᵢ")

plt.subplot(1, 2, 2)
cumulative = np.cumsum(S ** 2) / np.sum(S ** 2)
plt.plot(cumulative, marker='.')
plt.axhline(0.9, color='r', linestyle='--', label='90% variance')
plt.axhline(0.99, color='g', linestyle='--', label='99% variance')
plt.title("Cumulative explained variance")
plt.xlabel("Number of singular values")
plt.ylabel("Fraction of variance")
plt.legend()
plt.tight_layout()
```

**Questions:**
- How many singular values are needed to capture 90% of the image variance? 99%?
- What is the ratio of the largest to smallest singular value (condition number)? What does this tell you about the image?
- Are there any zero singular values? What would it mean if there were?

## Part 3 — Reconstruct at various ranks

```python
def low_rank_approx(U, S, Vt, k):
    """Return the rank-k approximation."""
    return U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

ranks = [1, 5, 10, 20, 50, 100, 200, min(m, n)]
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.ravel()

for idx, k in enumerate(ranks):
    Ak = low_rank_approx(U, S, Vt, k)
    mse = np.mean((A - Ak) ** 2)
    compression_ratio = (k * (m + n)) / (m * n)

    axes[idx].imshow(Ak, cmap="gray", vmin=0, vmax=255)
    axes[idx].set_title(f"k = {k}\nMSE = {mse:.1f}\nRatio = {compression_ratio:.3f}")
    axes[idx].axis("off")

plt.tight_layout()
```

## Part 4 — Compression analysis

```python
# Storage: original = m*n floats
# Storage: rank-k = k*(m + n + 1) floats (U[:,:k], Vt[:k,:], S[:k])
# But S is typically stored as vector, so: k*m + k + k*n = k*(m + n + 1)

k_values = np.arange(1, min(m, n), 5)
mse_values = []
ratio_values = []

for k in k_values:
    Ak = low_rank_approx(U, S, Vt, k)
    mse_values.append(np.mean((A - Ak) ** 2))
    ratio_values.append(k * (m + n + 1) / (m * n))

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(k_values, mse_values)
plt.title("Reconstruction error vs. rank")
plt.xlabel("k (rank)")
plt.ylabel("MSE")
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(ratio_values, mse_values)
plt.scatter([r for r in ratio_values if r < 0.5],
            [mse_values[i] for i, r in enumerate(ratio_values) if r < 0.5],
            color='r', s=30, label='k < 0.5× storage')
plt.title("MSE vs. compression ratio")
plt.xlabel("Compression ratio (stored / original)")
plt.ylabel("MSE")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
```

**Questions:**
- What rank gives a 10× compression (ratio ≈ 0.1)? What is the visual quality and MSE at that rank?
- Is the MSE-vs-ratio curve monotonic? Why or why not?
- Why do we store U_k (m×k), Σ_k (k), V_kᵀ (k×n) instead of just A_k directly?
- How would the result differ for a color image? (Hint: 3 channels → 3 SVDs.)

## Part 5 — Noise removal via truncated SVD

Small singular values often correspond to high-frequency noise. Truncating them acts as a denoiser.

```python
np.random.seed(42)
noise = np.random.randn(m, n) * 25  # Gaussian noise, std=25 pixel values
A_noisy = np.clip(A + noise, 0, 255)

U_n, S_n, Vt_n = np.linalg.svd(A_noisy, full_matrices=False)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(A, cmap="gray", vmin=0, vmax=255)
axes[0].set_title("Original")
axes[0].axis("off")

axes[1].imshow(A_noisy, cmap="gray", vmin=0, vmax=255)
axes[1].set_title(f"Noisy (σ=25)")
axes[1].axis("off")

# Find k that minimizes MSE between denoised and original
k_best = 1
best_mse = float("inf")
for k in range(1, min(m, n), 10):
    Ak = low_rank_approx(U_n, S_n, Vt_n, k)
    mse = np.mean((A - Ak) ** 2)
    if mse < best_mse:
        best_mse = mse
        k_best = k

A_denoised = low_rank_approx(U_n, S_n, Vt_n, k_best)
axes[2].imshow(A_denoised, cmap="gray", vmin=0, vmax=255)
axes[2].set_title(f"Denoised (k={k_best}, MSE={best_mse:.1f})")
axes[2].axis("off")
plt.tight_layout()
```

**Question:** Why does truncating SVD remove noise? Why does too-aggressive truncation (very small k) lose signal as well?

## What I learned doing it

SVD image compression demonstrates the Eckart–Young theorem visually: the reconstructed image at rank k is
the optimal rank-k approximation of the original, and the error equals the sum of squares of the discarded
singular values. The elbow in the singular value spectrum tells you the "effective rank" of the image — the
number of independent degrees of freedom needed to represent it at the desired fidelity.

The denoising experiment shows that noise inflates the small singular values. Truncating them recovers a cleaner signal, but you pay a price: the signal component living in the discarded dimensions is also lost. The optimal truncation rank is where the marginal loss of signal equals the marginal removal of noise.

## Linked skill
- [[00_meta/02_skill-tree]] → item: Applied linear algebra (SVD)
