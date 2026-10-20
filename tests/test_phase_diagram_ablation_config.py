"""The pre-registered protocol ablation of issue #168, pinned.

Why this file exists
--------------------
Issue #168 pre-registered a ten-cell protocol ablation: the Nanda-faithful
baseline plus exactly one deviation per cell, three seeds each, 20k
optimizer steps each, classified as SPARSE (3/3), MIXED (1-2/3) or DENSE
(0/3) with the per-seed count always reported.

The runner's *default* configuration was a different, larger sweep (43
cells across a P-sweep). Nothing was wrong with either file; the danger
was that a bare `python scripts/phase_diagram_sweep.py` would have run
five times the experiment that was pre-registered, and that the README's
"ten cells" and the runner's default would have disagreed in a way nobody
would have noticed until the manifests were on disk.

These tests pin the pre-registration itself, so a change to the design has
to be a visible change to a test, not a silent edit of a YAML file.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

from scripts.phase_diagram_sweep import SweepCell, generate_sweep_grid

REPO_ROOT = Path(__file__).resolve().parents[1]
ABLATION_CONFIG = REPO_ROOT / "configs" / "phase_diagram_ablation.yaml"
LEGACY_SWEEP_CONFIG = REPO_ROOT / "configs" / "phase_diagram_sweep.yaml"

# The deviations the ablation is allowed to switch on, one per cell. Some
# deviations need two keys to express (minibatch is "not full batch" *and*
# "a batch size"), so the check is on groups, not on keys.
DEVIATION_GROUPS = (
    ("batch_size", "full_batch"),
    ("beta2",),
    ("schedule",),
    ("normalize_embeddings",),
    ("layernorm",),
    ("grad_clip",),
)


def _cells() -> list[dict]:
    config = yaml.safe_load(ABLATION_CONFIG.read_text(encoding="utf-8"))
    return config["cells"]


class TestPreRegisteredDesign:
    def test_the_ablation_has_ten_cells(self) -> None:
        assert len(_cells()) == 10

    def test_every_cell_runs_20k_steps(self) -> None:
        for cell in _cells():
            assert cell.get("steps") == 20000, cell["cell_id"]

    def test_every_cell_is_a_p113_solo_nanda_cell(self) -> None:
        for cell in _cells():
            assert cell["modulus"] == 113, cell["cell_id"]
            assert cell["mode"] == "solo", cell["cell_id"]
            assert cell["protocol"] == "nanda", cell["cell_id"]
            assert cell["d_model"] == 128 and cell["d_mlp"] == 512, cell["cell_id"]
            assert cell["n_layers"] == 1 and cell["n_heads"] == 4, cell["cell_id"]

    def test_every_cell_switches_on_at_most_one_deviation(self) -> None:
        """The design contract: baseline plus *exactly one* deviation.

        The weight-decay axis is not a deviation (it is an axis), so the
        cells that only change the weight decay are allowed to carry no
        deviation key at all.
        """
        for cell in _cells():
            deviations = [
                group
                for group in DEVIATION_GROUPS
                if any(key in cell for key in group)
            ]
            assert len(deviations) <= 1, (cell["cell_id"], deviations)

    def test_the_weight_decay_axis_is_present(self) -> None:
        decays = sorted(c["weight_decay"] for c in _cells())
        assert decays == [0.1, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0]

    def test_the_cell_ids_are_unique(self) -> None:
        ids = [c["cell_id"] for c in _cells()]
        assert len(set(ids)) == len(ids)

    def test_the_runner_reads_this_config_into_the_same_cells(self) -> None:
        config = yaml.safe_load(ABLATION_CONFIG.read_text(encoding="utf-8"))
        cells = generate_sweep_grid(config)
        assert len(cells) == 10
        assert all(isinstance(c, SweepCell) for c in cells)
        assert {c.steps for c in cells} == {20000}

    def test_the_legacy_sweep_is_a_different_and_larger_design(self) -> None:
        """The two configs must not be confused for one another."""
        legacy = yaml.safe_load(LEGACY_SWEEP_CONFIG.read_text(encoding="utf-8"))
        assert len(legacy["cells"]) != len(_cells())
        assert len(legacy["cells"]) > len(_cells())


class TestDefaultConfiguration:
    def test_the_default_is_the_pre_registered_ablation(self) -> None:
        """A bare invocation must run the experiment that was pre-registered."""
        from scripts.phase_diagram_sweep import build_parser

        args = build_parser().parse_args([])
        assert args.config == "configs/phase_diagram_ablation.yaml"
        assert (REPO_ROOT / args.config).is_file()

    def test_the_help_names_the_legacy_sweep_as_explicit(self) -> None:
        out = subprocess.run(
            [sys.executable, "scripts/phase_diagram_sweep.py", "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        assert "configs/phase_diagram_ablation.yaml" in out
        assert "configs/phase_diagram_sweep.yaml" in out
