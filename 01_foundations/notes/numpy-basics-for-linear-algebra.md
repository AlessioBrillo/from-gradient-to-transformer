---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-16
---

# NumPy Basics for Linear Algebra

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
NumPy is Python's numerical computing library; its ndarray is the standard data structure for vectors, matrices, and tensors in the Python ecosystem.

## Why it exists / what problem it solves
Pure Python loops are 10-100x too slow for linear algebra on large data. NumPy uses optimized C/Fortran under the hood and provides vectorized operations that run at near-C speed.

## How it works

```python
import numpy as np

# Creating arrays
v = np.array([1, 2, 3])          # 1D vector
A = np.array([[1, 2], [3, 4]])   # 2D matrix
Z = np.zeros((3, 3))             # all zeros
I = np.eye(3)                    # identity matrix
R = np.random.randn(2, 3)        # random normal

# Core operations
A @ v        # matrix-vector product (use @, not *)
A @ B        # matrix-matrix product
A * B        # element-wise (Hadamard) product — different from @
A.T          # transpose
np.linalg.inv(A)   # inverse (only for square non-singular)
np.linalg.det(A)   # determinant
np.linalg.eig(A)   # eigenvalues and eigenvectors
```

## Links
- [[01_foundations/notes/vectors-and-linear-transformations|Vectors and Linear Transformations]]
- [[01_foundations/notes/three-dimensional-linear-transformations|Three-Dimensional Linear Transformations]]
- [[01_foundations/notes/dot-products-and-duality|Dot Products and Duality]]
- [[01_foundations/notes/eigenvalues-and-eigenvectors|Eigenvalues and Eigenvectors]]

## Insight
Broadcasting aligns dimensions from the right: an array of shape (3, 1) + (3,) becomes (3, 1) + (1, 3) = (3, 3). Size-1 dimensions are "stretched" to match the other array without copying data — broadcasting creates a **view** (virtual repetition), not a copy. This makes broadcasting memory-efficient: adding a (1000, 1) to a (1, 1000) creates a (1000, 1000) result without allocating intermediate copies.
