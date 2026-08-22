---
tags: [type/moc, phase/6, phase/7, research/experiment, state/roadmap]
created: 2026-08-22
---

# Micro-Phase 71 — Next Micro-Phase Roadmap: Executing the GPU Unblock and Cascade

> **STATUS: EXECUTION-READY ROADMAP.** This note is my step-by-step plan for the micro-phase
> that starts after MP-70's Session 8 release. It is written from the reviewer's chair in the
> same first-person register as my progress log so it doubles as the public record of how I
> reason about the program's steady state *before* the work begins. Everything factual in this
> file was re-verified against the repository on 2026-08-22: working tree clean,
> `origin/main` at `ea90829` (PR #104's squash of MP-68's review and roadmap),
> `origin/dev` at `2e74577` (the reconcile merge), `git diff origin/main origin.dev` empty,
> 189 tests collected, ruff clean, blocking mypy clean on `src/results.py` +
> `src/experiments/runner.py`, `verify-claims` at 0, all five manifests on disk. The three
> hard blockers from MP-70's roadmap (GPU access for P=113, induction heads at scale,
> clean-clone proof) are the *only* research questions this phase opens — no improvisation
> at Session 0.

---

## Showcase Framing — How This Document Reads in Public

This is not an internal memo. It is a dated, first-person artifact of how a research program
reasons about its own steady state: what is verified, what is honestly still open, and what the
next step is — before that step runs. Anyone reading the repository in sequence (MP-37 through
this file) can watch the same discipline recur: facts re-verified sitting by sitting, a ledger
that stamps rows or closes them with one named reason, negatives shipped as loudly as positives,
and one deep question chosen per phase. If you take one thing from this phase's chapter, take
the measured line in Part III: **the record ships its 40th dated direction or the phase does not
release.**

---

## Part I — Where I Stand (State Review, Re-Verified 2026-08-22)

### The Scientific Ledger

The record's deepest fact has not changed and still carries every dated confirmation the record
holds: **no run in this repository's history has ever produced a sparse Fourier solution.** The
count advances only with a new verdict; between MP-70's drafting and this one, no new Fourier
cell landed — the microscope's trials 2 (`--schedule constant`) and 3 (wd 1.5×) remain pending
in ADR-0003's budget.

- **P=59 drills dense 59/59**; **P=113's three-seed verdict is NO-GROK** (val 1.0, k_99 = 111/113); the positive-control scan stamped **ALL-DENSE** at P=59/67/97.
- **Microscope trial 1 FALSIFIED** (embedding re-normalization is not the suppressor: k_99 = 112/113, val 0.7176); trials 2 and 3 pending in ADR-0003's budget.
- **R1 standard-scale ×3-seed run COMPLETED 2026-08-14** with the scheduled no-head negative
as its verdict (0/8 heads, peak diag+1 mass 0.075 at epoch 499, peak val accuracy 0.5083
near epoch 1950, K-composition max 0.056). This remains the newest dated fact on the
record's negative side.
- All five manifests are on disk (`results/exp1…exp5`), and `verify-claims` is at **0** — re-verified live in this drafting sitting.

The arc my science has taken is the strongest thing I own: *will grokking reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what is the dense solution's structure?* (MP-29 S3's characterization) → *which open question is deepest?* (MP-36) → the question chain from MP-37 through MP-67 → *which of C145–C148 does the consumed thirty-sixth verdict open?* (MP-68) → *the GPU unblock that the previous twenty-three could not execute locally* (MP-69/70). **This phase executes that unblock.**

### The Stack at Intake

- **MP-29** is current and mid-execution (terminus ≈ 2026-08-26).
- **MP-30 through MP-36** stand pre-registered, gated in series, the cap at seven. Each phase's Session 0 consumes the previous phase's release report: no release, no phase.
- **ADR-0042** = MP-68's ledger (eight rows); **ADR-0043** = MP-69's ledger (eight rows); **ADR-0023** = MP-70's ledger (eight rows, to be filled this cycle).
- This phase's ledger will be **ADR-0024** (the twentieth continuum ledger, written from MP-70's release report).

