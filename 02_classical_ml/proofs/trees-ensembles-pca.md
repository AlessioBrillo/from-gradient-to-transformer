---
tags: [phase/2, proof, state/review]
---

# Proof to Myself: Decision Trees, Ensembles, and PCA

## Question
Without looking at any notes or code, explain how a decision tree decides where to split, how a random forest reduces variance, and how PCA finds principal components. Then connect each to a mechanistic interpretability concept.

## 1. Decision Tree Splitting
The tree evaluates each feature at each candidate threshold. For each split, it computes the weighted average impurity of the two child nodes. The split with the largest reduction in impurity (information gain) is chosen.

Impurity metrics: Gini = 1 - Σpᵢ², Entropy = -Σpᵢlog(pᵢ), MSE = variance (regression).

The process is recursive: children are split until a stopping criterion (max depth, min samples, pure node).

**MI connection:** Attention entropy is the same mathematical quantity applied to attention probability distributions. An "induction head" is a circuit where attention is highly "pure" (low entropy) — it consistently attends to the correct position. Gini impurity maps to attention entropy as a measure of circuit specificity.

## 2. Random Forest Variance Reduction
A single tree has high variance (small changes in training data → different splits). A random forest reduces this by:
- Bootstrap aggregation (bagging): each tree trains on a different bootstrap sample
- Random feature selection: at each split, each tree considers only a random subset of features

The ensemble averages many high-variance, low-correlation trees into a lower-variance prediction.

**MI connection:** Attention heads in a multi-head transformer function like a "forest" — each head learns a different attention pattern (specialized function), and their outputs are combined. The QK circuit determines "which features to look at" (analogous to max_features selection), and the OV circuit determines "what to copy" (analogous to the tree's prediction).

## 3. PCA via SVD
PCA finds the orthogonal directions of maximum variance in the data.

1. Center the data (subtract mean)
2. Compute SVD: X = UΣVᵀ
3. Principal components = rows of Vᵀ (eigenvectors of XᵀX)
4. Explained variance = singular values² / total sum of squares

The first component captures the direction of highest variance, the second captures the most remaining variance orthogonal to the first, etc.

**MI connection:** PCA is the conceptual ancestor of sparse autoencoders (SAEs). PCA learns a dense, orthogonal basis; SAEs learn a sparse, overcomplete basis. The residual stream features are superposed (not orthogonal), which is why PCA fails where SAEs succeed. Understanding PCA's limitations = understanding why we need dictionary learning for MI.
