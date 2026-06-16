---
tags: [type/proof, phase/1]
created: 2026-06-16
---

# Proof to myself: Linear Algebra Foundations

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate
That I can explain and apply the core concepts of linear algebra covered by the 3Blue1Brown Essence of Linear Algebra series: vectors, linear transformations, span/basis, matrix multiplication as composition, determinant, inverse, column/null space, dot products, norms, change of basis, eigenvalues/eigenvectors, and how they connect to neural networks.

## What I produced from memory

### 1. Explain in plain English

- **What is a matrix?** A matrix is a linear transformation — it takes a vector as input and produces another vector as output. Its **columns** tell you where the basis vectors (i-hat, j-hat, k-hat) land after the transformation. Reading the columns is the fastest way to visualize what a matrix does.

- **What does the determinant measure?** The determinant measures how much the transformation scales area (in 2D) or volume (in 3D). det = 1 preserves area, det = 0 collapses space into a lower dimension (information loss), det < 0 flips orientation (reflection).

- **When does a matrix fail to have an inverse?** When det = 0, or equivalently when the columns are linearly dependent. The null space is non-trivial (multiple inputs map to the same output), so the transformation cannot be reversed uniquely.

- **What is an eigenvector?** An eigenvector is a direction that the transformation only scales without rotating: Av = λv. The eigenvalue λ is the scaling factor along that direction. Eigenvectors reveal the invariant axes of the transformation — the "natural coordinates" of the system. PCA is built on this: eigenvectors of the covariance matrix point to directions of maximum variance.

### 2. Code from memory

```python
import numpy as np

def analyze_matrix(A):
    """Analyze a 2×2 matrix: determinant, trace, invertibility, eigenvalues."""
    det = np.linalg.det(A)
    trace = np.trace(A)
    invertible = abs(det) > 1e-10
    
    if not invertible:
        print("Matrix is singular (det ≈ 0). No inverse exists.")
        return
    
    eigvals, eigvecs = np.linalg.eig(A)
    
    # Verify A @ v = λv
    for i in range(len(eigvals)):
        v = eigvecs[:, i]
        lam = eigvals[i]
        assert np.allclose(A @ v, lam * v), f"Eigenpair {i} failed"
    
    print(f"det = {det:.3f}, trace = {trace:.3f}")
    print(f"Eigenvalues: {eigvals}")
    print(f"Inverse exists: {invertible}")
    return eigvals, eigvecs
```

### 3. Visual reasoning

- **Matrix multiplication as composition**: Applying A then B composes into BA. Order matters because each matrix transforms the space, and the second matrix operates on the result of the first. BA is generally different from AB — just like putting on socks then shoes is different from shoes then socks.

- **det(A) = 0**: The column space is a lower-dimensional subspace (e.g., a line in 2D), and the null space contains all vectors that map to zero. The transformation destroys information along the null space directions — you cannot recover what was lost.

- **Change of basis and word embeddings**: Word embeddings like word2vec learn a basis (the embedding space) where semantic relationships correspond to vector arithmetic. "King - Man + Woman = Queen" works because the coordinate system (basis) was learned to make these relationships linear. Changing the basis rotates the space without changing the relationships — cosine similarity remains invariant under orthogonal transformations.

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
