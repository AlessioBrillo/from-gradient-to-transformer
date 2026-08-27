---
tags: [type/moc, phase/7, research/experiment, state/roadmap]
created: 2026-08-27
consumes: [ADR-0026]
---

# Micro-Phase 76 — Next Micro-Phase Roadmap: Capstone Integration & Publication

> **STATUS: PLAN MODE** — This document is the pre-registered roadmap for MP-76, written from the reviewer's chair before the work begins. It consumes MP-75's release report and opens the final integration arc: paper prose from manifests, portfolio project write-ups, HF Spaces SAE browser deploy, Pages deploy workflow, and final release. No improvisation at Session 0.

---

## Showcase Framing

This is the twenty-fourth roadmap written from an *executed* roadmap's release report. Anyone reading the repository in sequence (MP-37 through this file) watches the same discipline recur: facts re-verified session by session, a ledger that stamps rows or closes them with one named reason, negatives shipped as loudly as positives, and one deep question chosen per phase. The measured line in Part III: **ADR-0027 at zero UNDECIDED rows on release day, with the capstone's final deliverables manifest-tagged and the showcase live.**

---

## Part I — Where I Stand (State Review, Anticipated Post-MP-75)

### The Scientific Ledger (Anticipated Post-MP-75)

| Experiment | Expected Verdict | Evidence |
|------------|------------------|----------|
| **Rung 1: Induction Heads** | 10k-epoch verdict (heads or boundary documented) | `results/exp1_induction_heads.json` extended |
| **Rung 2: Grokking P=113** | GPU 3-seed run completed; dense Fourier confirmed (k₉₉ ≈ 111) | `results/exp2_grokking.json` + `figures/exp2_neuron_ablation.png` |
| **Rung 3: Superposition** | Solid baseline (already reproducible) | `results/exp3_superposition.json` |
| **Rung 4: Circuit Patching** | On real head (if R1 confirms) OR synthetic only | `results/exp4_circuit_patching.json` |
| **Rung 5: SAE Dashboard** | On real head activations (if R1 confirms) OR synthetic | `results/exp5_sae_dashboard.json` |

**The arc**: MP-74 executes GPU unblock → MP-75 executes cascade → **MP-76 integrates into publication**.

### The Stack at Intake (Inherited from MP-75)

- **MP-29** terminus ≈ 2026-08-26 (control for dense solution structure)
- **MP-30 through MP-36** pre-registered, gated in series, cap at seven — **MP-76 is where they execute**
- **ADR-0026** = MP-73's ledger (twenty-second continuum ledger)
- **ADR-0027** = MP-76's ledger (twenty-third continuum ledger — **this phase's output**)

### CI Floor & Toolchains (Verified Gaps to Close in MP-76)

| Gap | Owner | MP-76 Target |
|-----|-------|--------------|
| No LaTeX toolchain (`make paper` graceful) | MP-31 | Install TeXLive or document as dated reason |
| No Pages deploy workflow | MP-31 | Add `.github/workflows/pages.yml` |
| No `publish:` frontmatter policy | MP-31 | Define in `04_conventions.md` |
| `portfolio/projects/` holds figures, no write-ups | MP-32 | Write 5 project pages (one per rung) |
| W&B never connected | MP-33 | Connect or close with reason |
| Clean-clone proof | MP-34 | **Must be green** — Phase 6 gate |

---

## Part II — The Bottleneck Analysis (What I Must Not Let Drift)

### 1. The Consumption Chain Is Now Thirty-Three Generations Deep

MP-40's Ex-N defined terminal state → MP-41 executed → ... → **MP-76 Session 0 must consume MP-75's Session-0 decision with dates**. The single most dangerous drift is re-litigating a thirty-three-times-consumed decision. The decision chain is now thirty-three generations deep; a session stamps, it never re-decides.

### 2. MP-76 Is the "Pay the Debt" Phase

MP-30 through MP-36 have been pre-registered since MP-70 (2026-08-21). Seven phases of residue. **MP-76 is the only phase that directly executes them.** Every row in `checklists/gate-debt.md` must go from PENDING → LAUNCHED-with-transcript or CLOSED-with-one-reason by Session 8.

