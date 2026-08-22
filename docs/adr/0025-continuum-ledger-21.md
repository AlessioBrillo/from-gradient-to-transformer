---
adr: 0025
title: GPU Unblock and Cascade Execution — Micro-Phase 72 (Twenty-First Continuum Ledger)
date: 2026-08-22
status: OPEN
tags: [phase/7, research/experiment, plan]
---

## ADR-0025: GPU Unblock and Cascade Execution — Micro-Phase 72 (Twenty-First Continuum Ledger)

## Context

Micro-Phase 29 (the positive-negative harness) remains mid-execution. The P=113 grokking flagship
(Rung 2) has never run on GPU — this environment is CPU-only. The cascade (Rung 1 → 4 → 5)
requires a Rung 1 checkpoint with a confirmed induction head, which the 3000-epoch fresh-batches
run did not produce (peak diag+1 mass 0.075 vs 0.3 threshold). Phase 6's clean-clone
reproducibility proof is not yet green.

Three hard blockers gate everything downstream:
1. **GPU access** for the P=113 3-seed grokking run
2. **Induction heads at scale** — extended run to 10k epochs or wider model
3. **Clean-clone proof** — `uv sync && make reproduce` from fresh clone

This phase's Session 0 consumed MP-71's Session-0 decision with dates (thirtieth-generation consumption). The post-record arc did not continue; the pre-record arc governs. The candidate set R1–R8 is frozen per the MP-71 roadmap.

## Decision

Execute Micro-Phase 72 as a twenty-first execution of the continuum law with the following eight rows, each with explicit windows, kill-dates, and opening conditions.

## Rows

### Row 1 — GPU Grokking 3-Seed P=113 (Primary Flagship)
- **Protocol**: `notebooks/colab_grokking_full_run.ipynb` on Colab A100/T4
- **Config**: P=113, d_model=128, d_mlp=512, n_heads=4, wd=1.0, train=30%, epochs=5000, 3 seeds (0,1,2), checkpoint every 500 epochs
- **Opens**: Always (primary flagship)
- **Kill date**: Session 1 + 3 calendar days
- **Success**: Manifest `results/exp2_grokking.json` with per-seed generalization epoch, k_90, k_99, final val acc
- **Falsifier**: If Colab OOMs at batch_size=512 → reduce to 256, log change, re-run

### Row 2 — Extended Induction Heads 10k Epochs ×3 Seeds
- **Protocol**: `uv run python -m src.experiments.exp1_induction_heads --standard --epochs 10000 --checkpoint-every 500 --save-model --seeds 0,1,2`
- **Config**: vocab=2048, seq=64, d_model=64, 2 layers, 4 heads, fresh-batches, lr=1e-3, wd=0.1
- **Opens**: Rung 1 standard run < 0.3 diag+1 at 3k epochs (confirmed 2026-08-14)
- **Kill date**: Session 2 + 5 calendar days
- **Measure every 500 epochs**: Step 1 (L0 duplicate mass), Step 2 (K-composition), val acc, diag+1 mass
- **Falsifier**: If 10k epochs still 0 heads → hypothesis "fresh-batches at standard scale produces heads" falsified; document boundary

### Row 3 — Neuron Ablation on Dense Grokking
- **Protocol**: On existing P=113 checkpoints (seed 0,1,2), ablate MLP neurons by activation magnitude; compare degradation to Fourier ablation
- **Opens**: GPU run completes (uses existing checkpoints)
- **Kill date**: Session 2 + 3 calendar days
- **Output**: `figures/exp2_neuron_ablation.png`, manifest entry in `exp2_grokking.json`

### Row 4 — Clean-Clone Reproducibility Proof
- **Protocol**: Fresh clone → `uv sync` → `make reproduce-quick` → `make verify-claims`
- **Opens**: Always (Phase 6 gate)
- **Kill date**: Session 4
- **Output**: Transcript in `06_production_ai/proofs/reproducible-from-clean-clone.md` with timestamps

### Row 5 — SAE on Confirmed-Head Checkpoint
- **Protocol**: `uv run python -m src.experiments.exp5_sae_dashboard --activations-from <head_checkpoint> --hooks ln_final --dict-size 256 --epochs 300 --seeds 0,1,2`
- **Opens**: Rung 1 produces confirmed induction head (Row 2 verdict at Session 3)
- **Kill date**: Session 5 + 3 calendar days
- **Compare**: L0/FVE tradeoff vs. synthetic baseline (expect sparsity improvement if features real)

### Row 6 — Teaching Artifact v19: "From Dense Grokking to Sparse Circuits"
- **Protocol**: Runnable Colab notebook with cells: train/load P=113, Fourier analysis, ablation sweep, neuron ablation, comparison to Nanda et al., honest conclusion
- **Opens**: Always (showcase lane)
- **Kill date**: Session 6
- **Transcript**: Stranger runs on fresh Colab → saves output → transcript committed

### Row 7 — Paper v19 / Annex v19
- **Protocol**: If Rows 1/2/3/5 produce new numbers → paper v19 diff + annex v19; else "v18 is the record" dated memo
- **Opens**: New numbers from Row 1, 2, 3, or 5
- **Kill date**: Session 7

### Row 8 — Gate-Debt Re-verification
- **Protocol**: Re-verify all MP-30 through MP-36 row closures with transcripts; `gate-debt.md` complete or absent-with-date
- **Opens**: All MP-30–MP-36 rows
- **Kill date**: Session 1 (initial), re-verified Session 7

## Universal Override

If GPU run (Row 1) produces **sparse Fourier** (k₉₉ < P/2 sustained ≥3 checkpoints) → Row 1 becomes the sparse-regime mechanism study (Nanda-style per-frequency reading), Rows 2/5 reprioritized to characterize the difference between this run and the NO-GROK runs.

## Post-Record Override

If MP-71's Session 0 continued the post-record arc → Row 1 becomes "Post-Record Harness Design from Dated Negatives", Row 2 becomes "Ninth Post-Record Question", etc. MP-71 has consumed MP-70's decision; the pre-record arc governs.

## Exit Criteria (Session 8)

- ADR-0025 at zero UNDECIDED rows
- Exactly one LAUNCHED research row (GPU grokking run) whose verdict re-derives from its manifest
- `verify-claims` at 0 with every public number traceable to one command
- Clean-clone proof transcript on disk
- Nineteenth teaching artifact shipped with stranger-runnable transcript
- `dev == main`
- Program's twenty-first dated direction (or post-record arc's ninth)