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

1. ``confirmed_content_mass`` >= 0.30 — the **confirmed head** puts a third
   of its attention mass on the content key.
2. ``confirmed_content_mass - peak_offset_mass`` >= 0.10 — and that mass
   beats the best fixed offset.
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

Criteria 1 and 2 read the **confirmed head's** content mass, exactly as the
pre-registration's table says ("`content_mass` of the confirmed head"). They
do not read ``peak_content_mass``, which is the strongest head on the screen
whether or not that head was confirmed: on 2026-10-25 the two were the same
number only because the strongest head was also the one the rule looked for.
When no head is confirmed there is no confirmed-head mass to measure, so the
two criteria are ``NOT MEASURED`` — the same rule criterion 6 already used
for ablation. A fabricated 0.0 would turn "nothing was confirmed" into a
failed measurement.

The seed verdict is ``POSITIVE`` when all seven are met, ``PARTIAL`` when a
head is confirmed but the criteria are not all met, and ``NEGATIVE``
otherwise. The run verdict requires the pre-registered three seeds:
``POSITIVE`` when a majority of them are positive, ``PARTIAL`` when any seed
is partial, and ``NEGATIVE`` otherwise. Fewer seeds are a pilot, not the
run, and report ``INCOMPLETE``.

Two verdicts, never one (2026-11-11)
------------------------------------
The training run was pinned at commit ``88147ee``; the cascade that
measures criterion 7 was executed **afterwards**, at ``891ef46``. The
pre-registration's decision rule was applied to the run *as it was
launched* — criterion 7 was a post-hoc addendum, and the ledger says so in
the same words. So the module computes two verdicts and publishes them
side by side:

* ``pre_registered`` — the training run alone. Criterion 7 is
  ``NOT MEASURED`` there, because the cascade was not part of that run.
* ``causal_addendum`` — the same run plus the cascade, with the commit
  difference **declared** in its provenance.

Merging them is what made ``make content-verdict`` refuse to compute
anything at all (the cascade's commit is not the training run's commit), and
merging them would also hide which instrument produced which label. The
strict refusal still exists for the merged mode (:func:`run_verdict`): a
cascade measured at a different commit is not the pre-registered instrument.

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
from dataclasses import dataclass, field
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


