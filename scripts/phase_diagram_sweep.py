#!/usr/bin/env python3
"""Phase Diagram Sweep Runner for Grokking.

Runs a targeted sweep over modulus P, model size, weight decay, protocol
deviations, and training mode (solo vs joint), collecting per-cell aggregates
across 3 seeds. Emits a working manifest (torch .pt, for resume) and, on
request, per-cell standard `ResultsManifest` JSON files that the honesty
system (`make verify-claims`) can cite.

Usage:
    python scripts/phase_diagram_sweep.py --config configs/phase_diagram_sweep.yaml
    python scripts/phase_diagram_sweep.py --config configs/phase_diagram_sweep_test.yaml \
        --emit-manifests results/ --dry-run   # prints the cells

Design contract (issue #168): a sweep cell IS an exp2/exp6 run at that
config, not a re-implementation that can drift from one. The solo path
delegates to `exp2_grokking.run_single_seed` with an argparse namespace built
by exp2's own parser + `apply_protocol`, so the Nanda/repo protocol and
every deviation flag are exp2's code, applied by exp2's code. The joint path
delegates to `exp6_capstone.train_single_seed` with a config dict built from
the capstone config schema. `tests/test_phase_diagram_sweep.py` pins the
parity: the same seed + config must produce identical metrics through either
entry point.

Budgets are stated in optimizer steps, never epochs. The 2026-10-08 audit
found small-modulus cells untrained because the budget was counted in epochs
and at P=29 one epoch is two steps; `SweepCell.epochs_for_steps` converts
explicitly (identity under full-batch, where one epoch is one step) and is
itself tested.
"""

import argparse
import logging
import math
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field, fields
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import torch
import yaml

# Repo root on sys.path so `python scripts/phase_diagram_sweep.py` works from
# the root without PYTHONPATH gymnastics (same bootstrap as
# scripts/verify_sae_induction.py). `python -m scripts.phase_diagram_sweep`
# works either way.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.experiments import exp2_grokking, exp6_capstone  # noqa: E402
from src.experiments.runner import run_seeds  # noqa: E402

logger = logging.getLogger(__name__)

RESULTS_DIR = Path("results")
CHECKPOINTS_DIR = Path("checkpoints")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Fallback sparse/dense classification when a manifest predates the energy
# metric (joint cells measured with exp6's L1 k_99; the solo path carries the
# audited energy metric too). The L1-mass k_99 is the metric the 2026-10-08
# audit falsified — it calls a noisy sparse embedding dense — so the energy
# classification wins whenever it is present.
L1_SPARSE_RATIO = 0.5


@dataclass
class SweepCell:
    """A single cell in the phase diagram sweep.

    Axes that select an exp2 protocol deviation are Optional; None means
    "inherit from the protocol preset". Everything else is a pinned value.
    """

    cell_id: str
    modulus: int
    d_model: int
    n_layers: int
    n_heads: int
    d_mlp: int
    weight_decay: float
    mode: str  # "solo" or "joint"
    protocol: str = "nanda"  # exp2 preset: "nanda" (full-batch) or "repo"
    train_fraction: float = 0.3
    lr: float = 1e-3
    steps: int = 2000  # optimizer steps — the only budget unit
    batch_size: int = 128
    warmup_steps: int = 100
    checkpoint_every: int = 500  # in steps
    seed: int = 42  # base seed, actual seeds = seed + 0,1,2
    # Protocol deviations (None = inherit the preset's value)
    schedule: Optional[str] = None
    normalize_embeddings: Optional[bool] = None
    layernorm: Optional[bool] = None
    grad_clip: Optional[float] = None
    beta2: Optional[float] = None
    full_batch: Optional[bool] = None

    @property
    def steps_per_epoch(self) -> int:
        """Optimizer steps in one epoch at this cell's batch size.

        Under full-batch (the Nanda protocol), one epoch IS one step — the
        identity. Under minibatch, one epoch is ceil(n_train_pairs /
        batch_size) steps, which at small moduli is *less than one* batch:
        that is the audit's "at P=29 an epoch is 2 steps" failure, and why
        budgets live in steps.
        """
        if self.full_batch or self.protocol == "nanda":
            return 1
        n_train_pairs = int(self.modulus * self.modulus * self.train_fraction)
        return max(1, math.ceil(n_train_pairs / self.batch_size))

    def epochs_for_steps(self) -> int:
        """Epoch count that realizes `steps` optimizer steps."""
        return max(1, math.ceil(self.steps / self.steps_per_epoch))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "SweepCell":
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})


