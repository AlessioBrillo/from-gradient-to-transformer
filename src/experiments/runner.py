"""Multi-seed experiment runner.

Repeats a single-seed experiment function across several seeds and
aggregates the results into mean/std/min/max per metric. This module only
handles the looping and aggregation — actual seeding still goes through the
existing `src.reproducibility.set_seed`, called by each experiment's own
training routine exactly as it already is for single-seed runs.

Built 2026-08-02 (Micro-Phase 8, the Evidence Pass) because
`checklists/reproducibility-checklist.md` claimed
"[x] Results reported as mean ± std over ≥3 seeds" while no experiment in
`src/` had ever run more than one seed. See
06_production_ai/notes/multi-seed-experiment-design.md.

Optional W&B integration added 2026-09-01 (MP-78) for experiment tracking.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


# Optional W&B integration — lazy import to avoid hard dependency
_wandb: Any = None


def _get_wandb() -> Any:
    global _wandb
    if _wandb is None:
        try:
            import wandb

            _wandb = wandb
        except ImportError:
            _wandb = False
    return _wandb


def init_wandb(
    project: str,
    entity: str | None = None,
    config: dict[str, Any] | None = None,
    tags: list[str] | None = None,
    group: str | None = None,
    name: str | None = None,
) -> Any | None:
    """Initialize W&B run if available. Returns run object or None."""
    wandb = _get_wandb()
    if not wandb:
        logger.debug("wandb not available, skipping initialization")
        return None
    try:
        run = wandb.init(
            project=project,
            entity=entity,
            config=config,
            tags=tags,
            group=group,
            name=name,
        )
        logger.info(f"W&B run initialized: {run.url}")
        return run
    except Exception as e:
        logger.warning(f"Failed to initialize W&B: {e}")
        return None


def log_wandb_metrics(
    run: Any, metrics: dict[str, float], step: int | None = None
) -> None:
    """Log metrics to W&B run if available."""
    wandb = _get_wandb()
    if not wandb or run is None:
        return
    try:
        if hasattr(run, "log"):
            run.log(metrics, step=step)
    except Exception as e:
        logger.warning(f"Failed to log metrics to W&B: {e}")


def log_wandb_artifact(
    run: Any, filepath: str, name: str, type_: str = "model"
) -> None:
    """Log file as W&B artifact if available."""
    wandb = _get_wandb()
    if not wandb or run is None:
        return
    try:
        if hasattr(run, "log_artifact"):
            artifact = wandb.Artifact(name, type=type_)
            artifact.add_file(filepath)
            run.log_artifact(artifact)
    except Exception as e:
        logger.warning(f"Failed to log artifact to W&B: {e}")


def finish_wandb(run: Any) -> None:
    """Finish W&B run if available."""
    wandb = _get_wandb()
    if not wandb or run is None:
        return
    try:
        if hasattr(run, "finish"):
            run.finish()
    except Exception as e:
        logger.warning(f"Failed to finish W&B run: {e}")


@dataclass
class SeedAggregate:
    """Per-metric mean/std/min/max/n aggregated across seeds, plus the raw
    per-seed values (never discard the individual runs — the aggregate is a
    summary, not the source of truth)."""

    per_seed: list[dict[str, float]]
    aggregate: dict[str, dict[str, float]]
    wall_clock_seconds: float

    def summary_line(self, metric: str, fmt: str = ".4f") -> str:
        a = self.aggregate[metric]
        return (
            f"{a['mean']:{fmt}} ± {a['std']:{fmt}} "
            f"(n={int(a['n'])}, range [{a['min']:{fmt}}, {a['max']:{fmt}}])"
        )


def run_seeds(
    fn: Callable[[int], dict[str, float]],
    seeds: Sequence[int],
) -> SeedAggregate:
    """Run `fn(seed)` once per seed and aggregate the returned metric dicts.

    `fn` is responsible for calling `src.reproducibility.set_seed(seed)`
    itself — exactly what every experiment's training routine already does
    for a single seed — and must return a flat `dict[str, float]` of scalar
    metrics. Every seed must report the same metric keys; a seed run that
    silently drops a metric produces a silently smaller aggregate, which is
    worse than a loud failure.

    Raises:
        ValueError: if `seeds` is empty, or if seeds disagree on which
            metric keys they report.
    """
    if not seeds:
        raise ValueError("run_seeds requires at least one seed")

    per_seed: list[dict[str, float]] = []
    start = time.monotonic()
    for seed in seeds:
        logger.info(f"=== seed {seed} ===")
        metrics = fn(seed)
        per_seed.append(metrics)
    wall_clock = time.monotonic() - start

    keys = set(per_seed[0].keys())
    for i, m in enumerate(per_seed[1:], start=1):
        if set(m.keys()) != keys:
            raise ValueError(
                f"Seed {seeds[i]} reported different metric keys "
                f"({set(m.keys())}) than seed {seeds[0]} ({keys}) — every "
                "seed must report the same metrics for a valid aggregate."
            )

    aggregate = aggregate_metrics(per_seed)

    return SeedAggregate(per_seed=per_seed, aggregate=aggregate, wall_clock_seconds=wall_clock)


def aggregate_metrics(per_seed: list[dict[str, float]]) -> dict[str, dict[str, float]]:
    """Aggregate per-seed metric dicts into mean/std/min/max/n per metric.

    The single aggregation used by the live runner and by the manifest
    producers that rebuild manifests from disk checkpoints, so a pinned
    manifest is indistinguishable from a locally-run one. Requires every
    seed to report the same metric keys."""
    keys = set(per_seed[0].keys())
    aggregate: dict[str, dict[str, float]] = {}
    for key in keys:
        values = np.array([m[key] for m in per_seed], dtype=float)
        aggregate[key] = {
            "mean": float(values.mean()),
            "std": float(values.std(ddof=0)) if len(values) > 1 else 0.0,
            "min": float(values.min()),
            "max": float(values.max()),
            "n": float(len(values)),
        }
    return aggregate


def parse_seeds(seeds_arg: str) -> list[int]:
    """Parse a comma-separated `--seeds` CLI argument, e.g. "0,1,2"."""
    return [int(s.strip()) for s in seeds_arg.split(",") if s.strip()]
