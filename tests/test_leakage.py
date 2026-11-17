"""Metrics against hand-computed values, and the leakage demonstration."""

from __future__ import annotations

import numpy as np

from src.evaluation.leakage import cv_accuracy_on_noise
from src.evaluation.metrics import (
    accuracy_score,
    cross_val_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

# 10 samples: 4 positives. The classifier finds 3 of them and raises 1 false alarm.
Y = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0])
P = np.array([1, 1, 1, 0, 1, 0, 0, 0, 0, 0])


def test_hand_computed_classification_metrics() -> None:
    assert accuracy_score(Y, P) == 0.8  # 8 of 10 right
    assert precision_score(Y, P) == 0.75  # 3 of the 4 flagged are real
    assert recall_score(Y, P) == 0.75  # 3 of the 4 real are found
    assert f1_score(Y, P) == 0.75  # harmonic mean of equal values


def test_accuracy_hides_a_useless_classifier_on_imbalanced_data() -> None:
    y = np.array([1] + [0] * 99)
    always_negative = np.zeros(100, dtype=int)
    assert accuracy_score(y, always_negative) == 0.99
    assert recall_score(y, always_negative) == 0.0


def test_auc_of_a_perfect_ranking_a_reversed_one_and_a_tie() -> None:
    y = np.array([0, 0, 1, 1])
    assert roc_auc_score(y, np.array([0.1, 0.2, 0.8, 0.9])) == 1.0
    assert roc_auc_score(y, np.array([0.9, 0.8, 0.2, 0.1])) == 0.0
    assert roc_auc_score(y, np.array([0.5, 0.5, 0.5, 0.5])) == 0.5  # a constant scorer


def test_auc_counts_a_tied_positive_negative_pair_as_half() -> None:
    """Positives score {0.5, 0.9}, negatives {0.5, 0.1}: of the 4 pairs, three are
    won outright and one is tied, so AUC = (3 + 0.5) / 4. The result must not
    depend on the order in which tied scores happen to appear."""
    scores = np.array([0.5, 0.5, 0.9, 0.1])
    for y in (np.array([0, 1, 1, 0]), np.array([1, 0, 1, 0])):
        assert roc_auc_score(y, scores) == 0.875


class _Majority:
    """A model that always predicts the most common training label."""

    label = 0

    def fit(self, features: np.ndarray, y: np.ndarray) -> "_Majority":
        self.label = int(np.bincount(y).argmax())
        return self

    def predict(self, features: np.ndarray) -> np.ndarray:
        return np.full(len(features), self.label)


def test_cross_val_score_is_reproducible_with_a_seed_and_covers_every_sample() -> None:
    X, y = np.arange(40).reshape(20, 2), np.array([0, 1] * 10)
    a = cross_val_score(_Majority(), X, y, cv=5, seed=3)
    b = cross_val_score(_Majority(), X, y, cv=5, seed=3)
    assert np.array_equal(a, b) and len(a) == 5


def test_selecting_features_before_cross_validation_leaks_the_labels() -> None:
    """On pure-noise labels the truth is 0.5. Selecting the 20 best of 2000 features on
    all the data first gives ~0.96; selecting inside each training fold gives ~0.48."""
    leaky = np.mean([cv_accuracy_on_noise(s, leak=True) for s in range(10)])
    clean = np.mean([cv_accuracy_on_noise(s, leak=False) for s in range(10)])
    assert leaky > 0.85
    assert 0.4 < clean < 0.6
    assert leaky - clean > 0.3
