---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-16
---

# Vectors and Linear Transformations

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
A vector is an object with magnitude and direction; a matrix is a linear transformation that maps vectors to other vectors.

## Why it exists / what problem it solves
Vectors represent data as coordinates in space. Linear transformations (matrices) let us rotate, scale, shear, or project that data — the core operation behind every neural network layer.

## How it works
- A vector v = (v₁, v₂) is a point in 2D space.
- A matrix A = [[a, b], [c, d]] applied to v gives A·v = (a·v₁ + b·v₂, c·v₁ + d·v₂).
- The columns of A are where the basis vectors i-hat and j-hat land after the transformation.
- Composing A then B is the matrix product BA.

```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
v = np.array([5, 6])
A @ v  # matrix-vector product
```

## Links
- [[01_foundations/notes/matrix-multiplication-as-composition|Matrix Multiplication as Composition]]
- [[01_foundations/notes/general-2x2-matrix-as-transformation|General 2×2 Matrix as Transformation]]
- [[01_foundations/notes/determinant-and-area-scaling|Determinant and Area Scaling]]

## Open questions
- #question Why must the inner dimensions match for matrix multiplication?