### 3. The Paper's Compile Gate Is the Hardest Artifact

No TeX on this machine — verified repeatedly. **Toolchains pinned in S0, never discovered at S7.** Paper v24 rule ("opens only for new numbers from MP-74/75, else v23 is the record") is the insurance.

### 4. The Showcase's Receipts Must Compound

The twenty-second stranger-run transcript lands only if the lanes execute. MP-76's teaching artifact must ship with transcript, and the HF Spaces demo must be live.

---

## Part III — The Roadmap, Step by Step (Continuum Law, Twenty-Third Execution)

### The Frozen Candidate Set (Frozen at MP-76 Session 0, Consumed from MP-75)

| # | Candidate | Opens Only If | Why It Would Close |
|---|-----------|---------------|-------------------|
| R1 | **Capstone Research Plan Execution** — write mini-paper prose from MP-74/75 manifests | Clean-clone proof green (Phase 6 gate) | If clean-clone fails → fix blocker, re-run; no prose without reproducibility |
| R2 | **Paper Prose from Manifests** — 4–8 page LaTeX: abstract, method, results (Rungs 1–5), ablations, limitations, references | R1 opens (clean-clone green) | If no new numbers from MP-74/75 → "v23 is the record" memo |
| R3 | **W&B Integration + Dashboard** — connect runs, log progress measures, loss curves | Always (MP-30/33 residue) | If W&B unavailable → document as dated reason; local plots suffice |
| R4 | **HF Spaces SAE Browser Deploy** — interactive feature dashboard from Rung 5 | R5 executed with confirmed head (MP-75 R2) | If no confirmed head → deploy on synthetic SAE; document limitation |
| R5 | **Portfolio Project Write-ups** — 5 pages in `portfolio/projects/` (one per rung) | Figures exist for all 5 rungs | If any rung missing → write what exists; document gaps honestly |
| R6 | **Pages Deploy Workflow** — GitHub Pages action for `portfolio/` | Paper v24 compiles (R2) | If no TeX → workflow deploys static HTML from `portfolio/` only |
| R7 | **Final Integration & Release** — `verify-claims` at 0, all manifests tagged, RESULTS.md current, home wired | Rows 1–6 complete | Blockers tracked in ADR-0027 row 7 |
| R8 | **Gate-Debt Final Closure** — re-verify all MP-30–MP-36 row closures | All MP-30–MP-36 rows | Session 1 (initial), re-verified Session 7 |

### The Nine Sessions

#### Session 0 (~1 h) — Gate Truthing + Thirty-Third-Generation Arc

- Consume MP-75 release report row by row: ADR-0026 at zero UNDECIDED, live URL re-clicked, `verify-claims` at actual count, twenty-first teaching transcript on disk, `dev == main`
- Commit intake table before any continuum row opens
- **Ex-T: Consume MP-75's Session-0 decision with dates** — thirty-third-generation consumption
- Open ADR-0027 with eight rows, windows, kill-dates; declare terminus (release = merge + 14 calendar days)
- **Exit**: intake signed; row 1 (capstone execution) opens contingent on clean-clone proof

#### Session 1 (~2 h) — Clean-Clone Proof Re-verification + Gate-Debt Initial Audit

- Re-execute clean-clone protocol from MP-75 Session 4: fresh clone → `uv sync` → `make reproduce-quick` → `make verify-claims`
- Full transcript to `06_production_ai/proofs/reproducible-from-clean-clone.md` (append MP-76 session)
- **Row 8 initial**: audit all MP-30–MP-36 rows from `checklists/gate-debt.md` — each LAUNCHED-with-transcript or CLOSED-with-one-reason
- **Exit**: clean-clone re-verified; gate-debt initial pass dated; **R1 unblocks if clean-clone green**

#### Session 2 (~3 h) — Mini-Paper Prose from Manifests (R1→R2)

