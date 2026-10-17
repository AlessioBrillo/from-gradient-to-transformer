"""Phase diagram sweep: parity with exp2/exp6, step budgets, citable manifests.

The sweep's original sin (issue #168) was that it re-implemented exp2's
training loop with its own epoch budgets, so a sweep cell matched no exp2 run
at any config — and at P=29 "one epoch" was two steps, so small-modulus cells
were silently undertrained. These tests pin the refactored contract:

- a solo cell IS an exp2 run: same seed + same cell -> identical metrics
  through the sweep and through exp2 directly (the drift falsifier);
- budgets are optimizer steps, converted to epochs explicitly and tested
  at the exact modulus the audit caught (P=29, 2 steps/epoch);
- protocol deviations override the preset, never the other way round;
- the emitted per-cell manifest is a ResultsManifest `make verify-claims`
  accepts, so a sweep number can be cited without hand-written JSON.
"""

from __future__ import annotations

from scripts.phase_diagram_sweep import (
    CellResult,
    SweepCell,
    emit_cell_manifest,
    exp2_args_for_cell,
    exp6_cfg_for_cell,
    generate_sweep_grid,
    run_joint_cell,
    run_solo_cell,
)

ZERO_AGG = {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "n": 0}


def _tiny_solo_cell(**overrides) -> SweepCell:
    kwargs = dict(
        cell_id="parity",
        modulus=11,
        d_model=16,
        n_layers=1,
        n_heads=2,
        d_mlp=32,
        weight_decay=1.0,
        mode="solo",
        protocol="nanda",
        steps=3,
        seed=42,
        checkpoint_every=0,
    )
    kwargs.update(overrides)
    return SweepCell(**kwargs)


class TestExp2ArgsMapping:
    """The cell -> exp2 namespace mapping is the parity contract."""

    def test_nanda_protocol_is_applied(self) -> None:
        args = exp2_args_for_cell(_tiny_solo_cell())
        # NANDA_PROTOCOL values, applied by exp2's own apply_protocol.
        assert args.full_batch is True
        assert args.no_layernorm is True
        assert args.no_normalize_embeddings is True
        assert args.grad_clip == 0.0
        assert args.beta2 == 0.98
        assert args.schedule == "constant"

    def test_full_batch_epochs_equal_steps(self) -> None:
        """The identity that makes 'steps' an honest budget unit under the
        Nanda protocol: one epoch is one optimizer step."""
        cell = _tiny_solo_cell(modulus=113, steps=2000)
        args = exp2_args_for_cell(cell)
        assert cell.steps_per_epoch == 1
        assert args.epochs == 2000

    def test_minibatch_budget_converted_to_epochs(self) -> None:
        """The 2026-10-08 audit's untrained small-P cells: at P=29 an epoch
        is 2 steps, so an epoch budget silently halves the training. A step
        budget must convert explicitly."""
        cell = _tiny_solo_cell(
            modulus=29, protocol="repo", full_batch=False, steps=2000, batch_size=128
        )
        # ceil(29^2 * 0.3 / 128) = ceil(252/128) = 2 steps per epoch
        assert cell.steps_per_epoch == 2
        assert cell.epochs_for_steps() == 1000
        args = exp2_args_for_cell(cell)
        assert args.epochs == 1000

    def test_deviations_override_the_preset(self) -> None:
        cell = _tiny_solo_cell(
            protocol="nanda",
            schedule="cosine",
            normalize_embeddings=True,
            layernorm=True,
            grad_clip=1.0,
            beta2=0.999,
        )
        args = exp2_args_for_cell(cell)
        assert args.schedule == "cosine"  # cosine over the preset's constant
        assert args.no_normalize_embeddings is False  # renorm re-enabled
        assert args.no_layernorm is False  # LayerNorm re-enabled
        assert args.grad_clip == 1.0
        assert args.beta2 == 0.999

    def test_progress_interval_scales_with_budget(self) -> None:
        args = exp2_args_for_cell(_tiny_solo_cell(steps=400))
        assert args.progress_interval == 100

    def test_checkpoint_dir_is_per_cell(self) -> None:
        """A shared checkpoint dir would let cell B's seed-N checkpoint
        satisfy cell A's resume with the wrong weights."""
        args = exp2_args_for_cell(_tiny_solo_cell(cell_id="p113_wd1"))
        assert "sweep_p113_wd1" in args.checkpoint_dir