@dataclass
class CellResult:
    """Aggregated results for one cell (3 seeds)."""

    cell_id: str
    modulus: int
    d_model: int
    n_layers: int
    n_heads: int
    d_mlp: int
    weight_decay: float
    mode: str
    seeds: list[int]
    # Aggregate metrics (mean/std/min/max/n). Optional when the measuring
    # path does not produce them (the joint path has no generalization-epoch
    # or top-k mass measure): absent, never a fabricated zero.
    final_val_acc: dict[str, float]
    generalization_epoch: Optional[dict[str, float]]
    final_fourier_sparsity: dict[str, float]
    k_90_percent: dict[str, float]
    k_99_percent: dict[str, float]
    total_mass_top_k: Optional[dict[str, float]]
    # Everything below has a default: optional metrics, then provenance.
    # Joint-specific metrics (if mode == "joint")
    final_induction_acc: Optional[dict[str, float]] = None
    final_kcomp: Optional[dict[str, float]] = None
    # Energy-metric fields (the audited sparse/dense criterion), solo path only
    k_energy_90: Optional[dict[str, float]] = None
    k_energy_99: Optional[dict[str, float]] = None
    frac_energy_top5: Optional[dict[str, float]] = None
    energy_sparse: Optional[dict[str, float]] = None
    # The raw per-seed metric dicts run_seeds produced — kept so an emitted
    # manifest can carry real per-seed values, not the mean repeated n times.
    per_seed: list[dict[str, float]] = field(default_factory=list)
    wall_clock_seconds: float = 0.0

    def is_sparse(self) -> bool:
        """Sparse-regime classification.

        Prefers the energy metric (a clean 5-frequency embedding with 1%
        noise is correctly called sparse by it; the L1-mass k_99 calls it
        dense). Falls back to the L1 criterion k_99/P < 0.5 for manifests
        recorded before the energy metric existed.
        """
        if self.energy_sparse is not None and self.energy_sparse.get("n", 0):
            return self.energy_sparse["mean"] >= 0.5
        return self.k_99_percent["mean"] < self.modulus * L1_SPARSE_RATIO

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "CellResult":
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})


def _git_short_sha() -> str:
    """Short HEAD sha, or "unknown" when this is not a git checkout.

    Guards the sweep against being run from an exported tarball, where every
    git command fails and the manifest would otherwise lose its provenance.
    """
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], text=True, stderr=subprocess.DEVNULL
            )
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "unknown"


def load_existing_manifest(manifest_path: Path) -> dict[str, CellResult] | None:
    """Load existing phase diagram manifest if it exists."""
    if not manifest_path.exists():
        return None
    try:
        data = torch.load(manifest_path, map_location="cpu", weights_only=False)
        if isinstance(data, dict) and "cells" in data:
            return {k: CellResult.from_dict(v) for k, v in data["cells"].items()}
        return None
    except Exception as e:
        logger.warning(f"Failed to load existing manifest: {e}")
        return None


def save_manifest(
    manifest_path: Path, cells: dict[str, CellResult], metadata: dict[str, Any]
) -> None:
    """Save phase diagram manifest with provenance."""
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "metadata": metadata,
        "cells": {k: v.to_dict() for k, v in cells.items()},
    }
    torch.save(data, manifest_path)
    logger.info(f"Saved sweep manifest to {manifest_path} ({len(cells)} cells)")


