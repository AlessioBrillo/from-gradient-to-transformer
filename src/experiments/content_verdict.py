"""The pre-registered verdict of the content-based induction task (issue #200).

Why this module exists
----------------------
The verdict of issue #200 used to live *inside a notebook cell*, and the
notebook read a metric that the experiment it was reading does not produce:
criterion 7 (``mean_path_patch_effect``) lives in the **exp4** manifest, not
in the exp1 one, so the cell raised ``KeyError`` on the first seed — after
the GPU session had already been spent, and before the manifests were
zipped. The criteria were frozen in
`07_capstone/notes/variable-distance-induction-preregistration.md`; this
module is the single place where they live in code, so they cannot drift
from the pre-registration and so the verdict can be tested.

What the module decides
-----------------------
The **seven frozen criteria**, in the order they were frozen, evaluated per
seed and then for the run:

1. ``peak_content_mass`` >= 0.30 — some head puts a third of its attention
   mass on the content key.
2. ``peak_content_mass - peak_offset_mass`` >= 0.10 — and that mass beats
   the best fixed offset.
3. ``copy_accuracy`` >= 0.60 — the model copies on the copy queries.
4. ``copy_accuracy_nonmodal`` >= 0.50 — and it copies on the queries whose
   distance is *not* the modal one, where a fixed-offset head scores ~0.
5. ``copy_accuracy - fixed_offset_baseline`` >= 0.20 — and it beats the
   best single fixed offset.
6. ``mean_copy_ablation_drop`` >= 0.10 — removing a confirmed head costs
   the model its copy accuracy.
7. ``mean_path_patch_effect`` >= 0.20 — patching that head's direct
   contribution to the logits moves the answer with it. **This one is
   measured by exp4**, so it is read from the exp4 manifest.

The seed verdict is ``POSITIVE`` when all seven are met, ``PARTIAL`` when a
head is confirmed but the criteria are not all met, and ``NEGATIVE``
otherwise. The run verdict requires the pre-registered three seeds:
``POSITIVE`` when a majority of them are positive, ``PARTIAL`` when any seed
is partial, and ``NEGATIVE`` otherwise. Fewer seeds are a pilot, not the
run, and report ``INCOMPLETE``.

What the module refuses to do
-----------------------------
It never guesses. A criterion whose measurement is missing is reported as
missing, and a run whose manifest does not carry the measurement gets the
status ``INCOMPLETE`` and **no verdict** — "the model has no content-based
induction head" and "this manifest never measured one" are different
statements, and only the first is a scientific claim.

The secondary *mechanism report* (the circuit-level measurement of
`src/experiments/copy_circuit.py`) is printed next to the verdict and is
explicitly **not** part of it: the seven criteria decide, the mechanism
report explains.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from src.experiments.copy_circuit import classify_mechanism

VERDICT_POSITIVE = "POSITIVE"
VERDICT_PARTIAL = "PARTIAL"
VERDICT_NEGATIVE = "NEGATIVE"

STATUS_COMPLETE = "COMPLETE"
STATUS_INCOMPLETE = "INCOMPLETE"

CHECK_PASS = "PASS"
CHECK_FAIL = "FAIL"
CHECK_NOT_MEASURED = "NOT MEASURED"
CHECK_MISSING = "MISSING"

SOURCE_EXP1 = "exp1"
SOURCE_EXP4 = "exp4"


@dataclass(frozen=True)
class Criterion:
    """One frozen criterion.

    ``metric`` is the number the criterion reads. When ``other`` is set, the
    criterion reads the *difference* ``metric - other`` (the two contrasts
    the pre-registration names: content against the best fixed offset, and
    the copy accuracy against the fixed-offset baseline). ``source`` says
    which experiment measures it — criterion 7 is exp4's.
    """

    name: str
    metric: str
    threshold: float
    other: Optional[str] = None
    source: str = SOURCE_EXP1

    @property
    def expression(self) -> str:
        """The criterion as it reads in the pre-registration."""
        if self.other:
            return f"{self.metric} - {self.other} >= {self.threshold}"
        return f"{self.metric} >= {self.threshold}"


#: The seven criteria, frozen on 2026-10-20 and unchanged since.
CRITERIA: tuple[Criterion, ...] = (
    Criterion("content mass", "peak_content_mass", 0.30),
    Criterion("content beats position", "peak_content_mass", 0.10, other="peak_offset_mass"),
    Criterion("copy accuracy", "copy_accuracy", 0.60),
    Criterion("non-modal accuracy", "copy_accuracy_nonmodal", 0.50),
    Criterion("beats fixed offset", "copy_accuracy", 0.20, other="fixed_offset_baseline"),
    Criterion("ablation drop", "mean_copy_ablation_drop", 0.10),
    Criterion("path patching", "mean_path_patch_effect", 0.20, source=SOURCE_EXP4),
)


@dataclass(frozen=True)
class Check:
    """The outcome of one criterion for one seed."""

    criterion: Criterion
    value: Optional[float]
    status: str

    @property
    def met(self) -> bool:
        return self.status == CHECK_PASS

    @property
    def measured(self) -> bool:
        return self.status in (CHECK_PASS, CHECK_FAIL)


@dataclass(frozen=True)
class SeedVerdict:
    """The verdict of one seed, with the check that produced it."""

    seed: int
    checks: tuple[Check, ...]
    confirmed_heads: Optional[int]
    note: str = ""

    @property
    def missing(self) -> tuple[str, ...]:
        return tuple(c.criterion.name for c in self.checks if c.status == CHECK_MISSING)

    @property
    def not_measured(self) -> tuple[str, ...]:
        return tuple(
            c.criterion.name for c in self.checks if c.status == CHECK_NOT_MEASURED
        )

    @property
    def failed(self) -> tuple[str, ...]:
        return tuple(c.criterion.name for c in self.checks if c.status == CHECK_FAIL)

    @property
    def complete(self) -> bool:
        """Did every criterion get a number?

        A criterion that was *not measured* (the cascade did not run) is a
        legitimate absence — the pre-registered rule then fails that
        criterion. A criterion whose metric is *missing from the manifest*
        means the manifest never carried that measurement, and then no
        verdict can be computed at all. ``note`` carries the same refusal
        for a missing input that is not itself a criterion (the head count
        that decides whether criterion 6 is measurable).
        """
        return not self.missing and not self.note

    @property
    def verdict(self) -> str:
        """The frozen rule: POSITIVE / PARTIAL / NEGATIVE ("" when incomplete)."""
        if not self.complete:
            return ""
        if all(c.met for c in self.checks):
            return VERDICT_POSITIVE
        if (self.confirmed_heads or 0) > 0:
            return VERDICT_PARTIAL
        return VERDICT_NEGATIVE


@dataclass(frozen=True)
class RunVerdict:
    """The verdict of the run, and the per-seed verdicts behind it."""

    label: str
    seeds: tuple[SeedVerdict, ...]
    status: str
    verdict: str
    note: str = ""

    @property
    def complete(self) -> bool:
        return self.status == STATUS_COMPLETE


def _read_metric(metrics: Mapping[str, Any], name: str) -> Optional[float]:
    """The value of one metric of a manifest, or ``None`` when it is absent."""
    if name not in metrics:
        return None
    try:
        return float(metrics[name])
    except (TypeError, ValueError):  # pragma: no cover - manifests are numeric
        return None


def check_criterion(
    criterion: Criterion,
    metrics: Mapping[str, Any],
    not_measured_reason: Optional[str] = None,
) -> Check:
    """Evaluate one criterion against one seed's metrics.

    ``not_measured_reason`` is set when the measurement was deliberately not
    taken (for instance the cascade did not run, so there is no exp4
    manifest). The criterion then fails with that reason — it is *not* a
    missing metric, and it does not make the run incomplete.
    """
    value = _read_metric(metrics, criterion.metric)
    if value is None:
        if not_measured_reason is not None:
            return Check(criterion, None, CHECK_NOT_MEASURED)
        return Check(criterion, None, CHECK_MISSING)
    if criterion.other is not None:
        other = _read_metric(metrics, criterion.other)
        if other is None:
            if not_measured_reason is not None:
                return Check(criterion, None, CHECK_NOT_MEASURED)
            return Check(criterion, None, CHECK_MISSING)
        value = value - other
    status = CHECK_PASS if value >= criterion.threshold else CHECK_FAIL
    return Check(criterion, value, status)


def _exp4_criterion_not_measured(
    criterion: Criterion, metrics: Mapping[str, Any]
) -> bool:
    """True when exp4 recorded that this criterion was not measured.

    Path patching needs a confirmed head to patch. The new manifests write
    ``path_patch_measured = 0`` and omit ``mean_path_patch_effect``; older
    manifests carry a placeholder ``0.0`` and no flag, so a manifest with
    ``total_induction_heads == 0`` is read the same way. A 0.0 in either form
    is not a causal measurement.
    """
    if criterion.metric != "mean_path_patch_effect":
        return False
    measured = _read_metric(metrics, "path_patch_measured")
    if measured is not None:
        return measured == 0.0
    return _read_metric(metrics, "total_induction_heads") == 0.0


def evaluate_seed(
    seed: int,
    exp1_metrics: Mapping[str, Any],
    exp4_metrics: Optional[Mapping[str, Any]] = None,
    criteria: Sequence[Criterion] = CRITERIA,
) -> SeedVerdict:
    """The verdict of one seed, from the exp1 and exp4 metrics of that seed.

    ``exp4_metrics`` is ``None`` when the cascade did not run: criterion 7
    is then *not measured* (and fails, with the reason), which is different
    from a manifest that simply does not carry the metric.
    """
    confirmed: Optional[int] = None
    raw = exp1_metrics.get("total_induction_heads")
    if raw is not None:
        try:
            confirmed = int(float(raw))
        except (TypeError, ValueError):
            confirmed = None
    # The head count is the input that decides whether criterion 6 is
    # measurable at all. Without it, a fabricated 0.0 would read as "no head
    # confirmed" and the run would be reported as a negative it never
    # measured; the seed is incomplete instead.
    note = ""
    if confirmed is None:
        note = "the exp1 manifest does not carry a usable total_induction_heads"
    checks: list[Check] = []
    for criterion in criteria:
        if criterion.source == SOURCE_EXP4:
            if exp4_metrics is None or _exp4_criterion_not_measured(
                criterion, exp4_metrics
            ):
                checks.append(
                    Check(
                        criterion,
                        None,
                        CHECK_NOT_MEASURED,
                    )
                )
                continue
            checks.append(check_criterion(criterion, exp4_metrics))
            continue
        # Criterion 6 ablates a *confirmed* head. With none confirmed there is
        # nothing to remove, so the mean is undefined — not a measured zero.
        # This is the same distinction exp4 draws for path patching.
        if criterion.metric == "mean_copy_ablation_drop" and confirmed in (None, 0):
            checks.append(Check(criterion, None, CHECK_NOT_MEASURED))
            continue
        checks.append(check_criterion(criterion, exp1_metrics))
    return SeedVerdict(
        seed=seed, checks=tuple(checks), confirmed_heads=confirmed, note=note
    )


def load_manifest(path: str | Path) -> dict[str, Any]:
    """Read a manifest from disk."""
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):  # pragma: no cover - manifests are objects
        raise ValueError(f"{path} is not a manifest")
    return data


def per_seed_metrics(manifest: Mapping[str, Any]) -> dict[int, Mapping[str, Any]]:
    """The manifest's per-seed metrics, keyed by seed."""
    seeds = manifest.get("seeds", [])
    metrics = manifest.get("per_seed_metrics", [])
    out: dict[int, Mapping[str, Any]] = {}
    for seed, row in zip(seeds, metrics):
        out[int(seed)] = row
    return out


