---
tags: [type/moc, phase/6, phase/7, research/experiment, state/roadmap]
created: 2026-08-23
---

# Micro-Phase 73 — Next Micro-Phase Roadmap: The Cascade Executes

> **STATUS: PLAN MODE** — This document is the pre-registered roadmap for MP-73, written from the reviewer's chair before the work begins. It consumes MP-72's release report (which itself consumes MP-71's verdicts) and opens the three-rung cascade: Grokking characterization (R3), Induction head scale verification (R2→R4/R5), and SAE on real heads (R5). No improvisation at Session 0.

---

## Showcase Framing — How This Document Reads in Public

This is the twenty-third roadmap written from an *executed* roadmap's release report.
Anyone reading the repository in sequence (MP-37 through this file) watches the same
discipline recur: facts re-verified sitting by sitting, a ledger that stamps rows or
closes them with one named reason, negatives shipped as loudly as positives, and one
deep question chosen per phase. The measured line in Part III is: **ADR-0026 at zero
UNDECIDED rows on release day, with the cascade's first real results manifest-tagged
and the paper's compile gate pinned at Session 0.**

---

## Part I — Where I Stand (State Review, Re-Verified at MP-73 Drafting)

### The Scientific Ledger

The record's deepest fact remains unchanged: **no run in this repository's history has ever produced a sparse Fourier solution.**

- **P=59 drills dense 59/59**; **P=113's three-seed verdict is NO-GROK** (val 1.0, k_99 = 111/113); positive-control scan stamped **ALL-DENSE** at P=59/67/97.
- **Microscope trial 1 FALSIFIED** (embedding re-normalization is not the suppressor: k_99 = 112/113, val 0.7176); trials 2 (`--schedule constant`) and 3 (weight decay 1.5×) pending in ADR-0003's budget.
- **R1 standard-scale ×3-seed run COMPLETED** (0/8 heads, peak diag+1 mass 0.075 at epoch 499, peak val accuracy 0.5083 near epoch 1950, K-composition max 0.056). This remains the newest dated fact on the record's negative side.
- All five manifests on disk (`results/exp1…exp5`), `verify-claims` at **0**.

The arc: *will grokking reproduce?* (MP-28) → *is the harness the suppressor?* (MP-29) → *dense solution structure?* (MP-29 S3) → *which open question deepest?* (MP-36) → question chain MP-37→MP-67 → *which of C145–C148 opens?* (MP-68) → *GPU unblock* (MP-69/70) → **MP-71 executes unblock** → **MP-72 consumes verdicts and opens cascade** → **MP-73 executes the cascade**.

### The Stack at Intake (Inherited from MP-72)

- **MP-29** terminus ≈ 2026-08-26 (mid-execution, the control for dense solution structure)
- **MP-30 through MP-36** pre-registered, gated in series, cap at seven
- **ADR-0025** = MP-72's ledger (to be filled MP-72's cycle)
- This phase's ledger will be **ADR-0026** (twenty-second continuum ledger)

### The CI Floor and Toolchains

189 tracked tests, ruff, blocking mypy (`src/results.py` + `src/experiments/runner.py`), markdownlint green; `verify-claims` at 0. Verified gaps (owned by MP-30–MP-36):
- No LaTeX toolchain (`make paper` graceful, not green)
- No Pages deploy workflow
- No `publish:` frontmatter policy
- `portfolio/projects/` holds figures but no project write-ups
- W&B never connected

### The Three Hard Blockers — MP-72 Session 0 Consumption

| Blocker | MP-72 Status | MP-73 Inheritance |
|---------|--------------|-------------------|
| **GPU Access** — P=113 grokking flagship | MP-71 Colab launched; MP-72 Session 1 ingests verdict | MP-73 Session 0 ingests MP-72's ingestion; R3 (neuron ablation) executes on GPU checkpoints |
| **Induction Heads at Scale** — 10k epochs ×3 seeds | MP-71 Session 2 launched; MP-72 Session 2 ingests verdict | MP-73 Session 0 ingests; if heads confirmed → R4 (circuit patching) + R5 (SAE) gate open |
| **Clean-Clone Proof** | MP-71 Session 4 executes; MP-72 Session 4 re-verifies | MP-73 Session 0 re-verifies; must be green for release |

