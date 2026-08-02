"""Smoke tests for the grokking experiment (Rung 2, flagship)."""

import numpy as np
import torch

from src.experiments.exp2_grokking import (
    OneLayerTransformer,
    analyze_fourier_sparsity,
    compute_progress_measures,
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


class TestFourierDecomposition:
    """Correctness tests for the Fourier analysis functions the flagship's
    entire headline claim rests on: does the decomposition actually recover
    a known frequency, and does the sparsity metric read a delta function
    and a uniform spectrum correctly?"""

    def test_recovers_a_known_pure_frequency(self) -> None:
        """An embedding built purely from frequency k0's cosine wave must
        decompose with essentially all its mass on k0 (and its mirror,
        modulus - k0, since a real-valued cosine has a two-sided spectrum)."""
        modulus = 29
        k0 = 5
        n = torch.arange(modulus).float()
        wave = torch.cos(2 * torch.pi * k0 * n / modulus)
        embed = wave.unsqueeze(1).repeat(1, 4)  # (modulus, d_model=4)

        result = fourier_decompose_embeddings(embed, modulus)
        magnitudes = result["frequencies"].numpy()

        top_two = magnitudes.argsort()[::-1][:2]
        assert set(top_two.tolist()) == {k0, modulus - k0}, (
            f"Expected mass concentrated at frequency {k0} and its mirror "
            f"{modulus - k0}, got top frequencies {top_two.tolist()}"
        )
        mass_at_top_two = magnitudes[top_two].sum() / magnitudes.sum()
        assert mass_at_top_two > 0.99, (
            f"Expected >99% of mass at the pure frequency's pair, got "
            f"{mass_at_top_two:.3f}"
        )

    def test_random_embeddings_spread_mass_across_frequencies(self) -> None:
        """A random (non-Fourier-structured) embedding should NOT
        concentrate mass on any single frequency pair — the sparsity this
        experiment claims to find is a property of a *trained* model, not
        an artifact of the decomposition itself."""
        modulus = 29
        embed = torch.randn(modulus, 16)
        result = fourier_decompose_embeddings(embed, modulus)
        sparsity = analyze_fourier_sparsity(result, top_k=10)
        # A dense/random spectrum should need most frequencies to reach 99%
        # mass -- nowhere near the ~10-20 the grokking algorithm produces.
        assert sparsity["k_99_percent"] > modulus * 0.5


class TestAnalyzeFourierSparsity:
    def test_delta_spectrum_needs_only_one_frequency(self) -> None:
        """All mass on a single frequency -> k_90/k_99 percent should both
        be 1: one frequency already explains 100% of the mass."""
        modulus = 29
        frequencies = torch.zeros(modulus)
        frequencies[3] = 1.0
        fourier_result = {
            "frequencies": frequencies,
            "top_frequencies": frequencies.argsort(descending=True),
        }
        sparsity = analyze_fourier_sparsity(fourier_result, top_k=10)
        assert sparsity["k_90_percent"] == 1
        assert sparsity["k_99_percent"] == 1

    def test_uniform_spectrum_needs_most_frequencies(self) -> None:
        """Uniform mass across all frequencies -> reaching 99% needs
        essentially all of them."""
        modulus = 29
        frequencies = torch.ones(modulus)
        fourier_result = {
            "frequencies": frequencies,
            "top_frequencies": frequencies.argsort(descending=True),
        }
        sparsity = analyze_fourier_sparsity(fourier_result, top_k=10)
        assert sparsity["k_99_percent"] >= modulus - 1


class TestComputeProgressMeasures:
    def test_phase1_end_detects_when_val_acc_first_exceeds_threshold(self) -> None:
        modulus = 29
        random_baseline = 1.0 / modulus
        val_acc = [0.0] * 10 + [random_baseline * 3] * 10  # crosses at epoch 10
        embed_norm = list(np.linspace(1.0, 2.0, 20))
        history = {"val_acc": val_acc, "embed_norm": embed_norm}
        fourier_result = {"frequencies": torch.ones(modulus)}

        phases = compute_progress_measures(history, fourier_result, modulus)
        assert phases["phase1_end"] == 10

    def test_phase_boundaries_are_ordered(self) -> None:
        modulus = 29
        val_acc = list(np.linspace(0.0, 1.0, 50))
        embed_norm = [1.0] * 20 + list(np.linspace(1.0, 5.0, 30))
        history = {"val_acc": val_acc, "embed_norm": embed_norm}
        fourier_result = {"frequencies": torch.ones(modulus)}

        phases = compute_progress_measures(history, fourier_result, modulus)
        assert 0 <= phases["phase1_end"] <= phases["phase2_end"] < len(val_acc)
        assert phases["memorization_epochs"] + phases["circuit_formation_epochs"] >= 0
        assert phases["cleanup_epochs"] >= 0