class TestSoloCellMatchesExp2:
    """The drift falsifier: the sweep and a direct exp2 run at the same
    seed + config must produce identical numbers."""

    def test_same_seed_and_config_give_identical_metrics(self) -> None:
        from src.experiments import exp2_grokking

        cell = _tiny_solo_cell()
        sweep_result = run_solo_cell(cell, seeds=[42])
        direct = exp2_grokking.run_single_seed(42, exp2_args_for_cell(cell))

        # With one seed the aggregate mean IS that seed's value.
        assert abs(sweep_result.final_val_acc["mean"] - direct["final_val_acc"]) < 1e-12
        assert (
            abs(sweep_result.k_90_percent["mean"] - direct["k_90_percent"]) < 1e-12
        )
        assert (
            abs(sweep_result.k_99_percent["mean"] - direct["k_99_percent"]) < 1e-12
        )
        assert (
            abs(sweep_result.k_energy_90["mean"] - direct["k_energy_90"]) < 1e-12
        )
        assert sweep_result.energy_sparse["mean"] == direct["energy_sparse"]

    def test_solo_cell_carries_the_energy_metric(self) -> None:
        """The L1 k_99 is the audited metric; the sweep must record the
        energy metric that replaced it, or its sparse/dense labels repeat
        the falsified classification."""
        result = run_solo_cell(_tiny_solo_cell(), seeds=[42])
        assert result.k_energy_90 is not None
        assert result.energy_sparse is not None
        assert result.energy_sparse["n"] == 1


class TestJointCellDelegation:
    def test_cfg_matches_the_capstone_schema(self) -> None:
        cfg = exp6_cfg_for_cell(
            _tiny_solo_cell(cell_id="joint", mode="joint", modulus=59, steps=50)
        )
        assert cfg["task"]["modular"]["modulus"] == 59
        assert cfg["training"]["steps"] == 50
        assert cfg["model"]["d_model"] == 16
        # The keys train_single_seed reads — a missing one is a KeyError
        # hours into a sweep.
        assert set(cfg["instrumentation"]) >= {"fourier_every", "kcomp_every"}
        assert cfg["checkpoint_every"] >= 1

    def test_tiny_joint_cell_runs(self) -> None:
        """End-to-end through exp6's own train_single_seed: if the cfg
        shape drifts from what exp6 consumes, this fails cheaply instead of
        at sweep time."""
        cell = _tiny_solo_cell(
            cell_id="joint_tiny",
            mode="joint",
            modulus=11,
            steps=2,
            batch_size=8,
            checkpoint_every=0,
        )
        result = run_joint_cell(cell, seeds=[42])
        assert result.final_val_acc["n"] == 1
        assert 0.0 <= result.final_val_acc["mean"] <= 1.0
        assert result.final_induction_acc is not None
        assert result.final_kcomp is not None
        # exp6 now emits the post-audit energy metric; joint cells must carry
        # it (never classify on the falsified L1 k_99 alone).
        assert result.k_energy_90 is not None and result.k_energy_90["n"] == 1
        assert result.energy_sparse is not None and result.energy_sparse["n"] == 1


