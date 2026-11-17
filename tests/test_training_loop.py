"""The training loop learns, and gradient accumulation equals the large batch."""

from __future__ import annotations

import torch
from torch import nn

from src.training.loop import fit
from src.training.optim import AdamW


def _data(n: int = 64, seed: int = 0) -> tuple[torch.Tensor, torch.Tensor]:
    g = torch.Generator().manual_seed(seed)
    x = torch.randn(n, 5, generator=g)
    true_w = torch.tensor([1.0, -2.0, 0.5, 0.0, 3.0])
    return x, x @ true_w + 0.01 * torch.randn(n, generator=g)


def _model(seed: int = 1) -> nn.Linear:
    torch.manual_seed(seed)
    return nn.Linear(5, 1)


def _mse(pred: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    return nn.functional.mse_loss(pred.squeeze(-1), y)


def test_the_loop_reduces_the_loss() -> None:
    x, y = _data()
    model = _model()
    batches = [(x[i : i + 16], y[i : i + 16]) for i in range(0, 64, 16)] * 30
    losses = fit(model, batches, AdamW(model.parameters(), lr=0.05, weight_decay=0.0), _mse)
    assert losses[-1] < 0.01 * losses[0]


def test_accumulating_four_micro_batches_equals_one_large_batch() -> None:
    x, y = _data(32)
    big, small = _model(), _model()
    fit(big, [(x, y)], AdamW(big.parameters(), lr=0.1), _mse)
    micro = [(x[i : i + 8], y[i : i + 8]) for i in range(0, 32, 8)]
    fit(small, micro, AdamW(small.parameters(), lr=0.1), _mse, accum_steps=4)
    for a, b in zip(big.parameters(), small.parameters()):
        assert torch.allclose(a, b, atol=1e-6), (a - b).abs().max()


def test_forgetting_to_divide_by_accum_steps_changes_the_result() -> None:
    """The classic bug, reproduced: summing un-scaled micro-batch losses is a
    different (larger) gradient, so a plain-SGD step is four times too big."""
    x, y = _data(32)
    right, wrong = _model(), _model()
    fit(right, [(x[i : i + 8], y[i : i + 8]) for i in range(0, 32, 8)],
        torch.optim.SGD(right.parameters(), lr=0.01), _mse, accum_steps=4)
    opt = torch.optim.SGD(wrong.parameters(), lr=0.01)
    for i in range(0, 32, 8):
        _mse(wrong(x[i : i + 8]), y[i : i + 8]).backward()  # no / accum_steps
    opt.step()
    assert not torch.allclose(right.weight, wrong.weight, atol=1e-4)


def test_gradient_clipping_bounds_the_update_norm() -> None:
    x, y = _data(8)
    model = _model()
    before = [p.detach().clone() for p in model.parameters()]
    fit(model, [(x * 100, y * 100)], torch.optim.SGD(model.parameters(), lr=1.0), _mse,
        max_grad_norm=0.5)
    moved = torch.cat([(p.detach() - b).flatten() for p, b in zip(model.parameters(), before)])
    assert moved.norm() <= 0.5 + 1e-5