def _manifest_seed_problem(manifest: Mapping[str, Any], label: str) -> str:
    """Why the manifest's declared seeds cannot be trusted, or ``""``.

    ``per_seed_metrics`` zips the two lists, so a truncated, overlong or
    duplicated seed list would silently drop or collapse rows before any
    verdict is computed. Validate the raw lists first: the verdict must be
    about the manifest that exists, not the prefix ``zip`` kept.
    """
    seeds = manifest.get("seeds", [])
    rows = manifest.get("per_seed_metrics", [])
    if not isinstance(seeds, list) or not isinstance(rows, list):
        return f"{label} does not carry seed and metric lists"
    if len(seeds) != len(rows):
        return (
            f"{label} declares {len(seeds)} seed(s) but carries "
            f"{len(rows)} metric row(s)"
        )
    ids: list[int] = []
    for seed in seeds:
        # ``int()`` would coerce 1.5, True and "1" into the pre-registered
        # IDs; a manifest must name them as integers.
        if type(seed) is not int:
            return f"{label} carries a non-integer seed"
        ids.append(seed)
    if len(set(ids)) != len(ids):
        return f"{label} carries duplicate seed(s)"
    return ""


def run_verdict(
    exp1: Mapping[str, Any],
    exp4: Optional[Mapping[str, Any]] = None,
    criteria: Sequence[Criterion] = CRITERIA,
    expected_seeds: Sequence[int] = (0, 1, 2),
) -> RunVerdict:
    """The verdict of a run, from the exp1 manifest and (optionally) exp4's.

    The pre-registration fixes **three seeds, 0, 1 and 2**. A manifest that
    carries a different set is not the run: it gets ``INCOMPLETE`` and no
    verdict, so neither a one-seed pilot nor an extra seed can be reported
    as the pre-registered POSITIVE. An empty manifest is likewise
    ``INCOMPLETE`` rather than a vacuous negative.
    """
    exp1_problem = _manifest_seed_problem(exp1, "the exp1 manifest")
    if exp1_problem:
        return RunVerdict(
            label="run",
            seeds=(),
            status=STATUS_INCOMPLETE,
            verdict="",
            note=exp1_problem,
        )
    exp1_rows = per_seed_metrics(exp1)
    exp1_seeds = [int(s) for s in exp1.get("seeds", [])]
    exp4_rows: dict[int, Mapping[str, Any]] = {}
    if exp4 is not None:
        exp4_problem = _manifest_seed_problem(exp4, "the exp4 manifest")
        if exp4_problem:
            return RunVerdict(
                label="run",
                seeds=(),
                status=STATUS_INCOMPLETE,
                verdict="",
                note=exp4_problem,
            )
        exp4_seeds = [int(s) for s in exp4.get("seeds", [])]
        missing_exp4 = sorted(set(exp1_seeds) - set(exp4_seeds))
        extra_exp4 = sorted(set(exp4_seeds) - set(exp1_seeds))
        if missing_exp4 or extra_exp4:
            parts = []
            if missing_exp4:
                parts.append(f"missing {missing_exp4}")
            if extra_exp4:
                parts.append(f"unexpected {extra_exp4}")
            return RunVerdict(
                label="run",
                seeds=(),
                status=STATUS_INCOMPLETE,
                verdict="",
                note=(
                    "the exp4 manifest does not carry the exp1 seeds "
                    f"({'; '.join(parts)}); a cascade that did not analyse "
                    "a seed did not measure it"
                ),
            )
        exp4_rows = per_seed_metrics(exp4)
    seeds: list[SeedVerdict] = []
    for seed in sorted(exp1_rows):
        seeds.append(
            evaluate_seed(seed, exp1_rows[seed], exp4_rows.get(seed), criteria)
        )
    if not exp1_seeds:
        return RunVerdict(
            label="run",
            seeds=(),
            status=STATUS_INCOMPLETE,
            verdict="",
            note="the exp1 manifest carries no seeds",
        )
    expected = set(expected_seeds)
    if set(exp1_seeds) != expected:
        missing = sorted(expected - set(exp1_seeds))
        extra = sorted(set(exp1_seeds) - expected)
        parts = []
        if missing:
            parts.append(f"missing {missing}")
        if extra:
            parts.append(f"unexpected {extra}")
        return RunVerdict(
            label="run",
            seeds=tuple(seeds),
            status=STATUS_INCOMPLETE,
            verdict="",
            note=(
                "the exp1 manifest does not carry the pre-registered seeds "
                f"{sorted(expected)} ({'; '.join(parts)})"
            ),
        )
    incomplete = [s for s in seeds if not s.complete]
    if incomplete:
        missing_measurements = sorted(
            {name for s in incomplete for name in s.missing}
        )
        notes = sorted({s.note for s in incomplete if s.note})
        parts = []
        if missing_measurements:
            parts.append(
                f"missing measurements: {', '.join(missing_measurements)}"
            )
        if notes:
            parts.append("; ".join(notes))
        return RunVerdict(
            label="run",
            seeds=tuple(seeds),
            status=STATUS_INCOMPLETE,
            verdict="",
            note="; ".join(parts),
        )
    verdicts = [s.verdict for s in seeds]
    n_positive = verdicts.count(VERDICT_POSITIVE)
    if n_positive * 2 > len(verdicts):
        overall = VERDICT_POSITIVE
    elif VERDICT_PARTIAL in verdicts:
        overall = VERDICT_PARTIAL
    else:
        overall = VERDICT_NEGATIVE
    return RunVerdict(
        label="run",
        seeds=tuple(seeds),
        status=STATUS_COMPLETE,
        verdict=overall,
    )


