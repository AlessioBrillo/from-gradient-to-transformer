"""Execute the teaching artifact end to end.

`notebooks/capstone_teaching_artifact_v22.ipynb` was executed once, by hand, on
2026-09-08 against a historical code state, and was never re-validated. By the
time this test was written every one of its five code cells called an API that
no longer existed: `ckpt['config']`, `fourier_result['k_99']`,
`make_repeated_token_data(num_samples=...)` returning a dict,
`train_sae(steps=5000)`, and `run_activation_patching(...)` without its
required arguments. A notebook that is not executed by CI is a notebook that
rots.

This test runs v23 with `nbclient` and asserts on its outputs, so a future API
change breaks the build here rather than in front of a reader.
"""

from __future__ import annotations

from pathlib import Path

import pytest

nbformat = pytest.importorskip("nbformat")
nbclient = pytest.importorskip("nbclient")

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = REPO_ROOT / "notebooks" / "capstone_teaching_artifact_v23.ipynb"


@pytest.fixture(scope="module")
def executed_notebook():
    """Execute the notebook once; the CI job is the only consumer."""
    if not NOTEBOOK.exists():
        pytest.fail(f"teaching artifact missing: {NOTEBOOK}")
    nb = nbformat.read(NOTEBOOK, as_version=4)
    client = nbclient.NotebookClient(nb, timeout=600, kernel_name="python3")
    # The notebook chdirs itself when started from notebooks/, so cwd does not
    # matter; run it from the repo root regardless.
    client.execute(cwd=REPO_ROOT)
    return nb


def _stream_texts(nb) -> str:
    """Concatenate every stream output in the notebook."""
    chunks = []
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        for out in cell.get("outputs", []):
            if out.get("output_type") == "stream":
                chunks.append("".join(out.get("text", [])))
    return "\n".join(chunks)


def _errors(nb) -> list[str]:
    """Every error output, so a traceback is reported by name, not silently."""
    errs = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                errs.append(f"cell {i}: {out.get('ename')}: {out.get('evalue')}")
    return errs


def test_no_notebook_errors(executed_notebook) -> None:
    """Every cell must execute without raising."""
    assert _errors(executed_notebook) == []


def test_trains_and_reports_model_size(executed_notebook) -> None:
    text = _stream_texts(executed_notebook)
    assert "parameters, vocab=" in text, "the training cell never printed its model size"
    assert "metrics from a fresh run" in text


def test_fourier_sanity_check_passes(executed_notebook) -> None:
    """The planted frequency-3 neuron must resolve to k_99 <= 2.

    This is the same planted-construction check
    tests/test_grokking.py::TestFourierEnergySparsity uses. Without it, the
    notebook's k_99 printout is an unverifiable number — exactly the failure
    mode the 2026-10-08 audit was about, where a metric bug went unnoticed
    because nothing evaluated it on an input with a known answer.

    A pure real cosine at frequency 3 concentrates all its DFT energy in the
    conjugate pair {3, P-3}, so k_99 must be at most 2.
    """
    text = _stream_texts(executed_notebook)
    assert "planted frequency-3 neuron" in text
    import re

    m = re.search(r"planted frequency-3 neuron: k_99 = ([\d.]+) \(expect <= 2\)", text)
    assert m, f"could not parse the planted-frequency line:\n{text}"
    k99 = float(m.group(1))
    assert k99 <= 2, f"planted k_99 was {k99}, expected <= 2"


def test_detector_verdict_is_reported_either_way(executed_notebook) -> None:
    """The notebook must print one of the three explicit verdict lines.

    It must never silently skip detection: an absent verdict is the bug this
    guards against.
    """
    text = _stream_texts(executed_notebook)
    verdicts = (
        "K-comp is VACUOUS",
        "HEAD CONFIRMED",
        "NO HEAD confirmed at the 0.3 mass threshold",
    )
    assert any(v in text for v in verdicts), (
        f"no detector verdict printed. Output was:\n{text}"
    )


def test_sae_runs_on_real_activations(executed_notebook) -> None:
    text = _stream_texts(executed_notebook)
    assert "harvested" in text and "activations from" in text
    assert "FVE" in text
    assert "dead features" in text
