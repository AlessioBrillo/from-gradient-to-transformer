---
tags: [type/moc, phase/7, research/experiment, state/roadmap]
created: 2026-09-01
consumes: [ADR-0024]
---

# Micro-Phase 78 — Capstone Integration & Publication: The 21st Dated Direction

> **STATUS: PRE-EXECUTION.** This roadmap covers MP-78, the capstone integration and publication phase. It consumes MP-74/77's release report (ADR-0024 at zero UNDECIDED rows, target 2026-09-06). ADR-0027 is the 21st continuum ledger. Everything factual here is pre-registered — the candidate set is frozen at Session 0, never improvised.

---

## Showcase Framing

This is the 21st roadmap written from an *executed* roadmap's release report — the program at its normal, confirmed twenty-one times. The discipline that has held for twenty phases now holds for the twenty-first: facts re-verified session by session, a ledger that stamps rows or closes them with one named reason, negatives shipped as loudly as positives, and one deep question chosen per phase. The measured line: **ADR-0027 at zero UNDECIDED rows on release day, with the capstone decoder-only transformer trained, reverse-engineered, and the portfolio live.**

---

## Part I — Where I Stand (State Review, Pre-Registered)

### The Scientific Ledger (Carried Forward from MP-74/77)

The record's deepest fact remains unchanged: **no run in this repository's history has ever produced a sparse Fourier solution.** The count advances only with a new verdict.

- **P=59 drills dense 59/59**; **P=113 CPU 3-seed: NO-GROK** (val 1.0, k₉₉ = 111/113); positive-control scan **ALL-DENSE** at P=59/67/97.
- **Microscope trials**: embedding re-normalization falsified as suppressor (k₉₉ = 112/113, val 0.7176); schedule/weight-decay trials logged in ADR-0003.
- **R1 standard-scale ×3-seed**: 0/8 heads at 3k epochs (peak diag+1 mass 0.075 at epoch 499, peak val acc 0.5083 at epoch 1950, K-composition max 0.056).
- **GPU P=113 3-seed**: Launched Colab 2026-08-24 (MP-74 Session 1), verdict pending MP-74 Sessions 2-3.
- **Extended Induction 10k epochs ×3 seeds**: Launched MP-74 Session 2, in progress.
- **Neuron Ablation on Dense Grokking**: Launched MP-74 Session 2 parallel, in progress.
- **Clean-Clone Proof**: **GREEN 2026-08-27** — full transcript in `06_production_ai/proofs/reproducible-from-clean-clone.md`.
- **All five manifests on disk** (`results/exp1…exp5`), `verify-claims` at **0** — re-verified live.
- **CI Floor**: 197 tests, ruff, blocking mypy, markdownlint green; `verify-claims` at 0.

### The Stack at Intake

- **MP-74/77** (GPU unblock + execution): Sessions 2–8 in progress / complete by 2026-09-06.
- **ADR-0024** = 20th continuum ledger — will be finalized at MP-74 release with zero UNDECIDED rows.
- **ADR-0027** = 21st continuum ledger (this phase) — eight rows pre-stamped below.
- **MP-30 through MP-36**: Gate-debt ledger tracked in `checklists/gate-debt.md` — all PENDING, owned by their respective phases.

### The Three Hard Blockers (Resolved or In-Progress)

| Blocker | Status | Resolution |
|---------|--------|------------|
| **GPU Access** — P=113 grokking never run on GPU | Colab launched 2026-08-24 | MP-74 Sessions 2-3: monitor, download, verdict |
| **Induction Heads at Scale** — 0/8 heads at 3k epochs | 10k epoch run launched MP-74 Session 2 | MP-74 Session 3: monitor at 4k/6k/8k/10k |
| **Clean-Clone Proof** — Phase 6 gate | **GREEN 2026-08-27** | Phase 6 gate unlocked; MP-35 capstone unblocked |

---

## Part II — The Bottleneck Analysis (What Must Not Drift)

### 1. The Consumption Chain Is Now 31st Generation Deep

MP-74 Session 0 consumed MP-70's release report; MP-78 Session 0 will consume MP-74's release report. The chain is now thirty-first generation deep. **A session stamps, it never re-decides.** The candidate set is frozen before S0.

### 2. The Capstone Training Is the New Critical Path

MP-35 (capstone research plan execution) has been gated on Phase 6 since 2026-08-23. The clean-clone proof green unlocks it. **My highest-leverage act: protect the capstone training window** — it is the artifact the portfolio, paper, and teaching artifact all consume.

### 3. The Publication Artifacts Are the Hardest Deliverables

