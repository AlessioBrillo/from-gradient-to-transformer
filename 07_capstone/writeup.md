---
title: "Writeup — Reverse-Engineering a Micro-Transformer"
tags: [type/lesson, phase/7, capstone, writeup, state/consolidated]
created: 2026-10-11
updated: 2026-10-16
---

## Writeup — Reverse-Engineering a Micro-Transformer

**Status: written from the manifests, 2026-10-16.**

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

**Verdict: REPRODUCED 2026-10-14 — the 2026-08-11 NO-GROK was an L1-mass
metric artifact, retracted.**
<!-- manifest: results/grokking_nanda_p113.json -->
<!-- manifest: results/grokking_repo_p113_energy.json -->

Setup: 1-layer decoder-only transformer, `a + b mod 113`, 30% train fraction
split **by equation** (random pairs held out, not target classes), AdamW with
weight decay 1.0, cosine LR, three seeds to 40,000 full-batch steps (Job A,
Nanda-faithful protocol) and 5,000 epochs (Job B, historical repo protocol),
both on GPU.

Measured: Job A reaches **validation accuracy 0.9999 ± 0.0002** with
generalization epoch 5919 ± 547; Job B reaches **1.0000 ± 0.0000** with
generalization epoch 759 ± 140. The model solves the task. Its embedding energy
concentrates in **k_energy_90 = 5.7 ± 1.2 of 56 frequencies** (Job A) and
**8.7 ± 1.2 of 56** (Job B) — below the sparsity criterion k₉₀ < P/2 = 56.5 —
on 3/3 seeds of both runs. The sparse Fourier circuit Nanda et al. describe is
real.

**The audit.** The *k₉₉* metric behind the 2026-08-11 NO-GROK verdict used an
L1-mass threshold over magnitudes, which classifies a noisy-but-sparse
embedding as dense — demonstrated by
`tests/test_grokking.py::TestFourierEnergySparsity` and, decisively, by
re-reading the same embeddings both ways (L1 reads 109–110/113 dense; energy
reads 5.7–8.7/56 sparse). The training, the split fix, the checkpoint
machinery and the multi-seed manifests were all correct throughout; only the
reading was wrong. See the Honesty Ledger in [[portfolio/RESULTS]].

**Causal confirmation.** Frequency ablation confirms the mechanism: keeping
the top 111 of 113 frequencies preserves accuracy 1.0; keeping only the top 20
drops it to chance (1/113); removing the top 20 destroys it. The few
energy-carrying frequencies are load-bearing; the L1-mass spectrum around them
is noise.

The positive control P=59 (k₉₉ = 58/59) was read only through the L1 metric, so
its NO-GROK label carried the same defect. It was re-measured with the energy
metric on 2026-10-19 and came back **MIXED — 2 of 3 seeds sparse**, a boundary
cell rather than a confirmation, and it is reported as one.
<!-- manifest: results/phase_diagram_positive_control.json -->
<!-- manifest: results/grokking_p59_repo_energy.json -->

See [[07_capstone/notes/grokking-verdict-p113]] (the verdict),
[[07_capstone/notes/positive-control-protocol]] (the protocol), and
[[07_capstone/notes/dense-solutions-modular-addition]] (the characterised
regime).

## 3. Induction heads

**Verdict: a head forms and it copies by a fixed offset — the content-based
claim is still open (2026-10-20).**
<!-- manifest: results/exp1_induction_heads.json -->
<!-- manifest: results/induction_standard_emergence.json -->
<!-- manifest: results/induction_standard.json -->

Setup: 2-layer attention-only transformer on repeated random tokens. The old
detector measured the attention mass on `q-1` (the previous token) and called
it "diag+1"; the copy offset on this task is `q-(L-1)`. Its peak was
0.177 ± 0.006 against a 0.3 threshold — but on the wrong offset, so it is not
evidence about induction heads. The corrected detector
(`src/experiments/induction_detection.py`) reports the induction mass on the
copy offset with the previous-token mass as a control, and confirms a head only
when the K-composition mechanism agrees.

**The standard-scale run, with the corrected detector (GPU, 3 seeds, 3000
epochs = 384k steps per seed):** a head is confirmed on **every seed —
3.00 ± 0.00 heads**, all of them in the first layer (0.00 above it), with
copy-offset mass **0.8084 ± 0.0700** at the final checkpoint against a previous-token control of
0.0470 ± 0.0251. It appears early: the emergence run confirms it at
**epoch 100** (3.33 ± 0.47 heads per seed, 12.8k steps, mass 0.9485 ± 0.0186). The two-step circuit is
absent: the K-composition score is 0.0833 ± 0.0335. (Re-measured on 2026-11-17 after the
seeding fix; the first measurement, 2026-10-20, was 2.67 ± 0.47 heads, mass 0.9451 ± 0.0013,
K-composition 0.0521 ± 0.0075, and is kept as `results/induction_standard_pre_seedfix.json`.)

