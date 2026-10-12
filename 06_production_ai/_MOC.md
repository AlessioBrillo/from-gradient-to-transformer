---
tags: [type/moc, phase/6, state/review]
---

# Phase 6 · Production AI — MOC (reframed: Reproducible Research Infra)

Index and links for this phase. Detailed topics/resources/exercises: see [[00_meta/01_roadmap]] (corresponding section).

**Reframing:** The infrastructure serves the research goal — making every result auditable, extendable, and trustworthy. One command regenerates all figures. Every experiment is tracked. CI validates reproducibility.

## Notes (lessons)
- [[06_production_ai/notes/multi-seed-experiment-design|Multi-Seed Experiment Design]] — mean ± std over >= 3 seeds, and why a single run is not a result.
- [[06_production_ai/notes/results-manifests-and-provenance|Results Manifests and Provenance]] — the `results/*.json` contract: seeds, args, git SHA, device, wall clock.
- [[06_production_ai/notes/figure-provenance-and-evidence-gates|Figure Provenance and Evidence Gates]] — a figure must be tracked and cited, not merely present on disk.
- [[06_production_ai/notes/checkpoint-resume-durability|Checkpoint Resume Durability]] — the kill-drill requirement: resume must be bit-identical.
- [[06_production_ai/notes/descope-register|Descope Register]] — every Phase 5/6/7 breadth item, with a dated reason for why it is out of scope.
- [[06_production_ai/notes/gpu-colab-execution-protocol|GPU Colab Execution Protocol]] — the P=113 3-seed run that has never executed on GPU.

> **Five capstone-research notes live in [[07_capstone/_MOC|the Phase 7 MOC]], not here.**
> The positive-control protocol, the microscope trial table, the scheduled
> negatives, the dense-solution characterisation and the P=113 grokking verdict
> were authored into this phase but tagged `phase/7` from the start — they are
> capstone research, not production infrastructure. `check_vault.py` now
> requires a note's `phase/N` tag to match the directory it lives in, so on
> 2026-10-11 they moved rather than staying mis-filed. They are listed in
> [[07_capstone/_MOC]].

## Exercises
- [[06_production_ai/exercises/ex-01-falsify-your-own-metric|Falsify Your Own Metric]] — take the metric that made you look good and break it.
- [[06_production_ai/exercises/ex-02-results-manifest|Results Manifest]] — write a manifest by hand, then read it back with `verify-claims`.
- [[06_production_ai/exercises/ex-03-induction-task-design|Induction Task Design]] — the birthday-problem collision that made the original task ill-posed.
- [[06_production_ai/exercises/ex-04-kill-drill|Kill Drill]] — hard-kill a run mid-training and prove resume is exact.
- [[06_production_ai/exercises/ex-05-falsify-the-figure-gate|Falsify the Figure Gate]] — plant a stale figure and watch `verify-claims` catch it.

## Proofs to myself
- [[06_production_ai/proofs/reproducible-from-clean-clone|Reproducible From a Clean Clone]] — fresh clone → `uv sync` → `make reproduce-quick` → `make verify-claims`, GREEN 2026-08-27.
- [[06_production_ai/proofs/kill-drill-checkpoint-resume|Kill-Drill: Checkpoint Resume]] — resume continues bit-for-bit.

## Phase checklist → [[06_production_ai/checklist]]

## Links
- ⬅️ [[05_llm_engineering/_MOC|Phase 5 · LLM Engineering]]
- ➡️ [[07_capstone/README|Phase 7 · Capstone: Train + Reverse-Engineer]]
- 🔬 [[portfolio/README|Portfolio: Ship reproducible research]]