class TestBudgetUnits:
    """Budgets live in steps; the config speaks steps, not epochs."""

    def test_grid_reads_steps_keys(self) -> None:
        config = {
            "steps": 2000,
            "steps_small_p": 5000,
            "cells": [
                {"cell_id": "a", "modulus": 113, "d_model": 128, "n_layers": 1,
                 "n_heads": 4, "d_mlp": 512, "weight_decay": 1.0, "mode": "solo"},
                {"cell_id": "b", "modulus": 11, "d_model": 128, "n_layers": 1,
                 "n_heads": 4, "d_mlp": 512, "weight_decay": 1.0, "mode": "solo"},
            ],
        }
        cells = generate_sweep_grid(config)
        assert cells[0].steps == 2000
        assert cells[1].steps == 5000  # small-P budget, still in STEPS

    def test_legacy_epochs_keys_read_as_steps(self) -> None:
        config = {
            "epochs": 1500,
            "cells": [
                {"cell_id": "a", "modulus": 113, "d_model": 128, "n_layers": 1,
                 "n_heads": 4, "d_mlp": 512, "weight_decay": 1.0, "mode": "solo"},
            ],
        }
        cells = generate_sweep_grid(config)
        assert cells[0].steps == 1500

    def test_no_cell_field_is_named_epochs(self) -> None:
        assert not hasattr(SweepCell(cell_id="x", modulus=11, d_model=16,
                                     n_layers=1, n_heads=2, d_mlp=32,
                                     weight_decay=1.0, mode="solo"), "epochs")


