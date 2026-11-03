#!/usr/bin/env python3
"""Rebuild one multi-seed manifest from per-seed recovery manifests.

Why this module exists
----------------------
The content-task cascade (issue #200) is long enough that a free GPU session
can die between seeds. Each experiment therefore writes a complete
``ResultsManifest`` for a seed as soon as that seed finishes
(``results/<experiment>_seed<N>.json``). If the session dies before the last
seed, the multi-seed manifest is never written — and the verdict needs the
pre-registered seeds 0, 1 and 2 in **one** manifest.

This tool is the recovery path: it takes the per-seed manifests, checks that
they describe the same run (same experiment, same config, same commit, same
environment), rebuilds the aggregate with the same function the live runner
uses, and writes the multi-seed manifest. It refuses to combine manifests
from different runs, and it refuses a dirty tree: a recovered record must be
as trustworthy as one written in a single session, or it is not evidence.

Usage:
    python -m src.experiments.merge_manifests \
        --inputs results/induction_content_seed0.json \
                 results/induction_content_seed1.json \
                 results/induction_content_seed2.json \
        --output results/induction_content.json \
        --expected-seeds 0,1,2

    # or a directory / glob; files are matched as *_seed*.json
    python -m src.experiments.merge_manifests --inputs results --output ...
"""

from __future__ import annotations

import argparse
import glob
import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from src.experiments.runner import aggregate_metrics, parse_seeds
from src.results import ResultsManifest

logger = logging.getLogger(__name__)

#: Fields that describe the run's environment. Combining manifests that
#: disagree on any of them would attach one run's provenance to another
#: run's numbers.
ENVIRONMENT_FIELDS = (
    "experiment",
    "git_sha",
    "git_dirty",
    "device",
    "torch_version",
    "numpy_version",
    "python_version",
    "n_parameters",
)


def _expand_inputs(raw_inputs: Sequence[str]) -> list[Path]:
    """Every manifest file named by paths, directories or shell-style globs."""
    files: list[Path] = []
    for raw in raw_inputs:
        matches = [Path(m) for m in glob.glob(raw)]
        if not matches:
            raise SystemExit(f"--inputs: {raw!r} does not exist")
        for match in matches:
            if match.is_dir():
                files.extend(sorted(match.glob("*_seed*.json")))
            else:
                files.append(match)
    # Preserve the caller's order but drop an input named twice.
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in files:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    if not unique:
        raise SystemExit("--inputs: no per-seed manifests found")
    return unique


def _load_one(path: Path) -> ResultsManifest:
    """Load one manifest and require that it describes exactly one seed."""
    try:
        manifest = ResultsManifest.load(path)
    except Exception as exc:  # noqa: BLE001 - report, don't crash
        raise SystemExit(f"{path}: not a ResultsManifest ({exc})") from exc
    if len(manifest.seeds) != 1 or len(manifest.per_seed_metrics) != 1:
        raise SystemExit(
            f"{path}: expected exactly one seed and one metric row, got "
            f"seeds={manifest.seeds} and {len(manifest.per_seed_metrics)} "
            "row(s)"
        )
    return manifest


def _check_compatible(manifests: Sequence[ResultsManifest]) -> None:
    """Refuse to combine manifests that are not the same run."""
    first = manifests[0]
    for manifest in manifests[1:]:
        for field in ENVIRONMENT_FIELDS:
            left = getattr(first, field)
            right = getattr(manifest, field)
            if left != right:
                raise SystemExit(
                    f"cannot merge: {field} differs between the inputs "
                    f"({left!r} vs {right!r}). The per-seed files are not "
                    "one run."
                )
        if manifest.args != first.args:
            differing = sorted(
                key
                for key in set(first.args) | set(manifest.args)
                if first.args.get(key) != manifest.args.get(key)
            )
            raise SystemExit(
                "cannot merge: the recorded arguments differ "
                f"({', '.join(differing)}). A seed run with another config "
                "is not a seed of this run."
            )
    if any(m.git_dirty for m in manifests):
        raise SystemExit(
            "cannot merge: at least one input was recorded with a dirty "
            "working tree. Its numbers do not correspond to a committed "
            "instrument."
        )


def _metric_keys_problem(
    manifests: Sequence[ResultsManifest],
) -> str:
    """Why the per-seed metric key sets differ, or ``""``."""
    first = set(manifests[0].per_seed_metrics[0])
    for manifest in manifests[1:]:
        keys = set(manifest.per_seed_metrics[0])
        if keys != first:
            missing = sorted(first - keys)
            extra = sorted(keys - first)
            parts = []
            if missing:
                parts.append(f"missing {missing}")
            if extra:
                parts.append(f"unexpected {extra}")
            return (
                f"seed {manifest.seeds[0]} reports different metrics "
                f"({'; '.join(parts)}) than seed {manifests[0].seeds[0]}"
            )
    return ""


