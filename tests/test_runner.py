"""Tests for the multi-seed runner (src/experiments/runner.py)."""

import pytest

from src.experiments.runner import parse_seeds, run_seeds


class TestParseSeeds:
    def test_parses_comma_separated(self) -> None:
        assert parse_seeds("0,1,2") == [0, 1, 2]

    def test_strips_whitespace(self) -> None:
        assert parse_seeds(" 0, 1 ,2 ") == [0, 1, 2]

    def test_single_seed(self) -> None:
        assert parse_seeds("7") == [7]


class TestRunSeeds:
    def test_aggregates_mean_std_min_max(self) -> None:
        def fn(seed: int) -> dict[str, float]:
            return {"metric": float(seed)}

        result = run_seeds(fn, [0, 1, 2])
        assert result.aggregate["metric"]["mean"] == 1.0
        assert result.aggregate["metric"]["min"] == 0.0
        assert result.aggregate["metric"]["max"] == 2.0
        assert result.aggregate["metric"]["n"] == 3.0
        assert result.aggregate["metric"]["std"] == pytest.approx(0.8164965809)
        assert len(result.per_seed) == 3

    def test_single_seed_has_zero_std(self) -> None:
        result = run_seeds(lambda s: {"metric": 5.0}, [0])
        assert result.aggregate["metric"]["std"] == 0.0

    def test_empty_seeds_raises(self) -> None:
        with pytest.raises(ValueError, match="at least one seed"):
            run_seeds(lambda s: {"metric": 1.0}, [])

    def test_mismatched_metric_keys_raises(self) -> None:
        def fn(seed: int) -> dict[str, float]:
            return {"a": 1.0} if seed == 0 else {"a": 1.0, "b": 2.0}

        with pytest.raises(ValueError, match="different metric keys"):
            run_seeds(fn, [0, 1])

    def test_optional_keys_may_be_absent_and_are_not_aggregated(self) -> None:
        # A mixed run (one seed confirmed a head, one did not) must not crash
        # after training: the optional metric is absent for one seed and has
        # no run-level mean.
        def fn(seed: int) -> dict[str, float]:
            return {"a": 1.0} if seed == 0 else {"a": 1.0, "b": 2.0}

        result = run_seeds(fn, [0, 1], optional_keys={"b"})
        assert result.per_seed[0] == {"a": 1.0}
        assert "b" not in result.aggregate
        assert result.aggregate["a"]["n"] == 2.0

    def test_an_optional_key_present_in_every_seed_is_aggregated(self) -> None:
        result = run_seeds(lambda _s: {"a": 1.0, "b": 2.0}, [0, 1], optional_keys={"b"})
        assert result.aggregate["b"]["mean"] == 2.0

    def test_a_dropped_required_key_still_raises(self) -> None:
        def fn(seed: int) -> dict[str, float]:
            return {"a": 1.0, "b": 2.0} if seed == 0 else {"b": 2.0}

        with pytest.raises(ValueError, match="different metric keys"):
            run_seeds(fn, [0, 1], optional_keys={"b"})

    def test_fn_receives_the_seed(self) -> None:
        seen = []

        def fn(seed: int) -> dict[str, float]:
            seen.append(seed)
            return {"metric": 0.0}

        run_seeds(fn, [3, 1, 4])
        assert seen == [3, 1, 4]

    def test_on_seed_is_called_after_each_seed_not_at_the_end(self) -> None:
        """A dead session must keep the seeds it already finished.

        The callback is the recovery hook the long GPU runs use to write a
        per-seed manifest. It has to fire between seeds; collecting the
        calls and replaying them at the end would lose exactly the work the
        hook exists to save.
        """
        order: list[tuple[str, int]] = []

        def fn(seed: int) -> dict[str, float]:
            order.append(("run", seed))
            return {"metric": float(seed)}

        def on_seed(seed: int, metrics: dict[str, float], seconds: float) -> None:
            assert metrics == {"metric": float(seed)}
            assert seconds >= 0.0
            order.append(("callback", seed))

        run_seeds(fn, [0, 1, 2], on_seed=on_seed)
        assert order == [
            ("run", 0),
            ("callback", 0),
            ("run", 1),
            ("callback", 1),
            ("run", 2),
            ("callback", 2),
        ]

    def test_a_callback_exception_propagates(self) -> None:
        """A broken recovery artifact is a bug, not a logging inconvenience."""

        def on_seed(seed: int, metrics: dict[str, float], seconds: float) -> None:
            raise RuntimeError("disk full")

        with pytest.raises(RuntimeError, match="disk full"):
            run_seeds(lambda s: {"metric": 1.0}, [0], on_seed=on_seed)

    def test_on_seed_is_optional(self) -> None:
        result = run_seeds(lambda s: {"metric": 1.0}, [0, 1])
        assert result.aggregate["metric"]["n"] == 2.0
