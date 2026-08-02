"""Smoke tests for the superposition experiment (Rung 3)."""

import torch

from src.experiments.exp3_superposition import SparseFeatureDataset, ToyAutoencoder


class TestToyAutoencoder:
    def test_shape(self) -> None:
        model = ToyAutoencoder(n_dimensions=8, n_features=16)
        x = torch.randn(8, 8)
        recon, latent = model(x)
        assert recon.shape == (8, 8)
        assert latent.shape == (8, 16)

    def test_gradient_flows(self) -> None:
        model = ToyAutoencoder(n_dimensions=8, n_features=16)
        x = torch.randn(4, 8)
        recon, latent = model(x)
        loss = ((recon - x) ** 2).mean() + 0.01 * latent.abs().sum()
        loss.backward()
        assert model.encoder.weight.grad is not None
        assert not torch.isnan(model.encoder.weight.grad).any()

    def test_sparse_output(self) -> None:
        model = ToyAutoencoder(n_dimensions=8, n_features=16)
        x = torch.randn(32, 8)
        _, latent = model(x)
        active = (latent.abs().sum(dim=0) > 1e-6).float().mean()
        assert active > 0.1, "At least some latents should fire"

    def test_reconstruction_loss_decreases(self) -> None:
        model = ToyAutoencoder(n_dimensions=4, n_features=8)
        opt = torch.optim.SGD(model.parameters(), lr=0.1)
        x = torch.randn(16, 4)
        losses = []
        for _ in range(50):
            opt.zero_grad()
            recon, latent = model(x)
            loss = ((recon - x) ** 2).mean() + 0.1 * latent.abs().sum()
            loss.backward()
            opt.step()
            losses.append(loss.item())
        assert losses[-1] < losses[0], "Loss should decrease over training"

    def test_decoder_is_tied_to_encoder_transpose(self) -> None:
        """Decoder weights must be the *same parameter* as the encoder's
        transpose (canonical Elhage et al. setup), not a second
        independently-learned matrix — untied weights give the model extra
        degrees of freedom to reconstruct without the encoder rows ever
        converging to the true generative directions, which breaks the
        premise of compute_feature_recovery()."""
        model = ToyAutoencoder(n_dimensions=5, n_features=20)
        assert not hasattr(model, "decoder"), "No separate decoder parameter should exist"

        x = torch.randn(3, 5)
        recon, latent = model(x)
        expected = latent @ model.encoder.weight  # (B, n_features) @ (n_features, n_dim)
        assert torch.allclose(recon, expected, atol=1e-5)

        # Only one set of weights to train — gradients must flow into the
        # single encoder parameter from both the encode and decode paths.
        loss = recon.pow(2).sum()
        loss.backward()
        assert model.encoder.weight.grad is not None
        n_params = sum(1 for _ in model.parameters())
        assert n_params == 1, "Tied weights means exactly one parameter tensor"


class TestSparseFeatureDataset:
    def test_shapes(self) -> None:
        dataset = SparseFeatureDataset(
            n_features=16, n_dimensions=8, sparsity=0.1, num_samples=100
        )
        x, f = dataset[0]
        assert x.shape == (8,)
        assert f.shape == (16,)

    def test_sparsity_level(self) -> None:
        dataset = SparseFeatureDataset(
            n_features=32, n_dimensions=8, sparsity=0.2, num_samples=500
        )
        total_nonzero = 0
        for i in range(len(dataset)):
            _, f = dataset[i]
            total_nonzero += (f != 0).sum().item()
        active_fraction = total_nonzero / (len(dataset) * 32)
        assert abs(active_fraction - 0.2) < 0.05
