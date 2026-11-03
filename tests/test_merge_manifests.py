"""Tests for the per-seed recovery merge (src/experiments/merge_manifests.py).

The content-task GPU session can die between seeds. Each seed writes its own
complete manifest, and this tool rebuilds the multi-seed record the verdict
needs. The tests freeze the property that makes the rebuilt record evidence:
it refuses to combine files that are not the same run.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.experiments.merge_manifests import (
    _expand_inputs,
    main,
    merge_manifests,
)
from src.experiments.runner import aggregate_metrics
from src.results import ResultsManifest


def _manifest(seed: int, **overrides) -> ResultsManifest:
    metrics = {
        "copy_accuracy": 0.5 + seed / 100.0,
        "total_induction_heads": float(seed),
    }
    manifest = ResultsManifest(
        experiment="exp1_induction_heads",
        seeds=[seed],
        args={"task": "variable", "epochs": 3000},
        per_seed_metrics=[metrics],
        aggregate=aggregate_metrics([metrics]),
        wall_clock_seconds=100.0 + seed,
        git_sha="abc1234",
        git_dirty=False,
        device="cpu",
        torch_version="2.0",
        numpy_version="1.26",
        python_version="3.12",
        n_parameters=1234,
        notes=f"seed {seed}",
        source_provenance={
            "checkpoints": [
                {
                    "path": f"checkpoints/exp1_checkpoint_seed{seed}.pt",
                    "seed": seed,
                    "epoch": 3000,
                    "git_sha": "abc1234",
                    "git_dirty": False,
                }
            ]
        },
    )
    for key, value in overrides.items():
        setattr(manifest, key, value)
    return manifest


def _save(tmp_path: Path, manifest: ResultsManifest) -> Path:
    path = tmp_path / f"exp_seed{manifest.seeds[0]}.json"
    manifest.save(path)
    return path


class TestMergeManifests:
    def test_it_rebuilds_the_multi_seed_record(self) -> None:
        merged = merge_manifests([_manifest(0), _manifest(1), _manifest(2)])
        assert merged.seeds == [0, 1, 2]
        assert [row["copy_accuracy"] for row in merged.per_seed_metrics] == [
            0.5,
            0.51,
            0.52,
        ]
        assert merged.aggregate["copy_accuracy"]["n"] == 3.0
        assert merged.aggregate["copy_accuracy"]["mean"] == pytest.approx(0.51)
        assert merged.wall_clock_seconds == pytest.approx(303.0)
        assert "Merged from 3" in (merged.notes or "")

    def test_input_order_does_not_matter(self) -> None:
        merged = merge_manifests([_manifest(2), _manifest(0), _manifest(1)])
        assert merged.seeds == [0, 1, 2]
        assert [row["copy_accuracy"] for row in merged.per_seed_metrics] == [
            0.5,
            0.51,
            0.52,
        ]

    def test_a_duplicate_seed_is_refused(self) -> None:
        with pytest.raises(SystemExit, match="duplicate seeds"):
            merge_manifests([_manifest(0), _manifest(0)])

    def test_the_pre_registered_seed_set_is_required(self) -> None:
        with pytest.raises(SystemExit, match="missing \\[2\\]"):
            merge_manifests([_manifest(0), _manifest(1)], expected_seeds=[0, 1, 2])

    def test_an_extra_seed_is_refused(self) -> None:
        with pytest.raises(SystemExit, match="unexpected \\[3\\]"):
            merge_manifests(
                [_manifest(0), _manifest(1), _manifest(2), _manifest(3)],
                expected_seeds=[0, 1, 2],
            )

    def test_a_different_experiment_is_refused(self) -> None:
        other = _manifest(1, experiment="exp4_circuit_patching")
        with pytest.raises(SystemExit, match="experiment differs"):
            merge_manifests([_manifest(0), other])

    def test_a_different_config_is_refused(self) -> None:
        other = _manifest(1, args={"task": "variable", "epochs": 600})
        with pytest.raises(SystemExit, match="epochs"):
            merge_manifests([_manifest(0), other])

    def test_a_mixed_dirty_flag_is_refused(self) -> None:
        with pytest.raises(SystemExit, match="git_dirty differs"):
            merge_manifests([_manifest(0), _manifest(1, git_dirty=True)])

    def test_an_all_dirty_tree_is_refused(self) -> None:
        """Equal flags are not enough: dirty is dirty."""
        with pytest.raises(SystemExit, match="dirty working tree"):
            merge_manifests([_manifest(0, git_dirty=True), _manifest(1, git_dirty=True)])

    def test_a_different_commit_is_refused(self) -> None:
        with pytest.raises(SystemExit, match="git_sha differs"):
            merge_manifests([_manifest(0), _manifest(1, git_sha="def5678")])

    def test_optional_metric_differences_are_refused_by_default(self) -> None:
        first = _manifest(0)
        second = _manifest(1)
        del second.per_seed_metrics[0]["total_induction_heads"]
        with pytest.raises(SystemExit, match="--allow-optional"):
            merge_manifests([first, second])

    def test_allow_optional_keeps_only_the_common_aggregate(self) -> None:
        first = _manifest(0)
        second = _manifest(1)
        del second.per_seed_metrics[0]["total_induction_heads"]
        merged = merge_manifests([first, second], allow_optional=True)
        assert "total_induction_heads" not in merged.aggregate
        assert "total_induction_heads" not in merged.per_seed_metrics[1]
        assert "total_induction_heads" in merged.per_seed_metrics[0]

    def test_source_provenance_is_merged_in_seed_order(self) -> None:
        merged = merge_manifests([_manifest(2), _manifest(0), _manifest(1)])
        assert merged.source_provenance is not None
        checkpoints = merged.source_provenance["checkpoints"]
        assert [c["seed"] for c in checkpoints] == [0, 1, 2]

    def test_a_partial_source_provenance_is_refused(self) -> None:
        with pytest.raises(SystemExit, match="only some inputs"):
            merge_manifests([_manifest(0), _manifest(1, source_provenance=None)])

    def test_a_checkpoint_from_another_seed_is_refused(self) -> None:
        other = _manifest(1)
        other.source_provenance = {
            "checkpoints": [{"seed": 0, "git_sha": "abc1234", "git_dirty": False}]
        }
        with pytest.raises(SystemExit, match="names model seed 0"):
            merge_manifests([_manifest(0), other])


class TestTheCommandLine:
    def test_it_writes_the_merged_manifest(self, tmp_path, capsys) -> None:
        paths = [_save(tmp_path, _manifest(seed)) for seed in (2, 0, 1)]
        output = tmp_path / "merged.json"
        code = main(
            [
                "--inputs",
                *[str(path) for path in paths],
                "--output",
                str(output),
                "--expected-seeds",
                "0,1,2",
            ]
        )
        assert code == 0
        merged = ResultsManifest.load(output)
        assert merged.seeds == [0, 1, 2]
        assert "Merged from 3" in (merged.notes or "")

    def test_a_directory_input_expands_seed_manifests(self, tmp_path, capsys) -> None:
        for seed in (0, 1, 2):
            _save(tmp_path, _manifest(seed))
        output = tmp_path / "merged.json"
        code = main(["--inputs", str(tmp_path), "--output", str(output)])
        assert code == 0
        assert ResultsManifest.load(output).seeds == [0, 1, 2]

    def test_an_unknown_input_is_an_error(self, tmp_path, capsys) -> None:
        with pytest.raises(SystemExit, match="does not exist"):
            _expand_inputs([str(tmp_path / "missing*.json")])

    def test_a_multi_seed_input_is_refused(self, tmp_path, capsys) -> None:
        manifest = _manifest(0)
        manifest.seeds = [0, 1]
        manifest.per_seed_metrics = [manifest.per_seed_metrics[0]] * 2
        path = tmp_path / "multi.json"
        manifest.save(path)
        with pytest.raises(SystemExit, match="exactly one seed"):
            main(["--inputs", str(path), "--output", str(tmp_path / "out.json")])
