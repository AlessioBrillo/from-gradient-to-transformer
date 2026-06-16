---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-16
---

# Linear Combinations, Span, and Basis Vectors

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
A linear combination is a sum of scaled vectors. The span of a set of vectors is the set of all possible linear combinations. Basis vectors span the space while being linearly independent.

## Why it exists / what problem it solves
These concepts define the "grammar" of vector spaces. The span tells you what directions you can reach. Linear independence tells you whether you have redundant directions. Basis vectors give you a coordinate system — and choosing a different basis is the core idea behind embeddings and representation learning in neural networks.

## How it works
- **Linear combination**: av + bw (scale v by a, w by b, then add).
- **Span**: all points reachable by varying a and b. For two non-parallel vectors in 2D, the span is the entire plane.
- **Linear dependence**: when one vector can be expressed as a combination of others — it lies in their span.
- **Basis**: a set of linearly independent vectors that span the space. Every vector in the space can be written uniquely as a combination of the basis vectors.

```python
import numpy as np

v = np.array([1, 2])
w = np.array([3, 1])

# Linear combination: 2v + 0.5w
result = 2 * v + 0.5 * w  # [3.5, 4.5]

# Check if a third vector is in the span of v and w
u = np.array([4, 5])
# Solve c0*v + c1*w = u to see if u lies in span([v, w])
A = np.column_stack([v, w])
try:
    coeffs = np.linalg.solve(A, u)
    print(f"u is in the span: {coeffs[0]:.1f}v + {coeffs[1]:.1f}w")
except np.linalg.LinAlgError:
    print("u is NOT in the span of v and w")
```

Standard basis in 2D: i-hat = (1, 0), j-hat = (0, 1). Any vector (x, y) = x·i-hat + y·j-hat.

## Links
- [[01_foundations/notes/vectors-and-linear-transformations|Vectors and Linear Transformations]]
- [[01_foundations/notes/change-of-basis|Change of Basis]]

## Insight
In 2D, any set of more than 2 vectors is linearly dependent — one vector can be expressed as a combination of the others. The representation is no longer unique: the same point can be reached by infinitely many combinations of the redundant vectors. The number of basis vectors equals the dimension of the space. In neural networks, overcomplete representations (more basis vectors than dimensions) are used in sparse coding, but they sacrifice uniqueness for robustness.
