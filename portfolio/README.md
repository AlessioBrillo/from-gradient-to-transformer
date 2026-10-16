---
tags: [portfolio]
---

# Portfolio

Research showcase for `from-gradient-to-transformer`. The verified headline finding today is
**Rung 2: grokking modular addition — REPRODUCED 2026-10-14**. The model reaches val accuracy
0.9999 ± 0.0002 on the Nanda protocol (GPU, 3 seeds) with k_energy_90 = 5.7 ± 1.2 of 56
frequencies — the sparse Fourier circuit Nanda et al. describe. The 2026-08-11 NO-GROK verdict
was an L1-mass metric artifact, retracted after the 2026-10-08 audit (see [Honesty Ledger](RESULTS.md#honesty-ledger)).
Rung 3's superposition phase transition remains root-caused, reproduced, and backed by a
multi-seed manifest. See [RESULTS](RESULTS.md) for exact status per rung.

| Artifact | Link |
|----------|------|
| Headline results | [RESULTS](RESULTS.md) |
| Research plan | [research-plan](../07_capstone/research-plan.md) |
| Mini-paper | LaTeX source at [`paper/main.tex`](paper/main.tex); PDF compiled and shipped on the [live site](https://alessiobrillo.github.io/from-gradient-to-transformer/paper.pdf) (`make paper` compiles locally when a TeX toolchain is present) |
| Model card | [model-card](model-card.md) |
| Interactive demo (SAE feature browser) | descoped 2026-10-11: needs a confirmed induction-head checkpoint before real-activation SAE is meaningful (issue #169) |
| Experiment tracking | descoped 2026-10-11: no W&B credentials; manifests on disk are the record (issue #167/#169/#170) |
| Code (experiments) | `src/experiments/` |
| Code (capstone models) | `src/models/decoder_only_transformer.py` — `07_capstone/src/` is empty; see [_MOC](../07_capstone/_MOC.md) |
