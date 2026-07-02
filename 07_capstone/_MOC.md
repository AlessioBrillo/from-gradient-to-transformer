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
| 1 | Induction heads | [ ] Planned | `src/experiments/exp1_induction_heads.py` |
| 2 | Grokking modular addition ★ | [ ] Planned | `src/experiments/exp2_grokking.py` |
| 3 | Superposition geometry | [ ] Planned | `src/experiments/exp3_superposition.py` |
| 4 | Circuit verification (patching) | [ ] Planned | `src/experiments/exp4_circuit_patching.py` |
| 5 | SAE feature dashboard | [ ] Planned | `src/experiments/exp5_sae_dashboard.py` |
| 6 | Automated vs hand-found circuit | [ ] Stretch | `src/experiments/exp6_automated_circuit.py` |

## Source code (capstone)
- [[07_capstone/src/model]] — decoder-only Transformer
- [[07_capstone/src/train]] — training loop with W&B
- [[07_capstone/src/config]] — hyperparameter configurations
- [[07_capstone/src/analysis]] — Fourier decomposition, progress measures
- [[07_capstone/src/sae]] — SAE training wrapper

## Links
- ⬅️ [[00_meta/00_home|Home]]
- 🔬 `src/experiments/` — shared experiment code
- 📚 [[portfolio/RESULTS]] — headline results table
