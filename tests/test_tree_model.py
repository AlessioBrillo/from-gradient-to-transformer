"""Tests for DecisionTree and RandomForest from scratch."""

import numpy as np

from src.data.datasets import make_classification
from src.models.tree_model import DecisionTree, RandomForest


class TestDecisionTree:
    def test_shape(self) -> None:
        X, y = make_classification(n_samples=50, n_features=4, seed=42)
        model = DecisionTree(max_depth=5, seed=42)
        model.fit(X, y)
        preds = model.predict(X)
        assert preds.shape == (50,)

    def test_perfect_fit(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.standard_normal((100, 2))
        y = (X[:, 0] + X[:, 1] > 0).astype(np.float64)
        model = DecisionTree(max_depth=10, seed=42)
        model.fit(X, y)
        preds = model.predict(X)
        acc = (preds == y).mean()
        assert acc > 0.9, f"Accuracy too low: {acc:.3f}"

    def test_predict_before_fit_raises(self) -> None:
        model = DecisionTree()
        try:
            model.predict(np.ones((3, 2)))
            assert False, "Should have raised"
        except RuntimeError:
            pass

    def test_max_depth(self) -> None:
        X, y = make_classification(n_samples=100, n_features=4, seed=42)
        model = DecisionTree(max_depth=3, seed=42)
        model.fit(X, y)
        assert model.tree_ is not None


class TestRandomForest:
    def test_shape(self) -> None:
        X, y = make_classification(n_samples=50, n_features=4, seed=42)
        model = RandomForest(n_estimators=10, max_depth=5, seed=42)
        model.fit(X, y)
        preds = model.predict(X)
        assert preds.shape == (50,)

    def test_improves_over_single_tree(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.standard_normal((200, 5))
        y = (X[:, 0] + X[:, 2] > 0).astype(np.float64)
        tree = DecisionTree(max_depth=None, seed=42)
        tree.fit(X, y)
        tree_acc = (tree.predict(X) == y).mean()
        forest = RandomForest(n_estimators=20, max_depth=None, seed=42)
        forest.fit(X, y)
        forest_acc = (forest.predict(X) == y).mean()
        assert forest_acc >= tree_acc - 0.05

    def test_n_estimators(self) -> None:
        X, y = make_classification(n_samples=50, n_features=4, seed=42)
        model = RandomForest(n_estimators=5, seed=42)
        model.fit(X, y)
        assert len(model.trees_) == 5
