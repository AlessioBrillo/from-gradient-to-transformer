"""Every remote GPU notebook must satisfy the remote-run contract.

The teaching artifact v22 rotted because nothing executed or checked it:
by the time anyone ran it, every code cell called an API that no longer
existed. The GPU notebooks here are not executable in CI (no GPU), but
they ARE checkable: modules must import, flags must exist in the parsers
they claim, manifests must route under results/, the download cell must
serve both runtimes, and a pinned BRANCH must be present so a remote
manifest names a real commit.

This is the same validation `scripts/kaggle_run.py --dry-run` runs before
spending GPU hours — a typo pushed to Kaggle burns a session to discover
a misspelled flag.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.kaggle_run import load_notebook, validate_notebook

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((REPO_ROOT / "notebooks").glob("kaggle_*.ipynb"))

pytestmark = pytest.mark.skipif(not NOTEBOOKS, reason="no kaggle notebooks found")


@pytest.fixture(scope="module")
def validation_results() -> dict[str, list[str]]:
    """Validate every remote notebook once, flags included (~10s each)."""
    return {nb.name: validate_notebook(load_notebook(nb)) for nb in NOTEBOOKS}


def test_notebooks_exist() -> None:
    assert NOTEBOOKS, "expected notebooks/kaggle_*.ipynb files to lint"


@pytest.mark.parametrize("name", [nb.name for nb in NOTEBOOKS])
def test_notebook_passes_the_contract(validation_results, name: str) -> None:
    problems = validation_results[name]
    assert problems == [], f"{name} violates the remote-run contract:\n" + "\n".join(
        f"  - {p}" for p in problems
    )


class TestValidateNotebook:
    """The lint rules themselves, on a synthetic notebook."""

    def _nb(self, *code_cells: str) -> dict:
        return {
            "cells": [
                {"cell_type": "code", "metadata": {}, "source": [src], "outputs": []}
                for src in code_cells
            ]
        }

    def test_missing_branch_assignment_is_a_problem(self) -> None:
        nb = self._nb("!uv run python -m src.experiments.exp1_induction_heads --seeds 0")
        assert any("BRANCH" in p for p in validate_notebook(nb, check_flags=False))

    def test_unknown_flag_is_caught(self) -> None:
        nb = self._nb(
            'BRANCH = "main"',
            "!uv run python -m src.experiments.exp2_grokking --protocol nanda "
            "--definitely-not-a-flag --manifest-path results/x.json",
        )
        problems = validate_notebook(nb)
        assert any("--definitely-not-a-flag" in p for p in problems)

    def test_a_module_that_cannot_be_introspected_says_so(self) -> None:
        """A dead `--help` is not a notebook full of unknown flags.

        The lint used to report "flag --x does not exist" for every flag of
        a module whose `--help` had produced no output — which is what a
        killed process (an out-of-memory kill on a loaded machine) looks
        like. The message has to name the process failure instead, or the
        reader goes looking for a typo that is not there.
        """
        nb = self._nb(
            'BRANCH = "main"',
            "!uv run python -m src.experiments.definitely_not_a_module --seeds 0",
        )
        problems = validate_notebook(nb)
        assert any(
            "does not import" in p or "--help` exited" in p for p in problems
        ), problems

    def test_manifest_path_must_live_under_results(self) -> None:
        nb = self._nb(
            'BRANCH = "main"',
            "!uv run python -m src.experiments.exp1_induction_heads "
            "--manifest-path /tmp/elsewhere.json",
        )
        problems = validate_notebook(nb, check_flags=False)
        assert any("--manifest-path" in p for p in problems)

    def test_colab_fallback_is_required(self) -> None:
        nb = self._nb('BRANCH = "main"', "print('hi')")
        problems = validate_notebook(nb, check_flags=False)
        assert any("google.colab" in p for p in problems)

    def test_absolute_host_path_is_caught(self) -> None:
        nb = self._nb(
            'BRANCH = "main"',
            "!uv run python -m src.experiments.exp1_induction_heads "
            "--manifest-path results/x.json  # C:\\Users\\me",
        )
        problems = validate_notebook(nb, check_flags=False)
        assert any("absolute host path" in p for p in problems)
