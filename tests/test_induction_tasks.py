"""Tests for the two induction tasks (the geometry, not the science).

The variable-distance task is the one that makes Rung 1's headline claim
testable at all (ADR 0033), so its *invariants* are pinned here:

1. every token appears at most twice, and a copied token's previous
   occurrence is unique — the task must be well posed;
2. the copy queries are exactly the positions where "copy what followed the
   previous occurrence" is the right answer, and they are derived from the
   tokens alone (the detector must not have to trust the generator);
3. the distance between a token and its previous occurrence *varies*, which
   is the whole point: a fixed-offset head must not be able to solve the
   task;
4. the best fixed-offset predictor stays far below what a content-matching
   head reaches — that gap is the claim;
5. the periodic task's data is bit-for-bit what it always was, so every
   manifest this repository has written stays reproducible.
"""

from __future__ import annotations

import numpy as np
import pytest
import torch

from src.experiments.induction_tasks import (
    GENERATOR_VERSION,
    TASK_PERIODIC,
    TASK_VARIABLE,
    TaskSpec,
    copy_accuracy_by_distance,
    copy_mask_for_pairs,
    copy_queries,
    fixed_offset_baseline,
    make_task_batch,
    make_variable_tokens,
    previous_occurrences,
    task_datasets,
)

VARIABLE = TaskSpec.variable()
SMALL = TaskSpec.variable(
    vocab_size=64, seq_len=24, key_len=12, copy_blocks=2, copy_block_len=3
)


class TestTaskSpec:
    def test_periodic_spec_keeps_its_own_convention(self) -> None:
        spec = TaskSpec.periodic(vocab_size=32, seq_len=64)
        assert spec.prefix_len == 32
        assert spec.to_dict()["name"] == TASK_PERIODIC
        assert spec.to_dict()["prefix_len"] == 32

    def test_variable_spec_reports_its_geometry(self) -> None:
        d = VARIABLE.to_dict()
        assert d["name"] == TASK_VARIABLE
        assert d["generator_version"] == GENERATOR_VERSION
        assert d["n_copy_queries"] == VARIABLE.n_copy_queries
        assert d["filler_total"] == VARIABLE.filler_total

    def test_variable_spec_rejects_a_layout_that_does_not_fit(self) -> None:
        with pytest.raises(ValueError):
            TaskSpec.variable(seq_len=16, key_len=12, copy_blocks=2, copy_block_len=3)

    def test_variable_spec_rejects_overlapping_source_windows(self) -> None:
        with pytest.raises(ValueError):
            TaskSpec.variable(key_len=8, copy_blocks=2, copy_block_len=6)

    def test_unknown_task_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            TaskSpec(name="nope")


class TestVariableTaskInvariants:
    def test_every_token_appears_at_most_twice(self) -> None:
        tokens = make_variable_tokens(VARIABLE, 32, seed=0)
        for row in tokens:
            _values, counts = np.unique(row, return_counts=True)
            assert counts.max() <= 2, "a token appeared three times: the task is ill posed"

    def test_a_copied_token_has_exactly_one_previous_occurrence(self) -> None:
        tokens = make_variable_tokens(VARIABLE, 32, seed=1)
        prev = previous_occurrences(tokens)
        for b in range(tokens.shape[0]):
            for q in range(tokens.shape[1]):
                if prev[b, q] >= 0:
                    # exactly one previous occurrence: the *nearest* one is
                    # the only one, and the token is not a third copy
                    assert tokens[b, prev[b, q]] == tokens[b, q]

    def test_the_copied_block_is_a_verbatim_slice_of_the_key(self) -> None:
        tokens = make_variable_tokens(VARIABLE, 16, seed=2)
        geom = copy_queries(tokens)
        for b in range(tokens.shape[0]):
            row = tokens[b]
            for q in np.nonzero(geom["mask"][b])[0]:
                src = int(geom["prev"][b, q])
                assert src < VARIABLE.key_len, "the source is not in the key"
                # the token after the source is the token after the query
                assert row[src + 1] == row[q + 1]

    def test_copy_queries_are_derived_from_the_tokens_alone(self) -> None:
        tokens = make_variable_tokens(VARIABLE, 8, seed=3)
        geom = copy_queries(tokens)
        for b in range(tokens.shape[0]):
            row = tokens[b]
            for q in range(tokens.shape[1] - 1):
                expected = False
                for p in range(q):
                    if row[p] == row[q] and row[p + 1] == row[q + 1]:
                        expected = True
                        break
                assert bool(geom["mask"][b, q]) == expected

    def test_the_number_of_copy_queries_is_the_specified_one(self) -> None:
        batch = make_task_batch(VARIABLE, 16, seed=4)
        assert batch.n_copy_queries == 16 * VARIABLE.n_copy_queries

    def test_the_distance_varies(self) -> None:
        tokens = make_variable_tokens(VARIABLE, 64, seed=5)
        geom = copy_queries(tokens)
        distances = geom["distance"][geom["mask"]]
        assert len(set(distances.tolist())) >= 8, (
            "the repeats must sit at varying distances — that is the whole "
            "point of the task"
        )

    def test_the_best_fixed_offset_predictor_stays_far_below_a_content_head(self) -> None:
        tokens = make_variable_tokens(VARIABLE, 128, seed=6)
        geom = copy_queries(tokens)
        baseline = fixed_offset_baseline(tokens, geom["mask"])
        assert baseline["n_queries"] > 0
        assert baseline["best_accuracy"] < 0.30, (
            f"a fixed offset already explains {baseline['best_accuracy']:.1%} of "
            "the copy queries — the task does not separate the mechanisms"
        )

    def test_a_content_oracle_solves_every_copy_query(self) -> None:
        """The ceiling of the content mechanism is 1.0 by construction."""
        tokens = make_variable_tokens(VARIABLE, 8, seed=7)
        geom = copy_queries(tokens)
        answers = tokens[:, 1:]
        mask = geom["mask"][:, :-1]
        content_key = geom["content_key"]
        predictions = np.take_along_axis(
            tokens, np.clip(content_key, 0, tokens.shape[1] - 1), axis=1
        )[:, :-1]
        assert (predictions[mask] == answers[mask]).all()

    def test_the_task_is_reproducible(self) -> None:
        a = make_variable_tokens(VARIABLE, 8, seed=11)
        b = make_variable_tokens(VARIABLE, 8, seed=11)
        c = make_variable_tokens(VARIABLE, 8, seed=12)
        assert np.array_equal(a, b)
        assert not np.array_equal(a, c)


