"""verify_claims only checks git-tracked manifests.

`results/probe_*_quick.json` — where `--quick` runs go, see
src.results.resolve_manifest_path — is deliberately untracked scratch. It is
necessarily recorded against a dirty tree (you run `--quick` while editing
code), so checking it failed the whole verifier for a file no document cites.
This was not hypothetical: an early version of the .gitignore rule was added
after one such file had already been committed, and `make verify-claims` went
red as a result.
"""

from __future__ import annotations

from pathlib import Path

import src.results as results_mod
from src.results import ResultsManifest, verify_claims

TRACKED = "probe_tracked.json"
SCRATCH = "probe_x_quick.json"


def _manifest(tmp_path: Path, name: str, dirty: bool) -> Path:
    m = ResultsManifest(
        experiment="probe",
        seeds=[0],
        args={},
        per_seed_metrics=[{"acc": 1.0}],
        aggregate={"acc": {"mean": 1.0, "std": 0.0, "min": 1.0, "max": 1.0, "n": 1}},
        wall_clock_seconds=1.0,
        git_sha="deadbee",
        git_dirty=dirty,
        device="cpu",
        torch_version="test",
        numpy_version="test",
        python_version="test",
        n_parameters=1,
    )
    m.save(tmp_path / name)
    return tmp_path / name


def _claims_file(tmp_path: Path) -> Path:
    path = tmp_path / "claims.md"
    path.write_text("", encoding="utf-8")
    return path


def _only_tracked_checked(monkeypatch) -> None:
    """One manifest tracked, the scratch one not — the production situation."""

    def fake_tracked(path: Path) -> bool:
        return path.name == TRACKED

    monkeypatch.setattr(results_mod, "_git_tracked", fake_tracked)


def test_untracked_dirty_manifest_is_ignored(tmp_path: Path, monkeypatch) -> None:
    _manifest(tmp_path, TRACKED, dirty=False)
    _manifest(tmp_path, SCRATCH, dirty=True)
    _only_tracked_checked(monkeypatch)

    problems = verify_claims(tmp_path, _claims_file(tmp_path))
    manifest_tier = [p for p in problems if "no <!-- manifest" not in p]
    assert manifest_tier == [], manifest_tier


def test_tracked_dirty_manifest_is_still_a_problem(tmp_path: Path, monkeypatch) -> None:
    """The guard must not weaken the original contract for tracked files."""
    _manifest(tmp_path, TRACKED, dirty=True)
    _manifest(tmp_path, SCRATCH, dirty=False)
    _only_tracked_checked(monkeypatch)

    problems = verify_claims(tmp_path, _claims_file(tmp_path))
    assert any("dirty working tree" in p for p in problems), problems


def test_all_tracked_clean_manifests_pass(tmp_path: Path, monkeypatch) -> None:
    _manifest(tmp_path, TRACKED, dirty=False)
    _manifest(tmp_path, SCRATCH, dirty=False)
    monkeypatch.setattr(results_mod, "_git_tracked", lambda _p: True)

    problems = verify_claims(tmp_path, _claims_file(tmp_path))
    manifest_tier = [p for p in problems if "no <!-- manifest" not in p]
    assert manifest_tier == [], problems
