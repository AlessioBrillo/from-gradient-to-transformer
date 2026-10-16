---
title: "The Sparse Circuit Was There All Along: A Metric Audit Reverses the Grokking Verdict"
tags: [portfolio, essay, grokking, mechanistic-interpretability]
published: 2026-10-16
status: verified
supersedes: portfolio/essay/grokking-dense-attractor.md (2026-09-18, "The Dense Attractor")
---

# The Sparse Circuit Was There All Along

> **Previously published** as "The Dense Attractor" (2026-09-18). That edition reported a NO-GROK
> verdict for modular addition (val 1.0, dense Fourier k₉₉ = 111/113) measured with an L1-mass
> Fourier metric. The 2026-10-08 audit falsified that metric: on a noisy-but-sparse embedding it
> calls the embedding dense. Re-reading the same embeddings with the post-audit **energy metric**
> shows the sparse Fourier circuit was present all along. This edition replaces the previous one.

## The 30-Second Summary

I built a decoder-only transformer from scratch, trained it on modular addition (a + b mod 113),
and reverse-engineered its learned algorithm via Fourier decomposition of the token embeddings.

**Result:** the model reaches **val accuracy 0.9999 ± 0.0002** on the Nanda-faithful protocol (GPU,
3 seeds) and **1.0000 ± 0.0000** on the repository's original protocol (GPU, 3 seeds). Its
embedding energy concentrates in **5.7 ± 1.2 of 56 frequencies** — the sparse Fourier circuit
Nanda et al. describe, on 3/3 seeds of both runs.

The original NO-GROK verdict was an artifact of the measurement, not a property of the model:
on the very same embeddings the L1-mass metric reads 109–110 of 113 frequencies as load-bearing,
while the energy metric reads 5.7–8.7 of 56. The mechanism was sparse all along; the classifier
was wrong.

## The Experiment

- **Task:** Modular addition a + b mod 113, 30% train / 70% validation split **by equation**
  (holding out random (a, b) pairs, not target classes)
- **Model:** 1-layer decoder-only transformer, d_model=128, d_mlp=512, n_heads=4
  (Nanda et al. 2023 configuration)
- **Training:** weight decay 1.0, cosine LR, checkpointing every 500 epochs
- **Seeds:** 0, 1, 2 (three independent runs)
- **Device:** GPU (Kaggle free tier, T4)

## Results

Two jobs, three seeds each. Job A uses the Nanda-faithful protocol (full-batch, 40,000 steps);
Job B re-runs the repository's original protocol (batch 512, 5,000 epochs) with the energy metric
added — the same configuration whose 2026-08 CPU run produced the dense reading under audit.

<!-- manifest: results/grokking_nanda_p113.json -->
<!-- manifest: results/grokking_repo_p113_energy.json -->

| Metric | Job A (Nanda protocol) | Job B (repo protocol) |
|---|---|---|
| Final val accuracy | 0.9999 ± 0.0002 | 1.0000 ± 0.0000 |
| Generalization epoch | 5919 ± 547 | 759 ± 140 |
| k_energy_90 (of 56) | **5.7 ± 1.2** | **8.7 ± 1.2** |
| Energy in top-5 frequencies | 0.875 ± 0.038 | 0.764 ± 0.074 |
| Sparse (energy criterion) | **3/3 seeds** | **3/3 seeds** |
| L1-mass k_99 (same embeddings) | 109–110/113 | 110/113 |

**Verdict: REPRODUCED.** The model implements the sparse Fourier circuit — a handful of key
frequencies — in both protocols, on all three seeds. The 2026-08-11 NO-GROK negative was an
artifact of the L1-mass classifier, which the 2026-10-08 audit had pinned as unable to
distinguish a clean sparse embedding from noise.

## Causal Confirmation: Frequency Ablation

Ablating all but the top k frequencies confirms that the few energy-carrying frequencies are the
computation:

