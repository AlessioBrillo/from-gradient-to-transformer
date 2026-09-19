---
adr: 0029
title: Phase Diagram First — Micro-Phase 93 (Twenty-Fourth Continuum Ledger)
date: 2026-09-18
status: OPEN
phase: 7
tags: [type/ledger, phase/7, research/experiment]
consumes: [ADR-0028]
---

**Written at Session 0 of MP-93, from MP-92's release state.**
**Terminus**: Release = merge + 14 calendar days (target 2026-10-02).
**Consumes**: ADR-0028 final state (all 8 rows LAUNCHED or CLOSED-WITH-ONE-REASON, `verify-claims=0`, 223 tests green, premiere pre-drafts committed).

---

## Continuum Law Executed

ADR-0028 terminated at Session 6 with zero UNDECIDED rows. The frozen candidate set from MP-91/MP-92 had four candidates:

| Candidate | Description | Status |
|-----------|-------------|--------|
| **C1** | Solution-regime phase diagram (sparse vs dense across P, model size, joint/solo) | **SELECTED** |
| **C2** | Scaled Rung 1 induction (standard config, GPU, multi-seed) | Closed — dated reason |
| **C3** | SAE on confirmed-head checkpoint | Closed — dated reason |
| **C4** | ACDC on real circuit | Closed — dated reason |

**Decision**: C1 selected as the single research question for ADR-0029.

---

## Candidate Adjudication (Dated Reasons)

### C2: Scaled Rung 1 Induction — CLOSED
> **Reason**: Standard-scale induction (d_model=64, seq_len=64, 10k epochs) requires GPU and is a scale follow-up, not a primary research question. The 800-epoch fresh-batches result (52.2% vs 0.05%) is the trustworthy scale for this paper. GPU P=113 grokking (MP-74) already pending as external dependency; adding another GPU dependency compounds external risk without new scientific framing. Deferred to a future ledger if GPU access materializes.

### C3: SAE on Confirmed-Head Checkpoint — CLOSED
> **Reason**: Contingent on C2 producing a confirmed induction head. No head exists at current scales (0/8 at quick, 0/4 at patching scale, 0/8 at 800-epoch fresh). SAE on dense reconstructions (53% L0) is already characterized as capacity/budget limit, not scientific signal. Re-opens only when C2 or C1 produces a verified sparse circuit.

### C4: ACDC on Real Circuit — CLOSED
> **Reason**: ACDC automates circuit discovery but requires a ground-truth circuit to validate against. No verified induction head circuit exists at any scale in this repo (all patching _vacuous or 0 heads). ACDC on dense/dissociated circuits would measure algorithmic artifacts, not ground truth. Deferred until a verified circuit exists.

---

## Ledger Row (Single, Pre-Stamped)

| Row | Candidate | Opens Only If | Window | Kill-Date | Status |
|-----|-----------|---------------|--------|-----------|--------|
| 1 | **Solution-regime phase diagram** (sparse vs dense across P, model size, joint/solo) | Always | Session 1–3 | 2026-10-02 | OPEN |

---

## Row Detail: Solution-Regime Phase Diagram

### Scientific Framing

The NO-GROK negative (P=113, val 1.0, k₉₉=111/113 dense) and the capstone dissociation (induction learns, modular doesn't, both dense) suggest a **phase diagram** where:
- Sparse Fourier circuit exists only in specific regime (P, model size, weight decay, LR schedule, solo vs joint)
- Dense attractor is the default for this protocol (cosine LR, wd=1.0, embedding renormalization)
- Joint training shifts the boundary — modular never reaches sparse regime even with dedicated embeddings

### Protocol

Systematic sweep over the control parameters:
1. **Modulus P**: 11, 17, 29, 59, 67, 97, 113 (existing) + 131, 173 (new)
2. **Model size**: d_model ∈ {64, 128, 256, 512}, n_layers ∈ {1, 2, 4}
3. **Weight decay**: 0.1, 0.5, 1.0, 1.5, 2.0
4. **LR schedule**: cosine vs constant vs linear decay
5. **Embedding renormalization**: on vs off (microscope trial 1)
6. **Training mode**: solo modular vs joint modular+induction

### Measurements per Run

- Final val accuracy
- Generalization epoch (first epoch > 0.9 val acc)
- Fourier k₉₉ / P ratio (sparse if < 0.5)
- Fourier sparsity (normalized entropy)
- Fourier ablation: accuracy vs k kept

### Success Criteria

Phase diagram produced as heatmap: P × model_size × wd × schedule → sparse/dense classification. Boundary characterized analytically (theory) and empirically (sweep). At least 3 seeds per cell for statistics.

### Deliverables

- `results/phase_diagram.json` manifest with all cell measurements
- `figures/phase_diagram_heatmap.png` — sparse/dense phase map
- `figures/phase_boundary_analysis.png` — theory vs empirical boundary
- Paper section: "When Does Grokking Occur? A Phase Diagram"

---

## Universal Override

If GPU P=113 run (MP-74, ADR-0024 Row 1) lands SPARSE-FOURIER while ADR-0029 executes:
- Row 1 prioritizes the GPU sparse solution as a new data point in the phase diagram
- Kill-dates adjusted in same session; GPU manifest consumed, never waited on

If GPU run lands NO-GROK (current expectation):
- Row 1 incorporates the GPU dense data point at P=113 with larger model
- Phase diagram boundary shifts accordingly

---

## Sign-Off

**Session 0 (2026-09-18)**: MP-92 release merged (commit 2372877, PR #151). ADR-0028 at zero UNDECIDED rows. Premiere pre-drafts committed. `verify-claims=0`, 223 tests pass, ruff clean, blocking mypy clean. Continuum law executed: exactly one research question (C1) selected; C2, C3, C4 closed with dated reasons above.

**Toolchains pinned**: pdflatex/latexmk absent; `pages.yml` deployed; wandb 0.28.0 (login unverified); hf 1.28.0 (no Space).

**Baseline re-verified Session 0**: 223 tests pass, `ruff check src/ tests/` clean, blocking `mypy` clean on `src/results.py` + `src/experiments/runner.py`, `verify-claims` at 0, 12 manifests on disk, 4 capstone checkpoints.

**Session 6 (target 2026-10-02)**: ADR-0029 at zero UNDECIDED rows; merge green; `main` confirmed; home wired; roadmap archived with deviations as dated ledger notes; program's twenty-fourth dated direction.