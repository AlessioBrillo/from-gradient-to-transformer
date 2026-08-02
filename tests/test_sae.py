"""Smoke tests for the sparse autoencoder experiment (Rung 5)."""

from pathlib import Path

import torch
from torch.utils.data import DataLoader, TensorDataset

from src.experiments.exp1_induction_heads import AttentionOnlyTransformer
from src.experiments.exp5_sae_dashboard import (
    ActivationGenerator,
    SparseAutoencoder,
    analyze_features,
    evaluate_reconstruction,
    harvest_activations_from_checkpoint,
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


class TestAnalyzeFeatures:
    """Correctness tests for the dead-feature and sparsity accounting the
    2026-08-01 fixed-threshold fix depends on (see exp5's analyze_features
    docstring for the size-dependence bug it replaced)."""

    def test_dead_and_never_fires_counts(self) -> None:
        model = SparseAutoencoder(d_model=4, n_features=4)
        feature_activations = torch.zeros(1000, 4)
        feature_activations[:, 0] = 1.0  # fires 100% -> alive
        feature_activations[:200, 1] = 1.0  # fires 20% -> alive
        # features 2 and 3 stay all-zero -> dead AND never_fires
        dummy_dataset = TensorDataset(torch.zeros(1, 4), torch.zeros(1, 4))

        result = analyze_features(model, dummy_dataset, feature_activations=feature_activations)

        assert result["total_features"] == 4
        assert result["never_fires"] == 2
        assert result["dead_features"] == 2
        assert result["dead_rate"] == 0.5
        assert result["feature_frequency"][0] == 1.0
        assert abs(result["feature_frequency"][1] - 0.2) < 1e-6

    def test_l0_sparsity_matches_known_active_count(self) -> None:
        model = SparseAutoencoder(d_model=4, n_features=6)
        feature_activations = torch.zeros(10, 6)
        feature_activations[:, :3] = 1.0  # exactly 3 active features/sample
        dummy_dataset = TensorDataset(torch.zeros(1, 4), torch.zeros(1, 4))

        result = analyze_features(model, dummy_dataset, feature_activations=feature_activations)
        assert result["l0_sparsity"] == 3.0

    def test_dead_threshold_is_fixed_not_size_scaled(self) -> None:
        """A feature firing at 5e-5 sits ABOVE the old size-scaled threshold
        at n_features=10000 (1/(10*10000) = 1e-5 — the old code called this
        'alive') but BELOW the current fixed 1e-4 threshold (correctly
        'dead' now) — the exact boundary the 2026-08-01 fix moved. Uses a
        1-column tensor rather than a real (n_samples, 10000) activation
        matrix — only `model.n_features` needs to be large, not the tensor
        analyze_features actually receives here."""
        model = SparseAutoencoder(d_model=4, n_features=10000)
        n_samples = 20000
        feature_activations = torch.zeros(n_samples, 1)
        feature_activations[0, 0] = 1.0  # freq = 1/20000 = 5e-5
        dummy_dataset = TensorDataset(torch.zeros(1, 4), torch.zeros(1, 4))

        result = analyze_features(model, dummy_dataset, feature_activations=feature_activations)
        old_scaled_threshold = 1.0 / (10 * model.n_features)  # = 1e-5

        assert result["dead_threshold"] == 1e-4
        assert result["feature_frequency"][0] > old_scaled_threshold  # old code: alive
        assert result["feature_frequency"][0] < result["dead_threshold"]  # new code: dead


class TestEvaluateReconstruction:
    """Correctness tests for the MSE/FVE metrics Rung 5's headline 97.2%
    FVE number is computed from."""

    class _IdentityModel(torch.nn.Module):
        d_model = 4

        def forward(self, x: torch.Tensor) -> tuple:
            return x, x

    class _MeanPredictorModel(torch.nn.Module):
        d_model = 4

        def __init__(self, mean: torch.Tensor) -> None:
            super().__init__()
            self.mean = mean

        def forward(self, x: torch.Tensor) -> tuple:
            return self.mean.expand_as(x), x

    def test_perfect_reconstruction_gives_fve_one_mse_zero(self) -> None:
        loader = DataLoader(
            TensorDataset(torch.randn(32, 4), torch.zeros(32, 4)), batch_size=8
        )
        result = evaluate_reconstruction(self._IdentityModel(), loader)
        assert abs(result["mse"]) < 1e-10
        assert abs(result["fve"] - 1.0) < 1e-6

    def test_predicting_the_mean_gives_fve_zero(self) -> None:
        x = torch.randn(64, 4)
        loader = DataLoader(TensorDataset(x, torch.zeros(64, 4)), batch_size=64)
        model = self._MeanPredictorModel(mean=x.mean(dim=0))
        result = evaluate_reconstruction(model, loader)
        assert abs(result["fve"]) < 1e-4


class TestHarvestActivationsFromCheckpoint:
    """End-to-end test for --activations-from: train a tiny real
    induction-heads checkpoint, save it, then harvest activations from it
    exactly as the CLI path does."""

    def test_harvests_real_shaped_activations(self, tmp_path: Path) -> None:
        vocab_size, seq_len, d_model, n_layers, n_heads = 8, 8, 8, 1, 2
        model = AttentionOnlyTransformer(
            vocab_size=vocab_size,
            d_model=d_model,
            n_layers=n_layers,
            n_heads=n_heads,
            max_seq_len=seq_len,
        )
        checkpoint_path = tmp_path / "tiny_checkpoint.pt"
        torch.save(model.state_dict(), checkpoint_path)

        activations = harvest_activations_from_checkpoint(
            checkpoint_path=checkpoint_path,
            vocab_size=vocab_size,
            seq_len=seq_len,
            d_model=d_model,
            n_layers=n_layers,
            n_heads=n_heads,
            num_samples=50,
            seed=0,
        )

        assert activations.shape == (50, d_model)
        assert not torch.isnan(activations).any()

    def test_wrong_architecture_raises(self, tmp_path: Path) -> None:
        model = AttentionOnlyTransformer(
            vocab_size=8, d_model=8, n_layers=1, n_heads=2, max_seq_len=8
        )
        checkpoint_path = tmp_path / "tiny_checkpoint.pt"
        torch.save(model.state_dict(), checkpoint_path)

        import pytest

        with pytest.raises(RuntimeError):
            harvest_activations_from_checkpoint(
                checkpoint_path=checkpoint_path,
                vocab_size=8,
                seq_len=8,
                d_model=16,  # mismatched -- state dict won't load
                n_layers=1,
                n_heads=2,
                num_samples=10,
                seed=0,
            )