---

## Part II — The Bottleneck Analysis (What I Must Not Let Drift)

### 1. The Consumption Chain Is Now Thirty-One Generations Deep

MP-40's Ex-N defined terminal state; MP-41 executed; MP-42 consumed... MP-72 consumed MP-71. **MP-73 Session 0 must consume MP-72's Session-0 decision with dates** — the single most dangerous drift is re-litigating a thirty-one-times-consumed decision. The decision chain is now thirty-one generations deep; a sitting stamps, it never re-decides.

### 2. The Stacked Execution Remains the Critical Path

MP-73 Session 0 consumes MP-72's release report → consumes ADR-0025 → awaits MP-29 through MP-40. **My highest-leverage act: protect MP-29's window** — its release report is the artifact everything downstream consumes. Nothing in MP-73 may borrow a minute from it.

### 3. The Cascade Opens Three Rungs Simultaneously — This Phase Executes Them

MP-72's Session 0 adjudicates R1–R8; MP-73's Session 0 consumes those verdicts. The cascade architecture:

- **If R1 (GPU Grokking) = sparse Fourier** (universal override): Rung 2 becomes primary flagship with Nanda-style per-frequency reading; Rung 1 reprioritized to characterize difference from NO-GROK runs; Rung 5 gates on R2's confirmed head.
- **If R1 = dense Fourier** (expected per MP-29 positive-control): Rung 2's dense-solution characterization (R3 neuron ablation) becomes primary contribution; Rung 1's 10k-epoch verdict determines whether Rung 5 runs on real or synthetic activations; Rung 4 (circuit patching) gates on Rung 1's confirmed head.

### 4. The Steady State Must Not Become Ceremony

Twenty-third roadmap from executed roadmap's release report — the program at its normal. The machinery (ledgers, sessions, gate criteria) is now twenty-two executions deep; countermeasure: rows must still be dated in the sitting that owns them, verdicts consumed as artifacts, zero UNDECIDED rows at Session 8.

### 5. The Paper's Compile Gate Remains the Hardest Artifact

No TeX on this machine — verified again. MP-31's canon applies: *toolchains pinned in Session 0, never discovered at Session 7.* Paper v22 rule ("opens only for new numbers, else v21 is the record") is my insurance.

### 6. The Showcase's Receipts Compound

The twentieth stranger-run transcript lands only if lanes execute; the receipt compounds only if the lanes execute. MP-73's teaching artifact must ship with transcript.

---

## Part III — The Roadmap, Step by Step (Continuum Law, Twenty-Second Execution)

### The Frozen Candidate Set (Inherited from MP-72, Consumed at Session 0)

| # | Candidate | Opens Only If | Why It Would Close |
|---|-----------|---------------|-------------------|
| R1 | **GPU Grokking Verdict Execution** — R3 (neuron ablation) on GPU checkpoints; compare degradation to Fourier ablation | MP-72 R1 verdict ingested | If GPU run failed → R3 on CPU checkpoints (already exist) |
| R2 | **Extended Induction Verdict Execution** — if heads confirmed at 10k epochs: R4 (circuit patching on real head) + R5 (SAE on head checkpoint) | MP-72 R2 verdict ingested | If 0 heads at 10k → hypothesis falsified; document boundary; R4/R5 stay on synthetic |
| R3 | **Neuron Ablation Characterization** — scripted sweep on P=113 checkpoints (seeds 0,1,2); output `figures/exp2_neuron_ablation.png`, manifest entry | GPU run completes (uses existing checkpoints) | If neuron ablation also graceful → dense solution is distributed linear map, not sparse DFT |
| R4 | **Circuit Patching on Confirmed Head** — `--seeds 0,1,2` on checkpoint with verified induction head; activation + path patching + head ablation | R2 produces confirmed induction head | If no head → path patching remains unit-tested only; document dependency |
| R5 | **SAE on Confirmed-Head Checkpoint** --activations-from <head_ckpt> --hooks ln_final --dict-size 256 --epochs 300 --seeds 0,1,2 | R2 produces confirmed head | If no head → SAE stays on synthetic; document the gap honestly |
| R6 | **Teaching Artifact v22: "From Dense Grokking to Sparse Circuits — The Cascade Verdict"** — updated Colab with MP-72's actual GPU verdict, R3 neuron ablation, R2 10k verdict | Always (showcase lane) | If no GPU run → use CPU checkpoints; artifact teaches the *negative result* |
| R7 | **Paper v22 / Annex v22** — if R1/R2/R3/R4/R5 produce new numbers → paper v22 diff + annex v22; else "v21 is the record" dated memo | New numbers from R1–R5 | If no new numbers → v22 is dated memo, not compilation crisis |
| R8 | **Gate-Debt Final Verification** — re-verify all MP-30–MP-36 row closures; `gate-debt.md` complete or absent-with-date | All MP-30–MP-36 rows | Session 1 (initial), re-verified Session 7 |

