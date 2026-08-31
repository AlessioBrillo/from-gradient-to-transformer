---
tags: [type/moc, phase/7, research/experiment, state/roadmap]
created: 2026-08-31
consumes: [ADR-0024]
---

# Micro-Phase 75 — Post-GPU-Unblock Capstone Execution & Publication Roadmap

> **STATUS: PLANNING MODE.** This roadmap defines the work for MP-75 / ADR-0027, the micro-phase that begins immediately after MP-74 releases (target: 2026-09-06). It inherits a clean clone proof, a GPU grokking verdict (sparse or dense), an extended induction boundary, a neuron ablation characterization, a teaching artifact with stranger transcript, and a gate-debt ledger at zero UNDECIDED rows. My task is to execute the capstone research plan, ship the paper, deploy the interactive demos, and close the seven-phase arc.

---

## Part I — Where I Stand (Inherited State, Re-Verified at MP-75 Session 0)

### The Scientific Record at Handoff

The MP-74 release report (ADR-0024 at zero UNDECIDED) hands me the following dated facts:

| Artifact | State at 2026-09-06 | My Inheritance |
|----------|---------------------|----------------|
| **GPU Grokking (R1)** | 3-seed P=113 complete on Colab A100/T4; manifest on disk; `verify-claims` updated | **The verdict** — SPARSE-FOURIER or NO-GROK. This is the primary flagship result. |
| **Extended Induction (R2)** | 10k epochs ×3 seeds complete or killed with boundary documented | **The emergence boundary** — confirmed head or falsified hypothesis at standard scale. |
| **Neuron Ablation (R3)** | Figure + manifest entry on existing P=113 checkpoints | **The dense solution characterization** — graceful vs. catastrophic degradation curve. |
| **Clean-Clone Proof (R4)** | GREEN — transcript in `06_production_ai/proofs/reproducible-from-clean-clone.md` | **Phase 6 gate unlocked** — capstone research plan execution unblocked. |
| **SAE on Head Checkpoint (R5)** | Executed (if R2 produced head) or closed with reason | **Real-activation sparsity** — or honest negative documenting the dependency. |
| **Teaching Artifact v20 (R6)** | Shipped with stranger-runnable transcript | **Showcase receipt** — 19th runnable artifact, proves the format compounds. |
| **Paper v20 / Annex v20 (R7)** | Diff + scaffold **or** "v19 is the record" memo | **Publication decision** — new numbers or dated closure. |
| **Gate-Debt Ledger (R8)** | Complete or absent-with-date | **Phase 6/7 residue tracked** — MP-30 through MP-36 rows resolved or documented. |

### The Arc I'm Consuming (31st Generation)

```
MP-40 Ex-N → MP-41 → ... → MP-69 → MP-70 → MP-74 → **MP-75 (this phase)**
```

The consumption chain is now **thirty-first generation deep**. MP-75 Session 0 consumes MP-74's release report (ADR-0024 at zero) and adjudicates ADR-0027's candidate set. I stamp; I never re-decide.

### The Three Execution Lanes

MP-75 splits into three parallel lanes that must not borrow from each other:

| Lane | Scope | Owner | Terminus |
|------|-------|-------|----------|
| **Lane A: Science → Paper** | Capstone execution (Rung 2→5), paper prose from manifests, annex v21 | Research self | Paper v21 compiles; annex on live shelf |
| **Lane B: Infrastructure → Deploy** | W&B integration, HF Spaces SAE browser, Pages deploy, portfolio write-ups | Engineering self | All deploys green; portfolio projects documented |
| **Lane C: Closure → Release** | Gate-debt closure (MP-30–MP-36), final integration, `dev == main`, home wired | Release self | Merge green; program's 21st dated direction |

---

## Part II — Deep-Dive Study & Research Topics

Each reading below has: *the question it must answer*, *the prediction I write before reading*, *the primary source on disk*.

### 1. The Dense Attractor Derivation (Rung 2 → Paper Prose)

**Question**: *What is the mathematical structure of the dense modular addition solution, and how do I derive its generalization without sparse Fourier structure?*

- **Primary sources on disk**:
  - `03_deep_learning/notes/training-dynamics-and-grokking.md` — progress measures, phase transitions
  - `04_nlp_and_transformers/notes/superposition-and-feature-capacity.md` — superposition as alternative to sparsity
  - `06_production_ai/notes/dense-solutions-modular-addition.md` — my running derivation
  - `src/experiments/exp2_grokking.py` — `compute_progress_measures`, `analyze_fourier_sparsity`
