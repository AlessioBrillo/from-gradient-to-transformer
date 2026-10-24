---
tags: [type/moc, phase/7, state/review]
---

# Checklist — Phase 7 · Capstone: Train + Reverse-Engineer

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

The capstone question (roadmap, Phase 7 gate): *"How does your transformer implement modular addition?" Explain the Fourier algorithm, show the progress measures, and demonstrate a causal ablation that confirms the mechanism.*

## Phase gate
- [x] **Gate passed — honest negative stamped 2026-10-12, upgraded to the positive 2026-10-14.** The capstone question ("how does your transformer implement modular addition?") has a defended, manifest-backed answer: the model implements the **sparse Fourier circuit** — val accuracy 0.9999 ± 0.0002 at P=113 with k_energy_90 = 5.7 ± 1.2 of 56 frequencies on the Nanda protocol, 3/3 seeds GPU (the 2026-08-11 NO-GROK was an L1-metric artifact, retracted). The negative answer this gate first carried is preserved in [[07_capstone/notes/capstone-gate-honest-negative|the superseded gate note]] — including the falsifier that fired. The Rung 2 re-run under audit was a **gate confirmation**, and it flipped the answer, not the gate.

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
- [x] **Honesty ledger maintained** — seven audits, all entries kept visible: [[portfolio/RESULTS|Honesty Ledger]]

## Still open (tracked in GitHub Issues, not checklist items)
- [x] **3 seeds × 20k steps, capstone** — issue #170 (GPU: `make remote-run-capstone`); run executed 2026-10-14, dissociation persists at full budget (`results/capstone_20k.json`). W&B never connected (no credentials) — closed-with-reason.
- [x] **Rung 1 standard-scale run + head validation, then the exp4/exp5 cascade** — issue #169 (GPU: `make remote-run-induction`); the detector behind every previous head count was fixed on 2026-10-19 (it measured the previous-token offset; the counts are retracted), the run now uses the corrected detector with early stop, and the cascade analyses **the same checkpoint** at Rungs 4 and 5. Run executed 2026-10-20: a head forms (2–3 per seed, copy-offset mass 0.945) but the probe puts the copy on a **fixed offset**, so it is a *prefix-copying* head. The content-based task that removes the shortcut is pre-registered (ADR-0033) and is the open item of issue #200.
- [x] **Rung 2 P=113 positive control and NO-GROK re-verdict** — issue #167 (GPU: `make remote-run-grokking`); reversed 2026-10-14, sparse circuit reproduced on both protocols. Follow-up closed: the `exp2_*` figures were regenerated from the GPU re-run (2026-10-17) and the P=59 positive control was re-measured with the energy metric (issue #196, 2026-10-19): **2 of 3 seeds sparse — MIXED**, not the SPARSE label a majority rule produces.
- [ ] **Protocol-ablation phase diagram** — issue #168, moved to the v1.1 milestone on 2026-10-19. Ten pre-registered cells (`configs/phase_diagram_ablation.yaml`: the Nanda-faithful baseline plus exactly one deviation per cell, 3 seeds × 20k steps each), whose taxonomy was clarified before the first cell runs: SPARSE = 3/3, MIXED = 1–2/3, DENSE = 0/3, per-seed counts always reported. The runner's default configuration is now that file, so a bare invocation cannot run a different experiment than the one that was pre-registered.
- [ ] **Content-based induction task** — issue #200: the periodic task cannot separate copying by content from copying by a fixed offset, so Rung 1's headline claim is still open. The task (ADR-0033), its thresholds, its budget and its decision rule are pre-registered in [[07_capstone/notes/variable-distance-induction-preregistration]]; the GPU notebook is `notebooks/kaggle_induction_content.ipynb` (`make remote-run-induction-content`). **Instrument ready (2026-10-22):** the verdict is a tested module (`src/experiments/content_verdict.py`) that joins the two manifests instead of dying on a `KeyError`, the circuit-level measurement (`src/experiments/copy_circuit.py`) is in place for the distributed case, the cascade's counterfactual is a minimal pair, and the protocol is amended before the run (vocabulary 256, `--stop-rule any`). **The GPU run is the open item.**

## Links
- [[07_capstone/research-plan|Capstone research plan]]
- [[07_capstone/README|Capstone README]]
- [[portfolio/RESULTS|Honesty Ledger]]
