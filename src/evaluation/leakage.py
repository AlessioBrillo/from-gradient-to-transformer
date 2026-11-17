"""A demonstration of data leakage through feature selection (Phase 2 exercise).

Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning*, section 7.10.2:
choose the features most correlated with the label using *all* the data, then
cross-validate a classifier on those features. On labels that are pure noise the
cross-validated accuracy is far above chance, because the selection step has already
seen every validation label. Doing the selection inside each training fold removes
the effect.
"""

from __future__ import annotations

import numpy as np


def top_k_by_correlation(X: np.ndarray, y: np.ndarray, k: int) -> np.ndarray:
    """Indices of the k features with the largest |correlation| with y."""
    Xc = X - X.mean(axis=0)
    yc = y - y.mean()
    corr = np.abs(Xc.T @ yc) / (np.linalg.norm(Xc, axis=0) * np.linalg.norm(yc) + 1e-12)
    return np.argsort(corr)[::-1][:k]


def nearest_centroid_accuracy(
    X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray
) -> float:
    """Accuracy of a classifier that assigns the class with the closest mean."""
    mu0, mu1 = X_train[y_train == 0].mean(axis=0), X_train[y_train == 1].mean(axis=0)
    pred = (np.linalg.norm(X_val - mu1, axis=1) < np.linalg.norm(X_val - mu0, axis=1)).astype(int)
    return float((pred == y_val).mean())


def cv_accuracy_on_noise(
    seed: int, leak: bool, n: int = 50, p: int = 2000, k: int = 20, folds: int = 5
) -> float:
    """Cross-validated accuracy on random labels, with or without leakage.

    `leak=True` selects features on the whole data set before splitting;
    `leak=False` selects inside each training fold. The truth is 0.5 either way.
    """
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    y = rng.integers(0, 2, size=n)
    chosen_early = top_k_by_correlation(X, y, k) if leak else None
    order = rng.permutation(n)
    scores = []
    for fold in np.array_split(order, folds):
        train = np.setdiff1d(order, fold)
        cols = chosen_early if leak else top_k_by_correlation(X[train], y[train], k)
        Xtr, Xva = X[train][:, cols], X[fold][:, cols]
        scores.append(nearest_centroid_accuracy(Xtr, y[train], Xva, y[fold]))
    return float(np.mean(scores))