- Paper v21 compile gate (LaTeX toolchain still missing — MP-31 Row 1)
- Pages deploy workflow (MP-31 Row 2)
- HF Spaces SAE browser (MP-30 Row 2, gated on R5)
- Portfolio write-ups (MP-32 Row 1)
- W&B integration (MP-30 Row 1, MP-33 Row 1)

Each is a dated row owned by MP-30–MP-36 — their residue, never my re-planning.

### 4. The Steady State Must Not Become Ceremony

This is the 21st roadmap from an executed roadmap's release report. The drift risk inverts: the machinery is 20 executions deep, so the countermeasure is that rows must still be dated in the session that owns them, verdicts still consumed as artifacts, and zero UNDECIDED rows at Session 8.

### 5. The Capstone's Receipt Is the Final Proof

The 20th teaching artifact (MP-74 Session 6) ships with a stranger transcript. The 21st (capstone) must do the same — but with a *trained* model, not a loaded checkpoint. This is the hardest receipt: train → reverse-engineer → teach, all in one runnable notebook.

---

## Part III — The Roadmap, Step by Step (Continuum Law, 21st Execution, Sessions 0–8)

### The Frozen Candidate Set (Chosen at Session 0, Never Improvised)

| # | Candidate | Opens Only If | Window | Kill-Date | Status |
|---|-----------|---------------|--------|-----------|--------|
| 1 | **Capstone Research Plan Execution** | Clean-clone proof GREEN (Phase 6 gate) | Session 1–5 | 2026-09-12 | **READY** |
| 2 | **Paper Prose from Manifests** | Paper v21 diff exists (new numbers from MP-74) | Session 2 | 2026-09-10 | **GATED** |
| 3 | **W&B Integration + Dashboard** | Always (Phase 6 residue) | Session 1–2 | 2026-09-08 | **READY** |
| 4 | **HF Spaces SAE Browser Deploy** | R5 executed with confirmed head (MP-74) | Session 3 | 2026-09-11 | **GATED** |
| 5 | **Portfolio Project Write-ups (×5)** | Figures exist for all 5 rungs | Session 3–4 | 2026-09-11 | **READY** |
| 6 | **Pages Deploy Workflow** | Paper v21 compiles | Session 5 | 2026-09-12 | **GATED** |
| 7 | **Capstone Teaching Artifact v21** | Capstone training complete + circuit discovery | Session 6 | 2026-09-13 | **GATED** |
| 8 | **Gate-Debt Closure + Final Release** | Rows 1–6 complete | Session 7–8 | 2026-09-14 | **GATED** |

### Universal Override

If MP-74 GPU run (R1) produced **SPARSE-FOURIER**:
- Row 2 (Paper) prioritizes per-frequency reading on the first sparse solution this harness ever produced
- Row 4 (SAE Browser) uses the sparse-regime checkpoint
- Row 7 (Teaching Artifact) centers the sparse circuit discovery narrative
- Kill-dates adjusted in the same session

If MP-74 GPU run produced **NO-GROK** (current expectation):
- Row 2 (Paper) writes the "dense attractor" derivation from R3 neuron ablation
- Row 4 (SAE Browser) stays on synthetic + best-available real checkpoint
- Row 7 (Teaching Artifact) centers "sometimes the model finds a different algorithm"

### Post-Record Override

If MP-74 Session 0 continued the post-record arc (it did not per ADR-0024 intake):
- Row 1 becomes "Post-Record Harness Design from Dated Negatives"
- Row 2 becomes "Ninth Post-Record Question"
- Row 3 becomes "Tenth Post-Record Question"
- etc.

---

### Session 0 (~2 h) — Gate Truthing + 31st-Generation Arc Consumption

**Objective**: Consume MP-74 release report; freeze ADR-0027 candidate set; verify toolchains.

#### Actions

1. **Consume MP-74 Release Report (ADR-0024 Final State)**:
   - Read ADR-0024 at zero UNDECIDED rows
   - Extract R1 verdict (SPARSE-FOURIER or NO-GROK)
   - Extract R2/R3/R5 verdicts
   - Extract teaching artifact v20 transcript location
   - Extract paper v20 decision (diff or "v19 is record" memo)

2. **Adjudicate ADR-0027 Candidate Set**:
   - Row 1: Capstone execution — **OPEN** (clean-clone proof GREEN)
   - Row 2: Paper prose — **OPEN** if new numbers, else **CLOSED** "v20 is record"
   - Row 3: W&B integration — **OPEN** (always)
   - Row 4: HF SAE Browser — **OPEN** if MP-74 R5 produced confirmed head, else **CLOSED** "no real head"
   - Row 5: Portfolio write-ups — **OPEN** (figures exist)
   - Row 6: Pages deploy — **OPEN** if paper compiles, else **CLOSED** "no TeX"
   - Row 7: Capstone teaching artifact — **OPEN** (capstone training runs)
   - Row 8: Gate-debt closure — **OPEN** (ledger exists)

