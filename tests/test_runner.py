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

    def test_fn_receives_the_seed(self) -> None:
        seen = []

        def fn(seed: int) -> dict[str, float]:
            seen.append(seed)
            return {"metric": 0.0}

        run_seeds(fn, [3, 1, 4])
        assert seen == [3, 1, 4]
