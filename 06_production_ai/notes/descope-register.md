---
title: "Descope Register — Phase 5/6/7 Breadth Items"
tags: [type/lesson, phase/6, state/consolidated, research/experiment]
created: 2026-10-11
consumes: [ADR-0031]
---

## Descope Register — Phase 5/6/7 Breadth Items

## What this is

ADR-0031 froze the micro-phase ledgers on 2026-10-08 and routed remaining work
to GitHub issues under the `v1.0` milestone. Issue #172 asks for the Phase 5/6/7
breadth items to be **marked descoped with a dated reason** rather than left as
`[ ]` checkboxes that have been open for months.

This note is that register. An open checkbox that nobody intends to tick is not
a plan; it is noise that makes the remaining `[ ]` items harder to read. A
descoped item with a dated reason is information.

## Register

| Item | Was on | Verdict | Dated reason |
|---|---|---|---|
| **nnsight** (intervention graphs, remote execution) | Phase 5 checklist | **Descoped 2026-10-11** | The repo's intervention needs are met by the hand-rolled hooks in `src/models/decoder_only_transformer.py` and the patchers in `exp4_circuit_patching.py`. nnsight's value is *remote* execution on models too large to load locally; every model here is < 5M parameters and runs on CPU. Adding a dependency to reach a capability the architecture does not need is the mistake `pyproject.toml` already documents on 2026-08-01. |
| **RAG** (retrieval-augmented generation) | Phase 5 breadth | **Descoped 2026-10-11** | Phase 5 was reframed from "LLM engineering" to "model instrumentation" because that is what the MI thesis needs. RAG is a systems topic orthogonal to reverse-engineering a transformer's internals; it would add a retrieval dependency and a corpus, neither of which any rung reads. |
| **LoRA / QLoRA fine-tuning** | Phase 5 breadth | **Descoped 2026-10-11** | Fine-tuning adapts a *pretrained* model. This repo trains from scratch and studies the resulting circuit; there is no pretrained model to adapt and no headroom to preserve. Note this is a *scope* descope, not a judgement that LoRA is unimportant. |
| **LLM-as-judge / eval harness** | Phase 5 breadth | **Descoped 2026-10-11** | Every task here has an exact, programmatic answer (`a + b mod P`, next-token in a repeated sequence). An LLM judge replaces a deterministic checker with a stochastic one — strictly worse, and against the reproducibility discipline in `06_production_ai/notes/figure-provenance-and-evidence-gates`. |
| **RLHF / DPO** | Phase 5 breadth | **Descoped 2026-10-11** | Same reasoning as LoRA: preference-tuning presupposes a pretrained policy. |
| **DVC / lakeFS (data versioning)** | Phase 6 breadth | **Descoped 2026-10-11** | All data here is synthetic and generated from a seed (`src/data/datasets.py`, and every experiment's `make_*_data`). There is no external dataset to version. The provenance problem is *code + config + seed*, which `src/results.py` manifests already solve; duplicating that in a data-VCS would create two sources of truth for the same fact. |
| **Docker / containerised deploys** | Phase 6 breadth | **Descoped 2026-10-11** | `uv.lock` plus `make ci-check` already pins the environment; the clean-clone proof (`06_production_ai/proofs/reproducible-from-clean-clone`) demonstrates it. A container would be a second, slower-to-update definition of the same environment. |
| **HF Spaces SAE dashboard** | Phase 6 checklist, Rung 5 | **Descoped 2026-10-11** — *conditional* | Blocked on a confirmed induction head, which does not exist (0/8; see `04_nlp_and_transformers/notes/induction-extended-run`). An interactive feature browser over 53%-dense features would be a demo of the SAE *not working*. Revisit if and only if a checkpoint with a confirmed head lands. |
| **W&B experiment tracking** | Phase 6 checklist | **CLOSED-WITH-ONE-REASON 2026-09-08** | Credentials never configured; the manifests on disk carry the same per-seed and aggregate numbers W&B would. Recorded in `checklists/gate-debt.md` and `07_capstone/notes/mp-90-wandb-gpu-close`. |
| **Compiled paper PDF** | Phase 6 checklist | **In progress — not descoped** | `.github/workflows/paper.yml` compiles `main.tex` on push; the prosa itself is issue #171. The PDF is a build product, not a capability. |
| **Rung 6 / ACDC** | Phase 7 ladder | **Descoped 2026-08-01** | `exp6_automated_circuit.py` simulated results with random draws. Deleted rather than kept as scaffolding. Revisit only with a real ACDC implementation. |
| **FlashAttention** | Phase 4 breadth | **Descoped 2026-10-11** | A memory-bandwidth optimisation for long sequences. The longest sequence here is 128 positions on a < 5M-parameter model, where it would be pure overhead. |
| **BERT / encoder-only** | Phase 4 breadth | **Descoped 2026-10-11** | Now documented rather than absent: see `04_nlp_and_transformers/notes/encoder-only-bert` for why the MI thesis rules it out. |

## What stays open

Deliberately **not** descoped, because they are the actual research:

| Item | Issue |
|---|---|
| Rung 2 P=113 positive control and NO-GROK recheck (GPU) | #167 |
| Phase diagram rebuilt as a protocol ablation | #168 |
| Rung 1/4/5 standard-scale induction run and head validation (GPU) | #169 |
| Capstone 3 seeds × 20k steps with W&B | #170 |
| Paper prose from committed manifests | #171 |
| **This register** | #172 |

## How to use this note

When a Phase 5/6/7 checklist item is `[ ]`, it should either be in this table
with a dated reason, or be traceable to an open issue. If it is neither, the
checklist is lying — which is the specific failure `check_vault.py` and
`make verify-claims` now guard against elsewhere.

## Links

- [[06_production_ai/_MOC]] — Phase 6 index
- [[07_capstone/_MOC]] — Phase 7 index and the ladder this register refers to
- [[06_production_ai/notes/figure-provenance-and-evidence-gates]] — the discipline that motivates the descopes
- [[portfolio/RESULTS]] — the Honesty Ledger, where the ACDC descope is recorded
- [[04_nlp_and_transformers/notes/encoder-only-bert]] — one descope expanded into a note

## Open questions

- #question Should the interactive SAE browser be built on *synthetic* activations anyway, as a teaching artifact, even though the real-activation result is not publishable?
