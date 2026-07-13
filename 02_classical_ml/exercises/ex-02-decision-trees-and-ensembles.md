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

## Solution

### 1. Decision Tree: Depth vs. Accuracy
```python
import numpy as np
import matplotlib.pyplot as plt
from src.data.datasets import make_classification, train_test_split
from src.models.tree_model import DecisionTree

X, y = make_classification(n_samples=500, n_features=8, n_informative=6, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

depths = range(1, 21)
train_scores, test_scores = [], []
for d in depths:
    tree = DecisionTree(max_depth=d, criterion="gini")
    tree.fit(X_train, y_train)
    train_scores.append(np.mean(tree.predict(X_train) == y_train))
    test_scores.append(np.mean(tree.predict(X_test) == y_test))

plt.plot(depths, train_scores, label="Train")
plt.plot(depths, test_scores, label="Test")
plt.axvline(x=6, color="red", linestyle="--", alpha=0.5, label="Optimal depth ~6")
plt.xlabel("max_depth"); plt.ylabel("Accuracy"); plt.legend()
plt.savefig("figures/ex02_depth_vs_accuracy.png", dpi=150)
```
Overfitting begins around depth 8-10: training accuracy continues rising while test accuracy plateaus or declines.

### 2. Feature Importance
```python
tree = DecisionTree(max_depth=6)
tree.fit(X_train, y_train)
importances = tree.feature_importances()
for i, imp in enumerate(importances):
    print(f"Feature {i}: {imp:.3f}")
```

### 3. Random Forest
```python
from src.models.tree_model import RandomForest

n_estimators_list = [10, 20, 50, 100, 200]
rf_scores = []
for n in n_estimators_list:
    rf = RandomForest(n_estimators=n, max_depth=10)
    rf.fit(X_train, y_train)
    rf_scores.append(np.mean(rf.predict(X_test) == y_test))

plt.plot(n_estimators_list, rf_scores, marker="o")
plt.xlabel("n_estimators"); plt.ylabel("Test Accuracy")
plt.savefig("figures/ex02_forest_accuracy.png", dpi=150)
```
Random forest reduces variance without increasing bias: it does not overfit as depth increases because each tree is trained on a different bootstrap sample with random feature subsets, decorrelating their errors.

### 4. sklearn Comparison
```python
from sklearn.ensemble import RandomForestClassifier
sk_rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
sk_rf.fit(X_train, y_train)
sk_acc = np.mean(sk_rf.predict(X_test) == y_test)
# Typical result: own RF ~0.86 vs sklearn ~0.88 — small gap due to optimizations
```

### MI Forward Link
Attention heads operate as an ensemble of specialized information selectors, each reading different positions and features via their QK/OV circuits. Like random forests reduce variance by combining diverse trees, multi-head attention reduces representational bias by combining diverse head views. The phase change in grokking — where the model prunes unnecessary circuits — is analogous to cost-complexity pruning in decision trees, where weak branches are removed to improve generalization.

## Deliverables
- Plots: depth vs. accuracy, n_estimators vs. accuracy
- Table: comparison of your implementation vs. sklearn
- Paragraph: MI connection

## Links

- [[02_classical_ml/proofs/trees-ensembles-pca]] — the formal proof of decision tree splitting, random forest variance reduction, and PCA that this exercise verifies in code.
- [[03_deep_learning/notes/training-dynamics-and-grokking]] — links ensemble pruning to the grokking phase change where models shed unnecessary circuits.

