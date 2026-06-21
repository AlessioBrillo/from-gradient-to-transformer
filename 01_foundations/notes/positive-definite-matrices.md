---
tags: [type/lesson, phase/1]
state: consolidated
created: 2026-06-19
---

# Positive Definite Matrices and Quadratic Forms

> **Resources**: *Mathematics for Machine Learning* — Deisenroth, Faisal, Ong, Ch. 4 | [M4ML — Vector Calculus](https://mml-book.github.io/) Ch. 5 for Hessian applications | Boyd & Vandenberghe Ch. 3 for semidefiniteness in convexity

## What it is

A symmetric matrix A ∈ ℝ^{n×n} is positive definite if the scalar quantity xᵀAx is strictly positive for every non-zero vector x. If xᵀAx ≥ 0 for all x, A is positive semidefinite. The expression xᵀAx is called a quadratic form — the multivariable analogue of a single-variable quadratic ax².

## Why it exists / what problem it solves

Quadratic forms are the language of curvature in high dimensions:

- The Hessian ∇²f(x) of a loss function is a quadratic form — its definiteness tells you whether you are at a minimum, maximum, or saddle point.
- The covariance matrix Σ is positive semidefinite — its quadratic form xᵀΣx computes the variance of the projection xᵀZ.
- Mahalanobis distance (x − μ)ᵀΣ⁻¹(x − μ) is a quadratic form that measures how many "standard deviations" a point is from the mean, accounting for correlated dimensions.
- Kernel methods require positive definite kernel functions — the Gram matrix must be PSD for the optimization to be convex.
- The Cholesky decomposition A = LLᵀ exists only for PD matrices and is the numerical workhorse for sampling from multivariate Gaussians and solving linear systems.

## How it works

### Quadratic forms

For a symmetric matrix A and vector x:

f(x) = xᵀAx = Σᵢⱼ A_{ij} x_i x_j

In 2D:

f(x, y) = A₁₁x² + 2A₁₂xy + A₂₂y²

The sign of this scalar value encodes the curvature of the surface z = xᵀAx:

| Definiteness | Eigenvalues | Surface shape | Example |
|-------------|-------------|--------------|---------|
| Positive definite | All λ > 0 | Bowl (minimum) | x² + y² |
| Positive semidefinite | All λ ≥ 0 | Trough (flat ridge) | x² |
| Negative definite | All λ < 0 | Dome (maximum) | −x² − y² |
| Indefinite | Mixed signs | Saddle | x² − y² |

```python
import numpy as np

def classify_matrix(A):
    A = (A + A.T) / 2  # enforce symmetry
    eigvals = np.linalg.eigvalsh(A)
    if np.all(eigvals > 1e-8):
        return "positive definite"
    elif np.all(eigvals >= -1e-8):
        return "positive semidefinite"
    elif np.all(eigvals < -1e-8):
        return "negative definite"
    else:
        return "indefinite"

A_pd = np.array([[2, 0], [0, 3]])     # positive definite
A_id = np.array([[2, 0], [0, 0]])     # positive semidefinite
A_sp = np.array([[2, 0], [0, -1]])    # indefinite (saddle)

for name, A in [("PD", A_pd), ("PSD", A_id), ("Indef", A_sp)]:
    print(f"{name}: {classify_matrix(A)}")
```

### The Hessian and critical points

For a twice-differentiable function f:

- **∇f(x) = 0** and **∇²f(x) ≻ 0**  → strict local minimum.
- **∇f(x) = 0** and **∇²f(x) ≺ 0**  → strict local maximum.
- **∇f(x) = 0** and **∇²f(x)** indefinite → saddle point.

In high-dimensional loss landscapes, saddle points are overwhelmingly more common than local minima. The Hessian of a neural network at the end of training typically has a mixture of positive, negative, and near-zero eigenvalues.

### Cholesky decomposition

Any positive definite matrix A can be decomposed uniquely as:

A = LLᵀ

where L is lower-triangular with positive diagonal entries. The Cholesky decomposition is the most efficient way to:

- **Solve linear systems**: Ax = b → LLᵀx = b → forward substitution (Lz = b) → backward substitution (Lᵀx = z). This is O(n³/3) vs O(n³) for Gaussian elimination.
- **Sample from N(μ, Σ)**: compute L from Σ, sample z ∼ N(0, I), return μ + Lz.

```python
# Sample from a multivariate Gaussian via Cholesky
mu = np.array([0.0, 0.0])
cov = np.array([[1.0, 0.8], [0.8, 1.0]])
L = np.linalg.cholesky(cov)
z = np.random.randn(2)
sample = mu + L @ z
print(f"Sample from N(μ, Σ): {sample}")
```

### Connection to convexity

A twice-differentiable function is convex if and only if its Hessian is positive semidefinite **everywhere**:

f convex  ⇔  ∇²f(x) ⪰ 0  for all x

This is the link between linear algebra (eigenvalues of symmetric matrices) and optimization (global minima). For MSE: ∇²L = 2XᵀX/n, which is always positive semidefinite. For logistic regression: ∇²L = XᵀSX where S is a diagonal matrix of σ(ŷ)(1−σ(ŷ)) > 0, so the Hessian is positive definite.

## Links
- [[01_foundations/notes/convex-optimization-basics]]
- [[01_foundations/notes/higher-order-derivatives-and-taylor-series]]
- [[01_foundations/notes/eigenvalues-and-eigenvectors]]
- [[01_foundations/notes/singular-value-decomposition]]

## Insight
The definiteness of a matrix is **scale-dependent**: multiplying A by −1 flips definiteness.
This is why maximizing log-likelihood (concave) is equivalent to minimizing negative
log-likelihood (convex). The convention in ML is to frame every problem as minimization of a
convex (or at least non-convex) loss — not because maximization is harder, but because gradient
descent is defined for minimization, and the convexity guarantee only applies in the "minimize"
direction.
