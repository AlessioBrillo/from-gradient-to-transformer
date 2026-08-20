"""Smoke tests for the grokking experiment (Rung 2, flagship)."""

import numpy as np
import torch

from src.experiments.exp2_grokking import (
    OneLayerTransformer,
    analyze_fourier_sparsity,
    compute_progress_measures,
    fourier_decompose_embeddings,
    fourier_sparsity_progress,
    make_modular_addition_data,
    weight_norm_progress,
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


class TestProgressMeasures:
    """Fourier-sparsity and weight-norm progress measures (Micro-Phase 10):
    the instrument that must exist before the GPU run, so the run is
    analysis-ready the moment it finishes."""

    def test_sparse_fourier_embedding_scores_higher_than_dense(self) -> None:
        """A single-frequency embedding must read as maximally sparse
        (-> 1.0), a uniform/random one as near-zero."""
        modulus = 59
        n = torch.arange(modulus).float()
        sparse = torch.cos(2 * torch.pi * 7 * n / modulus).unsqueeze(1).repeat(1, 8)
        dense = torch.randn(modulus, 8)

        sparse_score = fourier_sparsity_progress(sparse, modulus)
        dense_score = fourier_sparsity_progress(dense, modulus)
        # A real cosine has a two-sided spectrum (k and P-k), so the
        # maximally-sparse real signal uses 2 of P frequencies, not 1:
        # 1 - log(2)/log(59) ≈ 0.83. That is still unambiguously sparse.
        assert sparse_score > 0.7, f"Expected ~0.83 for a pure cosine, got {sparse_score:.3f}"
        assert dense_score < 0.2, f"Expected ~0 for a dense spectrum, got {dense_score:.3f}"
        assert sparse_score > dense_score

    def test_weight_norm_progress_is_positive_and_finite(self) -> None:
        model = OneLayerTransformer(d_model=32, d_mlp=64, n_heads=2, modulus=29)
        norm = weight_norm_progress(model)
        assert norm > 0.0
        assert norm == norm  # not NaN

    def test_progress_measures_tracked_during_training(self) -> None:
        """train_model must populate the fourier_sparsity/weight_norm history
        keys (carried forward between samples) so the progress-measure plot
        has data without a separate analysis pass."""
        from torch.utils.data import DataLoader

        from src.experiments.exp2_grokking import train_model

        model = OneLayerTransformer(d_model=32, d_mlp=64, n_heads=2, modulus=11)
        train_x = torch.randint(0, 11, (64, 2))
        train_y = (train_x[:, 0] + train_x[:, 1]) % 11
        loader = DataLoader(list(zip(train_x, train_y)), batch_size=32, shuffle=True)
        history = train_model(
            model=model,
            train_loader=loader,
            val_loader=loader,
            epochs=5,
            lr=1e-3,
            weight_decay=0.1,
            seed=0,
            progress_interval=2,
        )
        assert len(history["fourier_sparsity"]) == 5
        assert len(history["weight_norm"]) == 5
        assert all(0.0 <= s <= 1.0 for s in history["fourier_sparsity"])
        assert history["weight_norm"][-1] > 0.0


class TestGrokkingCheckpointResume:
    """Falsification tests for Micro-Phase 28's checkpoint/resume port into
    exp2 (the P=113 flagship). Mirrors TestCheckpointResume from
    test_induction_heads.py: a resumed run must be *indistinguishable* from
    one that never stopped (same model, same history, same RNG-drawn batch
    order). The port exists because ADR-0003 row 1's
    "checkpoint-every-500 + resume" promise was not mechanically real in
    exp2: a ~5.5 h P=113 run cannot be launched without a resume path."""

    ARGS_DEFAULTS = dict(
        modulus=11,
        d_model=32,
        d_mlp=64,
        n_heads=2,
        batch_size=32,
    )

    @staticmethod
    def _args(**overrides):
        from types import SimpleNamespace

        defaults = dict(TestGrokkingCheckpointResume.ARGS_DEFAULTS)
        defaults.update(overrides)
        return SimpleNamespace(**defaults)

    @staticmethod
    def _model(args):
        return OneLayerTransformer(
            d_model=args.d_model,
            d_mlp=args.d_mlp,
            n_heads=args.n_heads,
            modulus=args.modulus,
        )

    @staticmethod
    def _initial_state(args):
        """Snapshot the initial weights of a freshly constructed model. Both
        sides of a resume comparison must start from *identical* weights —
        constructing two models independently gives them different random
        inits, which would make even an uninterrupted comparison diverge."""
        import copy

        return copy.deepcopy(TestGrokkingCheckpointResume._model(args).state_dict())

    @staticmethod
    def _model_from(state):
        args = TestGrokkingCheckpointResume._args()
        model = TestGrokkingCheckpointResume._model(args)
        model.load_state_dict(state)
        return model

    @staticmethod
    def _loaders(args):
        from torch.utils.data import DataLoader

        train, val = make_modular_addition_data(
            modulus=args.modulus, train_fraction=0.5, seed=0
        )
        return (
            DataLoader(train, batch_size=args.batch_size, shuffle=True),
            DataLoader(val, batch_size=args.batch_size, shuffle=False),
        )

    @staticmethod
    def _train(**kwargs):
        from src.experiments.exp2_grokking import train_model

        return train_model(**kwargs)

    def test_resume_matches_uninterrupted(self, tmp_path) -> None:
        """Interrupt at epoch 3, resume to end: every history curve must
        equal the uninterrupted run's exactly (the RNG snapshot guarantees
        the resumed run draws the identical shuffled batches)."""
        import numpy as np

        from src.experiments.exp2_grokking import checkpoint_path_for_seed

        args = self._args()
        tl, vl = self._loaders(args)
        state = self._initial_state(args)

        full_hist = self._train(
            model=self._model_from(state), train_loader=tl, val_loader=vl,
            epochs=8, lr=1e-3, weight_decay=0.1, seed=0,
        )

        broken_model = self._model_from(state)
        self._train(
            model=broken_model, train_loader=tl, val_loader=vl,
            epochs=3, lr=1e-3, weight_decay=0.1, seed=0,
            checkpoint_dir=str(tmp_path), checkpoint_every=1,
            schedule_epochs=8,  # partial run: anneal LR over the full 8-epoch horizon
        )
        resumed_hist = self._train(
            model=broken_model, train_loader=tl, val_loader=vl,
            epochs=8, lr=1e-3, weight_decay=0.1, seed=0,
            resume_from=str(checkpoint_path_for_seed(str(tmp_path), "exp2", 0)),
        )

        assert len(resumed_hist["train_loss"]) == 8
        for key in full_hist:
            np.testing.assert_allclose(
                resumed_hist[key], full_hist[key], err_msg=f"history[{key}] diverged"
            )

    def test_resume_twice_matches_uninterrupted(self, tmp_path) -> None:
        """Two consecutive interruptions (checkpoints at epochs 1 and 3) must
        still converge to exactly the uninterrupted run."""
        import numpy as np

        from src.experiments.exp2_grokking import checkpoint_path_for_seed

        args = self._args()
        tl, vl = self._loaders(args)
        state = self._initial_state(args)

        full_hist = self._train(
            model=self._model_from(state), train_loader=tl, val_loader=vl,
            epochs=8, lr=1e-3, weight_decay=0.1, seed=0,
        )

        broken = self._model_from(state)
        self._train(
            model=broken, train_loader=tl, val_loader=vl,
            epochs=4, lr=1e-3, weight_decay=0.1, seed=0,
            checkpoint_dir=str(tmp_path), checkpoint_every=2,
            schedule_epochs=8,
        )
        resumed_hist = self._train(
            model=broken, train_loader=tl, val_loader=vl,
            epochs=8, lr=1e-3, weight_decay=0.1, seed=0,
            resume_from=str(checkpoint_path_for_seed(str(tmp_path), "exp2", 0)),
        )
        for key in full_hist:
            np.testing.assert_allclose(
                resumed_hist[key], full_hist[key], err_msg=f"history[{key}] diverged"
            )

    def test_resume_missing_checkpoint_starts_fresh(self, tmp_path) -> None:
        """An explicit resume path that does not exist must not crash or part
        train — it falls back to a fresh full run, with the full history."""
        args = self._args()
        tl, vl = self._loaders(args)
        hist = self._train(
            model=self._model_from(self._initial_state(args)),
            train_loader=tl, val_loader=vl,
            epochs=2, lr=1e-3, weight_decay=0.1, seed=0,
            resume_from=str(tmp_path / "does_not_exist.pt"),
        )
        assert len(hist["val_acc"]) == 2


class TestLRSchedule:
    """Microscope trial-2 enabler (ADR-0003 row 2): a constant-LR schedule
    option so the cosine-annealing interaction can be tested as a one-change
    trial against the frozen P=113 protocol. RED before the factory existed
    (ImportError), GREEN after — the MP-28 falsification pattern."""

    def test_constant_schedule_keeps_lr_flat(self) -> None:
        """schedule="constant" must hold the LR at its base value across the
        whole horizon — the falsification for "the cosine schedule locks in
        the dense solution before the sparse one is reachable"."""
        import torch

        from src.experiments.exp2_grokking import make_lr_scheduler

        opt = torch.optim.AdamW([torch.nn.Parameter(torch.zeros(4))], lr=1e-3)
        sched = make_lr_scheduler(opt, schedule="constant", epochs=100, schedule_epochs=None)
        assert abs(sched.get_last_lr()[0] - 1e-3) < 1e-9
        for _ in range(100):
            opt.step()
            sched.step()
        assert abs(sched.get_last_lr()[0] - 1e-3) < 1e-9

    def test_cosine_schedule_still_decays(self) -> None:
        """The default cosine schedule must keep annealing toward zero — the
        constant option must not silently change the frozen protocol."""
        import torch

        from src.experiments.exp2_grokking import make_lr_scheduler

        opt = torch.optim.AdamW([torch.nn.Parameter(torch.zeros(4))], lr=1e-3)
        sched = make_lr_scheduler(opt, schedule="cosine", epochs=100, schedule_epochs=None)
        first = sched.get_last_lr()[0]
        for _ in range(50):
            opt.step()
            sched.step()
        assert sched.get_last_lr()[0] < first
