---
tags: [type/moc, phase/7, research/experiment, state/roadmap]
created: 2026-09-19
consumes: [ADR-0029]
---

# Micro-Phase 93 — Solution-Regime Phase Diagram: When Does Grokking Occur?

> **STATUS: PLANNING — Session 0 freeze.** This roadmap consumes MP-92's release state (ADR-0028 at zero unstamped rows, 223 tests green, `verify-claims=0`, 12 manifests, premiere pre-drafts committed) and defines the frozen candidate set for the phase diagram sweep. Zero new candidates after this file is committed.

## Showcase Framing

If you have 30 seconds: I systematically map the phase boundary between **sparse Fourier circuit** (the grokking mechanism Nanda et al. describe) and **dense attractor** (what my protocol actually produces) across modulus P, model size, weight decay, LR schedule, embedding renormalization, and solo vs joint training. My strongest verified result remains Rung 3's superposition phase transition (10/20 → 20/20 features, pentagon geometry at sparsity ≤0.1). My most honest result is Rung 2's NO-GROK negative (P=113, val accuracy 1.0 across 3 seeds, Fourier dense k_99 = 111/113). In MP-93 I ship: the phase diagram heatmap with analytical boundary characterization, the paper section "When Does Grokking Occur?", and the next continuum ledger (ADR-0030) with exactly one new research question.

## Part I — My State Review (Re-Verified Live, 2026-09-18)

| Dimension | Status | Evidence |
|-----------|--------|----------|
| **Branch** | `main` synced with `origin/main`, working tree clean | `git status` |
| **Tests** | 223 passing (62.98s) | `uv run pytest -x -q` |
| **Lint** | `ruff check src/ tests/` clean | |
| **Typecheck (blocking)** | `mypy src/results.py src/experiments/runner.py --strict` clean | CI gate |
| **Full-tree mypy** | 201 errors (non-blocking, tracked) | exit 1, no crash |
| **verify-claims** | 0 — all headline numbers manifest-backed | `uv run python -m src.results verify` |
| **Manifests on disk** | 12 (6 flagship + 3 retune + 3 fix/resume) | `results/*.json` |
| **Capstone checkpoints** | 4 (steps 500, 1000, 1500, 2000, seed 0) | `checkpoints/*.pt` |
| **ADR-0028** | Zero unstamped rows — all 8 LAUNCHED or CLOSED-WITH-ONE-REASON | `docs/adr/0028-continuum-ledger-23.md` |
| **ADR-0029** | OPEN — Row 1: Solution-regime phase diagram (C1 SELECTED) | `docs/adr/0029-continuum-ledger-24.md` |
| **Portfolio** | 5 rung pages locked, manifest tags, `../../figures/` prefixes, ≥2 `[[links]]` each | `portfolio/projects/rung-{1..5}/index.md` |
| **Gate-debt** | 11/11 cells LAUNCHED-WITH-TRANSCRIPT or CLOSED-WITH-ONE-REASON | `checklists/gate-debt.md` |
| **Premiere pre-drafts** | 5 channels committed in `1e5e301` | `portfolio/premiere-ledger.md` |

What I trust, in order:
1. Rung 3's phase transition (10/20 → 20/20, pentagon geometry, multi-seed manifest)
2. Rung 2's NO-GROK negative (P=113, val 1.0×3, Fourier dense k_99=111/113, dated 2026-08-11)
3. Capstone shakedown dissociation (2000 steps: ind 0.5041, mod 0.0047, Fourier k_99 98.1 dense)
4. Rung 1's fixed-vs-fresh comparison (52.2% vs 0.05% — real, large, matched effect)
5. Rung 4's activation patching (~0.20 recovery, internally consistent with 0 heads)
6. Rung 5's synthetic SAE (97.5% FVE, 18.9% L0, architecturally simple)

## Part II — Bottleneck Analysis

