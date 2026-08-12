---
tags: [type/lesson, phase/7, research/experiment, state/review]
created: 2026-08-12
---

# Dense Solutions of Modular Addition — the characterization study

## Why this note exists

The P=113 flagship closed NO-GROK: three seeds reached val 1.0 but kept a
dense Fourier representation (k_99 = 111/113 of 113 frequencies). If the
microscope lane and the positive control
([[06_production_ai/notes/microscope-trial-table]],
[[06_production_ai/notes/positive-control-protocol]]) cannot produce a sparse
solution anywhere in the harness, the dense solution is not a footnote to the
negative — it is the algorithm this model actually learned, and it becomes
the phase's headline contribution: *"grokking modular addition at P=113 was
not reproduced under this protocol; here is the algorithm the model found
instead."*

Even if a sparse config IS found, the dense checkpoints remain a legitimate
object of study — the comparison between the two regimes is the interesting
science either way.

## What is known before any new run (reading from disk)

- `results/exp2_grokking.json`: 3/3 seeds at val 1.0, gen epochs
  1250/1048/1326, k_99 = 111/113, k_90 ∈ {92, 94, 92}, total_mass_top_20 ≈
  0.50 ± 0.02, fourier_sparsity (progress measure) ≈ 0.079 ± 0.006.
- The docstring literature: the *ideal* modular-addition function has full
  Fourier support (all P frequencies, the DFT expansion of the addition
  table); Nanda et al.'s sparse solution reaches the same function with ~√P
  frequencies and specific phase structure. My run found a generalizing
  solution in the dense regime — accuracy alone cannot distinguish the two,
  which is exactly why the frozen criterion is conjunctive
  ([[06_production_ai/notes/grokking-verdict-p113]]).

## The study plan (Session 3, pre-registered questions)

1. **Per-head Fourier dictionary.** Which frequencies does each head carry,
   with what amplitude? Dense does not mean uniform — the structure inside
   the 111/113 mass is the first unknown. The dictionary is compared against
   (a) the ideal dense DFT solution and (b) Nanda et al.'s reported sparse
   dictionary. Prediction: the mass concentrates on blocks of frequencies
   per head, with interleaving phase structure — the dense solution is not
   random, it is a different factorization of the same function.
2. **Norm structure per layer.** The sparse solution's embedding rows are
   low-norm and phase-structured. The dense solution's are unit-norm by
   construction (the renormalization that was on). The interaction between
   the in-place renormalization and the learned representation is measured,
   not assumed — comparison against trial 1's no-norm runs if they exist.
3. **Frequency ablation on the dense circuit.** The exp2 ablation instrument
   already exists; the question is which frequencies are *causal* on the
   dense solution — does ablating the top-k carry the same failure signature
   as on the sparse circuit? Prediction: no small ablation collapses
   accuracy — the dense solution's robustness is distributed, which is
   itself the explanation for why it settled (a flat energy landscape under
   the norm constraint).
4. **SAE reading of the dense residual stream.** Train the dashboard SAE on
   dense-solution activations vs. the synthetic baseline: L0, FVE, dead
   features. Prediction: FVE stays high but L0 stays high too — a dense
   residual stream is reconstructible densely, and the features found are
   not the clean dictionary the sparse circuit would produce. The honest
   delta paragraph is written either way.
5. **The falsification column, filled before the runs.** Every claim above
   gets its "what would falsify this" line: e.g., "the dictionary is
   uniform with no per-head structure" falsifies claim 1; "some 10-frequency
   ablation near-totally collapses accuracy" falsifies claim 3.

## What the study owes the record

- Every number manifest-tagged (`results/*.json` + `<!-- manifest: -->` in
  RESULTS.md) — no prose-only numbers, per the standing provenance law.
- The paper's Grokking section reads this note as its source once the
  characterization is written from disk.
- The graduation proof (ADR-0003 row 7) is assembled from this note's three
  instrument families: Fourier, progress measures, causal ablation.

## Links

- [[00_meta/28_micro-phase-29-the-positive-negative]] — the roadmap whose
  Session 3 executes this study.
- [[06_production_ai/notes/grokking-verdict-p113]] — the verdict note this
  study extends; checkpoints and figures indexed there.
- [[06_production_ai/notes/microscope-trial-table]] ·
  [[06_production_ai/notes/positive-control-protocol]] — the lanes that
  decide whether this study is headline or comparison.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every number cites.
- [[portfolio/RESULTS]] — the Rung 2 section this study rewrites.