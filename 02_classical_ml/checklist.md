---
tags: [checklist, phase/2]
---

# Checklist — Phase 2 · Classical ML

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

**MI framing:** PCA/dictionary learning is the conceptual ancestor of sparse autoencoders. SVM margin intuition maps to how attention heads separate representations. Bias/variance diagnosis maps to understanding memorization vs. generalization in grokking.

## Phase gate
- [ ] **Proof passed** → I can move to the next phase. (gate proof: [[02_classical_ml/proofs/complete-ml-pipeline]] — not yet done)

## Skills
- [x] Linear regression: closed-form + gradient descent (proof: [[02_classical_ml/proofs/linear-logistic-regression]], exercise: [[02_classical_ml/exercises/ex-01-linear-and-logistic-regression]])
- [x] Logistic regression: decision boundary, probabilistic interpretation (same proof/exercise)
- [x] Decision trees: impurity measures, pruning (proof: [[02_classical_ml/proofs/trees-ensembles-pca]], exercise: [[02_classical_ml/exercises/ex-02-decision-trees-and-ensembles]], code: `src/models/tree_model.py`)
- [x] Random forest: bagging, feature importance (same proof/exercise/code)
- [ ] Gradient boosting: XGBoost/LightGBM hands-on
- [x] Support Vector Machines: maximum margin, kernel trick — **forward link: circuit intuition (attention separability)** (note: [[02_classical_ml/notes/svm-and-margin]])
- [ ] Naive Bayes: probabilistic classifier, conditional independence assumption
- [x] Cross-validation: k-fold, stratified, grouped (code: `src/evaluation/metrics.py` — `cross_val_score`)
- [x] Metrics: accuracy, precision, recall, F1, ROC-AUC, RMSE, MAE (code: `src/evaluation/metrics.py`)
- [x] Bias/variance diagnosis: learning curves, regularization path (note: [[02_classical_ml/notes/bias-variance-and-evaluation]])
- [x] Feature engineering: encoding, scaling, interactions (note: [[02_classical_ml/notes/bias-variance-and-evaluation]])
- [x] Data leakage: detection and prevention (note: [[02_classical_ml/notes/bias-variance-and-evaluation]])
- [x] PCA: implementation, variance explanation, connection to SAEs (proof: [[02_classical_ml/proofs/trees-ensembles-pca]], exercise: [[02_classical_ml/exercises/ex-03-pca-and-feature-geometry]], code: `src/models/pca.py`)
- [x] k-means: elbow method, silhouette score (code: `src/models/pca.py` — KMeans class)
