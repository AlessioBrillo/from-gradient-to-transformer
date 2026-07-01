"""Smoke tests for the sparse autoencoder experiment (Rung 5)."""

import torch

from src.experiments.exp5_sae_dashboard import (
    ActivationGenerator,
    SparseAutoencoder,
)


class TestSparseAutoencoder:
    """Test the SAE implementation."""

    def test_shape(self) -> None:
        """SAE should reconstruct input shape."""
        sae = SparseAutoencoder(d_model=32, n_features=128)
        x = torch.randn(8, 32)
        recon, latent = sae(x)
        assert recon.shape == (8, 32), f"Expected (8, 32), got {recon.shape}"
        assert latent.shape == (8, 128), f"Expected (8, 128), got {latent.shape}"

    def test_sparsity(self) -> None:
        """Latent should be sparse (many zeros from ReLU)."""
        sae = SparseAutoencoder(d_model=32, n_features=128)
        x = torch.randn(32, 32)
        _, latent = sae(x)
        sparsity = (latent == 0).float().mean().item()
        assert sparsity > 0.3, f"Expected >30% zeros, got {sparsity:.1%}"

    def test_gradient_flows(self) -> None:
        """Loss should backpropagate through SAE."""
        sae = SparseAutoencoder(d_model=32, n_features=128)
        x = torch.randn(8, 32)
        recon, latent = sae(x)
        l2 = ((recon - x) ** 2).mean()
        l1 = latent.abs().sum(dim=-1).mean()
        loss = l2 + 1e-3 * l1
        loss.backward()
        assert sae.encoder.weight.grad is not None
        assert not torch.isnan(sae.encoder.weight.grad).any()

    def test_decoder_normalization(self) -> None:
        """Decoder columns should be unit norm after _normalize_decoder."""
        sae = SparseAutoencoder(d_model=32, n_features=128)
        norms = sae.decoder.weight.norm(dim=0)
        assert torch.allclose(norms, torch.ones_like(norms), atol=1e-5)


class TestActivationGenerator:
    """Test the synthetic activation generator."""

    def test_shapes(self) -> None:
        """Generator should produce (n_samples, d_model) activations."""
        gen = ActivationGenerator(d_model=32, n_true_features=10, seed=42)
        activations, features = gen.generate(100)
        assert activations.shape == (100, 32)
        assert features.shape == (100, 10)
