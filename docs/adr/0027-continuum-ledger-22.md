---
adr: 0027
title: Capstone Integration & Publication — Micro-Phase 78 (Twenty-Second Continuum Ledger)
date: 2026-09-01
status: OPEN
phase: 7
tags: [type/ledger, phase/7, research/experiment]
consumes: [ADR-0024]
---

**Written from MP-74/77's release report at Session 0 of MP-78.**
**Terminus**: Release = merge + 14 calendar days (target 2026-09-20).
**Consumes**: ADR-0024 final state (zero UNDECIDED rows, R1 verdict, R2/R3/R5 verdicts, teaching artifact v20 transcript, paper v20 decision).

**MP-74 Actual Verdicts (as of 2026-09-03, Session 0 sync):**
- **R1 (GPU Grokking 3-Seed P=113)**: IN_PROGRESS — Colab launched 2026-08-24, verdict pending (no manifest downloaded yet)
- **R2 (Extended Induction 10k Epochs ×3 Seeds)**: NOT_STARTED — only tiny 150-epoch multi-seed exists; 10k standard-scale not yet run
- **R3 (Neuron Ablation on Dense Grokking)**: COMPLETE — results in `results/exp2_grokking.json` under `neuron_ablation`; graceful degradation confirms dense distributed solution
- **R4 (Clean-Clone Reproducibility Proof)**: **GREEN 2026-08-27** — transcript at `06_production_ai/proofs/reproducible-from-clean-clone.md`
- **R5 (SAE on Confirmed-Head Checkpoint)**: GATED — no confirmed induction head produced
- **R6 (Teaching Artifact v20)**: PENDING — not yet built
- **R7 (Paper v20 / Annex v20)**: GATED — no new numbers from MP-74
- **R8 (Gate-Debt Re-verification)**: IN_PROGRESS — ledger updated in `checklists/gate-debt.md`

---

## Ledger Rows (Eight, Pre-Stamped with Windows and Kill-Dates)

| Row | Candidate | Opens Only If | Window | Kill-Date | Status |
|-----|-----------|---------------|--------|-----------|--------|
| 1 | **Capstone Research Plan Execution** | Clean-clone proof GREEN (Phase 6 gate) | Session 1–5 | 2026-09-12 | PENDING |
| 2 | **Paper Prose from Manifests** | Paper v21 diff exists (new numbers from MP-74) | Session 2 | 2026-09-10 | GATED |
| 3 | **W&B Integration + Dashboard** | Always (Phase 6 residue) | Session 1–2 | 2026-09-08 | PENDING |
| 4 | **HF Spaces SAE Browser Deploy** | R5 executed with confirmed head (MP-74) | Session 3 | 2026-09-11 | GATED |
| 5 | **Portfolio Project Write-ups (×5)** | Figures exist for all 5 rungs | Session 3–4 | 2026-09-11 | PENDING |
| 6 | **Pages Deploy Workflow** | Paper v21 compiles | Session 5 | 2026-09-12 | GATED |
| 7 | **Capstone Teaching Artifact v21** | Capstone training complete + circuit discovery | Session 6 | 2026-09-13 | GATED |
| 8 | **Gate-Debt Closure + Final Release** | Rows 1–6 complete | Session 7–8 | 2026-09-14 | GATED |

---

## Universal Override

If MP-74 GPU run (ADR-0024 Row 1) produced **SPARSE-FOURIER**:
- Row 2 (Paper) prioritizes per-frequency reading on the first sparse solution this harness ever produced
- Row 4 (SAE Browser) uses the sparse-regime checkpoint from MP-74
- Row 7 (Teaching Artifact) centers the sparse circuit discovery narrative
- Kill-dates adjusted in the same session

If MP-74 GPU run produced **NO-GROK** (current expectation):
- Row 2 (Paper) writes the "dense attractor" derivation from ADR-0024 Row 3 neuron ablation
- Row 4 (SAE Browser) stays on synthetic + best-available real checkpoint
- Row 7 (Teaching Artifact) centers "sometimes the model finds a different algorithm"