- **Prediction to write before drafting**: The dense solution implements addition as a *distributed linear map* in the embedding space. The MLP acts as a learned interpolation table over the cyclic group. Generalization emerges when weight decay forces the embedding matrix into a low-rank circulant structure — not sparse DFT, but *implicit* Fourier via the circulant's eigenbasis. The neuron ablation curve (graceful) vs. Fourier ablation (catastrophic) proves the representation is distributed, not frequency-localized.
- **Output**: `06_production_ai/notes/dense-attractor-derivation.md` — runnable algebraic derivation with a test in `tests/test_dense_attractor.py`.

### 2. Induction Head Emergence at Scale (Rung 1 → Comparative Baseline)

**Question**: *At what (width, depth, data, compute) does the induction head phase transition actually occur, and how does fresh-batches data regime shift the boundary?*

- **Primary sources**:
  - `04_nlp_and_transformers/notes/induction-heads.md` — original Nanda/Jacobsen two-step path
  - `04_nlp_and_transformers/notes/induction-extended-run.md` — MP-74 R2 curves (Step 1/Step 2 trajectory)
  - `src/experiments/exp1_induction_heads.py` — `diagnose_induction_formation`, `KComposition`
  - Olsson et al. (2022), Liu et al. (2023) — memorization as competing attractor
- **Prediction**: At `d_model=64, 2-layer, 4 heads, fresh-batches`, the 10k-epoch run crosses the Step 1 → Step 2 threshold. Step 1 (L0 duplicate mass) forms by ~3k epochs; Step 2 (K-composition) requires the *copying head* to compose with the *duplicate head*, which only happens when the duplicate pattern is stable enough — a second-order phase transition. If still 0 heads at 10k, the boundary is at >10k or requires width >64.
- **Output**: Updated `induction-extended-run.md` with 10k curves; `figures/exp1_step1_step2_trajectory.png`.

### 3. SAE Sparsity Gap: Synthetic vs. Real Activations (Rung 5 → Frontier Showpiece)

**Question**: *Why does the SAE achieve 99.97% FVE at 17% sparsity (L0=136/256) on real activations vs. 97.5% FVE at 18% sparsity on synthetic? What does this say about feature geometry in undertrained vs. circuit-bearing models?*

- **Primary sources**:
  - `04_nlp_and_transformers/notes/superposition-and-feature-capacity.md` — feature capacity, superposition phase change
  - `src/experiments/exp5_sae_dashboard.py` — `SparseAutoencoder`, `harvest_activations_from_checkpoint`, `analyze_features`
  - Bricken et al. (2023), Cunningham et al. (2024), Templeton et al. (2024) — dead features, L0/FVE tradeoffs, dictionary scaling
- **Prediction**: The 32-dim residual stream from a 150–300 epoch model (no confirmed induction head) contains *no genuinely sparse features* — the SAE learns a dense overcomplete basis. Once R2 produces a checkpoint with real induction heads, the SAE on *that* checkpoint should show sparse features (L0 ~ 20–30) and the FVE/L0 curve should bend toward the synthetic baseline.
- **Output**: `figures/exp5_sparsity_tradeoff_real_vs_synthetic.png`; `portfolio/essay-annex-21.md` section on SAE sparsity gap.

### 4. Circuit Verification Methodology (Rung 4 → Causal Rigor)

**Question**: *How do I report activation patching / path patching results honestly given known confounds (layernorm denominator, subspace illusions, attribution patching linearity failure)?*

- **Primary sources**:
  - `04_nlp_and_transformers/notes/activation-patching.md`, `path-patching.md`, `qk-ov-circuits.md`
  - `src/experiments/exp4_circuit_patching.py` — `ActivationPatcher`, `PathPatcher`, `InductionHeadDetector`
  - Makelov, Lange & Nanda (2023) — layernorm denominator confound
  - Heimersheim & Janiak (2024) — circuit faithfulness metrics not robust
- **Prediction**: My circuit patching on the capstone model (or GPT-2-small) will recover the induction head pattern, but the *logit-difference recovery* metric will be inflated by layernorm scaling. I must report both raw recovery and denominator-corrected recovery, and explicitly state the approximation bounds.
- **Output**: `06_production_ai/notes/circuit-verification-honest-reporting.md` — methodology checklist for the paper.

### 5. The Post-Record Program, Tenth Generation (New, Deepest)

**Question**: *What does the record's ninth post-record verdict open?*

