---
tags: [type/exercise, phase/1]
skill: Applied linear algebra (NumPy)
created: 2026-06-16
---

# Exercise: Dot Products, Norms, and Change of Basis

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## Goal / skill it demonstrates
Practice dot products, norms, projections, orthogonality, and change of basis in NumPy. These are the building blocks of attention mechanisms, embeddings, and representation learning.

## Setup

```python
import numpy as np
```

## Part 1 — Dot products and orthogonality

Given the vectors below, compute their dot products and determine which pairs are orthogonal.

```python
v1 = np.array([1, 0, 2])
v2 = np.array([0, 3, 0])
v3 = np.array([2, 0, -1])
v4 = np.array([1, 1, 1])

# 1. Compute v1 @ v2, v1 @ v3, v2 @ v4
# 2. Which pairs are orthogonal? (dot product ≈ 0)
# 3. Compute the cosine similarity between v1 and v4
```

## Part 2 — Projections

Project v onto w and decompose v into parallel and perpendicular components.

```python
v = np.array([4, 1])
w = np.array([2, 3])

def project_onto(v, w):
    """Return the projection of v onto w."""
    return (v @ w) / (w @ w) * w

proj = project_onto(v, w)      # component of v along w
perp = v - proj                 # component of v perpendicular to w

# Verify: proj is parallel to w, perp is orthogonal to w
assert np.allclose(proj @ perp, 0)  # orthogonal
```

## Part 3 — Norms

```python
x = np.array([3, -4, 12])

# Compute by hand then verify:
l2 = np.linalg.norm(x, ord=2)        # should be 13.0
l1 = np.linalg.norm(x, ord=1)        # should be 19.0

# Frobenius norm of a matrix
A = np.array([[1, 2], [3, 4], [5, 6]])
frob = np.linalg.norm(A, ord='fro')  # sqrt(1+4+9+16+25+36) = sqrt(91)
```

## Part 4 — Change of basis

You have a vector expressed in the standard basis. Convert it to a new basis B and back.

```python
# New basis vectors (columns of B)
B = np.column_stack([
    np.array([1, 1]),
    np.array([1, -1])
])

# A vector in standard coordinates
v_standard = np.array([3, 2])

# Convert to B-coordinates
B_inv = np.linalg.inv(B)
v_new_basis = B_inv @ v_standard

# Verify round-trip
v_back = B @ v_new_basis
assert np.allclose(v_standard, v_back)

# 1. What are the B-coordinates of [3, 2]?
# 2. What is [1, 0]_B in standard coordinates? (hint: B @ [1, 0])
# 3. Are the basis vectors orthogonal? Check with dot product.
```

## Part 5 — Nonsquare transformation

```python
# Tall matrix: 3x2 (maps 2D → 3D)
A_tall = np.array([[1, 0], [0, 1], [1, 1]])
v_2d = np.array([2, 3])
v_3d = A_tall @ v_2d  # what shape is this?

# Wide matrix: 2x3 (maps 3D → 2D)
A_wide = np.array([[1, 0, 1], [0, 1, 1]])
v_3d = np.array([1, 2, 3])
v_2d = A_wide @ v_3d  # what shape is this?

# 1. What is the rank of A_tall? Of A_wide?
# 2. Can a 3x2 matrix have rank 3? Why or why not?
```

## Reflection questions

1. If v·w = 0, the vectors are perpendicular (orthogonal). Geometrically, the projection of v onto w is zero — they share no component along each other's direction. In high dimensions, orthogonality means independence: knowing one tells you nothing about the other.

2. Proj(Proj(v)) = Proj(v). Once you remove the perpendicular component and keep only the part along w, projecting again does nothing — the result is already on the w-line. This idempotence (P² = P) is the defining property of a projection matrix.

3. Rotating the embedding space changes the coordinates but the **relationships** stay the same. Dot products and cosine similarities are invariant under rotation (orthogonal transformation). If "king" - "man" + "woman" ≈ "queen" in one basis, it holds in any rotated basis — the semantic structure is in the geometry, not the coordinate numbers.

4. Expanding from 10 → 64 dimensions creates more "knobs" to learn useful representations in. A wider layer can capture more features, separate classes with richer boundaries, and learn redundant patterns (robustness). The expansion gives the network room to find a good basis for the task — then the next layer can compress back to the output space.

## What I learned doing it

This exercise clarified the deep connection between dot products and geometric operations like projection and orthogonality. The change-of-basis section was the most valuable conceptually: converting a vector from standard to B-coordinates and back shows exactly what `B_inv @ v_standard` means geometrically.
I now see that a neural network layer Wx + b is just a change of basis (W) plus a translation (b). The Frobenius norm of a weight matrix measures its overall "energy" — a concept that reappears in weight decay regularization.

## Linked skill
- [[00_meta/02_skill-tree]] → item: Applied linear algebra (NumPy)