- **If R1 open**: Write paper prose directly from manifests:
  - `results/exp1_induction_heads.json` → Induction Heads section
  - `results/exp2_grokking.json` + `figures/exp2_neuron_ablation.png` → Grokking section
  - `results/exp3_superposition.json` → Superposition section
  - `results/exp4_circuit_patching.json` → Circuit Patching section
  - `results/exp5_sae_dashboard.json` → SAE section
- Reverse claims audit: every sentence → manifest → command
- **Output**: `portfolio/paper/main.tex` v24 + diff log
- **Exit**: paper prose drafted; ADR-0027 Row 2 stamped

#### Session 3 (~2 h) — W&B Integration + Portfolio Project Write-ups (R3, R5)

- **R3**: Connect W&B to existing runs (or close with reason); log progress measures from `exp2_grokking.json`
- **R5**: Write 5 project pages in `portfolio/projects/`:
  - `01_induction_heads.md` — from exp1 manifest + figures
  - `02_grokking_modular_addition.md` — from exp2 manifest + figures + neuron ablation
  - `03_superposition.md` — from exp3 manifest + figures
  - `04_circuit_patching.md` — from exp4 manifest + figures
  - `05_sae_dashboard.md` — from exp5 manifest + figures
- Each page: problem, method, results, code link, reproducibility command
- **Exit**: W&B status resolved; 5 project pages committed

#### Session 4 (~3 h) — HF Spaces SAE Browser Deploy (R4)

- **If MP-75 R2 produced confirmed head**: Deploy SAE dashboard on HF Spaces using `sae-vis` export
- **Else**: Deploy on synthetic SAE (already trained) with clear limitation banner
- Steps: `sae-vis` → generate static HTML → push to HF Space → verify live
- **Output**: Live URL in `portfolio/README.md` and `RESULTS.md`
- **Exit**: HF Space live; ADR-0027 Row 4 stamped

#### Session 5 (~2 h) — Pages Deploy Workflow + Paper Compile (R6)

- Add `.github/workflows/pages.yml`:
  - Trigger: push to main touching `portfolio/`
  - Build: if TeX available → compile paper → deploy `portfolio/` + `paper/`
  - Else → deploy `portfolio/` only (static HTML)
- Test workflow on feature branch; merge to main
- **Exit**: Pages workflow green; live URL verified

#### Session 6 (~2 h) — Essay Annex v24 + Final RESULTS.md Sync (R2 completion)

- `portfolio/essay-annex-24.md` on live shelf: MP-74/75 verdict set distilled
- Reverse claims audit at zero (prose → manifest → command)
- Update `RESULTS.md` with all manifest tags:
  ```markdown
  <!-- manifest: results/exp1_induction_heads.json -->
  <!-- manifest: results/exp2_grokking.json -->
  <!-- manifest: results/exp3_superposition.json -->
  <!-- manifest: results/exp4_circuit_patching.json -->
  <!-- manifest: results/exp5_sae_dashboard.json -->
  ```
- **Exit**: annex drafted; RESULTS.md current; all manifests tagged

#### Session 7 (~2 h) — Shelf Rehearsal + Gate-Debt Re-verification + Teaching Polish

- **Row 5 re-check**: hostile-webmaster walk at zero beside browser — every public number clicked back to disk
- **Row 6 re-check**: dated
- **Row 7**: twenty-second teaching artifact (from MP-75) runs end-to-end on stranger's machine; transcript is receipt
- **Row 8 re-verification**: all MP-30–MP-36 rows closed with transcripts/reasons
- **Exit**: rows 5, 6, 7, 8 dated; `gate-debt.md` complete

#### Session 8 (~1 h) — The Release

- ADR-0027 at zero UNDECIDED rows; merge green locally and on GitHub; `dev == main`; home wired
- Archive roadmap with deviations as dated ledger notes
- **Exit**: the merge; program's twenty-third dated direction

### The One Measured Line