**Universal Override**: If GPU run (R1) produces **sparse Fourier** (k₉₉ < P/2 sustained ≥3 checkpoints) → R1 becomes sparse-regime mechanism study, R2/R5 reprioritized.

**Post-Record Override**: If MP-72's Session 0 continued post-record arc → R1 becomes "Post-Record Harness Design from Dated Negatives", etc. — but MP-72 assumes pre-record arc.

### The Nine Sessions

#### Session 0 (~1 h) — The Gate Truthing + The Thirty-Second-Generation Arc
- Consume MP-72's release report row by row: ADR-0025 at zero UNDECIDED, live URL re-clicked, `verify-claims` at actual count, twentieth teaching transcript on disk, `dev == main`
- Commit intake table before any continuum row opens
- **Ex-T: Consume MP-72's Session-0 decision with dates** — thirty-second-generation consumption: if post-record arc continued, tenth post-record question's verdict read from ADR-0025 row 3; if not, R1–R8 adjudication: exactly one opens as row 3, unchosen close with one dated reason each
- Open ADR-0026 with eight rows, windows, kill-dates; declare terminus (release = merge + 14 calendar days); promote this roadmap from MP-72's release report
- **Exit**: intake signed; thirty-second-generation arc stamped; row 3 chosen; ledger open

#### Session 1 (~2 h) — The GPU Verdict Execution (R1→R3)
- Ingest MP-72's R1 GPU verdict (already on disk from MP-72 Session 1)
- Execute R3: neuron ablation on GPU checkpoints (seeds 0,1,2)
  - Ablate MLP neurons by activation magnitude (top-k)
  - Compare degradation curve to Fourier ablation curve
  - Output: `figures/exp2_neuron_ablation.png`, manifest entry in `exp2_grokking.json`
- Row 8: MP-72's stamped closures re-verified (W&B, clean-clone proof, graduation proof, reproduce-multiseed exp2/exp5, exp5 1000-epoch resolution, README fix, residue removal) — each LAUNCHED-with-transcript or CLOSED-with-one-reason
- **Exit**: R3 manifest entry; rows 8 stamped; `verify-claims` updated

#### Session 2 (~2 h) — The Extended Induction Verdict Execution (R2→R4/R5)
- Ingest MP-72's R2 10k-epoch verdict (from MP-72 Session 2)
- If heads confirmed: launch R4 (circuit patching) + R5 (SAE) on head checkpoint
  - R4: `exp4_circuit_patching --activations-from <head_ckpt> --seeds 0,1,2`
  - R5: `exp5_sae_dashboard --activations-from <head_ckpt> --hooks ln_final --dict-size 256 --epochs 300 --seeds 0,1,2`
- If 0 heads: document boundary in ADR-0026 row 2; R4/R5 remain synthetic
- **Exit**: R4/R5 running or closed with reason; `verify-claims` updated

#### Session 3 (~2 h) — The Dense-Solution Characterization + SAE Comparison
- Complete R3 analysis: does neuron ablation show graceful degradation (distributed map) or catastrophic collapse (sparse DFT)?
- If R5 running: compare L0/FVE tradeoff on real head activations vs. synthetic baseline vs. undertrained real activations (from MP-72)
- **Exit**: R3 complete; R5 comparison entry; R5 protocol written or closed

