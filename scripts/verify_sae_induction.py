"""Smoke check: a locally saved SAE produces non-trivial feature activations on
real activations from the exp1 checkpoint.

This is NOT an induction-circuit test: inputs are not filtered to induction
positions and there is no baseline, so any non-degenerate SAE passes. Requires
a local `sae_model.pt` (state_dict), which exp5_sae_dashboard.py does not write.
"""
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.experiments.exp5_sae_dashboard import (  # noqa: E402
    SparseAutoencoder,
    harvest_activations_from_checkpoint,
)

CHECKPOINT = Path("figures/exp1_trained_model.pt")
SAE_PATH = Path("sae_model.pt")


def verify() -> None:
    for p in (CHECKPOINT, SAE_PATH):
        if not p.exists():
            sys.exit(f"missing {p}; see module docstring")
    # Architecture constants must match the exp1 run that produced CHECKPOINT.
    activations = harvest_activations_from_checkpoint(
        CHECKPOINT, num_samples=100, vocab_size=256, seq_len=24,
        d_model=32, n_layers=2, n_heads=4, seed=42,
    )
    sae = SparseAutoencoder(d_model=32, n_features=512)
    sae.load_state_dict(torch.load(SAE_PATH, weights_only=True))
    sae.eval()
    with torch.no_grad():
        features = sae.get_feature_activations(activations)
    l0 = (features > 0).float().sum(-1).mean().item()
    print(f"max activation: {features.max():.3f}, L0: {l0:.1f}/512")
    assert features.max() > 0.5, f"no feature activation, max {features.max()}"
    print("SAE smoke check passed.")


if __name__ == "__main__":
    verify()
