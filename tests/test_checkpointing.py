"""Tests for the rolling resume checkpoint metadata (checkpointing.py).

Why this file exists
--------------------
The content-task cascade loads exp1's checkpoint in exp4, possibly in a
later session on a different commit. Until 2026-10-31 the checkpoint carried
only the weights, the optimizer state and the epoch: nothing said *which
model seed* the weights were, *which task* they had learned, or *which
commit* had written them. exp4 therefore could not tell a cascade about
exp1's final model from a cascade about a stale checkpoint of another seed.

These tests freeze the metadata contract. They do not test the RNG-state
continuity — `tests/test_induction_heads.py` already falsifies that with a
bit-for-bit resume.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import torch

from src.experiments.checkpointing import (
    architecture_metadata,
    load_training_checkpoint,
    save_training_checkpoint,
)
from src.models.decoder_only_transformer import DecoderOnlyTransformer


def _model() -> DecoderOnlyTransformer:
    return DecoderOnlyTransformer(vocab_size=16, d_model=8, n_layers=1, n_heads=2, max_seq_len=8)


def _save(tmp_path: Path, **kwargs) -> Path:
    model = _model()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lambda _e: 1.0)
    path = tmp_path / "checkpoint.pt"
    save_training_checkpoint(
        path=path,
        epoch=7,
        model=model,
        optimizer=optimizer,
        scheduler=scheduler,
        history={"val_acc": [0.1]},
        rng_state=torch.random.get_rng_state(),
        **kwargs,
    )
    return path


class TestTheMetadata:
    def test_it_records_the_commit_that_wrote_it(self, tmp_path: Path) -> None:
        state = load_training_checkpoint(_save(tmp_path))
        assert state is not None
        assert isinstance(state["git_sha"], str) and state["git_sha"]
        assert isinstance(state["git_dirty"], bool)

    def test_it_records_the_seed_and_task_when_given(self, tmp_path: Path) -> None:
        path = _save(tmp_path, seed=3, task="variable")
        state = load_training_checkpoint(path)
        assert state is not None
        assert state["seed"] == 3
        assert state["task"] == "variable"

    def test_seed_and_task_are_optional(self, tmp_path: Path) -> None:
        """exp2 writes the same format and has neither concept."""
        state = load_training_checkpoint(_save(tmp_path))
        assert state is not None
        assert "seed" not in state
        assert "task" not in state

    def test_it_records_the_architecture_when_given(self, tmp_path: Path) -> None:
        path = _save(tmp_path, arch=architecture_metadata(_model()))
        state = load_training_checkpoint(path)
        assert state is not None
        assert state["arch"]["d_model"] == 8
        assert state["arch"]["n_layers"] == 1

    def test_the_epoch_is_zero_based_as_before(self, tmp_path: Path) -> None:
        """The metadata change must not move the resume point."""
        state = load_training_checkpoint(_save(tmp_path))
        assert state is not None
        assert state["epoch"] == 7

    def test_a_missing_file_returns_none(self, tmp_path: Path) -> None:
        assert load_training_checkpoint(tmp_path / "missing.pt") is None

    def test_a_malformed_file_raises(self, tmp_path: Path) -> None:
        """A corrupt checkpoint is not "nothing to resume": it is a bug."""
        path = tmp_path / "garbage.pt"
        path.write_bytes(b"not a torch file")
        with pytest.raises(Exception):
            load_training_checkpoint(path)
