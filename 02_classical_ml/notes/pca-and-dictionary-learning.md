---
tags: [phase/2, note, state/review]
MI-forward-link: "PCA is the conceptual ancestor of sparse autoencoders. Both decompose data into a sparse, interpretable basis. PCA gives orthogonal components; SAEs give overcomplete, sparse features."
---

# PCA and Dictionary Learning — Notes

## PCA (Principal Component Analysis)

**Goal:** Find orthogonal directions of maximum variance in the data.

**Method:**
1. Center the data: subtract mean
2. Compute covariance matrix: Σ = (1/n) XᵀX
3. Eigendecomposition of Σ → eigenvectors (principal components) + eigenvalues (variance explained)
4. Or equivalently: SVD of centered X → U, s, Vᵀ. Components = rows of Vᵀ, variance = s²

**Key properties:**
- Components are orthogonal and sorted by decreasing variance
- Optimal linear dimensionality reduction (minimum reconstruction error for given k)
- No sparsity: each component is a dense linear combination of all features

## PCA as Dictionary Learning

PCA learns a dictionary of k components, each of size d_features. A data point is reconstructed as a linear combination of these components:
X̂ᵢ = Σⱼ zⱼ * componentⱼ where zⱼ are the coordinates in PCA space.

**Limitation:** PCA allows all k components to contribute to every reconstruction. Real-world features are often sparse — a given input uses only a few features, not all of them.

## Sparse Dictionary Learning (SAE connection)

A sparse autoencoder replaces PCA's dense reconstruction with:
- An overcomplete dictionary (n_features >> d_model)
- A sparsity penalty (L1 on activations)
- The latent vector z is sparse: most entries are 0

This is the core conceptual bridge: PCA → sparse dictionary learning → SAEs.

## MI Forward Link (Critical)

The residual stream of a transformer is a d_model-dimensional vector space. If features in this space are superposed (Elhage et al. 2022), PCA cannot disentangle them because they're not orthogonal. SAEs solve this by learning an overcomplete, sparse decomposition.

Understanding PCA's limitations = understanding why SAEs exist.