#### Session 4 (~2 h) — Clean-Clone Re-verification + Paper v22 Decision
- Execute clean-clone protocol: fresh clone → `uv sync` → `make reproduce-quick` → `make verify-claims`
- Full transcript to `06_production_ai/proofs/reproducible-from-clean-clone.md`
- Paper v22 decision: if R1–R5 produced new numbers → paper v22 diff + annex v22 scaffold; else "v21 is the record" memo
- **Exit**: clean-clone transcript; paper decision dated

#### Session 5 (~2 h) — Essay Annex v22 + SAE Completion (If Gated)
- `portfolio/essay-annex-22.md`: R1/R2/R3/R4/R5 verdict set distilled into one dated annex; reverse claims audit at zero
- If R5 open: complete SAE run; compare L0/FVE vs. synthetic baseline
- **Exit**: annex drafted; R5 complete

#### Session 6 (~3 h) — The Teaching Artifact v22 + Stranger Run
- Build R6 (Teaching Artifact v22 Colab notebook) with MP-72's actual GPU verdict, R3 neuron ablation, R2 10k verdict
- Execute on fresh Colab session as stranger — full transcript saved
- Compare against previous artifact's transcript
- **Exit**: artifact shipped with transcript; Ex-F distillation complete

#### Session 7 (~2 h) — The Shelf Rehearsal + The Re-check Row
- Row 5: hostile-webmaster walk at zero beside browser; repo-shelf findings re-checked
- Row 6's re-check row dated
- Row 7: twentieth artifact runs end-to-end on stranger's machine; transcript is receipt
- **Exit**: rows 5, 6, 7 dated; artifact shipped with transcript

#### Session 8 (~1 h) — The Release
- ADR-0026 at zero UNDECIDED rows; merge green locally and on GitHub; `dev == main`; home wired
- If post-record arc governs: this sitting stamps post-record arc's tenth dated direction
- **Exit**: the merge; program's twenty-second dated direction — or post-record arc's tenth

### The One Measured Line

ADR-0026 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row whose verdict re-derives from a manifest; `verify-claims` at 0 with
every public number re-derivable from one command line; hostile-webmaster walk at
zero on live shelf and repo shelf; twentieth teaching artifact shipped with
stranger-runnable transcript; `dev == main` and program's twenty-second dated
direction — or post-record arc's tenth.

---

## Part IV — Deep-Dive Study and Research Topics

### 1. The Dense Grokking Mechanism as a Distributed Linear Map (the R3 Reading)

**Question**: *What algorithm does the model actually learn when it solves modular addition without sparse Fourier structure?*

- **Primary sources**:
  - Varma et al., *Explaining grokking through circuit efficiency* (2023) — circuit efficiency as driver
  - Lyu et al., *Understanding the training dynamics of transformers on modular arithmetic* (2024) — loss landscape structure
  - Gromov, *Grokking: A Memory Perspective* (2023) — memorization vs. generalization as compression
  - Chughtai et al., *A Toy Model of Universality* (2023) — why dense solutions might be universal attractors

- **Prediction to write before analysis**: The dense solution at P=113 implements addition via a *distributed linear map* in the embedding space, not a sparse DFT. The MLP acts as a learned interpolation table. Ablating individual neurons should show graceful degradation, not catastrophic collapse.

- **Experiment**: On existing P=113 checkpoints (seed 0,1,2), run neuron-level ablation sweep on `W_in`/`W_out` of MLP. Compare degradation curve to Fourier ablation curve.

### 2. Induction Head Emergence Boundary at Scale (the R2 Reading)

**Question**: *At what (width, depth, data, compute) does the induction head phase transition actually occur?*

- **Primary sources**:
  - Olsson et al., *In-context Learning and Induction Heads* (2022) — original emergence curves
  - Nanda & Jacobsen, *Attention as a Step Towards the Emergence of the Induction Head* (2023) — two-step path
  - Liu et al., *Transformers Learn Shortcuts by Default* (2023) — memorization as competing attractor