---

## Post-Record Override

If MP-74 Session 0 continued the post-record arc (it did not per ADR-0024 intake):
- Row 1 becomes "Post-Record Harness Design from Dated Negatives"
- Row 2 becomes "Ninth Post-Record Question"
- Row 3 becomes "Tenth Post-Record Question"
- etc.

---

## Row 1: Capstone Research Plan Execution

**Protocol**: Execute `src/experiments/exp6_capstone.py` with config `configs/capstone.yaml`, 3 seeds × 20000 steps, checkpoint every 1000 steps, full mechanistic instrumentation (Fourier, K-composition, activation harvesting, SAE hooks, circuit patching).

**Config** (`configs/capstone.yaml`):
```yaml
task: modular_addition + induction
modular:
  P: 113
  train_frac: 0.3
  epochs: 5000  # within 20k step budget
induction:
  vocab_size: 2048
  seq_len: 128
  num_train: 8192
model:
  d_model: 256
  n_layers: 4
  n_heads: 8
  d_mlp: 1024
  dropout: 0.1
training:
  steps: 20000
  batch_size: 128
  lr: 3e-4
  weight_decay: 0.1
  lr_schedule: cosine
  warmup_steps: 1000
  gradient_clip: 1.0
instrumentation:
  fourier_every: 500
  kcomp_every: 500
  sae_hooks: [ln_final]
  circuit_patching_every: 2000
seeds: [0, 1, 2]
checkpoint_every: 1000
wandb_project: "from-gradient-to-transformer-capstone"
```

**Success Criteria**:
- All 3 seeds complete 20000 steps without OOM or divergence
- Checkpoints saved every 1000 steps
- `results/exp6_capstone.json` manifest produced with per-seed:
  - Modular addition: generalization epoch, Fourier sparsity (k_90, k_99), final val acc
  - Induction: Step 1 (L0 duplicate mass), Step 2 (K-composition), head count
  - Circuit patching: induction head detection scores, path patching effects
  - SAE: L0/FVE tradeoff on real activations at multiple checkpoints
- Figures: `exp6_modular_curve.png`, `exp6_fourier_spectrum.png`, `exp6_induction_kcomp.png`, `exp6_circuit_patching.png`, `exp6_sae_features.png`

**Falsifier**: OOM at batch_size=128 → reduce to 64, log change, re-run. If loss diverges → check gradient clipping, lr schedule, weight decay. If all 3 seeds fail → document failure, close Row 1 with reason.

**Heartbeat**: Step count monitored every session; first checkpoint (1000 steps) at Session 1; Fourier/K-comp trajectories logged to W&B.

---

## Row 2: Paper Prose from Manifests (GATED)

**Protocol**: If MP-74 Rows 1/2/3/5 produced new numbers → paper v21 diff + annex v21 scaffold in `portfolio/paper/main.tex`; else "v20 is the record" dated memo.

**Opens Only If**: New numbers from ADR-0024 Rows 1, 2, 3, or 5 (MP-74 GPU grokking, extended induction, neuron ablation, SAE on head).

**Success Criteria**:
- Every quantitative claim in Results section has `<!-- manifest: ... -->` tag in `portfolio/RESULTS.md` resolving to a number in the JSON
- `make paper` re-verified in CI mirror (graceful if no TeX)
- `portfolio/essay-annex-21.md` on live shelf, manifest-tagged, amended never rewritten
- `verify-claims` passes with updated manifests

**If Not Opened**: Write dated memo: "v20 is the record — no new numbers from MP-78 capstone yet; capstone results reserved for v22." Close Row 2 with reason.

---

## Row 3: W&B Integration + Dashboard

**Protocol**: Add `wandb` logging to `src/experiments/runner.py` (opt-in via `--wandb`). Backfill MP-74 runs (exp1 10k, exp2 GPU) via manifest upload. Dashboard: 6 experiment groups (exp1–exp6) with comparison panels.