3. **Toolchain Verification (Pinned in S0, Never Discovered at S7)**:
   ```bash
   # LaTeX
   which pdflatex || echo "MISSING: will use graceful fallback"
   # W&B
   wandb login --verify || echo "NEEDS: wandb login"
   # HF CLI
   hf auth status || echo "NEEDS: hf auth login"
   # Pages workflow
   test -f .github/workflows/pages.yml || echo "MISSING: will create in Session 5"
   ```

4. **Write Ex-T31 Execution Memo**:
   - Document: MP-74 verdict consumed, ADR-0027 rows adjudicated, conditions cited
   - Stamp: date, session, decision rule

**Exit Criteria**: ADR-0027 eight rows stamped PENDING/GATED/CLOSED-with-reason; Ex-T31 memo committed; toolchain status recorded.

---

### Session 1 (~4 h) — Capstone Training Launch + W&B Connection

**Objective**: Launch decoder-only transformer training; connect all experiments to W&B.

#### Actions

1. **Launch Capstone Training (Row 1)**:
   ```bash
   # Config: decoder-only, d_model=256, n_layers=4, n_heads=8, vocab=2048, seq_len=128
   # Modular addition task (P=113) + induction task (repeated prefixes)
   # Full instrumentation: Fourier analysis, K-composition, activation harvesting, SAE hooks
   uv run python -m src.experiments.exp6_capstone \
     --config configs/capstone.yaml \
     --seeds 0,1,2 \
     --checkpoint-every 1000 \
     --save-model \
     --wandb-project "from-gradient-to-transformer-capstone"
   ```
   - Multi-seed (3) with checkpointing every 1000 steps
   - Modular addition (grokking) + in-context learning (induction) joint training
   - Full circuit discovery instrumentation enabled

2. **W&B Integration (Row 3)**:
   - Add `wandb` logging to `src/experiments/runner.py` (opt-in via `--wandb`)
   - Log: metrics (loss, acc, Fourier sparsity, K-composition), configs, checkpoints as artifacts
   - Backfill MP-74 runs (exp1 10k, exp2 GPU) via manifest upload
   - Dashboard: 6 experiment groups (exp1–exp6) with comparison panels

3. **Monitor Capstone**:
   - Verify first 1000 steps: loss decreasing, gradients flowing, checkpoints saving
   - Confirm Fourier analysis hooks firing (log spectrum every 500 steps)
   - Confirm K-composition diagnostic logging

**Exit Criteria**: Capstone running ×3 seeds; W&B dashboard live with all 6 experiment groups; first checkpoint saved.

---

### Session 2 (~3 h) — Paper v21 Decision + Capstone Monitor

**Objective**: Decide paper v21; monitor capstone at 5k steps.

#### Actions

1. **Paper v21 Decision (Row 2)**:
   ```bash
   # If MP-74 produced new numbers (R1/R2/R3/R5):
   # Edit portfolio/paper/main.tex with new prose from manifests
   # make paper  # verify compile (graceful if no TeX)
   # Else:
   # Write dated memo: "v20 is the record — no new numbers from MP-78 capstone yet"
   ```
   - Every quantitative claim must have `<!-- manifest: ... -->` tag in RESULTS.md
   - Success criterion: `verify-claims` passes with updated manifests

2. **Capstone Monitor (5k steps)**:
   - Check Fourier sparsity trajectory: dense → sparse transition?
   - Check K-composition: induction heads forming?
   - Check validation accuracy on both tasks

3. **Update ADR-0027**:
   - Row 2: stamp paper decision with date
   - Row 1: update capstone status (step count, any early signals)

**Exit Criteria**: Paper decision dated; capstone at 5k+ steps; ADR-0027 Row 2 stamped.

---

### Session 3 (~3 h) — HF SAE Browser Deploy (Gated) + Portfolio Write-ups Start

**Objective**: Deploy SAE browser if real head exists; write Rung 1-2 project pages.

#### Actions

1. **HF Spaces SAE Browser (Row 4 — Gated)**:
   ```bash
   # If MP-74 R5 produced confirmed induction head checkpoint:
   uv run python -m src.experiments.exp5_sae_dashboard \
     --activations-from checkpoints/exp1_trained_model_seed0.pt \
     --hooks ln_final --dict-size 256 --epochs 300 \
     --export-hf-space --hf-repo "username/sae-browser"
   # Push to HF Spaces; verify Space builds and loads
   ```
   - If no real head: document dependency honestly, close Row 4 with reason

2. **Portfolio Write-ups (Row 5) — Rung 1 & 2**:
   - `portfolio/projects/rung-1-induction-heads/index.md`
   - `portfolio/projects/rung-2-grokking/index.md`
   - Each: problem, method, key figure (manifest-linked), notebook link, limitations