### The CI Floor and Toolchains

189 tracked tests, ruff, blocking mypy, and markdownlint are green at the last release;
`verify-claims` at 0. The verified gaps, stated as facts not hopes:
- No LaTeX toolchain on this machine (`make paper` is graceful, not green)
- No Pages deploy workflow in `.github/workflows/`
- No `publish:` frontmatter policy
- `portfolio/projects/` holds figures but no project write-ups
- W&B never connected

Each is a dated row owned by MP-30–MP-36 — their residue, never my re-planning.

### The Three Hard Blockers (From MP-70, Frozen as This Phase's Intake)

| Blocker | Status | What Must Happen |
|---------|--------|------------------|
| **GPU Access** — P=113 grokking flagship never run on GPU | Colab notebook hardened, unexecuted | Execute 3-seed P=113 on Colab A100/T4; checkpoint every 500 epochs; manifest to Drive |
| **Induction Heads at Scale** — 0/8 heads at 3k epochs standard scale | Fresh-batches run completed 2026-08-14 | Extend to 10k epochs ×3 seeds with checkpointing every 500; track Step 1/Step 2 independently |
| **Clean-Clone Proof** — Phase 6 gate not green | `reproducible-from-clean-clone.md` proof exists but unexecuted | Fresh clone → `uv sync` → `make reproduce-quick` → `make verify-claims`; full transcript |

---

## Part II — The Bottleneck Analysis (What I Must Not Let Drift)

### 1. The Consumption Chain Is Now Twenty-Nine Generations Deep

MP-40's Ex-N defined the terminal state; MP-41's Session 0 executed it; MP-42's Session 0 consumed that execution and chose; ... MP-70's Session 0 consumed MP-69's Session-0 decision with dates. **This phase's Session 0 must consume MP-70's Session-0 decision with dates** — the single most dangerous drift is re-litigating a thirty-times-consumed decision. The decision chain is now twenty-nine generations deep; a sitting stamps, it never re-decides.

### 2. The Stacked Execution Remains the Critical Path

This phase's Session 0 consumes MP-70's release report, which consumes ADR-0043's, which awaits MP-29 through MP-40. A slip at any link slides the whole chain; **my highest-leverage act is unchanged: protect MP-29's window** — its release report is the artifact everything downstream consumes. Nothing in this phase may borrow a minute from it.

### 3. The Science's Next Fork Is Three Hard Blockers Deep — This Phase Addresses Them Directly

The MP-70 roadmap's eight candidates (R1–R8) are this phase's frozen candidate set. They are conditions, not predictions; a sitting decides, it never invents.

### 4. The Steady State Must Not Become Ceremony

This will be the twenty-first roadmap written from an *executed* roadmap's release report
— the program's normal, confirmed twenty-one times. The drift risk inverts and deepens: the
machinery (ledgers, sessions, gate criteria) is now twenty executions deep, so the law's
countermeasure is that rows must still be dated in the sitting that owns them, verdicts still
consumed as artifacts, and zero UNDECIDED rows at Session 8.

### 5. The Paper's Compile Gate Remains the Hardest Artifact

No TeX on this machine — verified again in this sitting; MP-31's own canon applies early: *toolchains are pinned in Session 0, never discovered at Session 7.* The paper v20 rule ("opens only for new numbers, else v19 is the record") is my insurance.

### 6. The Showcase's Receipts Are Still Future, One Deeper

The eighteenth stranger-run transcript lands only if the lanes execute; C67 (the rate as a policy) is conditioned on ≥ 18 transcripts on disk at Session 0 — the receipt compounds only if the lanes execute.

---

## Part III — The Roadmap, Step by Step (Continuum Law, Twentieth Execution)

### The Frozen Candidate Set (Chosen at Session 0, Never Improvised)

