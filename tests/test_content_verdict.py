"""Tests for the pre-registered verdict of the content-based induction task.

Why this file exists
--------------------
The verdict of issue #200 used to live in a notebook cell, and the cell
read ``mean_path_patch_effect`` from the **exp1** manifest — a metric that
only the **exp4** manifest carries. The cell therefore raised ``KeyError``
on the first seed, after the GPU session had been spent and before the
manifests were zipped.

The test that pins that down is `test_the_path_patching_criterion_comes_from_the_exp4_manifest`:
it is the bug, frozen as a test. The rest of the file freezes the seven
criteria and the decision rule, so that a future change to the verdict has
to be a deliberate one.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.experiments.content_verdict import (
    CHECK_FAIL,
    CHECK_MISSING,
    CHECK_NOT_MEASURED,
    CHECK_PASS,
    CRITERIA,
    STATUS_COMPLETE,
    STATUS_INCOMPLETE,
    VERDICT_NEGATIVE,
    VERDICT_PARTIAL,
    VERDICT_POSITIVE,
    evaluate_seed,
    format_report,
    main,
    per_seed_metrics,
    run_verdict,
    run_verdicts,
    verdict_payload,
    write_verdict_json,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DERISK_MANIFEST = REPO_ROOT / "results/induction_content_derisk_standard.json"


def _exp1_metrics(**overrides: float) -> dict[str, float]:
    """A seed that meets every criterion but the causal one."""
    base = {
        "confirmed_content_mass": 0.45,
        "peak_content_mass": 0.45,
        "peak_offset_mass": 0.20,
        "copy_accuracy": 0.72,
        "copy_accuracy_nonmodal": 0.61,
        "fixed_offset_baseline": 0.18,
        "mean_copy_ablation_drop": 0.30,
        "total_induction_heads": 1.0,
    }
    base.update(overrides)
    return base


def _manifest(
    seeds: list[int],
    rows: list[dict[str, float]],
    task: str = "variable",
    **extra: object,
) -> dict:
    return {
        "experiment": "exp1_induction_heads",
        "seeds": seeds,
        "per_seed_metrics": rows,
        "args": {"task": task},
        **extra,
    }


class TestTheFrozenCriteria:
    def test_there_are_seven_criteria_in_the_frozen_order(self) -> None:
        assert [c.name for c in CRITERIA] == [
            "content mass",
            "content beats position",
            "copy accuracy",
            "non-modal accuracy",
            "beats fixed offset",
            "ablation drop",
            "path patching",
        ]

    def test_the_thresholds_are_the_frozen_ones(self) -> None:
        expressions = {c.name: c.expression for c in CRITERIA}
        assert expressions["content mass"] == "confirmed_content_mass >= 0.3"
        assert (
            expressions["content beats position"]
            == "confirmed_content_mass - peak_offset_mass >= 0.1"
        )
        assert expressions["copy accuracy"] == "copy_accuracy >= 0.6"
        assert expressions["non-modal accuracy"] == "copy_accuracy_nonmodal >= 0.5"
        assert expressions["beats fixed offset"] == "copy_accuracy - fixed_offset_baseline >= 0.2"
        assert expressions["ablation drop"] == "mean_copy_ablation_drop >= 0.1"
        assert expressions["path patching"] == "mean_path_patch_effect >= 0.2"

    def test_only_the_causal_criterion_comes_from_exp4(self) -> None:
        sources = {c.name: c.source for c in CRITERIA}
        assert sources["path patching"] == "exp4"
        assert all(source == "exp1" for name, source in sources.items() if name != "path patching")


class TestTheSeedVerdict:
    def test_a_seed_that_meets_every_criterion_is_positive(self) -> None:
        verdict = evaluate_seed(0, _exp1_metrics(), {"mean_path_patch_effect": 0.55})
        assert verdict.verdict == VERDICT_POSITIVE
        assert all(check.met for check in verdict.checks)

    def test_a_confirmed_head_with_a_failing_criterion_is_partial(self) -> None:
        verdict = evaluate_seed(0, _exp1_metrics(), {"mean_path_patch_effect": 0.05})
        assert verdict.verdict == VERDICT_PARTIAL
        assert "path patching" in verdict.failed

    def test_no_head_and_a_failing_criterion_is_negative(self) -> None:
        verdict = evaluate_seed(
            0,
            _exp1_metrics(total_induction_heads=0.0, copy_accuracy=0.10),
            {"mean_path_patch_effect": 0.0},
        )
        assert verdict.verdict == VERDICT_NEGATIVE

    def test_no_confirmed_head_makes_the_ablation_criterion_not_measured(self) -> None:
        metrics = _exp1_metrics(total_induction_heads=0.0)
        del metrics["mean_copy_ablation_drop"]
        verdict = evaluate_seed(0, metrics, {"mean_path_patch_effect": 0.5})
        check = next(c for c in verdict.checks if c.criterion.name == "ablation drop")
        assert check.status == CHECK_NOT_MEASURED
        assert verdict.complete
        assert verdict.verdict == VERDICT_NEGATIVE

    def test_an_old_placeholder_zero_is_not_a_measurement(self) -> None:
        # Manifests written before the fix carry 0.0 for the empty set.
        metrics = _exp1_metrics(total_induction_heads=0.0, mean_copy_ablation_drop=0.0)
        verdict = evaluate_seed(0, metrics, {"mean_path_patch_effect": 0.5})
        check = next(c for c in verdict.checks if c.criterion.name == "ablation drop")
        assert check.status == CHECK_NOT_MEASURED

    def test_a_confirmed_head_without_the_ablation_metric_is_incomplete(self) -> None:
        metrics = _exp1_metrics(total_induction_heads=1.0)
        del metrics["mean_copy_ablation_drop"]
        verdict = evaluate_seed(0, metrics, {"mean_path_patch_effect": 0.5})
        assert not verdict.complete
        assert "ablation drop" in verdict.missing

    def test_exp4_flag_says_path_patching_was_not_measured(self) -> None:
        # The de-risked expected outcome: 0 confirmed heads, 3 candidates.
        # exp4 omits the metric and writes path_patch_measured = 0; that is
        # NOT MEASURED, not a missing measurement and not a failed 0.0.
        verdict = evaluate_seed(
            0,
            _exp1_metrics(total_induction_heads=0.0),
            {
                "total_induction_heads": 0.0,
                "n_candidate_heads": 3.0,
                "path_patch_measured": 0.0,
            },
        )
        check = next(c for c in verdict.checks if c.criterion.name == "path patching")
        assert check.status == CHECK_NOT_MEASURED
        assert verdict.complete
        assert verdict.verdict == VERDICT_NEGATIVE

    def test_an_old_exp4_placeholder_zero_is_not_a_measurement(self) -> None:
        # Manifests written before the fix carry 0.0 and no flag. With no
        # confirmed head there was nothing to patch, so the 0.0 is a
        # placeholder, not a measured failure.
        verdict = evaluate_seed(
            0,
            _exp1_metrics(total_induction_heads=0.0),
            {"total_induction_heads": 0.0, "mean_path_patch_effect": 0.0},
        )
        check = next(c for c in verdict.checks if c.criterion.name == "path patching")
        assert check.status == CHECK_NOT_MEASURED

    def test_no_head_with_high_copy_and_low_content_is_negative_unexplained(self) -> None:
        # copy accuracy is high (0.72 >= 0.60) but content mass is low
        # (0.15 < 0.30), no head confirmed: the detector cannot explain the
        # copy — "NEGATIVE (unexplained)".
        verdict = evaluate_seed(
            0,
            _exp1_metrics(
                total_induction_heads=0.0,
                peak_content_mass=0.15,
                peak_offset_mass=0.33,
            ),
            None,
        )
        assert verdict.verdict == VERDICT_NEGATIVE

    def test_the_path_patching_criterion_comes_from_the_exp4_manifest(self) -> None:
        """The bug, frozen as a test.

        The exp1 manifest has never carried ``mean_path_patch_effect`` —
        that is exp4's metric — and the notebook used to read it from
        there, which is how the verdict of issue #200 died with a
        ``KeyError`` after the GPU session was spent.
        """
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3,
        }
        assert "mean_path_patch_effect" not in exp1["per_seed_metrics"][0]
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_COMPLETE
        assert result.verdict == VERDICT_POSITIVE

    def test_without_the_cascade_the_causal_criterion_is_not_measured(self) -> None:
        """A cascade that did not run is a failure, not a missing measurement."""
        verdict = evaluate_seed(0, _exp1_metrics(), None)
        assert "path patching" in verdict.not_measured
        assert verdict.missing == ()
        assert verdict.complete
        assert verdict.verdict == VERDICT_PARTIAL

    def test_a_manifest_without_the_content_fields_has_no_verdict(self) -> None:
        """A missing measurement is not a negative."""
        verdict = evaluate_seed(0, {"total_induction_heads": 1.0}, None)
        assert "content mass" in verdict.missing
        assert not verdict.complete
        assert verdict.verdict == ""

    def test_the_mechanism_report_does_not_change_the_verdict(self) -> None:
        """The mechanism report is secondary: it explains, it does not decide."""
        without = evaluate_seed(0, _exp1_metrics(), {"mean_path_patch_effect": 0.55})
        with_report = evaluate_seed(
            0,
            {**_exp1_metrics(), "group_ablation_drop": 0.9, "mechanism_kind": 2.0},
            {"mean_path_patch_effect": 0.55},
        )
        assert without.verdict == with_report.verdict == VERDICT_POSITIVE

    def test_criteria_1_and_2_read_the_confirmed_heads_mass(self) -> None:
        """The screen's peak is not the confirmed head's mass.

        A strong unconfirmed head must not carry criteria 1-2 for a weak
        confirmed one: the pre-registration says "content_mass of the
        confirmed head", and the screen's peak is a different number.
        """
        metrics = _exp1_metrics(
            confirmed_content_mass=0.20,
            peak_content_mass=0.95,
        )
        verdict = evaluate_seed(0, metrics, {"mean_path_patch_effect": 0.55})
        mass = next(c for c in verdict.checks if c.criterion.name == "content mass")
        beats = next(c for c in verdict.checks if c.criterion.name == "content beats position")
        assert mass.status == CHECK_FAIL
        assert beats.status == CHECK_FAIL
        assert verdict.verdict == VERDICT_PARTIAL

    def test_no_confirmed_head_leaves_the_content_criteria_not_measured(self) -> None:
        """Nothing confirmed means no confirmed-head mass — not a zero."""
        metrics = _exp1_metrics(total_induction_heads=0.0)
        del metrics["confirmed_content_mass"]
        verdict = evaluate_seed(0, metrics, None)
        statuses = {c.criterion.name: c.status for c in verdict.checks}
        assert statuses["content mass"] == CHECK_NOT_MEASURED
        assert statuses["content beats position"] == CHECK_NOT_MEASURED
        assert verdict.complete
        assert verdict.verdict == VERDICT_NEGATIVE


class TestTheDistributedNegative:
    """The 2026-10-25 de-risk shape: behavior solved, no head confirmed.

    The content verdict must describe the distributed circuit as a
    pre-specified secondary finding without changing the frozen NEGATIVE.
    """

    def _exp1_row(self, seed: int, **overrides: float) -> dict[str, float]:
        row = {
            "total_induction_heads": 0.0,
            "peak_content_mass": 0.9116,
            "peak_offset_mass": 0.1585,
            "copy_accuracy": 0.9993,
            "copy_accuracy_nonmodal": 0.9991,
            "fixed_offset_baseline": 0.1646,
            "n_candidate_heads": 3.0,
            "group_ablation_drop": 0.9956,
            "max_single_ablation_drop": 0.0986,
            "k_composition_score": 0.0918,
            "epochs_run": 3000.0,
        }
        row.update(overrides)
        return row

    def _exp4_row(self, seed: int, **overrides: float) -> dict[str, float]:
        row = {
            "total_induction_heads": 0.0,
            "path_patch_measured": 0.0,
            "checkpoint_epoch": 3000.0,
            "source_model_seed": float(seed),
            "counterfactual_minimal_pair": 1.0,
            "group_path_patch_effect": 0.87,
        }
        row.update(overrides)
        return row

    def _run(self, **exp1_overrides: float):
        seeds = [0, 1, 2]
        exp1 = _manifest(seeds, [self._exp1_row(seed, **exp1_overrides) for seed in seeds])
        exp4 = {
            "seeds": seeds,
            "per_seed_metrics": [self._exp4_row(seed) for seed in seeds],
        }
        return exp1, exp4, run_verdict(exp1, exp4)

    def test_the_frozen_verdict_is_negative(self) -> None:
        _exp1, _exp4, result = self._run()
        assert result.status == STATUS_COMPLETE
        assert result.verdict == VERDICT_NEGATIVE

    def test_the_report_names_the_distributed_circuit(self) -> None:
        exp1, exp4, result = self._run()
        report = format_report(result, per_seed_metrics(exp1), per_seed_metrics(exp4))
        assert "NEGATIVE (unexplained)" in report
        assert "distributed" in report
        assert "0.9956" in report
        assert "0.0986" in report
        assert "group path-patch effect" in report
        assert "0.8700" in report
        assert "secondary finding" in report

    def test_the_secondary_finding_does_not_change_the_label(self) -> None:
        _exp1, _exp4, result = self._run()
        assert result.verdict == VERDICT_NEGATIVE
        assert all(seed.verdict == VERDICT_NEGATIVE for seed in result.seeds)

    def test_a_low_content_mass_still_gets_the_detector_blind_spot_sentence(
        self,
    ) -> None:
        exp1, exp4, result = self._run(
            peak_content_mass=0.15,
            n_candidate_heads=0.0,
            group_ablation_drop=0.0,
            max_single_ablation_drop=0.0,
        )
        report = format_report(result, per_seed_metrics(exp1), per_seed_metrics(exp4))
        assert "NEGATIVE (unexplained)" in report
        assert "no head passes the content-mass screen" in report
        assert "distributed" not in report


class TestTheProvenanceRefusals:
    """A NEGATIVE is only about the pre-registered run.

    The same seven criteria applied to a periodic task, a dirty tree, or a
    cascade from another commit would attach the word NEGATIVE to a
    measurement that never answered the content question.
    """

    def test_a_periodic_manifest_gets_no_verdict(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3, task="periodic")
        result = run_verdict(exp1, None)
        assert result.status == STATUS_INCOMPLETE
        assert result.verdict == ""
        assert "periodic" in result.note

    def test_a_manifest_without_a_declared_task_gets_no_verdict(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        del exp1["args"]["task"]
        result = run_verdict(exp1, None)
        assert result.status == STATUS_INCOMPLETE
        assert "does not declare its task" in result.note

    def test_a_dirty_exp1_manifest_gets_no_verdict(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3, git_dirty=True)
        result = run_verdict(exp1, None)
        assert result.status == STATUS_INCOMPLETE
        assert "dirty working tree" in result.note

    def test_a_dirty_exp4_manifest_gets_no_verdict(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3,
            "git_dirty": True,
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert result.verdict == ""
        assert "dirty working tree" in result.note

    def test_a_cascade_from_another_commit_gets_no_verdict(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3, git_sha="aaaaaaa")
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3,
            "git_sha": "bbbbbbb",
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert "different commit" in result.note

    def test_exp4_can_name_an_abbreviated_source_commit(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3, git_sha="aaaaaaa")
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3,
            "git_sha": "aaaaaaabbbb",
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_COMPLETE

    def test_exp4_without_a_checkpoint_gets_no_verdict(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55, "checkpoint_epoch": -1.0}] * 3,
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert "did not analyse a checkpoint" in result.note

    def test_a_stale_checkpoint_is_not_the_final_model(self) -> None:
        rows = [_exp1_metrics(epochs_run=3000.0) for _ in range(3)]
        exp1 = _manifest([0, 1, 2], rows)
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55, "checkpoint_epoch": 2750.0}] * 3,
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert "checkpoint epoch 2750" in result.note
        assert "exp1 ran 3000 epochs" in result.note

    def test_a_cascade_on_another_model_seed_gets_no_verdict(self) -> None:
        rows = [_exp1_metrics(epochs_run=3000.0) for _ in range(3)]
        exp1 = _manifest([0, 1, 2], rows)
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [
                {
                    "mean_path_patch_effect": 0.55,
                    "checkpoint_epoch": 3000.0,
                    "source_model_seed": 1.0,
                }
            ]
            * 3,
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert "analysed model seed 1, not 0" in result.note

    def test_a_disjoint_counterfactual_gets_no_verdict(self) -> None:
        rows = [_exp1_metrics(epochs_run=3000.0) for _ in range(3)]
        exp1 = _manifest([0, 1, 2], rows)
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [
                {
                    "mean_path_patch_effect": 0.55,
                    "checkpoint_epoch": 3000.0,
                    "counterfactual_minimal_pair": 0.0,
                }
            ]
            * 3,
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert "disjoint counterfactual" in result.note

    def test_a_checkpoint_from_another_commit_gets_no_verdict(self) -> None:
        rows = [_exp1_metrics(epochs_run=3000.0) for _ in range(3)]
        exp1 = _manifest([0, 1, 2], rows, git_sha="aaaaaaa")
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [
                {
                    "mean_path_patch_effect": 0.55,
                    "checkpoint_epoch": 3000.0,
                    "source_model_seed": float(seed),
                }
                for seed in range(3)
            ],
            "git_sha": "aaaaaaa",
            "source_provenance": {
                "checkpoints": [
                    {"seed": seed, "git_sha": "bbbbbbb", "git_dirty": False} for seed in range(3)
                ]
            },
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert "trained at bbbbbbb" in result.note

    def test_a_dirty_checkpoint_gets_no_verdict(self) -> None:
        rows = [_exp1_metrics(epochs_run=3000.0) for _ in range(3)]
        exp1 = _manifest([0, 1, 2], rows, git_sha="aaaaaaa")
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [
                {
                    "mean_path_patch_effect": 0.55,
                    "checkpoint_epoch": 3000.0,
                    "source_model_seed": float(seed),
                }
                for seed in range(3)
            ],
            "git_sha": "aaaaaaa",
            "source_provenance": {
                "checkpoints": [
                    {"seed": seed, "git_sha": "aaaaaaa", "git_dirty": True} for seed in range(3)
                ]
            },
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert "dirty working tree" in result.note


class TestTheRunVerdict:
    def test_a_majority_of_positive_seeds_is_a_positive_run(self) -> None:
        exp1 = _manifest(
            [0, 1, 2],
            [
                _exp1_metrics(),
                _exp1_metrics(),
                _exp1_metrics(copy_accuracy=0.10, total_induction_heads=0.0),
            ],
        )
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3,
        }
        result = run_verdict(exp1, exp4)
        assert result.verdict == VERDICT_POSITIVE

    def test_one_positive_seed_of_three_is_not_a_positive_run(self) -> None:
        exp1 = _manifest(
            [0, 1, 2],
            [
                _exp1_metrics(),
                _exp1_metrics(copy_accuracy=0.10, total_induction_heads=0.0),
                _exp1_metrics(copy_accuracy=0.10, total_induction_heads=0.0),
            ],
        )
        exp4 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3,
        }
        result = run_verdict(exp1, exp4)
        assert result.verdict != VERDICT_POSITIVE

    def test_an_incomplete_seed_stops_the_run_verdict(self) -> None:
        exp1 = _manifest(
            [0, 1, 2],
            [_exp1_metrics(), _exp1_metrics(), {"total_induction_heads": 1.0}],
        )
        result = run_verdict(exp1, None)
        assert result.status == STATUS_INCOMPLETE
        assert result.verdict == ""

    def test_an_empty_manifest_is_incomplete_not_a_negative(self) -> None:
        result = run_verdict({"seeds": [], "per_seed_metrics": []}, None)
        assert result.status == STATUS_INCOMPLETE
        assert result.verdict == ""
        report = format_report(result, {})
        assert "NEGATIVE (unexplained)" not in report
        assert "no seeds" in report

    def test_partial_with_only_a_not_measured_criterion_says_so(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        result = run_verdict(exp1, None)
        report = format_report(result, per_seed_metrics(exp1))
        assert "Not measured: path patching." in report
        assert "Failing criteria: ." not in report

    def test_a_truncated_exp4_manifest_is_incomplete(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        exp4 = {
            "seeds": [0, 1],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 2,
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert "missing [2]" in result.note

    def test_a_single_seed_is_a_pilot_not_a_positive_run(self) -> None:
        exp1 = _manifest([0], [_exp1_metrics()])
        exp4 = {
            "seeds": [0],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}],
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert result.verdict == ""
        assert "pre-registered seeds" in result.note
        assert "missing [1, 2]" in result.note

    def test_four_seeds_are_not_the_pre_registered_run(self) -> None:
        exp1 = _manifest([0, 1, 2, 3], [_exp1_metrics()] * 4)
        exp4 = {
            "seeds": [0, 1, 2, 3],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 4,
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert result.verdict == ""
        assert "unexpected [3]" in result.note

    def test_unexpected_seed_ids_are_not_the_pre_registered_run(self) -> None:
        exp1 = _manifest([5, 6, 7], [_exp1_metrics()] * 3)
        result = run_verdict(exp1, None)
        assert result.status == STATUS_INCOMPLETE
        assert result.verdict == ""
        assert "missing [0, 1, 2]" in result.note

    def test_more_declared_seeds_than_rows_is_incomplete(self) -> None:
        # `per_seed_metrics` zips the lists, so a declared fourth seed with
        # only three rows used to be truncated away before the set check.
        exp1 = {
            "seeds": [0, 1, 2, 3],
            "per_seed_metrics": [_exp1_metrics()] * 3,
        }
        result = run_verdict(exp1, None)
        assert result.status == STATUS_INCOMPLETE
        assert "declares 4 seed(s) but carries 3 metric row(s)" in result.note

    def test_more_rows_than_declared_seeds_is_incomplete(self) -> None:
        exp1 = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [_exp1_metrics()] * 4,
        }
        result = run_verdict(exp1, None)
        assert result.status == STATUS_INCOMPLETE
        assert "declares 3 seed(s) but carries 4 metric row(s)" in result.note

    def test_duplicate_seed_ids_are_incomplete(self) -> None:
        exp1 = {
            "seeds": [0, 1, 2, 2],
            "per_seed_metrics": [_exp1_metrics()] * 4,
        }
        result = run_verdict(exp1, None)
        assert result.status == STATUS_INCOMPLETE
        assert "duplicate seed(s)" in result.note

    def test_exp4_with_an_extra_seed_is_incomplete(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        exp4 = {
            "seeds": [0, 1, 2, 3],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 4,
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert "unexpected [3]" in result.note

    def test_non_integer_seed_ids_are_incomplete(self) -> None:
        # 1.5, True and "1" all coerce to pre-registered IDs under int();
        # a manifest must name the seeds as integers.
        for bad in (1.5, True, "1"):
            exp1 = {
                "seeds": [0, bad, 2],
                "per_seed_metrics": [_exp1_metrics()] * 3,
            }
            result = run_verdict(exp1, None)
            assert result.status == STATUS_INCOMPLETE
            assert "non-integer seed" in result.note

    def test_a_manifest_without_the_head_count_is_incomplete(self) -> None:
        # The head count decides whether criterion 6 is measurable. Absent,
        # it must not be read as "0 confirmed" and turned into a negative.
        rows = [_exp1_metrics() for _ in range(3)]
        for row in rows:
            del row["total_induction_heads"]
        exp1 = _manifest([0, 1, 2], rows)
        result = run_verdict(exp1, None)
        assert result.status == STATUS_INCOMPLETE
        assert result.verdict == ""
        assert "total_induction_heads" in result.note
        report = format_report(result, per_seed_metrics(exp1))
        assert "heads=?" in report
        assert "RUN VERDICT" not in report


class TestTheDeRiskManifestReadsNotMeasured:
    """The tracked CPU de-risk manifest is a seed-0 pilot (600 epochs /
    2048 samples vs the pre-registered 3000 / 8192) that never ran the
    exp4 cascade. Its causal criterion must read NOT MEASURED, and the
    head-level criteria must read NOT MEASURED because no head was
    confirmed - never a fabricated measured zero.

    The manifest itself is kept with its documented placeholder zeros and
    is deliberately not regenerated (see the 2026-11-04 hardening note).
    """

    @pytest.fixture
    def derisk(self) -> dict:
        assert DERISK_MANIFEST.is_file(), DERISK_MANIFEST
        return json.loads(DERISK_MANIFEST.read_text(encoding="utf-8"))

    def test_seed_zero_is_a_pilot_not_the_run(self, derisk: dict) -> None:
        result = run_verdict(derisk, None)
        assert result.status == STATUS_INCOMPLETE
        assert result.verdict == ""
        assert "missing [1, 2]" in result.note

    def test_no_cascade_means_path_patching_is_not_measured(
        self, derisk: dict
    ) -> None:
        row = per_seed_metrics(derisk)[0]
        seed = evaluate_seed(0, row, None)
        path_patch = next(c for c in seed.checks if c.criterion.name == "path patching")
        assert path_patch.status == CHECK_NOT_MEASURED

    def test_no_confirmed_head_means_head_criteria_are_not_measured(
        self, derisk: dict
    ) -> None:
        row = per_seed_metrics(derisk)[0]
        seed = evaluate_seed(0, row, None)
        assert seed.confirmed_heads == 0
        for name in ("content mass", "content beats position", "ablation drop"):
            check = next(c for c in seed.checks if c.criterion.name == name)
            assert check.status == CHECK_NOT_MEASURED, name

    def test_measured_copy_criteria_still_pass(self, derisk: dict) -> None:
        row = per_seed_metrics(derisk)[0]
        seed = evaluate_seed(0, row, None)
        for name in ("copy accuracy", "non-modal accuracy", "beats fixed offset"):
            check = next(c for c in seed.checks if c.criterion.name == name)
            assert check.status == CHECK_PASS, name


class TestTheTwoVerdicts:
    """The pre-registered verdict and the causal addendum are two verdicts.

    Why they are two (2026-11-11): the content task's training run was
    pinned at commit ``88147ee``; the cascade that measures criterion 7 was
    executed **afterwards**, at ``891ef46``. The pre-registration's decision
    rule was applied to the run as it was launched — the ledger says so, in
    the same words: criterion 7 was a post-hoc addendum. So the record has
    two verdicts: the pre-registered one (criterion 7 NOT MEASURED) and the
    causal addendum (criterion 7 measured, with the commit difference
    declared). Merging them would hide which instrument produced which label
    — and the merged version is what made ``make content-verdict`` refuse to
    compute anything at all.
    """

    def test_the_pre_registered_verdict_ignores_the_cascade(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        exp4 = {"seeds": [0, 1, 2], "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3}
        bundle = run_verdicts(exp1, exp4)
        assert bundle.pre_registered.verdict == VERDICT_PARTIAL
        assert bundle.addendum is not None
        assert bundle.addendum.verdict == VERDICT_POSITIVE

    def test_the_pre_registered_verdict_has_criterion_7_not_measured(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        exp4 = {"seeds": [0, 1, 2], "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3}
        bundle = run_verdicts(exp1, exp4)
        seed0 = bundle.pre_registered.seeds[0]
        assert "path patching" in seed0.not_measured
        assert "path patching" not in seed0.failed

    def test_without_a_cascade_there_is_no_addendum(self) -> None:
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        bundle = run_verdicts(exp1, None)
        assert bundle.addendum is None
        assert bundle.pre_registered.verdict == VERDICT_PARTIAL

    def test_a_cascade_at_a_later_commit_is_declared_not_refused(self) -> None:
        """The addendum's whole point: the cascade ran later, and that is a
        fact to declare, not a reason to refuse to compute anything."""
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3, git_sha="aaaaaaa")
        exp4 = {
            "seeds": [0, 1, 2],
            "git_sha": "bbbbbbb",
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3,
        }
        bundle = run_verdicts(exp1, exp4)
        assert bundle.addendum is not None
        assert bundle.addendum.status == STATUS_COMPLETE
        assert bundle.addendum.verdict == VERDICT_POSITIVE
        assert bundle.addendum.provenance["exp1_git_sha"] == "aaaaaaa"
        assert bundle.addendum.provenance["exp4_git_sha"] == "bbbbbbb"
        assert bundle.addendum.provenance["declared"] is True

    def test_the_strict_verdict_still_refuses_a_cascade_from_another_commit(self) -> None:
        """The refusal is not deleted — it is only *not* the addendum's mode."""
        exp1 = _manifest([0, 1, 2], [_exp1_metrics()] * 3, git_sha="aaaaaaa")
        exp4 = {
            "seeds": [0, 1, 2],
            "git_sha": "bbbbbbb",
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3,
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert "different commit" in result.note

    def test_the_addendum_still_refuses_a_cascade_of_another_model(self) -> None:
        """Declaring the commit difference does not relax the *model* checks."""
        rows = [
            {
                "mean_path_patch_effect": 0.55,
                "path_patch_measured": 1.0,
                "source_model_seed": 0.0,
                "counterfactual_minimal_pair": 1.0,
                "checkpoint_epoch": 3000.0,
                "total_induction_heads": 1.0,
            }
            for _ in range(3)
        ]
        rows[1]["source_model_seed"] = 2.0  # seed 1 analysed the wrong model
        exp1 = _manifest(
            [0, 1, 2],
            [_exp1_metrics(), _exp1_metrics(), _exp1_metrics(epochs_run=3000.0)],
            git_sha="aaaaaaa",
        )
        exp4 = {"seeds": [0, 1, 2], "git_sha": "bbbbbbb", "per_seed_metrics": rows}
        bundle = run_verdicts(exp1, exp4)
        assert bundle.addendum is not None
        assert bundle.addendum.status == STATUS_INCOMPLETE
        assert "model seed" in bundle.addendum.note

    def test_the_artifact_carries_both_verdicts(self, tmp_path) -> None:
        exp1_path = tmp_path / "exp1.json"
        exp4_path = tmp_path / "exp4.json"
        exp1_path.write_text(
            json.dumps(_manifest([0, 1, 2], [_exp1_metrics()] * 3)), encoding="utf-8"
        )
        exp4_path.write_text(
            json.dumps(
                {"seeds": [0, 1, 2], "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3}
            ),
            encoding="utf-8",
        )
        out = tmp_path / "verdict.json"
        code = main(
            ["--exp1", str(exp1_path), "--exp4", str(exp4_path), "--output", str(out)]
        )
        assert code == 0
        payload = json.loads(out.read_text(encoding="utf-8"))
        assert payload["schema"] == "content-verdict/2"
        assert set(payload["verdicts"]) == {"pre_registered", "causal_addendum"}
        assert payload["verdicts"]["pre_registered"]["label"] == "pre_registered"
        assert payload["verdicts"]["causal_addendum"]["label"] == "causal_addendum"


class TestTheCommandLine:
    def _write(self, tmp_path, name, payload):
        path = tmp_path / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return str(path)

    def test_it_prints_the_verdict_and_exits_zero(self, tmp_path, capsys) -> None:
        exp1 = self._write(tmp_path, "exp1.json", _manifest([0, 1, 2], [_exp1_metrics()] * 3))
        exp4 = self._write(
            tmp_path,
            "exp4.json",
            {
                "seeds": [0, 1, 2],
                "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3,
            },
        )
        code = main(["--exp1", exp1, "--exp4", exp4])
        out = capsys.readouterr().out
        assert code == 0
        assert "RUN VERDICT: POSITIVE" in out
        assert "PASS" in out
        assert "path patching" in out

    def test_it_refuses_to_verdict_an_incomplete_manifest(self, tmp_path, capsys) -> None:
        exp1 = self._write(
            tmp_path,
            "exp1.json",
            _manifest(
                [0, 1, 2],
                [_exp1_metrics(), _exp1_metrics(), {"total_induction_heads": 1.0}],
            ),
        )
        code = main(["--exp1", exp1])
        out = capsys.readouterr().out
        assert code == 1
        assert STATUS_INCOMPLETE in out
        assert "No verdict is computed" in out

    def test_a_missing_exp4_manifest_is_a_warning_not_a_crash(self, tmp_path, capsys) -> None:
        exp1 = self._write(tmp_path, "exp1.json", _manifest([0, 1, 2], [_exp1_metrics()] * 3))
        code = main(["--exp1", exp1, "--exp4", str(tmp_path / "does-not-exist.json")])
        captured = capsys.readouterr()
        assert code == 0
        assert "does not exist" in captured.err
        assert "NOT MEASURED" in captured.out

    def test_it_warns_when_the_manifest_is_not_the_content_task(self, tmp_path, capsys) -> None:
        exp1 = self._write(
            tmp_path,
            "exp1.json",
            _manifest([0], [_exp1_metrics()], task="periodic"),
        )
        main(["--exp1", exp1])
        out = capsys.readouterr().out
        assert "WARNING" in out

    def test_the_json_report_carries_every_check(self, tmp_path, capsys) -> None:
        exp1 = self._write(tmp_path, "exp1.json", _manifest([0, 1, 2], [_exp1_metrics()] * 3))
        exp4 = self._write(
            tmp_path,
            "exp4.json",
            {
                "seeds": [0, 1, 2],
                "per_seed_metrics": [{"mean_path_patch_effect": 0.05}] * 3,
            },
        )
        main(["--exp1", exp1, "--exp4", exp4, "--json"])
        payload = json.loads(capsys.readouterr().out)
        assert payload["verdict"] == VERDICT_PARTIAL
        checks = payload["seeds"][0]["checks"]
        assert len(checks) == len(CRITERIA)
        assert {c["name"] for c in checks} == {c.name for c in CRITERIA}

    def test_it_writes_the_verdict_artifact(self, tmp_path) -> None:
        """The GPU session must save the verdict, not only print it."""
        exp1 = self._write(tmp_path, "exp1.json", _manifest([0, 1, 2], [_exp1_metrics()] * 3))
        exp4 = self._write(
            tmp_path,
            "exp4.json",
            {
                "seeds": [0, 1, 2],
                "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3,
            },
        )
        output = tmp_path / "content_verdict.json"
        code = main(["--exp1", exp1, "--exp4", exp4, "--output", str(output)])
        assert code == 0
        payload = json.loads(output.read_text(encoding="utf-8"))
        assert payload["schema"] == "content-verdict/2"
        assert payload["sources"]["exp1"] == exp1
        # The two verdicts are kept apart: the pre-registered one has no
        # cascade (criterion 7 was not part of that run), the addendum has it.
        assert payload["verdicts"]["pre_registered"]["verdict"] == VERDICT_PARTIAL
        assert payload["verdicts"]["causal_addendum"]["verdict"] == VERDICT_POSITIVE
        assert payload["seeds"][0]["mechanism"]["peak_content_mass"] == 0.45
        assert payload["seeds"][0]["cascade"]["mean_path_patch_effect"] == 0.55

    def test_the_payload_helper_and_the_cli_agree(self, tmp_path) -> None:
        exp1_payload = _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        exp4_payload = {
            "seeds": [0, 1, 2],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}] * 3,
        }
        result = run_verdict(exp1_payload, exp4_payload)
        payload = verdict_payload(
            result,
            per_seed_metrics(exp1_payload),
            per_seed_metrics(exp4_payload),
            "variable",
            {"exp1": "exp1.json", "exp4": "exp4.json"},
        )
        path = write_verdict_json(payload, tmp_path / "verdict.json")
        assert json.loads(path.read_text(encoding="utf-8")) == payload


class TestTheCheckStatuses:
    def test_the_three_states_are_distinguishable(self) -> None:
        verdict = evaluate_seed(0, _exp1_metrics(), None)
        statuses = {check.criterion.name: check.status for check in verdict.checks}
        assert statuses["copy accuracy"] == CHECK_PASS
        assert statuses["path patching"] == CHECK_NOT_MEASURED
        assert statuses["content mass"] != CHECK_MISSING

    def test_a_missing_metric_is_reported_as_missing(self) -> None:
        verdict = evaluate_seed(0, {"copy_accuracy": 0.9}, None)
        statuses = {check.criterion.name: check.status for check in verdict.checks}
        assert statuses["content mass"] == CHECK_MISSING