**Exit Criteria**: Row 4 stamped (deployed or closed); Rung 1-2 pages drafted.

---

### Session 4 (~3 h) — Portfolio Write-ups Complete + Capstone Circuit Discovery

**Objective**: Finish all 5 portfolio pages; run circuit discovery on capstone checkpoint.

#### Actions

1. **Portfolio Write-ups (Row 5) — Rung 3, 4, 5**:
   - Rung 3: Superposition (`portfolio/projects/rung-3-superposition/`)
   - Rung 4: Circuit Patching (`portfolio/projects/rung-4-circuit-patching/`)
   - Rung 5: SAE Dashboard (`portfolio/projects/rung-5-sae/`)
   - Each page: manifest-linked figure, runnable notebook, honest limitations

2. **Capstone Circuit Discovery (Row 1 Deepening)**:
   - Load latest capstone checkpoint (10k+ steps)
   - Run `exp4_circuit_patching.py` diagnostics: induction head detection, activation patching, path patching
   - Run `exp5_sae_dashboard` on capstone activations (real model, real features)
   - Log results to capstone manifest (`results/exp6_capstone.json`)

**Exit Criteria**: All 5 portfolio pages drafted; capstone circuit discovery manifest entries added.

---

### Session 5 (~2 h) — Pages Deploy Workflow + Capstone Final Monitor

**Objective**: Deploy portfolio to GitHub Pages; verify capstone training complete.

#### Actions

