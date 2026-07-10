---
tags: [moc, phase/4]
---

# Phase 4 · NLP & Transformers — MOC (LOAD-BEARING for MI)

Index and links for this phase. Detailed topics/resources/exercises: see [[00_meta/01_roadmap]] (corresponding section).

**This is the most important phase for the MI thesis.** Every concept here directly feeds the capstone. The goal is to learn to *read* transformers: QK/OV circuits, induction heads, logit lens, activation patching.

## Notes (lessons)
- [[04_nlp_and_transformers/notes/qk-ov-circuits|QK/OV Circuit Decomposition — The Central Abstraction]]
- [[04_nlp_and_transformers/notes/induction-heads|Induction Heads — The Mechanism of In-Context Learning]]
- [[04_nlp_and_transformers/notes/activation-patching|Activation Patching — Causal Intervention for Circuit Discovery]]
- [[04_nlp_and_transformers/notes/bpe-tokenizer|BPE Tokenizer — From Scratch]]
- [[04_nlp_and_transformers/notes/scaling-laws|Scaling Laws — Kaplan & Chinchilla]]
- [[04_nlp_and_transformers/notes/path-patching|Path Patching — Tracing Causal Edges]]
- [[04_nlp_and_transformers/notes/mi-tooling|MI Tooling — TransformerLens, SAELens, nnsight, CircuitsVis]]

## Exercises
- [[04_nlp_and_transformers/exercises/ex-01-transformer-from-scratch|Build a Decoder-Only Transformer from Scratch]]
- [[04_nlp_and_transformers/exercises/ex-02-induction-head-detection|Identify Induction Heads via Attention Patterns]]
- [[04_nlp_and_transformers/exercises/ex-03-activation-patching|Activation Patching to Verify Circuit Components]]

## Proofs to myself
- [[04_nlp_and_transformers/proofs/qk-ov-decomposition|QK/OV Circuit Decomposition]]
- [[04_nlp_and_transformers/proofs/residual-stream-communication-channel|Residual Stream as Communication Channel]]
- [[04_nlp_and_transformers/proofs/logit-lens|Logit Lens — Reading the Residual Stream]]
- [[04_nlp_and_transformers/proofs/circuit-analysis-complete|Gate Proof: Complete Circuit Analysis Pipeline]]

## Phase checklist → [[04_nlp_and_transformers/checklist]]

## Links
- ⬅️ [[03_deep_learning/_MOC|Phase 3 · Deep Learning]]
- ➡️ [[05_llm_engineering/_MOC|Phase 5 · LLM Engineering (Model Instrumentation)]]
- 🔬 [[07_capstone/README|Capstone: Apply all MI skills]]