- **Primary sources**: Lakatos, *Methodology of Scientific Research Programmes* (1978) — read for the tenth time, now for the *ninth* question past a completed program.
- **Reading focus**: Progressive vs. degenerating problem shifts when the *ninth* post-record verdict lands; Kuhn's normal science as the post-record arc's axioms; the honest criterion for the tenth post-record question.
- **Output**: `00_meta/ADR-0027-post-record-tenth-question.md` — consumed by MP-76 Session 0.

### 6. The Record Teaches, Round Twenty

**Question**: *Can I distill the twentieth verdict into four registers without leakage?*

- **The four registers**: (1) Paper's sentence, (2) Annex's sentence, (3) 30-second spoken claim, (4) 5-minute teaching explanation with worked toy a stranger can run.
- **The leak**: The gap between registers 3 and 4 is where teaching leaks. I will write all four for the MP-74 verdict (dense attractor or sparse Fourier) and measure the delta.
- **Output**: `portfolio/teaching-distillation-20.md` — four registers side by side.

---

## Part III — Documentation Requirements (The Contract)

Everything MP-75 claims re-derives from a manifest and a command. The documentation I will write, and where:

| Artifact | Location | Trigger | Owner Lane |
|----------|----------|---------|------------|
| **ADR-0027** (candidate ledger, row verdicts, heartbeats) | `docs/adr/0027-continuum-ledger-21.md` | Session 0 (promoted from companion) | All |
| **Dense Attractor Derivation** | `06_production_ai/notes/dense-attractor-derivation.md` | Session 1 | Lane A |
| **Induction Extended Run v2** (10k curves + boundary) | `04_nlp_and_transformers/notes/induction-extended-run-v2.md` | Session 1 | Lane A |
| **SAE Real-Activation Report** | `06_production_ai/notes/sae-real-activation-report.md` | Session 2 (gated on R5) | Lane A |
| **Circuit Verification Honest Reporting** | `06_production_ai/notes/circuit-verification-honest-reporting.md` | Session 2 | Lane A |
| **Paper v21 Diff + Annex v21** | `portfolio/paper/main.tex` v21 + `portfolio/essay-annex-21.md` | Session 3 | Lane A |
| **W&B Integration Spec + Dashboard** | `06_production_ai/notes/wandb-integration.md` + live dashboard URL | Session 2 | Lane B |
| **HF Spaces SAE Browser Deploy** | `07_capstone/deploy/sae-browser/` + live Space URL | Session 3 (gated on R5) | Lane B |
| **Pages Deploy Workflow** | `.github/workflows/pages-deploy.yml` | Session 3 | Lane B |
| **Portfolio Project Write-ups** (5 rungs) | `portfolio/projects/rung-{1..5}/README.md` | Session 2–3 | Lane B |
| **Gate-Debt Closure Ledger** | `checklists/gate-debt.md` (final) | Session 4 | Lane C |
| **Final Integration Test Report** | `06_production_ai/proofs/final-integration.md` | Session 4 | Lane C |
| **MP-75 Release Report** (ADR-0027 at zero) | `00_meta/75_micro-phase-75-release-report.md` | Session 4 | Lane C |
| **Progress Log Entry** | `00_meta/03_progress-log.md` | Every session | All |

### Manifest Tags Required in RESULTS.md (Updated)

```markdown
<!-- manifest: results/exp1_induction_heads.json -->  (10k-epoch extended run)
<!-- manifest: results/exp2_grokking.json -->         (GPU 3-seed P=113 verdict)
<!-- manifest: results/exp3_superposition.json -->    (superposition phase change)
<!-- manifest: results/exp4_circuit_patching.json --> (causal verification on capstone/GPT-2)
<!-- manifest: results/exp5_sae_dashboard.json -->    (real activation from head checkpoint + synthetic baseline)
<!-- manifest: results/exp2_neuron_ablation.json -->  (dense solution characterization)
```

---

## Part IV — Practical Exercises & Hands-On Challenges

### Ex-1 · Capstone Research Plan Execution (Session 1–2, Lane A)

**Goal**: Execute the research plan from `07_capstone/research-plan.md` now that Phase 6 gate is green.

