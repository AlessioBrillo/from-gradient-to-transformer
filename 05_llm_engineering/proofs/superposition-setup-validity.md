---
tags: [type/proof, phase/5, research/experiment]
created: 2026-08-02
---

# Proof to myself: A Toy Model Only Reproduces What It Structurally Permits

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate

That I understand, well enough to catch my own mistake, why my Rung 3 (Toy Models of
Superposition) implementation showed flat, near-zero "feature recovery" at *every* sparsity
level across two separate audits (2026-07-26, 2026-08-01), and why the fix I tried in
between — tying the decoder weights to the encoder's transpose — could not have changed
that, which is exactly what its own before/after numbers showed (0.100 → 0.100 at
sparsity=0.01).

The open question left on the table 2026-08-01 was: *if it's not the tied-weights thing,
what is it?* This is that reconstruction.

## What I produced from memory

### 1. Read the shapes before running anything

Elhage et al.'s toy model is a **compression**: `n_features` sparse ground-truth features,
each literally a standard basis vector of `R^n_features`, get squeezed through a bottleneck
of `n_dimensions < n_features`, then decompressed back out with `ReLU`:

```
h  = W x            # R^n_features -> R^n_dimensions   (n_dimensions < n_features)
x' = ReLU(Wᵀh + b)   # R^n_dimensions -> R^n_features
```

My `exp3_superposition.py` did something else. `SparseFeatureDataset` generated the sparse
features, then **immediately embedded them into `n_dimensions` space itself**, using its own
random matrix `W_gt`:

```python
# old code
W = rng.standard_normal((n_features, n_dimensions))   # the dataset's own compression
embedded = features @ W                                 # ALREADY compressed to R^n_dimensions
```

`ToyAutoencoder` then autoencoded that *already-compressed* `n_dimensions`-vector through a
**wider** `n_features`-dimensional ReLU latent — an expansion, not a compression. The
dataset had done the one thing the model was supposed to be forced to do, before the model
ever saw a single sample. There was no bottleneck left for superposition to be a solution
*to*.

### 2. Confirm the shape argument empirically, not just on paper

I ran the current (buggy) architecture and the canonical one side by side, same seed, same
feature statistics:

```
A (buggy: dataset pre-compresses, model expands)
  sparsity=0.10 : final MSE=0.000020   recovery=0.050
  sparsity=0.01 : final MSE=0.000000   recovery=0.000

B (canonical: model itself compresses n_features -> n_dimensions)
  sparsity=0.50 : MSE=0.435   recovery=0.150   features represented (‖W_i‖>0.5) = 11/20
  sparsity=0.10 : MSE=0.089   recovery=0.250   features represented            = 19/20
  sparsity=0.01 : MSE=0.003   recovery=0.050   features represented            = 20/20
  sparsity=0.001: MSE=0.000   recovery=0.150   features represented            = 18/20
```