| Bottleneck | Why It Matters | Resolution Path |
|------------|----------------|-----------------|
| **No GPU access for P=113 sweeps** | Phase diagram needs multi-seed at P=113 for statistics; CPU 3-seed × 20k steps ≈ 10h per cell | Run CPU-feasible sweeps (small P, reduced steps) first; characterize boundary analytically; GPU run consumed as data point if it lands |
| **Exponential parameter space** | 7 (P) × 12 (model sizes) × 5 (wd) × 3 (schedule) × 2 (renorm) × 2 (mode) = 5,040 cells | Structured factorial design: fix non-critical dims, sweep critical ones first; use theoretical boundary to prune |
| **Dense attractor = default** | Every run in repo history has been dense (k_99 ≈ P); sparse regime may not exist for this protocol | Lead with negative: characterize dense regime thoroughly, prove boundary conditions analytically, only then claim sparse regime reachable |
| **No ground-truth sparse run to validate against** | Can't verify phase diagram's "sparse" label without at least one confirmed sparse Fourier run | Use MP-29 positive control (P=59/67/97 at 1500-3000 epochs) as existence proof if it produces sparse; else label boundary as "theoretical" |
| **Joint vs solo interaction complex** | Capstone shakedown showed joint training suppresses modular (0.0047) while induction takes off (0.5041) | Treat joint/solo as separate sub-diagrams; characterize interaction as shift in boundary |

## Part III — Deep-Dive Study Topics (Session −1 Waiting Window)

| # | Topic | Source | Why Now |
|---|-------|--------|---------|
| **S-1** | Phase transitions in overparameterized models | Varma et al. (2023); Lyu et al. (2024) | Dense attractor is the contribution; need theoretical framework for boundary |
| **S-2** | Fourier progress measures at convergence | Nanda et al. (2023) §4–5 | k_99=111/113 at val 1.0 — "memorizing circuit that generalizes" or distinct mechanism? |
| **S-3** | Induction head formation thresholds | Olsson et al. (2022); Nanda & Jacobsen (2023) | Joint training produced 0.504 induction accuracy without detected head — circuitry or memorization? |
| **S-4** | Weight decay as sparsity control | Nakkiran et al. (2021); Power et al. (2022) | WD=1.0 is grokking standard; my sweep must test WD as primary sparse/dense knob |
| **S-5** | Honest negative result communication | Pineau et al. (2021); Nosek & Lakens (2014) | If phase diagram shows sparse regime unreachable at this protocol, that IS the paper |
| **S-6** | Experimental design for factorial sweeps | Box et al. (1978); domain-specific MI papers | 5,040 cells impossible; need principled subsampling + theoretical interpolation |

## Part IV — Documentation Contract

| Artifact | Location | Trigger | Falsifier |
|----------|----------|---------|-----------|
| Phase diagram manifest | `results/phase_diagram.json` | Session 2 | Missing cell; measurement not in {val_acc, gen_epoch, k_99/P, sparsity, ablation_curve} |
| Phase diagram heatmap | `figures/phase_diagram_heatmap.png` | Session 3 | File missing; no manifest tag in RESULTS.md |
| Phase boundary analysis | `figures/phase_boundary_analysis.png` | Session 3 | No theory-vs-empirical overlay |
| Paper section | `portfolio/paper/main.tex` (Grokking section v21) | Session 4 | Section without manifest tag; number not in cited manifest |
| ADR-0030 | `docs/adr/0030-continuum-ledger-25.md` | Session 5 | Any row not LAUNCHED/CLOSED; >1 research question selected |

## Part V — Practical Exercises (Falsifiable Drills)

| Exercise | Description | Falsifier |
|----------|-------------|-----------|
| **Ex-1** | Implement factorial sweep runner with JSON manifest output | Cell without 3-seed aggregate; manifest missing required keys |
| **Ex-2** | Reproduce MP-29 positive control (P=59) at standard config | val_acc < 0.9 OR k_99/P > 0.5 |
| **Ex-3** | Analytical boundary derivation (WD × P × d_model) | Derivation doesn't match empirical boundary within 2× |
| **Ex-4** | Dense attractor characterization: per-head Fourier dictionary + norm structure | Analysis claims sparse features where k_99/P > 0.5 |
| **Ex-5** | Kill drill: interrupt sweep, resume, verify bit-identical continuation | Resumed cell produces different k_99 trajectory |
| **Ex-6** | Hostile click-through audit of phase diagram figures | One dangling reference; figure not git-tracked |

## Part VI — Strategic Tips & Architectural Best Practices

1. **Phase diagram = manifest index + theory boundary.** Every cell → manifest tag. Theory boundary derived from weight decay × model capacity × data density. No manifest = no cell in heatmap.

