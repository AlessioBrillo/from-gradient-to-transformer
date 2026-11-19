---
tags: [type/exercise, phase/3, state/review]
authorship: claude
created: 2026-11-17
---

# Exercise 04 — A training loop, and gradient accumulation done right

> **Authorship.** Written by Claude on 2026-11-17 to close a gap the vault's own rule
> exposed (see [[00_meta/02_skill-tree]]). The code is tested; it is not the repository
> owner's own solution.

## Goal / skill it demonstrates

Write the loop every experiment in this repository runs, and show that gradient
accumulation is exactly a larger batch, not an approximation of one.

## Task

1. Write `fit(model, batches, optimizer, loss_fn, accum_steps, max_grad_norm)`:
   forward, loss, backward, optional clipping, step, `zero_grad`.
2. Make `accum_steps=k` over micro-batches of size `n/k` equal one step on a batch of
   size `n`.
3. Reproduce the classic bug and measure it.

## Solution

Code: `src/training/loop.py`. Tests: `tests/test_training_loop.py`.

The one line that matters:

```python
loss = loss_fn(model(x), y) / accum_steps   # the mean over the *whole* batch
```

Measured on a 5-feature linear regression, 32 samples:

| Comparison | Result |
|---|---|
| 1 step on a batch of 32 vs 4 accumulated micro-batches of 8 (AdamW) | largest parameter difference **0.0** |
| plain SGD, the loss divided by `accum_steps` vs not divided | the step is **4.00×** too long without the division |
| a loop over 120 mini-batches (AdamW, no decay) | the final loss is under 1% of the first |

Clipping is tested as a bound: with `max_grad_norm=0.5` and SGD at `lr=1`, the
parameter movement has norm at most 0.5 even when the gradients are two orders of
magnitude larger.

## What this shows

- The equivalence is exact because the gradient of a mean is the mean of the micro-batch
  gradients when the micro-batches have equal size. See
  [[03_deep_learning/proofs/gradient-accumulation-is-the-large-batch]] for when that
  stops being true.
- The wrong version still trains, just with a learning rate that is `accum_steps` times
  larger than intended. Nothing crashes; the symptom is a loss curve that looks "a bit
  unstable", which is why it is worth a test.

## Not covered

Mixed precision. The skill "gradient accumulation, mixed precision" is therefore only
half evidenced; the checklist now names accumulation alone.

## Linked skill

- [[00_meta/02_skill-tree]] → PyTorch training loop; training tricks (accumulation)
