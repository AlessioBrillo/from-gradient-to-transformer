---
tags: [type/moc, phase/5, state/review]
---

# Checklist — Phase 5 · LLM Engineering (reframed: Model Instrumentation)

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

**Reframing:** Instead of building RAG pipelines and agents, the focus is on the engineering that powers MI research — reliable, reproducible, scalable activation harvesting and model instrumentation.

## Phase gate
- [x] **Proof passed** → I can move to the next phase. Hook-based instrumentation
  (ex-01), deterministic inference (ex-02), activation harvesting (ex-02 proof),
  synthetic circuit dataset construction (ex-03) all have linked proofs in this phase.

## Core MI Engineering
- [x] **TransformerLens hooks deep-dive:** pre/post hooks on any layer, module, attention head
  - Exercise: [[05_llm_engineering/exercises/ex-01-hook-instrumentation|Hook-Based Activation Capture]]
  - Proof: [[05_llm_engineering/proofs/hook-intervention|Hook Intervention Changes Model Output]]
- [x] **Deterministic inference:** seed control, deterministic algorithms, float determinism
  - Exercise: [[05_llm_engineering/exercises/ex-02-activation-harvesting|Activation Harvesting]]
  - Proof: [[05_llm_engineering/proofs/determinism-necessity|Determinism is Necessary]]
- [x] **Activation harvesting:** collecting activations across prompts, storage, memory management
  - Exercise: [[05_llm_engineering/exercises/ex-02-activation-harvesting|Activation Harvesting]]
  - Proof: [[05_llm_engineering/proofs/activation-patching|Activation Patching]]
- [x] **Dataset construction for circuit tasks:** synthetic data (IOI, greater-than, docstring) with controlled templates
  - Exercise: [[05_llm_engineering/exercises/ex-03-circuit-dataset|Circuit Dataset]]
  - Proof: [[05_llm_engineering/proofs/activation-patching|Activation Patching]]
- [x] **nnsight:** (descoped 2026-10-11: no remote execution needed) intervention graphs for remote/large-model execution

## Light Touch (context only)
- [x] RAG end-to-end (descoped 2026-10-11: not MI-focused) (retrieval as context for circuit analysis)
- [x] LoRA/QLoRA fine-tune (descoped 2026-10-11: no pretrained model) (architectural understanding, not focus)
- [x] Evaluation: LLM-as-judge (descoped 2026-10-11: stochastic worse than deterministic), benchmarks
- [x] RLHF/DPO alignment (descoped 2026-10-11: no pretrained policy) (understanding how fine-tuning changes circuits)