2. **Dense is the default; sparse is the exception.** Lead with what you found (dense attractor stable across P=11..113, solo and joint). Sparse regime exists only if positive control produces it. If not, the paper section is "Why Grokking Didn't Occur: A Phase Diagram of the Dense Attractor."

3. **Factorial design beats grid search.** Fix non-critical dims (seq_len=128, batch_size=128, cosine LR, warmup=1000, ReLU, MHA, RoPE). Sweep: P × {d_model, n_layers} × WD × {solo, joint}. Renormalization and LR schedule as 2×2 follow-up only if boundary unclear.

4. **Three seeds per cell minimum.** Single-seed phase diagrams are noise, not science. CPU budget: 3 seeds × 2000 steps × ~20 cells = ~12h. Prioritize cells near theoretical boundary.

5. **Measurements per cell must be uniform.** Every cell: final val_acc, generalization epoch (first >0.9), k_99/P ratio, normalized Fourier entropy, ablation curve (acc vs k_kept). No ad-hoc metrics.

6. **Joint training = separate sub-diagram.** The dissociation (ind 0.5041, mod 0.0047) means joint mode has its own boundary. Plot solo and joint as side-by-side heatmaps with shared axes.

7. **verify-claims = gate before every commit touching numbers.** Must be 0 after each session's manifest writes.

8. **GPU P=113 = data point, not blocker.** If GPU run lands during MP-93, incorporate as single cell at P=113, d_model=256, 4L, joint. If NO-GROK, it extends dense regime. If SPARSE, it becomes the anchor for sparse regime existence.

9. **Paper section writes from manifests only.** "When Does Grokking Occur?" opens only for cells that exist. Theory boundary plotted as dashed line; empirical cells as dots with error bars.

## Part VII — Frozen Candidate Set (Sessions 0–6)

| # | Candidate | Opens Only If | Kill-Date |
|---|-----------|---------------|-----------|
| 1 | **Factorial sweep runner + CPU-feasible cells** | Always (Session 0 done) | S2 |
| 2 | **Positive control reproduction (P=59/67/97)** | Runner ready | S2 |
| 3 | **Full phase diagram sweep (20 cells × 3 seeds)** | Positive control reproduced OR S2 timeout | S4 |
| 4 | **Analytical boundary derivation + theory-vs-empirical figure** | Sweep data available | S4 |
| 5 | **Paper section v21 "When Does Grokking Occur?"** | Heatmap + boundary figure ready | S5 |
| 6 | **ADR-0030 + release merge (main)** | All rows stamped, verify-claims=0 | S6 |

## Part VIII — Step-by-Step Execution Plan

### Session 0 (This Commit) — Freeze Candidate Set
- [x] Write this roadmap
- [x] Freeze candidate set (table above) — **zero new candidates after this**
- [x] Verify baseline: 223 tests, ruff clean, blocking mypy clean, verify-claims=0, 12 manifests
- [x] Commit roadmap

### Session 1 — Sweep Runner + Positive Control
- [ ] Build `scripts/phase_diagram_sweep.py`: consumes YAML grid, runs cells with 3 seeds, emits `results/phase_diagram.json` manifest with per-cell aggregates
- [ ] Runner must: resume from partial manifest, skip completed cells, bit-identical resume (kill drill validated in MP-87)
- [ ] Reproduce MP-29 positive control: P=59 at standard config (d_model=128, 4H, d_mlp=512, WD=1.0, cosine, 5000 epochs) × 3 seeds
- [ ] **Exit**: positive control manifest shows sparse (k_99/P < 0.5) OR dense with dated reason; runner passes kill drill

### Session 2 — CPU-Feasible Sweep (Core Grid)
- [ ] Execute core factorial grid on CPU:
  - P ∈ {11, 17, 29, 59, 97, 113} (6)
  - Model: {d_model=64/128/256} × {n_layers=1/2} (6)
  - WD ∈ {0.1, 0.5, 1.0, 1.5, 2.0} (5)
  - Mode: {solo, joint} (2)
  - **Total: 6 × 6 × 5 × 2 = 360 cells → SUBSAMPLE to ~20 critical cells near theoretical boundary**
- [ ] Subsampling strategy: fix n_layers=1, d_model=128 for P-sweep; fix P=59 for model-size sweep; fix P=113 for WD sweep; joint only at P=113, d_model=128
- [ ] Each cell: 3 seeds, 2000 steps (or 5000 for P≤59), checkpoint-every=500
- [ ] **Exit**: `results/phase_diagram.json` with ≥20 cells × 3 seeds; verify-claims=0

