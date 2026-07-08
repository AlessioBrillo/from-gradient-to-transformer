"""Decision Tree and Random Forest from scratch (NumPy only)."""

from collections import Counter

import numpy as np


def _gini(y: np.ndarray) -> float:
    _, counts = np.unique(y, return_counts=True)
    probs = counts / counts.sum()
    return 1.0 - (probs ** 2).sum()


def _entropy(y: np.ndarray) -> float:
    _, counts = np.unique(y, return_counts=True)
    probs = counts / counts.sum()
    return -(probs * np.log(probs + 1e-10)).sum()


def _mse(y: np.ndarray) -> float:
    return np.var(y) if len(y) > 0 else 0.0


_CRITERION_FN = {"gini": _gini, "entropy": _entropy, "mse": _mse}


class DecisionTree:
    """Decision Tree classifier/regressor from scratch.

    Parameters
    ----------
    max_depth : int
        Maximum tree depth (default: None = unlimited).
    min_samples_split : int
        Minimum samples to split an internal node (default: 2).
    min_samples_leaf : int
        Minimum samples per leaf (default: 1).
    criterion : str
        Split criterion: "gini" (classification), "entropy" (classification),
        "mse" (regression) (default: "gini").
    max_features : int or float or None
        Number of features to consider for best split (default: None = all).
    seed : int
        Random seed (default: 42).
    """

    def __init__(
        self,
        max_depth: int | None = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        criterion: str = "gini",
        max_features: int | float | None = None,
        seed: int = 42,
    ) -> None:
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.max_features = max_features
        self.seed = seed
        self.tree_: dict | None = None
        self.n_classes_: int | None = None
        self.n_features_: int | None = None
        self._rng = np.random.default_rng(seed)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "DecisionTree":
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y)
        self.n_features_ = X.shape[1]
        self.n_classes_ = len(np.unique(y)) if y.ndim == 1 else None
        self.tree_ = self._grow(X, y, depth=0)
        return self

    def _grow(self, X: np.ndarray, y: np.ndarray, depth: int) -> dict:
        n_samples, n_features = X.shape
        n_classes = len(np.unique(y))

        stop = (
            (self.max_depth is not None and depth >= self.max_depth)
            or n_samples < self.min_samples_split
            or n_classes == 1
        )
        if stop:
            return self._make_leaf(y)

        feature_idxs = self._get_feature_idxs(n_features)
        best_split = self._best_split(X, y, feature_idxs)
        if best_split is None:
            return self._make_leaf(y)

        left_idx = X[:, best_split["feature"]] <= best_split["threshold"]
        if left_idx.sum() < self.min_samples_leaf or (~left_idx).sum() < self.min_samples_leaf:
            return self._make_leaf(y)

        return {
            "feature": best_split["feature"],
            "threshold": best_split["threshold"],
            "left": self._grow(X[left_idx], y[left_idx], depth + 1),
            "right": self._grow(X[~left_idx], y[~left_idx], depth + 1),
        }

    def _get_feature_idxs(self, n_features: int) -> np.ndarray:
        if self.max_features is None:
            return np.arange(n_features)
        if isinstance(self.max_features, float):
            k = max(1, int(self.max_features * n_features))
        else:
            k = min(n_features, self.max_features)
        return self._rng.choice(n_features, k, replace=False)

    def _make_leaf(self, y: np.ndarray) -> dict:
        if y.ndim == 1:
            values, counts = np.unique(y, return_counts=True)
            return {"value": values[counts.argmax()], "counts": counts.tolist()}
        return {"value": float(y.mean())}

    def _best_split(self, X: np.ndarray, y: np.ndarray, feature_idxs: np.ndarray) -> dict | None:
        best = None
        best_gain = -1.0
        criterion_fn = _CRITERION_FN.get(self.criterion, _gini)
        parent_loss = criterion_fn(y)

        for feat in feature_idxs:
            thresholds = np.unique(X[:, feat])
            if len(thresholds) > 10:
                # Speed up: quantile thresholds
                thresholds = np.percentile(thresholds, np.linspace(5, 95, 10))

            for thr in thresholds:
                left = y[X[:, feat] <= thr]
                right = y[X[:, feat] > thr]
                if len(left) < self.min_samples_leaf or len(right) < self.min_samples_leaf:
                    continue
                gain = parent_loss - (
                    len(left) * criterion_fn(left) + len(right) * criterion_fn(right)
                ) / len(y)
                if gain > best_gain:
                    best_gain = gain
                    best = {"feature": feat, "threshold": thr}

        return best

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.tree_ is None:
            raise RuntimeError("Model not fitted yet. Call .fit() first.")
        X = np.asarray(X, dtype=np.float64)
        return np.array([self._predict_row(row, self.tree_) for row in X])

    def _predict_row(self, row: np.ndarray, node: dict) -> float:
        if "value" in node:
            return float(node["value"])
        if row[node["feature"]] <= node["threshold"]:
            return self._predict_row(row, node["left"])
        return self._predict_row(row, node["right"])


class RandomForest:
    """Random Forest classifier/regressor.

    Parameters
    ----------
    n_estimators : int
        Number of trees (default: 100).
    max_depth : int or None
        Maximum tree depth (default: None).
    min_samples_split : int
        Minimum samples to split (default: 2).
    max_features : str or int or float or None
        Feature sampling: "sqrt", "log2", int, float, or None (default: "sqrt").
    criterion : str
        Split criterion (default: "gini").
    seed : int
        Random seed (default: 42).
    """

    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int | None = None,
        min_samples_split: int = 2,
        max_features: str | int | float | None = "sqrt",
        criterion: str = "gini",
        seed: int = 42,
    ) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.criterion = criterion
        self.seed = seed
        self.trees_: list[DecisionTree] = []
        self._rng = np.random.default_rng(seed)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "RandomForest":
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y)
        n_features = X.shape[1]
        n_samples = X.shape[0]

        mf: int | float | None
        if isinstance(self.max_features, str):
            if self.max_features == "sqrt":
                mf = max(1, int(np.sqrt(n_features)))
            elif self.max_features == "log2":
                mf = max(1, int(np.log2(n_features)))
            else:
                mf = None
        else:
            mf = self.max_features

        self.trees_ = []
        for i in range(self.n_estimators):
            # Bootstrap sample
            idx = self._rng.integers(0, n_samples, size=n_samples)
            X_boot, y_boot = X[idx], y[idx]
            tree = DecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                min_samples_leaf=1,
                criterion=self.criterion,
                max_features=mf,
                seed=self.seed + i,
            )
            tree.fit(X_boot, y_boot)
            self.trees_.append(tree)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.trees_:
            raise RuntimeError("Model not fitted yet. Call .fit() first.")
        X = np.asarray(X, dtype=np.float64)
        preds = np.array([t.predict(X) for t in self.trees_])
        # Majority vote per sample
        return np.array([
            Counter(preds[:, i].tolist()).most_common(1)[0][0]
            for i in range(X.shape[0])
        ])

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.trees_:
            raise RuntimeError("Model not fitted yet. Call .fit() first.")
        X = np.asarray(X, dtype=np.float64)
        preds = np.array([t.predict(X) for t in self.trees_])
        n_classes = len(np.unique(preds))
        probas = np.zeros((X.shape[0], n_classes))
        for i in range(X.shape[0]):
            counts = Counter(preds[:, i].tolist())
            for cls, cnt in counts.items():
                probas[i, int(cls)] = cnt / len(self.trees_)
        return probas
