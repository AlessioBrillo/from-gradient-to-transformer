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

Answer in your own words after running the code:

1. **Scale_x**: The eigenvector is clearly (1, 0) with eigenvalue 3. Why is (0, 1) also an eigenvector? What is its eigenvalue?
2. **Shear**: The matrix `[[1, 1.5], [0, 1]]` has det = 1. Does it preserve area? How is that possible when it visibly skews shapes?
3. **Squish**: Why does `np.linalg.inv` fail? What does det = 0 tell you about the columns?
4. **Rotate_90**: What do the complex eigenvalues tell you about this transformation? Why is there no real eigenvector?

## What I learned doing it

_(Write 3–5 sentences here after completing)_

## Linked skill
- [[00_meta/02_skill-tree]] → item: Applied linear algebra (NumPy)
