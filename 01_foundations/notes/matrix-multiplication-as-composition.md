---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-16
---

# Matrix Multiplication as Composition

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
Matrix multiplication is the composition of two linear transformations: applying A then B is equivalent to the single transformation BA.

## Why it exists / what problem it solves
Instead of applying transformations sequentially, we can combine them into one matrix. This is why neural networks can stack layers — each layer is a transformation, and the forward pass composes them into a single function.

## How it works
- A is m×n, B is n×p → AB is m×p.
- Entry (i,j) of AB = dot product of row i of A and column j of B.
- Order matters: AB ≠ BA in general. A(Bv) = (AB)v — composition is associative.

Geometrically, if A scales x by 2 and B rotates by 90°, then BA rotates first then scales — the order changes the result.

```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
B = np.array([[0, 1], [1, 0]])
A @ B  # apply B then A
B @ A  # apply A then B — different result!
```

## Links
- [[01_foundations/notes/vectors-and-linear-transformations|Vectors and Linear Transformations]]
- [[01_foundations/notes/identity-and-inverse-matrices|Identity and Inverse Matrices]]
- [[01_foundations/notes/determinant-and-area-scaling|Determinant and Area Scaling]]

## Open questions
- #question Why is matrix multiplication defined this way and not element-wise? What breaks if we used Hadamard product instead?
