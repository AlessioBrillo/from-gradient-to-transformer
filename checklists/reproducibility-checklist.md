---
tags: [checklist, reproducibility]
---

# Reproducibility Checklist

Based on Pineau et al., "Improving Reproducibility in Machine Learning Research," JMLR 22(164), 2021.

## Model

- [x] Model architecture is fully specified (source code in `src/experiments/` and `07_capstone/src/`)
- [x] All hyperparameters are documented (in experiment argparse and configs)
- [ ] Number of parameters reported per experiment
- [ ] Training time reported per experiment
- [ ] Hardware specifications reported per experiment

## Data

- [x] All datasets are synthetic (generated on-the-fly; seed-controlled)
- [x] Data generation pipeline is deterministic (seed-controlled)
- [x] Train/validation/test split is fixed and reproducible (seed-controlled)

## Experiments

- [x] All random seeds are controlled via `src.reproducibility.set_seed()`
- [x] Results reported as mean ± std over ≥3 seeds
- [x] Deterministic algorithms enabled where possible
- [x] Single-run results are explicitly flagged if reported

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