The tell is `MSE=0.000000` at `sparsity=0.01` in run A: a genuinely lossy compression cannot
reach exact zero on features it must actively choose to drop. Run A reaches it because
there is no compression happening in the model at all — the encoder is free to learn an
exact linear inverse of `W_gt`, and does. This is a **structural** signature, not something
more training or a different metric threshold would fix; it is why the 2026-08-01
tied-weights change (a real correctness fix, matching Elhage's parameter sharing) left the
number completely unchanged. Tying weights fixes how the *existing* bottleneck is
parameterized; it does nothing if there is no bottleneck to begin with.

Run B, with the actual bottleneck restored, shows the phase transition immediately: **11/20
features represented at dense (sparsity=0.5) rising to 20/20 at sparse (sparsity=0.01)** —
exactly Elhage et al.'s claim, on the very first side-by-side run.

### 3. The metric was a second, independent bug

Even in run B, the old `feature_recovery_rate` (`cos_sim > 0.9` against an invented
`W_gt`) reads 0.05–0.25 while the encoder is doing something real. Two things are wrong
with it:
- **There is no `W_gt` in the actual paper.** Features are literally the input basis; the
  model's own encoder weight columns *are* the learned feature directions. Comparing them
  against a second, independently-random matrix compares the model to a target it was never
  shown and has no reason to match.
- **A hard `cos > 0.9` threshold is the wrong shape of question.** Even a well-behaved run
  puts `mean_max_cos` around 0.83–0.86 — informative, but a threshold at 0.9 reads that as
  near-total failure. The paper's own signal is simpler and doesn't need an external
  target at all: **does each feature get a nonzero direction (`‖W_i‖ > τ`) at all**, and
  **how many dimensions does it effectively get to itself**
  (`D_i = ‖W_i‖² / Σⱼ(Ŵᵢ·Wⱼ)²`)? Both are computable from the encoder alone.

### 4. The fix, and why it is falsifiable

`src/experiments/exp3_superposition.py`, rewritten 2026-08-02:
- `SparseFeatureDataset` now emits the sparse feature vector directly in `R^n_features` — no
  `W_gt`, no pre-embedding.
- `ToyAutoencoder` enforces `n_dimensions < n_features` at construction (raises
  `ValueError` otherwise) and adds the decoder bias `b`, which is what lets the model push
  small cross-feature interference below the `ReLU` floor instead of always paying for it —
  the second missing ingredient, separate from the bottleneck itself.
- `compute_feature_geometry` replaces the ground-truth comparison with `n_represented` and
  per-feature `dimensionality`, both computed from the encoder alone.

Falsified with `tests/test_exp3_superposition.py::TestFeatureGeometryFalsification`:
- `test_model_is_a_bottleneck` — on fully dense data, loss cannot collapse to the old
  code's `0.000000`; asserts a nonzero floor.
- `test_dense_regime_drops_features` / `test_sparse_regime_represents_all_features` — the
  two ends of the phase transition run B demonstrated above, now as an automated check
  rather than a one-off script.
- `test_dimensionality_is_one_when_monosemantic` — a hand-constructed orthogonal encoder
  scores `D_i ≈ 1.0`, the metric's sanity floor.

None of these four would have passed against the pre-rewrite code: it had no
`n_dimensions < n_features` guard, no `decoder_bias` parameter, and its
`compute_feature_recovery` function does not even exist post-rewrite.

## Limitations — what this note does *not* prove

- The side-by-side numbers above are from a **diagnostic script**, not the committed
  experiment's own `--quick`/full sweep with its actual argparse defaults and plotting
  path. The committed sweep (`make reproduce-superposition`) needs its own run before
  `portfolio/RESULTS.md` can cite numbers from it — see [[portfolio/RESULTS]].
- Single seed. No claim here about variance across seeds — that is
  [[06_production_ai/notes/multi-seed-experiment-design]]'s job, not this proof's.
- I have not reproduced Elhage et al.'s geometric claims beyond the represented-feature
  count — the antipodal-pair and polytope structure in the Gram matrix is plotted
  (`exp3_feature_geometry.png`) but not yet independently checked against a known
  low-dimensional case (e.g. 5 features into 2 dimensions should show a clean pentagon).
- `importance_decay` defaults to `1.0` (uniform importance) in the committed sweep; Elhage
  et al.'s more elaborate claims about *which* features get dropped when they differ in
  importance are not exercised by the default config.

## Links
- [[04_nlp_and_transformers/notes/superposition-and-feature-capacity]]
- [[06_production_ai/exercises/ex-01-falsify-your-own-metric]]
- [[05_llm_engineering/proofs/intervention-validity]] — same house style, same lesson
  (instrument validity before results), different failure mode: this one is a modeling
  bug, that one was three measurement-site bugs.
- [[portfolio/RESULTS]]
- Code: `src/experiments/exp3_superposition.py`, `tests/test_exp3_superposition.py`
- Elhage et al., *Toy Models of Superposition*, Anthropic (2022)

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
