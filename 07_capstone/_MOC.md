---
tags: [type/moc, phase/7, capstone, state/review]
---

# Phase 7 · Capstone — MOC

Index and links for the capstone phase. Detailed plan: [[07_capstone/README]].

## Key documents
- [[archive/process/README|Archived process history]] — the dated session notes of the micro-phase process (shakedown, retune, positive-control runs). Frozen and not current: the status below and in [[portfolio/RESULTS]] supersedes them.
- [[07_capstone/notes/capstone-gate-honest-negative|Capstone Gate — the honest negative]] — the Phase 7 gate answer: dense mechanism defended with manifests.
- [[07_capstone/checklist|Capstone checklist]] — phase items and the stamped gate.
- [[07_capstone/design|Capstone design]] — the joint-training pipeline: model, tasks, instrumentation, analysis chain, honest limits.
- [[07_capstone/README|Capstone README]] — full pipeline overview, experiment ladder
- [[07_capstone/writeup]] — mini-paper outline: grokking, circuits, SAE

## Experiment ladder

| Rung | Experiment | Status | Code |
|------|------------|--------|------|
| 1 | Induction heads | ⚠️ A prefix-copying head forms at standard scale; on the **content-based** task (issue #200, run 2026-11-09) the copy is content-based on 3/3 seeds, but the pre-registered per-head rule confirms no head on any seed (re-measured 2026-11-17 after the seeding fix) → both verdicts NEGATIVE | `src/experiments/exp1_induction_heads.py` |
| 2 | Grokking modular addition ★ | ✅ REPRODUCED 2026-10-14 (sparse circuit, energy metric) | `src/experiments/exp2_grokking.py` |
| 3 | Superposition geometry | ✅ Phase transition confirmed | `src/experiments/exp3_superposition.py` |
| 4 | Circuit verification (patching) | ✅ The cascade ran end to end on Rung 1's own checkpoint (ablation 0.5895, path patching 0.7052) — on a prefix-copying head | `src/experiments/exp4_circuit_patching.py` |
| 5 | SAE feature dashboard | ⚠️ Real activations sparse (L0 3.7%) but the dictionary is ~8× too wide, 66% dead | `src/experiments/exp5_sae_dashboard.py` |
| 6 | Automated vs hand-found circuit | ❌ Descoped | — |
| 7 | The instruments on GPT-2 small | ⚠️ Pre-registered (ADR-0034): parity, induction-head ranking and the indirect-object task pass; the ablation stages do not reproduce under zero or mean ablation (ADR-0035), while one-hop path patching ranks the name movers first to third | `src/experiments/exp7_gpt2_small.py` |

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
- [[07_capstone/notes/grokking-verdict-p113|Grokking Verdict P=113]] — REPRODUCED 2026-10-14; the 2026-08-11 NO-GROK was an L1-mass metric artifact, retracted.
- [[07_capstone/notes/dense-solutions-modular-addition|Dense Solutions on Modular Addition]] — the P=59 positive-control characterisation (k_99 = 58/59 under the retracted L1-mass metric; re-measured with the energy metric on 2026-10-19: 2 of 3 seeds sparse, MIXED).
- [[07_capstone/notes/microscope-trial-table|Microscope Trial Table]] — the pre-registered trial schedule for the protocol ablation.
- [[07_capstone/notes/scheduled-negatives-mp28|Scheduled Negatives (MP-28)]] — experiments registered to falsify, not to confirm.
- [[07_capstone/notes/variable-distance-induction-preregistration|Variable-Distance Induction Task — Pre-Registration]] — the frozen task, thresholds, budget and decision rule for issue #200.

## Source code
Core implementations live in the root `src/` directory, not in `07_capstone/src/`:
- `src/models/decoder_only_transformer.py` — full DecoderOnlyTransformer with RoPE, RMSNorm, hookable cache
- `src/experiments/` — the 5 remaining experiment runners with CLI, training, analysis, and plotting

## Links
- ⬅️ [[00_meta/00_home|Home]]
- 🔬 `src/experiments/` — shared experiment code
- 📚 [[portfolio/RESULTS]] — headline results table
