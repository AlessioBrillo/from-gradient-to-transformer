"""Tests for LinearRegression and LogisticRegression from scratch."""

import numpy as np

from src.data.datasets import make_classification, make_regression
from src.models.linear_model import LinearRegression, LogisticRegression


class TestLinearRegression:
    def test_svd_shape(self) -> None:
        X, y = make_regression(n_samples=50, n_features=5, seed=42)
        model = LinearRegression(solver="svd")
        model.fit(X, y)
        assert model.coef_ is not None and model.coef_.shape == (5,)
        assert isinstance(model.intercept_, float)
        preds = model.predict(X)
        assert preds.shape == (50,)

    def test_svd_recovery(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.standard_normal((100, 3))
        true_w = np.array([2.5, -1.3, 0.7])
        true_b = 4.2
        y = X @ true_w + true_b
        model = LinearRegression(solver="svd").fit(X, y)
        assert np.allclose(model.coef_, true_w, atol=1e-10)
        assert np.allclose(model.intercept_, true_b, atol=1e-10)

    def test_sgd_converges(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.standard_normal((200, 5))
        true_w = np.array([1.0, -2.0, 0.5, 3.0, -1.0])
        y = X @ true_w + 0.5
        model = LinearRegression(solver="sgd", fit_intercept=False)
        model.fit(X, y, lr=0.01, epochs=500, batch_size=32, seed=42)
        assert model.coef_ is not None
        assert np.allclose(model.coef_, true_w, atol=0.5)

    def test_no_intercept(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.standard_normal((50, 2))
        y = X @ np.array([1.5, -2.0])
        model = LinearRegression(solver="svd", fit_intercept=False)
        model.fit(X, y)
        assert model.intercept_ == 0.0
        assert np.allclose(model.coef_, [1.5, -2.0], atol=1e-10)

    def test_predict_before_fit_raises(self) -> None:
        model = LinearRegression()
        try:
            model.predict(np.ones((3, 2)))
            assert False, "Should have raised"
        except RuntimeError:
            pass

    def test_shape_mismatch_raises(self) -> None:
        model = LinearRegression()
        try:
            model.fit(np.ones((10, 2)), np.ones(5))
            assert False, "Should have raised"
        except ValueError:
            pass

    def test_not_2d_raises(self) -> None:
        model = LinearRegression()
        try:
            model.fit(np.ones(10), np.ones(10))
            assert False, "Should have raised"
        except ValueError:
            pass


class TestLogisticRegression:
    def test_shape(self) -> None:
        X, y = make_classification(n_samples=50, n_features=4, seed=42)
        model = LogisticRegression()
        model.fit(X, y, lr=0.1, epochs=500, seed=42)
        assert model.coef_ is not None and model.coef_.shape == (4,)
        preds = model.predict(X)
        assert preds.shape == (50,)
        probs = model.predict_proba(X)
        assert probs.shape == (50,)
        assert np.all((probs >= 0) & (probs <= 1))

    def test_binary_separable(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.standard_normal((100, 2))
        # Linearly separable: x0 > 0 -> class 1
        y = (X[:, 0] > 0).astype(np.float64)
        model = LogisticRegression(C=10.0)
        model.fit(X, y, lr=0.1, epochs=1000, seed=42)
        preds = model.predict(X)
        acc = (preds == y).mean()
        assert acc > 0.95, f"Accuracy too low: {acc:.3f}"

    def test_predict_proba_range(self) -> None:
        X, y = make_classification(n_samples=50, n_features=3, seed=42)
        model = LogisticRegression().fit(X, y, seed=42)
        probs = model.predict_proba(X)
        assert np.all(probs >= 0.0) and np.all(probs <= 1.0)

    def test_auto_label_mapping(self) -> None:
        """Should auto-map labels like [-1, 1] to {0, 1}."""
        rng = np.random.default_rng(42)
        X = rng.standard_normal((50, 2))
        y = np.where(X[:, 0] > 0, 1, -1)
        model = LogisticRegression()
        model.fit(X, y, epochs=500, seed=42)
        preds = model.predict(X)
        assert set(preds.astype(int).tolist()).issubset({0, 1})

    def test_decision_function(self) -> None:
        X, y = make_classification(n_samples=30, n_features=3, seed=42)
        model = LogisticRegression().fit(X, y, epochs=500, seed=42)
        d = model.decision_function(X)
        assert d.shape == (30,)
        probs = model.predict_proba(X)
        assert np.allclose(probs, 1.0 / (1.0 + np.exp(-d)), atol=1e-10)

    def test_multiclass_raises(self) -> None:
        X = np.random.default_rng(42).standard_normal((30, 2))
        y = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2, 0] * 3)
        model = LogisticRegression()
        try:
            model.fit(X, y)
            assert False, "Should have raised on multi-class"
        except ValueError:
            pass