- **Prediction**: At `d_model=64, 2-layer, 4 heads, fresh-batches`, induction head requires ≥10k epochs (not 3k). The 3000-epoch run was in "pre-emergence" regime where Step 1 (L0 duplicate mass) forms but Step 2 (K-composition) hasn't crossed threshold.

- **Experiment**: MP-72 Session 2 ingests the 10k-epoch verdict; MP-73 plots the two-step trajectory across checkpoints (2k/4k/6k/8k/10k).

### 3. SAE Sparsity Gap on Real Activations with Confirmed Heads (the R5 Reading)

**Question**: *Why does SAE achieve 99.97% FVE but only 17% sparsity (L0=136/256) on undertrained real activations vs. 97.5% FVE at 18% sparsity on synthetic? What changes with a confirmed induction head checkpoint?*

- **Primary sources**:
  - Bricken et al., *Towards Monosemanticity* (2023) — SAE architecture, dead features, FVE vs. L0 tradeoff
  - Cunningham et al., *Sparse Autoencoders Find Highly Interpretable Features in Language Models* (ICLR 2024) — evaluation metrics
  - Templeton et al., *Scaling Monosemanticity* (2024) — dictionary size scaling laws

- **Prediction**: The 32-dim residual stream from a small, undertrained model (150-300 epochs, no confirmed induction head) contains *no genuinely sparse features* — SAE learns dense overcomplete basis because ground truth isn't sparse yet. Once Rung 1 produces a checkpoint with real induction heads, SAE on *that* checkpoint should show sparse features (L0 ~ 20-30).

- **Experiment**: Re-run `exp5_sae_dashboard --activations-from` on first checkpoint with confirmed induction head. Compare L0/FVE tradeoff curves.

### 4. The Post-Record Program, Tenth Generation (New, Deepest)

**Question**: *What does the record's ninth post-record verdict open?*

- **Primary sources**: Lakatos, *The Methodology of Scientific Research Programmes*
  (1978) — read eleventh time, now for the *tenth* question past a completed
  program: progressive vs degenerating problem shifts when the *ninth* post-record
  verdict lands; Kuhn's normal science as post-record arc's axioms; honest
  criterion for the tenth post-record question — a question that must earn the
  post-record arc's ninth *new* paragraph.

### 5. The Record Teaches, Round Twenty-One

**Question**: *Can I distill the twenty-first verdict into four registers without leakage?*

The twenty-first verdict in four registers — paper's sentence, annex's sentence, 30-second spoken claim, 5-minute teaching explanation with worked toy a stranger can run; the gap between the last two is where my teaching leaks, measured deliberately by writing all four registers for the same verdict (Ex-F).

### 6. The Redemption Reading, or Negative Results as Maps, Twenty-First Pass

**Question**: *How is the completed law reported honestly?*

If sparse cell exists by S0: Nanda et al.'s full per-frequency reading on first
sparse solution this harness ever produced. If not: how the *completed* law is
reported honestly — domain closed with measured boundaries, failure cells
explained/mapped, driver a principle or case study with dated exception map,
drift numbers ten deep, negative as contribution — and how the post-record
harness (if PR-22 governs) would be designed from dated negatives instead of
hope. Either way, the paper's hardest paragraph claims the dense solution
*computes something*; I will draft it against this reading and let the manifest
referee it.

---

## Part V — Documentation Requirements (The Contract)

Everything this phase claims re-derives from a manifest and a command. Documentation I will write, and where:

