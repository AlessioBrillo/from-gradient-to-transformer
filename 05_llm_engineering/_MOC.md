---
tags: [moc, phase/5]
---

# Phase 5 · LLM Engineering — MOC (reframed: Model Instrumentation)

Index and links for this phase. Detailed topics/resources/exercises: see [[00_meta/01_roadmap]] (corresponding section).

**Reframing:** The focus is on the engineering that powers MI research — hooks, activation caching, deterministic inference, synthetic dataset construction for circuit tasks.

## Notes (lessons)
- [[05_llm_engineering/notes/01-transformer-lens-hooks|TransformerLens Hooks and Model Instrumentation]]
- [[05_llm_engineering/notes/02-deterministic-inference|Deterministic Inference for Reproducible Research]]
- [[05_llm_engineering/notes/03-activation-harvesting|Activation Harvesting at Scale]]
- [[05_llm_engineering/notes/04-circuit-datasets|Synthetic Dataset Construction for Circuit Tasks]]

## Exercises
- [[05_llm_engineering/exercises/ex-01-hook-instrumentation|Hook-Based Activation Capture]]
- [[05_llm_engineering/exercises/ex-02-activation-harvesting|Activation Harvesting Across Prompts]]
- [[05_llm_engineering/exercises/ex-03-circuit-dataset|Synthetic Circuit Dataset Construction]]

## Proofs to myself
- [[05_llm_engineering/proofs/hook-intervention|Hook Intervention Changes Model Output]]
- [[05_llm_engineering/proofs/determinism-necessity|Determinism is Necessary for Reproducible Activation Analysis]]
- [[05_llm_engineering/proofs/activation-patching|Activation Patching Localizes Model Behavior]]

## Phase checklist → [[05_llm_engineering/checklist]]

## Links
- ⬅️ [[04_nlp_and_transformers/_MOC|Phase 4 · NLP & Transformers]]
- ➡️ [[06_production_ai/_MOC|Phase 6 · Production AI (Research Infra)]]
- 🔬 [[07_capstone/README|Capstone: Apply instrumentation skills]]
