"""A --quick run must never overwrite a tracked manifest.

Found the hard way: `python -m src.experiments.exp6_capstone --quick` wrote
straight to `results/exp6_capstone.json`, replacing a tracked run's git sha,
device, torch version and interpreter version with the smoke run's — while
`portfolio/RESULTS.md` still cited that file as the record for the canonical
run. Every experiment's `main()` had the same shape. The resulting manifest
recorded `torch 2.12.1+cpu` and `python 3.14.7` for a run that had actually
used CUDA and 3.12 three weeks earlier, so the provenance the manifest exists
to carry was silently false.

`src.results.resolve_manifest_path` routes quick runs to
`results/probe_<experiment>_quick.json` instead. These tests pin the contract.
"""

from __future__ import annotations

from pathlib import Path

from src.results import resolve_manifest_path


def test_quick_run_never_writes_the_default_path() -> None:
    default = Path("results") / "exp1_induction_heads.json"
    assert resolve_manifest_path("exp1_induction_heads", default, None, quick=True) != default


def test_quick_run_lands_in_a_probe_path() -> None:
    path = resolve_manifest_path(
        "exp2_grokking", Path("results") / "exp2_grokking.json", None, quick=True
    )
    assert path == Path("results") / "probe_exp2_grokking_quick.json"


def test_canonical_run_uses_the_default_path() -> None:
    default = Path("results") / "exp3_superposition.json"
    assert resolve_manifest_path("exp3_superposition", default, None, quick=False) == default


def test_explicit_override_always_wins() -> None:
    """The retune A/B arms pass --manifest-path deliberately, quick or not."""
    override = "results/probe_capstone_ab_control.json"
    default = Path("results") / "exp2_grokking.json"
    assert (
        resolve_manifest_path("exp2_grokking", default, override, quick=False) == Path(override)
    )
    assert (
        resolve_manifest_path("exp2_grokking", default, override, quick=True) == Path(override)
    )


def test_quick_paths_are_distinct_per_experiment() -> None:
    """Two rungs must not share one scratch file and clobber each other."""
    a = resolve_manifest_path("exp1_induction_heads", Path("results/a.json"), None, quick=True)
    b = resolve_manifest_path("exp2_grokking", Path("results/b.json"), None, quick=True)
    assert a != b
