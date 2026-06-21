---
tags: [checklist, reproducibility]
---

# Reproducibility Checklist

Based on Pineau et al., "Improving Reproducibility in Machine Learning Research," JMLR 22(164), 2021.

## Model

- [x] Model architecture is fully specified (source code in `src/models/`)
- [x] All hyperparameters are documented (in experiment configs)
- [ ] Number of parameters reported
- [ ] Training time reported
- [ ] Hardware specifications reported

## Data

- [ ] All datasets used are named and their licenses documented
- [ ] Data processing pipeline is deterministic and documented
- [ ] Train/validation/test split is fixed and reproducible

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

## Paper

- [ ] Results include comparison to a baseline
- [ ] At least one ablation study is included
- [ ] Limitations section is present
- [ ] Primary literature is cited for all key claims
- [ ] Dataset licenses are explicitly stated
