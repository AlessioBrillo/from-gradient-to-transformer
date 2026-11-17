"""AdamW and a cosine schedule from scratch (Phase 3 exercise).

`torch.optim.AdamW` is the optimizer behind the grokking runs (weight decay
1.0 on the Nanda protocol). This is the same update written out in a dozen
lines so that every term can be seen, and `tests/test_optim.py` holds it equal
to PyTorch's to float precision.

The point of the exercise is the *decoupled* decay. Adam with an L2 penalty
adds `wd * w` to the gradient, which then passes through the adaptive
denominator and is rescaled per parameter. AdamW applies `lr * wd * w`
directly to the weight, outside that denominator, so the decay strength does
not depend on the gradient history.
"""

from __future__ import annotations

import math
from collections.abc import Iterable

import torch


class AdamW:
    """AdamW (Loshchilov & Hutter 2019), same defaults as `torch.optim.AdamW`."""

    def __init__(
        self,
        params: Iterable[torch.Tensor],
        lr: float = 1e-3,
        betas: tuple[float, float] = (0.9, 0.999),
        eps: float = 1e-8,
        weight_decay: float = 1e-2,
        decoupled: bool = True,
    ) -> None:
        self.params = [p for p in params if p.requires_grad]
        self.lr, self.betas, self.eps = lr, betas, eps
        self.weight_decay = weight_decay
        self.decoupled = decoupled
        self.t = 0
        self.m = [torch.zeros_like(p) for p in self.params]
        self.v = [torch.zeros_like(p) for p in self.params]

    def zero_grad(self) -> None:
        for p in self.params:
            p.grad = None

    @torch.no_grad()
    def step(self) -> None:
        self.t += 1
        b1, b2 = self.betas
        for p, m, v in zip(self.params, self.m, self.v):
            if p.grad is None:
                continue
            g = p.grad
            if self.decoupled:
                p.mul_(1.0 - self.lr * self.weight_decay)  # decay outside the denominator
            else:
                g = g + self.weight_decay * p  # L2: the decay is rescaled by 1/sqrt(v)
            m.mul_(b1).add_(g, alpha=1.0 - b1)
            v.mul_(b2).addcmul_(g, g, value=1.0 - b2)
            m_hat = m / (1.0 - b1**self.t)
            v_hat = v / (1.0 - b2**self.t)
            p.addcdiv_(m_hat, v_hat.sqrt().add_(self.eps), value=-self.lr)


def cosine_lr(step: int, total_steps: int, base_lr: float, warmup_steps: int = 0) -> float:
    """Linear warmup, then cosine decay to zero."""
    if warmup_steps and step < warmup_steps:
        return base_lr * (step + 1) / warmup_steps
    progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
    return 0.5 * base_lr * (1.0 + math.cos(math.pi * min(1.0, progress)))
