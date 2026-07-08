# Exercise 03 — PCA, Feature Geometry, and the SAE Connection

## Objective
Implement PCA from scratch, understand the geometry of dimensionality reduction, and build the conceptual bridge to sparse autoencoders.

## Tasks

### 1. PCA from Scratch
Using your `PCA` implementation in `src/models/pca.py`:
- Generate a synthetic dataset with 20 features where only 5 are informative
- Fit PCA and plot explained variance ratio
- How many components capture 90% of variance?
- Compare with sklearn's PCA

### 2. Visualization
- Apply PCA to the Iris dataset (4D → 2D)
- Color points by class
- Interpret the separation in PCA space

### 3. PCA as Data Compression
- Use PCA to compress and reconstruct the Iris data with k = [1, 2, 3, 4] components
- Plot reconstruction error (MSE) vs. number of components
- Find the "elbow"

### 4. The SAE Bridge
- PCA gives you orthogonal components, sorted by variance
- A sparse autoencoder gives you overcomplete, sparse features
- For the same 20-feature synthetic data, why would PCA struggle if features are not axis-aligned?
- Write a note: "When PCA fails, SAEs are needed"

### MI Forward Link
The residual stream is a vector space where features live in superposition. PCA assumes features are orthogonal — but in superposition, features are not orthogonal (they share dimensions). This is why we need sparse dictionary learning (SAEs) instead of PCA for MI work.

## Deliverables
- Explained variance plot (scree plot)
- 2D PCA visualization of Iris
- Reconstruction error curve
- Written explanation of PCA vs. SAE
