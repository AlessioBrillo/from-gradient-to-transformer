---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-16
---

# Change of Basis

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
A change of basis re-expresses the same vector in a different coordinate system. The transformation matrix contains the new basis vectors as its columns.

## Why it exists / what problem it solves
The same point in space has different coordinates depending on your reference frame. Change of basis is how neural networks learn **representations**: the hidden layers re-express the input in a new basis that makes the task easier. PCA is a change of basis where the new axes align with maximum variance. Word embeddings are a learned basis that captures semantic relationships.

## How it works
- Let B be a matrix whose columns are the new basis vectors (expressed in the standard basis).
- A vector v with coordinates [v]_s in the standard basis has coordinates [v]_B = B⁻¹v in the B-basis.
- To convert FROM the B-basis back to standard: v = B · [v]_B.

```python
import numpy as np

# Standard basis: i-hat=(1,0), j-hat=(0,1)
# New basis: b1=(2,1), b2=(1,2)
B = np.column_stack([
    np.array([2, 1]),   # first basis vector
    np.array([1, 2])    # second basis vector
])

# A vector in standard coordinates
v_standard = np.array([5, 5])

# Convert to B-coordinates
B_inv = np.linalg.inv(B)
v_new_basis = B_inv @ v_standard  # coordinates in B-basis

# Convert back
v_back = B @ v_new_basis
assert np.allclose(v_standard, v_back)  # True

# This is exactly what happens in a neural network layer:
# W @ x + b — the weight matrix W defines a new basis
```

Geometrically: the change-of-basis matrix B tells you where the new basis vectors land in standard coordinates. The inverse B⁻¹ tells you how to read coordinates written in the new system.

PCA is the most important example: the eigenvectors of the covariance matrix form a new basis aligned with the directions of maximum variance.

## Links
- [[01_foundations/notes/linear-combinations-span-and-basis|Linear Combinations, Span, and Basis Vectors]]
- [[01_foundations/notes/dot-products-and-duality|Dot Products and Duality]]
- [[01_foundations/notes/eigenvalues-and-eigenvectors|Eigenvalues and Eigenvectors]]

## Insight
In a Transformer, each attention head projects the input into a **query**, **key**, and **value** space — these are learned basis changes. The query and key spaces align to measure relevance via dot products (attention scores), and the value space provides the new representation. Every attention layer is a dynamic, data-dependent change of basis where each token assembles its new coordinates from other tokens' values.
