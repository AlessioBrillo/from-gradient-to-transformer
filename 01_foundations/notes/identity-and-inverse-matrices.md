---
tags: [type/lesson, phase/1, state/consolidated]
state: consolidated
created: 2026-06-16
---

# Identity and Inverse Matrices

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
The identity matrix I is the transformation that does nothing. The inverse A⁻¹ of a matrix A is the unique transformation that undoes A: A⁻¹A = I.

## Why it exists / what problem it solves
Inverses let us solve systems of linear equations. Given Av = x, we can recover v = A⁻¹x — this is the foundation of solving for weights in linear regression, computing transformations back to original coordinates, and understanding whether a problem has a unique solution.

## How it works
- Identity I = `[[1, 0], [0, 1]]`: i-hat and j-hat stay where they are.
- A⁻¹ exists **if and only if** det(A) ≠ 0 (non-singular).
- A⁻¹A = AA⁻¹ = I.
- Geometrically: if A scales by 2, A⁻¹ scales by ½. If A rotates 90° clockwise, A⁻¹ rotates 90° counter-clockwise.

```python
import numpy as np

A = np.array([[2, 0], [0, 3]])
A_inv = np.linalg.inv(A)

np.allclose(A @ A_inv, np.eye(2))  # True — they cancel
np.allclose(A_inv @ A, np.eye(2))  # True — order doesn't matter for inverse

# Solving Ax = v
v = np.array([4, 9])
x = np.linalg.solve(A, v)          # [2, 3] — because 2*2=4, 3*3=9
```

A matrix with det = 0 has no inverse — there is no way to undo a transformation that collapses information. This connects directly to the [[01_foundations/notes/column-space-and-null-space|column space and null space]]: when the null space is non-trivial, multiple inputs map to the same output, making inversion impossible.

## Links
- [[01_foundations/notes/determinant-and-area-scaling|Determinant and Area Scaling]]
- [[01_foundations/notes/column-space-and-null-space|Column Space and Null Space]]
- [[01_foundations/notes/matrix-multiplication-as-composition|Matrix Multiplication as Composition]]

## Insight
Both cases are possible. If x lies **in** the column space of A, there are infinitely many solutions: if v₀ is one solution, then v₀ + n is also a solution for any n in the null space. If x is **outside** the column space, no solution exists — the best we can do is find the least-squares approximation (minimizing |Av − x|²), which is the projection of x onto the column space.
