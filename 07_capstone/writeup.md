---
title: "Writeup — Reverse-Engineering a Micro-Transformer"
tags: [type/lesson, phase/7, capstone, writeup, state/consolidated]
created: 2026-10-11
---

# Writeup — Reverse-Engineering a Micro-Transformer

**Status: written from the manifests, 2026-10-11.**

This document used to be a skeleton of *expected* outcomes. Section 2 said the
Fourier decomposition "embeds into sparse frequencies" and that "ablating the
remaining ~95% **improves** it" — the opposite of what was measured. Section 3
still carried a conditional "*If this is the primary flagship (grokking
fallback):*", a branch the 2026-08-11 NO-GROK verdict had already settled. It is
now written against `results/*.json`, and every number is tagged.

The authority on what is true is [[portfolio/RESULTS]]; this is the narrative.

## 1. Thesis and motivation

From gradient to transformer to circuit: the case for small-scale mechanistic
interpretability. The foundational MI results were *obtained on tiny models*
(1–2 layers, single-digit millions of parameters). Small scale is the *native*
setting for circuit discovery, not a compromise — which is why the capstone
trains a 4.26M-parameter model rather than borrowing a 7B one.

The arc: train → observe emergence → form causal hypotheses → test with
interventions → extract features.

## 2. Grokking modular addition

**Verdict: NO-GROK — under audit since 2026-10-08.**
<!-- manifest: results/exp2_grokking.json -->

Setup: 1-layer transformer, `a + b mod 113`, 30% train fraction split **by
equation** (random pairs held out, not target classes), AdamW with weight decay
1.0, three seeds to 5000 epochs.

Measured: all three seeds reach **validation accuracy 1.0**, at generalization
epochs 1048 / 1250 / 1326 (mean 1208 ± 117). The model solves the task. But its
embedding spectrum is **dense**: *k₉₀* = 92.7 ± 0.9 and *k₉₉* = 111/113, against
a sparsity criterion of *k₉₉* < P/2 = 56.5. Fourier sparsity (normalized entropy)
is 0.079 ± 0.006, deep in the dense regime.

The causal test agrees with the spectral one. Keeping the top 111 of 113
frequencies preserves accuracy 1.0; keeping only the top 20 drops it to chance
(1/113); removing the top 20 from the full set destroys it. The model uses
essentially *all* frequencies — a dense Fourier representation, not the sparse
circuit the grokking literature describes.

**The audit.** The *k₉₉* metric behind that verdict used an L1 mass threshold over
*magnitudes*, which classifies a noisy-but-sparse embedding as dense. The
replacement (`fourier_energy_sparsity`, with planted-weights tests in
`tests/test_grokking.py::TestFourierEnergySparsity`) is implemented; the re-run
itself is issue #167 and needs a GPU. Until it lands this verdict is not citable.

The positive control is manifest-backed and never was: P=59 with the Nanda-faithful
config, 3 seeds, 5000 epochs → *k₉₉* = 58.0 ± 0.0, validation accuracy
0.9999 ± 0.0002. **NO-GROK confirmed at P=59.**
<!-- manifest: results/phase_diagram_positive_control.json -->

See [[06_production_ai/notes/grokking-verdict-p113]] (the verdict),
[[06_production_ai/notes/positive-control-protocol]] (the protocol), and
[[06_production_ai/notes/dense-solutions-modular-addition]] (the characterised
regime).

## 3. Induction heads

**Verdict: no head detected at any scale run (0/8).**
<!-- manifest: results/exp1_induction_heads.json -->

Setup: 2-layer attention-only transformer on repeated random tokens. Peak
per-head diag+1 attention mass reaches 0.177 ± 0.006 against the 0.3 detection
threshold of Olsson et al. (2022). The extended 10k-epoch run did not cross it
either — see [[04_nlp_and_transformers/notes/induction-extended-run]].

The one solid, matched finding is **fixed versus fresh batches** at otherwise
identical configs: validation accuracy 0.05% (loss 24.31) with a fixed training
set versus 52.2% (loss 3.65) with fresh batches each epoch. The default
fixed-batch regime makes the task ill-posed, so the 0/8 number describes that
regime rather than the ceiling of the method. See
[[04_nlp_and_transformers/notes/induction-heads]].

## 4. Toy models of superposition

**Verdict: fully reproduced — the only rung that is.**
<!-- manifest: results/exp3_superposition.json -->

Tiny ReLU autoencoder with a real bottleneck, sparse features. As sparsity drops,
represented features rise from 10/20 to 19.67 ± 0.47 of 20. In the sparse regime
five features settle on a regular pentagon in two dimensions (inter-angle gaps
70.2–73.8°, standard deviation ≤ 1.4°), matching the geometry Elhage et al.
(2022) predicts. See [[04_nlp_and_transformers/notes/superposition-and-feature-capacity]].

