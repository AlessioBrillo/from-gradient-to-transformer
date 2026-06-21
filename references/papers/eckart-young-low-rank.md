---
tags: [reference]
---

# The Approximation of One Matrix by Another of Lower Rank

**Authors**: Carl Eckart, Gale Young
**Year**: 1936
**Journal**: Psychometrika, 1(3), 211–218
**URL**: https://doi.org/10.1007/BF02288367

**Used in Phase 1 for**: SVD low-rank approximation theorem

**Key result**: For any matrix A ∈ ℝ^{m×n}, the matrix A_k of rank k that minimizes ‖A − A_k‖_F (Frobenius norm) is given by the truncated SVD A_k = U_k Σ_k V_kᵀ. The squared error equals Σ_{i=k+1}^{r} σᵢ².

**Why it matters**: This theorem is the theoretical foundation for PCA (truncated SVD of the data matrix), image compression, Latent Semantic Analysis in NLP, collaborative filtering via matrix factorization, and neural network compression via low-rank weight approximation.

**Connected notes**:
- [[01_foundations/notes/singular-value-decomposition]]
- [[01_foundations/exercises/svd-image-compression]]
