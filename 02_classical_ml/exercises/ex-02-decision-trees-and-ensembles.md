---
tags: [type/exercise, phase/2, state/review]
---

# Exercise 02 — Decision Trees and Random Forests

## Objective
Implement and compare decision trees, random forests, and gradient boosting on a real dataset. Understand the bias-variance dynamics of each method.

## Setup
Use the Titanic or a similar Kaggle dataset. Load, clean, and perform EDA.

## Tasks

### 1. Decision Tree from Scratch
Using your `DecisionTree` implementation in `src/models/tree_model.py`, train a tree on the dataset:
- Vary `max_depth` from 1 to 20
- Plot train/val accuracy vs. depth
- Identify the depth where overfitting begins

### 2. Feature Importance
Extract feature importances from your tree (how often each feature is used for splitting). Compare with sklearn's `DecisionTreeClassifier.feature_importances_`.

### 3. Random Forest
Train your `RandomForest` on the same data:
- Vary `n_estimators` from 10 to 200
- Compare the learning curve with a single decision tree
- Does the forest overfit as depth increases? Why or why not?

### 4. Compare with sklearn
Use `sklearn.ensemble.RandomForestClassifier` on the same data. Compare accuracy, training time, and feature importances.

### MI Forward Link
Write 3-4 sentences connecting ensemble methods to transformer circuits:
- Attention heads can be seen as an "ensemble" of information selectors
- The QK/OV decomposition means each head has specialized function (like trees in a forest)
- Pruning in decision trees (cost-complexity pruning) is analogous to weight decay pruning unnecessary circuits in grokking

## Deliverables
- Plots: depth vs. accuracy, n_estimators vs. accuracy
- Table: comparison of your implementation vs. sklearn
- Paragraph: MI connection

## Links

- [[02_classical_ml/proofs/trees-ensembles-pca]] — the formal proof of decision tree splitting, random forest variance reduction, and PCA that this exercise verifies in code.
- [[03_deep_learning/notes/training-dynamics-and-grokking]] — links ensemble pruning to the grokking phase change where models shed unnecessary circuits.

