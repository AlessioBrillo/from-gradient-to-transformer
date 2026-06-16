---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-16
---

# General 2×2 Matrix as Transformation

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
Every 2×2 matrix [[a, b], [c, d]] represents a linear transformation of 2D space. The four entries control where the basis vectors land.

## Why it exists / what problem it solves
Understanding what each entry does lets you look at any matrix and immediately visualize the transformation — instead of treating it as a black box of numbers.

## How it works

The columns of the matrix tell you where the basis vectors go:

```
[a  b]     i-hat → (a, c)
[c  d]     j-hat → (b, d)
```

- **a** — where i-hat lands on the x-axis (scaling / reflection along x)
- **c** — where i-hat lands on the y-axis (vertical shear)
- **b** — where j-hat lands on the x-axis (horizontal shear)
- **d** — where j-hat lands on the y-axis (scaling / reflection along y)

### Examples

| Matrix | Effect | a | b | c | d |
|--------|--------|---|---|---|---|
| [[1,0],[0,1]] | Identity — nothing changes | 1 | 0 | 0 | 1 |
| [[2,0],[0,1]] | Scale x by 2 | 2 | 0 | 0 | 1 |
| [[1,1],[0,1]] | Horizontal shear | 1 | 1 | 0 | 1 |
| [[0,1],[1,0]] | Swap axes (reflect over y=x) | 0 | 1 | 1 | 0 |
| [[0,-1],[1,0]] | Rotate 90° CCW | 0 | -1 | 1 | 0 |

```python
import numpy as np

def transform(A, v):
    """Apply matrix A to vector v and print result."""
    return A @ v

i_hat = np.array([1, 0])
j_hat = np.array([0, 1])

A = np.array([[2, 0], [0, 1]])   # scale x by 2
print(A @ i_hat, A @ j_hat)      # [2, 0] [0, 1] → i-hat raddoppia, j-hat invariato
```

## Links
- [[01_foundations/notes/vectors-and-linear-transformations|Vectors and Linear Transformations]]
- [[01_foundations/notes/three-dimensional-linear-transformations|Three-Dimensional Linear Transformations]]
- [[01_foundations/notes/change-of-basis|Change of Basis]]
- [[01_foundations/notes/determinant-and-area-scaling|Determinant and Area Scaling]]

## Open questions
- #question Can I predict the determinant just by looking at a, b, c, d? (ad − bc)