| # | Candidate | Opens Only If | Why It Would Close |
|---|-----------|---------------|-------------------|
| R1 | **GPU Grokking 3-Seed P=113** — execute `notebooks/colab_grokking_full_run.ipynb` on Colab A100/T4, 3 seeds × 5000 epochs, checkpoint every 500, manifest to Drive | Always (primary flagship) | Colab OOM at batch_size=512 → reduce to 256, log, re-run; if all 3 seeds fail → document failure, proceed to R3 |
| R2 | **Extended Induction 10k Epochs ×3 Seeds** — `--standard --epochs 10000 --checkpoint-every 500 --save-model --seeds 0,1,2` | Rung 1 standard run < 0.3 diag+1 at 3k epochs (confirmed 2026-08-14) | If 10k epochs still 0 heads → hypothesis "fresh-batches at standard scale produces heads" falsified; document boundary |
| R3 | **Neuron Ablation on Dense Grokking** — on existing P=113 checkpoints (seed 0,1,2), ablate MLP neurons by activation magnitude; compare degradation to Fourier ablation | GPU run completes (uses existing checkpoints) | If neuron ablation also shows graceful degradation → dense solution is distributed linear map, not sparse DFT |
| R4 | **Clean-Clone Reproducibility Proof** — fresh clone → `uv sync` → `make reproduce-quick` → `make verify-claims` | Always (Phase 6 gate) | If fails → fix blocking issue, re-run; transcript required for release |
| R5 | **SAE on Confirmed-Head Checkpoint** — `--activations-from <head_checkpoint> --hooks ln_final --dict-size 256 --epochs 300 --seeds 0,1,2` | Rung 1 produces confirmed induction head (R2 verdict at Session 3) | If no head by R2 verdict → SAE stays on synthetic only; document the dependency |
| R6 | **Teaching Artifact v20: "From Dense Grokking to Sparse Circuits"** — runnable Colab notebook: train/load P=113, Fourier analysis, ablation sweep, neuron ablation, comparison to Nanda et al., honest conclusion | Always (showcase lane) | If no GPU run → use existing CPU checkpoints; the artifact teaches the *negative result* |
| R7 | **Paper v20 / Annex v20** — if R1/R2/R3/R5 produce new numbers → paper v20 diff + annex v20; else "v19 is the record" dated memo | New numbers from R1, R2, R3, or R5 | If no new numbers → v20 is a dated memo, not a compilation crisis |
| R8 | **Gate-Debt Re-verification** — re-verify all MP-30–MP-36 row closures with transcripts; `gate-debt.md` complete or absent-with-date | All MP-30–MP-36 rows | Session 1 (initial), re-verified Session 7 |

**Universal Override**: If GPU run (R1) produces **sparse Fourier** (k₉₉ < P/2 sustained ≥3 checkpoints) → R1 becomes the sparse-regime mechanism study (Nanda-style per-frequency reading), R2/R5 reprioritized to characterize the difference between this run and the NO-GROK runs.

**Post-Record Override**: If MP-70's Session 0 continued the post-record arc → R1 becomes "Post-Record Harness Design from Dated Negatives", R2 becomes "Eighth Post-Record Question", etc. — but MP-70 has not yet consumed MP-69's decision, so this roadmap assumes the pre-record arc.

### The Nine Sessions

#### Session 0 (~1 h) — The Gate Truthing + The Thirtieth-Generation Arc + The Continuum Choice
- Consume MP-70's release report row by row: ADR-0023 at zero UNDECIDED rows, the live URL re-clicked, `verify-claims` at actual count, the eighteenth teaching transcript on disk, `dev == main`.
- Commit the intake table before a single continuum row opens.
- **Ex-T: Consume MP-70's Session-0 decision with dates** — the thirtieth-generation consumption: if the post-record arc continued, the eighth post-record question's verdict is read from ADR-0023 row 3 and the ninth post-record question chosen from the pre-registered continuation set; if not, the R1–R8 adjudication: exactly one opens as row 3, the unchosen close with one dated reason each, stamped in the same sitting.
- Open ADR-0024 with its eight rows, windows and kill-dates; declare the terminus (release = merge + 14 calendar days); promote this roadmap from MP-70's release report, deviations recorded as dated ledger notes.
- **Exit**: intake signed; the thirtieth-generation arc stamped; row 3 chosen (or the post-record continuation row opened); ledger open.

