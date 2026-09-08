"""Retune A/B harness for exp6: vocab-offset + curriculum reweight.

MP-88 Row 1 verdict (dated 2026-09-07): joint training is viable but
imbalanced — induction 0.0005 -> 0.5041 while modular stays at 0.0047
(below chance 1/113) with Fourier dense (k_99 = 98.1). Two standing
hypotheses, in order: (a) shared-embedding overlap (modular ids 0..P-1
collide with induction token ids) harms the modular readout; (b) the
1.0/1.0 curriculum lets induction dominate (modular supervises 1 token
at logits[:, 1] while induction supervises 127 LM tokens).

Contract pinned here:
1. --vocab-offset relocates modular ids to a dedicated range
   [offset, offset+P) with pad at offset+P — zero overlap with
   induction ids [0, induction_vocab). Offset + P must fit in
   vocab_size or the run fails loudly (ValueError), never silently.
2. --modular-weight / --induction-weight override the config curriculum
   and change loss scaling only — data, model, and instrumentation
   stay identical across arms.
3. Arms differ in exactly one intervention each; probe manifests keep
   flagship bytes untouched (see test_exp6_manifest_path.py).
"""

from src.experiments.exp6_capstone import (
    build_parser,
    make_mixed_dataloaders,
    make_modular_addition_data,
)


def _tiny_cfg(vocab_offset: int = 0) -> dict:
    return {
        "task": {
            "modular": {
                "modulus": 7,
                "train_fraction": 0.5,
                "vocab_offset": vocab_offset,
            },
            "induction": {
                "vocab_size": 32,
                "seq_len": 8,
                "num_train": 64,
                "num_val": 16,
                "prefix_ratio": 0.5,
            },
        },
        "model": {
            "d_model": 16,
            "n_layers": 1,
            "n_heads": 2,
            "d_mlp": 32,
            "dropout": 0.0,
            "rotary_base": 10000,
            "rmsnorm_eps": 1e-5,
        },
        "training": {
            "steps": 4,
            "batch_size": 8,
            "lr": 1e-3,
            "weight_decay": 0.0,
            "warmup_steps": 1,
            "gradient_clip": 1.0,
            "modular_weight": 1.0,
            "induction_weight": 1.0,
        },
        "instrumentation": {
            "fourier_every": 10**9,
            "kcomp_every": 10**9,
        },
        "checkpoint_every": 2,
    }


def test_vocab_offset_defaults_to_zero() -> None:
    """Without the flag, modular ids stay at 0..P-1 (frozen control)."""
    args = build_parser().parse_args([])
    assert args.vocab_offset is None
    cfg = _tiny_cfg()
    assert cfg["task"]["modular"].get("vocab_offset", 0) == 0


def test_vocab_offset_flag_accepted() -> None:
    """Offset arm: dedicated id range for modular tokens."""
    args = build_parser().parse_args(["--vocab-offset", "32"])
    assert args.vocab_offset == 32


def test_reweight_flags_default_to_none() -> None:
    """Curriculum overrides must be explicit, never silent."""
    args = build_parser().parse_args([])
    assert args.modular_weight is None
    assert args.induction_weight is None


def test_reweight_flags_accepted() -> None:
    """Reweight arm: curriculum knobs turn without touching anything else."""
    args = build_parser().parse_args(
        ["--modular-weight", "5.0", "--induction-weight", "0.5"]
    )
    assert args.modular_weight == 5.0
    assert args.induction_weight == 0.5


def test_vocab_offset_eliminates_collision() -> None:
    """Offset modular ids must not overlap induction ids."""
    cfg = _tiny_cfg(vocab_offset=32)
    mod_train, _ = make_modular_addition_data(
        modulus=7, train_fraction=0.5, seq_len=8, seed=0, vocab_offset=32
    )
    x = mod_train.tensors[0]
    assert int(x.min()) >= 32, f"modular ids leak below offset: {int(x.min())}"
    assert int(x.max()) < 32 + 7 + 1, f"modular ids exceed range: {int(x.max())}"
    # Induction ids live in [0, 32); modular in [32, 40) — disjoint.
    train_loader, _ = make_mixed_dataloaders(cfg, seed=0)
    seen_mod_ids = set()
    for batch in train_loader:
        bx, _, _, task_id = batch
        if task_id == 0:
            seen_mod_ids.update(int(v) for v in bx.flatten().tolist())
    assert seen_mod_ids, "no modular batches seen"
    assert min(seen_mod_ids) >= 32


def test_vocab_offset_overflow_fails_loudly() -> None:
    """Offset + P beyond vocab must raise, never silently wrap."""
    import pytest

    cfg = _tiny_cfg(vocab_offset=10**9)
    # Model vocab here would be 32 + 7 + 10 = 49; offset 1e9 cannot fit.
    with pytest.raises(ValueError, match="[Oo]ffset"):
        make_mixed_dataloaders(cfg, seed=0)
