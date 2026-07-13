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
| 1 | Induction heads | ✅ Complete | `src/experiments/exp1_induction_heads.py` |
| 2 | Grokking modular addition ★ | ⏳ CPU-bound | `src/experiments/exp2_grokking.py` |
| 3 | Superposition geometry | ✅ Complete | `src/experiments/exp3_superposition.py` |
| 4 | Circuit verification (patching) | ✅ Complete | `src/experiments/exp4_circuit_patching.py` |
| 5 | SAE feature dashboard | ✅ Synthetic | `src/experiments/exp5_sae_dashboard.py` |
| 6 | Automated vs hand-found circuit | 🛠 Placeholder | `src/experiments/exp6_automated_circuit.py` |

## Source code
Core implementations live in the root `src/` directory, not in `07_capstone/src/`:
- `src/models/decoder_only_transformer.py` — full DecoderOnlyTransformer with RoPE, RMSNorm, hookable cache
- `src/experiments/` — all 6 experiment runners with CLI, training, analysis, and plotting

## Links
- ⬅️ [[00_meta/00_home|Home]]
- 🔬 `src/experiments/` — shared experiment code
- 📚 [[portfolio/RESULTS]] — headline results table