1. **Pages Deploy Workflow (Row 6 — Gated)**:
   ```yaml
   # .github/workflows/pages.yml
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
   - If paper compiles: include `portfolio/paper/main.pdf` in deploy
   - If no TeX: deploy portfolio without paper PDF

2. **Capstone Final Monitor**:
   - Verify training complete (target steps reached or early stopping)
   - Download final checkpoints ×3 seeds
   - Run full evaluation suite: Fourier, K-composition, circuit patching, SAE
   - Generate final manifests

**Exit Criteria**: Pages workflow green (portfolio live); capstone training complete; final manifests on disk.

---

### Session 6 (~3 h) — Capstone Teaching Artifact v21 + Stranger Run

**Objective**: Build and validate the capstone teaching notebook.

#### Actions

1. **Build Teaching Artifact v21** (`notebooks/capstone_teaching_artifact_v21.ipynb`):
   - Cell 1: Train decoder-only transformer (or load capstone checkpoint)
   - Cell 2: Modular addition Fourier analysis — show spectrum (dense/sparse per verdict)
   - Cell 3: Induction head detection — K-composition diagnostic
   - Cell 4: Circuit patching — activation/path patching on discovered circuits
   - Cell 5: SAE feature extraction — show real features from trained model
   - Cell 6: Compare to literature (Nanda sparse circuit, Olsson induction heads)
   - Cell 7: Honest conclusion — what we learned, what we didn't, what's next

2. **Stranger Run**:
   - Execute on fresh Colab session as stranger
   - Save output → transcript committed to `notebooks/capstone_teaching_artifact_v21_transcript.md`
   - Compare against MP-74 teaching artifact transcript (Ex-F distillation)

**Exit Criteria**: Artifact shipped with transcript; Ex-F distillation complete (four-register verdict for capstone).

---

### Session 7 (~2 h) — Shelf Rehearsal + Gate-Debt Final Re-verification

**Objective**: Final public shelf verification; gate-debt ledger complete.

#### Actions

1. **Shelf Rehearsal (Hostile-Webmaster Walk at Zero)**:
   - Every public number clicked back to disk (RESULTS.md tags → manifests → commands)
   - Local `main` reconciled with `origin/main`
   - README current, residue gone, annexes' home verified
   - Portfolio live at Pages URL, all links resolve

2. **Gate-Debt Re-verification (Row 8)**:
   - Re-verify all MP-30–MP-36 rows in `checklists/gate-debt.md`
   - Each cell: LAUNCHED-with-transcript or CLOSED-with-one-reason
   - A claimed closure without its transcript stays open and blocks Session 8

3. **Capstone Teaching Verification**:
   - Stranger transcript on disk and linked
   - Ex-F distillation (four registers) written

**Exit Criteria**: Shelf walk at zero; gate-debt.md complete; teaching artifact verified.

---

### Session 8 (~1 h) — The Release

**Objective**: Zero UNDECIDED rows; merge; dev == main; home wired.

#### Actions

1. **ADR-0027 at Zero UNDECIDED Rows**:
   - All eight rows: LAUNCHED-with-verdict or CLOSED-with-one-reason
   - Merge green locally and on GitHub
   - `dev == main`; home wired

2. **Archive Roadmap**:
   - This roadmap's companion status retired
   - Roadmap archived with deviations as dated ledger notes

3. **Post-MP-78 Transition Note**:
   - If capstone produced publishable results: next phase = paper submission + reproduction package
   - If capstone needs more compute: next phase = scaled training run
   - Record's closing sentence consumed 21 times, never repeated

**Exit Criteria**: The merge; the program's 21st dated direction.

---

### The One Measured Line

ADR-0027 at **zero UNDECIDED rows** on release day (target 2026-09-20), with exactly one
LAUNCHED research row (Row 1, capstone training) whose results re-derive from manifests;
`verify-claims` at 0 with every public number re-derivable from one command line; the
hostile-webmaster walk at zero on the live shelf (Pages URL) and on the repo's own shelf
(local `main` reconciled, README current, residue removed, gate-debt ledger complete);
the 20th teaching artifact (MP-74) and 21st teaching artifact (capstone) both shipped
with stranger-runnable transcripts; `dev == main` and the program's 21st dated direction.

---

## Part IV — Deep-Dive Study and Research Topics (Sessions 0–8)

### 1. The Dense Grokking Mechanism — From MP-74 R3 to Capstone

**Question**: *Does the capstone model (larger, jointly trained) find the same dense algorithm or a different one?*

- **Primary sources**: Varma et al. (2023), Lyu et al. (2024), Chughtai et al. (2023)
- **Prediction**: Joint training on modular addition + induction creates pressure toward compositional algorithms. The capstone model may develop *modular* circuits — separate Fourier-like subspaces for addition, separate induction heads for copying — with a routing mechanism.
- **Experiment**: On capstone checkpoints, run neuron ablation + Fourier ablation + path patching. Compare to P=113 CPU dense solution.

### 2. Induction Head Emergence at Scale — From MP-74 R2 to Capstone

**Question**: *Does joint training with modular addition accelerate or delay induction head emergence?*

- **Primary sources**: Olsson et al. (2022), Nanda & Jacobsen (2023), Liu et al. (2023)
- **Prediction**: The modular addition task provides a "curriculum" — the model learns positional structure first (useful for addition), which transfers to induction (positional copying). Expect earlier Step 1 formation vs. standard-scale alone.
- **Experiment**: Compare capstone Step 1/Step 2 trajectory at 3k/5k/10k steps vs. MP-74 R2 standard-scale 10k run.

### 3. SAE on Real Capstone Activations — The Sparsity Gap Resolution

**Question**: *Does a properly trained, circuit-rich model yield sparse SAE features?*

- **Primary sources**: Bricken et al. (2023), Cunningham et al. (2024), Templeton et al. (2024)
- **Prediction**: The capstone model at 20k+ steps with confirmed induction heads + grokking circuits will have genuinely sparse features. SAE L0 should drop to 20-30 (vs 136 on undertrained model).
- **Experiment**: SAE on capstone `ln_final` activations at multiple training checkpoints. Plot L0/FVE trajectory over training.

### 4. The Capstone as a Unified Mechanistic Model

**Question**: *Can a single small transformer simultaneously exhibit grokking, induction, superposition, and interpretable circuits?*

- **Primary sources**: Research plan in `07_capstone/research-plan.md`; all 5 rung papers
- **Prediction**: Yes — at `d_model=256, 4-layer, 8-head`, the model has capacity for all phenomena. The challenge is training dynamics: modular addition needs weight decay + cosine schedule; induction needs fresh batches + sufficient prefixes. Joint curriculum may resolve both.
- **Experiment**: Full capstone training run with all 5 rung diagnostics at checkpoints.

### 5. The Record Teaches, Round Twenty-One

**Question**: *Can I distill the 21st verdict into four registers without leakage?*

The 21st verdict in four registers — the paper's sentence, the annex's sentence, the 30-second spoken claim, and the 5-minute teaching explanation with a worked toy a stranger can run; the gap between the last two is where my teaching leaks, and I will measure it deliberately by writing all four registers for the same verdict (Ex-F, capstone edition).

---

## Part V — Documentation Requirements (The Contract)

| Artifact | Location | Trigger |
|----------|----------|---------|
| **This roadmap** (promoted from companion at Session 0) | `00_meta/78_micro-phase-78-execution-roadmap.md` | Session 0 |
| **ADR-0027 updates** (row verdicts, heartbeats) | `docs/adr/0027-continuum-ledger-21.md` | Each session |
| **Capstone Config & Execution Log** | `07_capstone/execution-log.md` | Session 1 |
| **W&B Dashboard URL** | `docs/adr/0027-continuum-ledger-21.md` (Row 3) | Session 1 |
| **Paper v21 Diff** or **"v20 is the record" memo** | `portfolio/paper/main.tex` v21 + diff log / memo | Session 2 |
| **HF Spaces SAE Browser URL** | `docs/adr/0027-continuum-ledger-21.md` (Row 4) | Session 3 |
| **Portfolio Project Pages (×5)** | `portfolio/projects/rung-{1..5}/index.md` | Session 3–4 |
| **Pages Deploy Workflow** | `.github/workflows/pages.yml` | Session 5 |
| **Capstone Manifest** | `results/exp6_capstone.json` | Session 5 |
| **Gate-Debt Ledger** (complete) | `checklists/gate-debt.md` | Session 7 |
| **Capstone Teaching Artifact v21 + Transcript** | `notebooks/capstone_teaching_artifact_v21.ipynb` + transcript | Session 6 |
| **Ex-T31 Execution Memo** | `00_meta/78_micro-phase-78-execution-roadmap.md` (companion) | Session 0 |
| **Progress Log** | `00_meta/03_progress-log.md` | Every session |
| **Final Release Report** | `00_meta/78_micro-phase-78-release-report.md` | Session 8 |

### Manifest Tags Required in RESULTS.md (Updated)

```markdown
<!-- manifest: results/exp1_induction_heads.json -->   (MP-74 extended 10k-epoch run)
<!-- manifest: results/exp2_grokking.json -->          (MP-74 GPU 3-seed P=113)
<!-- manifest: results/exp3_superposition.json -->     (pentagon geometry, solid)
<!-- manifest: results/exp4_circuit_patching.json -->  (with real head if MP-74 R2 opens)
<!-- manifest: results/exp5_sae_dashboard.json -->     (real activation from head if MP-74 R5 opens)
<!-- manifest: results/exp6_capstone.json -->          (capstone: Fourier, K-comp, circuits, SAE)
```

---

## Part VI — Practical Exercises and Hands-On Challenges

### Ex-1 · Capstone Training Drill (Sessions 1–5)

**Goal**: Train decoder-only transformer with full mechanistic instrumentation.

```bash
# Config in configs/capstone.yaml:
# task: modular_addition + induction
# P: 113 (modular) + vocab=2048, seq_len=128 (induction)
# model: d_model=256, n_layers=4, n_heads=8, d_mlp=1024
# training: 20000 steps, batch_size=128, lr=3e-4, cosine schedule, wd=0.1
# instrumentation: fourier_every=500, kcomp_every=500, sae_hooks=ln_final
# seeds: 0,1,2
# checkpoint_every: 1000

