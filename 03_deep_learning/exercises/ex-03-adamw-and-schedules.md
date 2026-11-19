---
tags: [type/exercise, phase/3, state/review]
authorship: claude
created: 2026-11-17
---

# Exercise 03 — AdamW and a cosine schedule from scratch

> **Authorship.** Written by Claude (an AI assistant) on 2026-11-17 to close a gap
> the vault's own rule exposed: the optimization skills were checked on a note
> alone. The code is verified by tests, but this is not the repository owner's
> own solution. See [[00_meta/02_skill-tree]].

## Goal / skill it demonstrates

Write the optimizer behind the grokking runs, so that the one term that makes
grokking happen (decoupled weight decay) can be seen rather than named.

- Optimization: Adam/AdamW and learning-rate schedules.
- Regularization: weight decay, and why it is *not* the same as an L2 penalty.

## Task

1. Implement AdamW without `torch.optim`: first and second moments, bias
   correction, and a decay term applied to the weight directly.
2. Add a switch that moves the decay into the gradient instead (L2).
3. Implement linear warmup followed by cosine decay.
4. Show that (1) equals `torch.optim.AdamW` and that (2) does not.

## Solution

Code: `src/training/optim.py`. Tests: `tests/test_optim.py`.

```python
if self.decoupled:
    p.mul_(1.0 - self.lr * self.weight_decay)   # decay outside the denominator
else:
    g = g + self.weight_decay * p               # L2: rescaled by 1/sqrt(v)
m.mul_(b1).add_(g, alpha=1 - b1)
v.mul_(b2).addcmul_(g, g, value=1 - b2)
p.addcdiv_(m / (1 - b1**t), (v / (1 - b2**t)).sqrt() + eps, value=-lr)
```

Measured on a 6→3 linear regression, 25 steps, `lr=3e-3`, `weight_decay=0.5`:

| Comparison | Largest parameter difference |
|---|---|
| this AdamW vs `torch.optim.AdamW` | 3.0e-08 |
| decoupled decay vs the L2 variant | 6.4e-02 |

The first row is float rounding; the second is a different algorithm. With a zero
gradient the decay is exactly `lr * weight_decay` per step
(`test_with_zero_gradient_the_decay_is_exactly_lr_times_wd`), which is the
property the proof below uses.

## What this shows

- In the L2 variant the decay term is divided by `sqrt(v_hat)`, so a parameter
  with a large gradient history is decayed *less* and one with a small history is
  decayed *more*. The strength of the regularizer depends on the gradients.
- In AdamW every parameter shrinks by the same factor `1 - lr * wd` per step. That
  uniform pressure is what lets a weight the task does not need go to zero.

## Errata to a neighbouring note

[[03_deep_learning/notes/training-dynamics-and-grokking]] says AdamW applies the
decay "after the adaptive gradient step". What defines it is not the order but
that the decay never passes through the adaptive denominator; `torch.optim.AdamW`
applies it before the moment update, as the code above does.

## Linked skill

- [[00_meta/02_skill-tree]] → Optimization (Adam/AdamW, LR schedulers); Regularization
- Proof: [[03_deep_learning/proofs/weight-decay-and-the-cleanup-phase]]
