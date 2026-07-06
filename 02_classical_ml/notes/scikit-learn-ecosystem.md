---
tags: [type/lesson, phase/2]
state: review
created: 2026-07-05
---

# scikit-learn Ecosystem

## What it is
A unified Python API for classical ML: every model has the same `fit(X, y)` / `predict(X)` interface, composable via `Pipeline`.

## Why it exists
Standardizes the ML workflow so you can swap models, transforms, and evaluation strategies without rewriting code. The `Pipeline` + `ColumnTransformer` combo is one of the best-designed APIs in scientific Python.

## Key API conventions

| Method | Purpose |
|--------|---------|
| `fit(X, y)` | Learn parameters from data |
| `predict(X)` | Generate predictions |
| `transform(X)` | Apply transformation (preprocessors) |
| `fit_transform(X, y)` | Fit then transform (for transformers) |
| `score(X, y)` | Default evaluation metric |

**Every estimator inherits from `BaseEstimator`** — this gives you `get_params()` / `set_params()` for free, which is what enables `GridSearchCV`.

## Pipeline pattern

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression()),
])
pipe.fit(X_train, y_train)
pipe.predict(X_test)
```

A Pipeline is itself an estimator — it can be cross-validated, grid-searched, and serialized. This is the fundamental building block.

## Connections to our codebase
- [[02_classical_ml/notes/linear-regression|Linear Regression]] — we implement from scratch with the same API
- [[02_classical_ml/notes/logistic-regression|Logistic Regression]] — same API, from scratch
- [[02_classical_ml/notes/cross-validation-and-metrics|Cross-Validation]] — reimplements `cross_val_score`

## Open questions
- How does `Pipeline` handle caching of intermediate transforms? (#question)

## Links
- [[02_classical_ml/_MOC|Phase 2 MOC]]
- [[01_foundations/notes/numpy-basics-for-linear-algebra|NumPy Basics]]
