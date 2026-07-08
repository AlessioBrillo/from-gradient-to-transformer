---
tags: [phase/2, note, state/review]
MI-forward-link: "Gini impurity maps to attention entropy as a measure of how diffused/pure a head's focus is."
---

# Decision Trees — Notes

## Core Idea
Partition the feature space recursively into axis-aligned regions. Each leaf predicts the majority class (classification) or mean value (regression) of training samples that fall into it.

## Splitting Criteria

**Gini impurity** (classification):
- For a node with class distribution p = [p₁, p₂, ..., pₖ]: Gini(p) = 1 - Σ pᵢ²
- Range: [0, 1-1/k], 0 = pure, higher = impure
- Interpretation: probability of misclassifying a random sample if we label it randomly per-class distribution

**Entropy** (classification):
- H(p) = - Σ pᵢ log(pᵢ)
- Range: [0, log(k)]
- More sensitive to class imbalance than Gini

**MSE** (regression):
- Var(y) in the node
- Pooled variance after split = weighted average of child variances

**Information Gain** = parent_impurity - weighted_avg(child_impurities)

## Key Hyperparameters
- max_depth: stop splitting at depth
- min_samples_split: don't split nodes with fewer samples
- min_samples_leaf: don't create leaves with fewer samples
- max_features: randomly sample features at each split (Random Forest's core trick)

## Bias-Variance in Trees
- Deep trees: low bias, high variance (overfit)
- Shallow trees: high bias, low variance (underfit)
- Ensemble methods (RF, boosting) reduce variance while keeping bias low

## Pruning
Cost-complexity pruning: minimize impurity + α * |leaves|. Higher α → smaller tree.

## MI Forward Link
Attention entropy (how diffused a head's focus is) is conceptually related to Gini impurity. An attention head that strongly attends to one position is "pure" (low entropy); one that distributes attention evenly is "impure" (high entropy). Gini impurity is used in circuits literature to measure induction-head formation.
