---
adr: 0024
title: Continuum Ledger — Twentieth Execution (MP-71/MP-74)
date: 2026-08-23
status: OPEN
phase: 7
tags: [type/ledger, phase/7, research/experiment]
consumes: [ADR-0023]
---

**Written from MP-70's release report at Session 0 of MP-74.**
**Terminus**: Release = merge + 14 calendar days (2026-09-06).
**Consumes**: ADR-0023 row 3 verdict (post-record arc or R1–R8 adjudication).

---

## Ledger Rows (Eight, Pre-Stamped with Windows and Kill-Dates)

| Row | Candidate | Opens Only If | Window | Kill-Date | Status |
|-----|-----------|---------------|--------|-----------|--------|
| 1 | **GPU Grokking 3-Seed P=113** | Always (primary flagship) | Session 1–3 | 2026-08-28 | PENDING |
| 2 | **Extended Induction 10k Epochs ×3 Seeds** | Rung 1 standard run < 0.3 diag+1 at 3k epochs (confirmed 2026-08-14) | Session 2–3 | 2026-08-30 | PENDING |
| 3 | **Neuron Ablation on Dense Grokking** | GPU run completes (uses existing checkpoints) | Session 2–3 | 2026-08-30 | PENDING |
| 4 | **Clean-Clone Reproducibility Proof** | Always (Phase 6 gate) | Session 4 | 2026-08-27 | PENDING |
| 5 | **SAE on Confirmed-Head Checkpoint** | Rung 1 produces confirmed induction head (R2 verdict at Session 3) | Session 5–6 | 2026-09-01 | GATED |
| 6 | **Teaching Artifact v20** | Always (showcase lane) | Session 6 | 2026-09-01 | PENDING |
| 7 | **Paper v20 / Annex v20** | New numbers from R1, R2, R3, or R5 | Session 4–5 | 2026-09-02 | GATED |
| 8 | **Gate-Debt Re-verification** | All MP-30–MP-36 rows | Session 1, 7 | 2026-09-03 | PENDING |

---

## Universal Override

If GPU run (Row 1) produces **sparse Fourier** (k₉₉ < P/2 sustained ≥3 checkpoints):
- Row 1 becomes the sparse-regime mechanism study (Nanda-style per-frequency reading)
- Rows 2/5 reprioritized to characterize the difference between this run and the NO-GROK runs
- Kill-dates adjusted in the same sitting

## Post-Record Override

If MP-70's Session 0 continued the post-record arc:
- Row 1 becomes "Post-Record Harness Design from Dated Negatives"
- Row 2 becomes "Eighth Post-Record Question"
- Row 3 becomes "Ninth Post-Record Question"
- etc.
- But MP-70 has not yet consumed MP-69's decision; this ledger assumes the pre-record arc.

---

## Row 1: GPU Grokking 3-Seed P=113

**Protocol**: Execute `notebooks/colab_grokking_full_run.ipynb` on Colab A100/T4, 3 seeds × 5000 epochs, checkpoint every 500 epochs, manifest to Drive.

**Success Criteria**:
- All 3 seeds complete 5000 epochs without OOM
- Checkpoints saved every 500 epochs to Drive
- `results/exp2_grokking.json` manifest produced with per-seed generalization epoch and Fourier sparsity
- Figures: `exp2_grokking_curve.png`, `exp2_fourier_weights.png`, `exp2_frequency_ablation.png`, `exp2_progress_measures.png`

**Falsifier**: Colab OOM at batch_size=512 → reduce to 256, log change, re-run. If all 3 seeds fail → document failure, close Row 1 with reason, proceed to Row 3.

**Heartbeat**: Colab runtime status checked every session; first checkpoint download at Session 2.

---

## Row 2: Extended Induction 10k Epochs ×3 Seeds

**Protocol**: `uv run python -m src.experiments.exp1_induction_heads --standard --epochs 10000 --checkpoint-every 500 --save-model --seeds 0,1,2`

**Success Criteria**:
- 3 seeds × 10000 epochs complete with checkpointing every 500 epochs
- Step 1 (L0 duplicate mass) and Step 2 (K-composition) tracked independently at each checkpoint
- `results/exp1_induction_heads.json` manifest updated with final metrics
- Figures: `exp1_induction_pattern.png`, `exp1_training_bump.png`, `exp1_step1_step2_trajectory.png`

**Falsifier**: If at 10k epochs still 0 heads → hypothesis "fresh-batches at standard scale produces heads" falsified. Document boundary in ADR-0024 row 2.

**Heartbeat**: Checkpoint monitor at Session 3 (2k/4k/6k/8k/10k epochs).

---

## Row 3: Neuron Ablation on Dense Grokking