uv run python -m src.experiments.exp6_capstone \
  --config configs/capstone.yaml \
  --seeds 0,1,2 \
  --checkpoint-every 1000 \
  --save-model \
  --wandb-project "from-gradient-to-transformer-capstone"
```

**Falsifier**: If OOM at batch_size=128 → reduce to 64, log change, re-run. If loss diverges → check gradient clipping, lr schedule.

---

### Ex-2 · W&B Integration Retrofit (Session 1)

**Goal**: Connect all 6 experiments to W&B with unified dashboard.

```python
# In src/experiments/runner.py — add to run_seeds():
if wandb_run is not None:
    wandb_run.log({f"seed_{seed}/{k}": v for k, v in metrics.items()})
    # Log checkpoint as artifact every N steps
    if step % checkpoint_every == 0:
        artifact = wandb.Artifact(f"checkpoint-step-{step}", type="model")
        artifact.add_file(checkpoint_path)
        wandb_run.log_artifact(artifact)
```

**Success**: All 6 experiment groups visible in W&B; metrics comparable across runs; checkpoints downloadable.

---

### Ex-3 · HF Spaces SAE Browser Deploy (Session 3, Gated)

**Goal**: Interactive feature browser for real model activations.

```bash
# If confirmed head checkpoint exists from MP-74 or capstone:
uv run python -m src.experiments.exp5_sae_dashboard \
  --activations-from checkpoints/best_head_checkpoint.pt \
  --hooks ln_final --dict-size 256 --epochs 300 \
  --export-hf-space --hf-repo "username/sae-browser-capstone"