- **This roadmap**, promoted from companion review at Session 0, rewritten from MP-72's release report, deviations recorded as dated ledger notes
- **ADR-0026**, the twenty-second continuum ledger — eight rows pre-stamped with windows/kill-dates; rows 1–2 consumed from ADR-0025's verdicts; row 3 the twenty-second research question with protocol note and heartbeat (or post-record continuation row's protocol); rows 4–8 the continuum's decisions
- **GPU Colab Execution Protocol** — `06_production_ai/notes/gpu-colab-execution-protocol.md` updated with actual run transcript
- **Extended Induction Run Spec** — `04_nlp_and_transformers/notes/induction-extended-run.md` updated with actual 10k-epoch curves
- **Neuron Ablation Characterization** — `06_production_ai/notes/dense-grokking-neuron-ablation.md` (new)
- **Circuit Patching on Real Head** — `04_nlp_and_transformers/notes/circuit-patching-real-head.md` (new, if R2 opens)
- **SAE on Real Head Checkpoint** — `05_llm_engineering/notes/sae-on-real-head.md` (new, if R2 opens)
- **Clean-Clone Reproducibility Proof** — `06_production_ai/proofs/reproducible-from-clean-clone.md` updated with actual transcript
- **Paper v22 Diff** — `portfolio/paper/main.tex` v22 + diff log or "v21 is the record" memo; `make paper` re-verified in CI mirror
- **Essay Annex v22** — `portfolio/essay-annex-22.md` (on live shelf), manifest-tagged, amended never rewritten; annexes' home recorded with date
- **Gate-Debt Ledger** — `checklists/gate-debt.md` — each cell's transcript or one-line reason, dated in Session 1; file's absence recorded with date if still absent
- **Research Row's Pre-registration Note** — in `06_production_ai/notes/` — heartbeat artifact; if R1: law-theory figure spec written before analysis, figure itself manifest-tagged after; if post-record: continuation row's protocol note instead
- **The Twenty-First Teaching Artifact + its Stranger-Run Transcript** — (fresh-clone or Colab session receipt)
- **Ex-T's Execution Memo** — MP-72's arc decision run with dates: post-record verdict consumed or R1–R8 adjudication executed, criteria cited, decision that follows, written verdict-agnostic in Session 2 and executed at Session 0
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at release; continuum ledger's rows cited by skill tree's publication flips

### Manifest Tags Required in RESULTS.md

```markdown
<!-- manifest: results/exp1_induction_heads.json -->  (extended 10k-epoch run, if heads)
<!-- manifest: results/exp2_grokking.json -->         (GPU 3-seed P=113 + neuron ablation)
<!-- manifest: results/exp3_superposition.json -->    (already solid)
<!-- manifest: results/exp4_circuit_patching.json --> (with real head, if R2 opens)
<!-- manifest: results/exp5_sae_dashboard.json -->    (real activation from head checkpoint, if R2 opens)
```

---

## Part VI — Practical Exercises and Hands-On Challenges

### Ex-1 · GPU Verdict Execution: Neuron Ablation Drill (Session 1)

**Goal**: Characterize the dense solution on P=113 GPU checkpoints.

```bash
# GPU checkpoints already downloaded from MP-72 Session 1
ls checkpoints/exp2_seed*_epoch5000.pt

# Neuron ablation script
uv run python -c "
from src.experiments.exp2_grokking import *
# For each seed 0,1,2:
#   load checkpoint
#   ablate MLP neurons by |W_out[:,i]| (top-k)
#   measure val accuracy drop per neuron
#   compare to Fourier ablation curve (already in manifest)
# save figures/exp2_neuron_ablation.png
# append to results/exp2_grokking.json
"
```

**Output**: `figures/exp2_neuron_ablation.png`, manifest entry in `exp2_grokking.json`

**Success Criterion**: If neuron ablation shows graceful degradation (no single neuron critical) while Fourier ablation shows catastrophic collapse → dense solution is distributed linear map, not sparse DFT.

**Falsifier**: If neuron ablation *also* shows catastrophic collapse at specific neurons → dense solution may have sparse structure after all; investigate which neurons.

### Ex-2 · Extended Induction Verdict Execution (Session 2)

**Goal**: Finalize 10k-epoch induction run; gate R4/R5.

```bash
# Check 10k epoch checkpoint exists
ls checkpoints/exp1_seed*_epoch10000.pt

# Compute final metrics
uv run python -c "
from src.experiments.exp1_induction_heads import *
# load model from 10k checkpoint
# run analyze_induction_heads, diagnose_induction_formation
# compute ablation drops
# update results/exp1_induction_heads.json
"

# Measure at every 500 epochs (already logged): Step 1 (L0 duplicate mass), 
# Step 2 (K-composition), val accuracy, diag+1 mass. Plot two-step trajectory.
```

