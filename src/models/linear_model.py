"""Linear and Logistic Regression from scratch (NumPy only)."""

from typing import Literal

import numpy as np
from numpy.linalg import LinAlgError


def _add_bias(X: np.ndarray) -> np.ndarray:
    if X.ndim != 2:
        raise ValueError(f"Expected 2D array, got shape {X.shape}")
    return np.c_[np.ones(X.shape[0]), X]


def _standardize(
    X: np.ndarray, mean: np.ndarray | None = None, std: np.ndarray | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if mean is None:
        mean = X.mean(axis=0)
    if std is None:
        std = X.std(axis=0)
        std[std == 0] = 1.0
    return (X - mean) / std, mean, std


def _sigmoid(z: np.ndarray) -> np.ndarray:
    # Clip to avoid overflow in np.exp
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


class LinearRegression:
    """Ordinary Least Squares via SVD (default) or Mini-batch SGD.

    Parameters
    ----------
    solver : str
        "svd" uses closed-form via SVD (default). "sgd" uses mini-batch gradient descent.
    fit_intercept : bool
        If True, includes a bias term (default: True).

    Attributes
    ----------
    coef_ : ndarray of shape (n_features,)
    intercept_ : float
    """

    def __init__(self, solver: Literal["svd", "sgd"] = "svd", fit_intercept: bool = True) -> None:
        self.solver = solver
        self.fit_intercept = fit_intercept
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0

    def fit(
        self, X: np.ndarray, y: np.ndarray,
        lr: float = 0.01, epochs: int = 1000, batch_size: int = 32,
        seed: int = 42,
    ) -> "LinearRegression":
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).ravel()
        if X.ndim != 2:
            raise ValueError(f"X must be 2D, got {X.shape}")
        if X.shape[0] != y.shape[0]:
            raise ValueError(f"n_samples mismatch: X={X.shape[0]}, y={y.shape[0]}")

        if self.solver == "svd":
            self._fit_svd(X, y)
        elif self.solver == "sgd":
            self._fit_sgd(X, y, lr, epochs, batch_size, seed)
        else:
            raise ValueError(f"Unknown solver: {self.solver}")
        return self

    def _fit_svd(self, X: np.ndarray, y: np.ndarray) -> None:
        if self.fit_intercept:
            X_aug = _add_bias(X)
        else:
            X_aug = X.copy()
        try:
            U, s, Vt = np.linalg.svd(X_aug, full_matrices=False)
            s_inv = np.zeros_like(s)
            mask = s > max(X_aug.shape) * np.finfo(s.dtype).eps * s[0]
            s_inv[mask] = 1.0 / s[mask]
            w = Vt.T @ (s_inv * (U.T @ y))
        except LinAlgError:
            # Fallback to normal equations for degenerate cases
            w = np.linalg.lstsq(X_aug, y, rcond=None)[0]
        if self.fit_intercept:
            self.intercept_ = float(w[0])
            self.coef_ = w[1:]
        else:
            self.intercept_ = 0.0
            self.coef_ = w

    def _fit_sgd(
        self, X: np.ndarray, y: np.ndarray, lr: float, epochs: int, batch_size: int, seed: int
    ) -> None:
        rng = np.random.default_rng(seed)
        if self.fit_intercept:
            X_aug = _add_bias(X)
        else:
            X_aug = X.copy()
        n = X_aug.shape[1]
        w = rng.standard_normal(n) * 0.01
        for _ in range(epochs):
            idx = rng.permutation(X_aug.shape[0])
            X_aug, y = X_aug[idx], y[idx]
            for start in range(0, X_aug.shape[0], batch_size):
                X_batch = X_aug[start : start + batch_size]
                y_batch = y[start : start + batch_size]
                grad = X_batch.T @ (X_batch @ w - y_batch) / X_batch.shape[0]
                w -= lr * grad
        if self.fit_intercept:
            self.intercept_ = float(w[0])
            self.coef_ = w[1:]
        else:
            self.intercept_ = 0.0
            self.coef_ = w

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.coef_ is None:
            raise RuntimeError("Model not fitted yet. Call .fit() first.")
        X = np.asarray(X, dtype=np.float64)
        return X @ self.coef_ + self.intercept_


class LogisticRegression:
    """Binary logistic regression via mini-batch gradient descent.

    Parameters
    ----------
    fit_intercept : bool
        If True, includes a bias term (default: True).
    C : float
        Inverse regularization strength (default: 1.0). Smaller = stronger reg.

    Attributes
    ----------
    coef_ : ndarray of shape (n_features,)
    intercept_ : float
    """

    def __init__(self, fit_intercept: bool = True, C: float = 1.0) -> None:
        self.fit_intercept = fit_intercept
        self.C = C
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0

    def fit(
        self, X: np.ndarray, y: np.ndarray,
        lr: float = 0.1, epochs: int = 2000, batch_size: int = 32,
        seed: int = 42,
    ) -> "LogisticRegression":
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).ravel()
        if X.ndim != 2:
            raise ValueError(f"X must be 2D, got {X.shape}")
        if X.shape[0] != y.shape[0]:
            raise ValueError(f"n_samples mismatch: X={X.shape[0]}, y={y.shape[0]}")
        # Convert labels to {0, 1}
        unique = np.unique(y)
        if set(unique) - {0, 1}:
            # Map to {0, 1} if binary labels are not already 0/1
            if len(unique) != 2:
                raise ValueError(f"Only binary classification supported, got labels: {unique}")
            y = np.where(y == unique[0], 0, 1).astype(np.float64)

        rng = np.random.default_rng(seed)
        if self.fit_intercept:
            X_aug = _add_bias(X)
        else:
            X_aug = X.copy()

        n = X_aug.shape[1]
        w = rng.standard_normal(n) * 0.01
        # L2 regularization strength
        alpha = 1.0 / (self.C * X_aug.shape[0]) if self.C > 0 else 0.0

        for _ in range(epochs):
            idx = rng.permutation(X_aug.shape[0])
            X_aug_s, y_s = X_aug[idx], y[idx]
            for start in range(0, X_aug_s.shape[0], batch_size):
                X_batch = X_aug_s[start : start + batch_size]
                y_batch = y_s[start : start + batch_size]
                pred = _sigmoid(X_batch @ w)
                grad = X_batch.T @ (pred - y_batch) / X_batch.shape[0]
                if alpha > 0:
                    grad += alpha * w  # L2
                w -= lr * grad

        if self.fit_intercept:
            self.intercept_ = float(w[0])
            self.coef_ = w[1:]
        else:
            self.intercept_ = 0.0
            self.coef_ = w
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if self.coef_ is None:
            raise RuntimeError("Model not fitted yet. Call .fit() first.")
        X = np.asarray(X, dtype=np.float64)
        z = X @ self.coef_ + self.intercept_
        return _sigmoid(z)

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(X) >= threshold).astype(np.float64)

    def decision_function(self, X: np.ndarray) -> np.ndarray:
        if self.coef_ is None:
            raise RuntimeError("Model not fitted yet. Call .fit() first.")
        X = np.asarray(X, dtype=np.float64)
        return X @ self.coef_ + self.intercept_
