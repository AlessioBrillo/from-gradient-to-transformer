"""Toy dataset generators and train/test splitting."""

import numpy as np


def train_test_split(
    X: np.ndarray, y: np.ndarray,
    test_size: float = 0.2, seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    X, y = np.asarray(X), np.asarray(y)
    n = X.shape[0]
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    split = int(n * (1 - test_size))
    return (
        X[idx[:split]], X[idx[split:]],
        y[idx[:split]], y[idx[split:]],
    )


def make_classification(
    n_samples: int = 100,
    n_features: int = 10,
    n_informative: int = 5,
    n_redundant: int = 2,
    flip_y: float = 0.01,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n_informative = min(n_informative, n_features)
    X = rng.standard_normal((n_samples, n_features))
    # Informative features: linear combination with random signs
    w = np.zeros(n_features)
    w[:n_informative] = rng.choice([-1.0, 1.0], size=n_informative)
    # Redundant features: copies of informative with noise
    for i in range(n_informative, min(n_informative + n_redundant, n_features)):
        src = rng.integers(0, n_informative)
        X[:, i] = X[:, src] + rng.standard_normal(n_samples) * 0.1
        w[i] = w[src] * 0.5
    logits = X @ w
    # Flip some labels for noise
    y = (logits > 0).astype(np.float64)
    n_flip = int(n_samples * flip_y)
    flip_idx = rng.choice(n_samples, n_flip, replace=False)
    y[flip_idx] = 1.0 - y[flip_idx]
    return X, y


def make_regression(
    n_samples: int = 100,
    n_features: int = 10,
    noise: float = 1.0,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n_samples, n_features))
    w = rng.standard_normal(n_features)
    y = X @ w + rng.standard_normal(n_samples) * noise
    return X, y


def make_moons(
    n_samples: int = 100,
    noise: float = 0.1,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = n_samples // 2
    t = np.linspace(0, np.pi, n)
    X1 = np.column_stack([np.cos(t), np.sin(t)])
    X1 += rng.standard_normal((n, 2)) * noise
    X2 = np.column_stack([1 - np.cos(t), -np.sin(t) + 0.5])
    X2 += rng.standard_normal((n, 2)) * noise
    X = np.vstack([X1, X2])
    y = np.hstack([np.zeros(n), np.ones(n)])
    return X, y