**Opens**: Always (Phase 6 residue from MP-30/MP-33).

**Success Criteria**:
- `wandb login` verified in Session 0
- All 6 experiment groups visible in W&B project `from-gradient-to-transformer-capstone`
- Metrics logged per step: loss, acc, Fourier sparsity, K-composition, learning rate
- Configs logged per run
- Checkpoints logged as artifacts every 1000 steps (capstone) / 500 epochs (MP-74 runs)
- Dashboard panels: training curves comparison, Fourier sparsity comparison, K-composition comparison, SAE L0/FVE comparison

**Falsifier**: W&B API rate limits → batch log writes. Authentication issues → `wandb login` in CI secrets.

**Heartbeat**: Session 1: connect capstone runs. Session 2: backfill MP-74 runs. Dashboard URL recorded in ADR-0027.

---

## Row 4: HF Spaces SAE Browser Deploy (GATED)

**Protocol**: Deploy interactive SAE feature browser to Hugging Face Spaces using real activation checkpoint.

**Opens Only If**: MP-74 ADR-0024 Row 5 (SAE on confirmed head) produced a confirmed induction head checkpoint.

**Success Criteria**:
```bash
uv run python -m src.experiments.exp5_sae_dashboard \
  --activations-from checkpoints/best_head_checkpoint.pt \
  --hooks ln_final --dict-size 256 --epochs 300 \
  --export-hf-space --hf-repo "username/sae-browser-capstone"
```
- Space builds successfully (Docker/Gradio)
- Browser loads: feature index, activation histograms, top-activating examples, Fourier spectra per feature
- Features clickable with detailed views
- Space URL recorded in ADR-0027

**If Not Opened**: SAE stays on synthetic + best-available real checkpoint; document dependency honestly. Close Row 4 with reason: "No confirmed induction head checkpoint available from MP-74."

---

## Row 5: Portfolio Project Write-ups (×5)

**Protocol**: Write 5 production-ready project pages in `portfolio/projects/rung-{1..5}/index.md`.

**Opens**: Figures exist for all 5 rungs (verified in MP-74).

**Success Criteria** (per page):
- Problem statement (1-2 paragraphs)
- Methodology (with links to source code)
- Key Result (with `<!-- manifest: ... -->` tag linking to JSON)
- Key Figure (manifest-linked, committed to `portfolio/figures/`)
- Runnable Notebook link (Colab or local)
- Honest Limitations (what this doesn't show, what's next)
- Clean markdown, no broken links

**Rung Mapping**:
- Rung 1: Induction Heads → `portfolio/projects/rung-1-induction-heads/`
- Rung 2: Grokking → `portfolio/projects/rung-2-grokking/`
- Rung 3: Superposition → `portfolio/projects/rung-3-superposition/`
- Rung 4: Circuit Patching → `portfolio/projects/rung-4-circuit-patching/`
- Rung 5: SAE Dashboard → `portfolio/projects/rung-5-sae/`

**Heartbeat**: Rung 1-2 drafted Session 3; Rung 3-5 drafted Session 4.

---

## Row 6: Pages Deploy Workflow (GATED)

**Protocol**: Create `.github/workflows/pages.yml` to auto-deploy `portfolio/` to GitHub Pages on push to `main`.

**Opens Only If**: Paper v21 compiles (Row 2 produces diff) OR portfolio-only deploy.

**Workflow** (`.github/workflows/pages.yml`):
```yaml
name: Deploy Portfolio
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: portfolio
      - uses: actions/deploy-pages@v4
```

**Success Criteria**:
- Workflow passes on push to `main`
- Portfolio live at `https://alessiobrillo.github.io/from-gradient-to-transformer/`
- All 5 project pages accessible
- If paper compiles: `main.pdf` included in deploy

**If Not Opened**: Document "No TeX toolchain — portfolio deployed without paper PDF." Close Row 6 with reason.

---