def _merge_source_provenance(
    manifests: Sequence[ResultsManifest],
) -> dict[str, Any] | None:
    """The combined checkpoint provenance of the inputs, or ``None``.

    A run either analysed checkpoints (every seed carries provenance) or it
    did not. A mixture is a bug: it would let a recovered record claim a
    source model for only part of itself.
    """
    present = [m for m in manifests if m.source_provenance is not None]
    if not present:
        return None
    if len(present) != len(manifests):
        raise SystemExit(
            "cannot merge: only some inputs carry source_provenance; the "
            "per-seed files are not one cascade."
        )
    checkpoints: list[dict[str, Any]] = []
    for manifest in manifests:
        provenance = manifest.source_provenance or {}
        entries = provenance.get("checkpoints", [])
        if not isinstance(entries, list):
            raise SystemExit(
                f"seed {manifest.seeds[0]}: source_provenance.checkpoints is not a list"
            )
        for entry in entries:
            if not isinstance(entry, dict):
                raise SystemExit(f"seed {manifest.seeds[0]}: a checkpoint record is not an object")
            checkpoint_seed = entry.get("seed")
            if checkpoint_seed is not None and int(checkpoint_seed) != int(manifest.seeds[0]):
                raise SystemExit(
                    f"seed {manifest.seeds[0]}: its checkpoint record names "
                    f"model seed {checkpoint_seed}"
                )
            checkpoints.append(entry)
    checkpoints.sort(key=lambda c: (c.get("seed") is None, c.get("seed") or -1))
    return {"checkpoints": checkpoints}


def merge_manifests(
    manifests: Sequence[ResultsManifest],
    *,
    allow_optional: bool = False,
    expected_seeds: Sequence[int] | None = None,
    notes: str | None = None,
) -> ResultsManifest:
    """Combine one-seed manifests into the multi-seed record.

    ``allow_optional`` is the recovery counterpart of ``run_seeds``'s
    ``optional_keys``: a seed with no confirmed head legitimately lacks the
    ablation metrics, and the aggregate then only carries the metrics every
    seed measured. The per-seed rows remain the source of truth either way.
    """
    if not manifests:
        raise SystemExit("cannot merge: no manifests")
    ordered = sorted(manifests, key=lambda m: int(m.seeds[0]))
    seeds = [int(m.seeds[0]) for m in ordered]
    if len(set(seeds)) != len(seeds):
        raise SystemExit(f"cannot merge: duplicate seeds in {seeds}")
    if expected_seeds is not None and set(seeds) != set(expected_seeds):
        missing = sorted(set(expected_seeds) - set(seeds))
        extra = sorted(set(seeds) - set(expected_seeds))
        parts = []
        if missing:
            parts.append(f"missing {missing}")
        if extra:
            parts.append(f"unexpected {extra}")
        raise SystemExit(
            "cannot merge: the pre-registered seeds are "
            f"{sorted(expected_seeds)} ({'; '.join(parts)})"
        )
    _check_compatible(ordered)
    if not allow_optional:
        problem = _metric_keys_problem(ordered)
        if problem:
            raise SystemExit(
                f"cannot merge: {problem}. Pass --allow-optional if the "
                "difference is a measurement that is legitimately undefined "
                "for a seed (e.g. no confirmed head); the aggregate will "
                "only carry the metrics every seed measured."
            )
    per_seed = [m.per_seed_metrics[0] for m in ordered]
    first = ordered[0]
    return ResultsManifest(
        experiment=first.experiment,
        seeds=seeds,
        args=first.args,
        per_seed_metrics=per_seed,
        aggregate=aggregate_metrics(per_seed),
        wall_clock_seconds=float(sum(m.wall_clock_seconds for m in ordered)),
        git_sha=first.git_sha,
        git_dirty=first.git_dirty,
        device=first.device,
        torch_version=first.torch_version,
        numpy_version=first.numpy_version,
        python_version=first.python_version,
        n_parameters=first.n_parameters,
        notes=notes or f"Merged from {len(ordered)} per-seed recovery manifests.",
        source_provenance=_merge_source_provenance(ordered),
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=("Rebuild a multi-seed ResultsManifest from per-seed recovery manifests.")
    )
    parser.add_argument(
        "--inputs",
        nargs="+",
        required=True,
        help="per-seed manifests: files, a directory, or shell-style globs",
    )
    parser.add_argument("--output", required=True, help="where to write the merged manifest")
    parser.add_argument(
        "--expected-seeds",
        default=None,
        help="comma-separated seeds the merged manifest must contain (e.g. 0,1,2)",
    )
    parser.add_argument(
        "--allow-optional",
        action="store_true",
        help=(
            "allow seeds to differ in metric keys; the aggregate then carries "
            "only the metrics every seed measured"
        ),
    )
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    paths = _expand_inputs(args.inputs)
    manifests = [_load_one(path) for path in paths]
    expected = parse_seeds(args.expected_seeds) if args.expected_seeds else None
    merged = merge_manifests(
        manifests,
        allow_optional=args.allow_optional,
        expected_seeds=expected,
        notes=(
            f"Merged from {len(paths)} per-seed recovery manifests: "
            + ", ".join(path.name for path in paths)
        ),
    )
    output = Path(args.output)
    merged.save(output)
    logger.info(f"Saved merged manifest to {output}")
    logger.info(f"  seeds: {merged.seeds}")
    for key, stats in merged.aggregate.items():
        logger.info(f"  {key}: {stats['mean']:.4f} ± {stats['std']:.4f} (n={int(stats['n'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
