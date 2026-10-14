"""Tests for the Kaggle run driver: rendering, validation, kernel metadata.

The driver spends GPU hours, so everything cheap is checked before push:
the notebook contract (`test_remote_notebooks.py` covers the shared rules),
the ref pinning, and the kernel metadata Kaggle needs. The kaggle CLI
itself is never called here.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.kaggle_run import (
    NotebookError,
    code_cells,
    kaggle_preflight,
    kernel_dir_for,
    load_notebook,
    set_branch,
    validate_notebook,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
GROKKING_NB = REPO_ROOT / "notebooks" / "kaggle_grokking_p113.ipynb"


class TestSetBranch:
    def test_rewrites_the_branch_assignment(self) -> None:
        nb = load_notebook(GROKKING_NB)
        rendered = set_branch(nb, "gpu-run-42")
        assert any('BRANCH = "gpu-run-42"' in c for c in code_cells(rendered))

    def test_raises_without_a_branch_assignment(self) -> None:
        nb = {"cells": [{"cell_type": "code", "source": ["print(1)"], "outputs": []}]}
        with pytest.raises(NotebookError):
            set_branch(nb, "main")

    def test_raises_on_missing_file(self) -> None:
        with pytest.raises(NotebookError):
            load_notebook(REPO_ROOT / "notebooks" / "does_not_exist.ipynb")


class TestKernelDir:
    def test_metadata_enables_gpu_and_internet(self, tmp_path: Path) -> None:
        nb = load_notebook(GROKKING_NB)
        out = kernel_dir_for(nb, GROKKING_NB, "main", "someuser", "grokking-p113", tmp_path)
        meta = json.loads((out / "kernel-metadata.json").read_text(encoding="utf-8"))
        assert meta["id"] == "someuser/grokking-p113"
        assert meta["enable_gpu"] is True
        assert meta["enable_internet"] is True
        assert meta["kernel_type"] == "notebook"
        assert meta["code_file"] == GROKKING_NB.name

    def test_rendered_notebook_carries_the_pinned_ref(self, tmp_path: Path) -> None:
        nb = load_notebook(GROKKING_NB)
        out = kernel_dir_for(nb, GROKKING_NB, "v1.0.0", "u", "s", tmp_path)
        rendered = json.loads((out / GROKKING_NB.name).read_text(encoding="utf-8"))
        assert any('BRANCH = "v1.0.0"' in c for c in code_cells(rendered))
        # The tracked notebook keeps its placeholder: the repo is ref-agnostic.
        original = json.loads(GROKKING_NB.read_text(encoding="utf-8"))
        assert any('BRANCH = "main"' in c for c in code_cells(original))

    def test_the_tracked_notebook_passes_validation(self) -> None:
        assert validate_notebook(load_notebook(GROKKING_NB)) == []


class TestDryRunEntryPoint:
    """The full CLI validation path, end to end, without pushing."""

    def test_dry_run_succeeds_on_a_pushed_ref(self) -> None:
        import subprocess
        import sys

        proc = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "kaggle_run.py"),
                "--notebook",
                "notebooks/kaggle_grokking_p113.ipynb",
                "--branch",
                "main",
                "--dry-run",
            ],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=600,
        )
        assert proc.returncode == 0, f"dry-run failed:\n{proc.stdout}\n{proc.stderr}"
        assert "DRY RUN OK" in proc.stdout

    def test_dry_run_rejects_a_nonexistent_ref(self) -> None:
        import subprocess
        import sys

        proc = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "kaggle_run.py"),
                "--notebook",
                "notebooks/kaggle_grokking_p113.ipynb",
                "--branch",
                "no-such-ref-anywhere",
                "--dry-run",
            ],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=600,
        )
        assert proc.returncode != 0
        assert "does not exist on origin" in proc.stderr


class TestPreflight:
    """The preflight must tell the operator exactly what is missing —
    the failure mode of this step is a confused human, not a crash."""

    def test_missing_credentials_are_explained(self, monkeypatch, tmp_path: Path) -> None:
        monkeypatch.delenv("KAGGLE_USERNAME", raising=False)
        monkeypatch.delenv("KAGGLE_KEY", raising=False)
        monkeypatch.delenv("KAGGLE_API_TOKEN", raising=False)
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        problems = kaggle_preflight()
        assert any("access_token" in p for p in problems)

    def test_kgat_token_file_is_accepted(self, monkeypatch, tmp_path: Path) -> None:
        """Kaggle's current auth: the KGAT token at ~/.kaggle/access_token
        (or KAGGLE_API_TOKEN) — the preflight must not demand the legacy
        username/key pair when it is present."""
        monkeypatch.delenv("KAGGLE_USERNAME", raising=False)
        monkeypatch.delenv("KAGGLE_KEY", raising=False)
        monkeypatch.delenv("KAGGLE_API_TOKEN", raising=False)
        kaggle_dir = tmp_path / ".kaggle"
        kaggle_dir.mkdir(parents=True)
        (kaggle_dir / "access_token").write_text("KGAT_fake", encoding="utf-8")
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        import scripts.kaggle_run as kr

        monkeypatch.setattr(
            kr, "_kaggle", lambda *a, **k: subprocess.CompletedProcess([], 0, "", "")
        )
        assert kaggle_preflight() == []

    def test_kgat_env_var_is_accepted(self, monkeypatch, tmp_path: Path) -> None:
        monkeypatch.delenv("KAGGLE_USERNAME", raising=False)
        monkeypatch.delenv("KAGGLE_KEY", raising=False)
        monkeypatch.setenv("KAGGLE_API_TOKEN", "KGAT_fake")
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        import scripts.kaggle_run as kr

        monkeypatch.setattr(
            kr, "_kaggle", lambda *a, **k: subprocess.CompletedProcess([], 0, "", "")
        )
        assert kaggle_preflight() == []

    def test_kaggle_is_invoked_as_a_module(self, monkeypatch) -> None:
        """No PATH lookup: `python scripts/kaggle_run.py` outside an
        activated venv must still find the CLI. The command form is the
        contract — the CLI itself is a host-side tool, not a lockfile
        dependency, so this must not require kaggle to be installed."""
        import scripts.kaggle_run as kr

        seen: list[list[str]] = []

        def fake_run(cmd, *args, **kwargs):
            seen.append(cmd)
            return subprocess.CompletedProcess(cmd, 0, "", "")

        monkeypatch.setattr(kr.subprocess, "run", fake_run)
        kr._kaggle(["kernels", "status", "user/slug"])
        assert seen[0] == [sys.executable, "-m", "kaggle", "kernels", "status", "user/slug"]
