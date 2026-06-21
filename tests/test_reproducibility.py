"""Tests for reproducibility infrastructure."""

import numpy as np

from src.reproducibility import set_seed


def test_set_seed_numpy() -> None:
    """Calling set_seed should produce deterministic NumPy output."""
    set_seed(42)
    a = np.random.randn(10)
    set_seed(42)
    b = np.random.randn(10)
    assert np.allclose(a, b), "NumPy outputs differ after same seed"


def test_set_seed_torch() -> None:
    """Calling set_seed should produce deterministic PyTorch output."""
    try:
        import torch
    except ImportError:
        return  # skip if torch unavailable

    set_seed(42)
    a = torch.randn(10)
    set_seed(42)
    b = torch.randn(10)
    assert torch.allclose(a, b), "PyTorch outputs differ after same seed"


def test_set_seed_different_seeds_differ() -> None:
    """Different seeds should produce different outputs."""
    set_seed(1)
    a = np.random.randn(10)
    set_seed(2)
    b = np.random.randn(10)
    assert not np.allclose(a, b), "Different seeds produced same output"