class TestEmitCellManifest:
    """A cited sweep number needs the standard manifest schema."""

    def test_emitted_manifest_loads_as_results_manifest(self, tmp_path) -> None:
        from src.results import ResultsManifest

        cell = _tiny_solo_cell(cell_id="emit")
        result = CellResult(
            cell_id="emit",
            modulus=cell.modulus,
            d_model=cell.d_model,
            n_layers=cell.n_layers,
            n_heads=cell.n_heads,
            d_mlp=cell.d_mlp,
            weight_decay=cell.weight_decay,
            mode="solo",
            seeds=[42, 43, 44],
            wall_clock_seconds=1.0,
            final_val_acc={"mean": 0.5, "std": 0.1, "min": 0.4, "max": 0.6, "n": 3},
            generalization_epoch=dict(ZERO_AGG),
            final_fourier_sparsity=dict(ZERO_AGG),
            k_90_percent=dict(ZERO_AGG),
            k_99_percent={"mean": 10.0, "std": 0.0, "min": 10.0, "max": 10.0, "n": 3},
            total_mass_top_k=dict(ZERO_AGG),
        )
        out = emit_cell_manifest(cell, result, tmp_path)
        loaded = ResultsManifest.load(out)
        # Exactly the structural checks verify_claims applies.
        assert len(loaded.seeds) == len(loaded.per_seed_metrics)
        for stats in loaded.aggregate.values():
            assert int(stats["n"]) == len(loaded.seeds)
        assert loaded.experiment == "phase_diagram_emit"

    def test_unmeasured_metrics_are_dropped_not_fabricated(self, tmp_path) -> None:
        """A ZERO_AGG (n=0) metric must not be emitted — padding it would
        fabricate a measurement and break the manifest contract."""
        cell = _tiny_solo_cell(cell_id="emit2")
        result = CellResult(
            cell_id="emit2",
            modulus=cell.modulus,
            d_model=cell.d_model,
            n_layers=cell.n_layers,
            n_heads=cell.n_heads,
            d_mlp=cell.d_mlp,
            weight_decay=cell.weight_decay,
            mode="joint",
            seeds=[42, 43, 44],
            final_val_acc={"mean": 0.5, "std": 0.1, "min": 0.4, "max": 0.6, "n": 3},
            generalization_epoch=None,
            final_fourier_sparsity=dict(ZERO_AGG),
            k_90_percent=dict(ZERO_AGG),
            k_99_percent=dict(ZERO_AGG),
            total_mass_top_k=None,
        )
        out = emit_cell_manifest(cell, result, tmp_path)
        from src.results import ResultsManifest

        loaded = ResultsManifest.load(out)
        assert set(loaded.aggregate) == {"final_val_acc"}

    def test_emitted_manifest_carries_real_per_seed_values(self, tmp_path) -> None:
        """Per-seed records must be the seeds' own values, not the mean
        printed n times — the aggregate is a summary, not the source."""
        from src.results import ResultsManifest

        cell = _tiny_solo_cell(cell_id="emit3")
        result = CellResult(
            cell_id="emit3",
            modulus=cell.modulus,
            d_model=cell.d_model,
            n_layers=cell.n_layers,
            n_heads=cell.n_heads,
            d_mlp=cell.d_mlp,
            weight_decay=cell.weight_decay,
            mode="solo",
            seeds=[42, 43, 44],
            final_val_acc={"mean": 0.5, "std": 0.1, "min": 0.4, "max": 0.6, "n": 3},
            generalization_epoch=dict(ZERO_AGG),
            final_fourier_sparsity=dict(ZERO_AGG),
            k_90_percent=dict(ZERO_AGG),
            k_99_percent=dict(ZERO_AGG),
            total_mass_top_k=dict(ZERO_AGG),
            per_seed=[
                {"final_val_acc": 0.4},
                {"final_val_acc": 0.5},
                {"final_val_acc": 0.6},
            ],
        )
        out = emit_cell_manifest(cell, result, tmp_path)
        loaded = ResultsManifest.load(out)
        assert [m["final_val_acc"] for m in loaded.per_seed_metrics] == [0.4, 0.5, 0.6]

    def test_emitted_manifest_carries_the_energy_metric(self, tmp_path) -> None:
        """A sweep manifest without the post-audit energy metric carries the
        same falsified L1 reading the 2026-10-08 audit removed — the
        classification must be decidable from the manifest alone."""
        from src.results import ResultsManifest

        cell = _tiny_solo_cell(cell_id="emit4")
        result = CellResult(
            cell_id="emit4",
            modulus=cell.modulus,
            d_model=cell.d_model,
            n_layers=cell.n_layers,
            n_heads=cell.n_heads,
            d_mlp=cell.d_mlp,
            weight_decay=cell.weight_decay,
            mode="solo",
            seeds=[42, 43, 44],
            final_val_acc={"mean": 1.0, "std": 0.0, "min": 1.0, "max": 1.0, "n": 3},
            generalization_epoch=dict(ZERO_AGG),
            final_fourier_sparsity=dict(ZERO_AGG),
            k_90_percent=dict(ZERO_AGG),
            k_99_percent={"mean": 110.0, "std": 0.0, "min": 110.0, "max": 110.0, "n": 3},
            total_mass_top_k=dict(ZERO_AGG),
            k_energy_90={"mean": 5.7, "std": 1.2, "min": 4.0, "max": 7.0, "n": 3},
            frac_energy_top5={"mean": 0.87, "std": 0.04, "min": 0.83, "max": 0.92, "n": 3},
            energy_sparse={"mean": 1.0, "std": 0.0, "min": 1.0, "max": 1.0, "n": 3},
        )
        out = emit_cell_manifest(cell, result, tmp_path)
        loaded = ResultsManifest.load(out)
        assert "energy_sparse" in loaded.aggregate
        assert loaded.aggregate["energy_sparse"]["mean"] == 1.0
        assert loaded.aggregate["k_energy_90"]["mean"] == 5.7

    def test_sparse_classification_prefers_energy_metric(self) -> None:
        """is_sparse must classify on the energy metric when present: the
        L1 k_99 calls a noisy sparse embedding dense, which is the exact
        misclassification the 2026-10-08 audit pinned."""
        result = CellResult(
            cell_id="s", modulus=113, d_model=128, n_layers=1, n_heads=4,
            d_mlp=512, weight_decay=1.0, mode="solo", seeds=[42],
            wall_clock_seconds=1.0,
            final_val_acc=dict(ZERO_AGG),
            generalization_epoch=dict(ZERO_AGG),
            final_fourier_sparsity=dict(ZERO_AGG),
            k_90_percent=dict(ZERO_AGG),
            k_99_percent={"mean": 111.0, "std": 0.0, "min": 111.0, "max": 111.0, "n": 1},
            total_mass_top_k=dict(ZERO_AGG),
            energy_sparse={"mean": 1.0, "std": 0.0, "min": 1.0, "max": 1.0, "n": 1},
        )
        # L1 says dense (111/113), energy says sparse -> energy wins.
        assert result.is_sparse() is True

    def test_falls_back_to_l1_without_energy_metric(self) -> None:
        result = CellResult(
            cell_id="s", modulus=113, d_model=128, n_layers=1, n_heads=4,
            d_mlp=512, weight_decay=1.0, mode="solo", seeds=[42],
            wall_clock_seconds=1.0,
            final_val_acc=dict(ZERO_AGG),
            generalization_epoch=dict(ZERO_AGG),
            final_fourier_sparsity=dict(ZERO_AGG),
            k_90_percent=dict(ZERO_AGG),
            k_99_percent={"mean": 111.0, "std": 0.0, "min": 111.0, "max": 111.0, "n": 1},
            total_mass_top_k=dict(ZERO_AGG),
        )
        assert result.is_sparse() is False


