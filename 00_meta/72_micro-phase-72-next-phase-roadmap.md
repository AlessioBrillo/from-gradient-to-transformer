---
tags: [type/moc, phase/6, phase/7, research/experiment, state/roadmap]
created: 2026-08-22
---

# Micro-Phase 72 — Next Micro-Phase Roadmap: The GPU Unblock Executes, The Cascade Begins

> **STATUS: EXECUTION-READY ROADMAP.** This note is my step-by-step plan for the micro-phase that starts after MP-71's Session 8 release. It is written from the reviewer's chair in the same first-person register as my progress log so it doubles as the public record of how I reason about the program's steady state *before* the work begins. Everything factual in this file was re-verified against the repository on 2026-08-22: working tree clean, `origin/main` at `ea90829` (PR #104's squash of MP-68's review and roadmap), `origin/dev` at `2e74577` (the reconcile merge), `git diff origin/main origin.dev` empty, 189 tests collected, ruff clean, blocking mypy clean on `src/results.py` + `src/experiments/runner.py`, `verify-claims` at 0, all five manifests on disk. The three hard blockers from MP-70/71's roadmap (GPU access for P=113, induction heads at scale, clean-clone proof) are the *only* research questions this phase opens — no improvisation at Session 0.

---

## Showcase Framing — How This Document Reads in Public

This is not an internal memo. It is a dated, first-person artifact of how a research program reasons about its own steady state: what is verified, what is honestly still open, and what the next step is — before that step runs. Anyone reading the repository in sequence (MP-37 through this file) can watch the same discipline recur: facts re-verified sitting by sitting, a ledger that stamps rows or closes them with one named reason, negatives shipped as loudly as positives, and one deep question chosen per phase. If you take one thing from this phase's chapter, take the measured line in Part III: **the record ships its 41st dated direction or the phase does not release.**

---

## Part I — Where I Stand (State Review, Re-Verified 2026-08-22)

### The Scientific Ledger

The record's deepest fact has not changed and still carries every dated confirmation the record holds: **no run in this repository's history has ever produced a sparse Fourier solution.** The count advances only with a new verdict; between MP-71's drafting and this one, no new Fourier cell landed — the microscope's trials 2 (`--schedule constant`) and 3 (wd 1.5×) remain pending in ADR-0003's budget.

- **P=59 drills dense 59/59**; **P=113's three-seed verdict is NO-GROK** (val 1.0, k_99 = 111/113); the positive-control scan stamped **ALL-DENSE** at P=59/67/97.
- **Microscope trial 1 FALSIFIED** (embedding re-normalization is not the suppressor: k_99 = 112/113, val 0.7176); trials 2 and 3 pending in ADR-0003's budget.
- **R1 standard-scale ×3-seed run COMPLETED 2026-08-14** with the scheduled no-head negative as its verdict (0/8 heads, peak diag+1 mass 0.075 at epoch 499, peak val accuracy 0.5083 near epoch 1950, K-composition max 0.056). This remains the newest dated fact on the record's negative side.
- All five manifests are on disk (`results/exp1…exp5`), and `verify-claims` is at **0** — re-verified live in this drafting sitting.

The arc my science has taken is the strongest thing I own: *will grokking reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what is the dense solution's structure?* (MP-29 S3's characterization) → *which open question is deepest?* (MP-36) → the question chain from MP-37 through MP-67 → *which of C145–C148 does the consumed thirty-sixth verdict open?* (MP-68) → *the GPU unblock that the previous twenty-three could not execute locally* (MP-69/70) → **MP-71 executes that unblock** → **MP-72 consumes MP-71's verdict and opens the cascade**.

### The Stack at Intake

- **MP-29** is current and mid-execution (terminus ≈ 2026-08-26).
- **MP-30 through MP-36** stand pre-registered, gated in series, the cap at seven. Each phase's Session 0 consumes the previous phase's release report: no release, no phase.
- **ADR-0042** = MP-68's ledger (eight rows); **ADR-0043** = MP-69's ledger (eight rows); **ADR-0023** = MP-70's ledger (eight rows); **ADR-0024** = MP-71's ledger (eight rows, to be filled MP-71's cycle).
- This phase's ledger will be **ADR-0025** (the twenty-first continuum ledger, written from MP-71's release report).

### The CI Floor and Toolchains

189 tracked tests, ruff, blocking mypy, and markdownlint are green at the last release; `verify-claims` at 0. The verified gaps, stated as facts not hopes:

- No LaTeX toolchain on this machine (`make paper` is graceful, not green)
- No Pages deploy workflow in `.github/workflows/`
- No `publish:` frontmatter policy
- `portfolio/projects/` holds figures but no project write-ups
- W&B never connected

