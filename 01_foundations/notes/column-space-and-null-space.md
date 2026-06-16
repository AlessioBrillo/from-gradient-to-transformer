---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-16
---

# Column Space and Null Space

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
The column space (range) of a matrix is the set of all possible outputs Av. The null space (kernel) is the set of all vectors v that map to zero: Av = 0.

## Why it exists / what problem it solves
Column space tells you what outputs are reachable — it defines the **range** of the transformation. Null space tells you which inputs get squished to zero — the **information loss**. Together they determine whether a system of equations has zero, one, or infinitely many solutions. In neural networks: the column space of a weight matrix determines the directions the layer can express; the null space reveals the information lost.

## How it works
- **Column space**: span of the columns of A. If v is in the column space, then Ax = v has a solution.
- **Null space**: set of all x such that Ax = 0. If non-trivial, multiple inputs map to the same output.
- **Rank**: dimension of the column space. Full rank = dim = min(rows, cols). Rank deficiency = det = 0 = information loss.
- **Rank-nullity theorem**: rank + nullity = number of columns.

```python
import numpy as np

def describe_matrix(A):
    print(f"Shape: {A.shape}")
    print(f"Rank: {np.linalg.matrix_rank(A)}")
    print(f"Determinant: {np.linalg.det(A):.3f}" if A.shape[0] == A.shape[1] else "Non-square")
    
    # Column space: throw away zero singular values
    U, S, Vt = np.linalg.svd(A)
    print(f"Singular values: {S}")
    print(f"Column space basis: columns of U corresponding to non-zero S")
    print(f"Null space basis: rows of Vt corresponding to zero S")

A = np.array([[1, 2], [2, 4]])  # rank 1
describe_matrix(A)
# v = [3, 6] is in the column space (it's 3 * column1)
# v = [1, 1] is NOT in the column space

# Null space: solutions to Ax = 0
# x = [2, -1] maps to zero
print(A @ np.array([2, -1]))  # [0, 0]
```

If the null space contains only the zero vector, the transformation is injective (one-to-one). Every non-zero null space means multiple inputs collapse to the same output.

## Links
- [[01_foundations/notes/identity-and-inverse-matrices|Identity and Inverse Matrices]]
- [[01_foundations/notes/determinant-and-area-scaling|Determinant and Area Scaling]]

## Insight
Information in the null space of the first layer is **irrecoverable** from that layer's output alone — it was squished to zero. However, later layers can still learn useful features from the column space representation. This is why skip connections (ResNet) and residual streams (Transformer) help: they add the original input back, bypassing the null space of intermediate layers.
