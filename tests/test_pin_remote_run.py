"""Tests for the remote-run manifest pinner (fail-closed).

`pin_remote_run.py` is the gate between a GPU run's output and the repo's
cited record. It must refuse, not forgive: a manifest with a fabricated or
unverifiable provenance is worse than a missing one, because
`verify-claims` would treat it as evidence.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.pin_remote_run import validate_manifest

REPO_ROOT = Path(__file__).resolve().parents[1]


def _head_sha() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=REPO_ROOT
    ).stdout.strip()


def _write_manifest(path: Path, **overrides) -> Path:
    manifest = {
        "experiment": "induction_scale_large",
        "seeds": [0, 1, 2],
        "args": {"modulus": 113},
        "per_seed_metrics": [
            {"final_val_acc": 0.9},
            {"final_val_acc": 0.91},
            {"final_val_acc": 0.92},
        ],
        "aggregate": {
            "final_val_acc": {"mean": 0.91, "std": 0.01, "min": 0.9, "max": 0.92, "n": 3}
        },
        "wall_clock_seconds": 120.0,
        "git_sha": _head_sha(),
        "git_dirty": False,
        "device": "cuda",
        "torch_version": "2.x",
        "numpy_version": "2.x",
        "python_version": "3.12.x",
        "n_parameters": 1000,
        "created_at": "2026-10-13T00:00:00+00:00",
        "notes": None,
    }
    manifest.update(overrides)
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


class TestValidateManifest:
    def test_valid_manifest_passes(self, tmp_path: Path) -> None:
        assert validate_manifest(_write_manifest(tmp_path / "ok.json")) == []

    def test_empty_aggregate_is_refused(self, tmp_path: Path) -> None:
        path = _write_manifest(tmp_path / "empty.json", aggregate={})
        problems = validate_manifest(path)
        assert any("empty aggregate" in p for p in problems)

    def test_seeds_must_match_per_seed_records(self, tmp_path: Path) -> None:
        path = _write_manifest(
            tmp_path / "mismatch.json",
            seeds=[0, 1, 2],
            per_seed_metrics=[{"final_val_acc": 0.9}],
        )
        problems = validate_manifest(path)
        assert any("per-seed records" in p for p in problems)

    def test_aggregate_n_must_match_seeds(self, tmp_path: Path) -> None:
        path = _write_manifest(
            tmp_path / "badn.json",
            aggregate={
                "final_val_acc": {"mean": 0.9, "std": 0.0, "min": 0.9, "max": 0.9, "n": 1}
            },
        )
        problems = validate_manifest(path)
        assert any("aggregate['final_val_acc']['n']=1" in p for p in problems)

    def test_dirty_tree_is_refused(self, tmp_path: Path) -> None:
        """A remote run clones a pinned ref, so git_dirty=true means the
        provenance is wrong — a local re-run stamped it, not the GPU run."""
        path = _write_manifest(tmp_path / "dirty.json", git_dirty=True)
        problems = validate_manifest(path)
        assert any("dirty working tree" in p for p in problems)

    def test_unknown_sha_is_refused(self, tmp_path: Path) -> None:
        path = _write_manifest(tmp_path / "ghost.json", git_sha="0" * 40)
        problems = validate_manifest(path)
        assert any("does not exist" in p for p in problems)

    def test_non_manifest_json_is_refused(self, tmp_path: Path) -> None:
        path = tmp_path / "garbage.json"
        path.write_text('{"hello": "world"}', encoding="utf-8")
        problems = validate_manifest(path)
        assert any("not a ResultsManifest" in p for p in problems)


class TestZipExpansion:
    """The notebooks ship manifests inside a zip (one archive for both
    runtimes), so a download directory usually holds no loose JSON at all."""

    def _zip_with_manifest(self, tmp_path: Path) -> Path:
        import zipfile

        src = tmp_path / "src"
        src.mkdir(parents=True, exist_ok=True)
        good = _write_manifest(src / "good.json")
        archive = tmp_path / "run.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            zf.write(good, arcname="results/good.json")
        return archive

    def test_zip_is_expanded_and_validated(self, tmp_path: Path) -> None:
        from scripts.pin_remote_run import _expand_zips

        archive = self._zip_with_manifest(tmp_path)
        # The download directory holds the zip (and nothing else useful):
        # that is exactly what the driver's `kaggle kernels output` gives.
        candidates = _expand_zips(tmp_path)
        assert any(c.name == "good.json" for c in candidates)
        extracted = archive.with_suffix("") / "results" / "good.json"
        assert extracted.exists()
        assert validate_manifest(extracted) == []

    def test_dry_run_pins_from_a_zip(self, tmp_path: Path) -> None:
        self._zip_with_manifest(tmp_path)
        proc = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "pin_remote_run.py"),
                "--from",
                str(tmp_path),
                "--dry-run",
            ],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "DRY RUN OK" in proc.stdout
        assert not (REPO_ROOT / "results" / "good.json").exists()

    def test_dry_run_pins_from_the_zip_file_itself(self, tmp_path: Path) -> None:
        """`--from <path-to.zip>` is the natural thing an operator types after
        `kaggle kernels output` hands them one archive."""
        archive = self._zip_with_manifest(tmp_path)
        proc = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "pin_remote_run.py"),
                "--from",
                str(archive),
                "--dry-run",
            ],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "DRY RUN OK" in proc.stdout


class TestDryRunEntryPoint:
    def test_dry_run_installs_nothing(self, tmp_path: Path) -> None:
        src = _write_manifest(tmp_path / "good.json")
        proc = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "pin_remote_run.py"),
                "--from",
                str(src),
                "--dry-run",
            ],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "DRY RUN OK" in proc.stdout
        assert not (REPO_ROOT / "results" / "good.json").exists()

    def test_invalid_manifest_fails_closed(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.json"
        bad.write_text('{"nope": 1}', encoding="utf-8")
        proc = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "pin_remote_run.py"),
                "--from",
                str(bad),
                "--dry-run",
            ],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode != 0
        assert "FAILED validation" in proc.stderr