## 5. Circuit discovery via activation patching

**Verdict: activation patching clean; path patching unit-tested only.**
<!-- manifest: results/exp4_circuit_patching.json -->

Validation accuracy 0.489 ± 0.014; mean logit-difference recovery 0.197 ± 0.007
across patched sites. **0/4 heads** detected in the model patched, which is why
head ablation and path patching were not run: they have nothing to target. The
retracted pre-fix recovery numbers were removed with their replacement, not left
dangling. See [[04_nlp_and_transformers/notes/activation-patching]] and
[[04_nlp_and_transformers/notes/path-patching]].

## 6. Sparse autoencoder extraction

**Verdict: synthetic reproduces; real activations are dense.**
<!-- manifest: results/exp5_sae_dashboard.json -->

Synthetic baseline: L0 96.60/512 (18.9% active), FVE 0.9749, MSE 0.00101, 39/512
dead features — the sparsity/reconstruction tradeoff behaves as Bricken et al.
(2023) describe.

On real residual-stream activations the reconstruction is better and the features
are *not* sparse: L0 136.25/256 (53.2% active), FVE 0.9997, 0/256 dead. A
32-dimensional residual stream from a small model with no confirmed induction
head may simply not contain disentangled features yet. Reported as an honest gap
rather than a result. See [[06_production_ai/notes/results-manifests-and-provenance]].

## 7. Capstone: joint training

**Verdict: a clean dissociation, and a falsified pair of hypotheses.**
<!-- manifest: results/probe_capstone_shakedown.json -->

Joint modular-addition + induction training for 2000 steps dissociates the two
tasks: induction accuracy rises to 0.5041 while modular stays at chance (0.0047
against 1/113 = 0.0088), with dense Fourier (*k₉₉* = 98.1 of P=113) and a
K-composition score of 0.394 that is explicitly `_vacuous` — no head exists to
attribute it to. See [[07_capstone/notes/mp-88-shakedown-verdict]].

The 500-step retune A/B falsified both standing hypotheses for why modular stays
at chance. Dedicated vocab offset (the shared-embedding interference hypothesis):
modular 0.0060. Curriculum reweight (the schedule hypothesis): modular 0.0065.
Control: 0.0062. All three *below* chance. **NO-MOVE.**
<!-- manifest: results/probe_capstone_ab_control.json -->
<!-- manifest: results/probe_capstone_ab_offset.json -->
<!-- manifest: results/probe_capstone_ab_reweight.json -->

See [[07_capstone/notes/mp-89-retune-verdict]].

## 8. Limitations

- Micro-scale models: findings may not transfer to 7B+ models.
- Modular addition is cleaner than natural language; circuits found here may not
  be representative.
- Attribution patching is a first-order approximation and is **not implemented**
  in this repo — see [[04_nlp_and_transformers/notes/attribution-patching]] for
  what it would take and why it has not been done.
- Activation patching can mislead via layernorm denominator effects and subspace
  projection illusions (Makelov, Lange & Nanda, 2023).
- SAE interpretability is human-judged, and features can be illusory.
- No induction head has ever been confirmed here, so the Rung 1 → 4 → 5 cascade
  is blocked at its first link. Every path-patching and SAE-on-real-activations
  claim is downstream of that.
- Single architecture family, single seed distribution — no claim of universality.

## 9. What I actually understood

- The residual stream is the single most useful abstraction: a shared vector
  space every layer reads from and writes to.
- Attention heads are not monolithic: QK computes *where* to look, OV computes
  *what* to copy, and they train independently.
- Grokking is not magic: it is the competition between memorization and
  generalizing circuits, mediated by weight decay. And a model can solve modular
  addition *without* the circuit the literature describes — which is this repo's
  headline negative.
- A detector's threshold is a hypothesis. `diag+1 ≥ 0.3` and `k₉₉ < P/2` are both
  choices, and both turned out to need re-derivation here.
- The hardest part of MI is not running experiments — it is forming precise,
  falsifiable hypotheses. The tools are easier than the thinking.
- **A negative result honestly reported is more valuable than a positive result
  overclaimed.** Four audits have caught real bugs in this repo's own claims, and
  they are all still visible in [[portfolio/RESULTS]].

## Links

- [[07_capstone/research-plan]] — the original ladder, timeline and distinctiveness gate
- [[07_capstone/execution-log]] — what was actually run, with dates
- [[portfolio/RESULTS]] — the Honesty Ledger, the authority on what is true
- [[07_capstone/_MOC]] — Phase 7 index and per-rung status
