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

from src.experiments.content_verdict import (
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
)


def _exp1_metrics(**overrides: float) -> dict[str, float]:
    """A seed that meets every criterion but the causal one."""
    base = {
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
) -> dict:
    return {
        "experiment": "exp1_induction_heads",
        "seeds": seeds,
        "per_seed_metrics": rows,
        "args": {"task": task},
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
        assert expressions["content mass"] == "peak_content_mass >= 0.3"
        assert (
            expressions["content beats position"]
            == "peak_content_mass - peak_offset_mass >= 0.1"
        )
        assert expressions["copy accuracy"] == "copy_accuracy >= 0.6"
        assert expressions["non-modal accuracy"] == "copy_accuracy_nonmodal >= 0.5"
        assert (
            expressions["beats fixed offset"]
            == "copy_accuracy - fixed_offset_baseline >= 0.2"
        )
        assert expressions["ablation drop"] == "mean_copy_ablation_drop >= 0.1"
        assert expressions["path patching"] == "mean_path_patch_effect >= 0.2"

    def test_only_the_causal_criterion_comes_from_exp4(self) -> None:
        sources = {c.name: c.source for c in CRITERIA}
        assert sources["path patching"] == "exp4"
        assert all(
            source == "exp1" for name, source in sources.items() if name != "path patching"
        )


class TestTheSeedVerdict:
    def test_a_seed_that_meets_every_criterion_is_positive(self) -> None:
        verdict = evaluate_seed(
            0, _exp1_metrics(), {"mean_path_patch_effect": 0.55}
        )
        assert verdict.verdict == VERDICT_POSITIVE
        assert all(check.met for check in verdict.checks)

    def test_a_confirmed_head_with_a_failing_criterion_is_partial(self) -> None:
        verdict = evaluate_seed(
            0, _exp1_metrics(), {"mean_path_patch_effect": 0.05}
        )
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
        metrics = _exp1_metrics(
            total_induction_heads=0.0, mean_copy_ablation_drop=0.0
        )
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
        assert "missing seed(s)" in result.note

    def test_a_single_seed_is_a_pilot_not_a_positive_run(self) -> None:
        exp1 = _manifest([0], [_exp1_metrics()])
        exp4 = {
            "seeds": [0],
            "per_seed_metrics": [{"mean_path_patch_effect": 0.55}],
        }
        result = run_verdict(exp1, exp4)
        assert result.status == STATUS_INCOMPLETE
        assert result.verdict == ""
        assert "1 of 3" in result.note


class TestTheCommandLine:
    def _write(self, tmp_path, name, payload):
        path = tmp_path / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return str(path)

    def test_it_prints_the_verdict_and_exits_zero(self, tmp_path, capsys) -> None:
        exp1 = self._write(
            tmp_path, "exp1.json", _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        )
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

    def test_a_missing_exp4_manifest_is_a_warning_not_a_crash(
        self, tmp_path, capsys
    ) -> None:
        exp1 = self._write(
            tmp_path, "exp1.json", _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        )
        code = main(
            ["--exp1", exp1, "--exp4", str(tmp_path / "does-not-exist.json")]
        )
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
        exp1 = self._write(
            tmp_path, "exp1.json", _manifest([0, 1, 2], [_exp1_metrics()] * 3)
        )
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
