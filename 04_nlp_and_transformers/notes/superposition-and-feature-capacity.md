---
tags: [type/lesson, phase/4, state/review]
---

# Superposition and Feature Capacity

## What it is

A network with `d` dimensions can represent **more than `d` features** by packing them
into non-orthogonal directions, at the cost of some interference between them — and it does
this exactly when features are **sparse** (rarely co-active), because interference between
two features only matters on the rare occasions both are active at once.

## Why it exists / what problem it solves

Real-world features vastly outnumber the neurons or residual-stream dimensions available to
represent them. If a network could only use `d` orthogonal directions for `d` dimensions, it
would be capacity-starved almost everywhere. Superposition is the mechanism that resolves
this: trade a small, sparsity-conditional amount of interference for representing far more
features than dimensions.

This is *why sparse autoencoders exist* — see [[02_classical_ml/notes/pca-and-dictionary-learning]].
If the residual stream is in superposition, PCA cannot cleanly separate the underlying
features (they aren't orthogonal to begin with); an overcomplete, sparsity-penalized
dictionary can, because it isn't limited to `d` output directions the way PCA is.

## How it works

**Setup (Elhage et al., 2022):** `n` sparse ground-truth features, each literally a
standard basis vector of `R^n` (feature `i` "active" means coordinate `i` is nonzero), get
compressed through a linear bottleneck into `R^m` (`m < n`) and decompressed back with ReLU:

```
h  = W x            # compress:   R^n -> R^m
x' = ReLU(Wᵀh + b)   # decompress: R^m -> R^n
```

`W` has one column per feature (`W_i ∈ R^m`), and that column **is** the direction the
model chose to represent feature `i` with — there is no separate "ground truth direction"
to compare it against, because the input basis already *is* the ground truth.

**The two knobs that control the phase transition:**
1. **Sparsity** — how often each feature is active. At high sparsity (features active
   together often), packing two features into overlapping directions causes frequent,
   costly interference, so the model prefers to drop rarely-important features entirely
   (some columns of `W` collapse toward zero). At low sparsity, two features are almost
   never both active, so interference is nearly free, and the model finds room to give
   (nearly) every feature *some* direction, even a shared one.
2. **The decoder bias `b`.** Without it, any nonzero interference directly corrupts the
   reconstruction. With it, the model can shift the pre-ReLU baseline down so small
   cross-feature "leakage" gets clipped to zero instead of showing up in the output — this
   is literally what makes superposition *pay for itself* rather than just costing loss.

**Two observables, both computed from `W` alone, no external comparison needed:**
- `n_represented = |{i : ‖W_i‖ > τ}|` — how many features got any direction at all.
- `D_i = ‖W_i‖² / Σⱼ (Ŵᵢ · Wⱼ)²` — "dimensionality" per feature: 1.0 for a feature with a
  fully dedicated, orthogonal direction (monosemantic); less than 1 the more it shares its
  dimension with others (superposed).

## What I got wrong the first time

My first implementation pre-compressed the sparse features into `R^m` **before** the model
ever saw them (the dataset did the bottleneck's job), so the model was expanding an
already-solved problem rather than solving a real one — MSE reached exactly `0.000000` at
every sparsity level, and a metric comparing encoder rows to an invented `W_gt` read this as
uniform, near-total "failure" regardless. Full reconstruction of the bug (with numbers):
[[05_llm_engineering/proofs/superposition-setup-validity]].

## Links
- [[02_classical_ml/notes/pca-and-dictionary-learning]]
- [[05_llm_engineering/proofs/superposition-setup-validity]]
- [[06_production_ai/exercises/ex-01-falsify-your-own-metric]]
- Code: `src/experiments/exp3_superposition.py`

## Open questions
- #question Does the Gram matrix (`WᵀW`) actually show the antipodal-pair / pentagon
  geometry Elhage et al. report at small `n`, `m`? Not yet independently checked against a
  known low-dimensional case.
- #question How does `importance_decay` (currently defaulted to `1.0`, uniform) change
  *which* features get dropped first, not just how many?
