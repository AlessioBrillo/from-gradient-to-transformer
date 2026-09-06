"""Regression tests for exp6 Fourier instrumentation on live weights.

The step-500 shakedown crash (MP-87 Session 1, dated 2026-09-06):
`train_single_seed()` passes `model.embed.weight[...]` — a tensor with
`requires_grad=True` — into `fourier_decomposition()`, which called
`.cpu().numpy()` on it. NumPy conversion of a grad-requiring tensor raises
`RuntimeError`, so every `--save-model` run reaching its first
`fourier_every` boundary died after ~34 minutes of training. The existing
capstone tests pin `fourier_every` to 10**9 (never fires), which is exactly
why the bug escaped: no test ever ran Fourier on a live weight.

Contract pinned here: instrumentation must never participate in autograd.
`fourier_decomposition()` must accept grad-requiring input and return plain
NumPy arrays with the same values as detached input.
"""

import numpy as np
import torch

from src.experiments.exp6_capstone import analyze_fourier_sparsity, fourier_decomposition


def _grad_embeddings(modulus: int = 17, d_model: int = 8) -> torch.Tensor:
    """Simulate the live-weight slice the training loop passes in."""
    return torch.randn(modulus, d_model, requires_grad=True)


def test_fourier_decomposition_accepts_grad_requiring_input():
    """Must not raise RuntimeError on live model weights (the step-500 crash)."""
    embeddings = _grad_embeddings()
    result = fourier_decomposition(embeddings, embeddings.shape[0])

    assert isinstance(result["fourier_magnitudes"], np.ndarray)
    assert isinstance(result["dominant_frequencies"], np.ndarray)
    assert isinstance(result["dominant_magnitudes"], np.ndarray)
    assert result["fourier_magnitudes"].shape == (17, 8)
    assert result["dominant_frequencies"].shape == (5, 8)


def test_fourier_decomposition_matches_detached_input():
    """Detaching at the boundary must not change the measured values."""
    torch.manual_seed(0)
    embeddings = _grad_embeddings()
    live = fourier_decomposition(embeddings, embeddings.shape[0])
    reference = fourier_decomposition(embeddings.detach(), embeddings.shape[0])

    np.testing.assert_allclose(
        live["fourier_magnitudes"], reference["fourier_magnitudes"], rtol=1e-5
    )
    np.testing.assert_array_equal(
        live["dominant_frequencies"], reference["dominant_frequencies"]
    )


def test_fourier_output_feeds_sparsity_analysis():
    """End of the crashed chain: magnitudes must flow into k_90/k_99."""
    embeddings = _grad_embeddings()
    result = fourier_decomposition(embeddings, embeddings.shape[0])
    sparsity = analyze_fourier_sparsity(result["fourier_magnitudes"], 17)

    assert 1 <= sparsity["k_99_mean"] <= 17
    assert 1 <= sparsity["k_90_mean"] <= 17
