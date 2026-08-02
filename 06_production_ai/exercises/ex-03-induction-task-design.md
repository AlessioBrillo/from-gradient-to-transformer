---
tags: [type/exercise, phase/6]
skill: task-design-validity
created: 2026-08-02
---

# Exercise: Is the Induction Task Even Well-Posed?

## Goal / skill it demonstrates

Before blaming "scale" or "training budget" for a negative result, check whether the task
itself has a well-defined answer. Predicting a collision probability by hand, then checking
it against the code, catches this class of bug before spending compute chasing a ghost.

## Setup

The induction task (Olsson et al., 2022) needs a prefix `[A_0, ..., A_{k-1}]` with **no
repeated tokens** — otherwise "attend to the position after the previous occurrence of the
current token" has more than one valid answer. `make_repeated_token_data` draws each prefix
token uniformly at random from a `vocab_size`-token vocabulary. This is exactly the birthday
problem: `k` draws from `n` items, probability of at least one repeat.

## Solution

**Step 1 — derive the formula from first principles.** `P(no collision)` is the probability
that draw 2 differs from draw 1 (`(n-1)/n`), draw 3 differs from both prior draws
(`(n-2)/n`), and so on:

```
P(no collision) = (n-1)/n · (n-2)/n · ... · (n-k+1)/n = ∏_{i=1}^{k-1} (1 - i/n)
```

Using `1 - x ≈ e^{-x}` for small `x` and summing the exponents
(`Σ_{i=1}^{k-1} i = k(k-1)/2`):

```
P(no collision) ≈ exp(-k(k-1) / (2n))
P(collision)    ≈ 1 - exp(-k(k-1) / (2n))
```

**Step 2 — predict, by hand, the classic textbook case** (23 people, 365 days) before
running any code: `k=23, n=365` → `k(k-1)/(2n) = 506/730 ≈ 0.693` →
`P ≈ 1 - e^{-0.693} ≈ 1 - 0.500 = 0.500`. (The well-known answer is 50.7%; the
approximation is close.)

**Step 3 — predict the repo's actual pre-fix defaults, *before* looking at any run
output.** Standard scale: `seq_len=64`, `prefix_ratio=0.5` → `prefix_len=32`,
`vocab_size=32` (the old default): `k(k-1)/(2n) = 32·31/64 = 15.5` →
`P ≈ 1 - e^{-15.5} ≈ 1 - 1.9×10⁻⁷ ≈ 100.0%`. `--quick`: `prefix_len=12`, `vocab_size=16`:
`k(k-1)/(2n) = 12·11/32 = 4.125` → `P ≈ 1 - e^{-4.125} ≈ 98.4%`.

**Step 4 — check the prediction against the actual code:**

```python
>>> from src.experiments.exp1_induction_heads import prefix_duplicate_probability
>>> prefix_duplicate_probability(vocab_size=32, prefix_len=32)   # old standard default
0.9999998106...
>>> prefix_duplicate_probability(vocab_size=16, prefix_len=12)   # old --quick default
0.9835844...
```

Matches the hand prediction to 3+ decimal places — both configurations had a prefix that
was *almost never* unambiguous.

**Step 5 — solve for a vocabulary size that brings this under a 30% working threshold**,
for the actual prefix lengths in use. Setting `k(k-1)/(2n) ≈ -ln(1 - 0.3) ≈ 0.357` and
solving for `n`:

```
Standard (k=32): n ≥ 32·31/(2·0.357) ≈ 1391  -> round to 2048 -> P = 21.5%
Quick    (k=12): n ≥ 12·11/(2·0.357) ≈ 185   -> round to 256  -> P = 22.7%
```

These are the current `--vocab-size` defaults (`src/experiments/exp1_induction_heads.py`).

**Step 6 — run it and see if fixing the task design alone produces induction heads.**

```
$ python -m src.experiments.exp1_induction_heads --quick
... (no "Prefix ambiguity" warning — confirms vocab_size=256 is under threshold)
Peak diag+1 mass at epoch 99 (value: 0.125) | Final diag+1 mass: 0.123
Total induction heads: 0 / 8
```

**Result: still zero heads at quick scale (500 epochs).** The ambiguity fix removed a real
defect, but it did not, by itself, produce the phenomenon — `diag1_mass` (0.125) is well
under the 0.3 detection threshold, consistent with the 2026-08-01 audit's separate finding
that heads genuinely have not formed within this epoch budget. Two different problems,
correctly not conflated: a task-design bug (fixed, confirmed by re-deriving the collision
probability under the new config) and a training-budget/scale question (still open,
addressed separately by the standard-scale multi-seed run in
[[portfolio/RESULTS]]).

## What I learned doing it

The instinct to reach for "needs more scale" is dangerous because it's *always* a plausible
explanation for a negative result — it can never be ruled out by inspection, only by
spending more compute. A task-design bug like this one is falsifiable in five minutes with
arithmetic, before touching a GPU. The general habit: when a training run shows a
suspiciously stubborn negative result, check whether the *task itself* has a well-defined
answer before assuming the *model* just needs more of something.

## Linked skill
- [[00_meta/02_skill-tree]] → item: Induction head reproduction (Research Skills section)
- [[04_nlp_and_transformers/notes/induction-heads]]
- [[06_production_ai/notes/multi-seed-experiment-design]]
