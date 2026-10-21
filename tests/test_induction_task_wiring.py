"""Tests for the task-aware wiring of Rung 1 (and the cascade it feeds).

What is pinned here:

1. `--task variable` produces the variable-distance data, `--task periodic`
   produces the historical data, and the two never mix;
2. the copy metrics are computed on the copy queries and not on the whole
   sequence — on the variable task only a quarter of the positions are
   learnable, so the overall accuracy would be mostly noise;
3. the detector is called with the task, so the periodic run's numbers stay
   the ones the manifests recorded and the variable run measures the
   content hypothesis;
4. the naming test follows the task: the periodic task needs the
   off-distribution batch, the variable task does not;
5. the Rung 4 patch batch is read at a *copy query* on the variable task —
   a fixed position would be a filler position, where the logit difference
   is noise.
"""

from __future__ import annotations

import argparse

import numpy as np
import torch
from torch.utils.data import DataLoader

from src.experiments.exp1_induction_heads import (
    AttentionOnlyTransformer,
    _run_task_probe,
    analyze_copy_metrics,
    causal_ablation,
    default_variable_geometry,
    make_task_data,
    task_spec_from_args,
)
from src.experiments.induction_tasks import (
    TASK_PERIODIC,
    TASK_VARIABLE,
    TaskSpec,
    copy_query_batch,
    task_datasets,
)


def _args(**overrides) -> argparse.Namespace:
    base = dict(
        task=TASK_VARIABLE,
        vocab_size=256,
        seq_len=24,
        d_model=32,
        n_layers=2,
        n_heads=4,
        num_train=64,
        batch_size=16,
        prefix_ratio=0.5,
        key_len=None,
        copy_blocks=None,
        copy_block_len=None,
        probe_dissociation=True,
    )
    base.update(overrides)
    return argparse.Namespace(**base)


def _model(vocab: int = 256, seq: int = 24) -> AttentionOnlyTransformer:
    return AttentionOnlyTransformer(
        vocab_size=vocab, d_model=32, n_layers=2, n_heads=4, max_seq_len=seq
    )


class TestTaskSelection:
    def test_the_default_is_the_periodic_task(self) -> None:
        spec = task_spec_from_args(_args(task=TASK_PERIODIC))
        assert spec.name == TASK_PERIODIC
        assert spec.prefix_len == 12

    def test_the_variable_task_derives_its_geometry(self) -> None:
        spec = task_spec_from_args(_args(task=TASK_VARIABLE))
        assert spec.name == TASK_VARIABLE
        assert spec.key_len == 15
        assert spec.copy_blocks == 2
        assert spec.copy_block_len == 3

    def test_the_standard_geometry_is_the_pre_registered_one(self) -> None:
        assert default_variable_geometry(64) == (36, 4, 5)
        spec = task_spec_from_args(_args(task=TASK_VARIABLE, seq_len=64))
        assert (spec.key_len, spec.copy_blocks, spec.copy_block_len) == (36, 4, 5)

    def test_explicit_geometry_wins(self) -> None:
        spec = task_spec_from_args(
            _args(task=TASK_VARIABLE, key_len=15, copy_blocks=2, copy_block_len=3)
        )
        assert spec.key_len == 15

    def test_the_data_follows_the_task(self) -> None:
        variable = make_task_data(_args(task=TASK_VARIABLE), 32, 16, seed=0)
        periodic = make_task_data(_args(task=TASK_PERIODIC), 32, 16, seed=0)
        assert not torch.equal(variable[0].tensors[0], periodic[0].tensors[0])