#### Session 1 (~2 h) — The GPU Launch + The Shelf Baseline + The Debt Re-verification
- Row 5: hostile-webmaster walk of the live site + Space at zero (links, assets, a11y, orphans) — extended to the repo's own shelf: local `main` re-verified reconciled to `origin/main`, `portfolio/README.md`'s staleness verified closed, the exp6 residue removed with a transcript, the annexes' location verified.
- Row 8: MP-70's stamped closures re-verified (W&B, clean-clone proof, graduation proof, `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch resolution, the README fix, the residue removal) — each cell LAUNCHED-with-transcript or CLOSED-with-one-reason; a claimed closure without its transcript stays open and blocks Session 8; `gate-debt.md`'s absence, if still absent, recorded with a date.
- **Launch R1 (GPU Grokking)** — upload notebook to Colab, mount Drive, start 3-seed run.
- **Exit**: rows 5 and 8 stamped; R1 running on Colab.

#### Session 2 (~3 h) — The Extended Induction Launch + Neuron Ablation + GPU Monitor
- Launch R2 (Extended Induction 10k epochs ×3 seeds) in background with checkpointing every 500 epochs.
- Launch R3 (Neuron Ablation) on existing P=113 CPU checkpoints — scripted, produces `figures/exp2_neuron_ablation.png`.
- Monitor R1: check Colab runtime, download first checkpoint if available.
- **Exit**: R2 running; R3 complete or running; R1 at 1000+ epochs per seed.

#### Session 3 (~2 h) — The GPU Run Verdict Intake + Extended Run Monitor
- R1 completes (or checkpoints at 3000+ epochs). Download: checkpoints,
`results/exp2_grokking.json`, `figures/exp2_*.png`. Verify manifest against
RESULTS.md tags (`verify-claims` at 0).
- R2 monitor: check 2k/4k epoch checkpoints for Step 1 formation (L0 duplicate mass).
- **Exit**: R1 manifest on disk; `verify-claims` updated; R2 at 4k+ epochs.

#### Session 4 (~2 h) — Clean-Clone Proof + Paper v20 Decision
- Execute clean-clone protocol: fresh clone → `uv sync` → `make reproduce-quick` → `make verify-claims`.
- Full transcript to `06_production_ai/proofs/reproducible-from-clean-clone.md`.
- Paper v20 decision: if R1/R2/R3 produced new numbers → paper v20 diff + annex v20 scaffold; else "v19 is the record" memo.
- **Exit**: clean-clone transcript; paper decision dated.

#### Session 5 (~2 h) — Essay Annex v20 + SAE Protocol (Gated on R2 Verdict)
- `portfolio/essay-annex-20.md` (on live shelf, dated): R1/R2/R3 verdict set distilled into one dated annex; reverse claims audit at zero (prose → manifest → command).
- If R2 produced confirmed head: write R5 protocol (SAE on head checkpoint) with site, metric, negative control, kill-date.
- **Exit**: annex drafted; R5 protocol written or closed with reason.

#### Session 6 (~3 h) — The Teaching Artifact + Stranger Run
- Build R6 (Teaching Artifact v20 Colab notebook).
- Execute on fresh Colab session as stranger — full transcript saved.
- Compare against previous artifact's transcript (Ex-M).
- **Exit**: artifact shipped with transcript; Ex-F distillation complete.

