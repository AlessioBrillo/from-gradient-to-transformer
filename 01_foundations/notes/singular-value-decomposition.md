---
tags: [type/lesson, phase/1]
state: consolidated
created: 2026-06-19
---

# Singular Value Decomposition (SVD) — In Depth

> **Resources**: [3Blue1Brown — Singular Value Decomposition](https://youtu.be/gXbThCXjZFM) (the visual intuition) | *Mathematics for Machine Learning* — Deisenroth, Faisal, Ong, Ch. 4.5 | [Eckart–Young theorem proof](https://en.wikipedia.org/wiki/Low-rank_approximation) | [Gilbert Strang — SVD lecture](https://youtu.be/E_xF0P6r5hg) (MIT 18.06)

## What it is

The Singular Value Decomposition (SVD) factors any real matrix A ∈ ℝ^{m×n} into three matrices:

A = U Σ Vᵀ

where:
- U ∈ ℝ^{m×m} is orthogonal (UᵀU = I). Its columns are the **left singular vectors**.
- Σ ∈ ℝ^{m×n} is diagonal with σ₁ ≥ σ₂ ≥ … ≥ σᵣ > 0, σ_{r+1} = … = 0. The σᵢ are the **singular values**.
- V ∈ ℝ^{n×n} is orthogonal (VᵀV = I). Its columns are the **right singular vectors**.
- r = rank(A) ≤ min(m, n).

## Why it exists / what problem it solves

SVD is the **fundamental theorem of linear algebra** for real matrices. Every matrix — square or rectangular, invertible or singular — has an SVD. It reveals the intrinsic geometry of a linear transformation: rotation (Vᵀ), scaling (Σ), rotation (U). This makes it the Swiss Army knife of numerical linear algebra:

- PCA: V is the matrix of principal components; σᵢ² are proportional to explained variance.
- Low-rank approximation: the best rank-k approximation of A is U_k Σ_k V_kᵀ (Eckart–Young theorem).
- Pseudoinverse: A⁺ = V Σ⁺ Uᵀ solves least-squares problems.
- Collaborative filtering: SVD on user-item matrices recovers latent factors.
- Data compression: discard small singular values, keep the big ones.
- Condition number: κ(A) = σ₁ / σᵣ measures sensitivity to perturbations.

## How it works

### The geometry of SVD

SVD applies any matrix as a sequence of three steps:

1. **Vᵀ**: rotate the input vector into the orthonormal basis where the transformation is a pure scaling.
2. **Σ**: scale each coordinate by a non-negative factor σᵢ (the singular values).
3. **U**: rotate the scaled vector into the output coordinate system.

This is the geometric analog of eigenvalue decomposition — but SVD works for **any** matrix, while eigendecomposition requires a square, diagonalizable matrix. For symmetric positive definite matrices, the SVD and eigenvalue decomposition coincide: U = V = eigenvectors, σᵢ = |λᵢ|.

### Full vs. reduced SVD

**Full SVD** (m > n): A = UΣVᵀ with U ∈ ℝ^{m×m}, Σ ∈ ℝ^{m×n}, V ∈ ℝ^{n×n}. The last m − n columns of U are an orthonormal basis for the left null space.

**Reduced (thin) SVD**: only the first r columns of U and rows of Σ. A = U_r Σ_r V_rᵀ, where U_r ∈ ℝ^{m×r}, Σ_r ∈ ℝ^{r×r}, V_r ∈ ℝ^{n×r}. This is the form used in practice — it takes less memory and captures all non-zero singular values.

```python
import numpy as np

A = np.array([[3, 1], [1, 3], [0, 0]])  # 3×2 matrix, rank 2

# Full SVD
U_full, S_full, Vt_full = np.linalg.svd(A, full_matrices=True)
print("Full U:", U_full.shape)     # (3, 3)
print("Full Σ:", S_full)           # [4., 2.]  (only 2 non-zero)

# Reduced SVD (default with full_matrices=False)
U_red, S_red, Vt_red = np.linalg.svd(A, full_matrices=False)
print("Reduced U:", U_red.shape)   # (3, 2)
print("Reduced Σ diagonal:", S_red)  # [4., 2.]

# Verify reconstruction
A_reconstructed = U_red @ np.diag(S_red) @ Vt_red
print("Reconstruction error:", np.linalg.norm(A - A_reconstructed))
```

### Eckart–Young theorem (low-rank approximation)

The best rank-k approximation of A under both the Frobenius norm and the spectral norm is:

A_k = U_k Σ_k V_kᵀ = Σᵢ₌₁ᵏ σᵢ uᵢ vᵢᵀ

where U_k ∈ ℝ^{m×k} and V_k ∈ ℝ^{n×k} contain only the first k columns.

The approximation error is:

‖A − A_k‖_F = √(Σᵢ₌ₖ₊₁ʳ σᵢ²)

The k-th singular value σ_k itself is the spectral-norm error: ‖A − A_{k−1}‖₂ = σ_k.

This is the theoretical foundation for:
- **Image compression**: keep the top k singular values, discard the rest.
- **Denoising**: small singular values often correspond to noise; truncating them reduces noise.
- **Latent semantic analysis**: truncating the term-document SVD at k ≈ 100–300 reveals the "latent concepts" in a text corpus.

```python
def low_rank_approximation(A, k):
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    return U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

# Compression ratio vs. error
A = np.random.randn(100, 200)
full_params = 100 * 200
for k in [1, 5, 10, 20, 50]:
    Ak = low_rank_approximation(A, k)
    stored = k * (100 + 200)  # U: 100×k, Vᵀ: k×200
    ratio = stored / full_params
    err = np.linalg.norm(A - Ak)
    print(f"k={k:2d}: stored {stored:5d} params, "
          f"ratio={ratio:.3f}, error={err:.2f}")
```

### Pseudoinverse via SVD

The Moore–Penrose pseudoinverse A⁺ ∈ ℝ^{n×m} is:

A⁺ = V Σ⁺ Uᵀ

where Σ⁺ replaces each non-zero σᵢ with 1/σᵢ (and leaves zeros as zero).

A⁺ solves the least-squares problem: for Ax ≈ b, x̂ = A⁺b minimizes ‖Ax − b‖₂. If multiple solutions exist (underdetermined), A⁺b gives the minimum-norm solution.

```python
# Solving a least-squares problem via pseudoinverse
A = np.array([[1, 2], [3, 4], [5, 6]])  # overdetermined 3×2
b = np.array([1, 2, 3])

# Via SVD pseudoinverse
U, S, Vt = np.linalg.svd(A, full_matrices=False)
S_inv = np.diag(1.0 / S)
x_svd = Vt.T @ S_inv @ U.T @ b

# Via lstsq (same result)
x_lstsq, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
print("SVD solution:", x_svd)
print("lstsq solution:", x_lstsq)
print("Match:", np.allclose(x_svd, x_lstsq))
```

### Connection to PCA

Given data matrix X ∈ ℝ^{n×d} (n samples, d features, centered):

- The covariance matrix is C = (1/(n−1)) XᵀX (assuming row-major convention).
- X = U Σ Vᵀ → XᵀX = V Σ² Vᵀ.
- The columns of V are the **principal components** (eigenvectors of XᵀX).
- The singular values σⱼ = √(λⱼ × (n−1)), where λⱼ are eigenvalues of C.
- The projection of X onto the top k principal components is X V_k = U_k Σ_k.

This is the numerically stable way to compute PCA — directly via SVD of X, instead of forming the covariance matrix XᵀX (which squares the condition number).

```python
def pca_via_svd(X, n_components):
    """PCA by SVD of the centered data matrix."""
    X_centered = X - X.mean(axis=0)
    U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
    # Principal components = Vt.T[:n_components]
    components = Vt[:n_components, :]
    # Explained variance ratio
    total_var = np.sum(S ** 2)
    explained_ratio = S[:n_components] ** 2 / total_var
    # Projection
    X_pca = X_centered @ components.T
    return X_pca, components, explained_ratio
```

## Links
- [[01_foundations/notes/column-space-and-null-space]]
- [[01_foundations/notes/eigenvalues-and-eigenvectors]]
- [[01_foundations/notes/change-of-basis]]
- [[01_foundations/notes/nonsquare-matrices-as-transformations]]
- [[01_foundations/notes/positive-definite-matrices]]

## Insight
SVD unifies three perspectives on the same object: **geometry** (A = rotate → scale → rotate),
**algebra** (A = sum of rank-1 matrices σᵢ uᵢ vᵢᵀ), and **statistics** (A captures covariance
structure, and truncating SVD = denoising). When you see a matrix in ML, always ask: what does
the SVD reveal? For embeddings: the SVD of the weight matrix reveals the effective rank (how many
latent dimensions are actually used). For attention: the SVD of the attention logits reveals the
"head bandwidth" — how many independent patterns each head captures.
