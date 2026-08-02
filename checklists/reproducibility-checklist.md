---
tags: [checklist, reproducibility]
---

# Reproducibility Checklist

Based on Pineau et al., "Improving Reproducibility in Machine Learning Research," JMLR 22(164), 2021.

## Model

- [x] Model architecture is fully specified (source code in `src/experiments/` and `07_capstone/src/`)
- [x] All hyperparameters are documented (in experiment argparse and configs)
- [~] Number of parameters reported per experiment — captured automatically by
  `ResultsManifest` (`src/results.py`) for the 3 experiments wired to
  `--seeds` (exp1, exp3, exp4) as of 2026-08-02; not yet exp2/exp5. See
  [[06_production_ai/notes/results-manifests-and-provenance]].
- [~] Training time reported per experiment — same manifest, `wall_clock_seconds`; same caveat.
- [~] Hardware specifications reported per experiment — same manifest, `device`; same caveat.

## Data

- [x] All datasets are synthetic (generated on-the-fly; seed-controlled)
- [x] Data generation pipeline is deterministic (seed-controlled)
- [x] Train/validation/test split is fixed and reproducible (seed-controlled)

## Experiments

- [x] All random seeds are controlled via `src.reproducibility.set_seed()`
- [~] Results reported as mean ± std over ≥3 seeds — the harness exists
  (`src.experiments.runner.run_seeds`) and 3 of 5 experiments (`exp1`, `exp3`,
  `exp4`, all via `--seeds`) have real manifests with genuine seed-to-seed
  spread as of 2026-08-02 (`results/*.json`). `exp2` has the flag but no run
  yet (needs the GPU run); `exp5` doesn't have it. Was wrongly checked `[x]`
  before 2026-08-01 with **zero** experiments actually doing this — see
  [[06_production_ai/notes/multi-seed-experiment-design]] for the
  correction. Re-check only once every rung reports this way.
- [x] Deterministic algorithms enabled where possible
- [~] Single-run results are explicitly flagged if reported — true going
  forward for anything using the manifest (`seeds: [N]` in the JSON makes
  this explicit and checkable); not yet retrofitted onto every number
  already sitting in [[portfolio/RESULTS]].

## Code

- [x] Source code is publicly available (MIT license)
- [x] Python environment is pinned (`uv.lock` / `pyproject.toml`)
- [x] `make reproduce` regenerates all figures and tables
- [x] All dependencies are listed with version constraints
- [x] Per-experiment `make reproduce-<name>` targets for individual experiments
- [x] CI smoke tests run on every push (tiny model, few steps)

## Paper

- [ ] Results include comparison to primary literature (Nanda et al., Olsson et al., Elhage et al.)
- [ ] At least one ablation study is included per experiment
- [ ] Limitations section is present in the mini-paper
- [ ] Primary literature is cited for all key claims
- [ ] Honest caveats about methods are documented (patching limitations, SAE illusions)
