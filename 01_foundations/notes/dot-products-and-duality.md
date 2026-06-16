---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-16
---

# Dot Products and Duality

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
The dot product v · w is the sum of element-wise products (v₁w₁ + v₂w₂ + ...). Geometrically, it is the length of the projection of v onto w times the length of w.

## Why it exists / what problem it solves
The dot product is how we measure **alignment** between vectors. It is the foundation of:
- **Attention** in Transformers: query · key scores determine which tokens to focus on.
- **Projections**: decomposing a vector into components along a direction.
- **Similarity**: cosine similarity = (v · w) / (|v| · |w|).
- **Linear transformations as dot products**: every linear transformation to 1D is equivalent to taking a dot product with some vector — this is the **duality** insight.

## How it works
- Algebraic: v · w = Σ vᵢ wᵢ = v[0]*w[0] + v[1]*w[1] + ...
- Geometric: v · w = |v| |w| cos(θ) where θ is the angle between them.
- If v · w = 0, the vectors are perpendicular (orthogonal).
- If v · w > 0, they point in roughly the same direction.
- If v · w < 0, they point in opposite directions.

```python
import numpy as np

v = np.array([2, 3])
w = np.array([4, 1])

dot = np.dot(v, w)       # 2*4 + 3*1 = 11
dot = v @ w              # same thing with @ operator

# Length (norm) from dot product
norm_v = np.sqrt(v @ v)  # sqrt(2² + 3²) = 3.606

# Cosine similarity (angle between vectors)
cos_theta = (v @ w) / (np.linalg.norm(v) * np.linalg.norm(w))

# Projection of v onto w
proj = (v @ w) / (w @ w) * w

def is_orthogonal(v, w, tol=1e-10):
    return abs(v @ w) < tol
```

### Duality
Every linear transformation from 2D to 1D can be represented as a dot product with a fixed vector. That vector is the "dual" of the transformation — this insight connects matrices (transformations) to vectors (dot products).

## Links
- [[01_foundations/notes/vectors-and-linear-transformations|Vectors and Linear Transformations]]
- [[01_foundations/notes/change-of-basis|Change of Basis]]

## Open questions
- #question How does duality generalize to higher dimensions? Is every row of a matrix a dual vector?
