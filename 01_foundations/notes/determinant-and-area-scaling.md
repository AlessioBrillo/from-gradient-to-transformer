---
tags: [type/lesson, phase/1, state/consolidated]
state: consolidated
created: 2026-06-16
---

# Determinant and Area Scaling

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
The determinant of a matrix measures how much the linear transformation scales the area (in 2D) or volume (in 3D) of any region in space.

## Why it exists / what problem it solves
The determinant tells you whether a transformation squishes space (det = 0), preserves area (det = 1), stretches it (det > 1), or flips orientation (det < 0). It is the single number that summarizes the global scaling behavior of the transformation.

## How it works
- For a 2×2 matrix `[[a, b], [c, d]]`: **det = ad − bc**.
- Geometrically, it is the area of the parallelogram formed by the transformed basis vectors.
- det = 0 means the transformation collapses space into a lower dimension (a line or a point) — the matrix is **singular** and has no inverse.
- det < 0 means the transformation flips the orientation of space (a reflection).

```python
import numpy as np

A = np.array([[2, 0], [0, 3]])   # scale x by 2, y by 3
np.linalg.det(A)                  # 6.0 — area scales by 6

B = np.array([[1, 2], [2, 4]])   # linearly dependent rows
np.linalg.det(B)                  # 0.0 — squishes to a line

C = np.array([[0, 1], [1, 0]])   # swap axes (reflection)
np.linalg.det(C)                  # -1.0 — area preserved, orientation flipped
```

Key properties:
- det(AB) = det(A) · det(B) — composing transformations multiplies their determinants.
- det(A⁻¹) = 1 / det(A) — undoing a transformation divides the area.
- det(A) = product of eigenvalues — connects scaling along invariant directions to total area change.

## Links
- [[01_foundations/notes/general-2x2-matrix-as-transformation|General 2×2 Matrix as Transformation]]
- [[01_foundations/notes/identity-and-inverse-matrices|Identity and Inverse Matrices]]

## Insight
In 3D, the determinant generalizes to the **scalar triple product**: a·(b×c) for a 3×3 matrix with columns a, b, c. The formula expands to a(ei − fh) − b(di − fg) + c(dh − eg) — a sum of 6 terms (3! for 3 dimensions). It measures volume scaling. For an n×n matrix, the determinant is a sum of n! terms, each product of n entries with a sign determined by the permutation parity.
