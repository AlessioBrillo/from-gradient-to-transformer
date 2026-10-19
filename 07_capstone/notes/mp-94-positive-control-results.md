---
tags: [phase/7, research/experiment, type/lesson, state/review]
created: 2026-09-27
updated: 2026-10-14
consumes: [ADR-0028, 07_capstone/_MOC]
---

# MP-94 Session 1 — Positive Control Results (P=59)

> **2026-10-14 correction — this note's "NO-GROK" label carries the same metric
> defect that reversed the P=113 verdict.** Every number above was read through
> the L1-mass k_99, the classifier the 2026-10-08 audit falsified: on the P=113
> GPU re-run (2026-10-14), the same embeddings that read k_99 = 109-110/113
> under L1 read k_energy_90 = 5.7 ± 1.2 of 56 under the energy metric — sparse.
> This run's k_99 = 58/59 is therefore evidence of *noise*, not density: the
> embeddings most likely contained the sparse circuit all along. The manifest and
> its provenance stay valid; the label does not. The checkpoints are gone, so the
> re-measurement is a re-run (now a one-command GPU job), not a re-analysis.
> See the Rung 2 section of portfolio/RESULTS.md for the reversal.
>
> **2026-10-19 — the probe was re-measured; the label is MIXED, not SPARSE.**
> Issue #196 re-ran the P=59 probe with the post-audit energy metric:
> `results/grokking_p59_repo_energy.json` (3 seeds, CPU, 5000 epochs,
> batch 128, weight decay 1.0, cosine LR — the **repo protocol**, not the
> Nanda-faithful one this note's body claims). Per seed:

| Seed | val accuracy | k_energy_90 (of 29) | fraction | energy_sparse |
|------|--------------|---------------------|----------|---------------|
| 42 | 1.0000 | 5 | 0.172 | sparse |
| 43 | 0.9918 | 8 | 0.276 | not sparse |
| 44 | 0.9988 | 7 | 0.241 | sparse |

**Verdict: 2 of 3 seeds sparse — MIXED.** The classification is knife-edge
(the `is_sparse` convention is "90% of the energy in fewer than 25% of the
frequencies": seed 44 sits at 0.241, seed 43 at 0.276), so the honest
reading is "2/3, with one seed's solution slightly denser" — not the
"SPARSE" label a majority rule would have produced. No re-run was attempted
to move the label: re-running a seed until it agrees is selection, not
measurement. The probe's job (a cheap positive control for the recipe) is
done by P=113, which is 3/3 on both protocols.

## Experiment

**Config**: P=59, d_model=128, d_mlp=512, n_heads=4, wd=1.0, cosine LR, embed renorm=on, solo, 5000 epochs, 3 seeds (42, 43, 44)

**Manifest**: `results/phase_diagram_positive_control.json` (git_sha 36b5a58, clean tree)

## Results

| Metric | Mean ± Std (n=3) | Range |
|--------|------------------|-------|
| Final val accuracy | 0.9999 ± 0.0002 | [0.9996, 1.0000] |
| Generalization epoch | 1791 ± 103 | [1699, 1934] |
| k_99 (frequencies for 99% mass) | **58.0 ± 0.0** | [58, 58] |
| k_90 (frequencies for 90% mass) | 45.7 ± 0.5 | [45, 46] |
| Fourier sparsity (1 - H/log P) | 0.107 ± 0.010 | [0.097, 0.120] |
| Top-k mass fraction | 0.697 ± 0.013 | [0.686, 0.715] |

## Interpretation

**NO-GROK CONFIRMED at P=59.** The standard Nanda et al. (ICLR 2023) configuration — which they report produces the sparse Fourier circuit — yields a **dense Fourier representation** (k_99 = 58/59 ≈ 98% of all frequencies) in this repository.

- All 3 seeds generalize perfectly (val acc = 1.0)
- Generalization occurs at epoch ~1791 (consistent with Nanda's "circuit formation" phase)
- But the learned algorithm uses **58 out of 59 Fourier frequencies** — essentially the full basis
- This is NOT the sparse circuit (which would use ~O(√P) ≈ 8 frequencies for P=59)

## Implications for MP-94

1. **The "standard config" is not sufficient** to produce the sparse regime at any P tested so far (P=59, 113).
2. The phase boundary must lie elsewhere in parameter space: higher weight decay, different LR schedule, no renormalization, larger model, or different initialization.
3. The core sweep (MP-94 Session 2) must explore the WD and LR schedule dimensions systematically.
4. Microscope trials from MP-29:
   - Trial 1 (--no-normalize-embeddings): FALSIFIED at P=113 (dense persists)
   - Trial 2 (--schedule constant): NEEDS TESTING
   - Trial 3 (wd=1.5×): NEEDS TESTING

## Next Steps

Run core sweep (configs/phase_diagram_core.yaml) covering:
- P-sweep at Nanda config (WD=1.0): P ∈ {11, 17, 29, 67, 97, 113}
- WD sweep at P=113: wd ∈ {0.1, 0.5, 1.5, 2.0}
- Model-size sweep at P=59: d_model ∈ {64, 256}, n_layers ∈ {2}
- LR schedule at P=59: cosine vs constant
- Renorm ablation at P=59: on vs off
- Joint mode at dissociation config

Target: Find ANY cell with k_99 < P/2 (sparse regime).

## Honesty Ledger Entry

> **2026-09-27 — MP-94 Session 1**: Positive control at P=59 (standard Nanda config, 3 seeds, 5000 epochs) completed. Result: **NO-GROK** — val acc 1.0 all seeds, but Fourier dense (k_99=58/59) all seeds. The sparse Fourier circuit does not emerge under the "standard config" at P=59 in this repository. This matches the P=113 NO-GROK finding. The phase boundary (if it exists) is not at the standard config point.

## See also
- [[07_capstone/notes/positive-control-protocol|Positive-Control Protocol]] — the protocol this run executed.
- [[07_capstone/notes/grokking-verdict-p113|Grokking Verdict P=113]] — the P=113 verdict this control was designed to test.
- [[07_capstone/notes/dense-solutions-modular-addition|Dense Solutions on Modular Addition]] — the characterization the k_99 = 58/59 result feeds.
- [[07_capstone/notes/mp-89-retune-verdict|MP-89 Retune Verdict]] — the NO-MOVE A/B that pushed the investigation toward this control.
