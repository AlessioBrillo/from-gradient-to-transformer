---
tags: [type/exercise, phase/1]
skill: Applied linear algebra (NumPy)
created: 2026-06-16
---

# Exercise: 2D Transformation Analysis

> **Series**: [Essence of Linear Algebra — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&si=IWGNxJnrtFTJegl0)

## Goal / skill it demonstrates
Combine everything from steps 1–3 (vectors, matrices as transformations, determinant, inverse, eigenvalues) into a single analysis pipeline. Given any 2×2 matrix, extract its complete geometric story from NumPy.

## Setup

```python
import numpy as np
```

## Part 1 — Read the transformation from the columns

Pick three matrices below and for each one:
1. Identify where i-hat and j-hat land (read from the columns).
2. Describe the transformation in plain English.

```python
TRANSFORMATIONS = {
    "scale_x":    np.array([[3, 0], [0, 1]]),
    "shear":      np.array([[1, 1.5], [0, 1]]),
    "rotate_90":  np.array([[0, -1], [1, 0]]),
    "reflect":    np.array([[-1, 0], [0, 1]]),
    "squish":     np.array([[1, 2], [2, 4]]),
}
```

## Part 2 — Compute the determinant

For each chosen matrix:
- Compute `np.linalg.det(A)`.
- Verify by hand: det = ad − bc.
- Answer: does this transformation squish space? Flip orientation? Preserve area?

```python
def analyze_determinant(A, name):
    det = np.linalg.det(A)
    print(f"{name}: det = {det:.3f}")
    if abs(det) < 1e-10:
        print("  → Singular! Squishes space into a lower dimension.")
    elif det < 0:
        print("  → Orientation flipped (reflection).")
    elif abs(det - 1) < 1e-10:
        print("  → Area preserved (unit determinant).")
    else:
        print(f"  → Area scales by {det:.3f}.")
```

## Part 3 — Invert (if possible)

For each non-singular matrix:
- Compute `np.linalg.inv(A)`.
- Verify `A @ A_inv ≈ I` and `A_inv @ A ≈ I`.
- Solve the system `A @ x = v` for `v = np.array([1, 1])` using `np.linalg.solve`.

```python
def analyze_inverse(A, name):
    if abs(np.linalg.det(A)) < 1e-10:
        print(f"{name}: no inverse (det = 0).")
        return
    A_inv = np.linalg.inv(A)
    print(f"{name} inverse:\n{A_inv}")
    assert np.allclose(A @ A_inv, np.eye(2)), "Inverse check failed"
    print(f"  → A @ A_inv ≈ I: verified.")
    
    v = np.array([1.0, 1.0])
    x = np.linalg.solve(A, v)
    print(f"  → A⁻¹ · [1,1] = {x}")
    print(f"  → Verify: A @ x = {A @ x} ≈ [1, 1]")
```

## Part 4 — Find eigenvalues and eigenvectors

For each non-singular matrix:
- Compute `np.linalg.eig(A)`.
- Identify which direction is purely stretched (not rotated).
- Verify `A @ v = λv` for each eigenpair.

```python
def analyze_eigen(A, name):
    eigvals, eigvecs = np.linalg.eig(A)
    print(f"{name} eigenvalues: {eigvals}")
    print(f"{name} eigenvectors (columns):\n{eigvecs}")
    for i in range(eigvals.shape[0]):
        v = eigvecs[:, i]
        lam = eigvals[i]
        lhs = A @ v
        rhs = lam * v
        match = np.allclose(lhs, rhs)
        print(f"  λ = {lam:.3f}: A·v ≈ λ·v? {match}")
    print(f"  det = product of eigenvalues = {np.prod(eigvals):.3f} "
          f"(matches np.linalg.det = {np.linalg.det(A):.3f})")
```

## Part 5 — Run the full pipeline

```python
for name, A in TRANSFORMATIONS.items():
    print(f"\n{'='*50}")
    print(f"  {name}")
    print(f"{'='*50}")
    print(f"Matrix A =\n{A}")
    analyze_determinant(A, name)
    analyze_inverse(A, name)
    analyze_eigen(A, name)
```

## Reflection questions

1. **Scale_x**: `[[3,0],[0,1]]` — (0, 1) is also an eigenvector with eigenvalue 1. The y-direction is unchanged, so it is trivially an eigenvector: A·(0,1) = 1·(0,1). Every vector on an axis of a diagonal matrix is an eigenvector.

2. **Shear**: `[[1,1.5],[0,1]]` has det = 1, meaning area **is** preserved. A shear skews the shape but the parallelogram formed by the transformed basis vectors has the same area as the unit square. Visually the shape looks stretched but the determinant tells you the area did not change — the horizontal shear trades width for height.

3. **Squish**: `np.linalg.inv` fails because det = 0. The second column is 2× the first column (linearly dependent). The column space is 1D — a line through the origin. Many different inputs map to the same output (every point on a line parallel to the null space collapses to the same result). No unique inverse exists because information is destroyed.

4. **Rotate_90**: `[[0,-1],[1,0]]` has eigenvalues ±i (purely imaginary). No real eigenvector exists because every non-zero vector gets rotated — no direction stays on the same line. Complex eigenvalues signal rotation: the magnitude of the eigenvalue (|i| = 1) tells you the scaling factor (1 = pure rotation, no stretching).

## What I learned doing it

Running the full pipeline on different transformations made the connection between numbers and geometry concrete. I can now look at a 2×2 matrix and roughly predict its effect: diagonal matrices scale axes, shear matrices preserve area but skew, singular matrices collapse dimension.
The most surprising insight: an area-preserving shear still looks like it distorts shapes — geometric intuition and the determinant measure different things.
The eigenvalue check was the most satisfying: verifying A·v = λv in code confirms that the eigenvectors found by `np.linalg.eig` really are the invariant directions.

## Linked skill
- [[00_meta/02_skill-tree]] → item: Applied linear algebra (NumPy)