def mechanism_report(metrics: Mapping[str, Any]) -> tuple[str, str]:
    """The secondary mechanism report of one seed.

    Returns ``(code, label)``. The code is the number the manifest carries
    (``mechanism_kind``); the label is decoded from it. When the manifest
    has no mechanism fields at all, the report says so instead of guessing.
    """
    if "group_ablation_drop" not in metrics:
        return "", "not measured (this manifest carries no mechanism report)"
    code, label = classify_mechanism({k: float(v) for k, v in metrics.items()})
    return str(code), label


# ---------------------------------------------------------------------------
# The printed report
# ---------------------------------------------------------------------------
def format_seed(seed: SeedVerdict) -> str:
    """The one-line summary of a seed."""
    heads = "?" if seed.confirmed_heads is None else seed.confirmed_heads
    parts = [
        f"seed {seed.seed}: {seed.verdict or 'NO VERDICT'}",
        f"| heads={heads}",
    ]
    for check in seed.checks:
        if check.value is None:
            continue
        parts.append(f"| {check.criterion.name}={check.value:.4f}")
    return " ".join(parts)


def format_report(
    result: RunVerdict,
    exp1_rows: Mapping[int, Mapping[str, Any]],
) -> str:
    """The full, printable report of a run."""
    lines: list[str] = []
    for seed in result.seeds:
        lines.append(format_seed(seed))
        for check in seed.checks:
            detail = check.criterion.expression
            if check.value is not None:
                detail += f" -> {check.value:.4f}"
            lines.append(f"    {check.status:<13} {check.criterion.name} ({detail})")
        row = exp1_rows.get(seed.seed, {})
        code, label = mechanism_report(row)
        if code:
            lines.append(f"    mechanism    {label} (code {code})")
        # Aggregate mechanism numbers — printed next to the verdict so the
        # report is self-contained and no one has to open the manifest.
        mech_keys = [
            "content_mass_total",
            "content_chance_mass",
            "content_mass_excess",
            "content_mass_ratio",
            "content_mass_top_share",
            "content_mass_heads_for_80pct",
            "n_candidate_heads",
            "exploratory_group_size",
            "group_ablation_drop",
            "max_single_ablation_drop",
            "exploratory_group_ablation_drop",
            "dla_content_minus_offset",
            "dla_top_head_share",
            "dla_positive_share",
        ]
        mech_lines = []
        for key in mech_keys:
            if key in row:
                try:
                    mech_lines.append(f"    mechanism {key} = {float(row[key]):.4f}")
                except (TypeError, ValueError):
                    pass
        if mech_lines:
            lines.extend(mech_lines)
    lines.append("")
    if not result.complete:
        if result.note:
            lines.append(
                f"RUN STATUS: {STATUS_INCOMPLETE} — {result.note}. "
                "No verdict is computed: a pilot or a missing measurement is "
                "not a negative."
            )
            return "\n".join(lines)
        missing = sorted({name for s in result.seeds for name in s.missing})
        lines.append(
            f"RUN STATUS: {STATUS_INCOMPLETE} — the manifest does not carry "
            f"the measurement these criteria need ({', '.join(missing)}). "
            "No verdict is computed: a missing measurement is not a negative."
        )
        return "\n".join(lines)
    lines.append(f"RUN VERDICT: {result.verdict}")
    if result.verdict == VERDICT_POSITIVE:
        lines.append(
            "A content-based induction head forms on a variable-distance task, "
            "and the causal interventions land. The word 'induction head' is "
            "earned on this task."
        )
    elif result.verdict == VERDICT_PARTIAL:
        failed = sorted({name for s in result.seeds for name in s.failed})
        not_measured = sorted(
            {name for s in result.seeds for name in s.not_measured}
        )
        detail = (
            f"Failing criteria: {', '.join(failed)}."
            if failed
            else f"Not measured: {', '.join(not_measured)}."
        )
        lines.append(
            "A copy head forms, but the causal evidence does not support the "
            f"induction claim. {detail} "
            "Report the missing criterion, do not re-run."
        )
    else:
        rows = exp1_rows
        no_head = bool(rows) and all(
            int(float(r.get("total_induction_heads", 0.0))) == 0
            for r in rows.values()
        )
        high_copy = bool(rows) and all(
            float(r.get("copy_accuracy", 0.0)) >= 0.60 for r in rows.values()
        )
        low_content = bool(rows) and all(
            float(r.get("peak_content_mass", 0.0)) < 0.30 for r in rows.values()
        )
        if no_head and high_copy and low_content:
            lines.append(
                "NEGATIVE (unexplained): the model solves the task by a "
                "mechanism the detector does not identify. Copy accuracy is "
                "high but no head passes the content-mass screen. Report it "
                "as a negative; the budget is not extended after the fact."
            )
        else:
            lines.append(
                "No content-based induction head at this budget. Report it as "
                "a negative. The budget is not extended after the fact."
            )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# The CLI
