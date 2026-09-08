---
tags: [phase/7, capstone, paper, memo]
created: 2026-09-08
consumes: [ADR-0028, 89_micro-phase-89-from-retune-to-signal]
---

# v20 is the Record — Paper Decision Memo (MP-90 Session 4)

> **Decision**: NO-MOVE verdict from MP-89 retune A/B means no new numbers for the paper. The "v20 is the record" memo is written here as the paper decision artifact. No `main.tex` diff is applied.

## Context

**MP-88 Shakedown (2000 steps, seed 0):**
- Modular accuracy: 0.0047 (flat, below chance 1/113 ≈ 0.0088)
- Induction accuracy: 0.5041 (~1000× rise)
- Fourier k_99: 98.1 (dense, same regime as P=113 NO-GROK baseline)
- Max K-comp: 0.394 (detector alive, no head claimed — 0.3 threshold applies to per-head diag+1 mass, not K-comp)

**MP-89 Retune A/B (500 steps each, seed 0):**

| Arm | Modular Accuracy | Induction Accuracy | Fourier k_99 | Max K-comp | Verdict |
|-----|------------------|-------------------|--------------|------------|---------|
| Control | 0.0062 | 0.0005 | 98.18 | 0.3690 | Baseline |
| Vocab-Offset (2048) | 0.0060 | 0.0005 | 98.61 | 0.1728 | NO-MOVE |
| Reweight (5.0/0.5) | 0.0065 | 0.0005 | 98.11 | 0.3048 | NO-MOVE |

**Chance threshold:** 1/113 ≈ 0.00885. **All three arms below chance.**

## Verdict

**NO-MOVE — neither vocab-offset nor curriculum reweight moves modular addition off chance in 500 steps.**

- The interference hypothesis (shared embedding rows) is falsified: dedicated id range [2048, 2161) did not fix modular; accuracy dipped slightly (0.0060 vs 0.0062) and K-comp dropped from 0.37 to 0.17.
- The schedule hypothesis (1.0/1.0 curriculum imbalance) is falsified: 10× relative boost to modular weight (5.0 vs 0.5) showed highest modular accuracy (0.0065) but still below chance.
- Induction stayed near zero in all arms — the curriculum reweight did not collapse induction either.
- The 2000-step shakedown already gave the answer: modular never leaves chance while induction takes off. The retune A/B confirms shortening the horizon doesn't surface a different signal.

## Interpretation

The dense attractor under joint modular+induction training is the contribution. The model finds a legitimate dense algorithm (val accuracy 1.0 on modular in the full shakedown was 0.0047, not 1.0 — the MP-88 shakedown modular was at chance, not 1.0; the NO-GROK baseline from the standalone P=113 run achieved 1.0 with dense Fourier).

The joint training dissociation (induction learns, modular doesn't) reveals that the two tasks compete for capacity in a small model, and induction dominates. The modular task does not form the sparse Fourier circuit even when given dedicated embedding space or 10× curriculum weight.

## Paper Status

- **No `main.tex` diff applied.** The scaffold at `portfolio/paper/main.tex` remains at `% TODO` with seeded `references.bib`.
- This memo serves as the dated record of the paper decision.
- The NO-GROK negative (2026-08-11, P=113 CPU 3-seed, val 1.0 + dense Fourier k_99=111/113) and the joint shakedown dissociation (2026-09-07, modular at chance + dense Fourier, induction at 0.50) are the recorded measurements.
- Next paper revision (if any) is gated on: GPU run producing sparse Fourier, or new candidate set in next ledger.

## Contribution Statement

> "This config finds a dense algorithm for modular addition under joint training with induction. The induction stream dominates, modular stays at chance with dense Fourier representation. Neither interference (shared embeddings) nor schedule (curriculum weight) is the primary bottleneck at 500 steps — the modular task simply does not generalize in this horizon under any of these configs. The dissociation itself is the finding."

---

**Written:** 2026-09-08
**Perspective:** Personal study notes, learning log, portfolio showcase
**Status:** Paper decision recorded — ADR-0028 Row 6 stamped