#### Session 7 (~2 h) — The Shelf Rehearsal + The Re-check Row + The Teaching Polish
- Row 5: hostile-webmaster walk at zero beside the browser, every public number clicked back
to disk; the repo-shelf findings re-checked (local `main` reconciled, README current,
residue gone, annexes' home verified).
- Row 6's re-check row dated.
- Row 7: the eighteenth artifact runs end to end on a stranger's machine (fresh clone /
Colab session); the run transcript is the receipt; the teaching distillation (Ex-F)
lands here.
- **Exit**: rows 5, 6, 7 dated; the artifact shipped with its transcript.

#### Session 8 (~1 h) — The Release
- ADR-0024 at zero UNDECIDED rows; the merge green locally and on GitHub; `dev == main`;
home wired — this roadmap's companion status retired; the roadmap archived with its
deviations, every deviation a dated ledger note.
- If the post-record arc governs, this sitting stamps the post-record arc's eighth dated direction — the record's closing sentence consumed eight times, never repeated.
- **Exit**: the merge; the program's twentieth dated direction — or the post-record arc's eighth.

### The One Measured Line

ADR-0024 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED research row
(R1, the GPU grokking run) whose verdict (or scheduled negative) re-derives from a manifest;
`verify-claims` at 0 with every public number re-derivable from one command line; the
hostile-webmaster walk at zero on the live shelf and on the repo's own shelf (local `main`
reconciled, README current, residue removed, the debt ledger present or absent-with-date);
the eighteenth teaching artifact shipped with a stranger-runnable transcript; `dev == main`
and the program's twentieth dated direction — or, if the post-record arc governs, its eighth
dated direction.

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

- **Experiment**: Extend the standard-scale run to 10k epochs with checkpointing every 500. Track Step 1 and Step 2 metrics independently (already instrumented in `diagnose_induction_formation`).

### 3. SAE Sparsity Gap on Real Activations (the R5 Reading — the Instrument as a Standard)

**Question**: *Why does the SAE achieve 99.97% FVE but only 17% sparsity (L0=136/256) on real activations vs. 97.5% FVE at 18% sparsity on synthetic?*

- **Primary sources**:
  - Bricken et al., *Towards Monosemanticity* (2023) — SAE architecture, dead features, FVE vs. L0 tradeoff
  - Cunningham et al., *Sparse Autoencoders Find Highly Interpretable Features in Language Models* (ICLR 2024) — evaluation metrics
  - Templeton et al., *Scaling Monosemanticity* (2024) — dictionary size scaling laws

- **Prediction**: The 32-dim residual stream from a small, undertrained model (150-300 epochs,
no confirmed induction head) contains *no genuinely sparse features* — the SAE is learning a
dense overcomplete basis because the ground truth isn't sparse yet. Once Rung 1 produces a
checkpoint with real induction heads, the SAE on *that* checkpoint should show sparse
features (L0 ~ 20-30).

- **Experiment**: Re-run `exp5_sae_dashboard --activations-from` on the first checkpoint that has a confirmed induction head. Compare L0/FVE tradeoff curves.

### 4. The Post-Record Program, Ninth Generation (New, Deepest)

**Question**: *What does the record's eighth post-record verdict open?*

- **Primary sources**: Lakatos, *The Methodology of Scientific Research Programmes* (1978) — read
a tenth time, now for the *ninth* question past a completed program: progressive vs
degenerating problem shifts when the *eighth* post-record verdict lands, Kuhn's normal
science as the post-record arc's axioms, and the honest criterion for the ninth
post-record question — a question that must earn the post-record arc's eighth *new*
paragraph. This reading feeds Ex-T and the Session-0 question this phase owns more deeply
than any phase before it: *what does the record's eighth post-record verdict open?* The
answer can be the post-record arc's ninth dated row — Lakatos' point is that the decision
is made on the record, never as a mood.

### 5. The Record Teaches, Round Nineteen

**Question**: *Can I distill the nineteenth verdict into four registers without leakage?*