### Session 3 — Figures + Boundary Analysis
- [ ] Generate `figures/phase_diagram_heatmap.png`: sparse/dense classification (k_99/P < 0.5 = sparse) as heatmap P × WD (solo) and P × WD (joint)
- [ ] Generate `figures/phase_boundary_analysis.png`: theoretical boundary (derived from WD × capacity × data density) vs empirical cells
- [ ] Characterize dense attractor: per-head Fourier dictionary norms, ablation curves, K-comp trajectories for joint cells
- [ ] **Exit**: both figures committed, git-tracked, manifest tags in RESULTS.md

### Session 4 — Paper Section v21
- [ ] Write `portfolio/paper/main.tex` Grokking section v21 from manifests only
- [ ] Lead with NO-GROK (val 1.0, k_99=111/113), then phase diagram as systematic characterization
- [ ] If positive control sparse: "sparse regime exists at small P, suppressed at P=113 by dense attractor; boundary at P≈60, WD≈1.0"
- [ ] If positive control dense: "dense attractor is universal for this protocol; no sparse regime found across P=11..113, WD=0.1..2.0, model sizes up to 4L/256"
- [ ] Every number → `<!-- manifest: results/phase_diagram.json -->` with cell coordinates
- [ ] **Exit**: section prose complete; verify-claims=0

### Session 5 — ADR-0030 + Release Prep
- [ ] Final verify-claims=0, 223 tests pass, ruff clean, blocking mypy clean
- [ ] ADR-0030: single row from frozen candidate set for next ledger:

  | Candidate | Description |
  |-----------|-------------|
  | **C1** | Scaled Rung 1 induction (standard config, GPU, multi-seed) |
  | **C2** | SAE on confirmed-head checkpoint (if C1 produces heads) |
  | **C3** | ACDC on real circuit (if C1+C2 produce verified circuit) |
  | **C4** | Joint training phase diagram at scale (GPU, d_model=512, 8L) |

- [ ] Update `00_meta/00_home.md` with MP-93 pointer
- [ ] Update `00_meta/03_progress-log.md` with Session 5 entry
- [ ] **Exit**: release-ready commit on `main`

### Session 6 — Release Merge
- [ ] Fast-forward merge already on `main` (no PR needed — MP-92 merged to main)
- [ ] Tag `mp-93-release` with GPG signature
- [ ] Write release report `00_meta/93_micro-phase-93-release-report.md`
- [ ] **Exit**: tag pushed; home wired to MP-93; next dated direction (ADR-0030)

## Part IX — Terminus Definition

MP-93 terminates at Session 6 when:
- ✅ `results/phase_diagram.json` manifest with ≥20 cells × 3 seeds, all required measurements
- ✅ `figures/phase_diagram_heatmap.png` + `figures/phase_boundary_analysis.png` committed and git-tracked
- ✅ Paper section v21 written from manifests only, `verify-claims=0`
- ✅ ADR-0030 at zero UNDECIDED rows with exactly ONE research question selected
- ✅ 223 tests pass, ruff clean, blocking mypy clean
- ✅ Tag `mp-93-release` on `main`; home wired to MP-93

Then the continuum law executes: ADR-0030 opens with exactly one new research question from frozen candidate set (C1–C4). Unchosen three close with dated reasons in same sitting.

## Links

- MP-92 release report — `00_meta/92_micro-phase-92-release-report.md`
- ADR-0029 (this phase's ledger) — `docs/adr/0029-continuum-ledger-24.md`
- ADR-0028 (consumed ledger) — `docs/adr/0028-continuum-ledger-23.md`
- Portfolio RESULTS — `portfolio/RESULTS.md`
- Capstone shakedown verdict — `07_capstone/notes/mp-88-shakedown-verdict.md`
- Retune A/B verdict — `07_capstone/notes/mp-89-retune-verdict.md`
- Grokking NO-GROK verdict — `06_production_ai/notes/grokking-verdict-p113.md`

---

**Written**: 2026-09-19  
**Perspective**: My personal study notes, learning log, and portfolio showcase  
**Status**: PLANNING — Session 0 complete, candidate set frozen