```bash
# Rung 2: Grokking — already complete (MP-74 GPU verdict). Write the dense attractor derivation.
# Rung 3: Superposition — already complete (exp3 figures on disk). Write the phase-change prose.
# Rung 4: Circuit Patching — run on capstone model (if grokking produced heads) or GPT-2-small.
uv run python -m src.experiments.exp4_circuit_patching \
  --model checkpoints/exp2_grokking_seed0.pt \
  --task induction \
  --output figures/exp4_capstone_circuit.png

# Rung 5: SAE Dashboard — run on confirmed head checkpoint (if R5 opened) or best available.
uv run python -m src.experiments.exp5_sae_dashboard \
  --activations-from checkpoints/exp1_induction_heads_seed0_10k.pt \
  --hooks ln_final --dict-size 256 --epochs 300 --seeds 0,1,2
```

**Falsifier**: If Rung 4 on capstone model finds no circuit → document honestly, run on GPT-2-small instead. If SAE on real activations still shows no sparsity → document the sparsity gap as the result.

---

### Ex-2 · Paper v21 from Manifests (Session 3, Lane A)

**Goal**: Every quantitative claim in the paper traces to a manifest tag in RESULTS.md.

```bash
# 1. Edit portfolio/paper/main.tex with prose derived from manifests
# 2. Every number in Results section has: <!-- manifest: results/expX.json -->
# 3. Verify compile (graceful if no TeX)
make paper

# 4. Run reverse claims audit: prose → manifest → command
python -m src.results verify
```

**Success Criterion**: `verify-claims` exits 0; `make paper` runs without error (or graceful fallback documented).

**Falsifier**: If a claim cannot be traced to a manifest → cut the claim or re-run the experiment.

---

### Ex-3 · W&B Integration + Live Dashboard (Session 2, Lane B)

**Goal**: Connect the experiment stack to Weights & Biases for live tracking.

```bash
# 1. Add W&B init to runner.py and experiment entry points
# 2. Log: loss curves, progress measures, Fourier sparsity, induction metrics
# 3. Create dashboard with panels: grokking curve, induction emergence, SAE tradeoff
# 4. Document API key handling (env var only, never in code)
```

**Deliverable**: `06_production_ai/notes/wandb-integration.md` with setup instructions; live dashboard URL in RESULTS.md.

**Falsifier**: If W&B API unavailable → document as known limitation, proceed with local tensorboard.

---

### Ex-4 · Hugging Face Spaces SAE Browser Deploy (Session 3, Lane B)

**Goal**: Deploy interactive SAE feature browser to HF Spaces.

```bash
# 1. Prepare SAE checkpoint + feature metadata from exp5
# 2. Build minimal Gradio app: feature index → activation histogram + top-activating examples
# 3. Push to HF Space (CPU basic tier)
# 4. Link from portfolio README and paper
```

**Structure**:
```
07_capstone/deploy/sae-browser/
├── app.py              # Gradio app
├── requirements.txt
├── README.md
└── sae_checkpoint.pt   # (downloaded at runtime from HF Hub or embedded if small)
```

**Success Criterion**: Space builds green; `/embed` works in portfolio.

---

### Ex-5 · GitHub Pages Deploy Workflow (Session 3, Lane B)

**Goal**: Automated deployment of portfolio site to GitHub Pages.

```yaml
# .github/workflows/pages-deploy.yml
name: Deploy Portfolio
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci && npm run build  # or python static site gen
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./portfolio/_site
```

**Deliverable**: Live portfolio at `https://alessiobrillo.github.io/from-gradient-to-transformer/`

---

### Ex-6 · Portfolio Project Write-ups (5 Rungs) (Session 2–3, Lane B)

**Goal**: Each rung gets a `portfolio/projects/rung-N/README.md` with:

```markdown
# Rung N: [Title]

## Headline
One-sentence result.

## Method
- Model / task / scale
- Key metric / visual

## Result
- Figure (linked from `figures/`)
- Manifest tag: `<!-- manifest: results/expN.json -->`

## What I Added Beyond Original
One sentence — the distinctiveness gate.

## Honest Caveats
Seed sensitivity, known limits, scope.
```

**Rungs to document**:
1. Induction Heads (exp1)
2. Grokking Modular Addition (exp2) — **primary flagship**
3. Toy Models of Superposition (exp3)
4. Circuit Verification via Activation Patching (exp4)
5. SAE Feature Dashboard (exp5)

---

### Ex-7 · Gate-Debt Closure (Session 4, Lane C)

**Goal**: Close all MP-30–MP-36 rows with transcripts or dated reasons.

```bash
# For each row in checklists/gate-debt.md:
# 1. If LAUNCHED → attach transcript link / commit SHA
# 2. If CLOSED → write one-sentence reason with date
# 3. If still PENDING → escalate to MP-76 or close with "superseded by MP-75 decision: [reason]"

# Final state: every cell has LAUNCHED-with-transcript or CLOSED-with-one-reason
```