**Falsifier**: If at 10k epochs still 0 heads → hypothesis "fresh-batches at standard scale produces heads" falsified. Document boundary in ADR-0026 row 2.

### Ex-3 · Circuit Patching on Confirmed Head (Session 2, Gated)

**Goal**: Validate path patching end-to-end on a real induction head.

```bash
# Once Ex-2 produces checkpoint with heads:
uv run python -m src.experiments.exp4_circuit_patching \
  --activations-from figures/exp1_trained_model_seed0_epoch10000.pt \
  --seeds 0,1,2
```

**Output**: `portfolio/figures/exp4_patching_results_real.png`, manifest entry in `exp4_circuit_patching.json`

**Validation**: Path patching's self-patch-is-zero test already passes; this validates against a *real* head for the first time.

### Ex-4 · SAE on First Confirmed Head Checkpoint (Session 2–3, Gated)

**Goal**: Run SAE on activations from a model that *actually has* induction heads.

```bash
# Once Ex-2 produces checkpoint with heads:
uv run python -m src.experiments.exp5_sae_dashboard \
  --activations-from figures/exp1_trained_model_seed0_epoch10000.pt \
  --hooks ln_final \
  --dict-size 256 --epochs 300 --seeds 0,1,2
```

**Compare**: L0/FVE tradeoff vs. synthetic baseline vs. undertrained real activations (MP-72). Expect sparsity to improve if features are real.

### Ex-5 · Clean-Clone Reproducibility (Session 4)

**Goal**: Prove `uv sync && make reproduce-quick` works from zero.

```bash
cd /tmp && git clone <repo> test-clone && cd test-clone
uv sync
make reproduce-quick  # all 5 rungs in --quick mode
make verify-claims    # must pass
```

**Document**: Full transcript in `06_production_ai/proofs/reproducible-from-clean-clone.md` with timestamps.

### Ex-6 · Teaching Artifact: "From Dense Grokking to Sparse Circuits — The Cascade Verdict" (Session 6)

**Goal**: One runnable Colab notebook that teaches the grokking story — including the actual GPU verdict, neuron ablation, and 10k-epoch induction verdict.

- Cell 1: Train P=113 (or load checkpoint from GPU run)
- Cell 2: Fourier analysis — show dense/sparse spectrum per actual verdict
- Cell 3: Ablation sweep — show graceful/catastrophic degradation per actual verdict
- Cell 4: Neuron ablation — show distributed representation
- Cell 5: Induction head emergence — 10k-epoch trajectory, two-step path
- Cell 6: SAE on real head (if R2 opens) — L0/FVE comparison
- Cell 7: The honest conclusion: "The model found a different algorithm" OR "The sparse Fourier circuit is universal and here is its per-frequency reading"

**Transcript**: Stranger runs it on fresh Colab session → saves output → transcript committed.

### Ex-7 · The Arc Consumption, Thirty-Second Generation (Session 0, Verdict-Agnostic)

The consumption chain's deepest run — MP-72's Session-0 decision consumed
with dates as MP-73's intake, the ninth-generation post-record verdict read from
ADR-0025 row 3 if arc governs, criteria cited, release that follows (tenth
post-record question or R1–R8 adjudication), and what each of ADR-0025's
possible verdicts changes in that execution. One runnable check: execution memo
exists, names the decision rule that closes or continues the program's science,
cites criteria from MP-72's release report — chain now thirty-two generations
deep, a sitting stamps, it never re-decides.

### Ex-8 · The Fork Drill, Deepest Form (Session 2, Verdict-Agnostic)

The continuing state (R1–R8) vs post-record state (continuation set) written as two one-page paths — what each verdict changes downstream, including R1-vs-R2 choice and post-record continuation choice — so next phase's S0 decision is a stamping, not a discovery.

---

## Part VII — Strategic Tips and Architectural Best Practices

- **The one-question law, twenty-second execution.** A phase that opens two research questions is drift; unchosen candidates close in the same sitting as the choice — and the arc consumption may close all of them with the post-record verdict. The continuum law is the mechanical refusal of this drift — proven executable twenty-one times, it must simply be executed again.

