---
tags: [type/lesson, phase/1, state/review]
state: review
created: 2026-06-16
---

# Abstract Vector Spaces

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
A vector space is any set that satisfies the vector space axioms (closure under addition and scalar multiplication, distributivity, identity elements). Functions, polynomials, and matrices can all be vectors.

## Why it exists / what problem it solves
The axioms define the least common denominator for doing linear algebra. Once you prove something for all vector spaces, it applies everywhere — not just to arrows in 2D. This is why we can treat sequences of numbers (embeddings), functions, and probability distributions with the same linear algebra toolkit.

## How it works
A set V is a vector space over the reals if:
- v + w ∈ V for all v, w ∈ V (closed under addition)
- c·v ∈ V for all c ∈ ℝ, v ∈ V (closed under scalar multiplication)
- Addition is commutative, associative, has identity (0) and inverses (-v)
- Scalar multiplication distributes over vector addition: c·(v + w) = c·v + c·w

**Examples of vector spaces**:
| Space | "Vectors" | "Scalar multiplication" |
|-------|-----------|------------------------|
| ℝⁿ | n-tuples of numbers | (x₁, …, xₙ) → (cx₁, …, cxₙ) |
| Polynomials of degree ≤ n | a₀ + a₁x + … + aₙxⁿ | multiply each coefficient by c |
| Functions f: ℝ → ℝ | real-valued functions | (c·f)(x) = c·f(x) |
| Matrices ℝ^{m×n} | m×n arrays | multiply each entry by c |

```python
import numpy as np

# Functions as vectors: we can add them and scale them
def f(x): return x**2
def g(x): return 2*x + 1

h = lambda x: f(x) + g(x)   # vector addition in function space
s = lambda x: 3 * f(x)      # scalar multiplication in function space

# Matrices as vectors: ℝ^{2×2} is a 4D vector space
A = np.array([[1, 2], [3, 4]])
B = np.array([[0, 1], [1, 0]])
C = A + B                    # vector addition in matrix space
D = 2.5 * A                  # scalar multiplication in matrix space
```

The power of abstraction: linear transformations between function spaces (Fourier transform, convolution) follow the same rules as matrix transformations. The dot product generalizes to inner products (integral of f·g).

## Links
- [[01_foundations/notes/linear-combinations-span-and-basis|Linear Combinations, Span, and Basis Vectors]]
- [[01_foundations/notes/column-space-and-null-space|Column Space and Null Space]]

## Insight
Probability distributions are **not** a vector space: they must sum to 1 and be non-negative. Scaling by -1 gives negative "probabilities", and adding two distributions exceeds the unit sum. This is why we work with log-probabilities (logits) instead — they live in a proper vector space.
