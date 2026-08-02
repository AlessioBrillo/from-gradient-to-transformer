---
tags: [type/exercise, phase/6]
skill: results-manifests
created: 2026-08-02
---

# Exercise: Build and Verify a Results Manifest

## Goal / skill it demonstrates

Wire an experiment's headline metric to the multi-seed harness end to end: run several
seeds, save a manifest, tag it in a claims document, and get `make verify-claims` to
actually pass — not just write the harness code and assume it works.

## Solution

**1. Ran Rung 3 (superposition) across 3 seeds at a small, fast config:**

```bash
python -m src.experiments.exp3_superposition \
  --n-features 8 --n-dimensions 3 --epochs 100 --num-samples 1000 --seeds 0,1,2
```

Console output:
```
=== seed 0 ===
=== seed 1 ===
=== seed 2 ===
Saved multi-seed manifest to results/exp3_superposition.json
  n_represented: 8.0000 ± 0.0000 (n=3, range [8.0000, 8.0000])
  mean_abs_correlation: 0.3790 ± 0.0027 (n=3, range [0.3763, 0.3828])
  mean_dimensionality: 0.3688 ± 0.0014 (n=3, range [0.3674, 0.3707])
```

**2. Read the manifest — every field the checklist wanted is there without extra work:**

```json
{
  "experiment": "exp3_superposition",
  "seeds": [0, 1, 2],
  "git_sha": "<short sha>",
  "git_dirty": true,
  "device": "cpu",
  "torch_version": "2.12.1+cu130",
  "aggregate": {
    "n_represented": {"mean": 8.0, "std": 0.0, "min": 8.0, "max": 8.0, "n": 3.0}
  }
}
```

Two things worth noticing, not just reading past:
- `git_dirty: true` — this run happened mid-edit, with uncommitted changes. That is
  *correctly* flagged, not silently accepted: a dirty-tree manifest can't back a claim
  about a specific committed version of the code, and `verify_claims` catches exactly this
  (see step 4).
- `n_represented` has **zero** spread at this tiny config (8 features, 3 dimensions,
  sparsity 0.01 — every feature gets represented, every seed, no exceptions). A real test of
  the harness needs a config where the outcome is *not* deterministic-looking, or the
  spread numbers never get exercised. (Left for a follow-up run at a config nearer the
  phase transition, where I'd actually expect a seed to occasionally disagree.)

**3. Tagged it in a scratch claims file and ran the verifier — first pass, on purpose,
without a tag:**

```bash
$ make verify-claims
verify-claims: 2 problem(s) found:
  - No manifests found in results/ — no headline claim is currently traceable to a run.
  - portfolio/RESULTS.md: no <!-- manifest: ... --> tags found — none of its numbers are traceable to a manifest.
```

This is the state of the actual repo as of this exercise — confirms the checker isn't a
no-op that passes trivially.

**4. Then with the manifest present but a dirty tree, `git_dirty` correctly surfaces:**

```bash
$ python -m src.results verify
verify-claims: 1 problem(s) found:
  - results/exp3_superposition.json: recorded with a dirty working tree — results may not correspond to any committed commit.
```

## What I learned doing it

The manifest fields I expected to be tedious (git SHA, library versions, device) were free —
`ResultsManifest.from_run` fills them in. The one that actually required a decision was
`git_dirty`: my first instinct was to treat it as a warning I could silence for
convenience during iteration, but the whole point of the check is that a claim can't be
tied to a specific commit if the tree wasn't clean when the number was produced. The
uncomfortable state (dirty tree, correctly flagged) is more useful than a comfortable one
that lies.

## Linked skill
- [[00_meta/02_skill-tree]] → item: Reproducibility harness (Phase 6)
- [[06_production_ai/notes/results-manifests-and-provenance]]
- [[06_production_ai/notes/multi-seed-experiment-design]]
