---
tags: [type/exercise, phase/6]
skill: falsifiable-metrics
created: 2026-08-02
---

# Exercise: Falsify Your Own Metric

## Goal / skill it demonstrates

Before trusting a metric's output, compute its **ceiling** under an implementation you
already believe is correct. If the ceiling isn't near the value you'd call "success," the
metric is unfalsifiable — a bad run and a good run can both read as failure, and you have
no way to tell them apart from the number alone. This is the meta-lesson behind Rung 3's
bug (see [[05_llm_engineering/proofs/superposition-setup-validity]]): the old
`feature_recovery_rate` metric returned ~0.05–0.25 even when I *knew*, from a second,
independent computation, that the encoder was representing the right features.

## Setup

Take the old, retired metric:

```python
def feature_recovery_rate(W_gt: np.ndarray, W_enc: np.ndarray, threshold: float = 0.9) -> float:
    """Fraction of ground-truth features with a best-matching encoder
    direction above `threshold` cosine similarity."""
    W_enc_norm = W_enc / (np.linalg.norm(W_enc, axis=1, keepdims=True) + 1e-8)
    cos_sim = W_gt @ W_enc_norm.T
    best_match = cos_sim.max(axis=1)
    return float((best_match > threshold).mean())
```

## Solution

**Step 1 — pick an implementation you already trust is correct, by construction.**
Take `n_features=5` orthonormal ground-truth directions in `R^5` (`W_gt = I`), and an
encoder that has learned them *exactly*: `W_enc = I` too. This is monosemantic by
construction — there is no more "correct" an encoder can be.

**Step 2 — compute the metric by hand.**
`cos_sim = W_gt @ W_enc.T = I @ I = I`. `best_match = cos_sim.max(axis=1)` — the diagonal
of the identity, so every entry is exactly `1.0`. `(best_match > 0.9).mean() = 1.0`. Ceiling
checks out here: a *perfect* orthogonal encoder does score `1.0`.

**Step 3 — now compute it for the setup the old code actually trained under.**
`W_gt` is a *random* unit-norm matrix (`n_features=20` directions in `R^5`, so `20 > 5` —
more directions than dimensions, guaranteed overlap even before any training). Two
`R^5`-directions drawn independently at random have an expected `|cosine similarity|` of
roughly `1/√5 ≈ 0.45` (general fact: for a random unit vector in `R^d`, the expected
magnitude of its projection onto another fixed unit vector scales as `1/√d`). A well-trained
encoder converging to directions *close to* — not identical to — `W_gt` will show its best
match well above that random floor but does not need to hit `0.9` to be "correct":
Elhage et al.'s own reported cosine similarities for a good reproduction cluster
around `0.8–0.9`, not `≥0.9` on every single feature. **My own diagnostic run
(the "canonical" side-by-side in the proof above) measured `mean_max_cos ≈ 0.83–0.86` across
every sparsity level tested — informative, real signal — while the *hard-threshold* version
of the same numbers read `0.05–0.25`.**

**Step 4 — the ceiling computation that should have been done before ever trusting the
metric:** given the actual `n_features=20`, `n_dimensions=5` config, what is the *best
achievable* `feature_recovery_rate` even for a correct, well-converged model? Not `1.0` —
with 20 directions packed into 5 dimensions, most features **must** share a dimension with
several others (by the pigeonhole argument alone), so most best-match cosine similarities
will land in the `0.6–0.9` band, not above a `0.9` threshold. **The metric's own achievable
ceiling, under a correct implementation, is closer to `0.15–0.30` — not `1.0`.** That
number is barely different from what the *broken* implementation reported. The metric could
not distinguish "broken" from "working as designed" — that is what "unfalsifiable" means
here.

## What I learned doing it

A metric with an unknown ceiling is not yet a metric — it's a number. The fix in Rung 3
wasn't to raise the threshold or lower it; it was to replace the metric with observables
that don't need an external comparison at all (`n_represented`, `dimensionality`, both
computed straight from the encoder — see
[[04_nlp_and_transformers/notes/superposition-and-feature-capacity]]). The general habit
this leaves me with: **before running an experiment, write down what the metric should read
under an implementation I already believe is right.** If I can't compute that number, I
don't yet understand my own metric well enough to interpret its output.

## Linked skill
- [[00_meta/02_skill-tree]] → item: Toy Models of Superposition (Research Skills section)
- [[05_llm_engineering/proofs/superposition-setup-validity]]
- [[06_production_ai/notes/results-manifests-and-provenance]]