**Falsifier**: A claimed closure without its transcript blocks Session 4 completion.

---

### Ex-8 · Final Integration & Release Rehearsal (Session 4, Lane C)

**Goal**: Full clean-clone → sync → reproduce → verify → test → lint → typecheck → paper → deploy.

```bash
# In a fresh temp directory:
git clone https://github.com/AlessioBrillo/from-gradient-to-transformer
cd from-gradient-to-transformer
uv sync --frozen
make reproduce-quick
make verify-claims
pytest
ruff check src/
python -m mypy src/results.py src/experiments/runner.py --strict
make paper  # graceful
# Verify HF Space builds, Pages workflow triggers
```

**Success Criterion**: All commands exit 0; `dev == main`; home wired; MP-75 release report written.

---

### Ex-9 · The Arc Consumption, Thirty-First Generation (Session 0, Verdict-Agnostic)

**Exercise**: Write the Ex-T memo that consumes MP-74's release report with dates, adjudicates ADR-0027's candidate set, and stamps the 31st generation consumption.

```markdown
# Ex-T: MP-75 Session 0 Arc Consumption

## Consumed
- MP-74 release report: ADR-0024 at zero UNDECIDED rows (dated 2026-09-06)
- GPU Grokking verdict: [SPARSE-FOURIER | NO-GROK] (dated)
- Extended Induction boundary: [confirmed head | falsified at 10k] (dated)
- Neuron Ablation: [graceful | catastrophic] degradation (dated)
- Clean-clone proof: GREEN (dated 2026-08-27)
- Teaching Artifact v20: shipped with transcript (dated)
- Gate-Debt: complete or absent-with-date (dated)

## ADR-0027 Candidate Set (Frozen Here, Never Improvised)
| Row | Candidate | Opens Only If |
|-----|-----------|---------------|
| 1 | Capstone Research Plan Execution | Clean-clone proof GREEN (confirmed) |
| 2 | Paper Prose from Manifests | Paper v20 diff exists (from MP-74) |
| 3 | W&B Integration + Dashboard | Always (Phase 6 residue) |
| 4 | HF Spaces SAE Browser Deploy | R5 executed with confirmed head |
| 5 | Portfolio Project Write-ups | Figures exist for all 5 rungs (confirmed) |
| 6 | Pages Deploy Workflow | Paper v21 compiles |
| 7 | Final Integration & Release | Rows 1–6 complete |
| 8 | Gate-Debt Closure | All MP-30–MP-36 resolved |

## Decision Rule
Row 1 is the research row (capstone execution). Rows 2–8 are engineering/deploy rows.
If Row 4 (SAE deploy) is gated, it stays GATED with a dated reason.
Terminus: Release = merge + 14 calendar days (2026-09-20).
```

---

## Part V — Strategic Tips & Architectural Best Practices

### 1. The One-Question Law, Twenty-First Execution

A phase that opens two research questions is drift. MP-75 has **one research row** (Row 1: Capstone Execution). Rows 2–8 are engineering/deploy. The continuum law is the mechanical refusal of drift — proven executable twenty times, it must simply be executed again.

### 2. The Candidate Set Is Frozen at S0, Never Improvised

ADR-0027's eight rows are conditions, not predictions. MP-75 Session 0 writes them; subsequent sessions decide, never invent. The terminal-state object (ADR-0027) is the hardest frozen object on the record.

### 3. Three Lanes, Zero Borrowing

Lane A (Science), Lane B (Infrastructure), Lane C (Closure) run in parallel. A slip in Lane B (HF Spaces deploy) does not borrow a minute from Lane A (paper prose). The highest-leverage act: **protect Lane A's writing window** — the paper is the artifact everything downstream consumes.

### 4. The Receipt Compounds, Twentieth Time