The nineteenth verdict in four registers — the paper's sentence, the annex's sentence,
the 30-second spoken claim, and the 5-minute teaching explanation with a worked toy a
stranger can run; the gap between the last two is where my teaching leaks, and I will
measure it deliberately by writing all four registers for the same verdict (Ex-F).

### 6. The Redemption Reading, or Negative Results as Maps, the Nineteenth Pass

**Question**: *How is the completed law reported honestly?*

If a sparse cell exists by S0: Nanda et al.'s full per-frequency reading on the first sparse
solution this harness ever produced. If not: how the *completed* law is reported honestly —
the law's domain closed with its measured boundaries and its failure cells explained or
mapped, the driver a principle or a case study with a dated exception map, the drift numbers
nine deep, the negative as a contribution — and how the post-record harness (if PR-22
governs) would be designed from the dated negatives instead of from hope. Either way, the
paper's hardest paragraph is the one that claims the dense solution *computes something*; I
will draft it against this reading and let the manifest referee it.

---

## Part V — Documentation Requirements (The Contract)

Everything this phase claims re-derives from a manifest and a command. The documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0, rewritten from MP-70's
release report, deviations recorded as dated ledger notes.
- **ADR-0024**, the twentieth continuum ledger — eight rows pre-stamped with windows and
kill-dates; rows 1–2 consumed from ADR-0023's verdicts; row 3 the twentieth research
question with its protocol note and heartbeat (or the post-record continuation row's
protocol); rows 4–8 the continuum's decisions.
- **GPU Colab Execution Protocol** — `06_production_ai/notes/gpu-colab-execution-protocol.md` updated with actual run transcript.
- **Extended Induction Run Spec** — `04_nlp_and_transformers/notes/induction-extended-run.md` updated with actual 10k-epoch curves.
- **Clean-Clone Reproducibility Proof** — `06_production_ai/proofs/reproducible-from-clean-clone.md` updated with actual transcript and timestamps.
- **Paper v20 Diff** — `portfolio/paper/main.tex` v20 + diff log or the dated "v19 is the record" memo; `make paper` re-verified in the CI mirror.
- **Essay Annex v20** — `portfolio/essay-annex-20.md` (on live shelf) manifest-tagged, amended never rewritten; the annexes' home (the live shelf) recorded with a date.
- **Gate-Debt Ledger** — `checklists/gate-debt.md` — each cell's transcript or one-line reason, dated in Session 1, including the exp5 1000-epoch resolution's receipt re-checked; the file's absence, if still absent, recorded with a date.
- **Research Row's Pre-registration Note** — in `06_production_ai/notes/` + the heartbeat
artifact; if R1: the law-theory figure spec written before the analysis, the figure itself
manifest-tagged after. If the post-record arc governs: the continuation row's protocol
note instead.
- **The Nineteenth Teaching Artifact + its Stranger-Run Transcript** — (fresh-clone or Colab session receipt).
- **Ex-T's Execution Memo** — MP-70's arc decision run with dates: the post-record verdict
consumed or the R1–R8 adjudication executed, the criteria cited, the decision that follows
(the ninth post-record question, or the continuation), written verdict-agnostic in Session 2
and executed at Session 0.
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

### Ex-1 · GPU Execution Drill (Session 1)

**Goal**: Execute the hardened Colab notebook for 3-seed P=113 grokking run.

```bash
# In Colab:
1. Upload notebooks/colab_grokking_full_run.ipynb
2. Runtime → Change runtime type → GPU (A100/T4)
3. Run all cells — captures 3 seeds, checkpoints every 500 epochs, manifests to Drive
4. Download: checkpoints/, results/exp2_grokking.json, figures/
5. Local: verify-claims passes with new manifest
```

**Falsifier**: If Colab OOMs at batch_size=512 → reduce to 256, log the change, re-run.

### Ex-2 · Extended Induction Run (Session 2–3)