**ADR-0027 at zero UNDECIDED rows on release day (target 2026-09-20), with:**
- Clean-clone proof green (Phase 6 gate unlocked)
- Mini-paper v24 compiled from manifests (or "v23 is the record" memo)
- 5 portfolio project pages live
- HF Spaces SAE browser deployed
- GitHub Pages workflow green
- W&B status resolved
- `verify-claims` at 0 with every public number re-derivable from one command
- Hostile-webmaster walk at zero on live shelf and repo shelf
- Twenty-second teaching artifact shipped with stranger-runnable transcript
- `dev == main` and the program's twenty-third dated direction

---

## Part IV — Deep-Dive Study and Research Topics

### 1. Writing the Dense Grokking Result as a Contribution (The R1 Reading)

**Question**: *How do I honestly report a negative result (dense Fourier) as a positive contribution?*

- **Primary sources**:
  - Nanda et al., *Progress Measures for Grokking* (ICLR 2023) — the sparse baseline I'm comparing against
  - Varma et al., *Explaining grokking through circuit efficiency* (2023) — circuit efficiency as driver
  - Lyu et al., *Training dynamics of transformers on modular arithmetic* (2024) — loss landscape
  - Gromov, *Grokking: A Memory Perspective* (2023) — memorization vs. generalization as compression

- **Prediction to write before drafting**: The paper's hardest paragraph claims the dense solution *computes addition via a distributed linear map in embedding space*. Neuron ablation shows graceful degradation (no single neuron critical), Fourier ablation shows catastrophic collapse — this double dissociation is the evidence. The contribution is not "we reproduced Nanda" but "we characterized the dense attractor and its algorithm."

- **Experiment**: Already done in MP-75 R3. Now: write the prose that lets the manifest referee it.

### 2. The Induction Head Boundary as a Scaling Law (The R2 Reading)

**Question**: *At what (width, depth, data, compute) does the induction head phase transition actually occur, and what does the boundary teach us?*

- **Primary sources**:
  - Olsson et al., *In-context Learning and Induction Heads* (2022) — original emergence curves
  - Nanda & Jacobsen, *Attention as a Step Towards Induction Heads* (2023) — two-step path
  - Liu et al., *Transformers Learn Shortcuts by Default* (2023) — memorization as competing attractor
  - Michaud et al., *The Quantization Model of Neural Scaling* (2024) — phase transitions as scaling laws

- **Prediction**: The 10k-epoch run at standard scale (`d_model=64, 2-layer, 4 heads, fresh-batches`) will either cross the threshold or definitively map the boundary. If 0 heads at 10k, the hypothesis "fresh-batches at standard scale produces heads" is falsified — the boundary moves to larger scale.

### 3. SAE Sparsity Gap: Real vs. Synthetic vs. Undertrained (The R5 Reading)

**Question**: *Why does SAE achieve 99.97% FVE but only 17% sparsity on undertrained real activations vs. 97.5% FVE at 18% sparsity on synthetic? What changes with confirmed induction heads?*

- **Primary sources**:
  - Bricken et al., *Towards Monosemanticity* (2023) — SAE architecture, dead features, FVE vs. L0
  - Cunningham et al., *SAEs Find Highly Interpretable Features* (ICLR 2024) — evaluation metrics
  - Templeton et al., *Scaling Monosemanticity* (2024) — dictionary size scaling laws
  - Makelov, Lange & Nanda, *SAEs can learn illusory features* (2023) — cautionary note

- **Prediction**: The 32-dim residual stream from a small undertrained model contains no genuinely sparse features — the SAE learns a dense overcomplete basis because the ground truth isn't sparse yet. With confirmed induction heads, sparsity should improve (L0 ~ 20-30).

### 4. The Post-Record Program, Eleventh Generation (New, Deepest)

**Question**: *What does the record's tenth post-record verdict open?*

- **Primary sources**: Lakatos, *The Methodology of Scientific Research Programmes* (1978) — read twelfth time, now for the *eleventh* question past a completed program: progressive vs degenerating problem shifts when the *tenth* post-record verdict lands; Kuhn's normal science as post-record arc's axioms; honest criterion for the eleventh post-record question.

### 5. The Record Teaches, Round Twenty-Three

