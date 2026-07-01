---
tags: [moc, phase/4]
---

# Phase 4 · NLP & Transformers — MOC (LOAD-BEARING for MI)

Index and links for this phase. Detailed topics/resources/exercises: see [[00_meta/01_roadmap]] (corresponding section).

**This is the most important phase for the MI thesis.** Every concept here directly feeds the capstone. The goal is to learn to *read* transformers: QK/OV circuits, induction heads, logit lens, activation patching.

## Notes (lessons)
*(link to notes in `notes/` as you write them)*

Key topics to cover:
- QK/OV circuit decomposition (Elhage et al. 2021)
- Induction heads (Olsson et al. 2022)
- Residual stream as communication channel
- Logit lens technique
- Activation patching / path patching / attribution patching
- TransformerLens: HookedTransformer, hook points, ActivationCache

## Exercises
*(link to exercises in `exercises/`)*

Core exercises:
- Build decoder-only transformer from scratch
- Identify induction heads via attention patterns
- Perform activation patching to verify circuit components

## Proofs to myself
*(link to proofs in `proofs/`)*

## Phase checklist → [[04_nlp_and_transformers/checklist]]

## Links
- ⬅️ [[03_deep_learning/_MOC|Phase 3 · Deep Learning]]
- ➡️ [[05_llm_engineering/_MOC|Phase 5 · LLM Engineering (Model Instrumentation)]]
- 🔬 [[07_capstone/README|Capstone: Apply all MI skills]]
