---
tags: [phase/7, capstone, execution/log]
created: 2026-09-01
consumes: [ADR-0027, configs/capstone.yaml]
---

# Capstone Execution Log — MP-78

## Session 0 (2026-09-01) — Gate Truthing + 31st-Gen Arc Consumption

**ADR-0027 Status**: Created at Session 0, all 8 rows adjudicated
**Research Row**: Row 1 (Capstone Research Plan Execution) — **OPEN**
**MP-74/77 Verdicts Consumed**: [TO BE FILLED AT SESSION 0]
- R1 GPU Grokking: [SPARSE-FOURIER / NO-GROK]
- R2 Extended Induction: [HEADS_DETECTED / NO_HEADS]
- R3 Neuron Ablation: [DENSE_ATTRACTOR_CONFIRMED / INCONCLUSIVE]
- R5 SAE on Head: [SPARSE_FEATURES / DENSE_RECONSTRUCTION]
- Teaching Artifact v20: [TRANSCRIPT_ON_SHELF / MISSING]
- Paper v20: [DIFF_EXISTS / "v19 IS RECORD"]

**Toolchain Status**:
- LaTeX: [pdflatex/latexmk available or MISSING]
- W&B: [wandb login verified or NEEDS_LOGIN]
- HF CLI: [hf auth status verified or NEEDS_LOGIN]
- Pages Workflow: [.github/workflows/pages.yml EXISTS or MISSING]

**Ex-T31 Execution Memo**: Committed at [timestamp]

---

## Session 1 — Capstone Training Launch + W&B Connection

**Date**: [YYYY-MM-DD]
**Action**: Launched capstone training ×3 seeds

### Training Command
```bash
uv run python -m src.experiments.exp6_capstone \
  --config configs/capstone.yaml \
  --seeds 0,1,2 \
  --checkpoint-every 1000 \
  --save-model \
  --wandb-project "from-gradient-to-transformer-capstone"
```

### Config (configs/capstone.yaml)
- Task: modular_addition (P=113, train_frac=0.3) + induction (vocab=2048, seq_len=128, num_train=8192)
- Model: d_model=256, n_layers=4, n_heads=8, d_mlp=1024, dropout=0.1
- Training: 20000 steps, batch_size=128, lr=3e-4, weight_decay=0.1, cosine schedule, warmup=1000, grad_clip=1.0
- Instrumentation: fourier_every=500, kcomp_every=500, sae_hooks=[ln_final], circuit_patching_every=2000

### Seed 0
- Start time: [timestamp]
- Device: [cuda/cpu]
- Steps completed: [N]
- Checkpoints saved: [step numbers]
- W&B run: [URL or ID]
- Early signals (step 1000):
  - Modular loss: [value]
  - Induction loss: [value]
  - Fourier k_99: [value]
  - Max K-comp: [value]

### Seed 1
- Start time: [timestamp]
- Device: [cuda/cpu]
- Steps completed: [N]
- Checkpoints saved: [step numbers]
- W&B run: [URL or ID]
- Early signals (step 1000): [same metrics]

### Seed 2
- Start time: [timestamp]
- Device: [cuda/cpu]
- Steps completed: [N]
- Checkpoints saved: [step numbers]
- W&B run: [URL or ID]
- Early signals (step 1000): [same metrics]