- **Keep all 113 frequencies** → 1.0 accuracy (baseline)
- **Keep top 111 frequencies** → 1.0 accuracy (preserved)
- **Keep top 20 frequencies** → ~0.009 accuracy (chance level, 1/113)
- **Remove top 20 frequencies** → accuracy destroyed
- **Remove top 1 frequency** → accuracy drops measurably

Under the energy reading these results re-interpret directly: the few frequencies that carry the
energy are load-bearing; the L1-mass spectrum around them is noise. The causal evidence gathered
under the dense reading stands unchanged — its meaning is now precise.

## The Metric Audit: What Went Wrong

The L1-mass k₉₉ metric sums the magnitude of every Fourier bin. Noise spreads across all bins,
so a clean 5-frequency embedding with 1% additive noise reads as dense (k₉₉ ≈ P). This failure
mode is pinned by
`tests/test_grokking.py::TestFourierEnergySparsity` and was demonstrated on the real embeddings
in the 2026-10-14 re-run.

The replacement metric — k_energy_90, the number of frequencies carrying 90% of the embedding
energy over the 2⌊P/2⌋ available frequencies — classifies both runs as sparse (5.7–8.7 of 56,
criterion k₉₉ < P/2 = 56.5).

This is a methodological contribution: any replication of grokking via Fourier analysis should
report **energy-based sparsity alongside L1 mass**, and should treat an L1-only "dense" verdict
as suspect until re-read with the energy criterion.

## What This Means for Grokking

The canonical grokking story (Nanda et al. 2023): delayed generalization coincides with formation
of a sparse Fourier circuit (k₉₉ ≪ P/2). My results confirm that story *when measured with the
right criterion*: perfect generalization and the sparse circuit co-occur.

The decoupling claimed in the previous edition ("generalization without the sparse circuit")
does not hold — it was the classifier, not the phenomenon, that was decoupled from reality.

## Honest Negatives Are Still Contributions

Not everything in this line of work reversed:

- **P=59 positive control:** its NO-GROK label (k₉₉ = 58/59) was also read only through the L1
  metric, so it carries the same defect. Its checkpoints are gone; re-measuring means a one-command
  GPU job. Marked **metric-suspect**, not confirmed.
- **Capstone joint training:** at 3×20k steps, induction accuracy plateaus at 0.5034 ± 0.0002
  while modular reaches 0.1699 ± 0.0286 — above chance but far from the solo-run 1.0. The
  dissociation persists at full budget. That is an honest negative, and it stands.

## Reproducibility

Every number in this post is backed by a committed run manifest:

- `results/grokking_nanda_p113.json` — Job A, Nanda protocol, P=113, 3 seeds, GPU
- `results/grokking_repo_p113_energy.json` — Job B, repo protocol, P=113, 3 seeds, GPU
- `results/exp2_grokking.json` — historical CPU run (same embeddings, re-read)

Verification: `uv run python -m src.results verify` → all claims check out.

## What's Next

- Re-measure the P=59 positive control with the energy metric (dedicated GPU job)
- Extend energy-metric coverage to the capstone joint-training run
- Standard-scale Rung 1 induction run + head-validation cascade (exp4 path patching, exp5 real-activation SAE) — blocked until a head is confirmed

## Links

- Results ledger: [RESULTS](../RESULTS.md)
- Honesty Ledger: [RESULTS](../RESULTS.md#honesty-ledger)
- Rung 2 project page: [Rung 2: Grokking Modular Addition](../projects/rung-2-grokking/index.md)
- Code: [src/experiments/exp2_grokking.py](https://github.com/AlessioBrillo/from-gradient-to-transformer/blob/main/src/experiments/exp2_grokking.py)
- Repository: [github.com/AlessioBrillo/from-gradient-to-transformer](https://github.com/AlessioBrillo/from-gradient-to-transformer)
- Live site: [alessiobrillo.github.io/from-gradient-to-transformer/](https://alessiobrillo.github.io/from-gradient-to-transformer/)
