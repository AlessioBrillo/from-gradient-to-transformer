"""Tests for PCA and KMeans from scratch."""

import numpy as np

from src.models.pca import PCA, KMeans


class TestPCA:
    def test_shape(self) -> None:
        X = np.random.default_rng(42).standard_normal((50, 10))
        pca = PCA(n_components=3).fit(X)
        assert pca.components_ is not None
        assert pca.components_.shape == (3, 10)
        assert pca.explained_variance_ratio_ is not None
        assert pca.explained_variance_ratio_.shape == (3,)

    def test_transform_shape(self) -> None:
        X = np.random.default_rng(42).standard_normal((50, 10))
        pca = PCA(n_components=3).fit(X)
        X_t = pca.transform(X)
        assert X_t.shape == (50, 3)

    def test_variance_sum(self) -> None:
        X = np.random.default_rng(42).standard_normal((100, 5))
        pca = PCA(n_components=5).fit(X)
        assert pca.explained_variance_ratio_ is not None
        assert np.allclose(pca.explained_variance_ratio_.sum(), 1.0, atol=1e-10)

    def test_inverse_transform(self) -> None:
        X = np.random.default_rng(42).standard_normal((50, 5))
        pca = PCA(n_components=5).fit(X)
        X_t = pca.transform(X)
        X_r = pca.inverse_transform(X_t)
        assert np.allclose(X, X_r, atol=1e-10)

    def test_whiten(self) -> None:
        X = np.random.default_rng(42).standard_normal((200, 5))
        pca = PCA(n_components=3, whiten=True).fit(X)
        X_t = pca.transform(X)
        assert np.allclose(X_t.var(axis=0), np.ones(3), atol=0.1)

    def test_predict_before_fit_raises(self) -> None:
        pca = PCA(n_components=2)
        try:
            pca.transform(np.ones((3, 4)))
            assert False, "Should have raised"
        except RuntimeError:
            pass


class TestKMeans:
    def test_shape(self) -> None:
        X = np.random.default_rng(42).standard_normal((50, 2))
        km = KMeans(n_clusters=3, seed=42).fit(X)
        assert km.cluster_centers_ is not None
        assert km.cluster_centers_.shape == (3, 2)
        assert km.labels_ is not None
        assert km.labels_.shape == (50,)

    def test_separable_clusters(self) -> None:
        rng = np.random.default_rng(42)
        X = np.vstack([
            rng.standard_normal((30, 2)) + np.array([0, 0]),
            rng.standard_normal((30, 2)) + np.array([5, 5]),
        ])
        km = KMeans(n_clusters=2, seed=42).fit(X)
        assert km.labels_ is not None
        # Check the two clusters are separated (each centroid captures one group)
        assert km.cluster_centers_ is not None
        dist = np.linalg.norm(km.cluster_centers_[0] - km.cluster_centers_[1])
        assert dist > 2.0, f"Centroids too close: {dist:.2f}"

    def test_predict_after_fit(self) -> None:
        X = np.random.default_rng(42).standard_normal((30, 2))
        km = KMeans(n_clusters=3, seed=42).fit(X)
        preds = km.predict(np.array([[0.0, 0.0], [10.0, 10.0]]))
        assert preds.shape == (2,)
