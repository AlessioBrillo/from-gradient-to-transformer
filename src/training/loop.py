"""A training loop with gradient accumulation (Phase 3 exercise).

Gradient accumulation trades memory for steps: run `accum_steps` micro-batches,
sum their gradients, step once. For a loss that is a *mean* over the batch it is
exactly equivalent to one batch `accum_steps` times larger, provided each
micro-batch loss is divided by `accum_steps`. Forgetting that division is the
classic bug: the effective learning rate silently grows by `accum_steps`.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable

import torch
from torch import nn


def fit(
    model: nn.Module,
    batches: Iterable[tuple[torch.Tensor, torch.Tensor]],
    optimizer: object,
    loss_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
    accum_steps: int = 1,
    max_grad_norm: float | None = None,
) -> list[float]:
    """Train over `batches`; return the (mean) loss of every optimizer step.

    `optimizer` needs `zero_grad()` and `step()`; both `torch.optim.*` and
    `src.training.optim.AdamW` qualify.
    """
    model.train()
    losses: list[float] = []
    running = 0.0
    optimizer.zero_grad()  # type: ignore[attr-defined]
    for i, (x, y) in enumerate(batches, start=1):
        loss = loss_fn(model(x), y) / accum_steps
        loss.backward()
        running += loss.item()
        if i % accum_steps == 0:
            if max_grad_norm is not None:
                nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()  # type: ignore[attr-defined]
            optimizer.zero_grad()  # type: ignore[attr-defined]
            losses.append(running)
            running = 0.0
    return losses
