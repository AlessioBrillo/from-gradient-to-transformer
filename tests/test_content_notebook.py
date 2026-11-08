"""The content-task notebook must not rot again.

The 2026-10-22 audit found that the verdict of issue #200 could not be
computed at all: the notebook cell that checked the seven pre-registered
criteria read ``mean_path_patch_effect`` out of the **exp1** manifest, a
metric only the **exp4** manifest carries, so the cell raised ``KeyError``
on the first seed — after the GPU session had been spent, and before the
manifests were zipped.

These tests pin the properties that make the next session safe:

* the verdict comes from the tested module, not from a cell;
* the artifacts are zipped *before* the verdict, so a verdict that fails
  cannot cost the session;
* the cascade runs when the behaviour is content-based, not only when a
  per-head detector fires;
* the cascade is pinned to exp1's final epoch and commit, and the SAE to
  the model seed;
* the redundant emergence run is gone (2026-10-25 addendum), and the exp4
  printer tolerates the metrics that are deliberately not measured;
* the distributed circuit is reported as a secondary finding, not as a
  reason to move the frozen verdict (2026-11-01 addendum).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = REPO_ROOT / "notebooks" / "kaggle_induction_content.ipynb"


@pytest.fixture(scope="module")
def notebook() -> dict:
    if not NOTEBOOK.exists():  # pragma: no cover - the notebook is in the repo
        pytest.skip("the content-task notebook is not in the tree")
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))


def _code_cells(notebook: dict) -> list[str]:
    return [
        "".join(cell.get("source", [])) for cell in notebook["cells"] if cell["cell_type"] == "code"
    ]


def _all_text(notebook: dict) -> str:
    return "\n".join("".join(cell.get("source", "")) for cell in notebook["cells"])


class TestTheVerdict:
    def test_the_criteria_are_not_written_out_in_the_notebook(self) -> None:
        """They live in `src.experiments.content_verdict`, which is tested."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "CRITERIA = [" not in text
        assert 'mean_path_patch_effect"] >= 0.20' not in text

    def test_the_verdict_comes_from_the_module(self) -> None:
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "from src.experiments.content_verdict import" in text
        assert "run_verdict" in text

    def test_the_cascade_numbers_are_read_from_the_exp4_manifest(self) -> None:
        """The exp1 manifest never carried them: that was the KeyError."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "results/exp4_content.json" in text
        assert "m_exp4" in text

    def test_the_report_is_given_the_exp4_rows_too(self) -> None:
        """The distributed paragraph needs the group path-patch effect."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "format_report(result, exp1_rows, exp4_rows)" in text

    def test_the_verdict_is_saved_next_to_the_manifests(self) -> None:
        """The GPU session must save the decision, not only print it."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "verdict_payload(" in text
        assert "write_verdict_json(" in text
        assert "results/content_verdict.json" in text


class TestTheOrder:
    def test_the_zip_comes_before_the_verdict(self) -> None:
        """A verdict that crashes must not cost the session."""
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        sources = ["".join(cell.get("source", "")) for cell in notebook["cells"]]
        zip_at = next(i for i, s in enumerate(sources) if "induction_content_results.zip" in s)
        verdict_at = next(i for i, s in enumerate(sources) if "full = report(" in s)
        assert zip_at < verdict_at

    def test_the_download_serves_both_runtimes(self) -> None:
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "google.colab" in text
        assert "/kaggle/working" in text


class TestTheRun:
    def test_the_cascade_runs_on_the_behaviour_too(self) -> None:
        """A distributed copy is invisible to the per-head screen."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "BEHAVIOUR_IS_CONTENT" in text
        assert "if BEHAVIOUR_IS_CONTENT or FOUND_HEAD:" in text

    def test_the_sae_falls_back_to_the_content_based_seed(self) -> None:
        """Skipping Rung 5 when no head is confirmed would discard the very
        model that shows the distributed circuit."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "def seed_for_cascade" in text
        assert "distributed content circuit" in text

    def test_the_cascade_checks_exp1s_epoch_and_commit(self) -> None:
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "--source-epochs {EXP1_EPOCHS}" in text
        assert "--source-git-sha {EXP1_SHA}" in text
        assert 'EXP1_SHA = m_full["git_sha"]' in text

    def test_the_sae_names_the_model_seed_separately(self) -> None:
        """The SAE seed varies the dictionary; the model seed picks the weights."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "--source-model-seed {seed}" in text

    def test_the_sae_pins_exp1_epoch_and_commit(self) -> None:
        """exp5 deve rifiutare uno checkpoint da un'altra epoca/commit: passa
        --source-epochs e --source-git-sha presi dal manifesto di exp1."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "--source-epochs {EXP1_EPOCHS}" in text
        assert "--source-git-sha {EXP1_SHA}" in text

    def test_it_refuses_a_stale_or_dirty_clone(self) -> None:
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "the clone is dirty" in text
        assert "source_epochs == 1" in text
        assert "source_model_seed == 0" in text

    def test_the_emergence_run_is_not_in_the_protocol(self) -> None:
        """The 2026-10-25 addendum removed it: `confirmed_epoch` is recorded
        by the full-budget run, and a second early-stopped run only doubled
        the GPU budget."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "induction_content_emergence" not in text
        assert "--stop-on-confirmed" not in text

    def test_the_seeds_variable_is_defined_before_the_first_run(self) -> None:
        """Deleting the emergence cell also deleted the only `SEEDS`
        definition, and every command below uses `$SEEDS`: the first run
        would have failed before training."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert 'os.environ["SEEDS"] = "0,1,2"' in text
        assert text.index('os.environ["SEEDS"]') < text.index("--seeds $SEEDS")

    def test_the_exp4_printer_tolerates_unmeasured_metrics(self) -> None:
        """No fabricated 0.0: absent path-patch metrics print 'not measured'."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "_fmt(metrics, 'mean_path_patch_effect')" in text
        assert "not measured" in text

    def test_the_config_is_the_content_standard(self) -> None:
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "--content-standard" in text
        assert "--vocab-size 256" in text
        assert "--vocab-size 2048" not in text

    def test_the_counterfactual_is_the_minimal_pair(self) -> None:
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "--counterfactual minimal-pair" in text

    def test_the_recovery_manifests_are_zipped(self) -> None:
        """A dead session must keep the seeds it finished."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "per-seed recovery manifests" in text
        assert "merge_manifests" in text


class TestTheReporting:
    def test_pinning_names_only_the_records(self) -> None:
        """The per-seed files and the verdict JSON are not evidence."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "pin_remote_run.py --from <dir> --only" in text
        assert "content_verdict.json" in text

    def test_the_distributed_circuit_does_not_move_the_headline(self) -> None:
        """The 2026-11-01 addendum: seven criteria decide; the circuit explains."""
        text = _all_text(json.loads(NOTEBOOK.read_text(encoding="utf-8")))
        assert "do not change the headline" in text
        assert "secondary finding" in text
        assert 'change the headline from "a head" to "a circuit"' not in text