class TestFixedOffsetBaseline:
    def test_a_planted_fixed_offset_head_is_found(self) -> None:
        """A predictor that always copies from q-d+1 is detected as such."""
        tokens = make_variable_tokens(SMALL, 32, seed=12)
        geom = copy_queries(tokens)
        baseline = fixed_offset_baseline(tokens, geom["mask"])
        d = baseline["best_offset"]
        answers = tokens[:, 1:]
        mask = geom["mask"][:, :-1]
        q_idx = np.arange(answers.shape[1])[None, :]
        key_idx = q_idx - d + 1
        valid = mask & (key_idx >= 0) & (key_idx < answers.shape[1])
        picked = np.take_along_axis(answers, np.clip(key_idx, 0, answers.shape[1] - 1), axis=1)
        planted = float((picked[valid] == answers[valid]).mean())
        assert planted == pytest.approx(baseline["best_accuracy"])

    def test_the_baseline_reports_the_query_count(self) -> None:
        tokens = make_variable_tokens(SMALL, 8, seed=13)
        geom = copy_queries(tokens)
        baseline = fixed_offset_baseline(tokens, geom["mask"])
        assert baseline["n_queries"] == int(geom["mask"].sum())


class TestDistanceBreakdown:
    def test_the_nonmodal_accuracy_separates_a_fixed_offset_head(self) -> None:
        """A fixed-offset predictor is wrong on the non-modal distances."""
        tokens = make_variable_tokens(VARIABLE, 64, seed=14)
        geom = copy_queries(tokens)
        answers = tokens[:, 1:]
        mask = geom["mask"][:, :-1]
        q_idx = np.arange(answers.shape[1])[None, :]
        d = 20
        key_idx = q_idx - d + 1
        valid = mask & (key_idx >= 0) & (key_idx < answers.shape[1])
        picked = np.take_along_axis(answers, np.clip(key_idx, 0, answers.shape[1] - 1), axis=1)
        predictions = np.where(valid, picked, -1)
        breakdown = copy_accuracy_by_distance(
            tokens, geom["mask"], geom["distance"], predictions
        )
        assert breakdown["copy_accuracy_nonmodal"] < 0.5
        assert breakdown["n_distances"] >= 8

    def test_a_content_oracle_is_right_on_every_distance(self) -> None:
        tokens = make_variable_tokens(VARIABLE, 32, seed=15)
        geom = copy_queries(tokens)
        content_key = geom["content_key"]
        predictions = np.take_along_axis(
            tokens, np.clip(content_key, 0, tokens.shape[1] - 1), axis=1
        )[:, :-1]
        breakdown = copy_accuracy_by_distance(
            tokens, geom["mask"], geom["distance"], predictions
        )
        assert breakdown["copy_accuracy_nonmodal"] == pytest.approx(1.0)
        assert min(breakdown["accuracy_by_distance"].values()) == pytest.approx(1.0)


class TestDatasets:
    def test_the_mask_matches_the_pairs(self) -> None:
        _train, val = task_datasets(VARIABLE, 16, 16, seed=16)
        x, y = val.tensors
        mask = copy_mask_for_pairs(x, y)
        assert mask.shape == x.shape
        assert mask.sum() > 0

    def test_the_periodic_task_is_bit_for_bit_the_old_data(self) -> None:
        """Every manifest in this repository depends on this."""
        from src.experiments.exp1_induction_heads import make_repeated_token_data

        spec = TaskSpec.periodic(vocab_size=32, seq_len=64)
        train, val = task_datasets(spec, 128, 64, seed=42)
        old_train, old_val = make_repeated_token_data(
            vocab_size=32, seq_len=64, num_train=128, num_val=64, seed=42
        )
        assert torch.equal(train.tensors[0], old_train.tensors[0])
        assert torch.equal(train.tensors[1], old_train.tensors[1])
        assert torch.equal(val.tensors[0], old_val.tensors[0])
        assert torch.equal(val.tensors[1], old_val.tensors[1])

    def test_the_variable_task_holds_out_fresh_sequences(self) -> None:
        train, val = task_datasets(VARIABLE, 16, 16, seed=17)
        assert not torch.equal(train.tensors[0], val.tensors[0])