**Goal**: Run standard-scale induction heads to 10k epochs with full diagnostics.

```bash
uv run python -m src.experiments.exp1_induction_heads \
  --standard --epochs 10000 --checkpoint-every 500 --save-model \
  --seeds 0,1,2  # multi-seed manifest
```

**Measure every 500 epochs**: Step 1 (L0 duplicate mass), Step 2 (K-composition), val accuracy, diag+1 mass. Plot the two-step trajectory.

**Falsifier**: If at 10k epochs still 0 heads → the hypothesis "fresh-batches at standard scale produces heads" is falsified. Document the boundary.

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

### Ex-4 · Clean-Clone Reproducibility (Session 4)

**Goal**: Prove `uv sync && make reproduce-quick` works from zero.

```bash
cd /tmp && git clone <repo> test-clone && cd test-clone
uv sync
make reproduce-quick  # all 5 rungs in --quick mode
make verify-claims    # must pass
```

**Document**: Full transcript in `06_production_ai/proofs/reproducible-from-clean-clone.md` with timestamps.

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

### Ex-6 · Teaching Artifact: "From Dense Grokking to Sparse Circuits" (Session 6)

**Goal**: One runnable Colab notebook that teaches the grokking story — including the negative result.

- Cell 1: Train P=113 (or load checkpoint)
- Cell 2: Fourier analysis — show dense spectrum
- Cell 3: Ablation sweep — show graceful degradation
- Cell 4: Neuron ablation — show distributed representation
- Cell 5: Compare to Nanda et al. sparse circuit (what we *expected* vs. what we *got*)
- Cell 6: The honest conclusion: "Sometimes the model finds a different algorithm"

**Transcript**: Stranger runs it on fresh Colab session → saves output → transcript committed.

### Ex-7 · The Arc Consumption, Thirtieth Generation (Session 0, New, Verdict-Agnostic)

The consumption chain's deepest run — MP-70's Session-0 decision consumed with dates as
MP-71's intake, the eighth-generation post-record verdict read from ADR-0023 row 3 if the arc
governs, the criteria cited, the release that follows (the ninth post-record question, or the
R1–R8 adjudication), and what each of ADR-0023's possible verdicts changes in that execution.
One runnable check: the execution memo exists, names the decision rule that closes or
continues the program's science, and cites the criteria from MP-70's release report — the
chain now thirty generations deep, a sitting stamps, it never re-decides.

### Ex-8 · The Fork Drill, Deepest Form (Session 2, Verdict-Agnostic)

The continuing state (R1–R8) vs the post-record state (continuation set) written as two
one-page paths — what each verdict changes downstream, including the R1-vs-R2 choice and the
post-record continuation choice — so next phase's S0 decision is a stamping, not a discovery.

---

## Part VII — Strategic Tips and Architectural Best Practices

- **The one-question law, twentieth execution.** A phase that opens two research questions is drift by another name; the unchosen candidates close in the same sitting as the choice — and the arc consumption may close all of them with the post-record verdict. The continuum law is the mechanical refusal of this drift — proven executable nineteen times, it must simply be executed again.

- **The candidate set is frozen before S0, never improvised at it.** R1–R8 are conditions,
not predictions; a sitting decides, it never invents — and the terminal-state object is the
hardest frozen object on the record: written by MP-40, executed by MP-41, consumed by
MP-42, consumed again by MP-43, consumed a third time by MP-44, consumed a fourth time by
MP-45, consumed a fifth time by MP-46, consumed a sixth time by MP-47, consumed a seventh
time by MP-48, consumed an eighth time by MP-49, consumed a ninth time by MP-50, consumed
a tenth time by MP-51, consumed an eleventh time by MP-52, consumed a twelfth time by
MP-53, consumed a thirteenth time by MP-54, consumed a fourteenth time by MP-55, consumed
a fifteenth time by MP-56, consumed a sixteenth time by MP-57, consumed a seventeenth time
by MP-58, consumed an eighteenth time by MP-59, consumed a nineteenth time by MP-60,
consumed a twentieth time by MP-61, consumed a twenty-first time by MP-62, consumed a
twenty-second time by MP-63, consumed a twenty-third time by MP-64, consumed a
twenty-fourth time by MP-65, consumed a twenty-fifth time by MP-66, consumed a
twenty-sixth time by MP-67, consumed a twenty-seventh time by MP-68, consumed a
twenty-eighth time by MP-69, consumed a twenty-ninth time by MP-70, **consumed a thirtieth
time by MP-71** — never re-negotiated in the consuming sitting.

