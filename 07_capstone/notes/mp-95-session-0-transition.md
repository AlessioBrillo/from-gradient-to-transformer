---
tags: [type/lesson, phase/7, state/transition]
created: 2026-10-09
---

# Micro-Phase 95: Session 0 — Transition from 94

## Context
Micro-Phase 94 concluded with a comprehensive phase diagram characterizing the "dense attractor" regime in Grokking.

## Transition
We move from a systematic exploration of the dense attractor regime (MP-94) to a targeted scaling effort in Rung 1 (Induction Heads in a 4L/256 model) (MP-95).

## Baseline Verification
- [x] Integrity (`uv run python -m src.results verify`): PASSED.
- [x] Unit Tests (Core/Logic): PASSED.
- [x] Environment (`uv`): OK.

## Action Plan
MP-95 focuses on:
1. Identifying induction heads via QK/OV circuits in a 4L/256 model.
2. Causal verification via activation patching.

Ready for Session 1: Scaled Rung 1 Experiment.

## See also
- [[07_capstone/notes/mp-94-positive-control-results|MP-94 Positive Control Results]] — the result that closed MP-94 and opened this transition.
- [[07_capstone/notes/mp-89-retune-verdict|MP-89 Retune Verdict]] — the NO-MOVE A/B verdict that re-prioritised Rung 1.
- [[04_nlp_and_transformers/notes/induction-heads|Induction Heads]] — the Rung 1 target this phase scales up.
- [[07_capstone/notes/positive-control-protocol|Positive-Control Protocol]] — the protocol-ablation still gated on the Rung 2 rerun.