### W&B Integration
- runner.py wandb logging: [ADDED/VERIFIED]
- Dashboard URL: [https://wandb.ai/...]
- MP-74 backfill: exp1 10k [DONE/PENDING], exp2 GPU [DONE/PENDING]

### Issues/Decisions
- [Any OOM, divergence, config changes, falsifier triggers]

---

## Session 2 — Paper v21 Decision + Capstone Monitor (5k steps)

**Date**: [YYYY-MM-DD]

### Paper v21 Decision
- New numbers from MP-74: [YES/NO]
- If YES: paper v21 diff applied to portfolio/paper/main.tex
- If NO: dated memo written "v20 is the record — no new numbers from MP-78 capstone yet"
- verify-claims: [PASSES/FAILS]

### Capstone Monitor (5k steps)

| Seed | Steps | Modular Acc | Induction Acc | Fourier k_99 | Max K-comp | Val Loss |
|------|-------|-------------|---------------|--------------|------------|----------|
| 0    | 5000  |             |               |              |            |          |
| 1    | 5000  |             |               |              |            |          |
| 2    | 5000  |             |               |              |            |          |

- Fourier trajectory: [DENSE → SPARSE transition observed? / STAYS_DENSE]
- K-comp trajectory: [Step 1 forming? Step 2 forming?]
- Decisions: [continue training / early stop / config adjustment]

---

## Session 3 — HF SAE Browser Deploy (Gated) + Portfolio Rung 1-2

**Date**: [YYYY-MM-DD]

### HF SAE Browser (Row 4)
- Condition met: [YES/NO - confirmed head from MP-74 R5?]
- If YES:
  - Checkpoint used: [path]
  - Deploy command executed: [YES/NO]
  - Space URL: [https://huggingface.co/spaces/...]
  - Space builds: [SUCCESS/FAIL]
  - Browser functional: [YES/NO]
- If NO: Row 4 closed with reason: "No confirmed induction head checkpoint available from MP-74"

### Portfolio Write-ups — Rung 1 & 2
- Rung 1 (Induction Heads): `portfolio/projects/rung-1-induction-heads/index.md` [DRAFTED/COMPLETE]
  - Manifest tag: `<!-- manifest: results/exp1_induction_heads.json -->`
  - Figure: `portfolio/figures/exp1_kcomp_trajectory.png` [COMMITTED/PENDING]
- Rung 2 (Grokking): `portfolio/projects/rung-2-grokking/index.md` [DRAFTED/COMPLETE]
  - Manifest tag: `<!-- manifest: results/exp2_grokking.json -->`
  - Figure: `portfolio/figures/exp2_grokking_curve.png` [COMMITTED/PENDING]

---

## Session 4 — Portfolio Rung 3-5 + Capstone Circuit Discovery

**Date**: [YYYY-MM-DD]

### Portfolio Write-ups — Rung 3, 4, 5
- Rung 3 (Superposition): `portfolio/projects/rung-3-superposition/index.md` [DRAFTED/COMPLETE]
  - Manifest: `results/exp3_superposition.json`
  - Figure: `portfolio/figures/exp3_pentagon_geometry.png`
- Rung 4 (Circuit Patching): `portfolio/projects/rung-4-circuit-patching/index.md` [DRAFTED/COMPLETE]
  - Manifest: `results/exp4_circuit_patching.json`
  - Figure: `portfolio/figures/exp4_patching_results.png`
- Rung 5 (SAE): `portfolio/projects/rung-5-sae/index.md` [DRAFTED/COMPLETE]
  - Manifest: `results/exp5_sae_dashboard.json`
  - Figure: `portfolio/figures/exp5_sparsity_tradeoff.png`

### Capstone Circuit Discovery (Row 1 Deepening)
- Checkpoint used: [latest capstone checkpoint path]
- Induction detection: [heads found? scores?]
- Activation patching: [recovery scores]
- Path patching: [direct effects]
- SAE on capstone activations: [L0, FVE, features]
- Manifest updated: `results/exp6_capstone.json` [YES/NO]

---

## Session 5 — Pages Deploy Workflow + Capstone Final Monitor

**Date**: [YYYY-MM-DD]

### Pages Deploy (Row 6)
- Workflow created: `.github/workflows/pages.yml` [YES/NO]
- Paper compiles: [YES/NO - if NO, deploy without paper PDF]
- Deploy triggered: [push to main]
- Workflow status: [GREEN/RED]
- Live URL: `https://alessiobrillo.github.io/from-gradient-to-transformer/`
- All 5 project pages accessible: [YES/NO]
- Links resolve: [YES/NO]

### Capstone Final Monitor
- Training complete: [YES - target steps reached / EARLY_STOPPED]
- Final checkpoints downloaded: seed 0 [PATH], seed 1 [PATH], seed 2 [PATH]
- Full evaluation suite run:
  - Fourier analysis: [k_90, k_99 per seed]
  - K-composition: [Step 1, Step 2, head count per seed]
  - Circuit patching: [activation/path patching results]
  - SAE: [L0/FVE on final checkpoints]
- Final manifest: `results/exp6_capstone.json` [COMPLETE]

---

## Session 6 — Capstone Teaching Artifact v21 + Stranger Run

**Date**: [YYYY-MM-DD]

### Teaching Artifact
- Notebook: `notebooks/capstone_teaching_artifact_v21.ipynb` [BUILT]
- Cells verified:
  - Cell 1: Train/load capstone model [WORKS]
  - Cell 2: Fourier analysis [WORKS]
  - Cell 3: K-composition [WORKS]
  - Cell 4: Circuit patching [WORKS]
  - Cell 5: SAE features [WORKS]
  - Cell 6: Literature comparison [WORKS]
  - Cell 7: Honest conclusion [WRITTEN]

### Stranger Run
- Fresh Colab session: [EXECUTED]
- Transcript saved: `notebooks/capstone_teaching_artifact_v21_transcript.md` [COMMITTED]
- Ex-F Distillation (Four Registers):
  1. Paper's sentence: [one quantitative claim]
  2. Annex's sentence: [one qualitative insight]
  3. 30-second spoken claim: [text]
  4. 5-minute teaching explanation with worked toy: [text/link]

---

## Session 7 — Shelf Rehearsal + Gate-Debt Final Re-verification

**Date**: [YYYY-MM-DD]

### Shelf Rehearsal (Hostile-Webmaster Walk at Zero)
- Every public number clicks back to disk: [VERIFIED]
  - RESULTS.md tags → manifests → commands
- Local `main` reconciled with `origin/main`: [YES/NO]
- README current: [YES/NO]
- Residue gone: [YES/NO]
- Annexes' home verified: [YES/NO]
- Portfolio live at Pages URL: [YES/NO]
- All links resolve: [YES/NO]

### Gate-Debt Re-verification (Row 8)
- `checklists/gate-debt.md` complete: [YES/NO]
- Every cell: LAUNCHED-with-transcript or CLOSED-with-one-reason
- Any claimed closure without transcript: [NONE / LISTED BELOW]
  - [If any: blocks Session 8]

### Capstone Teaching Verification
- Stranger transcript on disk and linked: [YES/NO]
- Ex-F distillation written: [YES/NO]

---

## Session 8 — The Release

**Date**: [YYYY-MM-DD]

### Final State
- ADR-0027 at zero UNDECIDED rows: [YES/NO]
  - Row 1: [LAUNCHED-WITH-VERDICT / CLOSED-WITH-REASON]
  - Row 2: [LAUNCHED-WITH-VERDICT / CLOSED-WITH-REASON]
  - Row 3: [LAUNCHED-WITH-VERDICT / CLOSED-WITH-REASON]
  - Row 4: [LAUNCHED-WITH-VERDICT / CLOSED-WITH-REASON]
  - Row 5: [LAUNCHED-WITH-VERDICT / CLOSED-WITH-REASON]
  - Row 6: [LAUNCHED-WITH-VERDICT / CLOSED-WITH-REASON]
  - Row 7: [LAUNCHED-WITH-VERDICT / CLOSED-WITH-REASON]
  - Row 8: [LAUNCHED-WITH-VERDICT / CLOSED-WITH-REASON]

- Merge green locally and on GitHub: [YES/NO]
- `dev == main`: [YES/NO]
- Home wired: [YES/NO]

### Archive
- This roadmap's companion status retired: [YES/NO]
- Roadmap archived with deviations as dated ledger notes: [YES/NO]

### Post-MP-78 Transition
- If capstone produced publishable results: next phase = paper submission + reproduction package
- If capstone needs more compute: next phase = scaled training run
- Record's closing sentence consumed 21 times, never repeated: [VERIFIED]

---

## Summary Metrics

| Metric | Target | Achieved |
|--------|--------|----------|
| Capstone seeds complete | 3/3 | /3 |
| Steps per seed | 20000 | |
| Manifests produced | 6 (exp1–exp6) | /6 |
| Portfolio pages live | 5 | /5 |
| Teaching artifacts with transcripts | 2 (v20 + v21) | /2 |
| verify-claims | 0 issues | |
| CI (lint/typecheck/test) | GREEN | |
| Gate-debt | Complete | |

---

**Written**: 2026-09-01 (Session 0 template)
**Perspective**: Personal execution log / learning showcase
**Status**: Ready for Session 1 execution