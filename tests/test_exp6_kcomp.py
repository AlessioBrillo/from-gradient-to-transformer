"""K-composition in exp6 must measure, not emit vacuous zeros.

The old compute_k_composition_scores appended 0.0 per head without reading
the attention cache. These tests pin the real port: induction batches yield
schema-valid per-head scores in [0, 1] with diagnosis metadata, while a
modular-only loader returns an explicit vacuous marker that callers must
not plot as a result.
"""

import torch
from torch.utils.data import DataLoader, TensorDataset

from src.experiments.exp6_capstone import compute_k_composition_scores
from src.models.decoder_only_transformer import DecoderOnlyTransformer


def _model() -> DecoderOnlyTransformer:
    return DecoderOnlyTransformer(
        vocab_size=64, d_model=16, n_layers=2, n_heads=2, d_mlp=32, dropout=0.0
    )


def _induction_loader() -> DataLoader:
    x = torch.randint(0, 64, (8, 11))
    y = torch.randint(0, 64, (8, 11))
    return DataLoader(TensorDataset(x, y), batch_size=4)


def test_kcomp_on_induction_returns_scores_not_zeros() -> None:
    scores = compute_k_composition_scores(_model(), _induction_loader(), num_batches=2)
    assert not scores.get("_vacuous", False)
    head_keys = [k for k in scores if not k.startswith("_")]
    assert len(head_keys) == 2, f"expected 2 L1 heads, got {head_keys}"
    for k in head_keys:
        assert 0.0 <= scores[k] <= 1.0
    assert "_diagnosis_step2" in scores


def test_kcomp_on_modular_only_is_vacuous() -> None:
    x = torch.zeros(4, 7, dtype=torch.long)
    y = torch.zeros(4, 7, dtype=torch.long)
    t = torch.zeros(4, dtype=torch.long)
    mod_loader = DataLoader(TensorDataset(x, y, t), batch_size=2)

    class ModularOnly:
        def __iter__(self):
            for b in mod_loader:
                yield (*b, 0)

    scores = compute_k_composition_scores(_model(), ModularOnly(), num_batches=2)  # type: ignore[arg-type]
    assert scores.get("_vacuous") is True
    assert not [k for k in scores if not k.startswith("_")]