# ---------------------------------------------------------------------------
# Cell -> exp2 / exp6 construction (the parity contract)
# ---------------------------------------------------------------------------

ZERO_AGG = {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "n": 0}


def exp2_args_for_cell(cell: SweepCell) -> argparse.Namespace:
    """The argparse namespace exp2 would parse for this cell.

    Built from exp2's own parser (so no field can be missing), then
    `apply_protocol` (so the protocol preset is exp2's code), then the cell's
    explicit deviations. A caller that runs exp2's CLI with the same flags
    gets bit-identical behavior — that is what the parity test pins.
    """
    argv = [
        "--protocol", str(cell.protocol),
        "--modulus", str(cell.modulus),
        "--d-model", str(cell.d_model),
        "--d-mlp", str(cell.d_mlp),
        "--n-heads", str(cell.n_heads),
        "--lr", str(cell.lr),
        "--weight-decay", str(cell.weight_decay),
        "--train-fraction", str(cell.train_fraction),
        "--batch-size", str(cell.batch_size),
        # Budget in steps: full-batch makes epochs == steps; the minibatch
        # deviation converts explicitly (tested in tests/test_phase_diagram_sweep.py).
        "--epochs", str(cell.epochs_for_steps()),
        "--progress-interval", str(max(1, cell.steps // 4)),
        "--checkpoint-every", str(max(1, cell.checkpoint_every // cell.steps_per_epoch)),
    ]
    if cell.schedule is not None:
        argv += ["--schedule", str(cell.schedule)]
    if cell.normalize_embeddings is False:
        argv += ["--no-normalize-embeddings"]
    if cell.layernorm is False:
        argv += ["--no-layernorm"]
    if cell.grad_clip is not None:
        argv += ["--grad-clip", str(cell.grad_clip)]
    if cell.beta2 is not None:
        argv += ["--beta2", str(cell.beta2)]
    if cell.full_batch:
        argv += ["--full-batch"]

    args = exp2_grokking.build_parser().parse_args(argv)
    exp2_grokking.apply_protocol(args)

    # Deviations applied AFTER the preset overwrites: an explicit cell axis
    # always beats the protocol default. (The argv flags above make the
    # equivalent CLI invocation self-documenting; these assignments are what
    # actually win — apply_protocol clobbers parsed values, so every axis
    # that can re-enable a preset-disabled feature must be re-applied here.)
    if cell.schedule is not None:
        args.schedule = cell.schedule
    if cell.normalize_embeddings is True:
        args.no_normalize_embeddings = False
    if cell.layernorm is True:
        args.no_layernorm = False
    if cell.grad_clip is not None:
        args.grad_clip = cell.grad_clip
    if cell.beta2 is not None:
        args.beta2 = cell.beta2
    if cell.full_batch is not None:
        args.full_batch = cell.full_batch
    if cell.warmup_steps is not None:
        # exp2's warmup is counted in epochs; convert so it stays a step count.
        args.warmup_epochs = max(0, math.ceil(cell.warmup_steps / cell.steps_per_epoch))
    # Per-cell checkpoint dir: a shared dir would let a later cell's seed-N
    # rolling checkpoint satisfy an earlier cell's --resume with the wrong
    # weights.
    args.checkpoint_dir = str(CHECKPOINTS_DIR / f"sweep_{cell.cell_id}")
    Path(args.checkpoint_dir).mkdir(parents=True, exist_ok=True)
    return args


def exp6_cfg_for_cell(cell: SweepCell) -> dict[str, Any]:
    """The capstone config dict exp6 expects for this cell.

    Same schema as configs/capstone.yaml, with the cell's axes substituted,
    so `train_single_seed` runs exactly the config it would run from YAML.
    """
    return {
        "task": {
            "name": "modular_addition + induction",
            "modular": {
                "modulus": cell.modulus,
                "train_fraction": cell.train_fraction,
                "vocab_offset": 0,
            },
            "induction": {
                "vocab_size": 2048,
                "seq_len": 128,
                "num_train": 8192,
                "num_val": 1024,
                "prefix_ratio": 0.5,
            },
        },
        "model": {
            "d_model": cell.d_model,
            "n_layers": cell.n_layers,
            "n_heads": cell.n_heads,
            "d_mlp": cell.d_mlp,
            "dropout": 0.1,
            "rotary_base": 10000,
            "rmsnorm_eps": 1e-5,
        },
        "training": {
            "steps": cell.steps,
            "batch_size": cell.batch_size,
            "lr": cell.lr,
            "weight_decay": cell.weight_decay,
            "lr_schedule": "cosine",
            "warmup_steps": cell.warmup_steps,
            "gradient_clip": 1.0,
            "modular_weight": 1.0,
            "induction_weight": 1.0,
            "eval_every": max(1, cell.steps // 4),
        },
        "instrumentation": {
            "fourier_every": max(1, cell.steps // 2),
            "kcomp_every": max(1, cell.steps // 2),
            "sae_hooks": ["ln_final"],
        },
        "checkpoint_every": max(1, cell.checkpoint_every),
    }


def _latest_exp6_step(checkpoint_dir: Path, seed: int) -> int:
    """Highest step recorded for a seed's exp6 checkpoints (0 if none).

    exp6 writes one file per checkpoint (`..._step{S}.pt`), not a rolling
    file, so mid-cell resume across a killed Kaggle session scans for the
    newest step rather than reloading a single path.
    """
    best = 0
    for path in checkpoint_dir.glob(f"exp6_capstone_seed{seed}_step*.pt"):
        try:
            best = max(best, int(path.stem.rsplit("_step", 1)[1]))
        except (IndexError, ValueError):
            continue
    return best


# ---------------------------------------------------------------------------
# Cell runners
# ---------------------------------------------------------------------------

def run_solo_cell(
    cell: SweepCell, seeds: Optional[list[int]] = None
) -> CellResult:
    """Run a solo modular-addition cell THROUGH exp2.

    The sweep is a protocol ablation over exp2's own flags, so the cell is
    an exp2 run: same parser, same protocol application, same training loop,
    same Fourier analysis (including the post-audit energy metric). Before
    this refactor the sweep re-implemented the loop and silently drifted
    from every protocol — a sweep cell matched no exp2 run at any config.

    `seeds` defaults to the cell's [base, base+1, base+2]; tests pass a
    single seed to compare per-seed values against a direct exp2 run.
    """
    args = exp2_args_for_cell(cell)
    if seeds is None:
        seeds = [cell.seed, cell.seed + 1, cell.seed + 2]
    result = run_seeds(lambda s: exp2_grokking.run_single_seed(s, args), seeds)

    # A seed that crashed or diverged can leave a metric absent from the
    # aggregate; fall back to an explicit zero triple rather than a KeyError
    # that would take the whole sweep down after hours of compute.
    def agg(key: str) -> dict[str, float]:
        return result.aggregate.get(key, ZERO_AGG)

    return CellResult(
        cell_id=cell.cell_id,
        modulus=cell.modulus,
        d_model=cell.d_model,
        n_layers=cell.n_layers,
        n_heads=cell.n_heads,
        d_mlp=cell.d_mlp,
        weight_decay=cell.weight_decay,
        mode="solo",
        seeds=seeds,
        wall_clock_seconds=result.wall_clock_seconds,
        final_val_acc=agg("final_val_acc"),
        generalization_epoch=agg("generalization_epoch"),
        final_fourier_sparsity=agg("final_fourier_sparsity"),
        k_90_percent=agg("k_90_percent"),
        k_99_percent=agg("k_99_percent"),
        total_mass_top_k=agg("total_mass_top_k"),
        k_energy_90=agg("k_energy_90"),
        k_energy_99=agg("k_energy_99"),
        frac_energy_top5=agg("frac_energy_top5"),
        energy_sparse=agg("energy_sparse"),
        per_seed=list(result.per_seed),
    )


def run_joint_cell(
    cell: SweepCell, seeds: Optional[list[int]] = None
) -> CellResult:
    """Run a joint modular+induction cell THROUGH exp6.

    exp6's joint loop and instrumentation are the ones the capstone runs;
    the sweep must not carry a second copy. Note the honest limitation:
    exp6 measures Fourier sparsity with its L1 k_99 only — the energy metric
    exists in exp2, not in exp6 — so joint cells classify on the L1
    criterion until exp6 gains the energy metric (tracked follow-up).
    """
    cfg = exp6_cfg_for_cell(cell)
    if seeds is None:
        seeds = [cell.seed, cell.seed + 1, cell.seed + 2]
    checkpoint_dir = CHECKPOINTS_DIR / f"sweep_{cell.cell_id}"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def run_one(seed: int) -> dict[str, float]:
        resume_step = _latest_exp6_step(checkpoint_dir, seed)
        metrics = exp6_capstone.train_single_seed(
            cfg=cfg,
            seed=seed,
            resume_step=resume_step,
            checkpoint_dir=checkpoint_dir,
        )
        # Only what exp6 actually measures. generalization_epoch and
        # total_mass_top_k have no exp6 equivalent; reporting them as
        # -1.0 / 0.0 would fabricate measurements, so they stay absent.
        return {
            "final_val_acc": float(metrics["final_modular_acc"]),
            "final_fourier_sparsity": float(metrics["final_k_99"] / cell.modulus),
            "k_90_percent": float(metrics["final_k_90"]),
            "k_99_percent": float(metrics["final_k_99"]),
            "final_induction_acc": float(metrics["final_induction_acc"]),
            "final_kcomp": float(metrics["final_max_kcomp"]),
        }

    result = run_seeds(run_one, seeds)

    def agg(key: str) -> dict[str, float]:
        return result.aggregate.get(key, ZERO_AGG)

    return CellResult(
        cell_id=cell.cell_id,
        modulus=cell.modulus,
        d_model=cell.d_model,
        n_layers=cell.n_layers,
        n_heads=cell.n_heads,
        d_mlp=cell.d_mlp,
        weight_decay=cell.weight_decay,
        mode="joint",
        seeds=seeds,
        wall_clock_seconds=result.wall_clock_seconds,
        final_val_acc=agg("final_val_acc"),
        generalization_epoch=None,
        final_fourier_sparsity=agg("final_fourier_sparsity"),
        k_90_percent=agg("k_90_percent"),
        k_99_percent=agg("k_99_percent"),
        total_mass_top_k=None,
        final_induction_acc=agg("final_induction_acc"),
        final_kcomp=agg("final_kcomp"),
        per_seed=list(result.per_seed),
    )


def generate_sweep_grid(config: dict) -> list[SweepCell]:
    """Generate cells from explicit config list."""
    cells = []

    # Fixed hyperparameters
    train_fraction = config.get("train_fraction", 0.3)
    lr = config.get("lr", 1e-3)
    batch_size = config.get("batch_size", 128)
    warmup_steps = config.get("warmup_steps", 100)
    checkpoint_every = config.get("checkpoint_every", 500)
    base_seed = config.get("base_seed", 42)
    # Budgets in optimizer steps. `steps_small_p` exists because a full-batch
    # step at P=11 is ~100x cheaper than at P=113; both keys are STEPS, never
    # epochs — the 2026-10-08 audit's untrained small-P cells came from an
    # epoch budget at a modulus where an epoch is a fraction of a step.
    steps_default = config.get("steps", config.get("epochs", 2000))
    steps_small_p = config.get("steps_small_p", config.get("epochs_small_p", 5000))

    for cell_config in config.get("cells", []):
        modulus = cell_config["modulus"]
        steps = steps_small_p if modulus <= 59 else steps_default

        cell = SweepCell(
            cell_id=cell_config["cell_id"],
            modulus=modulus,
            d_model=cell_config["d_model"],
            n_layers=cell_config["n_layers"],
            n_heads=cell_config["n_heads"],
            d_mlp=cell_config["d_mlp"],
            weight_decay=cell_config["weight_decay"],
            mode=cell_config["mode"],
            protocol=cell_config.get("protocol", "nanda"),
            train_fraction=train_fraction,
            lr=lr,
            steps=steps,
            batch_size=batch_size,
            warmup_steps=warmup_steps,
            checkpoint_every=checkpoint_every,
            seed=base_seed,
        )
        cells.append(cell)

    logger.info(f"Generated {len(cells)} explicit cells from config")
    return cells


def emit_cell_manifest(cell: SweepCell, result: CellResult, out_dir: Path) -> Path:
    """Write one cell as a standard ResultsManifest JSON in `out_dir`.

    The .pt sweep manifest is scratch for resume; a number that will be
    cited publicly needs the standard schema `make verify-claims` can
    check (seeds, per-seed metrics, aggregate, git provenance — all stamped
    by ResultsManifest.from_run itself).
    """
    from src.results import ResultsManifest

    n_seeds = len(result.seeds)
    # Only metrics actually measured across all seeds: an aggregate with
    # n=0 (or n != n_seeds) would violate the manifest contract
    # verify_claims enforces, and padding it would fabricate a measurement.
    candidates = {
        "final_val_acc": result.final_val_acc,
        "generalization_epoch": result.generalization_epoch,
        "final_fourier_sparsity": result.final_fourier_sparsity,
        "k_90_percent": result.k_90_percent,
        "k_99_percent": result.k_99_percent,
        "total_mass_top_k": result.total_mass_top_k,
        "final_induction_acc": result.final_induction_acc,
        "final_kcomp": result.final_kcomp,
        # The post-audit criterion — without it a sweep manifest carries the
        # same falsified L1 reading the 2026-10-08 audit removed from the
        # classification path.
        "k_energy_90": result.k_energy_90,
        "k_energy_99": result.k_energy_99,
        "frac_energy_top5": result.frac_energy_top5,
        "energy_sparse": result.energy_sparse,
    }
    aggregate = {
        key: stats
        for key, stats in candidates.items()
        if stats is not None and int(stats.get("n", 0)) == n_seeds
    }
    # Real per-seed values where the run kept them (falling back to the
    # aggregate mean only for a seed whose dict is missing a key — which
    # cannot happen for a key in `aggregate`, since run_seeds requires every
    # seed to report the same keys).
    per_seed_metrics: list[dict[str, float]] = []
    for seed_metrics in result.per_seed[:n_seeds]:
        per_seed_metrics.append(
            {key: float(seed_metrics.get(key, stats["mean"])) for key, stats in aggregate.items()}
        )
    while len(per_seed_metrics) < n_seeds:  # pragma: no cover - defensive
        per_seed_metrics.append({key: stats["mean"] for key, stats in aggregate.items()})
    manifest = ResultsManifest.from_run(
        experiment=f"phase_diagram_{cell.cell_id}",
        seeds=list(result.seeds),
        args=cell.to_dict(),
        per_seed_metrics=per_seed_metrics,
        aggregate=aggregate,
        wall_clock_seconds=result.wall_clock_seconds,
        device=str(DEVICE),
    )
    out_path = out_dir / f"phase_diagram_{cell.cell_id}.json"
    manifest.save(out_path)
    logger.info(f"Emitted citable manifest {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Phase Diagram Sweep Runner")
    parser.add_argument("--config", type=str, default="configs/phase_diagram_sweep.yaml")
    parser.add_argument("--manifest-path", type=str, default="results/phase_diagram.pt")
    parser.add_argument(
        "--max-cells", type=int, default=None, help="Limit number of cells (for testing)"
    )
    parser.add_argument("--dry-run", action="store_true", help="Print cells without running")
    parser.add_argument("--resume", action="store_true", help="Resume from existing manifest")
    parser.add_argument(
        "--emit-manifests",
        type=str,
        default=None,
        help="Directory for per-cell citable ResultsManifest JSON files (e.g. results/)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    # Load config
    with open(args.config) as f:
        config = yaml.safe_load(f)

    # Generate grid
    cells = generate_sweep_grid(config)

    if args.max_cells:
        cells = cells[: args.max_cells]
        logger.info(f"Limited to {args.max_cells} cells")

    if args.dry_run:
        for cell in cells:
            logger.info(
                f"  {cell.cell_id}: P={cell.modulus}, d_model={cell.d_model}, "
                f"n_layers={cell.n_layers}, wd={cell.weight_decay}, mode={cell.mode}, "
                f"protocol={cell.protocol}, steps={cell.steps} "
                f"(epochs={cell.epochs_for_steps()})"
            )
        return

    # Load existing manifest if resuming
    manifest_path = Path(args.manifest_path)
    existing = load_existing_manifest(manifest_path) if args.resume else {}
    completed = set(existing.keys()) if existing else set()

    # Filter out completed cells
    cells_to_run = [c for c in cells if c.cell_id not in completed]
    logger.info(f"Cells to run: {len(cells_to_run)} (completed: {len(completed)})")

    if not cells_to_run:
        logger.info("All cells already completed!")
        return

    # Run cells
    cells_results = dict(existing) if existing else {}
    start_time = time.monotonic()
    metadata: dict[str, Any] = {}  # Initialize early
    emit_dir = Path(args.emit_manifests) if args.emit_manifests else None
    if emit_dir is not None:
        emit_dir.mkdir(parents=True, exist_ok=True)

    for i, cell in enumerate(cells_to_run):
        logger.info(
            f"[{i+1}/{len(cells_to_run)}] Running {cell.cell_id}: "
            f"P={cell.modulus}, d_model={cell.d_model}, "
            f"n_layers={cell.n_layers}, wd={cell.weight_decay}, mode={cell.mode}"
        )

        try:
            if cell.mode == "solo":
                result = run_solo_cell(cell)
            else:
                result = run_joint_cell(cell)

            cells_results[cell.cell_id] = result

            # Save incrementally
            metadata = {
                "config": config,
                "git_sha": _git_short_sha(),
                "started_at": datetime.fromtimestamp(start_time, tz=timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "total_cells": len(cells),
                "completed_cells": len(cells_results),
            }
            save_manifest(manifest_path, cells_results, metadata)
            if emit_dir is not None:
                emit_cell_manifest(cell, result, emit_dir)

            logger.info(
                f"  -> val_acc={result.final_val_acc['mean']:.4f}, "
                f"k_99/P={result.k_99_percent['mean']/cell.modulus:.3f}, "
                f"sparse={result.is_sparse()}"
            )

        except Exception as e:
            logger.error(f"Cell {cell.cell_id} failed: {e}")
            import traceback

            traceback.print_exc()
            # Continue with other cells

    total_time = time.monotonic() - start_time
    logger.info(
        f"Sweep complete: {len(cells_results)}/{len(cells)} cells in {total_time / 60:.1f} min"
    )

    # Final save
    metadata["completed_at"] = datetime.now(timezone.utc).isoformat()
    metadata["total_wall_clock_seconds"] = total_time
    save_manifest(manifest_path, cells_results, metadata)

    # Summary
    sparse_cells = sum(1 for r in cells_results.values() if r.is_sparse())
    logger.info(f"Sparse regime cells: {sparse_cells}/{len(cells_results)}")


if __name__ == "__main__":
    main()
