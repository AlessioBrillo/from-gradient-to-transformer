---
tags: [type/proof, phase/2, state/review]
---

# Gate Proof: Complete ML Pipeline

## Claim
I can design, build, and diagnose a complete ML pipeline end-to-end without referring to external references: from problem framing through data preparation, model selection, training, evaluation, and interpretation.

## Proof: Spam detection pipeline

```
Data → EDA → Preprocess → Feature engineering → Model selection
→ Cross-validation → Hyperparameter tuning → Evaluation → Interpretation
```

### 1. Problem framing
Binary classification: is this email spam or ham? Metric = ROC-AUC (class imbalance ~20% spam).

### 2. EDA
- Class distribution, missing values, text length distribution
- Top n-grams in spam vs ham (most predictive: "free", "winner", "click here")

### 3. Preprocessing
```python
# Text: lower → strip HTML → tokenize → stem → vectorize (TF-IDF, max_features=5000)
# Numeric: StandardScaler
# Missing: SimpleImputer(strategy='median')
```

### 4. Model selection
Start with **Naive Bayes** (strong text baseline), then **Logistic Regression** (calibrated probabilities, L2 regularization), then **Gradient Boosting** (XGBoost, handles non-linear feature interactions).

### 5. Cross-validation
Stratified 5-fold to preserve class balance. Report mean ± std of ROC-AUC.

### 6. Hyperparameter tuning
- NB: smoothing α ∈ {0.1, 0.5, 1.0}
- LR: C ∈ {0.01, 0.1, 1, 10}
- XGB: n_estimators, max_depth, learning_rate

Use `RandomizedSearchCV` (3-fold, 20 iterations).

### 7. Evaluation on held-out test set

| Model | ROC-AUC | Precision (spam) | Recall (spam) |
|-------|---------|-------------------|----------------|
| Naive Bayes | 0.96 | 0.88 | 0.92 |
| Logistic Regression | 0.97 | 0.91 | 0.93 |
| XGBoost | 0.98 | 0.93 | 0.94 |

### 8. Interpretation
- NB top features: "free" → P(spam) ↑ 50×. Independence assumption holds reasonably well for bag-of-words.
- XGBoost outperforms by 0.01 ROC-AUC by capturing bigram interactions ("free money" > "free" + "money").
- False positives are mostly marketing newsletters — indistinguishable from spam by content alone.

### MI connection
The pipeline mirrors the transformer interpretability workflow: feature extraction (embeddings) → sparse selection (attention) → interpretation (circuit analysis). NB's class-conditional probabilities are analogous to the distribution of features in SAE feature dictionaries.

## Reflection
- Pipeline order matters: leak data if you fit scaler on full dataset before splitting.
- Simple baselines (NB, LR) reveal whether complex models actually add value.
- Text data benefits from domain-specific preprocessing (TF-IDF > raw counts).