Each is a dated row owned by MP-30–MP-36 — their residue, never my re-planning.

### The Three Hard Blockers (From MP-71, Frozen as This Phase's Intake)

| Blocker | Status | What Must Happen |
|---------|--------|------------------|
| **GPU Access** — P=113 grokking flagship never run on GPU | Colab notebook hardened, MP-71 Session 1 launched | MP-71 Session 3 downloads checkpoints/manifests; this phase ingests them |
| **Induction Heads at Scale** — 0/8 heads at 3k epochs standard scale | MP-71 Session 2 launched 10k-epoch ×3 seeds | MP-71 Session 3-4 monitors; this phase consumes verdict at Session 0 |
| **Clean-Clone Proof** — Phase 6 gate not green | MP-71 Session 4 executes protocol | MP-71 Session 4 produces transcript; this phase re-verifies at Session 0 |

---

## Part II — The Bottleneck Analysis (What I Must Not Let Drift)

### 1. The Consumption Chain Is Now Thirty Generations Deep

MP-40's Ex-N defined the terminal state; MP-41's Session 0 executed it; MP-42's Session 0 consumed that execution and chose; ... MP-71's Session 0 consumed MP-70's Session-0 decision with dates. **This phase's Session 0 must consume MP-71's Session-0 decision with dates** — the single most dangerous drift is re-litigating a thirty-times-consumed decision. The decision chain is now thirty generations deep; a sitting stamps, it never re-decides.

### 2. The Stacked Execution Remains the Critical Path

This phase's Session 0 consumes MP-71's release report, which consumes ADR-0024's, which awaits MP-29 through MP-40. A slip at any link slides the whole chain; **my highest-leverage act is unchanged: protect MP-29's window** — its release report is the artifact everything downstream consumes. Nothing in this phase may borrow a minute from it.

### 3. The Science's Next Fork Is The GPU Verdict — This Phase Consumes It

MP-71's eight candidates (R1–R8) are this phase's frozen intake. They are conditions, not predictions; a sitting decides, it never invents. **R1 (GPU Grokking) and R2 (Extended Induction) are already running** by MP-71 Session 3; this phase's Session 0 ingests their verdicts.

### 4. The Steady State Must Not Become Ceremony

This will be the twenty-second roadmap written from an *executed* roadmap's release report — the program's normal, confirmed twenty-two times. The drift risk inverts and deepens: the machinery (ledgers, sessions, gate criteria) is now twenty-one executions deep, so the law's countermeasure is that rows must still be dated in the sitting that owns them, verdicts still consumed as artifacts, and zero UNDECIDED rows at Session 8.

### 5. The Cascade Opens Three Rungs Simultaneously

If R1 produces **sparse Fourier** (the universal override): Rung 2 becomes the primary flagship with Nanda-style per-frequency reading; Rung 1 reprioritized to characterize the difference between this run and the NO-GROK runs; Rung 5 (SAE) gates on R2's confirmed head.