The nineteenth teaching artifact shipped with a stranger transcript. The twentieth (this phase's portfolio write-ups + HF Space + Pages) compounds the receipt: **read it, run it, watch me be wrong on the record** — now twenty receipts deep. The showcase story is the discipline, not the results.

### 5. Toolchains Are Pinned in S0, Never Discovered at S4

- LaTeX: `make paper` is graceful, not green — document this in S0, don't discover it at S3.
- HF Spaces: verify build locally before push; `requirements.txt` pinned.
- Pages: workflow tested on a feature branch before main.
- W&B: API key in env var, tested in CI mirror.

### 6. The Negative Stays the Signature

Every positive result has a negative twin measured, drafted, stamped. The dense attractor derivation *is* the negative twin of the sparse Fourier expectation. The induction head boundary *is* the negative twin of the emergence hope. The SAE sparsity gap *is* the negative twin of the monosemanticity promise. **I ship the negative as loudly as the positive.**

### 7. Architectural Integrity Check for MP-75

| Component | Status | MP-75 Action |
|-----------|--------|--------------|
| `src/experiments/checkpointing.py` | Battle-tested (MP-12/28/74) | Do not touch unless falsification test fails |
| `src/experiments/runner.py` | Multi-seed aggregation backbone | Extend for W&B logging only |
| `src/results.py` | Manifest/verification contract | Extend for new manifest tags only |
| `src/models/decoder_only_transformer.py` | Core capstone model | Freeze; capstone experiments import only |
| `src/experiments/neuron_ablation.py` | New (MP-74) | Stabilize API; add to runner if reusable |

### 8. Reproducibility as a First-Class Citizen (Non-Negotiable)

Every figure, every number, every claim traces to a manifest and a command. `make reproduce` is the single source of truth. If it drifts, the science drifts.

### 9. The S0 Gate Is a Checklist with Receipts

ADR-0024 at zero, `verify-claims` at 0, 19th teaching transcript on disk, `dev == main` — these are conditions with artifacts, not paragraphs. MP-75 Session 0 verifies all four before opening ADR-0027.

### 10. Post-MP-75 Transition Planning (MP-76 / ADR-0028 Preview)

Upon MP-75 release (2026-09-20), MP-76 will inherit:

- **If paper v21 compiles + deploys green**: MP-76 = "The Showcase Tour" — conference submission prep, talk rehearsals, blog post series, external replication invites.
- **If any deploy fails**: MP-76 = "The Hardening Sprint" — fix the broken deploy, re-verify, re-release.
- **Either way**: The capstone is *done*. The seven-phase arc closes. The next question is not "what experiment next" but "what does this record teach?"

---

## Part VI — MP-75 Session Plan (4 Sessions, 14 Days)

| Session | Date Target | Focus | Exit Criteria |
|---------|-------------|-------|---------------|
| **S0** | 2026-09-06 | Arc consumption (31st gen); ADR-0027 frozen; lanes assigned | ADR-0027 committed; Session 1 tasks assigned per lane |
| **S1** | 2026-09-09 | Lane A: Dense attractor derivation + paper prose start; Lane B: W&B init + portfolio write-ups start; Lane C: Gate-debt audit | Derivation draft; W&B logging in runner; 2/5 portfolio write-ups drafted |
| **S2** | 2026-09-12 | Lane A: Rung 4/5 execution + SAE report; Lane B: HF Spaces SAE deploy + Pages workflow; Lane C: Gate-debt closure | SAE browser live; Pages workflow green; gate-debt at zero PENDING |
| **S3** | 2026-09-15 | Lane A: Paper v21 diff + Annex v21; Lane B: Final portfolio polish; Lane C: Integration rehearsal | `make paper` runs; all deploys green; integration test passes |
| **S4** | 2026-09-19 | Release rehearsal; ADR-0027 at zero; merge; home wired | **MP-75 releases**; 21st dated direction shipped |

---

## Part VII — The One Measured Line

**ADR-0027 at zero UNDECIDED rows on release day (2026-09-20), with:**
- Capstone research plan executed (Rungs 2–5) and reported in paper v21 from manifests
- W&B dashboard live; HF Spaces SAE browser live; GitHub Pages portfolio live
- Five portfolio project write-ups published with manifest-tagged figures
- Gate-debt ledger complete (MP-30–MP-36 all LAUNCHED-with-transcript or CLOSED-with-one-reason)
- `make reproduce` → `make verify-claims` → `pytest` → `ruff` → `mypy` → `make paper` all green (or graceful with dated reason)
- `dev == main`; home wired; the program's **twenty-first dated direction**

---

## Part VIII — Written as My Study Notes

**Written**: 2026-08-31  
**Perspective**: Personal study notes / learning log / portfolio showcase  
**Status**: Ready for MP-74 release (2026-09-06) → MP-75 Session 0 kickoff. The GPU unblock measured the primary flagship on its native hardware; MP-75 writes the record from that measurement, deploys the interactive receipts, and closes the seven-phase arc.

> *The science was in the measurement. The contribution is in the honest reporting. The showcase is in the discipline that made both auditable.*