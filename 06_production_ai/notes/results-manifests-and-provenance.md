---
tags: [type/lesson, phase/6, state/review]
---

# Results Manifests and Provenance

## What it is

A machine-readable record (`results/<experiment>.json`) of exactly what produced a
number: the git commit, whether the working tree was clean, the full config, every seed's
raw metrics, the aggregate statistics, wall-clock time, hardware/library versions, and
parameter count.

## Why it exists / what problem it solves

This vault's own progress log records **two** separate incidents of documentation running
ahead of evidence: 2026-07-26 found `figures/` didn't exist despite being cited as
delivered; 2026-08-01 retracted three Rung 4 numbers that had been computed under a broken
patch site and metric. Both times, the fix was a person reading the code carefully and
re-running it by hand. A manifest doesn't replace that judgment, but it gives something for
a *mechanical* check to compare against, so the third time doesn't also require a full
manual audit to catch.

It also directly closes three lines in [[checklists/reproducibility-checklist]] that were
unchecked for lack of anywhere to record them: "Number of parameters reported per
experiment," "Training time reported per experiment," "Hardware specifications reported per
experiment" — each is one field on the manifest.

## How it works

`src/results.py`'s `ResultsManifest` is built from a `SeedAggregate`
([[06_production_ai/notes/multi-seed-experiment-design]]) via `ResultsManifest.from_run(...)`,
which stamps in the environment automatically (git SHA + dirty flag, torch/numpy/python
versions, device) so the caller only supplies what it actually measured:

```python
manifest = ResultsManifest.from_run(
    experiment="exp3_superposition",
    seeds=[0, 1, 2],
    args=vars(args),
    per_seed_metrics=result.per_seed,
    aggregate=result.aggregate,
    wall_clock_seconds=result.wall_clock_seconds,
    device=str(DEVICE),
    n_parameters=count_parameters(model),
)
manifest.save(Path("results/exp3_superposition.json"))
```

The convention that makes a manifest *load-bearing* rather than decorative: every headline
number in [[portfolio/RESULTS]] should sit next to an HTML comment tag,
`<!-- manifest: results/exp3_superposition.json -->`, pointing at the file that backs it.
`make verify-claims` (`src.results.verify_claims`) checks two things mechanically:

1. Every manifest in `results/` is internally consistent — its seed count matches its own
   `per_seed_metrics` length and every aggregate's recorded `n`, and it wasn't saved with a
   dirty working tree (a dirty-tree result can't be tied to any specific commit, so it can't
   back a claim about "the code as of commit X").
2. Every `<!-- manifest: ... -->` tag in `RESULTS.md` points at a manifest that actually
   exists on disk.

This deliberately does **not** parse the numbers out of RESULTS.md's prose and compare them
against the manifest's numbers — that would require a much more rigid claims format than a
hand-written research log should have. What it catches is the cheaper, more common failure:
a claim with *no* manifest at all, or a manifest tag that rotted after a file got renamed or
deleted. I confirmed it catches this on the very first run: `make verify-claims` against
today's `RESULTS.md` (no tags anywhere yet) reports exactly that — two problems, "no
manifests found" and "no manifest tags found" — before any reconciliation pass touched it.

## Links
- [[06_production_ai/notes/multi-seed-experiment-design]]
- [[06_production_ai/exercises/ex-02-results-manifest]]
- [[checklists/reproducibility-checklist]]
- [[portfolio/RESULTS]]
- Code: `src/results.py`
- Pineau et al., *Improving Reproducibility in Machine Learning Research*, JMLR 2021

## Open questions
- #question Should `verify-claims` be a CI gate (blocking `dev → main`) once every rung has
  a manifest, or does that create pressure to keep stale manifests around past when a rerun
  is actually warranted?