**Protocol**: On existing P=113 checkpoints (seed 0,1,2), ablate MLP neurons by activation magnitude; compare degradation to Fourier ablation.

**Success Criteria**:
- Scripted sweep produces `figures/exp2_neuron_ablation.png`
- Manifest entry appended to `exp2_grokking.json`
- Comparison: neuron ablation curve vs. Fourier ablation curve

**Interpretation**:
- If neuron ablation shows graceful degradation (no single neuron critical) while Fourier ablation shows catastrophic collapse → dense solution is distributed linear map, not sparse DFT
- If neuron ablation also shows catastrophic collapse at specific neurons → dense solution may have sparse structure after all

**Heartbeat**: Runs in parallel with Row 1 GPU monitor at Session 2.

---

## Row 4: Clean-Clone Reproducibility Proof

**Protocol**: Fresh clone → `uv sync` → `make reproduce-quick` → `make verify-claims`

**Success Criteria**:
- Full transcript recorded in `06_production_ai/proofs/reproducible-from-clean-clone.md` with timestamps
- All 5 rungs pass in `--quick` mode
- `make verify-claims` exits 0

**Falsifier**: If fails → fix blocking issue, re-run. Transcript required for release.

**Heartbeat**: Session 4 execution; re-verified Session 7.

---

## Row 5: SAE on Confirmed-Head Checkpoint (GATED)

**Protocol**: `uv run python -m src.experiments.exp5_sae_dashboard --activations-from <head_checkpoint> --hooks ln_final --dict-size 256 --epochs 300 --seeds 0,1,2`

**Opens Only If**: Row 2 produces confirmed induction head at Session 3.

**Success Criteria**:
- SAE trained on real head checkpoint activations
- L0/FVE tradeoff curve compared to synthetic baseline
- Expect sparsity to improve (L0 ~ 20-30) if features are real

**If Not Opened**: SAE stays on synthetic only; document dependency honestly.

---

## Row 6: Teaching Artifact v20

**Protocol**: Build runnable Colab notebook: "From Dense Grokking to Sparse Circuits"

**Contents**:
- Cell 1: Train P=113 (or load checkpoint from GPU run)
- Cell 2: Fourier analysis — show dense/sparse spectrum per actual verdict
- Cell 3: Ablation sweep — show graceful/catastrophic degradation per actual verdict
- Cell 4: Neuron ablation — show distributed representation
- Cell 5: Compare to Nanda et al. sparse circuit (expected vs. got)
- Cell 6: Honest conclusion

**Success Criteria**:
- Stranger runs on fresh Colab session → saves output → transcript committed
- Ex-F distillation complete (four-register verdict)

---

## Row 7: Paper v20 / Annex v20

**Protocol**: If Rows 1/2/3/5 produce new numbers → paper v20 diff + annex v20 scaffold; else "v19 is the record" dated memo.

**Success Criteria**:
- `make paper` re-verified in CI mirror
- `portfolio/essay-annex-20.md` on live shelf, manifest-tagged, amended never rewritten

---

## Row 8: Gate-Debt Re-verification

**Protocol**: Re-verify all MP-30–MP-36 row closures with transcripts; `gate-debt.md` complete or absent-with-date.

**Success Criteria**:
- Each cell: LAUNCHED-with-transcript or CLOSED-with-one-reason
- A claimed closure without its transcript stays open and blocks Session 8
- `gate-debt.md` file present or absent-with-date

**Heartbeat**: Session 1 (initial), re-verified Session 7.

---

## Deviations from MP-70's Release Report

None at Session 0. Any deviations recorded here as dated ledger notes.

---

## Sign-Off

**Session 0 (2026-08-23)**: Intake table committed; thirtieth-generation arc stamped; Row 1 (GPU Grokking 3-Seed P=113) chosen as research row; Rows 2–8 stamped PENDING/GATED; ADR-0024 promoted from MP-71's roadmap. Deviations from MP-70's release report: none at Session 0.

**Ex-T Execution Memo (2026-08-23, Session 0)**: MP-70's Session-0 decision consumed with dates as MP-74 intake. Pre-record arc governs (MP-69 did not continue post-record arc). MP-70's Session-0 adjudication: R1–R8 frozen, Row 1 (GPU Grokking) opened as research row, Rows 2–8 closed with dated reasons or marked GATED. Criteria cited: ADR-0023 at zero UNDECIDED, `verify-claims` at 0, 18th teaching transcript on live shelf, `dev == main`. The thirtieth-generation consumption chain: MP-40's Ex-N → MP-41 → ... → MP-69 → MP-70 → MP-74. A sitting stamps, it never re-decides.

**Session 8**: ADR-0024 at zero UNDECIDED rows; merge green; `dev == main`; home wired; roadmap archived with deviations as dated ledger notes.