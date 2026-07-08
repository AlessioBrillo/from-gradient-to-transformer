"""PCA and k-means clustering from scratch (NumPy only)."""

import numpy as np


class PCA:
    """Principal Component Analysis via SVD.

    Parameters
    ----------
    n_components : int or None
        Number of components to keep (default: None = keep all).
    whiten : bool
        If True, scale components to unit variance (default: False).

    Attributes
    ----------
    components_ : ndarray of shape (n_components, n_features)
        Principal axes in feature space (rows are components).
    explained_variance_ratio_ : ndarray of shape (n_components,)
        Percentage of variance explained by each component.
    mean_ : ndarray of shape (n_features,)
        Per-feature mean.
    singular_values_ : ndarray of shape (n_components,)
        Singular values from SVD.
    """

    def __init__(self, n_components: int | None = None, whiten: bool = False) -> None:
        self.n_components = n_components
        self.whiten = whiten
        self.components_: np.ndarray | None = None
        self.explained_variance_ratio_: np.ndarray | None = None
        self.mean_: np.ndarray | None = None
        self.singular_values_: np.ndarray | None = None

    def fit(self, X: np.ndarray) -> "PCA":
        X = np.asarray(X, dtype=np.float64)
        self.mean_ = X.mean(axis=0)
        X_centered = X - self.mean_

        # SVD on centered data
        U, s, Vt = np.linalg.svd(X_centered, full_matrices=False)
        n_components = self.n_components or X.shape[1]

        self.components_ = Vt[:n_components]
        self.singular_values_ = s[:n_components]

        total_var = (s ** 2).sum()
        self.explained_variance_ratio_ = (s[:n_components] ** 2) / total_var

        if self.whiten:
            scale = s[:n_components, np.newaxis] / np.sqrt(X.shape[0])
            self.components_ = self.components_ / scale

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.components_ is None or self.mean_ is None:
            raise RuntimeError("PCA not fitted. Call .fit() first.")
        X = np.asarray(X, dtype=np.float64)
        return (X - self.mean_) @ self.components_.T

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X_transformed: np.ndarray) -> np.ndarray:
        if self.components_ is None or self.mean_ is None:
            raise RuntimeError("PCA not fitted. Call .fit() first.")
        X_transformed = np.asarray(X_transformed, dtype=np.float64)
        return X_transformed @ self.components_ + self.mean_


class KMeans:
    """k-means clustering from scratch.

    Parameters
    ----------
    n_clusters : int
        Number of clusters (default: 8).
    max_iter : int
        Maximum iterations (default: 300).
    n_init : int
        Number of initializations with different centroid seeds (default: 10).
    seed : int
        Random seed (default: 42).

    Attributes
    ----------
    cluster_centers_ : ndarray of shape (n_clusters, n_features)
        Coordinates of cluster centers.
    labels_ : ndarray of shape (n_samples,)
        Labels for each point.
    inertia_ : float
        Sum of squared distances to nearest centroid.
    """

    def __init__(
        self,
        n_clusters: int = 8,
        max_iter: int = 300,
        n_init: int = 10,
        seed: int = 42,
    ) -> None:
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.n_init = n_init
        self.seed = seed
        self.cluster_centers_: np.ndarray | None = None
        self.labels_: np.ndarray | None = None
        self.inertia_: float = 0.0

    def fit(self, X: np.ndarray) -> "KMeans":
        X = np.asarray(X, dtype=np.float64)
        best_centers = None
        best_labels = None
        best_inertia = float("inf")

        for init in range(self.n_init):
            rng = np.random.default_rng(self.seed + init)
            centers = X[rng.choice(X.shape[0], self.n_clusters, replace=False)]
            labels, inertia = self._kmeans_iterate(X, centers)
            if inertia < best_inertia:
                best_centers = centers
                best_labels = labels
                best_inertia = inertia

        self.cluster_centers_ = best_centers
        self.labels_ = best_labels
        self.inertia_ = best_inertia
        return self

    def _kmeans_iterate(
        self, X: np.ndarray, centers: np.ndarray
    ) -> tuple[np.ndarray, float]:
        for _ in range(self.max_iter):
            distances = np.linalg.norm(X[:, np.newaxis] - centers, axis=2)
            labels = distances.argmin(axis=1)
            new_centers = np.array([
                X[labels == k].mean(axis=0) if (labels == k).sum() > 0 else centers[k]
                for k in range(self.n_clusters)
            ])
            if np.allclose(centers, new_centers):
                break
            centers = new_centers

        distances = np.linalg.norm(X[:, np.newaxis] - centers, axis=2)
        labels = distances.argmin(axis=1)
        inertia = (distances[np.arange(len(X)), labels] ** 2).sum()
        return labels, inertia

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.cluster_centers_ is None:
            raise RuntimeError("KMeans not fitted. Call .fit() first.")
        X = np.asarray(X, dtype=np.float64)
        distances = np.linalg.norm(X[:, np.newaxis] - self.cluster_centers_, axis=2)
        return distances.argmin(axis=1)

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        self.fit(X)
        return self.labels_