**And it is not an induction head.** The dissociation probe — the only
measurement that can separate the two mechanisms on this task — reads
**content mass 0.0311 ± 0.0001 against period mass 0.8088 ± 0.0696**:
the copy follows the fixed offset. That is not a detector artefact and not a
scale problem: on a perfectly periodic task the previous occurrence of a token
is *always* at `q-L`, so "attend to `q-L+1`" and "attend to the token after
the previous occurrence" are **the same function**, and the task does not
contain the question the rung asks. The honest name for this head is a
**prefix-copying head**.

The task that does contain the question — the same structure with the repeats
at *varying* distances, where the best single fixed offset explains 17.6% of
the copy queries — is specified in ADR-0033 and pre-registered in
[[07_capstone/notes/variable-distance-induction-preregistration]]. It **ran on
GPU on 2026-11-09 and was run again on 2026-11-17, after the seeding fix** (3 seeds
× 3000 epochs, manifest `results/induction_content.json`; the first run is kept as
`results/induction_content_pre_seedfix.json`). The re-run is the record, and it
changes the verdict:

- the **behaviour** is content-based on 3/3 seeds — copy accuracy 0.9968 / 0.9997 / 0.9995
  and non-modal accuracy 0.9962 / 0.9996 / 0.9995, against a
  best-single-fixed-offset baseline of 0.1646 / 0.1550 / 0.1584;
- the **causal** measurement is **not the same circuit on every seed**: the
  largest single-head ablation drop is 0.8903 / 0.9469 / 0.0275 and the group
  ablation 0.9938 / 0.9469 / 0.9940 — one head on seed 1, a distributed
  group on seeds 0 and 2;
- the **pre-registered per-head rule confirms no head on any seed**: the
  K-composition score (0.0407 / 0.0347 / 0.1311) stays far below
  the 0.40 bar.

