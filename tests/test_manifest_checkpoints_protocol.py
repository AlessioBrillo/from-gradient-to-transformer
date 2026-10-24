"""Protocol-aware checkpoint re-analysis for manifest_from_checkpoints.py.

Guardrails (2026-10-16):
- A checkpoint cannot be loaded with the wrong architecture: the Nanda
  protocol (no embedding re-normalization, no LayerNorm) and the historical
  repo default (both on) must select the matching OneLayerTransformer flags,
  else load_state_dict raises a size-mismatch error.
- The post-audit energy metric (k_energy_90 / frac_energy_top5 / energy_sparse)
  is recomputed from the embedding and lands in every exp2 re-analysis manifest.
"""

from argparse import Namespace

import torch

from scripts.manifest_from_checkpoints import (
    PROTOCOL_ARCH,
    arch_for_protocol,
    exp2_metrics,
)
from src.experiments.exp2_grokking import OneLayerTransformer


def _tmp_checkpoint(tmp_path, modulus: int, protocol: str, seed: int = 42) -> str:
    """Build + save a tiny exp2-style rolling checkpoint for `protocol`."""
    normalize_embed, use_layernorm = arch_for_protocol(protocol)
    model = OneLayerTransformer(
        d_model=16, d_mlp=32, n_heads=4, modulus=modulus,
        normalize_embed=normalize_embed, use_layernorm=use_layernorm,
    )
    ckpt = {
        "epoch": 9,
        "model": model.state_dict(),
        "history": {
            "val_acc": [0.1, 0.5, 0.9, 1.0],
            "fourier_sparsity": [0.5, 0.3, 0.15, 0.1],
        },
    }
    path = tmp_path / f"exp2_checkpoint_seed{seed}.pt"
    torch.save(ckpt, path)
    return str(path)


def _args(modulus: int, protocol: str, **overrides) -> Namespace:
    base = dict(
        modulus=modulus, d_model=16, d_mlp=32, n_heads=4,
        train_fraction=0.3, batch_size=64, checkpoint_every=500,
        protocol=protocol,
    )
    base.update(overrides)
    return Namespace(**base)


def test_arch_for_protocol_mapping() -> None:
    assert arch_for_protocol("repo") == (True, True)
    assert arch_for_protocol("nanda") == (False, False)
    assert set(PROTOCOL_ARCH) == {"repo", "nanda"}


def test_reanalysis_returns_energy_metric(tmp_path) -> None:
    path = _tmp_checkpoint(tmp_path, modulus=11, protocol="repo")
    metrics = exp2_metrics(path, _args(11, "repo"))
    for key in ("k_energy_90", "k_energy_99", "frac_energy_top5", "energy_sparse"):
        assert key in metrics, f"missing energy field {key}"
    assert 0.0 <= metrics["frac_energy_top5"] <= 1.0 + 1e-6
    assert metrics["energy_sparse"] in (0.0, 1.0)
    assert metrics["final_val_acc"] == 1.0


def test_wrong_protocol_cannot_load_checkpoint(tmp_path) -> None:
    """Falsifier: a nanda-arch checkpoint must not load under repo protocol."""
    path = _tmp_checkpoint(tmp_path, modulus=11, protocol="nanda")
    try:
        exp2_metrics(path, _args(11, "repo"))
    except RuntimeError:
        pass  # wrong architecture -> load failure: the property under test
    else:
        raise AssertionError(
            "loading a nanda checkpoint with repo architecture should raise"
        )


def test_nanda_protocol_loads_its_own_checkpoint(tmp_path) -> None:
    path = _tmp_checkpoint(tmp_path, modulus=11, protocol="nanda")
    metrics = exp2_metrics(path, _args(11, "nanda"))
    assert metrics["final_val_acc"] == 1.0
    assert "k_energy_90" in metrics