```

**Success**: Space builds; browser loads; features clickable with activation histograms, top-activating examples, Fourier spectra.

---

### Ex-4 · Portfolio Write-up Sprint (Sessions 3–4)

**Goal**: 5 production-ready project pages.

```markdown
# portfolio/projects/rung-1-induction-heads/index.md
## Rung 1: Induction Heads
**Problem**: Detect and verify induction heads in a 2-layer attention-only transformer.
**Method**: K-composition diagnostic (Nanda & Jacobsen 2023) on fresh-batches training.
**Key Result**: <!-- manifest: results/exp1_induction_heads.json --> [K-comp score at 10k epochs]
**Figure**: ![K-composition trajectory](figures/exp1_kcomp_trajectory.png) <!-- manifest: results/exp1_induction_heads.json -->
**Notebook**: `notebooks/exp1_induction_heads_demo.ipynb`
**Limitations**: Standard scale (d_model=64) may not reflect larger model dynamics.
```

**Falsifier**: Any claim without a manifest tag → cut or re-run.

---

### Ex-5 · Pages Deploy Pipeline (Session 5)

**Goal**: Auto-deploy portfolio on push to main.

```bash
# Create .github/workflows/pages.yml (see Session 5 actions)
# Test: push to dev → verify preview deployment
# Merge to main → verify production deployment
```

**Success**: `https://alessiobrillo.github.io/from-gradient-to-transformer/` serves portfolio with all 5 project pages.

---

### Ex-6 · Capstone Teaching Artifact: "One Model, Five Phenomena" (Session 6)

**Goal**: One runnable Colab that trains & reverse-engineers a decoder-only transformer.

- Cell 1: Train (or load) capstone model — modular addition + induction
- Cell 2: Fourier analysis — grokking spectrum (dense vs sparse)
- Cell 3: Induction detection — K-composition Step 1 → Step 2
- Cell 4: Circuit patching — activation/path patching on discovered circuits
- Cell 5: SAE features — real features from trained model
- Cell 6: Literature comparison — Nanda, Olsson, Elhage et al.
- Cell 7: Honest conclusion: "One model, five phenomena — but only if trained right"

**Transcript**: Stranger runs on fresh Colab → saves output → transcript committed.

---

### Ex-7 · The Arc Consumption, 31st Generation (Session 0, Verdict-Agnostic)

MP-74's release report consumed with dates as MP-78 intake. The execution memo (Ex-T31) exists, names the decision rule that closes or continues the program's science, cites criteria from MP-74's release report — the chain now 31st generation deep, a session stamps, it never re-decides.

---

### Ex-8 · The Fork Drill, Final Form (Session 0, Verdict-Agnostic)

Two one-page paths: `fork_sparse.md` (if MP-74 R1 = SPARSE-FOURIER) and `fork_dense.md` (if MP-74 R1 = NO-GROK) — what each verdict changes downstream, including paper framing, SAE browser checkpoint, teaching narrative — so MP-79's S0 decision is a stamping, not a discovery.

---

## Part VII — Strategic Tips and Architectural Best Practices

### 1. The One-Question Law, 21st Execution

A phase that opens two research questions is drift by another name; the unchosen candidates close in the same session as the choice. The continuum law is the mechanical refusal of this drift — proven executable twenty times, it must simply be executed again.

### 2. The Candidate Set Is Frozen Before S0, Never Improvised At It

ADR-0027's 8 rows are conditions, not predictions; a session decides, it never invents — and the terminal-state object is the hardest frozen object on the record: written by MP-40, executed by MP-41, consumed by MP-42... consumed a 31st time by MP-78 — never re-negotiated in the consuming session.

### 3. Consumption Is Execution

A verdict consumed into an artifact in the same session is a result; consumed into a paragraph written later it is a memory. Session 0 produces the Ex-T31 execution memo with dated verdicts — or the post-record statement, if the arc governs.

### 4. The Receipt Compounds

The 20th runnable artifact (MP-74) ships because 19 transcripts proved the format. The 21st (capstone) compounds this — but with a *trained* model, not a loaded checkpoint. This is the hardest receipt: train → reverse-engineer → teach, all in one runnable notebook.

### 5. The Steady State Is the Reward, Not the Ceremony

MP-78 is the 21st roadmap written from an *executed* roadmap's release report — the program at its normal, confirmed 21 times. The cap's lesson was that promises without dates drift; the steady state's discipline is that the machinery never becomes the goal: rows are dated in the session that owns them, or they are not rows.

### 6. Stop-and-Publish Stays Open, and the Post-Record Criterion Is Now 9 Questions Deep

ADR-0004's row 5 is the honest exit; a candidate set that cannot earn a paragraph the record lacks is a phase that should close itself. If the post-record arc governs, the deepest candidate earns the post-record arc's *9th new paragraph* — the record's closing sentence consumed 9 times, never repeated.

### 7. Toolchains Are Pinned in S0, Never Discovered at S7

The paper's compile gate is the hardest artifact in the stack; the v21 rule ("opens only for new numbers") is the insurance that makes a missing toolchain a dated reason, not a crisis.

### 8. Protect the Capstone Training Window

The serialized stack means MP-29's release → ... → MP-74 release → MP-78 capstone. A slip at any link slides the whole chain. The deepest law still applies: a promise can be re-planned forever, but a dated row is answered.

### 9. The S0 Gate Is a Checklist with Receipts

