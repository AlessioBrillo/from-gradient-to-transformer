---
tags: [type/moc, phase/7, research/experiment, state/roadmap, #research/experiment]
created: 2026-08-25
consumes: [ADR-0024]
---

# Micro-Phase 75 — Next Micro-Phase Roadmap: Executing the GPU Unblock Sessions 1–8 and the Post-Unblock Transition

> **STATUS: PLANNING FOR EXECUTION.** This roadmap covers the *remaining sessions of MP-74* (Sessions 1–8) and the *immediate post-MP-74 micro-phase* that will handle the verdict integration, showcase finalization, and capstone transition. Everything factual here was re-verified against the repository on 2026-08-25: working tree clean, `origin/main` at `ea90829` (PR #104), 189 tests green, ruff clean, blocking mypy clean on `src/results.py` + `src/experiments/runner.py`, `verify-claims` at 0, all five manifests on disk. ADR-0024 is OPEN with intake table committed at Session 0 (2026-08-23).

---

## Showcase Framing — How This Document Reads in Public

This is a dated, first-person artifact of how a research program plans its execution *before* the work runs. Anyone reading the repository in sequence (MP-37 through MP-74 and this file) can watch the same discipline recur: facts re-verified session by session, a ledger that stamps rows or closes them with one named reason, negatives shipped as loudly as positives, and one deep question chosen per phase. If you take one thing from this phase's chapter, take the measured line in Part III: **the GPU run launches in Session 1, or the phase does not release.**

---

## Part I — Where I Stand (State Review, Re-Verified 2026-08-25)

### The Scientific Ledger

The record's deepest fact remains unchanged and carries every dated confirmation: **no run in this repository's history has ever produced a sparse Fourier solution.** The count advances only with a new verdict.

- **P=59 drills dense 59/59**; **P=113's three-seed CPU verdict is NO-GROK** (val 1.0, k₉₉ = 111/113); the positive-control scan stamped **ALL-DENSE** at P=59/67/97.
- **Microscope trial 1 FALSIFIED** (embedding re-normalization is not the suppressor: k₉₉ = 112/113, val 0.7176); trials 2 (`--schedule constant`) and 3 (weight decay 1.5×) pending in ADR-0003's budget.
- **R1 standard-scale ×3-seed run COMPLETED 2026-08-14** with the scheduled no-head negative (0/8 heads, peak diag+1 mass 0.075 at epoch 499, peak val accuracy 0.5083 near epoch 1950, K-composition max 0.056). This remains the newest dated fact on the record's negative side.
- **All five manifests on disk** (`results/exp1…exp5`), `verify-claims` at **0** — re-verified live.

The arc my science has taken is the strongest thing I own:
*Will grokking reproduce?* (MP-28) → *Is the harness itself the suppressor?* (MP-29) → *What is the dense solution's structure?* (MP-29 S3) → *Which open question is deepest?* (MP-36) → the question chain MP-37→MP-67 → *Which of C145–C148 does the consumed 36th verdict open?* (MP-68) → *The GPU unblock that the previous 23 could not execute locally* (MP-69/70) → **MP-71/72/73 pre-registered the cascade** → **MP-74 executes the GPU unblock (Session 0 done, Sessions 1–8 remain).**

### The Stack at Intake

- **MP-29** is current and mid-execution (terminus ≈ 2026-08-26) — the control for dense solution structure.
- **MP-30 through MP-36** stand pre-registered, gated in series, the cap at seven. Each phase's Session 0 consumes the previous phase's release report: no release, no phase.
- **ADR-0023** = MP-70's ledger (eight rows, zero UNDECIDED); **ADR-0024** = MP-71/74's ledger (twentieth continuum ledger, OPEN, eight rows pre-stamped).
- **ADR-0025** = MP-72's ledger; **ADR-0026** = MP-73's ledger — already written as continuations.
- This roadmap will produce **ADR-0027** (twenty-first continuum ledger) from MP-74's release report.

### The CI Floor and Toolchains

189 tracked tests, ruff, blocking mypy, and markdownlint green at last release; `verify-claims` at 0. Verified gaps (facts, not hopes):

- No LaTeX toolchain on this machine (`make paper` graceful, not green)
- No Pages deploy workflow in `.github/workflows/`
- No `publish:` frontmatter policy
- `portfolio/projects/` holds figures but no project write-ups
- W&B never connected

Each is a dated row owned by MP-30–MP-36 — their residue, never my re-planning.

### The Three Hard Blockers (Frozen in ADR-0024 as This Phase's Intake)

| Blocker | Status | What Must Happen in Sessions 1–4 |
|---------|--------|----------------------------------|
| **GPU Access** — P=113 grokking flagship never run on GPU | Colab notebook hardened (`notebooks/colab_grokking_full_run.ipynb`), unexecuted | **Session 1**: Execute 3-seed P=113 on Colab A100/T4; checkpoint every 500 epochs; manifest to Drive |
| **Induction Heads at Scale** — 0/8 heads at 3k epochs standard scale | Fresh-batches run completed 2026-08-14 (0 heads) | **Session 2**: Extend to 10k epochs ×3 seeds with checkpointing every 500; track Step 1/Step 2 independently |
| **Clean-Clone Proof** — Phase 6 gate not green | `reproducible-from-clean-clone.md` proof exists but unexecuted | **Session 4**: Fresh clone → `uv sync` → `make reproduce-quick` → `make verify-claims`; full transcript |

---

## Part II — The Bottleneck Analysis (What I Must Not Let Drift)

### 1. The Consumption Chain Is Now Thirtieth Generation Deep

MP-40's Ex-N defined the terminal state; MP-41's Session 0 executed it; ... MP-70's Session 0 consumed MP-69's Session-0 decision with dates; **MP-74's Session 0 consumed MP-70's Session-0 decision with dates**. This phase's Sessions 1–8 must *execute* the rows opened at Session 0 — the single most dangerous drift is re-litigating a thirty-times-consumed decision. The decision chain is now thirtieth generation deep; a session stamps, it never re-decides.

### 2. The Stacked Execution Remains the Critical Path

This phase's Session 0 consumed MP-70's release report, which consumes ADR-0043's, which awaits MP-29 through MP-40. A slip at any link slides the whole chain; **my highest-leverage act is unchanged: protect MP-29's window** — its release report is the artifact everything downstream consumes. Nothing in Sessions 1–8 may borrow a minute from it.

### 3. The Science's Next Fork Is Three Hard Blockers Deep

ADR-0024's eight candidates (R1–R8) are this phase's frozen candidate set. They are conditions, not predictions; a session decides, it never invents.

### 4. The Steady State Must Not Become Ceremony

This is the twentieth roadmap written from an *executed* roadmap's release report — the program at its normal, confirmed twenty times. The drift risk inverts and deepens: the machinery (ledgers, sessions, gate criteria) is now nineteen executions deep, so the law's countermeasure is that rows must still be dated in the session that owns them, verdicts still consumed as artifacts, and zero UNDECIDED rows at Session 8.

### 5. The Paper's Compile Gate Remains the Hardest Artifact

No TeX on this machine — verified again; MP-31's canon applies early: *toolchains are pinned in Session 0, never discovered at Session 7.* The paper v20 rule ("opens only for new numbers, else v19 is the record") is my insurance.

### 6. The Showcase's Receipts Are Still Future, One Deeper

The eighteenth stranger-run transcript lands only if the lanes execute; C67 (the rate as a policy) is conditioned on ≥ 18 transcripts on disk at Session 0 — the receipt compounds only if the lanes execute.

---

## Part III — The Roadmap, Step by Step (Continuum Law, Twentieth Execution, Sessions 1–8)

### The Frozen Candidate Set (Chosen at Session 0, Never Improvised)

| # | Candidate | Opens Only If | Window | Kill-Date | Status |
|---|-----------|---------------|--------|-----------|--------|
| R1 | **GPU Grokking 3-Seed P=113** | Always (primary flagship) | Session 1–3 | 2026-08-28 | PENDING |
| R2 | **Extended Induction 10k Epochs ×3 Seeds** | Rung 1 < 0.3 diag+1 at 3k (confirmed) | Session 2–3 | 2026-08-30 | PENDING |
| R3 | **Neuron Ablation on Dense Grokking** | GPU run completes (uses existing checkpoints) | Session 2–3 | 2026-08-30 | PENDING |
| R4 | **Clean-Clone Reproducibility Proof** | Always (Phase 6 gate) | Session 4 | 2026-08-27 | PENDING |
| R5 | **SAE on Confirmed-Head Checkpoint** | R2 produces confirmed head (Session 3) | Session 5–6 | 2026-09-01 | GATED |
| R6 | **Teaching Artifact v20** | Always (showcase lane) | Session 6 | 2026-09-01 | PENDING |
| R7 | **Paper v20 / Annex v20** | New numbers from R1/R2/R3/R5 | Session 4–5 | 2026-09-02 | GATED |
| R8 | **Gate-Debt Re-verification** | All MP-30–MP-36 rows | Session 1, 7 | 2026-09-03 | PENDING |

### Universal Override

If GPU run (R1) produces **sparse Fourier** (k₉₉ < P/2 sustained ≥3 checkpoints):
- R1 becomes the sparse-regime mechanism study (Nanda-style per-frequency reading)
- R2/R5 reprioritized to characterize the difference between this run and the NO-GROK runs
- Kill-dates adjusted in the same session

### Post-Record Override

If MP-70's Session 0 continued the post-record arc (it did not — pre-record arc governs per ADR-0024):
- R1 becomes "Post-Record Harness Design from Dated Negatives"
- R2 becomes "Eighth Post-Record Question"
- R3 becomes "Ninth Post-Record Question"
- etc.

---

### Session 1 (~2 h) — The GPU Launch + The Shelf Baseline + The Debt Re-verification

**Objective**: Launch the primary flagship on its native hardware; verify the public shelf integrity; re-verify all MP-30–MP-36 row closures.

#### Actions

1. **Shelf Baseline (Row 5 of ADR-0024 / Row 8 of gate-debt)**:
   - Hostile-webmaster walk of the live site + Space at zero (links, assets, a11y, orphans)
   - Extend to repo's own shelf: local `main` re-verified reconciled to `origin/main`
   - `portfolio/README.md` staleness verified closed
   - Exp6 residue removed with transcript (already done 2026-08-23, re-verify)
   - Annexes' location verified (live shelf recorded with date)

2. **Gate-Debt Re-verification Initial Pass (Row 8)**:
   - Re-verify all MP-30–MP-36 stamped closures from MP-70's release report
   - Each cell: LAUNCHED-with-transcript or CLOSED-with-one-reason
   - A claimed closure without its transcript stays open and blocks Session 8
   - `gate-debt.md` absence (if still absent) recorded with date

3. **Launch R1 (GPU Grokking 3-Seed P=113)**:
   - Upload `notebooks/colab_grokking_full_run.ipynb` to Colab
   - Runtime → Change runtime type → GPU (A100 preferred, T4 fallback)
   - Run all cells: clones `dev` branch, `uv sync --frozen`, runs plotted run + 3-seed manifest run
   - Monitor for OOM at batch_size=512 → reduce to 256, log change, re-run
   - Zip figures, checkpoint, manifest → download to Drive/local

**Exit Criteria**: Rows 5 and 8 stamped; R1 running on Colab with first checkpoint expected at epoch 500.

**Falsifier**: If Colab OOMs persist at batch_size=256 → document failure, close Row 1 with reason, proceed to Row 3 (neuron ablation on existing CPU checkpoints).

---

### Session 2 (~3 h) — The Extended Induction Launch + Neuron Ablation + GPU Monitor

**Objective**: Launch the 10k-epoch induction run; run neuron ablation on existing P=113 checkpoints; monitor GPU run progress.

#### Actions

1. **Launch R2 (Extended Induction 10k Epochs ×3 Seeds)**:
   ```bash
   uv run python -m src.experiments.exp1_induction_heads \
     --standard --epochs 10000 --checkpoint-every 500 --save-model \
     --seeds 0,1,2
   ```
   - Run in background with checkpointing every 500 epochs
   - Track Step 1 (L0 duplicate mass) and Step 2 (K-composition) independently at each checkpoint

2. **Launch R3 (Neuron Ablation on Dense Grokking)**:
   - On existing P=113 CPU checkpoints (seed 0, 1, 2 from 2026-08-11 run)
   - Ablate MLP neurons by activation magnitude (top-k sweep)
   - Compare degradation curve to Fourier ablation curve
   - Scripted to produce `figures/exp2_neuron_ablation.png`
   - Manifest entry appended to `exp2_grokking.json`

3. **Monitor R1 (GPU Run)**:
   - Check Colab runtime status
   - Download first checkpoint if available (epoch 500+)
   - Verify checkpoint integrity (weights load, manifest partial)

**Exit Criteria**: R2 running; R3 complete or running; R1 at 1000+ epochs per seed.

---

### Session 3 (~2 h) — The GPU Run Verdict Intake + Extended Run Monitor

**Objective**: Download and verify GPU run results; monitor extended induction at 4k epochs.

#### Actions

1. **R1 Verdict Intake**:
   - Download from Colab: checkpoints, `results/exp2_grokking.json`, `figures/exp2_*.png`
   - Verify manifest against RESULTS.md tags (`verify-claims` at 0)
   - Read aggregate block: `final_val_acc` (target >0.9 mean), `generalization_epoch` (target well under 5000), `k_99_percent` (target well under 113, e.g., ~10–20 for sparse)
   - **Record verdict honestly**: sparse Fourier or dense (NO-GROK) — this is the measurement, not a hope

2. **R2 Monitor**:
   - Check 2k/4k/6k/8k epoch checkpoints for Step 1 formation (L0 duplicate mass)
   - Plot Step 1/Step 2 trajectory if data available

3. **Update ADR-0024**:
   - Row 1: stamp verdict (SPARSE-FOURIER or NO-GROK) with date
   - Row 2/5: if sparse → reprioritize per Universal Override; if dense → continue as GATED

**Exit Criteria**: R1 manifest on disk; `verify-claims` updated; R2 at 4k+ epochs; ADR-0024 Row 1 stamped.

---

### Session 4 (~2 h) — Clean-Clone Proof + Paper v20 Decision

**Objective**: Prove reproducibility from zero; make paper v20 decision based on new numbers.

#### Actions

1. **Execute Clean-Clone Protocol**:
   ```bash
   cd /tmp && git clone <repo> test-clone && cd test-clone
   uv sync
   make reproduce-quick  # all 5 rungs in --quick mode
   make verify-claims    # must pass
   ```
   - Full transcript to `06_production_ai/proofs/reproducible-from-clean-clone.md` with timestamps
   - If fails → fix blocking issue, re-run; transcript required for release

2. **Paper v20 Decision (Row 7)**:
   - If R1/R2/R3 produced new numbers → paper v20 diff + annex v20 scaffold
   - Else → "v19 is the record" dated memo (no compilation crisis)
   - `make paper` re-verified in CI mirror (graceful if no TeX)

**Exit Criteria**: Clean-clone transcript; paper decision dated; ADR-0024 Row 4 stamped.

---

### Session 5 (~2 h) — Essay Annex v20 + SAE Protocol (Gated on R2 Verdict)

**Objective**: Distill verdict set into essay annex; prepare SAE protocol if R2 produced confirmed head.

#### Actions

1. **Essay Annex v20** (`portfolio/essay-annex-20.md` on live shelf):
   - R1/R2/R3 verdict set distilled into one dated annex
   - Reverse claims audit at zero (prose → manifest → command)
   - Amended never rewritten; annexes' home (live shelf) recorded with date

2. **SAE Protocol (Row 5)**:
   - If R2 produced confirmed induction head at Session 3:
     - Write R5 protocol with site, metric, negative control, kill-date
     - `--activations-from <head_checkpoint> --hooks ln_final --dict-size 256 --epochs 300 --seeds 0,1,2`
   - If no head → SAE stays on synthetic only; document dependency honestly

**Exit Criteria**: Annex drafted; R5 protocol written or closed with reason.

---

### Session 6 (~3 h) — The Teaching Artifact + Stranger Run

**Objective**: Build and validate the runnable teaching artifact.

#### Actions

1. **Build R6 (Teaching Artifact v20 Colab Notebook)**:
   - Cell 1: Train P=113 (or load checkpoint from GPU run)
   - Cell 2: Fourier analysis — show dense/sparse spectrum per actual verdict
   - Cell 3: Ablation sweep — show graceful/catastrophic degradation per actual verdict
   - Cell 4: Neuron ablation — show distributed representation
   - Cell 5: Compare to Nanda et al. sparse circuit (expected vs. got)
   - Cell 6: Honest conclusion: "Sometimes the model finds a different algorithm"

2. **Stranger Run**:
   - Execute on fresh Colab session as stranger
   - Save output → transcript committed
   - Compare against previous artifact's transcript (Ex-M)

**Exit Criteria**: Artifact shipped with transcript; Ex-F distillation complete (four-register verdict).

---

### Session 7 (~2 h) — The Shelf Rehearsal + The Re-check Row + The Teaching Polish

**Objective**: Final public shelf verification; teaching artifact polish.

#### Actions

1. **Shelf Rehearsal (Row 5 re-check)**:
   - Hostile-webmaster walk at zero beside browser, every public number clicked back to disk
   - Repo-shelf findings re-checked (local `main` reconciled, README current, residue gone, annexes' home verified)

2. **Row 6 Re-check**: Dated

3. **Row 7 (Teaching Artifact Stranger Run Verification)**:
   - Eighteenth artifact runs end-to-end on stranger's machine (fresh clone / Colab session)
   - Run transcript is the receipt
   - Teaching distillation (Ex-F) lands here

**Exit Criteria**: Rows 5, 6, 7 dated; artifact shipped with transcript.

---

### Session 8 (~1 h) — The Release

**Objective**: Zero UNDECIDED rows; merge; dev == main; home wired.

#### Actions

1. **ADR-0024 at Zero UNDECIDED Rows**:
   - All eight rows: LAUNCHED-with-verdict or CLOSED-with-one-reason
   - Merge green locally and on GitHub
   - `dev == main`; home wired

2. **Archive Roadmap**:
   - This roadmap's companion status retired
   - Roadmap archived with deviations as dated ledger notes

3. **Post-Record Arc Check**:
   - If post-record arc governs (it doesn't per ADR-0024), stamp eighth dated direction
   - Record's closing sentence consumed eight times, never repeated

**Exit Criteria**: The merge; the program's twentieth dated direction — or the post-record arc's eighth.

---

### The One Measured Line

ADR-0024 at **zero UNDECIDED rows** on release day (2026-09-06), with exactly one LAUNCHED research row (R1, the GPU grokking run) whose verdict re-derives from a manifest; `verify-claims` at 0 with every public number re-derivable from one command line; the hostile-webmaster walk at zero on the live shelf and on the repo's own shelf (local `main` reconciled, README current, residue removed, the debt ledger present or absent-with-date); the eighteenth teaching artifact shipped with a stranger-runnable transcript; `dev == main` and the program's twentieth dated direction.

---

## Part IV — Deep-Dive Study and Research Topics (Sessions 1–8 + Post-MP-74)

The study I will do between sessions — each reading with the paper, the one question it must answer, the prediction I write before a single number is read, and the primary source on disk.

### 1. The Dense Grokking Mechanism (The R3 Reading — The Law as a Theory)

**Question**: *What algorithm does the model actually learn when it solves modular addition without sparse Fourier structure?*

- **Primary sources**:
  - Varma et al., *Explaining grokking through circuit efficiency* (2023) — circuit efficiency as the driver
  - Lyu et al., *Understanding the training dynamics of transformers on modular arithmetic* (2024) — loss landscape structure
  - Gromov, *Grokking: A Memory Perspective* (2023) — memorization vs. generalization as compression
  - Chughtai et al., *A Toy Model of Universality* (2023) — why dense solutions might be universal attractors

- **Prediction to write before analysis**: The dense solution at P=113 implements addition via a *distributed linear map* in the embedding space, not a sparse DFT. The MLP acts as a learned interpolation table. Ablating individual neurons (not frequencies) should show graceful degradation, not catastrophic collapse.

- **Experiment**: On the existing P=113 checkpoints (seed 0, 1, 2), run neuron-level ablation sweep on `W_in`/`W_out` of the MLP. Compare degradation curve to Fourier ablation curve. (R3 in ADR-0024)

### 2. Induction Head Emergence Boundary (The R2 Reading — The Principle's Exception Map)

**Question**: *At what (width, depth, data, compute) does the induction head phase transition actually occur?*

- **Primary sources**:
  - Olsson et al., *In-context Learning and Induction Heads* (2022) — original emergence curves
  - Nanda & Jacobsen, *Attention as a Step Towards the Emergence of the Induction Head* (2023) — two-step path (duplicate head → K-composition)
  - Liu et al., *Transformers Learn Shortcuts by Default* (2023) — memorization as competing attractor

- **Prediction**: At `d_model=64, 2-layer, 4 heads, fresh-batches`, the induction head requires ≥10k epochs (not 3k). The 3000-epoch run was in the "pre-emergence" regime where Step 1 (L0 duplicate mass) is forming but Step 2 (K-composition) hasn't crossed threshold.

- **Experiment**: Extend the standard-scale run to 10k epochs with checkpointing every 500. Track Step 1 and Step 2 metrics independently (already instrumented in `diagnose_induction_formation`). (R2 in ADR-0024)

### 3. SAE Sparsity Gap on Real Activations (The R5 Reading — The Instrument as a Standard)

**Question**: *Why does the SAE achieve 99.97% FVE but only 17% sparsity (L0=136/256) on real activations vs. 97.5% FVE at 18% sparsity on synthetic?*

- **Primary sources**:
  - Bricken et al., *Towards Monosemanticity* (2023) — SAE architecture, dead features, FVE vs. L0 tradeoff
  - Cunningham et al., *Sparse Autoencoders Find Highly Interpretable Features in Language Models* (ICLR 2024) — evaluation metrics
  - Templeton et al., *Scaling Monosemanticity* (2024) — dictionary size scaling laws

- **Prediction**: The 32-dim residual stream from a small, undertrained model (150–300 epochs, no confirmed induction head) contains *no genuinely sparse features* — the SAE is learning a dense overcomplete basis because the ground truth isn't sparse yet. Once Rung 1 produces a checkpoint with real induction heads, the SAE on *that* checkpoint should show sparse features (L0 ~ 20–30).

- **Experiment**: Re-run `exp5_sae_dashboard --activations-from` on the first checkpoint that has a confirmed induction head. Compare L0/FVE tradeoff curves. (R5 in ADR-0024, gated on R2)

### 4. The Post-Record Program, Ninth Generation (New, Deepest)

**Question**: *What does the record's eighth post-record verdict open?*

- **Primary sources**: Lakatos, *The Methodology of Scientific Research Programmes* (1978) — read a tenth time, now for the *ninth* question past a completed program: progressive vs degenerating problem shifts when the *eighth* post-record verdict lands, Kuhn's normal science as the post-record arc's axioms, and the honest criterion for the ninth post-record question — a question that must earn the post-record arc's eighth *new* paragraph. This reading feeds Ex-T and the Session-0 question this phase owns more deeply than any phase before it: *what does the record's eighth post-record verdict open?* The answer can be the post-record arc's ninth dated row — Lakatos' point is that the decision is made on the record, never as a mood.

### 5. The Record Teaches, Round Nineteen

**Question**: *Can I distill the nineteenth verdict into four registers without leakage?*

The nineteenth verdict in four registers — the paper's sentence, the annex's sentence, the 30-second spoken claim, and the 5-minute teaching explanation with a worked toy a stranger can run; the gap between the last two is where my teaching leaks, and I will measure it deliberately by writing all four registers for the same verdict (Ex-F).

### 6. The Redemption Reading, or Negative Results as Maps, the Nineteenth Pass

**Question**: *How is the completed law reported honestly?*

If a sparse cell exists by S0: Nanda et al.'s full per-frequency reading on the first sparse solution this harness ever produced. If not: how the *completed* law is reported honestly — the law's domain closed with its measured boundaries and its failure cells explained or mapped, the driver a principle or a case study with a dated exception map, the drift numbers nine deep, the negative as a contribution — and how the post-record harness (if PR-22 governs) would be designed from the dated negatives instead of from hope. Either way, the paper's hardest paragraph is the one that claims the dense solution *computes something*; I will draft it against this reading and let the manifest referee it.

---

## Part V — Documentation Requirements (The Contract)

Everything this phase claims re-derives from a manifest and a command. The documentation I will write, and where:

| Artifact | Location | Trigger |
|----------|----------|---------|
| **This roadmap** (promoted from companion at Session 0) | `00_meta/75_micro-phase-75-next-phase-roadmap.md` | Session 0 |
| **ADR-0024 updates** (row verdicts, heartbeats) | `docs/adr/0024-continuum-ledger-20.md` | Each session |
| **GPU Colab Execution Protocol** (actual transcript) | `06_production_ai/notes/gpu-colab-execution-protocol.md` | Session 1, 3 |
| **Extended Induction Run Spec** (actual 10k curves) | `04_nlp_and_transformers/notes/induction-extended-run.md` | Session 2, 3 |
| **Clean-Clone Reproducibility Proof** (full transcript) | `06_production_ai/proofs/reproducible-from-clean-clone.md` | Session 4 |
| **Paper v20 Diff** or **"v19 is the record" memo** | `portfolio/paper/main.tex` v20 + diff log / memo | Session 4 |
| **Essay Annex v20** | `portfolio/essay-annex-20.md` (live shelf) | Session 5 |
| **Gate-Debt Ledger** (complete or absent-with-date) | `checklists/gate-debt.md` | Session 1, 7 |
| **Research Row Pre-registration Note** | `06_production_ai/notes/` | Session 1 |
| **Teaching Artifact v20 + Stranger Transcript** | `notebooks/teaching_artifact_v20.ipynb` + transcript | Session 6 |
| **Ex-T Execution Memo** (MP-70 arc decision consumed) | `00_meta/74_micro-phase-74-next-phase-roadmap.md` (companion) | Session 2 |
| **Progress Log** | `00_meta/03_progress-log.md` | Every session |

### Manifest Tags Required in RESULTS.md

```markdown
<!-- manifest: results/exp1_induction_heads.json -->  (extended 10k-epoch run)
<!-- manifest: results/exp2_grokking.json -->         (GPU 3-seed P=113)
<!-- manifest: results/exp3_superposition.json -->    (already solid)
<!-- manifest: results/exp4_circuit_patching.json --> (with real head if R2 opens)
<!-- manifest: results/exp5_sae_dashboard.json -->    (real activation from head checkpoint if R5 opens)
```

---

## Part VI — Practical Exercises and Hands-On Challenges

### Ex-1 · GPU Execution Drill (Session 1)

**Goal**: Execute the hardened Colab notebook for 3-seed P=113 grokking run.

```bash
# In Colab:
1. Upload notebooks/colab_grokking_full_run.ipynb
2. Runtime → Change runtime type → GPU (A100/T4)
3. Run all cells — captures 3 seeds, checkpoints every 500 epochs,
   manifests to Drive
4. Download: checkpoints/, results/exp2_grokking.json, figures/
5. Local: verify-claims passes with new manifest
```

**Falsifier**: If Colab OOMs at batch_size=512 → reduce to 256, log the change, re-run.

---

### Ex-2 · Extended Induction Run (Session 2–3)

**Goal**: Run standard-scale induction heads to 10k epochs with full diagnostics.

```bash
uv run python -m src.experiments.exp1_induction_heads \
  --standard --epochs 10000 --checkpoint-every 500 --save-model \
  --seeds 0,1,2  # multi-seed manifest
```

**Measure every 500 epochs**: Step 1 (L0 duplicate mass), Step 2 (K-composition), val accuracy, diag+1 mass. Plot the two-step trajectory.

**Falsifier**: If at 10k epochs still 0 heads → the hypothesis "fresh-batches at standard scale produces heads" is falsified. Document the boundary.

---

### Ex-3 · Neuron Ablation on Dense Grokking (Session 2, Parallel)

**Goal**: Characterize the dense solution on existing P=113 checkpoints.

```python
# In notebook or script:
for seed in [0, 1, 2]:
    ckpt = load(f"checkpoints/exp2_seed{seed}_epoch5000.pt")
    model.load_state_dict(ckpt["model"])
    # Ablate MLP neurons one by one (top-k by activation magnitude)
    # Measure accuracy drop per neuron
    # Compare to Fourier ablation curve
```

**Output**: `figures/exp2_neuron_ablation.png`, manifest entry in `exp2_grokking.json`.

---

### Ex-4 · Clean-Clone Reproducibility (Session 4)

**Goal**: Prove `uv sync && make reproduce-quick` works from zero.

```bash
cd /tmp && git clone <repo> test-clone && cd test-clone
uv sync
make reproduce-quick  # all 5 rungs in --quick mode
make verify-claims    # must pass
```

**Document**: Full transcript in `06_production_ai/proofs/reproducible-from-clean-clone.md` with timestamps.

---

### Ex-5 · SAE on First Confirmed Head Checkpoint (Session 5+, Gated)

**Goal**: Run SAE on activations from a model that *actually has* induction heads.

```bash
# Once Ex-2 produces a checkpoint with heads:
uv run python -m src.experiments.exp5_sae_dashboard \
  --activations-from figures/exp1_trained_model_seed0.pt \
  --hooks ln_final \
  --dict-size 256 --epochs 300 --seeds 0,1,2
```

**Compare**: L0/FVE tradeoff vs. synthetic baseline. Expect sparsity to improve if features are real.

---

### Ex-6 · Teaching Artifact: "From Dense Grokking to Sparse Circuits" (Session 6)

**Goal**: One runnable Colab notebook that teaches the grokking story — including the negative result.

- Cell 1: Train P=113 (or load checkpoint)
- Cell 2: Fourier analysis — show dense spectrum
- Cell 3: Ablation sweep — show graceful degradation
- Cell 4: Neuron ablation — show distributed representation
- Cell 5: Compare to Nanda et al. sparse circuit (what we *expected* vs. what we *got*)
- Cell 6: The honest conclusion: "Sometimes the model finds a different algorithm"

**Transcript**: Stranger runs it on fresh Colab session → saves output → transcript committed.

---

### Ex-7 · The Arc Consumption, Thirtieth Generation (Session 0, Verdict-Agnostic)

The consumption chain's deepest run — MP-70's Session-0 decision consumed with dates as MP-74's intake, the eighth-generation post-record verdict read from ADR-0023 row 3 if the arc governs, the criteria cited, the release that follows (the ninth post-record question, or the R1–R8 adjudication), and what each of ADR-0023's possible verdicts changes in that execution. One runnable check: the execution memo exists, names the decision rule that closes or continues the program's science, and cites the criteria from MP-70's release report — the chain now thirtieth generation deep, a session stamps, it never re-decides.

---

### Ex-8 · The Fork Drill, Deepest Form (Session 2, Verdict-Agnostic)

The continuing state (R1–R8) vs the post-record state (continuation set) written as two one-page paths — what each verdict changes downstream, including the R1-vs-R2 choice and the post-record continuation choice — so next phase's S0 decision is a stamping, not a discovery.

---

## Part VII — Strategic Tips and Architectural Best Practices

### 1. The One-Question Law, Twentieth Execution

A phase that opens two research questions is drift by another name; the unchosen candidates close in the same session as the choice — and the arc consumption may close all of them with the post-record verdict. The continuum law is the mechanical refusal of this drift — proven executable nineteen times, it must simply be executed again.

### 2. The Candidate Set Is Frozen Before S0, Never Improvised At It

R1–R8 are conditions, not predictions; a session decides, it never invents — and the terminal-state object is the hardest frozen object on the record: written by MP-40, executed by MP-41, consumed by MP-42... consumed a thirtieth time by MP-74 — never re-negotiated in the consuming session.

### 3. Consumption Is Execution

A verdict consumed into an artifact in the same session is a result; consumed into a paragraph written later it is a memory. Row 1 consumes ADR-0023's row-3 verdict in the session that owns it — or the post-record statement, if the arc governs.

### 4. The Receipt Compounds

The nineteenth runnable artifact is only worth shipping because the first eighteen transcripts proved the format — and if R5 opens, the receipts are a drift-of-drift-of-drift-of-drift-of-drift-of-drift-of-drift number measured eight times in a row, tested by people I did not choose, across an aging codebase. My showcase's story is now "read it, run it, watch me be wrong on the record," nineteen receipts deep.

### 5. The Steady State Is the Reward, Not the Ceremony

MP-74 is the twentieth roadmap written from an *executed* roadmap's release report — the program at its normal, confirmed twenty times. The cap's lesson was that promises without dates drift; the steady state's discipline is that the machinery never becomes the goal: rows are dated in the session that owns them, or they are not rows.

### 6. Stop-and-Publish Stays Open, and the Post-Record Criterion Is Now Nine Questions Deep

ADR-0004's row 5 is the honest exit; a candidate set that cannot earn a paragraph the record lacks is a phase that should close itself. If the post-record arc governs, the deepest candidate earns the post-record arc's *eighth new paragraph* — the record's closing sentence consumed nine times, never repeated. This is the deepest form of laziness: do not build what the record has already said.

### 7. Toolchains Are Pinned in S0, Never Discovered at S7

The paper's compile gate is the hardest artifact in the stack; the v20 rule ("opens only for new numbers") is the insurance that makes a missing toolchain a dated reason, not a crisis.

### 8. Protect the Release Report

The serialized stack means MP-29's release is the artifact everything downstream consumes; a slip at any link slides the whole chain. The deepest law still applies: a promise can be re-planned forever, but a dated row is answered.

### 9. The S0 Gate Is a Checklist with Receipts

ADR-0023 at zero, the live URL, `verify-claims` at 0, the eighteenth teaching transcript on disk — a condition with artifacts, not a paragraph.

### 10. The Negative Stays the Signature

The row that closes with one reason dated in the session that owns it is the strongest artifact in the repository. Every positive result in this program has a negative twin that was measured, drafted, and stamped — and the negative twin is the one that proves the positive wasn't cherry-picked. The GPU unblock is the act of finally measuring the primary flagship on its native hardware; whatever it returns, the measurement is the contribution.

### 11. Architectural Integrity Check for This Phase

The checkpointing infrastructure in `src/experiments/checkpointing.py` (shared by exp1/exp2) was battle-tested in MP-12/MP-28 and must not be touched unless a falsification test fails. The `runner.py` multi-seed aggregation and `results.py` manifest/verification machinery are the backbone — they are the contract, not the implementation.

### 12. Reproducibility as a First-Class Citizen

Every figure, every number, every claim must trace back to a manifest and a command. The `make reproduce` target is the single source of truth for "what does this repo produce?" — if it drifts, the science drifts.

### 13. Post-MP-74 Transition Planning (The Next Micro-Phase)

Upon MP-74 release (2026-09-06), the next micro-phase (MP-75/ADR-0027) will inherit:

- **If R1 produced SPARSE-FOURIER**: Sparse regime mechanism study becomes the new flagship; paper v20 writes the per-frequency reading; induction heads reprioritized as comparative baseline.
- **If R1 produced NO-GROK (current expectation)**: Dense solution characterization (R3) becomes the contribution; paper v20 writes the "dense attractor" derivation; induction heads extended to 10k epochs becomes the fallback flagship characterization.
- **Either way**: Clean-clone proof green unlocks Phase 6 gate; teaching artifact v20 ships; gate-debt ledger complete; capstone research plan execution (MP-35 Row 1) unblocks.

The next micro-phase's Session 0 will consume MP-74's release report (ADR-0024 at zero UNDECIDED) and adjudicate ADR-0027's candidate set — the thirty-first generation consumption, never improvised.

---

## Part VIII — Post-MP-74 Micro-Phase Preview (MP-75 / ADR-0027)

### Expected Intake (from MP-74 Release Report)

| Item | Expected State at 2026-09-06 |
|------|-------------------------------|
| ADR-0024 | Zero UNDECIDED rows; R1 verdict (SPARSE-FOURIER or NO-GROK) stamped |
| GPU Grokking | Manifest on disk, `verify-claims` updated |
| Extended Induction | 10k epochs complete or killed with boundary documented |
| Neuron Ablation | Figure + manifest entry on disk |
| Clean-Clone Proof | Transcript on disk, Phase 6 gate GREEN |
| SAE on Head Checkpoint | Executed (if R2 produced head) or closed with reason |
| Teaching Artifact v20 | Shipped with stranger transcript |
| Paper v20 / Annex v20 | Diff + scaffold or "v19 is the record" memo |
| Gate-Debt Ledger | Complete or absent-with-date |

### MP-75 Candidate Set Preview (Frozen at MP-75 Session 0)

| Row | Candidate | Opens Only If |
|-----|-----------|---------------|
| 1 | **Capstone Research Plan Execution** | Clean-clone proof green (Phase 6 gate) |
| 2 | **Paper Prose from Manifests** | Paper v20 diff exists (new numbers from MP-74) |
| 3 | **W&B Integration + Dashboard** | Always (Phase 6 residue) |
| 4 | **Hugging Face Spaces SAE Browser Deploy** | R5 executed with confirmed head |
| 5 | **Portfolio Project Write-ups** | Figures exist for all 5 rungs |
| 6 | **Pages Deploy Workflow** | Paper v20 compiles |
| 7 | **Final Integration & Release** | Rows 1–6 complete |
| 8 | **Gate-Debt Closure** | All MP-30–MP-36 resolved |

### Terminus

Release = merge + 14 calendar days from MP-75 Session 0 (target: 2026-09-20).

---

**Written**: 2026-08-25  
**Perspective**: Personal study notes / learning log / portfolio showcase  
**Status**: Ready for Session 1 execution — candidate set frozen, conditions explicit, no improvisation. The GPU unblock is the act of finally measuring the primary flagship on its native hardware; whatever it returns, the measurement is the contribution.