## Row 7: Capstone Teaching Artifact v21

**Protocol**: Build runnable Colab notebook: "One Model, Five Phenomena" (`notebooks/capstone_teaching_artifact_v21.ipynb`).

**Opens Only If**: Capstone training complete (Row 1) + circuit discovery run (Row 1 deepening).

**Contents**:
- Cell 1: Train decoder-only transformer (or load capstone checkpoint)
- Cell 2: Modular addition Fourier analysis — show spectrum (dense/sparse per MP-74 verdict)
- Cell 3: Induction detection — K-composition Step 1 → Step 2 trajectory
- Cell 4: Circuit patching — activation/path patching on discovered circuits
- Cell 5: SAE feature extraction — real features from trained model
- Cell 6: Literature comparison — Nanda (sparse circuit), Olsson (induction heads), Elhage et al. (superposition)
- Cell 7: Honest conclusion — what we learned, what we didn't, what's next

**Success Criteria**:
- Stranger runs on fresh Colab session → saves output → transcript committed to `notebooks/capstone_teaching_artifact_v21_transcript.md`
- Ex-F distillation complete (four-register verdict for capstone):
  1. Paper's sentence (one quantitative claim)
  2. Annex's sentence (one qualitative insight)
  3. 30-second spoken claim
  4. 5-minute teaching explanation with worked toy

**Heartbeat**: Built Session 6; stranger run same session; transcript committed.

---

## Row 8: Gate-Debt Closure + Final Release

**Protocol**: Re-verify all MP-30–MP-36 row closures in `checklists/gate-debt.md`. Hostile-webmaster walk at zero on live shelf (Pages URL) and repo shelf.

**Opens Only If**: Rows 1–6 complete.

**Success Criteria**:
- `checklists/gate-debt.md` complete: every cell LAUNCHED-with-transcript or CLOSED-with-one-reason
- Shelf rehearsal: local `main` reconciled with `origin/main`; README current; residue gone; annexes' home verified; Pages URL live and all links resolve
- ADR-0027 at zero UNDECIDED rows
- Merge green locally and on GitHub
- `dev == main`; home wired

**Falsifier**: Any claimed closure without transcript → stays open, blocks Session 8.

**Heartbeat**: Session 7 (rehearsal + gate-debt); Session 8 (release).

---

## Deviations from MP-74/77's Release Report

None at Session 0. Any deviations recorded here as dated ledger notes.

---

## Sign-Off

**Session 0 (2026-09-03)**: Intake table committed; thirty-first-generation arc stamped; Row 1 (Capstone Research Plan Execution) chosen as research row; Rows 2–8 stamped PENDING/GATED with actual MP-74 verdicts; ADR-0027 updated. Deviations from ADR-0024 final state: R1 IN_PROGRESS (not complete), R2 NOT_STARTED, R3 COMPLETE, R4 GREEN.

**Ex-T31 Execution Memo (2026-09-03, Session 0)**: MP-74/77's release report consumed with dates as MP-78 intake. Pre-record arc governs (ADR-0024 confirms). MP-74/77's adjudication: R1 GPU grokking = IN_PROGRESS (Colab launched 2026-08-24, verdict pending); R2 extended induction = NOT_STARTED (10k standard-scale not run); R3 neuron ablation = COMPLETE (graceful degradation, dense distributed solution confirmed); R5 SAE on head = GATED (no confirmed head); teaching artifact v20 = PENDING; paper v20 = GATED (no new numbers). Criteria cited: ADR-0024 at zero UNDECIDED, `verify-claims` at 0, 20th teaching transcript on live shelf, `dev == main`. The thirty-first-generation consumption chain: MP-40's Ex-N → MP-41 → ... → MP-70 → MP-74 → MP-78. A session stamps, it never re-decides.

**Session 8**: ADR-0027 at zero UNDECIDED rows; merge green; `dev == main`; home wired; roadmap archived with deviations as dated ledger notes; program's twenty-second dated direction.