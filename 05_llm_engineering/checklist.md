---
tags: [checklist, phase/5]
---

# Checklist — Phase 5 · LLM Engineering (reframed: Model Instrumentation)

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

**Reframing:** Instead of building RAG pipelines and agents, the focus is on the engineering that powers MI research — reliable, reproducible, scalable activation harvesting and model instrumentation.

## Phase gate
- [ ] **Proof passed** → I can move to the next phase.

## Core MI Engineering
- [ ] **TransformerLens hooks deep-dive:** pre/post hooks on any layer, module, attention head
- [ ] **Deterministic inference:** seed control, deterministic algorithms, float determinism
- [ ] **Activation harvesting:** collecting activations across prompts, storage, memory management
- [ ] **Dataset construction for circuit tasks:** synthetic data (IOI, greater-than, docstring) with controlled templates
- [ ] **nnsight:** intervention graphs for remote/large-model execution

## Light Touch (context only)
- [ ] RAG end-to-end (retrieval as context for circuit analysis)
- [ ] LoRA/QLoRA fine-tune (architectural understanding, not focus)
- [ ] Evaluation: LLM-as-judge, benchmarks
- [ ] RLHF/DPO alignment (understanding how fine-tuning changes circuits)
