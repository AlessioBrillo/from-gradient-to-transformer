---
tags: [phase/7, type/proof, state/review]
created: 2026-10-12
updated: 2026-10-14
consumes: [07_capstone/research-plan, 07_capstone/notes/grokking-verdict-p113, portfolio/RESULTS]
---

# Capstone Gate — The Honest Negative

> **SUPERSEDED 2026-10-14.** This note's own falsifier fired: the energy-metric
> re-run of Rung 2 found the **sparse** Fourier circuit after all
> (`energy_sparse = 1/1` on 3/3 seeds of both GPU runs, `k_energy_90 = 5.7 ± 1.2`
> of 56 — see portfolio/RESULTS.md, Rung 2). The capstone question is therefore
> answered *positively*: the model implements the sparse Fourier algorithm Nanda
> et al. describe, demonstrated with progress measures and causal ablations. The
> NO-GROK reading this note defended was an artifact of the L1-mass k_99
> classifier — the very failure the 2026-10-08 audit had pinned, now demonstrated
> on the real embeddings. The note below is kept as the record of what the
> negative answer was and why it was wrong; the gate text it answered is now met
> by the positive itself.

## Claim

The Phase 7 gate asks: *someone asks "how does your transformer implement
modular addition?" — explain the Fourier algorithm, show the progress
measures, and demonstrate a causal ablation that confirms the mechanism.*
I can answer all three, and the answer is **not** the sparse Fourier circuit
the question assumed: in this repository's runs the model solves modular
addition with a **dense** embedding that generalizes perfectly. That answer,
defended with committed manifests, passes the gate — because the gate tests
whether I can explain and causally verify what the model *actually* learned,
not whether it learned the textbook algorithm.

## Evidence (every number manifest-backed)

| Claim | Value | Manifest |
|---|---|---|
| The task is solved | val accuracy 1.0000 ± 0.0000, P=113, 3 seeds | `results/exp2_grokking.json` |
| The Fourier representation is dense | k₉₉ = 111/113 (all 3 seeds) | `results/exp2_grokking.json` |
| The dense frequencies are causally load-bearing | keep 59/59 → 0.0000 accuracy | [[07_capstone/notes/grokking-verdict-p113\|grokking verdict P=113]] |
| The dense solution is not an artifact of one config | P=59 positive control, Nanda config, 3 seeds: k₉₉ = 58/59 | `results/phase_diagram_positive_control.json` |
| Joint training does not rescue modular | induction 0.5041 while modular sits at chance 0.0047 | `results/probe_capstone_shakedown.json` |

## Reconstruction (the defense, without notes)

1. **The mechanism.** The model embeds each operand as a superposition of
   Fourier features and multiplies them by attending over the frequency
   basis — but it uses essentially the *whole* basis (111 of 113
   frequencies) rather than the ~O(√P) key frequencies the sparse circuit
   uses. A dense basis still computes (a+b) mod P exactly; what it loses is
   the interpretability that makes the sparse circuit beautiful.
2. **The progress measures.** Generalization (val ≥ 0.9 at epoch 1208 ± 117)
   lands *before* any sparsification of the embedding: the model memorizes
   first, generalizes second — grokking's signature — while the Fourier
   spectrum stays dense throughout. "Grokked" and "sparse circuit" are
   separable outcomes, and this project measured the first without the
   second.
3. **The causal confirmation.** Zeroing all but 59 frequencies collapses
   accuracy to 0.0000: the dense frequencies are the computation, not
   decoration. The neuron-level ablation (`src/experiments/neuron_ablation.py`)
   characterizes the same solution from the MLP side.
4. **What would change my mind.** The Rung 2 verdict is under audit
   (2026-10-08): the L1-mass k₉₉ behind "dense" misclassifies a noisy sparse
   embedding as dense, and the protocol departs from Nanda et al. in five
   ways. The energy-metric re-run (issue #167, GPU) can flip the label —
   which is exactly why the audit is being run before the dense claim is
   published as final. If the energy metric says sparse, the gate answer
   changes to the positive and this note is superseded; the manifests stay
   either way.

## Why this passes

A phase gate that only a positive result can pass is not a gate, it is a
wish. The capstone's purpose is demonstrated end-to-end research capability:
train a model, form a mechanistic hypothesis, test it causally, and report
what is actually there. Every step of that loop ran here, and the result is
a well-characterized negative with its falsifier scheduled. That is the
capstone working, not the capstone failing.

## Links
- [[07_capstone/notes/grokking-verdict-p113|Grokking verdict P=113]] — the full P=113 analysis
- [[07_capstone/notes/mp-94-positive-control-results|MP-94 positive control]] — P=59 NO-GROK
- [[07_capstone/notes/dense-solutions-modular-addition|Dense solutions on modular addition]] — the characterization
- [[portfolio/RESULTS|Honesty Ledger]] — the audit trail this gate answer sits on
- [[00_meta/01_roadmap|Roadmap]] — the gate text this note answers
