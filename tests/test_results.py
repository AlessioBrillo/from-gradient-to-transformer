"""Tests for results manifests and the RESULTS.md claims verifier
(src/results.py)."""

import json
from pathlib import Path

import pytest
import torch
from torch import nn

from src.results import (
    ResultsManifest,
    _git_tracked,
    _tree_dirty_outside_results,
    count_parameters,
    git_provenance,
    verify_claims,
)


class TestGitProvenance:
    def test_returns_sha_and_dirty_flag(self) -> None:
        sha, dirty = git_provenance()
        assert isinstance(sha, str)
        assert len(sha) > 0
        assert isinstance(dirty, bool)

    def test_untracked_code_file_is_dirty(self) -> None:
        assert _tree_dirty_outside_results(["?? src/new_module.py"]) is True

    def test_modified_results_manifest_is_not_dirty(self) -> None:
        assert _tree_dirty_outside_results([" M results/exp1_induction_heads.json"]) is False
        assert _tree_dirty_outside_results(["?? results/exp9_brand_new.json"]) is False

    def test_empty_status_is_clean(self) -> None:
        assert _tree_dirty_outside_results([]) is False


class TestCountParameters:
    def test_counts_trainable_params(self) -> None:
        model = nn.Linear(4, 8, bias=False)
        assert count_parameters(model) == 32

    def test_counts_across_multiple_params(self) -> None:
        model = nn.Linear(4, 8, bias=True)
        assert count_parameters(model) == 4 * 8 + 8


class TestResultsManifest:
    def test_from_run_populates_environment_fields(self) -> None:
        manifest = ResultsManifest.from_run(
            experiment="test_exp",
            seeds=[0, 1],
            args={"lr": 0.01, "epochs": 10},
            per_seed_metrics=[{"acc": 0.9}, {"acc": 0.95}],
            aggregate={"acc": {"mean": 0.925, "std": 0.025, "min": 0.9, "max": 0.95, "n": 2}},
            wall_clock_seconds=1.23,
            device="cpu",
        )
        assert manifest.experiment == "test_exp"
        assert manifest.seeds == [0, 1]
        assert manifest.torch_version == torch.__version__
        assert manifest.device == "cpu"
        assert manifest.git_sha  # non-empty

    def test_save_and_load_roundtrip(self, tmp_path: Path) -> None:
        manifest = ResultsManifest.from_run(
            experiment="test_exp",
            seeds=[0],
            args={"lr": 0.01},
            per_seed_metrics=[{"acc": 0.9}],
            aggregate={"acc": {"mean": 0.9, "std": 0.0, "min": 0.9, "max": 0.9, "n": 1}},
            wall_clock_seconds=0.5,
            device="cpu",
            n_parameters=42,
        )
        path = tmp_path / "manifest.json"
        manifest.save(path)
        assert path.exists()

        loaded = ResultsManifest.load(path)
        assert loaded.experiment == "test_exp"
        assert loaded.n_parameters == 42
        assert loaded.aggregate["acc"]["mean"] == 0.9

    def test_non_json_safe_args_are_stringified(self, tmp_path: Path) -> None:
        manifest = ResultsManifest.from_run(
            experiment="test_exp",
            seeds=[0],
            args={"path_arg": Path("/some/path")},
            per_seed_metrics=[{"acc": 1.0}],
            aggregate={"acc": {"mean": 1.0, "std": 0.0, "min": 1.0, "max": 1.0, "n": 1}},
            wall_clock_seconds=0.1,
            device="cpu",
        )
        # Must not raise — Path is not JSON-serializable by default.
        path = tmp_path / "manifest.json"
        manifest.save(path)
        data = json.loads(path.read_text())
        assert data["args"]["path_arg"] == "/some/path"