So the verdict is **NEGATIVE**, for the pre-registered reading and for the causal
addendum alike. Before the fix it was PARTIAL (one head confirmed on seed 0, "a single
head on 3/3 seeds"); the behaviour is unchanged and the circuit is not, which makes
"the circuit on this task" a description of one initialization. The open question is
now **what the distributed groups compute**. The candidate explanation (a two-stage
circuit in which the first layer writes *where* and the second reads *what*) is
untested, and the K-composition measure cannot see it, because it assumes the first
layer's argmax *is* the previous occurrence. See [[portfolio/RESULTS]] for the full
table.

<!-- manifest: results/induction_content.json -->
<!-- manifest: results/exp4_content.json -->

The one solid, matched finding is **fixed versus fresh batches** at otherwise
identical configs: validation accuracy **0.46% ± 0.03%** (fixed, reused every
epoch) versus **53.52% ± 0.01%** (fresh, resampled every epoch), matched
3-seed comparison at 800 epochs (re-measured 2026-11-17 after the seeding fix; first measurement 0.45% against 53.53%). The fixed-batch regime makes the task
ill-posed (birthday-problem collision >99.99% at the old V=32 default), and the
fixed dataset actively harms generalization (val loss climbs to 24.3). The
default config (`vocab_size=2048` standard / `256` quick) was not the config
that produced the prose-only "0.05% vs 52.2%" quoted in nine documents with no
manifest behind it — those numbers are replaced by the manifest-backed values
above.

<!-- manifest: results/exp1_induction_fixed_batches.json -->
<!-- manifest: results/exp1_induction_fresh_batches.json -->

See [[04_nlp_and_transformers/notes/induction-heads]].

## 4. Toy models of superposition

**Verdict: fully reproduced.**
<!-- manifest: results/exp3_superposition.json -->
<!-- manifest: results/exp3_superposition_sweep.json -->

Tiny ReLU autoencoder with a real bottleneck, sparse features. As sparsity
drops, represented features rise from 10/20 to 20.00 ± 0.00 of 20 — and the
three-seed sweep records the same transition (10.00 ± 0.00 of 20 at sparsity
0.5, 20.00 ± 0.00 by sparsity 0.05, degrading to 16.33 ± 0.94 at sparsity
0.001). In the sparse
regime five features settle on a regular pentagon in two dimensions (inter-angle
gaps 70.2–73.8°, standard deviation ≤ 1.4°), matching the geometry Elhage et
al. (2022) predicts. See [[04_nlp_and_transformers/notes/superposition-and-feature-capacity]].

## 5. Circuit discovery via activation patching

**Verdict: the cascade ran end to end on Rung 1's own checkpoint — and the
head it found is a prefix-copying one (2026-10-20).**
<!-- manifest: results/exp4_circuit_patching.json -->
<!-- manifest: results/exp4_standard.json -->

Since 2026-10-19 this rung analyses **Rung 1's own checkpoint**
(`--from-checkpoint`) instead of training a second, differently shaped model,
so the three rungs measure one model. On the standard-scale checkpoint
(epoch 3000, 3 seeds) the interventions land: **head ablation 0.5895 ± 0.1405** and **path patching 0.7052 ± 0.0411** of the answer-vs-counterfactual
logit difference (re-measured 2026-11-17; the first measurement was 0.4445 ± 0.0425 and
0.8215 ± 0.1255) — the first end-to-end path-patching result in this
repository against a real head.

What the interventions validate is the **method**. The head they point at
copies by a fixed offset (probe: content 0.0310 ± 0.0002 against period
0.8096 ± 0.0694), so the circuit they certify is a prefix-copying circuit,
not an induction circuit. The cascade has to be re-run on a content-based
checkpoint before it says anything about induction.

The retracted pre-fix numbers were removed with their replacement, not left
dangling: the **0/4 heads** figure is retracted with the rest (2026-10-19),
because this rung's old detector measured the strict upper triangle of a
causal softmax, which is identically zero and could never fire on any model.
See [[04_nlp_and_transformers/notes/activation-patching]] and
[[04_nlp_and_transformers/notes/path-patching]].

## 6. Sparse autoencoder extraction

**Verdict: synthetic reproduces; on real activations the dictionary is sparse
but eight times too wide (2026-10-20).**
<!-- manifest: results/exp5_sae_dashboard.json -->
<!-- manifest: results/exp5_real_activations.json -->

Synthetic baseline: L0 96.60/512 (18.9% active), FVE 0.9749, MSE 0.00101, 39/512
dead features — the sparsity/reconstruction tradeoff behaves as Bricken et al.
(2023) describe.

On the real residual-stream activations of Rung 1's standard-scale checkpoint
(d_model 64) the reconstruction is essentially perfect (FVE 0.99998, MSE
0.0005) and the features are *sparse*: **L0 19.01/512 (3.7% active)**. The
open question is not the sparsity but the **size**: the dictionary is about
eight times wider than the 64-dimensional residual stream it has to cover,
and **65.6% of its features never fire** (dead rate 0.6562) — a dictionary
that is too large for its input has to be, and the honest reading is that the
sparsity measurement is evidence about the *over-completeness*, not yet about
a disentangled feature set. See [[06_production_ai/notes/results-manifests-and-provenance]].

## 7. Capstone: joint training

**Verdict: a clean dissociation, and a falsified pair of hypotheses.**
<!-- manifest: results/probe_capstone_shakedown.json -->
<!-- manifest: results/capstone_20k.json -->

Joint modular-addition + induction training for 2000 steps (shakedown,
seed 0) dissociates the two tasks: induction accuracy rises to 0.5041 while
modular stays at chance (0.0047 against 1/113 = 0.0088), with dense Fourier
(k₉₉ = 98.1 of P=113) and a K-composition score of 0.394 that is explicitly
`_vacuous` — no head exists to attribute it to.
See [[archive/process/capstone-notes/mp-88-shakedown-verdict]].

The 3×20,000-step capstone run (configs/capstone.yaml, d_model=256, 4 layers,
8 heads, GPU, 3 seeds) shows the dissociation **persists at full budget**:
induction accuracy 0.5034 ± 0.0002 (the same plateau as the 2k shakedown —
structural, not a budget artifact) and modular accuracy 0.1699 ± 0.0286,
above chance but far from the solo-run 1.0. The design's prediction that a
longer budget would let both tasks develop is falsified.
See [[07_capstone/execution-log]] and [[07_capstone/design]].

The 500-step retune A/B falsified both standing hypotheses for why modular stays
at chance. Dedicated vocab offset (the shared-embedding interference hypothesis):
modular 0.0060. Curriculum reweight (the schedule hypothesis): modular 0.0065.
Control: 0.0062. All three *below* chance. **NO-MOVE.**
<!-- manifest: results/probe_capstone_ab_control.json -->
<!-- manifest: results/probe_capstone_ab_offset.json -->
<!-- manifest: results/probe_capstone_ab_reweight.json -->

See [[archive/process/capstone-notes/mp-89-retune-verdict]].

## 8. Limitations

- Micro-scale models: findings may not transfer to 7B+ models.
- Modular addition is cleaner than natural language; circuits found here may not
  be representative.
- The sparse Fourier circuit has been observed under the energy metric (Rung 2,
  both protocols, 3/3 seeds); the capstone joint run is dense under the same
  metric (k_energy_90 = 49.0 of 56, sparse on 0/3 seeds).
- No *content-based* induction head has been confirmed here. A prefix-copying
  head forms at standard scale and the causal interventions land on it
  (ablation 0.5895, path patching 0.7052), but on the periodic task the two
  mechanisms are the same function, and the probe says the copy is the
  positional one. The content-based task that separates them ran on GPU
  (issue #200, 2026-11-09, repeated 2026-11-17 after the seeding fix): the copy **is**
  content-based on 3/3 seeds (0.9968–0.9997, non-modal 0.9962–0.9996,
  against a 0.155–0.165 fixed-offset baseline), but the pre-registered per-head rule
  — content mass ≥ 0.30 on the confirmed head, K-composition ≥ 0.40 — confirms a
  head on **no** seed (before the fix: 1/3). The pre-registered verdict is therefore
  **NEGATIVE**, and so is the causal addendum, and the word "induction head" is not
  used for this task. The circuit is one head on one seed and a distributed group on
  the other two, so what is still missing is the *mechanism*, and the candidate
  explanation (a two-stage circuit the K-composition measure cannot see) is untested.
  <!-- manifest: results/induction_content.json -->
  <!-- manifest: results/exp4_content.json -->
  The standard-geometry CPU de-risk of 2026-10-25
  (`results/induction_content_derisk_standard.json`) was a pilot — 600
  epochs on 2048 training samples against the run's 3000 epochs on 8192 —
  and it read differently from the first full run: a group ablation of 0.9956 with
  a largest single-head drop of 0.0986, i.e. a **distributed** circuit where
  the first full run measured a **single** head. The 2026-11-17 re-run after the seeding fix
  agrees with the pilot on two seeds out of three (a distributed group), which suggests the
  pilot was not the outlier. The verdict never depended on it, but it is the reason
  the pre-registration asked for a circuit-level report at all.
  <!-- manifest: results/induction_content_derisk_standard.json -->
- The real-activation SAE is sparse (L0 3.7%) but its dictionary is ~8× wider
  than the residual stream and 66% of its features never fire: the sparsity is
  evidence about the over-completeness, not yet about disentanglement.
- Attribution patching is a first-order approximation and is **not implemented**
  in this repo — see [[04_nlp_and_transformers/notes/attribution-patching]] for
  what it would take and why it has not been done.
- Activation patching can mislead via layernorm denominator effects and subspace
  projection illusions (Makelov, Lange & Nanda, 2023).
- SAE interpretability is human-judged, and features can be illusory.
- Single architecture family, single seed distribution — no claim of universality.

## 9. What I actually understood

- The residual stream is the single most useful abstraction: a shared vector
  space every layer reads from and writes to.
- Attention heads are not monolithic: QK computes *where* to look, OV computes
  *what* to copy, and they train independently.
- Grokking is not magic: it is the competition between memorization and
  generalizing circuits, mediated by weight decay. The sparse Fourier circuit is
  real when measured with the energy criterion — and the 2026-08-11 NO-GROK
  was the classifier's fault, not the model's.
- A detector's threshold is a hypothesis. `diag+1 ≥ 0.3` and `k₉₉ < P/2` are
  both choices, and both turned out to need re-derivation here.
- The hardest part of MI is not running experiments — it is forming precise,
  falsifiable hypotheses. The tools are easier than the thinking.
- **A negative result honestly reported is more valuable than a positive result
  overclaimed.** Thirteen audits have caught real bugs in this repo's own claims, and
  they are all still visible in [[portfolio/RESULTS]].

## Links

- [[07_capstone/research-plan]] — the original ladder, timeline and distinctiveness gate
- [[07_capstone/execution-log]] — what was actually run, with dates
- [[portfolio/RESULTS]] — the Honesty Ledger, the authority on what is true
- [[07_capstone/_MOC]] — Phase 7 index and per-rung status