class TestGridReadsPerCellDeviations:
    """generate_sweep_grid must honour per-cell protocol deviations and
    per-cell step budgets — otherwise the ablation config expresses nothing
    and the sweep silently re-runs the preset (issue #168's design gap)."""

    def test_grid_reads_per_cell_deviations(self) -> None:
        config = {
            "steps": 2000,
            "cells": [
                {
                    "cell_id": "base",
                    "modulus": 113,
                    "d_model": 128,
                    "n_layers": 1,
                    "n_heads": 4,
                    "d_mlp": 512,
                    "weight_decay": 1.0,
                    "mode": "solo",
                    "protocol": "nanda",
                },
                {
                    "cell_id": "dev_minibatch",
                    "modulus": 113,
                    "d_model": 128,
                    "n_layers": 1,
                    "n_heads": 4,
                    "d_mlp": 512,
                    "weight_decay": 1.0,
                    "mode": "solo",
                    "protocol": "nanda",
                    "batch_size": 512,
                    "full_batch": False,
                    "steps": 5000,
                },
                {
                    "cell_id": "dev_cosine",
                    "modulus": 113,
                    "d_model": 128,
                    "n_layers": 1,
                    "n_heads": 4,
                    "d_mlp": 512,
                    "weight_decay": 1.0,
                    "mode": "solo",
                    "protocol": "nanda",
                    "schedule": "cosine",
                    "normalize_embeddings": True,
                    "layernorm": True,
                    "grad_clip": 1.0,
                    "beta2": 0.999,
                },
            ],
        }
        cells = {c.cell_id: c for c in generate_sweep_grid(config)}

        base = cells["base"]
        assert base.schedule is None
        assert base.normalize_embeddings is None
        assert base.full_batch is None
        assert base.steps == 2000

        dev = cells["dev_minibatch"]
        assert dev.full_batch is False
        assert dev.batch_size == 512
        assert dev.steps == 5000  # per-cell budget overrides the top-level

        cosine = cells["dev_cosine"]
        assert cosine.schedule == "cosine"
        assert cosine.normalize_embeddings is True
        assert cosine.layernorm is True
        assert cosine.grad_clip == 1.0
        assert cosine.beta2 == 0.999
        assert cosine.steps == 2000  # fell back to the top-level budget


class TestBatchSizePropagatesToExp2:
    """batch_size was defined on SweepCell but never forwarded to exp2's
    args, so a minibatch deviation cell trained at exp2's parser default
    instead of the cell's batch size."""

    def test_batch_size_reaches_exp2_args(self) -> None:
        cell = _tiny_solo_cell(batch_size=256)
        args = exp2_args_for_cell(cell)
        assert args.batch_size == 256