class TestVerifyClaims:
    def _write_manifest(self, results_dir: Path, name: str, dirty: bool = False) -> Path:
        manifest = ResultsManifest.from_run(
            experiment=name,
            seeds=[0, 1, 2],
            args={},
            per_seed_metrics=[{"m": 1.0}, {"m": 2.0}, {"m": 3.0}],
            aggregate={"m": {"mean": 2.0, "std": 0.8, "min": 1.0, "max": 3.0, "n": 3}},
            wall_clock_seconds=1.0,
            device="cpu",
        )
        manifest.git_dirty = dirty
        path = results_dir / f"{name}.json"
        manifest.save(path)
        return path

    def test_clean_manifest_and_tagged_claims_pass(self, tmp_path: Path) -> None:
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        manifest_path = self._write_manifest(results_dir, "exp_a")

        claims_file = tmp_path / "RESULTS.md"
        claims_file.write_text(f"# Results\n\n<!-- manifest: {manifest_path} -->\n")

        problems = verify_claims(results_dir, claims_file)
        assert problems == []

    def test_missing_results_dir_is_a_problem(self, tmp_path: Path) -> None:
        results_dir = tmp_path / "nonexistent"
        claims_file = tmp_path / "RESULTS.md"
        claims_file.write_text("# Results\n")

        problems = verify_claims(results_dir, claims_file)
        assert any("No manifests found" in p for p in problems)

    def test_untagged_claims_file_is_a_problem(self, tmp_path: Path) -> None:
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        self._write_manifest(results_dir, "exp_a")

        claims_file = tmp_path / "RESULTS.md"
        claims_file.write_text("# Results\n\nSome number: 0.97\n")  # no manifest tag

        problems = verify_claims(results_dir, claims_file)
        assert any("no <!-- manifest:" in p for p in problems)

    def test_dangling_manifest_tag_is_a_problem(self, tmp_path: Path) -> None:
        results_dir = tmp_path / "results"
        results_dir.mkdir()

        claims_file = tmp_path / "RESULTS.md"
        claims_file.write_text("# Results\n\n<!-- manifest: results/does_not_exist.json -->\n")

        problems = verify_claims(results_dir, claims_file)
        assert any("references missing file" in p for p in problems)

    def test_dirty_manifest_is_flagged(self, tmp_path: Path) -> None:
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        manifest_path = self._write_manifest(results_dir, "exp_a", dirty=True)

        claims_file = tmp_path / "RESULTS.md"
        claims_file.write_text(f"# Results\n\n<!-- manifest: {manifest_path} -->\n")

        problems = verify_claims(results_dir, claims_file)
        assert any("dirty working tree" in p for p in problems)

    def test_missing_claims_file_is_a_problem(self, tmp_path: Path) -> None:
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        self._write_manifest(results_dir, "exp_a")

        problems = verify_claims(results_dir, tmp_path / "does_not_exist.md")
        assert any("file not found" in p for p in problems)

    def _fig_ref(self, path: Path) -> str:
        """Backtick-wrapped citation, matching how every real figure
        reference in portfolio/RESULTS.md is written. Uses as_posix() so the
        citation contains forward slashes on every OS — verify_claims'
        FIGURE_CITATION_RE looks for a literal 'figures/' substring, the
        same way real citations are always written regardless of platform."""
        return f"`{path.as_posix()}`"

    def test_cited_figure_missing_from_disk_is_a_problem(self, tmp_path: Path) -> None:
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        manifest_path = self._write_manifest(results_dir, "exp_a")
        missing_fig = tmp_path / "portfolio" / "figures" / "exp_a_plot.png"

        claims_file = tmp_path / "RESULTS.md"
        claims_file.write_text(
            f"## Rung A\n\n**Figures**: {self._fig_ref(missing_fig)}\n\n"
            f"<!-- manifest: {manifest_path} -->\n"
        )

        problems = verify_claims(results_dir, claims_file)
        assert any("does not exist on disk" in p for p in problems)

    def test_cited_figure_untracked_by_git_is_a_problem(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        manifest_path = self._write_manifest(results_dir, "exp_a")
        fig = tmp_path / "portfolio" / "figures" / "exp_a_plot.png"
        fig.parent.mkdir(parents=True)
        fig.write_bytes(b"")

        claims_file = tmp_path / "RESULTS.md"
        claims_file.write_text(
            f"## Rung A\n\n**Figures**: {self._fig_ref(fig)}\n\n"
            f"<!-- manifest: {manifest_path} -->\n"
        )

        monkeypatch.setattr("src.results._git_tracked", lambda p: False)
        problems = verify_claims(results_dir, claims_file)
        assert any("not tracked by git" in p for p in problems)

    def test_cited_figure_present_and_tracked_is_clean(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        manifest_path = self._write_manifest(results_dir, "exp_a")
        fig = tmp_path / "portfolio" / "figures" / "exp_a_plot.png"
        fig.parent.mkdir(parents=True)
        fig.write_bytes(b"")

        claims_file = tmp_path / "RESULTS.md"
        claims_file.write_text(
            f"## Rung A\n\n**Figures**: {self._fig_ref(fig)}\n\n"
            f"<!-- manifest: {manifest_path} -->\n"
        )

        monkeypatch.setattr("src.results._git_tracked", lambda p: True)
        problems = verify_claims(results_dir, claims_file)
        assert problems == []

    def test_section_with_figures_but_no_manifest_tag_is_a_problem(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        manifest_path = self._write_manifest(results_dir, "exp_a")
        fig = tmp_path / "figures" / "exp_b_plot.png"
        fig.parent.mkdir(parents=True)
        fig.write_bytes(b"")

        claims_file = tmp_path / "RESULTS.md"
        claims_file.write_text(
            f"<!-- manifest: {manifest_path} -->\n\n"
            f"## Rung B: Untagged Section\n\n**Outputs**: {self._fig_ref(fig)}\n"
        )

        monkeypatch.setattr("src.results._git_tracked", lambda p: True)
        problems = verify_claims(results_dir, claims_file)
        assert any(
            "Rung B: Untagged Section" in p and "no <!-- manifest:" in p
            for p in problems
        )

    def test_section_with_figures_and_its_own_tag_is_clean(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        manifest_path = self._write_manifest(results_dir, "exp_a")
        fig = tmp_path / "portfolio" / "figures" / "exp_a_plot.png"
        fig.parent.mkdir(parents=True)
        fig.write_bytes(b"")

        claims_file = tmp_path / "RESULTS.md"
        claims_file.write_text(
            f"## Rung A\n\n**Figures**: {self._fig_ref(fig)}\n\n"
            f"<!-- manifest: {manifest_path} -->\n"
        )

        monkeypatch.setattr("src.results._git_tracked", lambda p: True)
        problems = verify_claims(results_dir, claims_file)
        assert problems == []

    def test_falsifies_against_the_2026_08_07_state(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The checker existing before this change would pass this
        RESULTS.md — it never parses figure paths at all, and the whole-file
        'no tags anywhere' check stays quiet once *any* section has a tag.
        This reconstructs the real shape of the gap found in Micro-Phase 12:
        a cited figure that was never generated, and a results section with
        no manifest tag of its own even though the file has tags elsewhere."""
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        manifest_path = self._write_manifest(results_dir, "exp3_superposition")
        missing_fig = tmp_path / "figures" / "exp3_pentagon_geometry.png"
        untagged_fig = tmp_path / "figures" / "exp2_grokking_curve.png"
        untagged_fig.parent.mkdir(parents=True)
        untagged_fig.write_bytes(b"")

        claims_file = tmp_path / "RESULTS.md"
        claims_file.write_text(
            "## Rung 3: Superposition\n\n"
            f"<!-- manifest: {manifest_path} -->\n\n"
            f"Figure: {self._fig_ref(missing_fig)}.\n\n"
            "## Rung 2: Grokking\n\n"
            f"**Figures**: {self._fig_ref(untagged_fig)}\n"
        )

        monkeypatch.setattr("src.results._git_tracked", lambda p: True)
        problems = verify_claims(results_dir, claims_file)

        assert any("does not exist on disk" in p for p in problems)
        assert any("Rung 2: Grokking" in p and "no <!-- manifest:" in p for p in problems)


class TestGitTracked:
    def test_tracked_repo_file_returns_true(self) -> None:
        assert _git_tracked(Path("tests/test_results.py")) is True

    def test_untracked_path_returns_false(self, tmp_path: Path) -> None:
        untracked = tmp_path / "not_in_the_repo.png"
        untracked.write_bytes(b"")
        assert _git_tracked(untracked) is False