class TestCopyMetrics:
    def test_the_metrics_are_computed_on_the_copy_queries(self) -> None:
        args = _args()
        _train, val = make_task_data(args, 64, 64, seed=0)
        loader = DataLoader(val, batch_size=16, shuffle=False)
        stats = analyze_copy_metrics(_model(), loader)
        assert stats["n_copy_queries"] > 0
        # The overall accuracy and the copy accuracy are different numbers:
        # on this task only a quarter of the positions are copy queries.
        assert stats["overall_accuracy"] != stats["copy_accuracy"]
        assert 0.0 <= stats["fixed_offset_baseline"] <= 1.0
        assert stats["n_distances"] >= 4

    def test_the_ablation_can_be_restricted_to_the_copy_queries(self) -> None:
        args = _args()
        _train, val = make_task_data(args, 64, 64, seed=0)
        loader = DataLoader(val, batch_size=16, shuffle=False)
        model = _model()
        overall = causal_ablation(model, loader, 0, 0)
        on_copy = causal_ablation(model, loader, 0, 0, restrict_to_copy=True)
        assert 0.0 <= on_copy <= 1.0
        assert 0.0 <= overall <= 1.0

    def test_a_content_oracle_scores_a_perfect_copy_accuracy(self) -> None:
        """The metric's ceiling is 1.0 — the numbers are not capped lower."""
        spec = TaskSpec.variable(
            vocab_size=256, seq_len=24, key_len=15, copy_blocks=2, copy_block_len=3
        )
        _train, val = task_datasets(spec, 32, 32, seed=0)
        x, y = val.tensors
        full = torch.cat([x, y[:, -1:]], dim=1)
        from src.experiments.induction_tasks import copy_queries

        geom = copy_queries(full.numpy())
        key = np.clip(geom["content_key"], 0, full.shape[1] - 1)
        predictions = np.take_along_axis(full.numpy(), key, axis=1)[:, :-1]
        answers = full.numpy()[:, 1:]
        mask = geom["mask"][:, :-1]
        assert (predictions[mask] == answers[mask]).all()


class TestNamingTest:
    def test_the_variable_task_probes_in_distribution(self) -> None:
        args = _args()
        _train, val = make_task_data(args, 32, 32, seed=0)
        loader = DataLoader(val, batch_size=16, shuffle=False)
        tokens = next(iter(loader))[0]
        probe = _run_task_probe(_model(), args, loader, seed=0)
        assert "peak_offset_mass" in probe
        assert "logit_diff_content_minus_period" not in probe
        assert tokens.shape[0] > 0

    def test_the_periodic_task_probes_off_distribution(self) -> None:
        args = _args(task=TASK_PERIODIC)
        _train, val = make_task_data(args, 32, 32, seed=0)
        loader = DataLoader(val, batch_size=16, shuffle=False)
        probe = _run_task_probe(_model(), args, loader, seed=0)
        assert "peak_period_mass" in probe
        assert "logit_diff_content_minus_period" in probe


class TestPatchBatch:
    def test_the_patch_batch_reads_a_copy_query(self) -> None:
        args = _args()
        _train, val = make_task_data(args, 256, 256, seed=0)
        x, y = val.tensors
        patch = copy_query_batch(x, y, vocab_size=args.vocab_size)
        pos = patch["pos"]
        assert patch["clean_inputs"].shape[0] > 0
        assert patch["clean_answers"].shape[0] == patch["clean_inputs"].shape[0]
        # The answer at `pos` is the token that follows the copied token.
        full = torch.cat([x, y[:, -1:]], dim=1)
        from src.experiments.induction_tasks import copy_queries

        geom = copy_queries(full.numpy())
        assert bool(geom["mask"][:, pos].all())
        assert torch.equal(patch["clean_answers"], y[patch["clean_answers"].new_tensor(
            np.nonzero(geom["mask"][:, pos])[0][: patch["clean_inputs"].shape[0]]
        ), pos])

    def test_the_counterfactual_is_a_different_token(self) -> None:
        args = _args()
        _train, val = make_task_data(args, 256, 256, seed=0)
        x, y = val.tensors
        patch = copy_query_batch(x, y, vocab_size=args.vocab_size)
        assert bool((patch["clean_answers"] != patch["corrupted_answers"]).all())
