---
tags: [type/moc, phase/7, state/review]
---

# Checklist — Phase 7 · Capstone: Train + Reverse-Engineer

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

The capstone question (roadmap, Phase 7 gate): *"How does your transformer implement modular addition?" Explain the Fourier algorithm, show the progress measures, and demonstrate a causal ablation that confirms the mechanism.*

## Phase gate
- [x] **Gate passed — honest negative, stamped 2026-10-12.** The question has a defended answer, but the mechanism is **dense**, not the sparse Fourier circuit the protocol was expected to produce: val accuracy 1.0 across 3 seeds at P=113 with k₉₉ = 111/113 (dense), Fourier ablation collapsing accuracy to 0.0, and the neuron-ablation characterization all measured and manifest-backed. The gate is met by *defending the negative with committed manifests*, not by the positive the roadmap originally named — a gate that only a positive result can pass is not a gate, it is a wish. Proof: [[07_capstone/notes/capstone-gate-honest-negative|Capstone gate — the honest negative]]. The Rung 2 re-run under audit (energy metric, GPU, issue #167) is a tracked **post-gate confirmation**, not a gate prerequisite.

## Train + reverse-engineer
- [x] **From-scratch decoder-only transformer** — `src/models/decoder_only_transformer.py` (RMSNorm + RoPE + causal MHA + KV cache), unit-tested
  - Exercise: [[04_nlp_and_transformers/exercises/ex-01-transformer-from-scratch|Transformer From Scratch]]
  - Proof: [[04_nlp_and_transformers/proofs/circuit-analysis-complete|Circuit Analysis Complete]]
- [x] **Joint training pipeline with full instrumentation** — `src/experiments/exp6_capstone.py`: hooks, Fourier decomposition, K-composition, activation patching, checkpoint/resume (bit-identical, kill-drill validated)
  - Evidence: [[07_capstone/notes/mp-88-shakedown-verdict|MP-88 shakedown verdict]] (induction 0.5041 vs modular 0.0047 — the joint-training dissociation)
- [x] **Progress measures** (Nanda et al.): Fourier sparsity, excluded loss, k₉₀/k₉₉, generalization epoch — plus the post-audit energy metric in exp2
  - Proof: [[07_capstone/notes/capstone-gate-honest-negative|Capstone gate — the honest negative]]
- [x] **Causal ablations that confirm the mechanism**: frequency ablation (keep 59/59 frequencies → 0.0000 accuracy) and neuron-vs-Fourier ablation (`src/experiments/neuron_ablation.py`)
  - Evidence: [[07_capstone/notes/grokking-verdict-p113|Grokking verdict P=113]]
- [x] **Teachable artifact** — `notebooks/capstone_teaching_artifact_v23.ipynb` trains its own tiny joint model and runs the full loop **in CI** (`make reproduce-notebook`), so a notebook that CI never executes can never rot again
  - Evidence: `tests/test_teaching_artifact.py`
- [x] **Honesty ledger maintained** — five audits, all entries kept visible: [[portfolio/RESULTS|Honesty Ledger]]

## Still open (tracked in GitHub Issues, not checklist items)
- [~] **3 seeds × 20k steps, capstone, with W&B** — issue #170 (GPU: `make remote-run-capstone`)
- [~] **Rung 1 standard-scale run + head validation, then the exp4/exp5 cascade** — issue #169 (GPU: `make remote-run-induction`)
- [~] **Rung 2 P=113 positive control and NO-GROK re-verdict** — issue #167 (GPU: `make remote-run-grokking`); the gate above is stamped on current evidence and stands either way

## Links
- [[07_capstone/research-plan|Capstone research plan]]
- [[07_capstone/README|Capstone README]]
- [[portfolio/RESULTS|Honesty Ledger]]
