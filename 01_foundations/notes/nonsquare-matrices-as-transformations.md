---
tags: [type/lesson, phase/1, state/consolidated]
state: consolidated
created: 2026-06-16
---

# Nonsquare Matrices as Transformations

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
A nonsquare matrix maps between spaces of different dimensions. An m×n matrix transforms n-dimensional vectors into m-dimensional space.

## Why it exists / what problem it solves
Almost every weight matrix in a neural network is nonsquare: embedding layers (vocab_size × d_model), feed-forward layers (d_model × d_ff), output projections (d_model × vocab_size). Understanding nonsquare transformations is essential for reading model architectures. They either **compress** (reduce dimension) or **expand** (increase dimension) the data.

## How it works

### Tall matrices (more rows than columns) — compress
A 3×2 matrix maps 2D vectors into 3D space. The output lives on a 2D plane embedded in 3D — the column space is 2D (rank ≤ 2). Some 3D points are unreachable.

### Wide matrices (more columns than rows) — expand
A 2×3 matrix maps 3D vectors into 2D space. The 3D space gets squished onto a 2D plane — infinitely many different 3D vectors map to the same 2D point (non-trivial null space).

```python
import numpy as np

# Tall matrix: 3x2 — maps 2D inputs to 3D outputs
A_tall = np.array([[1, 0],
                   [0, 1],
                   [1, 1]])
v_2d = np.array([2, 3])
v_3d = A_tall @ v_2d  # [2, 3, 5] — lives on a 2D plane in 3D


# Wide matrix: 2x3 — maps 3D inputs to 2D outputs
A_wide = np.array([[1, 0, 1],
                   [0, 1, 1]])
v_3d = np.array([1, 2, 3])
v_2d = A_wide @ v_3d  # [4, 5] — 3D collapsed to 2D

# Rank reveals the true output dimensionality
print(np.linalg.matrix_rank(A_tall))  # 2 (max possible for 3x2)
print(np.linalg.matrix_rank(A_wide))  # 2 (max possible for 2x3)
```

Neural network analogy:
- `nn.Linear(10, 64)` — wide (10→64), expands, creates new dimensions to learn features in.
- `nn.Linear(64, 10)` — tall (64→10), compresses, projects back to output space.

## Links
- [[01_foundations/notes/column-space-and-null-space|Column Space and Null Space]]
- [[01_foundations/notes/change-of-basis|Change of Basis]]

## Insight
A tall matrix maps n-dim inputs to m-dim outputs (m > n). Its maximum rank is n. If rank < n, outputs shrink further. The unreachable region is the orthogonal complement of the column space.
This is what happens in underdetermined neural network layers: some output patterns can never be produced because the weight matrix lacks the rank to express them.
