"""A run seed pins the model's initial weights, on every code path.

The 2026-11-12 audit (Honesty Ledger) found that exp1, exp3 and exp4 built
the model *before* the per-seed `set_seed` call: a seed pinned the data and
the batch order, but the initial weights came from wherever the ambient torch
stream happened to be. Two commands of one nominal configuration (the exp3
single-sparsity path and the sweep path) therefore published different
numbers.

These tests use the audit's own instrument, a digest of the initial weights,
and they fail on the pre-fix code.
"""

from __future__ import annotations

import argparse
import hashlib

import pytest
import torch

from src.experiments import exp1_induction_heads as exp1
from src.experiments import exp3_superposition as exp3
from src.experiments import exp4_circuit_patching as exp4


def _digest(model: torch.nn.Module) -> str:
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()


def _disturb_ambient_stream() -> None:
    """Stand in for whatever ran before: another seed's training, a
    throwaway probe model, a different number of sweep levels."""
    torch.manual_seed(12345)
    torch.randn(1000)


_TRANSFORMER_ARGS = argparse.Namespace(
    vocab_size=32, d_model=16, n_layers=2, n_heads=2, seq_len=16, from_checkpoint=None
)


class TestExp3:
    def test_a_seed_alone_and_in_sequence_start_from_the_same_weights(self) -> None:
        alone = _digest(exp3.build_autoencoder(20, 5, seed=1))
        exp3.build_autoencoder(20, 5, seed=0)
        _disturb_ambient_stream()
        assert _digest(exp3.build_autoencoder(20, 5, seed=1)) == alone

    def test_different_seeds_start_from_different_weights(self) -> None:
        assert _digest(exp3.build_autoencoder(20, 5, seed=0)) != _digest(
            exp3.build_autoencoder(20, 5, seed=1)
        )

    def test_the_sweep_and_the_single_sparsity_path_agree(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The contradiction the audit found: same seed, same configuration,
        two code paths, two different starting points."""
        seen: list[str] = []

        def record_instead_of_training(model: torch.nn.Module, **_kwargs: object) -> dict:
            seen.append(_digest(model))
            _disturb_ambient_stream()  # a real training consumes the stream
            return {"loss": []}

        monkeypatch.setattr(exp3, "train_autoencoder", record_instead_of_training)
        args = argparse.Namespace(
            n_features=20,
            n_dimensions=5,
            num_samples=64,
            importance_decay=1.0,
            batch_size=32,
            epochs=1,
            lr=0.01,
            threshold=0.5,
            single_sparsity=0.01,
        )
        exp3.run_single_seed(0, args)
        single = seen.pop()
        exp3.run_sweep_seed(0, args)
        assert len(seen) == len(exp3.SWEEP_SPARSITIES)
        assert set(seen) == {single}


class TestExp1:
    def test_a_seed_alone_and_in_sequence_start_from_the_same_weights(self) -> None:
        alone = _digest(exp1.build_seeded_model(_TRANSFORMER_ARGS, seed=1))
        exp1.build_seeded_model(_TRANSFORMER_ARGS, seed=0)
        # The multi-seed run builds a throwaway model between seeds to count
        # parameters; that used to shift the next seed's starting point.
        exp1._probe_parameter_count(_TRANSFORMER_ARGS)
        assert _digest(exp1.build_seeded_model(_TRANSFORMER_ARGS, seed=1)) == alone

    def test_different_seeds_start_from_different_weights(self) -> None:
        assert _digest(exp1.build_seeded_model(_TRANSFORMER_ARGS, seed=0)) != _digest(
            exp1.build_seeded_model(_TRANSFORMER_ARGS, seed=1)
        )


class TestExp4:
    def test_a_seed_alone_and_in_sequence_start_from_the_same_weights(self) -> None:
        alone, _ = exp4._build_model(_TRANSFORMER_ARGS, seed=1)
        expected = _digest(alone)
        exp4._build_model(_TRANSFORMER_ARGS, seed=0)
        _disturb_ambient_stream()
        again, _ = exp4._build_model(_TRANSFORMER_ARGS, seed=1)
        assert _digest(again) == expected
