---
tags: [type/lesson, phase/6, state/review]
---

# Multi-Seed Experiment Design

## What it is

Running the same experiment several times with different random seeds and reporting a
spread (mean ± std, or min/max), instead of a single number from a single run.

## Why it exists / what problem it solves

A single-seed result cannot distinguish "this is what the method reliably does" from "this
is what happened to come out of one particular random initialization and data shuffle."
Henderson et al. (*Deep RL That Matters*, 2018) is the canonical demonstration: published
single-seed comparisons between methods routinely **flip** once re-run across several seeds
— the "better" method was sometimes just the luckier seed.

This repository had exactly the gap Henderson et al. warn about, for a while in a way that
was worse than silent: `checklists/reproducibility-checklist.md` had
`[x] Results reported as mean ± std over ≥3 seeds` **checked**, while no experiment in
`src/` ran more than one seed. A checked box that isn't true is the specific failure mode
[[00_meta/02_skill-tree]]'s own top rule warns against ("a checked box without proof is a
lie you tell yourself") — this was that rule's exact target, just in a checklist instead of
the skill tree.

## How it works

The harness ([[06_production_ai/notes/results-manifests-and-provenance]]) separates two
concerns that were previously tangled together in each experiment's `main()`:

1. **What to measure** — a `run_single_seed(seed, args) -> dict[str, float]` function per
   experiment, doing exactly the single-seed work the experiment already did, just
   returning a flat metrics dict instead of directly printing/plotting.
2. **How to aggregate** — `src.experiments.runner.run_seeds(fn, seeds)`, which is
   experiment-agnostic: it calls `fn` once per seed, requires every seed to report the
   *same* metric keys (a seed that silently drops a metric fails loudly instead of
   producing a quietly-smaller aggregate), and returns per-metric
   `{mean, std, min, max, n}`.

```python
from src.experiments.runner import run_seeds

def run_single_seed(seed: int, args) -> dict[str, float]:
    # ... train exactly as the single-seed path already does ...
    return {"val_accuracy": acc, "n_represented": n}

result = run_seeds(lambda s: run_single_seed(s, args), seeds=[0, 1, 2])
print(result.summary_line("val_accuracy"))  # "0.9123 ± 0.0087 (n=3, range [0.90, 0.92])"
```

Seeding itself is unchanged — `run_single_seed` still calls
`src.reproducibility.set_seed(seed)` exactly as the single-seed path did. The runner adds
the loop and the statistics; it does not add a second seeding mechanism.

## What still has only one seed

As of this note, only `src/experiments/exp3_superposition.py` has a `--seeds` flag wired to
this harness. Rungs 1, 4, and 5 get it as part of the standard-scale re-run work
([[06_production_ai/notes/results-manifests-and-provenance]] tracks which manifests exist);
Rung 2 (grokking) gets it as part of the Colab flagship run, since 3 seeds × 5000 epochs at
P=113 needs a GPU regardless of the harness. Until a rung has a manifest in `results/`, its
numbers in [[portfolio/RESULTS]] are still single-seed and should read that way.

## Links
- [[06_production_ai/notes/results-manifests-and-provenance]]
- [[06_production_ai/exercises/ex-02-results-manifest]]
- [[checklists/reproducibility-checklist]]
- Code: `src/experiments/runner.py`
- Henderson et al., *Deep Reinforcement Learning That Matters*, AAAI 2018
- Pineau et al., *Improving Reproducibility in Machine Learning Research*, JMLR 2021

## Open questions
- #question For a phenomenon as seed-sensitive as grokking (Nanda et al. report seed
  sensitivity in generalization epoch), is 3 seeds enough to report a defensible spread, or
  does the flagship number need more?