ADR-0024 at zero, the live URL, `verify-claims` at 0, the 20th teaching transcript on disk — a condition with artifacts, not a paragraph.

### 10. The Negative Stays the Signature

The row that closes with one reason dated in the session that owns it is the strongest artifact in the repository. Every positive result in this program has a negative twin that was measured, drafted, and stamped — and the negative twin is the one that proves the positive wasn't cherry-picked.

### 11. Architectural Integrity Check for This Phase

- `src/experiments/checkpointing.py` — battle-tested in MP-12/MP-28/MP-74, do not touch unless falsification test fails
- `src/experiments/runner.py` — multi-seed aggregation + W&B logging backbone
- `src/results.py` — manifest/verification contract, not implementation
- **New**: `src/experiments/exp6_capstone.py` — follows same patterns (checkpointing, runner, results)
- **New**: `configs/capstone.yaml` — single source of truth for capstone hyperparameters

### 12. Reproducibility as a First-Class Citizen

Every figure, every number, every claim must trace back to a manifest and a command. The `make reproduce` target is the single source of truth for "what does this repo produce?" — if it drifts, the science drifts.

### 13. Post-MP-78 Transition Planning (The Next Micro-Phase: MP-79 / ADR-0028)

Upon MP-78 release (target 2026-09-20), the next micro-phase will inherit:

| Item | Expected State at 2026-09-20 |
|------|-------------------------------|
| ADR-0027 | Zero UNDECIDED rows; Row 1 (capstone) verdict stamped |
| Capstone Training | Complete ×3 seeds; final manifests on disk |
| W&B Dashboard | Live with all 6 experiment groups |
| HF SAE Browser | Deployed (if real head) or closed with reason |
| Portfolio | 5 project pages live on Pages |
| Pages Workflow | Green; portfolio live at public URL |
| Teaching Artifacts | v20 (MP-74) + v21 (capstone) both with stranger transcripts |
| Gate-Debt | Complete or absent-with-date |

**MP-79 Candidate Set Preview** (Frozen at MP-79 Session 0):

| Row | Candidate | Opens Only If |
|-----|-----------|---------------|
| 1 | **Paper Submission Package** | Paper v21 compiles with capstone results |
| 2 | **Reproduction Package Release** | All 6 manifests + teaching artifacts + configs |
| 3 | **Scaled Training Run** | Capstone shows promise but needs more compute |
| 4 | **Mechanistic Paper Draft** | Capstone circuits novel + reproducible |
| 5 | **Final Integration & Archive** | Rows 1–4 complete |
| 6 | **Gate-Debt Final Closure** | All MP-30–MP-36 resolved |
| 7 | **Program Retrospective** | 21 phases of receipts synthesized |
| 8 | **Next Research Program Design** | Honest assessment of what's next |

**Terminus**: Release = merge + 14 calendar days from MP-79 Session 0 (target: 2026-10-04).

---

## Part VIII — Post-MP-78 Micro-Phase Preview (MP-79 / ADR-0028)

### Expected Intake (from MP-78 Release Report)

| Item | Expected State at 2026-09-20 |
|------|-------------------------------|
| ADR-0027 | Zero UNDECIDED rows; Row 1 verdict stamped |
| Capstone Training | Complete ×3 seeds; manifests on disk |
| W&B Dashboard | Live with 6 experiment groups |
| HF SAE Browser | Deployed or closed with reason |
| Portfolio | 5 pages live on Pages |
| Pages Workflow | Green |
| Teaching Artifacts | v20 + v21 both with transcripts |
| Gate-Debt | Complete |

### MP-79 Candidate Set Preview (Frozen at MP-79 Session 0)

| Row | Candidate | Opens Only If |
|-----|-----------|---------------|
| 1 | **Paper Submission Package** | Paper v21 compiles with capstone results |
| 2 | **Reproduction Package Release** | All 6 manifests + teaching artifacts + configs |
| 3 | **Scaled Training Run** | Capstone shows promise but needs more compute |
| 4 | **Mechanistic Paper Draft** | Capstone circuits novel + reproducible |
| 5 | **Final Integration & Archive** | Rows 1–4 complete |
| 6 | **Gate-Debt Final Closure** | All MP-30–MP-36 resolved |
| 7 | **Program Retrospective** | 21 phases of receipts synthesized |
| 8 | **Next Research Program Design** | Honest assessment of what's next |

### Terminus

Release = merge + 14 calendar days from MP-79 Session 0 (target: 2026-10-04).

---

**Written**: 2026-09-01  
**Perspective**: Personal study notes / learning log / portfolio showcase  
**Status**: Ready for Session 0 execution — candidate set frozen, conditions explicit, no improvisation. The capstone is the act of finally training the unified model on its native hardware; whatever it produces, the measurement is the contribution.

(End of file)