- **Consumption is execution.** A verdict consumed into an artifact in the same sitting is a result; consumed into a paragraph written later it is a memory. Row 1 consumes ADR-0023's row-3 verdict in the sitting that owns it — or the post-record statement, if the arc governs.

- **The receipt compounds.** The nineteenth runnable artifact is only worth shipping because the
first eighteen transcripts proved the format — and if R5 opens, the receipts are a
drift-of-drift-of-drift-of-drift-of-drift-of-drift-of-drift-of-drift number measured eight
times in a row, tested by people I did not choose, across an aging codebase. My showcase's
story is now "read it, run it, watch me be wrong on the record," nineteen receipts deep.

- **The steady state is the reward, not the ceremony.** MP-71 is the twenty-first roadmap written from an *executed* roadmap's release report — the program at its normal, confirmed twenty-one times. The cap's lesson was that promises without dates drift; the steady state's discipline is that the machinery never becomes the goal: rows are dated in the sitting that owns them, or they are not rows.

- **Stop-and-publish stays open, and the post-record criterion is now nine questions deep.** ADR-0004's row 5 is the honest exit; a candidate set that cannot earn a paragraph the record lacks is a phase that should close itself. If the post-record arc governs, the deepest candidate earns the post-record arc's *eighth new paragraph* — the record's closing sentence consumed nine times, never repeated. This is the deepest form of laziness: do not build what the record has already said.

- **Toolchains are pinned in S0, never discovered at S7.** The paper's compile gate is the hardest artifact in the stack; the v20 rule ("opens only for new numbers") is the insurance that makes a missing toolchain a dated reason, not a crisis.

- **Protect the release report.** The serialized stack means MP-29's release is the artifact everything downstream consumes; a slip at any link slides the whole chain. The deepest law still applies: a promise can be re-planned forever, but a dated row is answered.

- **The S0 gate is a checklist with receipts.** ADR-0023 at zero, the live URL, `verify-claims` at 0, the eighteenth teaching transcript on disk — a condition with artifacts, not a paragraph.

- **The negative stays the signature.** The row that closes with one reason dated in the sitting that owns it is the strongest artifact in the repository. Every positive result in this program has a negative twin that was measured, drafted, and stamped — and the negative twin is the one that proves the positive wasn't cherry-picked. The GPU unblock is the act of finally measuring the primary flagship on its native hardware; whatever it returns, the measurement is the contribution.

- **Architectural integrity check for this phase:** The checkpointing infrastructure in
`src/experiments/checkpointing.py` (shared by exp1/exp2) was battle-tested in MP-12/MP-28
and must not be touched unless a falsification test fails. The `runner.py` multi-seed
aggregation and `results.py` manifest/verification machinery are the backbone — they are the
contract, not the implementation.

- **Reproducibility as a first-class citizen:** Every figure, every number, every claim must trace back to a manifest and a command. The `make reproduce` target is the single source of truth for "what does this repo produce?" — if it drifts, the science drifts.

---

**Written**: 2026-08-22  
**Perspective**: Personal study notes / learning log / portfolio showcase  
**Status**: Ready for Session 0 consumption — candidate set frozen, conditions explicit, no improvisation at S0. The GPU unblock is the act of finally measuring the primary flagship on its native hardware; whatever it returns, the measurement is the contribution.