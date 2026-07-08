---
tags: [phase/2, note, state/review]
MI-forward-link: "SVM's maximum-margin intuition maps directly to how attention heads separate features in the residual stream."
---

# Support Vector Machines — Notes

## Core Idea
Find the hyperplane that maximizes the margin — the distance between the decision boundary and the nearest data points (support vectors).

## Primal Form (Hard Margin)
min ||w||² subject to yᵢ(w·xᵢ + b) ≥ 1 for all i

The constraint says: all points must be on the correct side and at least distance 1/||w|| from the boundary.

## Soft Margin (Slack Variables)
min ||w||² + C Σ ξᵢ subject to yᵢ(w·xᵢ + b) ≥ 1 - ξᵢ, ξᵢ ≥ 0

C controls the tradeoff: large C → hard margin (fewer violations), small C → soft margin (more tolerance).

## Dual Form and Kernel Trick
The dual optimization depends only on dot products between data points:
max Σ αᵢ - ½ Σᵢⱼ αᵢαⱼyᵢyⱼ(xᵢ·xⱼ)

Replace xᵢ·xⱼ with K(xᵢ, xⱼ) to get the kernel trick:
- Linear: K(x, z) = x·z
- Polynomial: K(x, z) = (γx·z + r)^d
- RBF: K(x, z) = exp(-γ||x-z||²)

## Support Vectors
Only the points on the margin boundary matter for the decision boundary. All other points can be removed without changing the model.

## MI Forward Link
Attention heads compute two separate functions:
- QK circuit: computes which positions to attend to (analogous to selecting support vectors)
- OV circuit: computes what to copy from those positions

The "separability" intuition from SVMs maps to how attention heads learn to separate relevant from irrelevant information in the residual stream.

The kernel trick's implicit high-dimensional mapping is conceptually related to how the residual stream implicitly provides a rich feature space through the composition of layers.
