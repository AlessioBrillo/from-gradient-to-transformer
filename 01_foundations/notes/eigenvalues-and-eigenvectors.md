---
tags: [type/lesson, phase/1, state/consolidated]
state: consolidated
created: 2026-06-16
---

# Eigenvalues and Eigenvectors

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## What it is
An eigenvector v of a matrix A is a non-zero vector that only gets scaled (not rotated) when A is applied: Av = λv. The scalar λ is the eigenvalue — the scaling factor along that direction.

## Why it exists / what problem it solves
Eigenvectors reveal the **invariant directions** of a transformation — the axes along which the transformation is a pure stretch. This is the key to PCA (finding directions of maximum variance in data), stability analysis in dynamical systems, spectral clustering, and understanding the convergence behavior of optimization algorithms.

## How it works
- Av = λv means v lies in the same (or opposite) direction after the transformation.
- The eigenvectors of a 2×2 matrix are the directions where the matrix acts like a scalar.
- The determinant equals the product of eigenvalues: det(A) = λ₁ · λ₂.
- The trace (sum of diagonal) equals the sum of eigenvalues: tr(A) = λ₁ + λ₂.

```python
import numpy as np

A = np.array([[2, 0], [0, 3]])   # scale x by 2, y by 3
eigvals, eigvecs = np.linalg.eig(A)

print(eigvals)                     # [2., 3.] — the scaling factors
print(eigvecs)                     # [[1., 0.], [0., 1.]] — i-hat and j-hat

# Verify: A @ v = λv for each eigenpair
for i in range(2):
    v = eigvecs[:, i]
    lam = eigvals[i]
    assert np.allclose(A @ v, lam * v)  # passes
```

Eigenvectors are not unique — any scalar multiple of an eigenvector is still an eigenvector with the same eigenvalue.

### Quick trick for computing eigenvalues (3B1B #15)
For a 2×2 matrix `[[a, b], [c, d]]`, the eigenvalues satisfy:
- λ₁ + λ₂ = trace = a + d
- λ₁ · λ₂ = determinant = ad − bc
- Characteristic equation: λ² − trace·λ + det = 0
- Solve: λ = (trace ± √(trace² − 4·det)) / 2

```python
import numpy as np

A = np.array([[2, 1], [1, 2]])
trace = np.trace(A)
det = np.linalg.det(A)
discriminant = trace**2 - 4*det
lambda1 = (trace + np.sqrt(discriminant)) / 2
lambda2 = (trace - np.sqrt(discriminant)) / 2
print(lambda1, lambda2)             # [3., 1.]
print(np.linalg.eigvals(A))         # same result
```

## Links
- [[01_foundations/notes/determinant-and-area-scaling|Determinant and Area Scaling]]
- [[01_foundations/notes/change-of-basis|Change of Basis]]
- [[01_foundations/notes/identity-and-inverse-matrices|Identity and Inverse Matrices]]

## Insight
Complex eigenvalues always come in conjugate pairs and signal **rotation** in the transformation. The magnitude |λ| = √(Re(λ)² + Im(λ)²) gives the scaling factor, and the angle arg(λ) gives the rotation amount. A 2×2 rotation matrix [[cosθ, -sinθ], [sinθ, cosθ]] has eigenvalues cosθ ± i·sinθ = e^{±iθ} — purely rotational, no real eigenvector exists because no direction stays on the same line.
