---
tags: [type/proof, phase/1]
state: consolidated
created: 2026-06-19
---

# Proof to myself: Singular Value Decomposition

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate

1. State the full SVD decomposition and explain the geometric interpretation.
2. Explain the Eckart–Young theorem and why it matters for compression and denoising.
3. Write the SVD pseudoinverse formula and connect it to least-squares.
4. Show how PCA emerges from SVD of the centered data matrix.
5. Code from memory: SVD + low-rank reconstruction.

## What I produced from memory

### 1. SVD

For any real matrix A ∈ ℝ^{m×n}:

A = U Σ Vᵀ

where UᵀU = I, VᵀV = I, and Σ is diagonal with σ₁ ≥ σ₂ ≥ … ≥ σᵣ > 0.

Geometric interpretation: every linear transformation is a rotation (Vᵀ), followed by a coordinate-wise scaling (Σ), followed by another rotation (U). This is the most complete description possible — no matrix escapes the SVD.

The columns of V (right singular vectors) form an orthonormal basis for the row space of A. The columns of U (left singular vectors) form an orthonormal basis for the column space. The null space of A is spanned by the columns of V corresponding to zero singular values (if r < n).

### 2. Eckart–Young theorem

The best rank-k approximation of A under the Frobenius norm ‖·‖_F is:

A_k = U_k Σ_k V_kᵀ

where U_k, Σ_k, V_k retain only the first k singular values/vectors.

Error: ‖A − A_k‖_F² = Σ_{i=k+1}^{r} σᵢ²

This is the foundation of SVD-based compression: drop the smallest singular values and the corresponding singular vectors. The error of the approximation equals the sum of squares of the discarded singular values.

### 3. Pseudoinverse

A⁺ = V Σ⁺ Uᵀ, where Σ⁺ inverts each non-zero σᵢ:

(Σ⁺)_{ii} = 1/σᵢ for σᵢ > 0, and 0 for σᵢ = 0.

The solution x = A⁺b minimizes ‖Ax − b‖₂ and, among all minimizers, has the smallest norm.

### 4. PCA from SVD

Centered data X ∈ ℝ^{n×d}: X = U Σ Vᵀ.

Covariance: C ∝ XᵀX = V Σ² Vᵀ.

The principal components are the columns of V. The explained variance of component j is σⱼ² / Σ σᵢ². The projection onto k components is X V_k = U_k Σ_k.

This avoids forming XᵀX explicitly, which squares the condition number and loses numerical precision.

### 5. Code from memory

```python
import numpy as np

def svd_compress(A, k):
    """Rank-k approximation of A via SVD."""
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    return U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

def svd_pseudoinverse(A):
    """Compute the Moore-Penrose pseudoinverse via SVD."""
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    S_inv = np.array([1/s if s > 1e-10 else 0 for s in S])
    return Vt.T @ np.diag(S_inv) @ U.T

# Verify: A @ A⁺ @ A ≈ A
A = np.array([[1, 2], [3, 4], [5, 6]])
Ap = svd_pseudoinverse(A)
print("A @ A⁺ @ A ≈ A:", np.allclose(A @ Ap @ A, A, atol=1e-12))

def pca_via_svd(X, k):
    Xc = X - X.mean(axis=0)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    components = Vt[:k, :]
    explained = (S[:k] ** 2) / (S ** 2).sum()
    return Xc @ components.T, components, explained
```

## Links
- [[01_foundations/notes/singular-value-decomposition]]
- [[01_foundations/notes/column-space-and-null-space]]
- [[01_foundations/notes/eigenvalues-and-eigenvectors]]

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
