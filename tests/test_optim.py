"""The from-scratch AdamW matches torch.optim.AdamW, and the decay is decoupled."""

from __future__ import annotations

import math

import torch

from src.training.optim import AdamW, cosine_lr


def _problem(seed: int = 0) -> tuple[torch.nn.Linear, torch.Tensor, torch.Tensor]:
    torch.manual_seed(seed)
    return torch.nn.Linear(6, 3), torch.randn(32, 6), torch.randn(32, 3)


def _run(opt_factory, steps: int = 25) -> list[torch.Tensor]:
    model, x, y = _problem()
    opt = opt_factory(model.parameters())
    for _ in range(steps):
        opt.zero_grad()
        torch.nn.functional.mse_loss(model(x), y).backward()
        opt.step()
    return [p.detach().clone() for p in model.parameters()]


def test_matches_torch_adamw() -> None:
    mine = _run(lambda ps: AdamW(ps, lr=3e-3, weight_decay=0.5))
    ref = _run(lambda ps: torch.optim.AdamW(ps, lr=3e-3, weight_decay=0.5))
    for a, b in zip(mine, ref):
        assert torch.allclose(a, b, atol=1e-6), (a - b).abs().max()


def test_l2_variant_differs_from_decoupled_decay() -> None:
    decoupled = _run(lambda ps: AdamW(ps, lr=3e-3, weight_decay=0.5, decoupled=True))
    l2 = _run(lambda ps: AdamW(ps, lr=3e-3, weight_decay=0.5, decoupled=False))
    assert any(not torch.allclose(a, b, atol=1e-4) for a, b in zip(decoupled, l2))


def test_with_zero_gradient_the_decay_is_exactly_lr_times_wd() -> None:
    w = torch.nn.Parameter(torch.ones(4))
    opt = AdamW([w], lr=0.1, weight_decay=0.5)
    w.grad = torch.zeros(4)
    opt.step()
    assert torch.allclose(w.detach(), torch.full((4,), 1.0 - 0.1 * 0.5))


def test_cosine_schedule_shape() -> None:
    assert cosine_lr(0, 100, 1.0, warmup_steps=10) == 0.1  # first warmup step
    assert math.isclose(cosine_lr(10, 100, 1.0, warmup_steps=10), 1.0)  # peak
    assert math.isclose(cosine_lr(100, 100, 1.0, warmup_steps=10), 0.0, abs_tol=1e-12)
    assert cosine_lr(55, 100, 1.0, warmup_steps=10) < cosine_lr(30, 100, 1.0, warmup_steps=10)
