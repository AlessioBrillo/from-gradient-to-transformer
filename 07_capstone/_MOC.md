---
tags: [type/moc, phase/7, capstone, state/review]
---

# Phase 7 · Capstone — MOC

Index and links for the capstone phase. Detailed plan: [[07_capstone/README]].

## Key documents
- [[07_capstone/notes/mp-78-session-0-preparation-capstone-integration-publication-roadmap|MP-78 Session 0: Capstone Integration Roadmap]] — the integration plan that set the shakedown sequence.
- [[07_capstone/notes/mp-78-session-capstone-checkpoint-fix|MP-78 Checkpoint Fix]] — the step-500 crash that broke the shakedown, fixed test-first.
- [[07_capstone/notes/mp-88-shakedown-verdict|MP-88 Shakedown Verdict]] — the joint-training dissociation: induction 0.504, modular at chance.
- [[07_capstone/notes/mp-89-retune-verdict|MP-89 Retune Verdict]] — NO-MOVE: vocab-offset and reweight arms both fail to lift modular off chance.
- [[07_capstone/notes/mp-90-wandb-gpu-close|MP-90 W&B and GPU-Watch Close]] — the closed-with-one-reason verdicts for W&B and the GPU watch.
- [[07_capstone/notes/mp-94-positive-control-results|MP-94 Positive Control Results]] — P=59, Nanda config, 3 seeds, k_99 = 58/59: NO-GROK.
- [[07_capstone/notes/mp-95-session-0-transition|MP-95 Session 0 Transition]] — pivot from the dense-attractor characterisation to scaled Rung 1.
- [[07_capstone/notes/capstone-gate-honest-negative|Capstone Gate — the honest negative]] — the Phase 7 gate answer: dense mechanism defended with manifests.
- [[07_capstone/checklist|Capstone checklist]] — phase items and the stamped gate.
- [[07_capstone/README|Capstone README]] — full pipeline overview, experiment ladder
- [[07_capstone/writeup]] — mini-paper outline: grokking, circuits, SAE

## Experiment ladder

| Rung | Experiment | Status | Code |
|------|------------|--------|------|
| 1 | Induction heads | ⚠️ Task design fixed, no head detected yet | `src/experiments/exp1_induction_heads.py` |
| 2 | Grokking modular addition ★ | ⏳ CPU-bound, GPU run pending | `src/experiments/exp2_grokking.py` |
| 3 | Superposition geometry | ✅ Phase transition confirmed | `src/experiments/exp3_superposition.py` |
| 4 | Circuit verification (patching) | ⚠️ Fixed, path patching still unvalidated (no real head) | `src/experiments/exp4_circuit_patching.py` |
| 5 | SAE feature dashboard | ⚠️ Synthetic + real-activation upgrade (informative, not conclusive) | `src/experiments/exp5_sae_dashboard.py` |
| 6 | Automated vs hand-found circuit | ❌ Descoped | — |

See [[portfolio/RESULTS]] for exact per-rung numbers and the 2026-08-02 Micro-Phase 8
Honesty Ledger entry — this table is a status summary, not the source of truth.

Rung 6 was removed on 2026-08-01: `exp6_automated_circuit.py` never implemented ACDC —
it drew numbers from `rng.poisson`/`rng.beta`/`rng.exponential` and plotted them as
"Faithfulness" and "Time to Discovery." It was labeled a placeholder in logs, but shipping
fabricated numbers next to real results in a portfolio repo is a liability even when
labeled. Deleted rather than fixed; revisit only with a real ACDC/attribution-patching
implementation, not before.

## Capstone research notes
- [[07_capstone/notes/positive-control-protocol|Positive-Control Protocol]] — reproduce the published setup before deviating from it; the Nanda-faithful P=59 run.
- [[07_capstone/notes/grokking-verdict-p113|Grokking Verdict P=113]] — **under audit** (2026-10-08): the k_99 metric misclassifies noisy sparse embeddings. Do not cite.
- [[07_capstone/notes/dense-solutions-modular-addition|Dense Solutions on Modular Addition]] — the k_99 = 58/59 P=59 positive-control characterisation.
- [[07_capstone/notes/microscope-trial-table|Microscope Trial Table]] — the pre-registered trial schedule for the protocol ablation.
- [[07_capstone/notes/scheduled-negatives-mp28|Scheduled Negatives (MP-28)]] — experiments registered to falsify, not to confirm.

## Source code
Core implementations live in the root `src/` directory, not in `07_capstone/src/`:
- `src/models/decoder_only_transformer.py` — full DecoderOnlyTransformer with RoPE, RMSNorm, hookable cache
- `src/experiments/` — the 5 remaining experiment runners with CLI, training, analysis, and plotting

## Links
- ⬅️ [[00_meta/00_home|Home]]
- 🔬 `src/experiments/` — shared experiment code
- 📚 [[portfolio/RESULTS]] — headline results table