# ---------------------------------------------------------------------------
def main(argv: Optional[Sequence[str]] = None) -> int:
    """Print the verdict of a run.

    ``python -m src.experiments.content_verdict --exp1 results/induction_content.json
    --exp4 results/exp4_content.json``
    """
    parser = argparse.ArgumentParser(
        description="The pre-registered verdict of the content-based induction task."
    )
    parser.add_argument("--exp1", required=True, help="the exp1 manifest of the run")
    parser.add_argument(
        "--exp4",
        default=None,
        help="the exp4 manifest of the cascade (criterion 7 lives there)",
    )
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)

    exp1 = load_manifest(args.exp1)
    task = exp1.get("args", {}).get("task")
    exp4 = None
    if args.exp4:
        if Path(args.exp4).exists():
            exp4 = load_manifest(args.exp4)
        else:
            print(
                f"WARNING: exp4 manifest {args.exp4!r} does not exist — "
                "criterion 7 is NOT MEASURED, not a failed path patch.",
                file=sys.stderr,
            )

    result = run_verdict(exp1, exp4)
    exp1_rows = per_seed_metrics(exp1)

    if args.json:
        payload = {
            "status": result.status,
            "verdict": result.verdict,
            "note": result.note,
            "task": task,
            "seeds": [
                {
                    "seed": s.seed,
                    "verdict": s.verdict,
                    "confirmed_heads": s.confirmed_heads,
                    "note": s.note,
                    "missing": list(s.missing),
                    "not_measured": list(s.not_measured),
                    "failed": list(s.failed),
                    "checks": [
                        {
                            "name": c.criterion.name,
                            "metric": c.criterion.metric,
                            "expression": c.criterion.expression,
                            "value": c.value,
                            "status": c.status,
                        }
                        for c in s.checks
                    ],
                }
                for s in result.seeds
            ],
        }
        print(json.dumps(payload, indent=2))
        return 0 if result.complete else 1

    print(f"=== content task verdict: {args.exp1} ===")
    if task is not None and task != "variable":
        print(
            f"WARNING: this manifest's task is {task!r}, not 'variable' — it is "
            "not the content-based run, and its numbers answer a different "
            "question."
        )
    print(format_report(result, exp1_rows))
    return 0 if result.complete else 1


if __name__ == "__main__":
    sys.exit(main())