#: The seven criteria, frozen on 2026-10-20. Thresholds and order unchanged;
#: criteria 1-2 read the confirmed head's mass (the pre-registration's
#: wording), not the screen's peak across every head.
CRITERIA: tuple[Criterion, ...] = (
    Criterion("content mass", "confirmed_content_mass", 0.30),
    Criterion(
        "content beats position",
        "confirmed_content_mass",
        0.10,
        other="peak_offset_mass",
    ),
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
        return tuple(c.criterion.name for c in self.checks if c.status == CHECK_NOT_MEASURED)

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
    #: Facts about *which* instrument produced the verdict. A verdict that
    #: merges a pre-registered run with a later cascade must say so here, or
    #: the reader cannot tell which measurement produced which label.
    provenance: Mapping[str, Any] = field(default_factory=dict)

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


def _exp4_criterion_not_measured(criterion: Criterion, metrics: Mapping[str, Any]) -> bool:
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


#: The exp1 metrics that only exist when a head was confirmed. With no
#: confirmed head there is nothing to measure, so these are ``NOT MEASURED``
#: rather than a failed 0.0 — the same rule exp4 already applied to path
#: patching.
HEAD_DEPENDENT_METRICS = frozenset({"confirmed_content_mass", "mean_copy_ablation_drop"})


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
    # The head count is the input that decides whether the head-level
    # criteria are measurable at all. Without it, a fabricated 0.0 would read
    # as "no head confirmed" and the run would be reported as a negative it
    # never measured; the seed is incomplete instead.
    note = ""
    if confirmed is None:
        note = "the exp1 manifest does not carry a usable total_induction_heads"
    checks: list[Check] = []
    for criterion in criteria:
        if criterion.source == SOURCE_EXP4:
            if exp4_metrics is None or _exp4_criterion_not_measured(criterion, exp4_metrics):
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
        # A head-level criterion needs a confirmed head. With none confirmed
        # there is nothing to measure — not a measured zero. This is the same
        # distinction exp4 draws for path patching.
        if criterion.metric in HEAD_DEPENDENT_METRICS and confirmed == 0:
            checks.append(Check(criterion, None, CHECK_NOT_MEASURED))
            continue
        checks.append(check_criterion(criterion, exp1_metrics))
    return SeedVerdict(seed=seed, checks=tuple(checks), confirmed_heads=confirmed, note=note)


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
        return f"{label} declares {len(seeds)} seed(s) but carries {len(rows)} metric row(s)"
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


def _manifest_arg(manifest: Mapping[str, Any], name: str) -> Any:
    """One value from a manifest's recorded arguments, or ``None``."""
    args = manifest.get("args")
    if not isinstance(args, Mapping):
        return None
    return args.get(name)


def _same_commit(left: str, right: str) -> bool:
    """True when two git SHAs name the same commit, allowing abbreviations."""
    left, right = left.strip(), right.strip()
    return bool(left and right) and (
        left == right or left.startswith(right) or right.startswith(left)
    )


def _exp1_problem(exp1: Mapping[str, Any]) -> str:
    """Why the exp1 manifest is not a measurement of the content task, or "".

    The seven criteria answer the content task only. A periodic manifest, or
    one recorded on a dirty tree, did not measure the thing the verdict is
    about, and the verdict must refuse rather than attach a label to it.
    """
    task = _manifest_arg(exp1, "task")
    if task is None:
        return (
            "the exp1 manifest does not declare its task; the seven criteria "
            "are the variable-distance task's"
        )
    if task != "variable":
        return (
            f"the exp1 manifest is the {task!r} task, not 'variable' — its "
            "numbers answer the periodic question"
        )
    if exp1.get("git_dirty") is True:
        return (
            "the exp1 manifest was recorded with a dirty working tree; its "
            "numbers do not correspond to a committed instrument"
        )
    return ""


def _exp4_problem(exp1: Mapping[str, Any], exp4: Mapping[str, Any]) -> str:
    """Why the exp4 manifest is not a cascade of this exp1 run, or "".

    The *commit* difference between the two manifests is **not** checked
    here: whether a cascade measured at a later commit may be merged into
    the pre-registered verdict is a decision about the record, not a fact
    about the measurement, and it is taken by the caller (see
    :func:`run_verdict` and :func:`run_addendum_verdict`).
    """
    task = _manifest_arg(exp1, "task")
    source_task = _manifest_arg(exp4, "source_task")
    if source_task is not None and source_task != task:
        return (
            f"exp4 analysed the {source_task!r} task, not {task!r}; the "
            "cascade and the run are not the same experiment"
        )
    if exp4.get("git_dirty") is True:
        return (
            "the exp4 manifest was recorded with a dirty working tree; its "
            "causal measurement does not correspond to a committed instrument"
        )
    return ""


def _commit_drift(exp1: Mapping[str, Any], exp4: Mapping[str, Any]) -> dict[str, Any]:
    """The fact that the cascade was measured at a different commit, or {}.

    On 2026-11-09 the content task's training run was pinned at
    ``88147ee``; the causal cascade — the addendum that measures criterion 7
    — was executed later, at ``891ef46``. The two are the same experiment
    (the cascade loads the training run's own checkpoints, and its
    ``source_provenance`` says so), but they are two instruments, and a
    record that merges them has to say which is which.
    """
    exp1_sha = exp1.get("git_sha")
    exp4_sha = exp4.get("git_sha")
    if not exp1_sha or not exp4_sha:
        return {}
    if str(exp1_sha) == "unknown" or str(exp4_sha) == "unknown":
        return {}
    if _same_commit(str(exp1_sha), str(exp4_sha)):
        return {}
    return {
        "exp1_git_sha": str(exp1_sha),
        "exp4_git_sha": str(exp4_sha),
        "declared": True,
        "reason": (
            "the cascade was executed after the pre-registered training run, "
            "at a later commit; it loads that run's own checkpoints and its "
            "source_provenance records them"
        ),
    }


def _cascade_problem(
    seed: int,
    exp1_row: Mapping[str, Any],
    exp4_row: Optional[Mapping[str, Any]],
    exp1: Optional[Mapping[str, Any]] = None,
    exp4: Optional[Mapping[str, Any]] = None,
) -> str:
    """Why exp4 did not analyse the model this exp1 seed trained, or ``""``.

    Four independent facts have to line up: the checkpoint must come from
    the same model seed, it must be the model's final epoch (a rolling
    checkpoint can be up to ``--checkpoint-every`` epochs stale), the
    checkpoint must have been written by the same commit exp1 ran, and the
    counterfactual must be the pre-registered minimal pair. A mismatch is a
    cascade about a different model or a different intervention.
    """
    if exp4_row is None:
        return ""
    source_seed = _read_metric(exp4_row, "source_model_seed")
    if source_seed is not None and int(source_seed) >= 0 and int(source_seed) != seed:
        return f"seed {seed}: exp4 analysed model seed {int(source_seed)}, not {seed}"
    minimal_pair = _read_metric(exp4_row, "counterfactual_minimal_pair")
    if minimal_pair is not None and minimal_pair != 1.0:
        return (
            f"seed {seed}: exp4 used a disjoint counterfactual, not the pre-registered minimal pair"
        )
    exp4_epoch = _read_metric(exp4_row, "checkpoint_epoch")
    if exp4_epoch is not None and exp4_epoch < 0:
        return (
            f"seed {seed}: exp4 did not analyse a checkpoint "
            "(checkpoint_epoch = -1) — it trained its own model, so this is "
            "not the cascade"
        )
    exp1_epochs = _read_metric(exp1_row, "epochs_run")
    if exp1_epochs is not None and exp4_epoch is not None and exp4_epoch >= 0:
        if int(exp1_epochs) != int(exp4_epoch):
            return (
                f"seed {seed}: exp4 analysed checkpoint epoch "
                f"{int(exp4_epoch)} but exp1 ran {int(exp1_epochs)} epochs; "
                "the cascade is not about the final model"
            )
    provenance = (exp4 or {}).get("source_provenance")
    if isinstance(provenance, Mapping):
        exp1_sha = (exp1 or {}).get("git_sha")
        checkpoints = provenance.get("checkpoints", [])
        if isinstance(checkpoints, list):
            for checkpoint in checkpoints:
                if not isinstance(checkpoint, Mapping):
                    continue
                try:
                    checkpoint_seed = int(checkpoint.get("seed", -1))
                except (TypeError, ValueError):
                    continue
                if checkpoint_seed != seed:
                    continue
                if checkpoint.get("git_dirty") is True:
                    return (
                        f"seed {seed}: the checkpoint was trained with a dirty "
                        "working tree — its weights do not correspond to a "
                        "committed instrument"
                    )
                checkpoint_sha = checkpoint.get("git_sha")
                if (
                    checkpoint_sha
                    and checkpoint_sha != "unknown"
                    and exp1_sha
                    and exp1_sha != "unknown"
                    and not _same_commit(str(checkpoint_sha), str(exp1_sha))
                ):
                    return (
                        f"seed {seed}: the checkpoint was trained at "
                        f"{checkpoint_sha} but exp1 ran at {exp1_sha}; the "
                        "cascade measured weights from a different instrument"
                    )
    return ""


def run_verdict(
    exp1: Mapping[str, Any],
    exp4: Optional[Mapping[str, Any]] = None,
    criteria: Sequence[Criterion] = CRITERIA,
    expected_seeds: Sequence[int] = (0, 1, 2),
    *,
    allow_commit_drift: bool = False,
    label: str = "run",
) -> RunVerdict:
    """The verdict of a run, from the exp1 manifest and (optionally) exp4's.

    The pre-registration fixes **three seeds, 0, 1 and 2**. A manifest that
    carries a different set is not the run: it gets ``INCOMPLETE`` and no
    verdict, so neither a one-seed pilot nor an extra seed can be reported
    as the pre-registered POSITIVE. An empty manifest is likewise
    ``INCOMPLETE`` rather than a vacuous negative.

    ``allow_commit_drift`` decides what happens when the cascade was measured
    at a **later commit** than the training run. Off (the default), the
    verdict refuses: two instruments are two instruments, and a merged label
    would hide which one produced it. On, the difference is **declared** in
    ``RunVerdict.provenance`` and the verdict is computed — the mode the
    causal addendum uses, where the cascade is reported separately from the
    pre-registered verdict rather than merged into it.
    """
    exp1_problem = _manifest_seed_problem(exp1, "the exp1 manifest")
    if exp1_problem:
        return RunVerdict(
            label=label,
            seeds=(),
            status=STATUS_INCOMPLETE,
            verdict="",
            note=exp1_problem,
        )
    exp1_rows = per_seed_metrics(exp1)
    exp1_seeds = [int(s) for s in exp1.get("seeds", [])]
    exp4_rows: dict[int, Mapping[str, Any]] = {}
    drift: dict[str, Any] = {}
    if exp4 is not None:
        exp4_problem = _manifest_seed_problem(exp4, "the exp4 manifest")
        if exp4_problem:
            return RunVerdict(
                label=label,
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
                label=label,
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
        seeds.append(evaluate_seed(seed, exp1_rows[seed], exp4_rows.get(seed), criteria))
    if not exp1_seeds:
        return RunVerdict(
            label=label,
            seeds=(),
            status=STATUS_INCOMPLETE,
            verdict="",
            note="the exp1 manifest carries no seeds",
        )
    exp1_issue = _exp1_problem(exp1)
    if exp1_issue:
        return RunVerdict(
            label=label,
            seeds=tuple(seeds),
            status=STATUS_INCOMPLETE,
            verdict="",
            note=exp1_issue,
        )
    if exp4 is not None:
        exp4_issue = _exp4_problem(exp1, exp4)
        if exp4_issue:
            return RunVerdict(
                label=label,
                seeds=tuple(seeds),
                status=STATUS_INCOMPLETE,
                verdict="",
                note=exp4_issue,
            )
        drift = _commit_drift(exp1, exp4)
        if drift and not allow_commit_drift:
            return RunVerdict(
                label=label,
                seeds=tuple(seeds),
                status=STATUS_INCOMPLETE,
                verdict="",
                note=(
                    f"exp1 was run at {drift['exp1_git_sha']} and exp4 at "
                    f"{drift['exp4_git_sha']}; a cascade from a different "
                    "commit is not the pre-registered instrument"
                ),
            )
    cascade_problems = [
        problem
        for seed in seeds
        if (
            problem := _cascade_problem(
                seed.seed,
                exp1_rows[seed.seed],
                exp4_rows.get(seed.seed),
                exp1,
                exp4,
            )
        )
    ]
    if cascade_problems:
        return RunVerdict(
            label=label,
            seeds=tuple(seeds),
            status=STATUS_INCOMPLETE,
            verdict="",
            note="; ".join(cascade_problems),
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
            label=label,
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
        missing_measurements = sorted({name for s in incomplete for name in s.missing})
        notes = sorted({s.note for s in incomplete if s.note})
        parts = []
        if missing_measurements:
            parts.append(f"missing measurements: {', '.join(missing_measurements)}")
        if notes:
            parts.append("; ".join(notes))
        return RunVerdict(
            label=label,
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
        label=label,
        seeds=tuple(seeds),
        status=STATUS_COMPLETE,
        verdict=overall,
        provenance=drift,
    )


def run_addendum_verdict(
    exp1: Mapping[str, Any],
    exp4: Mapping[str, Any],
    criteria: Sequence[Criterion] = CRITERIA,
    expected_seeds: Sequence[int] = (0, 1, 2),
) -> RunVerdict:
    """The verdict of the **causal addendum**: the pre-registered run plus
    the cascade that measures criterion 7.

    The addendum is reported **beside** the pre-registered verdict, never
    merged into it. Its provenance is declared in
    ``RunVerdict.provenance``: the cascade was executed after the training
    run, at a later commit, and it analyses that run's own checkpoints
    (the ``source_provenance`` of the exp4 manifest records them).

    Every other refusal still applies — a cascade that analysed a different
    model, a stale checkpoint, another task or a dirty tree is not an
    addendum of this run and gets ``INCOMPLETE`` with no label.
    """
    return run_verdict(
        exp1,
        exp4,
        criteria=criteria,
        expected_seeds=expected_seeds,
        allow_commit_drift=True,
        label="causal_addendum",
    )


@dataclass(frozen=True)
class VerdictBundle:
    """The two verdicts of the content task, kept apart.

    * ``pre_registered`` — the verdict of the run the pre-registration
      froze: the training run alone. Criterion 7 (path patching) is
      ``NOT MEASURED`` there, because the cascade was not part of that run.
    * ``addendum`` — the same run plus the causal cascade, reported
      separately with its own provenance.
    """

    pre_registered: RunVerdict
    addendum: Optional[RunVerdict] = None

    @property
    def complete(self) -> bool:
        return self.pre_registered.complete


def run_verdicts(
    exp1: Mapping[str, Any],
    exp4: Optional[Mapping[str, Any]] = None,
    criteria: Sequence[Criterion] = CRITERIA,
    expected_seeds: Sequence[int] = (0, 1, 2),
) -> VerdictBundle:
    """The pre-registered verdict and, when a cascade exists, the addendum."""
    pre_registered = run_verdict(
        exp1,
        None,
        criteria=criteria,
        expected_seeds=expected_seeds,
        label="pre_registered",
    )
    addendum = (
        run_addendum_verdict(exp1, exp4, criteria=criteria, expected_seeds=expected_seeds)
        if exp4 is not None
        else None
    )
    return VerdictBundle(pre_registered=pre_registered, addendum=addendum)


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


def _row_metric(row: Mapping[str, Any], key: str) -> Optional[float]:
    """One numeric metric from a per-seed manifest row, or ``None``."""
    return _read_metric(row, key)


def _numeric_fields(row: Mapping[str, Any], keys: Sequence[str]) -> dict[str, float]:
    """The subset of ``keys`` the row carries as numbers, in order."""
    fields: dict[str, float] = {}
    for key in keys:
        value = _row_metric(row, key)
        if value is not None:
            fields[key] = value
    return fields


#: The exp1 mechanism numbers printed next to the verdict. They are the
#: secondary circuit report, not the seven criteria.
MECHANISM_KEYS = (
    "peak_content_mass",
    "peak_offset_mass",
    "k_composition_score",
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
)

#: The exp4 cascade numbers printed next to the verdict.
CASCADE_KEYS = (
    "mean_path_patch_effect",
    "group_path_patch_effect",
    "mean_ablation_effect",
    "mean_activation_recovery",
    "checkpoint_epoch",
    "source_model_seed",
)


def _is_distributed(row: Mapping[str, Any]) -> bool:
    """The pre-registered ``distributed`` classification, read from the row.

    The same two conditions ``copy_circuit.classify_mechanism`` uses: the
    candidate group carries the copy (>= 0.20) and no single member does
    (<= 0.10). Requiring the single-head number to be present keeps an old
    manifest with no measured drop from being read as a zero.
    """
    candidates = _row_metric(row, "n_candidate_heads")
    group = _row_metric(row, "group_ablation_drop")
    single = _row_metric(row, "max_single_ablation_drop")
    return (
        candidates is not None
        and candidates > 0
        and group is not None
        and group >= 0.20
        and single is not None
        and single <= 0.10
    )


def _negative_lines(
    result: RunVerdict,
    exp1_rows: Mapping[int, Mapping[str, Any]],
    exp4_rows: Mapping[int, Mapping[str, Any]],
) -> list[str]:
    """The decision table's NEGATIVE sentences, with the secondary report.

    The frozen rule has two negatives: "no head is confirmed" and "the copy
    is high but the content mass is low" (the detector's blind spot). The
    2026-10-25 addendum added a third measured case that is still the second
    negative: the per-head screen can pass and the K-composition confirmation
    can still fail on a distributed circuit. The report names which one
    happened; it does not change the label.
    """
    confirmed_zero = {s.seed for s in result.seeds if (s.confirmed_heads or 0) == 0}
    high_copy = {
        seed
        for seed in confirmed_zero
        if (_row_metric(exp1_rows.get(seed, {}), "copy_accuracy") or 0.0) >= 0.60
    }
    if not high_copy:
        return [
            "No content-based induction head at this budget. Report it as a "
            "negative. The budget is not extended after the fact."
        ]

    seeds = ", ".join(str(s) for s in sorted(high_copy))
    lines = [
        "NEGATIVE (unexplained): the model solves the task by a mechanism the "
        f"detector does not identify (seed(s) {seeds}). Copy accuracy is high "
        "but no head is confirmed. Report it as a negative; the budget is not "
        "extended after the fact."
    ]
    distributed = sorted(seed for seed in high_copy if _is_distributed(exp1_rows.get(seed, {})))
    if distributed:
        group_drops = [_row_metric(exp1_rows[seed], "group_ablation_drop") for seed in distributed]
        single_drops = [
            _row_metric(exp1_rows[seed], "max_single_ablation_drop") for seed in distributed
        ]
        group_values = [v for v in group_drops if v is not None]
        single_values = [v for v in single_drops if v is not None]
        lines.append(
            "The mechanism report classifies the copy as distributed: the "
            "candidate group's ablation removes "
            f"{min(group_values):.4f}–{max(group_values):.4f} of the copy "
            "accuracy, while no single head removes more than "
            f"{max(single_values):.4f}. The per-head rule confirms no head "
            "because the K-composition confirmation does not fire; that is "
            "the detector's granularity, not the absence of a copy circuit."
        )
        group_patch = [
            _row_metric(exp4_rows.get(seed, {}), "group_path_patch_effect") for seed in distributed
        ]
        patch_values = [v for v in group_patch if v is not None]
        if patch_values:
            lines.append(
                "The cascade's group path-patch effect is "
                f"{min(patch_values):.4f}–{max(patch_values):.4f}."
            )
        lines.append(
            "This is a pre-specified secondary finding, not a change to the "
            "verdict: the seven criteria still decide, and the word "
            "'induction head' is not used."
        )
    else:
        low_content = all(
            (_row_metric(exp1_rows.get(seed, {}), "peak_content_mass") or 0.0) < 0.30
            for seed in high_copy
        )
        # A single head that carries the copy is the strongest thing the
        # mechanism report can say, and it is what the 2026-11-09 GPU run
        # measured on the seeds whose per-head screen confirmed nothing:
        # ablating one head removed 0.93-0.94 of the copy accuracy while the
        # screen saw 0.09-0.12 of content mass on that head. The report has
        # to name the carrier — the negative is about the *confirmation*,
        # not about the absence of a circuit.
        carried = {
            seed: value
            for seed, value in (
                (seed, _row_metric(exp1_rows.get(seed, {}), "max_single_ablation_drop"))
                for seed in high_copy
            )
            if value is not None and value >= 0.20
        }
        if carried:
            values = list(carried.values())
            lines.append(
                "The mechanism report names the carrier: ablating a single "
                f"head removes {min(values):.4f}–{max(values):.4f} of the copy "
                "accuracy (seed(s) "
                + ", ".join(str(s) for s in sorted(carried))
                + "). The copy is therefore carried by one head; the per-head "
                "rule does not confirm it because the content-mass screen and "
                "the K-composition confirmation do not fire on that head. That "
                "is the detector's granularity, not the absence of a copy "
                "circuit."
            )
        elif low_content:
            lines.append(
                "Copy accuracy is high but no head passes the content-mass "
                "screen. The mechanism report says which heads carry the copy."
            )
        else:
            lines.append(
                "A per-head candidate passes the content screen but the "
                "K-composition rule confirms no head. The mechanism report "
                "says whether the copy is distributed or undetermined."
            )
    return lines


def format_report(
    result: RunVerdict,
    exp1_rows: Mapping[int, Mapping[str, Any]],
    exp4_rows: Optional[Mapping[int, Mapping[str, Any]]] = None,
) -> str:
    """The full, printable report of a run.

    ``exp4_rows`` is optional so a caller with only the exp1 manifest still
    gets a report; when present, the cascade's group path-patch effect and
    checkpoint provenance are printed next to the verdict (they are the
    causal half of the secondary mechanism report).
    """
    exp4_rows = exp4_rows or {}
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
        mech_lines = []
        for key in MECHANISM_KEYS:
            if key in row:
                try:
                    mech_lines.append(f"    mechanism {key} = {float(row[key]):.4f}")
                except (TypeError, ValueError):
                    pass
        if mech_lines:
            lines.extend(mech_lines)
        cascade_row = exp4_rows.get(seed.seed, {})
        cascade_lines = []
        for key in CASCADE_KEYS:
            value = _row_metric(cascade_row, key)
            if value is not None:
                cascade_lines.append(f"    cascade      {key} = {value:.4f}")
        if cascade_lines:
            lines.extend(cascade_lines)
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
        not_measured = sorted({name for s in result.seeds for name in s.not_measured})
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
        lines.extend(_negative_lines(result, exp1_rows, exp4_rows))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# The saved artifact
# ---------------------------------------------------------------------------
#: Schema 1 merged the training run and the cascade into one verdict.
#: Schema 2 (2026-11-11) keeps them apart: ``pre_registered`` is the verdict
#: of the run the pre-registration froze, ``causal_addendum`` is the same
#: run plus the cascade that measures criterion 7, with its provenance
#: declared. The reason is a fact about the record, not about the code: the
#: cascade was executed **after** the training run, at a later commit, and
#: the pre-registration's own decision rule was applied to the run as it was
#: launched (criterion 7 was a post-hoc addendum, and the ledger says so).
VERDICT_SCHEMA = "content-verdict/2"


def _verdict_section(
    result: RunVerdict,
    exp1_rows: Mapping[int, Mapping[str, Any]],
    exp4_rows: Mapping[int, Mapping[str, Any]],
) -> dict[str, Any]:
    """One verdict (pre-registered or addendum) as a JSON-serialisable dict."""
    return {
        "label": result.label,
        "status": result.status,
        "verdict": result.verdict,
        "note": result.note,
        "provenance": dict(result.provenance),
        "seeds": [
            {
                "seed": seed.seed,
                "verdict": seed.verdict,
                "confirmed_heads": seed.confirmed_heads,
                "note": seed.note,
                "missing": list(seed.missing),
                "not_measured": list(seed.not_measured),
                "failed": list(seed.failed),
                "checks": [
                    {
                        "name": check.criterion.name,
                        "metric": check.criterion.metric,
                        "expression": check.criterion.expression,
                        "value": check.value,
                        "status": check.status,
                    }
                    for check in seed.checks
                ],
                "mechanism": _numeric_fields(exp1_rows.get(seed.seed, {}), MECHANISM_KEYS),
                "cascade": _numeric_fields(exp4_rows.get(seed.seed, {}), CASCADE_KEYS),
            }
            for seed in result.seeds
        ],
    }


def verdict_payload(
    result: RunVerdict,
    exp1_rows: Optional[Mapping[int, Mapping[str, Any]]] = None,
    exp4_rows: Optional[Mapping[int, Mapping[str, Any]]] = None,
    task: Optional[str] = None,
    sources: Optional[Mapping[str, Optional[str]]] = None,
    addendum: Optional[RunVerdict] = None,
) -> dict[str, Any]:
    """The verdict as a JSON-serialisable record.

    This is the artifact the GPU session saves next to the manifests. It is
    *not* a ``ResultsManifest`` and must not be pinned as one: it records the
    decision, the per-seed checks and the secondary mechanism numbers, all of
    which are re-derivable from the manifests named in ``sources``.

    The top level keeps the **pre-registered** verdict (the run the
    pre-registration froze). The causal addendum, when it exists, is in
    ``verdicts["causal_addendum"]`` with its provenance — never merged into
    the pre-registered one.
    """
    exp1_rows = exp1_rows or {}
    exp4_rows = exp4_rows or {}
    payload: dict[str, Any] = {
        "schema": VERDICT_SCHEMA,
        "task": task,
        "status": result.status,
        "verdict": result.verdict,
        "note": result.note,
        "sources": dict(sources or {}),
        "verdicts": {"pre_registered": _verdict_section(result, exp1_rows, exp4_rows)},
    }
    if addendum is not None:
        payload["verdicts"]["causal_addendum"] = _verdict_section(
            addendum, exp1_rows, exp4_rows
        )
        payload["provenance"] = dict(addendum.provenance)
    # The legacy top-level seed list stays the pre-registered one, so an old
    # reader of the artifact still finds the same shape it knows.
    payload["seeds"] = payload["verdicts"]["pre_registered"]["seeds"]
    return payload


def bundle_payload(
    bundle: VerdictBundle,
    exp1_rows: Optional[Mapping[int, Mapping[str, Any]]] = None,
    exp4_rows: Optional[Mapping[int, Mapping[str, Any]]] = None,
    task: Optional[str] = None,
    sources: Optional[Mapping[str, Optional[str]]] = None,
) -> dict[str, Any]:
    """The payload of both verdicts."""
    return verdict_payload(
        bundle.pre_registered,
        exp1_rows,
        exp4_rows,
        task,
        sources,
        addendum=bundle.addendum,
    )


def write_verdict_json(payload: Mapping[str, Any], path: str | Path) -> Path:
    """Write the verdict payload to ``path``, creating its directory."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return out


def format_bundle_report(
    bundle: VerdictBundle,
    exp1_rows: Mapping[int, Mapping[str, Any]],
    exp4_rows: Mapping[int, Mapping[str, Any]],
) -> str:
    """The printable report of **both** verdicts, kept apart.

    The pre-registered verdict comes first and is the one the record
    publishes. The causal addendum follows, with its provenance in the
    header — a reader must be able to tell which instrument produced which
    label without opening a manifest.
    """
    parts = [
        "=== 1. PRE-REGISTERED VERDICT (the training run alone; "
        "criterion 7 was not part of it) ===",
        format_report(bundle.pre_registered, exp1_rows, exp4_rows),
    ]
    if bundle.addendum is not None:
        drift = bundle.addendum.provenance
        header = "=== 2. CAUSAL ADDENDUM (the cascade that measures criterion 7) ==="
        if drift:
            header += (
                f"\n    provenance: training run at {drift.get('exp1_git_sha')}, "
                f"cascade at {drift.get('exp4_git_sha')} — "
                f"{drift.get('reason', '')}"
            )
        parts.append(header)
        parts.append(format_report(bundle.addendum, exp1_rows, exp4_rows))
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# The CLI
# ---------------------------------------------------------------------------
def main(argv: Optional[Sequence[str]] = None) -> int:
    """Print (and optionally save) the verdict of a run.

    ``python -m src.experiments.content_verdict --exp1 results/induction_content.json
    --exp4 results/exp4_content.json --output results/content_verdict.json``

    Two verdicts are printed and saved: the **pre-registered** one (the run
    the pre-registration froze — the training manifest alone) and the
    **causal addendum** (the same run plus the cascade that measures
    criterion 7, with its commit provenance declared). They are never merged:
    the addendum was measured after the fact, and the record has to show it.
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
    parser.add_argument(
        "--output",
        default=None,
        help="also write the JSON payload here (e.g. results/content_verdict.json)",
    )
    args = parser.parse_args(argv)

    exp1 = load_manifest(args.exp1)
    task = _manifest_arg(exp1, "task")
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

    bundle = run_verdicts(exp1, exp4)
    exp1_rows = per_seed_metrics(exp1)
    exp4_rows = per_seed_metrics(exp4) if exp4 is not None else {}
    payload = bundle_payload(
        bundle,
        exp1_rows,
        exp4_rows,
        task,
        {"exp1": args.exp1, "exp4": args.exp4},
    )
    if args.output:
        written = write_verdict_json(payload, args.output)
        print(f"verdict written to {written}", file=sys.stderr)

    if args.json:
        print(json.dumps(payload, indent=2))
        return 0 if bundle.complete else 1

    print(f"=== content task verdict: {args.exp1} ===")
    if task is not None and task != "variable":
        print(
            f"WARNING: this manifest's task is {task!r}, not 'variable' — it is "
            "not the content-based run, and its numbers answer a different "
            "question."
        )
    print(format_bundle_report(bundle, exp1_rows, exp4_rows))
    return 0 if bundle.complete else 1


if __name__ == "__main__":
    sys.exit(main())
