"""Smoke tests for the grokking experiment (Rung 2, flagship)."""

import torch

from src.experiments.exp2_grokking import (
    OneLayerTransformer,
    fourier_decompose_embeddings,
    make_modular_addition_data,
)


class TestOneLayerTransformer:
    """Test the 1-layer transformer used for grokking."""

    def test_shape(self) -> None:
        """Output shape should be (batch, modulus) for (batch, 2) input."""
        model = OneLayerTransformer(
            d_model=32, d_mlp=64, n_heads=2, modulus=29
        )
        x = torch.randint(0, 29, (4, 2))
        logits, _ = model(x, return_activations=False)
        assert logits.shape == (4, 29), f"Expected (4, 29), got {logits.shape}"

    def test_gradient_flows(self) -> None:
        """Loss should backpropagate through the full model."""
        model = OneLayerTransformer(
            d_model=32, d_mlp=64, n_heads=2, modulus=29
        )
        x = torch.randint(0, 29, (8, 2))
        y = (x[:, 0] + x[:, 1]) % 29
        logits, _ = model(x)
        loss = torch.nn.functional.cross_entropy(logits, y)
        loss.backward()
        assert model.embed.weight.grad is not None
        assert not torch.isnan(model.embed.weight.grad).any()

    def test_fourier_decomposition(self) -> None:
        """Fourier decomposition should return correct shape frequencies."""
        embed = torch.randn(29, 32)
        result = fourier_decompose_embeddings(embed, 29)
        assert result["frequencies"].shape == (29,)
        assert result["top_frequencies"].shape == (29,)


class TestGrokkingData:
    """Test the modular addition dataset."""

    def test_shapes(self) -> None:
        """Train and val datasets should have correct shapes."""
        train, val = make_modular_addition_data(
            modulus=29, train_fraction=0.3, seed=42
        )
        train_x, train_y = train[0]
        val_x, val_y = val[0]
        assert train_x.shape == (2,)
        assert train_y.shape == ()
        assert train_y.item() == (train_x[0].item() + train_x[1].item()) % 29

    def test_pairs_disjoint(self) -> None:
        """Train and val should hold out disjoint (a, b) equations."""
        train, val = make_modular_addition_data(
            modulus=29, train_fraction=0.3, seed=42
        )
        train_pairs = {(int(a), int(b)) for a, b in (train[i][0] for i in range(len(train)))}
        val_pairs = {(int(a), int(b)) for a, b in (val[i][0] for i in range(len(val)))}
        assert train_pairs.isdisjoint(val_pairs), "Train/val equations should be disjoint"

    def test_target_classes_shared_across_splits(self) -> None:
        """Every target class should be reachable from training data.

        Splitting by target value (instead of by equation) is a bug: it
        leaves some output classes with zero training signal, making
        generalization to them impossible by construction. Both splits must
        draw from the full target vocabulary.
        """
        train, val = make_modular_addition_data(
            modulus=29, train_fraction=0.3, seed=42
        )
        train_targets = {int(train[i][1]) for i in range(len(train))}
        val_targets = {int(val[i][1]) for i in range(len(val))}
        assert train_targets & val_targets, "Train/val should share target classes"
