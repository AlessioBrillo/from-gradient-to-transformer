"""Tests for evaluation metrics."""

import numpy as np

from src.evaluation.metrics import (
    accuracy_score,
    confusion_matrix,
    cross_val_score,
    f1_score,
    mae,
    precision_score,
    r2_score,
    recall_score,
    rmse,
    roc_auc_score,
)
from src.models.linear_model import LinearRegression, LogisticRegression


class TestAccuracy:
    def test_perfect(self) -> None:
        y = np.array([0, 1, 0, 1])
        assert accuracy_score(y, y) == 1.0

    def test_half(self) -> None:
        y_true = np.array([0, 0, 1, 1])
        y_pred = np.array([0, 1, 0, 1])
        assert accuracy_score(y_true, y_pred) == 0.5

    def test_mismatch_raises(self) -> None:
        try:
            accuracy_score(np.ones(3), np.ones(4))
            assert False
        except ValueError:
            pass


class TestConfusionMatrix:
    def test_binary(self) -> None:
        y_true = np.array([0, 0, 1, 1, 0])
        y_pred = np.array([0, 1, 1, 1, 0])
        cm = confusion_matrix(y_true, y_pred)
        assert cm.shape == (2, 2)
        assert cm[0, 0] == 2  # TN
        assert cm[0, 1] == 1  # FP
        assert cm[1, 0] == 0  # FN
        assert cm[1, 1] == 2  # TP


class TestPrecisionRecallF1:
    def test_perfect_binary(self) -> None:
        y = np.array([0, 0, 1, 1])
        assert precision_score(y, y, pos_label=1) == 1.0
        assert recall_score(y, y, pos_label=1) == 1.0
        assert f1_score(y, y, pos_label=1) == 1.0

    def test_imperfect(self) -> None:
        y_true = np.array([0, 0, 1, 1, 1])
        y_pred = np.array([0, 1, 1, 1, 0])
        p = precision_score(y_true, y_pred, pos_label=1)
        r = recall_score(y_true, y_pred, pos_label=1)
        assert p < 1.0 and r < 1.0
        f = f1_score(y_true, y_pred, pos_label=1)
        assert 0 < f < 1.0


class TestRegressionMetrics:
    def test_rmse_perfect(self) -> None:
        y = np.array([1.0, 2.0, 3.0])
        assert rmse(y, y) == 0.0

    def test_mae_perfect(self) -> None:
        y = np.array([1.0, 2.0, 3.0])
        assert mae(y, y) == 0.0

    def test_r2_perfect(self) -> None:
        y = np.array([1.0, 2.0, 3.0])
        assert r2_score(y, y) == 1.0


class TestRocAuc:
    def test_perfect_separation(self) -> None:
        y_true = np.array([0, 0, 1, 1])
        y_score = np.array([0.1, 0.2, 0.8, 0.9])
        assert roc_auc_score(y_true, y_score) == 1.0

    def test_random(self) -> None:
        rng = np.random.default_rng(42)
        y_true = rng.integers(0, 2, size=100)
        y_score = rng.uniform(size=100)
        auc = roc_auc_score(y_true, y_score)
        assert 0.3 < auc < 0.7  # random ~0.5

    def test_reversed(self) -> None:
        y_true = np.array([0, 0, 1, 1])
        y_score = np.array([0.9, 0.8, 0.1, 0.2])
        assert roc_auc_score(y_true, y_score) == 0.0


class TestCrossVal:
    def test_regression(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.standard_normal((50, 2))
        y = X[:, 0] * 2 + X[:, 1] * (-1) + 0.5
        scores = cross_val_score(
            LinearRegression(solver="svd"), X, y, cv=3, metric="r2"
        )
        assert scores.shape == (3,)
        assert scores.mean() > 0.5

    def test_classification(self) -> None:
        rng = np.random.default_rng(42)
        X = rng.standard_normal((60, 3))
        y = (X[:, 0] + X[:, 1] > 0).astype(np.float64)
        scores = cross_val_score(
            LogisticRegression(), X, y, cv=3, metric="accuracy"
        )
        assert scores.shape == (3,)
        assert scores.mean() > 0.5

    def test_invalid_metric_raises(self) -> None:
        X = np.ones((10, 2))
        y = np.ones(10)
        try:
            cross_val_score(LinearRegression(), X, y, cv=2, metric="bogus")
            assert False
        except ValueError:
            pass
