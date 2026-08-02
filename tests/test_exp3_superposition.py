"""Tests for the superposition experiment (Rung 3).

Includes falsification tests for the 2026-08-02 architecture rewrite (Micro-
Phase 8, the Evidence Pass): each targets one of the two structural bugs that
made the pre-rewrite version report flat, near-zero "recovery" at every
sparsity level (see 05_llm_engineering/proofs/superposition-setup-validity.md).
Bug A was that the model had no real bottleneck (the dataset pre-compressed
features before the model ever saw them); Bug B was that the recovery metric
compared against an invented ground-truth direction matrix with no
counterpart in Elhage et al.'s actual setup. These tests would fail against
the pre-rewrite `ToyAutoencoder`/`SparseFeatureDataset`, which had no
`n_dimensions < n_features` guard, no `decoder_bias`, and mapped
n_dimensions -> n_features (an expansion, not a compression).
"""

import numpy as np
import pytest
import torch
from torch.utils.data import DataLoader

from src.experiments.exp3_superposition import (
    SparseFeatureDataset,
    ToyAutoencoder,
    compute_feature_geometry,
    train_autoencoder,
)


class TestToyAutoencoder:
    def test_shape(self) -> None:
        model = ToyAutoencoder(n_features=16, n_dimensions=8)
        x = torch.randn(8, 16)
        recon, h = model(x)
        assert recon.shape == (8, 16)
        assert h.shape == (8, 8)

    def test_gradient_flows(self) -> None:
        model = ToyAutoencoder(n_features=16, n_dimensions=8)
        x = torch.randn(4, 16)
        recon, _h = model(x)
        loss = ((recon - x) ** 2).mean()
        loss.backward()
        assert model.encoder.weight.grad is not None
        assert not torch.isnan(model.encoder.weight.grad).any()
        assert model.decoder_bias.grad is not None
        assert not torch.isnan(model.decoder_bias.grad).any()

    def test_reconstruction_loss_decreases(self) -> None:
        model = ToyAutoencoder(n_features=8, n_dimensions=4)
        opt = torch.optim.SGD(model.parameters(), lr=0.1)
        x = torch.rand(16, 8)  # nonnegative, matches ReLU output range
        losses = []
        for _ in range(50):
            opt.zero_grad()
            recon, _h = model(x)
            loss = ((recon - x) ** 2).mean()
            loss.backward()
            opt.step()
            losses.append(loss.item())
        assert losses[-1] < losses[0], "Loss should decrease over training"

    def test_decoder_reuses_encoder_weight_transpose(self) -> None:
        """The decoder must reuse the encoder's weight transposed — a single
        tied parameter plus a separate bias, not an independently-learned
        decoder matrix."""
        model = ToyAutoencoder(n_features=20, n_dimensions=5)
        param_names = {name for name, _ in model.named_parameters()}
        assert param_names == {"encoder.weight", "decoder_bias"}

        x = torch.randn(3, 20)
        recon, h = model(x)
        expected = torch.relu(h @ model.encoder.weight + model.decoder_bias)
        assert torch.allclose(recon, expected, atol=1e-5)

    def test_bottleneck_is_enforced_at_construction(self) -> None:
        """n_dimensions must be strictly less than n_features — without a
        real bottleneck there is nothing for superposition to trade off
        against. The pre-rewrite code had no such guard and silently built
        an expansion (5 -> 20) instead of a compression."""
        with pytest.raises(ValueError, match="bottleneck"):
            ToyAutoencoder(n_features=10, n_dimensions=10)
        with pytest.raises(ValueError, match="bottleneck"):
            ToyAutoencoder(n_features=5, n_dimensions=10)


class TestSparseFeatureDataset:
    def test_shapes(self) -> None:
        dataset = SparseFeatureDataset(n_features=16, sparsity=0.1, num_samples=100)
        x, target = dataset[0]
        assert x.shape == (16,)
        assert target.shape == (16,)
        assert torch.equal(x, target), "Autoencoder target must equal input"

    def test_sparsity_level(self) -> None:
        dataset = SparseFeatureDataset(n_features=32, sparsity=0.2, num_samples=500)
        total_nonzero = sum((dataset[i][0] != 0).sum().item() for i in range(len(dataset)))
        active_fraction = total_nonzero / (len(dataset) * 32)
        assert abs(active_fraction - 0.2) < 0.05

    def test_importance_decay(self) -> None:
        dataset = SparseFeatureDataset(
            n_features=5, sparsity=0.1, num_samples=10, importance_decay=0.9
        )
        expected = torch.tensor([0.9**i for i in range(5)], dtype=torch.float32)
        assert torch.allclose(dataset.importance, expected, atol=1e-6)

    def test_uniform_importance_by_default(self) -> None:
        dataset = SparseFeatureDataset(n_features=5, sparsity=0.1, num_samples=10)
        assert torch.allclose(dataset.importance, torch.ones(5))


