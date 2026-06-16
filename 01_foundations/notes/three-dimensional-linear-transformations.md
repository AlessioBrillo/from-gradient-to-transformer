---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-16
---

# Three-Dimensional Linear Transformations

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
A 3×3 matrix represents a linear transformation in 3D space. The same intuitions from 2D generalize: columns are where the basis vectors land, the determinant measures volume scaling, and eigenvectors point along invariant directions.

## Why it exists / what problem it solves
Real-world data has many dimensions: images (thousands of pixels), embeddings (hundreds of numbers), hidden states (thousands of neurons). Understanding 3D transformations builds the intuition bridge from the 2D visual examples to the high-dimensional spaces that models actually operate in.

## How it works
- A 3×3 matrix `[[a, b, c], [d, e, f], [g, h, i]]` transforms (x, y, z) → (x', y', z').
- The three columns are where i-hat, j-hat, and k-hat land.
- The determinant measures **volume** scaling (3D analog of area).
- Eigenvectors now have 3 components: direction in 3D space.
- det = 0 → squishes 3D space into a plane, line, or point.

```python
import numpy as np

# Rotation around the z-axis (3D)
R_z = np.array([[0, -1, 0],
                [1,  0, 0],
                [0,  0, 1]])
v = np.array([1, 0, 0])
R_z @ v  # [0, 1, 0] — rotated 90° around z

# A projection: squish onto the xy-plane
P = np.array([[1, 0, 0],
              [0, 1, 0],
              [0, 0, 0]])
np.linalg.det(P)  # 0.0 — volume destroyed

# Eigenvalues in 3D
A = np.diag([2, 3, 4])  # scale x by 2, y by 3, z by 4
eigvals, eigvecs = np.linalg.eig(A)
print(eigvals)  # [2., 3., 4.] — three independent stretch directions
```

The determinant in 3D: scalar triple product a · (b × c). It equals the volume of the parallelepiped formed by the transformed basis vectors.

## Links
- [[01_foundations/notes/general-2x2-matrix-as-transformation|General 2×2 Matrix as Transformation]]
- [[01_foundations/notes/determinant-and-area-scaling|Determinant and Area Scaling]]

## Insight
Direct 4D visualization is impossible, but we rely on mathematical generalization: the same formulas for determinant, eigenvalues, matrix multiplication work in any dimension. The key intuition: all of linear algebra generalizes uniformly — if you understand 2D and 3D, the formulas for n-dimensions follow the same patterns. What helps: tracking rank (how many dimensions survive), eigenvalues (which directions get stretched), and dot products (how angles change).