If R1 produces **dense Fourier** (the expected path per MP-29's positive-control scan): Rung 2's dense-solution characterization (R3 neuron ablation) becomes the primary contribution; Rung 1's 10k-epoch verdict determines whether Rung 5 runs on real or synthetic activations; Rung 4 (circuit patching) gates on Rung 1's confirmed head.

### 6. The Paper's Compile Gate Remains the Hardest Artifact

No TeX on this machine — verified again in this sitting; MP-31's own canon applies early: *toolchains are pinned in Session 0, never discovered at Session 7.* The paper v21 rule ("opens only for new numbers, else v20 is the record") is my insurance.

### 7. The Showcase's Receipts Are Still Future, One Deeper

The nineteenth stranger-run transcript lands only if the lanes execute; C67 (the rate as a policy) is conditioned on ≥ 19 transcripts on disk at Session 0 — the receipt compounds only if the lanes execute.

---

## Part III — The Roadmap, Step by Step (Continuum Law, Twenty-First Execution)

### The Frozen Candidate Set (Inherited from MP-71, Consumed at Session 0)

| # | Candidate | Opens Only If | Why It Would Close |
|---|-----------|---------------|-------------------|
| R1 | **GPU Grokking 3-Seed P=113 VERDICT INTAKE** — download checkpoints, `results/exp2_grokking.json`, `figures/exp2_*.png` from Colab; verify manifest against RESULTS.md tags (`verify-claims` at 0) | MP-71 Session 3 completes | Colab run failed → document failure, proceed to R3 dense-characterization |
| R2 | **Extended Induction 10k Epochs VERDICT INTAKE** — check 2k/4k/6k/8k/10k checkpoints for Step 1 formation (L0 duplicate mass) and Step 2 (K-composition); finalize manifest | MP-71 Session 3-4 completes | If 10k epochs still 0 heads → hypothesis "fresh-batches at standard scale produces heads" falsified; document boundary |
| R3 | **Neuron Ablation on Dense Grokking** — on existing P=113 checkpoints (seed 0,1,2), ablate MLP neurons by activation magnitude; compare degradation to Fourier ablation | GPU run completes (uses existing checkpoints) | If neuron ablation also shows graceful degradation → dense solution is distributed linear map, not sparse DFT |
| R4 | **Clean-Clone Reproducibility Re-verification** — re-run MP-71 Session 4's clean-clone protocol on this phase's commit; full transcript to `06_production_ai/proofs/reproducible-from-clean-clone.md` | Always (Phase 6 gate) | If fails → fix blocking issue, re-run; transcript required for release |
| R5 | **SAE on Confirmed-Head Checkpoint** — `--activations-from <head_checkpoint> --hooks ln_final --dict-size 256 --epochs 300 --seeds 0,1,2` | Rung 1 produces confirmed induction head (R2 verdict at Session 0) | If no head by R2 verdict → SAE stays on synthetic only; document the dependency |
| R6 | **Teaching Artifact v21: "From Dense Grokking to Sparse Circuits — The Verdict"** — updated Colab notebook with MP-71's actual GPU verdict, ablation results, and honest conclusion | Always (showcase lane) | If no GPU run → use existing CPU checkpoints; the artifact teaches the *negative result* |
| R7 | **Paper v21 / Annex v21** — if R1/R2/R3/R5 produce new numbers → paper v21 diff + annex v21; else "v20 is the record" dated memo | New numbers from R1, R2, R3, or R5 | If no new numbers → v21 is a dated memo, not a compilation crisis |
| R8 | **Gate-Debt Re-verification** — re-verify all MP-30–MP-36 row closures with transcripts; `gate-debt.md` complete or absent-with-date | All MP-30–MP-36 rows | Session 1 (initial), re-verified Session 7 |

**Universal Override**: If GPU run (R1) produces **sparse Fourier** (k₉₉ < P/2 sustained ≥3 checkpoints) → R1 becomes the sparse-regime mechanism study (Nanda-style per-frequency reading), R2/R5 reprioritized to characterize the difference between this run and the NO-GROK runs.

**Post-Record Override**: If MP-71's Session 0 continued the post-record arc → R1 becomes "Post-Record Harness Design from Dated Negatives", R2 becomes "Eighth Post-Record Question", etc. — but MP-71 has not yet consumed MP-70's decision, so this roadmap assumes the pre-record arc.

### The Nine Sessions

#### Session 0 (~1 h) — The Gate Truthing + The Thirty-First-Generation Arc + The Continuum Choice

- Consume MP-71's release report row by row: ADR-0024 at zero UNDECIDED rows, the live URL re-clicked, `verify-claims` at actual count, the nineteenth teaching transcript on disk, `dev == main`.
- Commit the intake table before a single continuum row opens.
- **Ex-T: Consume MP-71's Session-0 decision with dates** — the thirty-first-generation consumption: if the post-record arc continued, the ninth post-record question's verdict is read from ADR-0024 row 3 and the tenth post-record question chosen from the pre-registered continuation set; if not, the R1–R8 adjudication: exactly one opens as row 3, the unchosen close with one dated reason each, stamped in the same sitting.
- Open ADR-0025 with its eight rows, windows and kill-dates; declare the terminus (release = merge + 14 calendar days); promote this roadmap from MP-71's release report, deviations recorded as dated ledger notes.
- **Exit**: intake signed; the thirty-first-generation arc stamped; row 3 chosen (or the post-record continuation row opened); ledger open.

#### Session 1 (~2 h) — The GPU Verdict Ingestion + The Shelf Baseline + The Debt Re-verification

- **Ingest R1 (GPU Grokking Verdict)**: download checkpoints, `results/exp2_grokking.json`, `figures/exp2_*.png` from Colab Drive. Verify manifest against RESULTS.md tags (`verify-claims` at 0). Log Fourier sparsity (k_99), generalization epoch per seed, val accuracy curve.
- Row 5: hostile-webmaster walk of the live site + Space at zero (links, assets, a11y, orphans) — extended to the repo's own shelf: local `main` re-verified reconciled to `origin/main`, `portfolio/README.md`'s staleness verified closed, the exp6 residue removed with a transcript, the annexes' location verified.
- Row 8: MP-71's stamped closures re-verified (W&B, clean-clone proof, graduation proof, `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch resolution, the README fix, the residue removal) — each cell LAUNCHED-with-transcript or CLOSED-with-one-reason; a claimed closure without its transcript stays open and blocks Session 8; `gate-debt.md`'s absence, if still absent, recorded with a date.
- **Exit**: R1 manifest on disk; `verify-claims` updated; rows 5 and 8 stamped.

#### Session 2 (~2 h) — The Extended Induction Verdict Ingestion + GPU Run Characterization

- **Ingest R2 (Extended Induction Verdict)**: final checkpoint at 10k epochs. Compute final val accuracy, total induction heads, peak diag+1 mass, K-composition score, mean ablation drop. Update `results/exp1_induction_heads.json` manifest.
- **Launch R3 (Neuron Ablation)** on GPU run checkpoints (or CPU checkpoints if R1 failed) — scripted, produces `figures/exp2_neuron_ablation.png`.
- **Exit**: R2 manifest on disk; R3 complete or running; `verify-claims` updated.

#### Session 3 (~2 h) — The Dense-Solution Characterization + SAE Protocol Decision

- **Complete R3 (Neuron Ablation)**: compare degradation curve to Fourier ablation curve. Log: does ablating individual neurons show graceful degradation (distributed map) or catastrophic collapse (sparse DFT)?
- **R5 Decision Gate**: based on R2 verdict, write R5 protocol (SAE on head checkpoint) with site, metric, negative control, kill-date, OR close R5 with one dated reason ("no confirmed head").
- **Exit**: R3 manifest entry in `exp2_grokking.json`; R5 protocol written or closed with reason.

#### Session 4 (~2 h) — Clean-Clone Re-verification + Paper v21 Decision

- Execute clean-clone protocol: fresh clone → `uv sync` → `make reproduce-quick` → `make verify-claims`.
- Full transcript to `06_production_ai/proofs/reproducible-from-clean-clone.md`.
- Paper v21 decision: if R1/R2/R3/R5 produced new numbers → paper v21 diff + annex v21 scaffold; else "v20 is the record" memo.
- **Exit**: clean-clone transcript; paper decision dated.

#### Session 5 (~2 h) — Essay Annex v21 + SAE Execution (If Gated Open)

- `portfolio/essay-annex-21.md` (on live shelf, dated): R1/R2/R3 verdict set distilled into one dated annex; reverse claims audit at zero (prose → manifest → command).
- If R5 open: execute SAE on first confirmed head checkpoint. Compare L0/FVE tradeoff vs. synthetic baseline.
- **Exit**: annex drafted; R5 complete or running.

#### Session 6 (~3 h) — The Teaching Artifact v21 + Stranger Run

- Build R6 (Teaching Artifact v21 Colab notebook) with MP-71's actual GPU verdict.
- Execute on fresh Colab session as stranger — full transcript saved.
- Compare against previous artifact's transcript (Ex-M).
- **Exit**: artifact shipped with transcript; Ex-F distillation complete.

#### Session 7 (~2 h) — The Shelf Rehearsal + The Re-check Row + The Teaching Polish

- Row 5: hostile-webmaster walk at zero beside the browser, every public number clicked back to disk; the repo-shelf findings re-checked (local `main` reconciled, README current, residue gone, annexes' home verified).
- Row 6's re-check row dated.
- Row 7: the nineteenth artifact runs end to end on a stranger's machine (fresh clone / Colab session); the run transcript is the receipt; the teaching distillation (Ex-F) lands here.
- **Exit**: rows 5, 6, 7 dated; the artifact shipped with its transcript.

#### Session 8 (~1 h) — The Release

- ADR-0025 at zero UNDECIDED rows; the merge green locally and on GitHub; `dev == main`; home wired — this roadmap's companion status retired; the roadmap archived with its deviations, every deviation a dated ledger note.
- If the post-record arc governs, this sitting stamps the post-record arc's ninth dated direction — the record's closing sentence consumed nine times, never repeated.
- **Exit**: the merge; the program's twenty-first dated direction — or the post-record arc's ninth.

### The One Measured Line

ADR-0025 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED research row (R1, the GPU grokking verdict) whose verdict re-derives from a manifest; `verify-claims` at 0 with every public number re-derivable from one command line; the hostile-webmaster walk at zero on the live shelf and on the repo's own shelf (local `main` reconciled, README current, residue removed, the debt ledger present or absent-with-date); the nineteenth teaching artifact shipped with a stranger-runnable transcript; `dev == main` and the program's twenty-first dated direction — or, if the post-record arc governs, its ninth dated direction.

---

## Part IV — Deep-Dive Study and Research Topics

The study I will do between now and the verdict sitting — each reading with the paper, the one question it must answer, the prediction I write before a single number is read, and the primary source on disk.

### 1. The Dense Grokking Mechanism (the R3 Reading — the Law as a Theory)

**Question**: *What algorithm does the model actually learn when it solves modular addition without sparse Fourier structure?*

- **Primary sources**:
  - Varma et al., *Explaining grokking through circuit efficiency* (2023) — circuit efficiency as the driver
  - Lyu et al., *Understanding the training dynamics of transformers on modular arithmetic* (2024) — loss landscape structure
  - Gromov, *Grokking: A Memory Perspective* (2023) — memorization vs. generalization as compression
  - Chughtai et al., *A Toy Model of Universality* (2023) — why dense solutions might be universal attractors

- **Prediction to write before analysis**: The dense solution at P=113 implements addition via a *distributed linear map* in the embedding space, not a sparse DFT. The MLP acts as a learned interpolation table. Ablating individual neurons (not frequencies) should show graceful degradation, not catastrophic collapse.

- **Experiment**: On the existing P=113 checkpoints (seed 0,1,2), run neuron-level ablation sweep on `W_in`/`W_out` of the MLP. Compare degradation curve to Fourier ablation curve.

### 2. Induction Head Emergence Boundary (the R2 Reading — the Principle's Exception Map)

**Question**: *At what (width, depth, data, compute) does the induction head phase transition actually occur?*

- **Primary sources**:
  - Olsson et al., *In-context Learning and Induction Heads* (2022) — original emergence curves
  - Nanda & Jacobsen, *Attention as a Step Towards the Emergence of the Induction Head* (2023) — two-step path (duplicate head → K-composition)
  - Liu et al., *Transformers Learn Shortcuts by Default* (2023) — memorization as competing attractor

- **Prediction**: At `d_model=64, 2-layer, 4 heads, fresh-batches`, the induction head requires ≥10k epochs (not 3k). The 3000-epoch run was in the "pre-emergence" regime where Step 1 (L0 duplicate mass) is forming but Step 2 (K-composition) hasn't crossed threshold.

- **Experiment**: Already running in MP-71. This phase ingests the verdict and plots the two-step trajectory.

### 3. SAE Sparsity Gap on Real Activations (the R5 Reading — the Instrument as a Standard)

**Question**: *Why does the SAE achieve 99.97% FVE but only 17% sparsity (L0=136/256) on real activations vs. 97.5% FVE at 18% sparsity on synthetic?*

- **Primary sources**:
  - Bricken et al., *Towards Monosemanticity* (2023) — SAE architecture, dead features, FVE vs. L0 tradeoff
  - Cunningham et al., *Sparse Autoencoders Find Highly Interpretable Features in Language Models* (ICLR 2024) — evaluation metrics
  - Templeton et al., *Scaling Monosemanticity* (2024) — dictionary size scaling laws

- **Prediction**: The 32-dim residual stream from a small, undertrained model (150-300 epochs, no confirmed induction head) contains *no genuinely sparse features* — the SAE is learning a dense overcomplete basis because the ground truth isn't sparse yet. Once Rung 1 produces a checkpoint with real induction heads, the SAE on *that* checkpoint should show sparse features (L0 ~ 20-30).

- **Experiment**: Re-run `exp5_sae_dashboard --activations-from` on the first checkpoint that has a confirmed induction head. Compare L0/FVE tradeoff curves.

### 4. The Post-Record Program, Tenth Generation (New, Deepest)

**Question**: *What does the record's ninth post-record verdict open?*

- **Primary sources**: Lakatos, *The Methodology of Scientific Research Programmes* (1978) — read an eleventh time, now for the *tenth* question past a completed program: progressive vs degenerating problem shifts when the *ninth* post-record verdict lands, Kuhn's normal science as the post-record arc's axioms, and the honest criterion for the tenth post-record question — a question that must earn the post-record arc's ninth *new* paragraph. This reading feeds Ex-T and the Session-0 question this phase owns more deeply than any phase before it: *what does the record's ninth post-record verdict open?* The answer can be the post-record arc's tenth dated row — Lakatos' point is that the decision is made on the record, never as a mood.

### 5. The Record Teaches, Round Twenty

**Question**: *Can I distill the twentieth verdict into four registers without leakage?*

The twentieth verdict in four registers — the paper's sentence, the annex's sentence, the 30-second spoken claim, and the 5-minute teaching explanation with a worked toy a stranger can run; the gap between the last two is where my teaching leaks, and I will measure it deliberately by writing all four registers for the same verdict (Ex-F).

### 6. The Redemption Reading, or Negative Results as Maps, the Twentieth Pass

**Question**: *How is the completed law reported honestly?*

If a sparse cell exists by S0: Nanda et al.'s full per-frequency reading on the first sparse solution this harness ever produced. If not: how the *completed* law is reported honestly — the law's domain closed with its measured boundaries and its failure cells explained or mapped, the driver a principle or a case study with a dated exception map, the drift numbers ten deep, the negative as a contribution — and how the post-record harness (if PR-22 governs) would be designed from the dated negatives instead of from hope. Either way, the paper's hardest paragraph is the one that claims the dense solution *computes something*; I will draft it against this reading and let the manifest referee it.

---

## Part V — Documentation Requirements (The Contract)

Everything this phase claims re-derives from a manifest and a command. The documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0, rewritten from MP-71's release report, deviations recorded as dated ledger notes.
- **ADR-0025**, the twenty-first continuum ledger — eight rows pre-stamped with windows and kill-dates; rows 1–2 consumed from ADR-0024's verdicts; row 3 the twenty-first research question with its protocol note and heartbeat (or the post-record continuation row's protocol); rows 4–8 the continuum's decisions.
- **GPU Colab Execution Protocol** — `06_production_ai/notes/gpu-colab-execution-protocol.md` updated with actual run transcript.
- **Extended Induction Run Spec** — `04_nlp_and_transformers/notes/induction-extended-run.md` updated with actual 10k-epoch curves.
- **Clean-Clone Reproducibility Proof** — `06_production_ai/proofs/reproducible-from-clean-clone.md` updated with actual transcript and timestamps.
- **Paper v21 Diff** — `portfolio/paper/main.tex` v21 + diff log or the dated "v20 is the record" memo; `make paper` re-verified in the CI mirror.
- **Essay Annex v21** — `portfolio/essay-annex-21.md` (on live shelf) manifest-tagged, amended never rewritten; the annexes' home (the live shelf) recorded with a date.
- **Gate-Debt Ledger** — `checklists/gate-debt.md` — each cell's transcript or one-line reason, dated in Session 1, including the exp5 1000-epoch resolution's receipt re-checked; the file's absence, if still absent, recorded with a date.
- **Research Row's Pre-registration Note** — in `06_production_ai/notes/` + the heartbeat artifact; if R1: the law-theory figure spec written before the analysis, the figure itself manifest-tagged after. If the post-record arc governs: the continuation row's protocol note instead.
- **The Twentieth Teaching Artifact + its Stranger-Run Transcript** — (fresh-clone or Colab session receipt).
- **Ex-T's Execution Memo** — MP-71's arc decision run with dates: the post-record verdict consumed or the R1–R8 adjudication executed, the criteria cited, the decision that follows (the tenth post-record question, or the continuation), written verdict-agnostic in Session 2 and executed at Session 0.
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at release; the continuum ledger's rows cited by the skill tree's publication flips.

### Manifest Tags Required in RESULTS.md

```markdown
<!-- manifest: results/exp1_induction_heads.json -->  (extended 10k-epoch run)
<!-- manifest: results/exp2_grokking.json -->         (GPU 3-seed P=113)
<!-- manifest: results/exp3_superposition.json -->    (already solid)
<!-- manifest: results/exp4_circuit_patching.json --> (with real head)
<!-- manifest: results/exp5_sae_dashboard.json -->    (real activation from head checkpoint)
```

---

## Part VI — Practical Exercises and Hands-On Challenges

### Ex-1 · GPU Verdict Ingestion Drill (Session 1)

**Goal**: Download and verify the GPU run artifacts from Colab.

```bash
# In Colab (already run in MP-71):
1. Check notebooks/colab_grokking_full_run.ipynb completed 3 seeds × 5000 epochs
2. Download: checkpoints/, results/exp2_grokking.json, figures/
3. Local:
   uv run python -m src.results verify  # must pass
   # Verify k_99_percent, generalization_epoch per seed
```

**Falsifier**: If Colab run failed (OOM, timeout, disconnection) → document failure with error message, proceed to R3 on CPU checkpoints.

### Ex-2 · Extended Induction Verdict Ingestion (Session 2)

**Goal**: Finalize the 10k-epoch induction run manifest.

```bash
# Check 10k epoch checkpoint exists
ls checkpoints/exp1_seed*_epoch10000.pt

# Compute final metrics
uv run python -c "
from src.experiments.exp1_induction_heads import *
# load model, run analyze_induction_heads, diagnose_induction_formation
# compute ablation drops
# update results/exp1_induction_heads.json
"
```

**Measure at every 500 epochs (already logged)**: Step 1 (L0 duplicate mass), Step 2 (K-composition), val accuracy, diag+1 mass. Plot the two-step trajectory.

**Falsifier**: If at 10k epochs still 0 heads → the hypothesis "fresh-batches at standard scale produces heads" is falsified. Document the boundary in ADR-0025 row 2.

### Ex-3 · Neuron Ablation on Dense Grokking (Session 2–3)

**Goal**: Characterize the dense solution on P=113 checkpoints.

```python
# In notebook or script:
for seed in [0, 1, 2]:
    ckpt = load(f"checkpoints/exp2_seed{seed}_epoch5000.pt")
    model.load_state_dict(ckpt["model"])
    # Ablate MLP neurons one by one (top-k by activation magnitude)
    # Measure accuracy drop per neuron
    # Compare to Fourier ablation curve (already in exp2_grokking.json)
```

**Output**: `figures/exp2_neuron_ablation.png`, manifest entry in `exp2_grokking.json`.

**Success Criterion**: If neuron ablation shows graceful degradation (no single neuron critical) while Fourier ablation shows catastrophic collapse → dense solution is distributed linear map, not sparse DFT.

### Ex-4 · Clean-Clone Reproducibility (Session 4)

**Goal**: Prove `uv sync && make reproduce-quick` works from zero.

```bash
cd /tmp && git clone <repo> test-clone && cd test-clone
uv sync
make reproduce-quick  # all 5 rungs in --quick mode
make verify-claims    # must pass
```

**Document**: Full transcript in `06_production_ai/proofs/reproducible-from-clean-clone.md` with timestamps.

### Ex-5 · SAE on First Confirmed Head Checkpoint (Session 5, Gated)

**Goal**: Run SAE on activations from a model that *actually has* induction heads.

```bash
# Once Ex-2 produces a checkpoint with heads:
uv run python -m src.experiments.exp5_sae_dashboard \
  --activations-from figures/exp1_trained_model_seed0.pt \
  --hooks ln_final \
  --dict-size 256 --epochs 300 --seeds 0,1,2
```

**Compare**: L0/FVE tradeoff vs. synthetic baseline. Expect sparsity to improve if features are real.

### Ex-6 · Teaching Artifact: "From Dense Grokking to Sparse Circuits — The Verdict" (Session 6)

**Goal**: One runnable Colab notebook that teaches the grokking story — including the actual GPU verdict.

- Cell 1: Train P=113 (or load checkpoint from GPU run)
- Cell 2: Fourier analysis — show dense/sparse spectrum per actual verdict
- Cell 3: Ablation sweep — show graceful/catastrophic degradation per actual verdict
- Cell 4: Neuron ablation — show distributed representation
- Cell 5: Compare to Nanda et al. sparse circuit (what we *expected* vs. what we *got*)
- Cell 6: The honest conclusion: "Sometimes the model finds a different algorithm" OR "The sparse Fourier circuit is universal and here is its per-frequency reading"

**Transcript**: Stranger runs it on fresh Colab session → saves output → transcript committed.

### Ex-7 · The Arc Consumption, Thirty-First Generation (Session 0, New, Verdict-Agnostic)

The consumption chain's deepest run — MP-71's Session-0 decision consumed with dates as MP-72's intake, the ninth-generation post-record verdict read from ADR-0024 row 3 if the arc governs, the criteria cited, the release that follows (the tenth post-record question, or the R1–R8 adjudication), and what each of ADR-0024's possible verdicts changes in that execution. One runnable check: the execution memo exists, names the decision rule that closes or continues the program's science, and cites the criteria from MP-71's release report — the chain now thirty-one generations deep, a sitting stamps, it never re-decides.

### Ex-8 · The Fork Drill, Deepest Form (Session 2, Verdict-Agnostic)

The continuing state (R1–R8) vs the post-record state (continuation set) written as two one-page paths — what each verdict changes downstream, including the R1-vs-R2 choice and the post-record continuation choice — so next phase's S0 decision is a stamping, not a discovery.

---

## Part VII — Strategic Tips and Architectural Best Practices

- **The one-question law, twenty-first execution.** A phase that opens two research questions is drift by another name; the unchosen candidates close in the same sitting as the choice — and the arc consumption may close all of them with the post-record verdict. The continuum law is the mechanical refusal of this drift — proven executable twenty times, it must simply be executed again.

- **The candidate set is frozen before S0, never improvised at it.** R1–R8 are conditions, not predictions; a sitting decides, it never invents — and the terminal-state object is the hardest frozen object on the record: written by MP-40, executed by MP-41, consumed by MP-42, consumed again by MP-43, consumed a third time by MP-44, consumed a fourth time by MP-45, consumed a fifth time by MP-46, consumed a sixth time by MP-47, consumed a seventh time by MP-48, consumed an eighth time by MP-49, consumed a ninth time by MP-50, consumed a tenth time by MP-51, consumed an eleventh time by MP-52, consumed a twelfth time by MP-53, consumed a thirteenth time by MP-54, consumed a fourteenth time by MP-55, consumed a fifteenth time by MP-56, consumed a sixteenth time by MP-57, consumed a seventeenth time by MP-58, consumed an eighteenth time by MP-59, consumed a nineteenth time by MP-60, consumed a twentieth time by MP-61, consumed a twenty-first time by MP-62, consumed a twenty-second time by MP-63, consumed a twenty-third time by MP-64, consumed a twenty-fourth time by MP-65, consumed a twenty-fifth time by MP-66, consumed a twenty-sixth time by MP-67, consumed a twenty-seventh time by MP-68, consumed a twenty-eighth time by MP-69, consumed a twenty-ninth time by MP-70, consumed a thirtieth time by MP-71, **consumed a thirty-first time by MP-72** — never re-negotiated in the consuming sitting.

- **Consumption is execution.** A verdict consumed into an artifact in the same sitting is a result; consumed into a paragraph written later it is a memory. Row 1 consumes ADR-0024's row-3 verdict in the sitting that owns it — or the post-record statement, if the arc governs.

- **The receipt compounds.** The twentieth runnable artifact is only worth shipping because the first nineteen transcripts proved the format — and if R5 opens, the receipts are a drift-of-drift-of-drift-of-drift-of-drift-of-drift-of-drift-of-drift number measured nine times in a row, tested by people I did not choose, across an aging codebase. My showcase's story is now "read it, run it, watch me be wrong on the record," twenty receipts deep.

- **The steady state is the reward, not the ceremony.** MP-72 is the twenty-second roadmap written from an *executed* roadmap's release report — the program at its normal, confirmed twenty-two times. The cap's lesson was that promises without dates drift; the steady state's discipline is that the machinery never becomes the goal: rows are dated in the sitting that owns them, or they are not rows.

- **Stop-and-publish stays open, and the post-record criterion is now ten questions deep.** ADR-0004's row 5 is the honest exit; a candidate set that cannot earn a paragraph the record lacks is a phase that should close itself. If the post-record arc governs, the deepest candidate earns the post-record arc's *ninth new paragraph* — the record's closing sentence consumed ten times, never repeated. This is the deepest form of laziness: do not build what the record has already said.

- **Toolchains are pinned in S0, never discovered at S7.** The paper's compile gate is the hardest artifact in the stack; the v21 rule ("opens only for new numbers") is the insurance that makes a missing toolchain a dated reason, not a crisis.

- **Protect the release report.** The serialized stack means MP-29's release is the artifact everything downstream consumes; a slip at any link slides the whole chain. The deepest law still applies: a promise can be re-planned forever, but a dated row is answered.

- **The S0 gate is a checklist with receipts.** ADR-0024 at zero, the live URL, `verify-claims` at 0, the nineteenth teaching transcript on disk — a condition with artifacts, not a paragraph.

- **The negative stays the signature.** The row that closes with one reason dated in the sitting that owns it is the strongest artifact in the repository. Every positive result in this program has a negative twin that was measured, drafted, and stamped — and the negative twin is the one that proves the positive wasn't cherry-picked. The GPU unblock is the act of finally measuring the primary flagship on its native hardware; whatever it returns, the measurement is the contribution.

- **Architectural integrity check for this phase:** The checkpointing infrastructure in `src/experiments/checkpointing.py` (shared by exp1/exp2) was battle-tested in MP-12/MP-28 and must not be touched unless a falsification test fails. The `runner.py` multi-seed aggregation and `results.py` manifest/verification machinery are the backbone — they are the contract, not the implementation.

- **Reproducibility as a first-class citizen:** Every figure, every number, every claim must trace back to a manifest and a command. The `make reproduce` target is the single source of truth for "what does this repo produce?" — if it drifts, the science drifts.

- **The cascade architecture:** This phase is where the experiment ladder's dependency graph becomes real. Rung 1's 10k-epoch verdict gates Rung 4 (circuit patching) and Rung 5 (SAE). Rung 2's GPU verdict gates Rung 3 (neuron ablation characterization) and determines whether the flagship is sparse or dense. The phase's Session 0 *ingests* these verdicts; Session 1-3 *acts* on them. The roadmap is the dependency graph made executable.

---

**Written**: 2026-08-22  
**Perspective**: Personal study notes / learning log / portfolio showcase  
**Status**: Ready for Session 0 consumption — candidate set frozen, conditions explicit, no improvisation at S0. The GPU unblock has executed in MP-71; this phase ingests its verdict and opens the cascade.