"""Capstone energy re-analysis from checkpoints (issue #170 follow-up).

Guardrails:
- Extracting the modular-addition embedding slice and running exp2's
  fourier_energy_sparsity on it must classify a synthetic single-frequency
  embedding as sparse (k_energy_90 small) — this is the computation the
  re-analysis performs on the real checkpoints.
- The real checkpoints live in gitignored scratch (results/remote/), so the
  end-to-end test runs only when they are present; it never gates CI on
  scratch files.
"""

import math

import torch

from src.experiments.exp2_grokking import fourier_energy_sparsity
from src.models.decoder_only_transformer import DecoderOnlyTransformer
from scripts.capstone_energy_from_checkpoints import _energy_from_checkpoint


def _single_frequency_embedding(P: int, d_model: int, k: int = 1) -> torch.Tensor:
    """An embedding whose only Fourier energy is at frequency k (plus DC=0)."""
    positions = torch.arange(P).float()
    emb = torch.zeros(P, d_model)
    # Two dims carry a sine/cosine pair at frequency k -> one folded frequency.
    emb[:, 0] = torch.sin(2 * math.pi * k * positions / P)
    emb[:, 1] = torch.cos(2 * math.pi * k * positions / P)
    return emb


def test_single_frequency_embedding_is_sparse() -> None:
    P, d_model = 113, 16
    emb = _single_frequency_embedding(P, d_model, k=1)
    energy = fourier_energy_sparsity(emb, P)
    # One folded frequency carries 100% of the energy -> k_energy_90 == 1.
    assert energy["k_energy_90"] == 1
    assert energy["is_sparse"] is True
    assert abs(energy["frac_energy_top5"] - 1.0) < 1e-6


def test_real_checkpoint_energy_if_present() -> None:
    """End-to-end on the real capstone checkpoints — skipped if the scratch
    directory has not been restored (gitignored, not part of the repo)."""
    import glob

    paths = sorted(
        glob.glob(
            "results/remote/capstone-20k/output3/repo/checkpoints/"
            "exp6_capstone_seed*_step20000.pt"
        )
    )
    if not paths:
        import pytest

        pytest.skip("capstone checkpoints not on disk (gitignored scratch)")

    import yaml

    with open("configs/capstone.yaml") as f:
        cfg = yaml.safe_load(f)
    for path in paths:
        m = _energy_from_checkpoint(__import__("pathlib").Path(path), cfg)
        for key in ("k_energy_90", "k_energy_99", "frac_energy_top5", "energy_sparse"):
            assert key in m
        assert 0.0 <= m["frac_energy_top5"] <= 1.0
        assert m["energy_sparse"] in (0.0, 1.0)