**Question**: *Can I distill the twenty-third verdict into four registers without leakage?*

The twenty-third verdict in four registers: paper's sentence, annex's sentence, 30-second spoken claim, 5-minute teaching explanation with worked toy a stranger can run. The gap between the last two is where my teaching leaks — measured deliberately by writing all four registers for the same verdict (Ex-F).

### 6. The Redemption Reading, Twenty-Third Pass

**Question**: *How is the completed law reported honestly?*

If sparse cell exists by MP-75 S0: Nanda's per-frequency reading on first sparse solution. If not: how the *completed* law is reported honestly — domain closed with measured boundaries, failure cells explained, driver a principle or case study with dated exception map, drift numbers eleven deep, negative as contribution — and how the post-record harness would be designed from dated negatives instead of hope.

---

## Part V — Documentation Requirements (The Contract)

Everything this phase claims re-derives from a manifest and a command.

| Artifact | Location | Trigger |
|----------|----------|---------|
| **This roadmap** (promoted from companion at S0) | `00_meta/76_micro-phase-76-next-phase-roadmap.md` | Session 0 |
| **ADR-0027 updates** (row verdicts, heartbeats) | `docs/adr/0027-continuum-ledger-23.md` | Each session |
| **Clean-Clone Reproducibility Proof** (append MP-76 session) | `06_production_ai/proofs/reproducible-from-clean-clone.md` | Session 1 |
| **Mini-Paper v24** (LaTeX + diff log) | `portfolio/paper/main.tex` v24 | Session 2 |
| **Portfolio Project Write-ups** (5 pages) | `portfolio/projects/01-05_*.md` | Session 3 |
| **HF Spaces SAE Browser** (live URL) | `portfolio/README.md` + HF Space | Session 4 |
| **Pages Deploy Workflow** | `.github/workflows/pages.yml` | Session 5 |
| **Paper v24 Compile Verification** | CI mirror / local if TeX | Session 5 |
| **Essay Annex v24** | `portfolio/essay-annex-24.md` (live shelf) | Session 6 |
| **RESULTS.md** (all manifest tags current) | `portfolio/RESULTS.md` | Session 6 |
| **Gate-Debt Ledger** (complete) | `checklists/gate-debt.md` | Session 1, 7 |
| **Teaching Artifact + Stranger Transcript** (MP-75's, re-verified) | `notebooks/teaching_artifact_v22.ipynb` + transcript | Session 7 |
| **Ex-T Execution Memo** | `00_meta/75_micro-phase-75-next-phase-roadmap.md` (companion) | Session 2 |
| **Progress Log** | `00_meta/03_progress-log.md` | Every session |

### Manifest Tags Required in RESULTS.md

```markdown
<!-- manifest: results/exp1_induction_heads.json -->  (10k-epoch run)
<!-- manifest: results/exp2_grokking.json -->         (GPU 3-seed P=113 + neuron ablation)
<!-- manifest: results/exp3_superposition.json -->    (solid baseline)
<!-- manifest: results/exp4_circuit_patching.json --> (real head if MP-75 R2 opened, else synthetic)
<!-- manifest: results/exp5_sae_dashboard.json -->    (real activation if MP-75 R2 opened, else synthetic)
```

---

## Part VI — Practical Exercises and Hands-On Challenges

### Ex-1 · Clean-Clone Re-verification Drill (Session 1)

**Goal**: Prove `uv sync && make reproduce-quick` works from zero — again, with transcript.

```bash
cd /tmp && git clone <repo> test-clone-mp76 && cd test-clone-mp76
uv sync
make reproduce-quick  # all 5 rungs in --quick mode
make verify-claims    # must pass
```

**Document**: Full transcript appended to `06_production_ai/proofs/reproducible-from-clean-clone.md` with timestamps. This is the Phase 6 gate — must be green.

---

### Ex-2 · Mini-Paper Prose from Manifests (Session 2)

**Goal**: Write 4–8 page LaTeX paper where every claim traces to a manifest.

```bash
# Structure:
# 1. Abstract (3 sentences: thesis, flagship result, caveat)
# 2. Introduction (from gradient to transformer to circuit)
# 3. Methods (model, data, interventions, SAE)
# 4. Results (5 subsections — one per rung, manifest-tagged)
# 5. Ablations (neuron vs Fourier, synthetic vs real SAE, 10k vs 3k induction)
# 6. Limitations (micro-scale, algorithmic tasks, patching approximations)
# 7. Related Work (MI canon + grokking + circuits + SAEs)
# 8. What I Truly Understood (the intuition that stays)

# Workflow:
cd portfolio/paper
# Edit main.tex directly from manifests
# make paper  # verify compile (graceful if no TeX)
```

**Success Criterion**: Every quantitative claim in Results section has a `<!-- manifest: ... -->` tag in RESULTS.md that resolves to a number in the JSON.

**Falsifier**: If a claim cannot be traced to a manifest → cut the claim or re-run the experiment.

---

### Ex-3 · Portfolio Project Write-ups (Session 3)

**Goal**: 5 project pages in `portfolio/projects/`, each a standalone showcase piece.

```bash
# Template for each (copy from templates/project.md):
# ---
# tags: [portfolio, phase/7, rung/N, #research/experiment]
# ---
# 
# # Rung N: [Title]
# 
# ## Problem
# One paragraph: what circuit/algorithm/feature are we looking for?
# 
# ## Method
# Model config, data, intervention, metric — from manifest args
# 
# ## Results
# Key figure + quantitative summary from manifest aggregate block
# 
# ## Code & Reproducibility
# ```bash
# uv run python -m src.experiments.exp{N}_... --quick
# ```
# 
# ## What This Taught Me
# One paragraph: the intuition that transfers.
```

**Output**: `01_induction_heads.md`, `02_grokking_modular_addition.md`, `03_superposition.md`, `04_circuit_patching.md`, `05_sae_dashboard.md`

---

### Ex-4 · HF Spaces SAE Browser Deploy (Session 4)

**Goal**: Deploy interactive SAE feature dashboard.

```bash
# If MP-75 R2 opened (real head checkpoint exists):
uv run python -m src.experiments.exp5_sae_dashboard \
  --activations-from <head_checkpoint> \
  --hooks ln_final --dict-size 256 --epochs 300 --seeds 0,1,2 \
  --export-sae-vis  # generates static HTML for HF Spaces

# Push to HF:
hf repo create <username>/sae-dashboard --type space
cp -r sae_vis_output/* <space_repo>/
cd <space_repo> && git push
```

**If no real head**: Use existing synthetic SAE checkpoint, add banner: *"Trained on synthetic activations — features may not correspond to real model circuits."*

**Success Criterion**: Live URL responds; features browsable; top-activating examples visible.

---

### Ex-5 · GitHub Pages Deploy Workflow (Session 5)

**Goal**: Automated deployment of `portfolio/` to GitHub Pages.

```yaml
# .github/workflows/pages.yml
name: Deploy Portfolio
on:
  push:
    branches: [main]
    paths: ['portfolio/**', '04_conventions.md']
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup TeX (optional)
        # If TeX available: compile paper
      - name: Deploy to Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./portfolio
```

**Test**: Push to feature branch → verify Pages deploy → merge to main.

---

### Ex-6 · Essay Annex v24 + RESULTS.md Sync (Session 6)

**Goal**: One dated annex distilling MP-74/75 verdict set; RESULTS.md with all manifest tags.

```bash
# Essay Annex structure:
# ## Verdict Set (MP-74/75)
# - R1 (GPU Grokking): [SPARSE-FOURIER | NO-GROK] — k₉₉ = X, gen_epoch = Y
# - R2 (Induction 10k): [HEADS CONFIRMED | BOUNDARY DOCUMENTED] — N heads at epoch Z
# - R3 (Neuron Ablation): [GRACEFUL | CATASTROPHIC] — compare to Fourier ablation
# - R4 (Circuit Patching): [REAL HEAD | SYNTHETIC ONLY] — logit-diff recovery = W
# - R5 (SAE): [REAL HEAD | SYNTHETIC] — L0 = V, FVE = U%
#
# ## What Changed from MP-73
# - [One sentence per rung]
#
# ## The Dense Attractor Claim (if NO-GROK)
# The model solves a+b mod 113 via a distributed linear map...
# Evidence: neuron ablation graceful, Fourier ablation catastrophic.
#
# ## Honest Caveats
# - Micro-scale, single architecture, single seed distribution...
```

**RESULTS.md**: Verify all 5 manifest tags present and current.

---

### Ex-7 · The Arc Consumption, Thirty-Third Generation (Session 0, Verdict-Agnostic)

The consumption chain's deepest run — MP-75's Session-0 decision consumed with dates as MP-76's intake, the tenth-generation post-record verdict read from ADR-0026 row 3 if arc governs, criteria cited, release that follows (eleventh post-record question or R1–R8 adjudication), and what each of ADR-0026's possible verdicts changes in that execution. One runnable check: execution memo exists, names the decision rule that closes or continues the program's science, cites criteria from MP-75's release report — chain now thirty-three generations deep, a session stamps, it never re-decides.

---

### Ex-8 · The Fork Drill, Deepest Form (Session 2, Verdict-Agnostic)

The continuing state (R1–R8) vs post-record state (continuation set) written as two one-page paths — what each verdict changes downstream, including the clean-clone gate choice and the post-record continuation choice — so next phase's S0 decision is a stamping, not a discovery.

---

## Part VII — Strategic Tips and Architectural Best Practices

### 1. The One-Question Law, Twenty-Third Execution

A phase that opens two research questions is drift by another name; the unchosen candidates close in the same session as the choice — and the arc consumption may close all of them with the post-record verdict. The continuum law is the mechanical refusal of this drift — proven executable twenty-two times, it must simply be executed again.

### 2. The Candidate Set Is Frozen Before S0, Never Improvised At It

R1–R8 are conditions, not predictions; a session decides, it never invents — and the terminal-state object is the hardest frozen object on the record: written by MP-40, executed by MP-41, consumed by MP-42... consumed a thirty-second time by MP-75, **consumed a thirty-third time by MP-76** — never re-negotiated in the consuming session.

### 3. MP-76 Is the Only Phase That Pays the MP-30–MP-36 Debt

Seven phases of pre-registered residue. `checklists/gate-debt.md` is the contract. Every row must be LAUNCHED-with-transcript or CLOSED-with-one-reason by Session 8. The clean-clone proof (MP-34 Row 1) is the Phase 6 gate — **if it's not green, nothing else ships**.

### 4. The Paper Is Written *From* Manifests, Not *To* Them

Reverse claims audit at zero: every sentence in the paper → manifest tag → JSON key → command that produced it. If the trace breaks, the claim is cut. This is not a writing exercise — it's a verification exercise.

### 5. The Receipt Compounds

The twenty-second runnable artifact is only worth shipping because the first twenty-one transcripts proved the format. My showcase's story is now "read it, run it, watch me be wrong on the record," twenty-two receipts deep.

### 6. The Steady State Is the Reward, Not the Ceremony

MP-76 is the twenty-fourth roadmap from an *executed* roadmap's release report — the program at its normal, confirmed twenty-four times. The machinery (ledgers, sessions, gate criteria) is now twenty-three executions deep; countermeasure: rows must still be dated in the session that owns them, verdicts consumed as artifacts, zero UNDECIDED rows at Session 8.

### 7. Stop-and-Publish Stays Open, Post-Record Criterion Twelve Questions Deep

ADR-0004's row 5 is the honest exit; a candidate set that cannot earn a paragraph the record lacks is a phase that should close itself. If the post-record arc governs, the deepest candidate earns the post-record arc's *eleventh new paragraph* — the record's closing sentence consumed twelve times, never repeated.

### 8. Toolchains Are Pinned in S0, Never Discovered at S7

The paper's compile gate is the hardest artifact; the v24 rule ("opens only for new numbers from MP-74/75") is the insurance that makes a missing toolchain a dated reason, not a crisis.

### 9. Protect the Release Report

The serialized stack means MP-29's release is the artifact everything downstream consumes; a slip at any link slides the whole chain. The deepest law still applies: a promise can be re-planned forever, but a dated row is answered.

### 10. The S0 Gate Is a Checklist with Receipts

ADR-0026 at zero, live URL, `verify-claims` at 0, twenty-first teaching transcript on disk — a condition with artifacts, not a paragraph.

### 11. The Negative Stays the Signature

The row that closes with one reason dated in the session that owns it is the strongest artifact in the repository. Every positive result has a negative twin that was measured, drafted, and stamped — the negative twin proves the positive wasn't cherry-picked.

### 12. Architectural Integrity Check for This Phase

The `src/results.py` manifest/verification machinery and `src/experiments/runner.py` multi-seed aggregation are the backbone — they are the contract, not the implementation. The checkpointing infrastructure in `src/experiments/checkpointing.py` must not be touched. The decoder-only transformer in `src/models/decoder_only_transformer.py` is frozen — all experiments use it as-is.

### 13. Reproducibility as a First-Class Citizen

Every figure, every number, every claim must trace back to a manifest and a command. The `make reproduce` target is the single source of truth for "what does this repo produce?" — if it drifts, the science drifts.

### 14. Post-MP-76: The Program Completes or Continues

Upon MP-76 release (target 2026-09-20), the program reaches its designed terminus. The capstone arc — **train a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns** — will have:

| Deliverable | Status at MP-76 Release |
|-------------|------------------------|
| Decoder-only transformer from scratch | ✅ Complete (MP-12) |
| Grokking flagship (Rung 2) | ✅ Executed on GPU, characterized (dense attractor or sparse Fourier) |
| Induction heads (Rung 1) | ✅ 10k-epoch boundary mapped |
| Superposition (Rung 3) | ✅ Reproducible baseline |
| Circuit patching (Rung 4) | ✅ Validated on real or synthetic head |
| SAE dashboard (Rung 5) | ✅ Deployed on HF Spaces |
| Mini-paper (LaTeX) | ✅ Compiled from manifests |
| Portfolio showcase | ✅ 5 project pages + live demo |
| Clean-clone reproducibility | ✅ Green (Phase 6 gate) |
| GitHub Pages + CI | ✅ Automated |

**If the program continues** (new research question earns the post-record arc's eleventh paragraph): MP-77 opens with ADR-0028, consumes MP-76's release report, and the thirty-fourth-generation arc begins.

**If the program completes**: The final merge is the twenty-third dated direction. The record closes with its measured boundaries, its failure cells mapped, its negative results shipped as contributions. The showcase stands: "read it, run it, watch me be wrong on the record."

---

## Part VIII — MP-76 Session 0 Gate Checklist (The Contract)

**MP-76 Session 0 cannot proceed until all are verified:**

| Gate | Verification Command | Expected |
|------|---------------------|----------|
| ADR-0026 at zero UNDECIDED | `cat docs/adr/0026-continuum-ledger-22.md` | All 8 rows LAUNCHED/CLOSED |
| Live URL accessible | `curl -sI <live_url> | head -1` | HTTP 200 |
| `verify-claims` at actual count | `make verify-claims` | Exit 0, count matches manifests |
| 21st teaching transcript on disk | `ls notebooks/teaching_artifact_v22.ipynb` | File exists |
| `dev == main` | `git diff origin/main origin/dev` | Empty |
| Clean-clone proof exists | `ls 06_production_ai/proofs/reproducible-from-clean-clone.md` | File exists |

**Only when all five gates pass does Session 0 open the intake table and stamp the thirty-third-generation consumption.**

---

**Written**: 2026-08-27  
**Perspective**: Personal study notes / learning log / portfolio showcase  
**Status**: Plan complete — ready for Session 0 consumption when MP-75 releases. Candidate set frozen, conditions explicit, no improvisation at S0. The capstone integration is the act of finally writing the honest record from the dated measurements; whatever they returned, the record is the contribution.