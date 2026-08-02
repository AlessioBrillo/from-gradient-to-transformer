---
tags: [moc, phase/7, capstone]
---

# Phase 7 · Capstone — MOC

Index and links for the capstone phase. Detailed plan: [[07_capstone/README]].

## Key documents
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

## Source code
Core implementations live in the root `src/` directory, not in `07_capstone/src/`:
- `src/models/decoder_only_transformer.py` — full DecoderOnlyTransformer with RoPE, RMSNorm, hookable cache
- `src/experiments/` — the 5 remaining experiment runners with CLI, training, analysis, and plotting

## Links
- ⬅️ [[00_meta/00_home|Home]]
- 🔬 `src/experiments/` — shared experiment code
- 📚 [[portfolio/RESULTS]] — headline results table