class TestFeatureGeometryFalsification:
    """Falsification tests for the two root-caused bugs (see module
    docstring): no bottleneck (Bug A) and an unfalsifiable metric (Bug B)."""

    def test_model_is_a_bottleneck(self) -> None:
        """On fully dense data (every feature always active), a real
        compression cannot drive reconstruction loss to ~0 — some
        interference is structurally unavoidable when n_dimensions <
        n_features. The pre-rewrite architecture, which was secretly an
        expansion, reached exactly 0.000000 MSE at every sparsity level
        tested (see the superposition-setup-validity proof)."""
        n_features, n_dimensions = 8, 3
        dataset = SparseFeatureDataset(
            n_features=n_features, sparsity=1.0, num_samples=2000, seed=0
        )
        loader = DataLoader(dataset, batch_size=256, shuffle=True)
        model = ToyAutoencoder(n_features=n_features, n_dimensions=n_dimensions)
        history = train_autoencoder(
            model, loader, dataset.importance, epochs=200, lr=1e-2, seed=0
        )
        assert history["loss"][-1] > 1e-3, (
            "A real bottleneck should leave a nonzero loss floor on dense "
            f"data; got {history['loss'][-1]:.2e}, indistinguishable from "
            "the no-bottleneck bug's exact-zero reconstruction."
        )

    def test_dense_regime_drops_features(self) -> None:
        """At high sparsity (features frequently co-active), interference
        pressure should force the model to not represent every feature."""
        n_features, n_dimensions = 8, 2
        dataset = SparseFeatureDataset(
            n_features=n_features, sparsity=0.5, num_samples=2000, seed=0
        )
        loader = DataLoader(dataset, batch_size=256, shuffle=True)
        model = ToyAutoencoder(n_features=n_features, n_dimensions=n_dimensions)
        train_autoencoder(model, loader, dataset.importance, epochs=300, lr=1e-2, seed=0)
        geometry = compute_feature_geometry(model, threshold=0.5)
        assert geometry["n_represented"] < n_features, (
            f"Expected fewer than {n_features} features represented in the "
            f"dense regime, got {geometry['n_represented']}"
        )

    def test_sparse_regime_represents_all_features(self) -> None:
        """At low sparsity (features rarely co-active), interference
        pressure is low and the model should find room for every feature —
        this is the other end of the phase transition Bug B made
        invisible."""
        n_features, n_dimensions = 8, 3
        dataset = SparseFeatureDataset(
            n_features=n_features, sparsity=0.01, num_samples=8000, seed=0
        )
        loader = DataLoader(dataset, batch_size=256, shuffle=True)
        model = ToyAutoencoder(n_features=n_features, n_dimensions=n_dimensions)
        train_autoencoder(model, loader, dataset.importance, epochs=500, lr=1e-2, seed=0)
        geometry = compute_feature_geometry(model, threshold=0.5)
        assert geometry["n_represented"] == n_features, (
            f"Expected all {n_features} features represented in the sparse "
            f"regime, got {geometry['n_represented']}"
        )

    def test_dimensionality_is_one_when_monosemantic(self) -> None:
        """Orthogonal, unit-norm encoder directions (one dimension fully
        dedicated per feature) must score dimensionality ≈ 1.0 — the
        monosemantic end of Elhage et al.'s D_i metric, which the old
        ground-truth-comparison metric never computed at all."""
        model = ToyAutoencoder(n_features=10, n_dimensions=5)
        with torch.no_grad():
            W = torch.zeros(5, 10)
            W[:, :5] = torch.eye(5)
            model.encoder.weight.copy_(W)

        geometry = compute_feature_geometry(model, threshold=0.5)
        assert geometry["n_represented"] == 5
        monosemantic_dims = geometry["dimensionality"][:5]
        assert np.allclose(monosemantic_dims, 1.0, atol=1e-3)