- **The candidate set is frozen before S0, never improvised at it.** R1–R8 are
  conditions, not predictions; a sitting decides, it never invents — and the
  terminal-state object is the hardest frozen object on the record: written by
  MP-40, executed by MP-41, consumed by MP-42, consumed again by MP-43...
  consumed a thirty-first time by MP-72, **consumed a thirty-second time by
  MP-73** — never re-negotiated in the consuming sitting.

- **Consumption is execution.** A verdict consumed into an artifact in the same
  sitting is a result; consumed into a paragraph written later it is a memory.
  Row 1 consumes ADR-0025's row-3 verdict in the sitting that owns it — or the
  post-record statement, if the arc governs.

- **The receipt compounds.** The twenty-first runnable artifact is only worth
  shipping because the first twenty transcripts proved the format — and if R5
  opens, the receipts are a drift-of-drift... number measured nine times in a
  row, tested by people I did not choose, across an aging codebase. My
  showcase's story is now "read it, run it, watch me be wrong on the record,"
  twenty-one receipts deep.

- **The steady state is the reward, not the ceremony.** MP-73 is the twenty-third roadmap from an *executed* roadmap's release report — the program at its normal, confirmed twenty-three times. The cap's lesson: promises without dates drift; steady state's discipline: rows dated in the sitting that owns them, or they are not rows.

- **Stop-and-publish stays open, and the post-record criterion is now eleven
  questions deep.** ADR-0004's row 5 is the honest exit; a candidate set that
  cannot earn a paragraph the record lacks is a phase that should close itself.
  If post-record arc governs, the deepest candidate earns the post-record arc's
  *tenth new paragraph* — record's closing sentence consumed eleven times,
  never repeated. This is the deepest form of laziness: do not build what the
  record has already said.

- **Toolchains are pinned in S0, never discovered at S7.** The paper's compile gate is the hardest artifact; the v22 rule ("opens only for new numbers") is the insurance that makes a missing toolchain a dated reason, not a crisis.

- **Protect the release report.** The serialized stack means MP-29's release is
  the artifact everything downstream consumes; a slip at any link slides the
  whole chain. The deepest law still applies: a promise can be re-planned
  forever, but a dated row is answered.

- **The S0 gate is a checklist with receipts.** ADR-0025 at zero, live URL,
  `verify-claims` at 0, twentieth teaching transcript on disk — a condition
  with artifacts, not a paragraph.

- **The negative stays the signature.** The row that closes with one reason dated
  in the sitting that owns it is the strongest artifact in the repository. Every
  positive result has a negative twin that was measured, drafted, and stamped —
  the negative twin proves the positive wasn't cherry-picked. The GPU unblock is
  the act of finally measuring the primary flagship on its native hardware;
  whatever it returns, the measurement is the contribution.

- **Architectural integrity check for this phase:** The checkpointing
  infrastructure in `src/experiments/checkpointing.py` (shared by exp1/exp2) was
  battle-tested in MP-12/MP-28 and must not be touched unless a falsification
  test fails. The `runner.py` multi-seed aggregation and `results.py`
  manifest/verification machinery are the backbone — they are the contract, not
  the implementation.

- **Reproducibility as a first-class citizen:** Every figure, every number,
  every claim must trace back to a manifest and a command. The `make reproduce`
  target is the single source of truth for "what does this repo produce?" — if
  it drifts, the science drifts.

- **The cascade architecture:** This phase is where the experiment ladder's
  dependency graph becomes real. Rung 1's 10k-epoch verdict gates Rung 4
  (circuit patching) and Rung 5 (SAE). Rung 2's GPU verdict gates Rung 3
  (neuron ablation characterization) and determines whether the flagship is
  sparse or dense. The phase's Session 0 *ingests* these verdicts; Session
  1-3 *acts* on them. The roadmap is the dependency graph made executable.

---

**Written**: 2026-08-23  
**Perspective**: Personal study notes / learning log / portfolio showcase  
**Status**: Plan complete — ready for Session 0 consumption when MP-72 releases. Candidate set frozen, conditions explicit, no improvisation at S0. The cascade executes in MP-73.