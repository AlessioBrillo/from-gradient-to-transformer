---
tags: [type/moc, phase/7, research/experiment, state/roadmap]
created: 2026-09-09
consumes: [ADR-0028]
---

# Micro-Phase 91 — From Release to Premiere: Paper v20, Teaching v22, Public Arc Launch

> **STATUS: PLANNING — Session 0 freeze.** This roadmap consumes MP-90's release
> (ADR-0028 at zero unstamped rows, 223 tests green, `verify-claims=0`, 9 manifests)
> and defines the frozen candidate set for the paper completion and premiere launch.
> Zero new candidates after this file is committed.

## Showcase Framing

If you have 30 seconds: I build a decoder-only transformer from scratch, then
reverse-engineer the algorithms it learns. My strongest verified result is Rung 3's
superposition phase transition (10/20 → 20/20 features represented, regular pentagon
geometry at sparsity ≤0.1). My most honest result is Rung 2's NO-GROK negative
(P=113, val accuracy 1.0 across 3 seeds, Fourier dense k_99 = 111/113). My
capstone shakedown (2000 steps, joint modular+induction) found a dissociation:
induction reached 0.5041 accuracy while modular stayed at chance (0.0047) with
Fourier dense (k_99 = 98.1). The retune A/B (500-step arms, vocab-offset +
curriculum reweight) confirmed NO-MOVE — neither intervention moves modular off
chance. The dense attractor under joint training *is* the contribution. In MP-91 I
ship: the mini-paper (prose from manifests only), the teaching artifact v22
(stranger-run on fresh Colab), and the premiere (essay, thread, site, Space,
walkthrough — atomic launch with URL receipts).

## Part I — My State Review (Re-Verified Live, 2026-09-09)

| Dimension | Status | Evidence |
|-----------|--------|----------|
| **Branch** | `dev` synced with `origin/dev`, working tree clean | `git status` |
| **Tests** | 223 passing (98.9s) | `uv run pytest -v` |
| **Lint** | `ruff check src/ tests/` clean | |
| **Typecheck (blocking)** | `mypy src/results.py src/experiments/runner.py --strict` clean | CI gate |
| **Full-tree mypy** | 201 errors (non-blocking, tracked) | exit 1, no crash |
| **verify-claims** | 0 — all headline numbers manifest-backed | `uv run python -m src.results verify` |
| **Manifests on disk** | 9 (6 flagship + 3 retune probes) | `results/*.json` |
| **ADR-0028** | **Zero unstamped rows** — all 8 LAUNCHED or CLOSED-WITH-ONE-REASON | `docs/adr/0028-continuum-ledger-23.md` |
| **Portfolio** | 5 rung pages locked, manifest tags, `../../figures/` prefixes, ≥2 `[[links]]` each | `portfolio/projects/rung-{1..5}/index.md` |
| **Gate-debt** | 11/11 cells LAUNCHED-WITH-TRANSCRIPT or CLOSED-WITH-ONE-REASON | `checklists/gate-debt.md` |
| **W&B (Row 5)** | CLOSED-WITH-ONE-REASON — credentials not configured | `07_capstone/notes/mp-90-wandb-gpu-close.md` |
| **GPU P=113 (MP-74 Row 1)** | PENDING-EXTERNAL — 15+ days stale, no manifest | same note |
| **Paper (`portfolio/paper/main.tex`)** | Scaffold only — every section `% TODO` pointing at its manifest/proof | |
| **Teaching artifacts** | v18 shipped (MP-70); v22 gated on MP-91 Session 2 | |

What I trust, in order:
1. Rung 3's phase transition (10/20 → 20/20, pentagon geometry, multi-seed manifest)
2. Rung 2's NO-GROK negative (P=113, val 1.0×3, Fourier dense k_99=111/113, dated 2026-08-11)
3. Capstone shakedown dissociation (2000 steps: ind 0.5041, mod 0.0047, Fourier k_99 98.1 dense)
4. Rung 1's fixed-vs-fresh comparison (52.2% vs 0.05% — real, large, matched effect)
5. Rung 4's activation patching (~0.20 recovery, internally consistent with 0 heads)
6. Rung 5's synthetic SAE (97.5% FVE, 18.9% L0, architecturally simple)
7. Capstone runner — three crashes smarter (Fourier detach, resume WARNING, retune plumbing)

## Part II — Bottleneck Analysis

| Bottleneck | Why It Matters | Resolution Path |
|------------|----------------|-----------------|
| **Paper prose 100% TODOs** | Capstone artifact needs narrative spine | Write prose *from manifests only* — each section opens only for numbers that exist |
| **No PDF compilation rehearsed in CI** | `pdflatex` absent on CI; PDF is review artifact | Compile on Overleaf/local for release; document toolchain gap |
| **Teaching artifact v22 not built** | Stranger-run is reproducibility proof | Build from `checkpoints/exp6_capstone_seed0_step2000.pt`; test on fresh Colab |
| **Public arc channels unopened** | Premiere law requires same-sitting launch with URL receipts | Pre-draft all five; launch atomically at release merge |
| **GPU manifest missing** | Only path to scale verdict on primary flagship | Consume if lands, else close PENDING-EXTERNAL with dated reason |
| **Rung 1 standard-scale open** | Fresh-batches 800-epoch real but sub-standard | Next continuum ledger; paper cites 800-epoch as trustworthy scale |

## Part III — Deep-Dive Study Topics (Session −1 Waiting Window)

| # | Topic | Source | Why Now |
|---|-------|--------|---------|
| **S-1** | Dense attractor under joint training | Varma et al. (2023); Lyu et al. (2024) | Retune A/B falsified interference & schedule; dense solution is the contribution |
| **S-2** | Fourier progress measures at convergence | Nanda et al. (2023) §4–5 | k_99=111/113 at val 1.0 — "memorizing circuit that generalizes"? |
| **S-3** | Induction head formation thresholds | Olsson et al. (2022); Nanda & Jacobsen (2023) | 0.504 accuracy without detected head — circuitry or memorization? |
| **S-4** | SAE sparsity on undertrained models | Bricken et al. (2023); Cunningham et al. (2024) | 53% L0 on real activations — capacity limit or budget limit? |
| **S-5** | Honest negative result communication | Pineau et al. (2021); Nosek & Lakens (2014) | NO-GROK and NO-MOVE are positive-negatives — model rigorous publication |

## Part IV — Documentation Contract

| Artifact | Location | Trigger | Falsifier |
|----------|----------|---------|-----------|
| Paper prose v20 | `portfolio/paper/main.tex` | Session 1 | Section without manifest tag; number not in cited manifest |
| Paper references | `portfolio/paper/references.bib` | Session 1 | Missing citation for any claimed result |
| Teaching artifact v22 | `notebooks/mp-91-teaching-artifact-v22.ipynb` | Session 2 | Stranger-run fails; output ≠ manifest |
| Public essay | `portfolio/essay/grokking-dense-attractor.md` | Session 4 (launch) | No URL receipt; no manifest links |
| Twitter/X thread | `portfolio/threads/mp-91-premiere-thread.md` | Session 4 (launch) | No URL receipt; no dated verdict citations |
| Portfolio site deploy | `.github/workflows/pages.yml` → GitHub Pages | Session 4 (launch) | `curl -I` returns ≠ 200 |
| Twitter Space recording | `portfolio/space/mp-91-space.md` (with link) | Session 4 (launch) | No dated link; no transcript commitment |
| Walkthrough video | `portfolio/walkthrough/mp-91-walkthrough.md` (with link) | Session 4 (launch) | No dated link; video >10 min or missing 30-sec thesis |
| Release report | `00_meta/91_micro-phase-91-release-report.md` | Session 5 | Missing ADR-0028 stamp; verify-claims≠0 |
| ADR-0028 final | `docs/adr/0028-continuum-ledger-23.md` | Session 5 | Any row not LAUNCHED/CLOSED |

## Part V — Practical Exercises (Falsifiable Drills)

| Exercise | Description | Falsifier |
|----------|-------------|-----------|
| **Ex-1** | Write paper section from manifest bytes only | Number without manifest key in same paragraph |
| **Ex-2** | Stranger-run rehearsal on fresh Colab (incognito) | Any cell error; output ≠ manifest |
| **Ex-3** | Four-register distillation (paper, annex, 30-sec, 5-min) | Registers cite different numbers |
| **Ex-4** | Hostile click-through audit | One dangling reference blocks launch |
| **Ex-5** | LaTeX compilation proof | Compilation fails or PDF has `??` |
| **Ex-6** | Premiere atomic launch (5 URLs in one commit) | Channel launches early/late; URL missing |

## Part VI — Strategic Tips & Architectural Best Practices

1. **Paper = manifest index.** Every quantitative claim → manifest tag. No manifest = no claim.
2. **Negatives ship loudly.** NO-GROK (val 1.0 + dense Fourier) and NO-MOVE (modular below chance under both interventions) *are* contributions — they falsify sparse-circuit hypothesis at this scale.
3. **Teaching artifact = reproducibility proof.** Stranger on fresh Colab must get same Fourier k_99, K-comp trajectory, patching recovery.
4. **Premiere law: same-sitting launch.** Five channels (essay, thread, site, Space, walkthrough) = single atomic action. Pre-draft all; commit URLs in release merge.
5. **verify-claims = pre-flight gate.** Must be 0 after every numbers change.
6. **GPU watch = PENDING-EXTERNAL, not blocker.** Paper already states: "GPU verdict pending as scale follow-up, not the decision."
7. **Rung 1 standard-scale = next ledger.** 800-epoch comparison (52.2%) is trustworthy scale for this paper.
8. **Atomic checkpoint/resume = durability standard.** Kill drill proved bit-identical resume; teaching artifact must demonstrate this.

## Part VII — Frozen Candidate Set (Sessions 0–6)

| # | Candidate | Opens Only If | Kill-Date |
|---|-----------|---------------|-----------|
| 1 | **Paper prose v20 (all sections from manifests)** | Always (Session 0 done) | S2 |
| 2 | **Teaching artifact v22 (stranger-run ready)** | Paper v20 drafted | S3 |
| 3 | **LaTeX compilation proof + PDF** | Paper v20 complete | S4 |
| 4 | **Public arc pre-draft (5 channels)** | Paper v20 complete | S4 |
| 5 | **Premiere atomic launch (5 URLs + receipts)** | All pre-drafts ready | S5 |
| 6 | **Release merge (dev→main, home wired)** | All rows stamped | S6 |

## Part VIII — Step-by-Step Execution Plan

### Session 0 (This Commit) — Freeze Candidate Set
- [x] Write this roadmap
- [x] Freeze candidate set (table above) — **zero new candidates after this**
- [x] Verify baseline: 223 tests, ruff clean, blocking mypy clean, verify-claims=0, 9 manifests
- [x] Commit roadmap

### Session 1 — Paper Prose v20 (Manifest-to-Prose Pass)
- [ ] For each rung with manifest (Rungs 1–5 + capstone shakedown), write paper section from manifest bytes only
- [ ] Grokking: lead with NO-GROK (val 1.0, k_99=111/113), characterize dense attractor, cite MP-29 positive control (FALSIFIED), microscope (trial 1 FALSIFIED), retune A/B (NO-MOVE)
- [ ] Induction: lead with fixed-vs-fresh (52.2% vs 0.05%), 0/8 heads at this scale, standard-scale as "pending scale follow-up"
- [ ] Superposition: phase transition 10/20→20/20, pentagon geometry, root cause (no bottleneck)
- [ ] Circuit patching: activation patching ~0.20 recovery, path patching unit-tested only, 0 heads → ablation skipped
- [ ] SAE: synthetic 97.5% FVE / 18.9% L0; real 99.97% FVE / 53% L0 — read honestly as capacity/budget limit
- [ ] Capstone: shakedown dissociation as joint-training finding; retune A/B as falsification of interference/schedule
- [ ] Every number gets `<!-- manifest: results/<file>.json -->` tag
- [ ] **Exit**: `portfolio/paper/main.tex` all sections prose, `verify-claims=0`

### Session 2 — Teaching Artifact v22 (Stranger-Run Notebook)
- [ ] Build notebook from `checkpoints/exp6_capstone_seed0_step2000.pt` (MP-88 shakedown checkpoint)
- [ ] Pipeline: load → Fourier (k_99≈98) → K-comp (max≈0.39, `_vacuous`) → activation patching (~0.20) → path patching (unit test) → SAE on harvested (99.97% FVE, 53% L0) → literature → honest conclusion
- [ ] Include kill-drill demo (resume from step 1000 → bit-identical)
- [ ] Test on fresh Colab (incognito): `uv sync --frozen`, all cells green, outputs match manifests
- [ ] Commit notebook + Colab transcript
- [ ] **Exit**: stranger-run transcript committed; notebook executable from cold start

### Session 3 — LaTeX Compilation + Public Arc Pre-Draft
- [ ] `cd portfolio/paper && latexmk -pdf main.tex` → `main.pdf` clean
- [ ] If `pdflatex` absent: compile on Overleaf, download PDF, commit as build artifact
- [ ] Pre-draft five premiere channels:
    - **Essay**: "The Dense Attractor: Why My Transformer Solved Modular Addition Without Grokking" — 2000 words, cites exp2 + shakedown manifests
    - **Thread**: 12-tweet thread, each tweet = one manifest-backed number + insight
    - **Site**: GitHub Pages deploy via `pages.yml` — verify 200 OK
    - **Space**: Schedule Space for release week; prep 10-min talk script (from four-register distillation)
    - **Walkthrough**: 8-min screen-recorded video (thesis → Rung 2 NO-GROK → Rung 3 → capstone dissociation → retune NO-MOVE → teaching artifact)
- [ ] **Exit**: PDF exists; five pre-draft files ready to publish

### Session 4 — Premiere Atomic Launch
- [ ] Single sitting: Publish essay → commit URL; Post thread → commit URL; Deploy site → verify 200; Announce Space → commit link; Upload walkthrough → commit link
- [ ] All five URLs committed in *one commit*: `feat(portfolio): premiere launch — five channels live`
- [ ] Cross-link: essay ↔ thread ↔ site ↔ Space/walkthrough
- [ ] **Exit**: `portfolio/premiere-ledger.md` with five URLs + timestamps; `verify-claims=0`

### Session 5 — Release Preparation
- [ ] Final `verify-claims=0`, 223 tests pass, ruff clean, blocking mypy clean
- [ ] Update `00_meta/00_home.md` with MP-91 pointer
- [ ] Update `00_meta/03_progress-log.md` with Session 5 entry
- [ ] ADR-0028 final verification: all 8 rows LAUNCHED or CLOSED-WITH-ONE-REASON
- [ ] **Exit**: release-ready commit on `dev`

### Session 6 — Release Merge
- [ ] PR `dev` → `main` with conventional commit `merge(capstone): mp-91 release — paper v20, teaching v22, premiere launched`
- [ ] GPG sign; CI green (pytest, ruff, blocking mypy, commitlint)
- [ ] `dev == main` confirmed
- [ ] Write release report `00_meta/91_micro-phase-91-release-report.md`
- [ ] **Exit**: merge complete; next dated direction (MP-92 / ADR-0029)

## Part IX — Terminus Definition

MP-91 terminates at Session 6 release merge when:
- ✅ Paper v20 compiles to PDF with all manifested numbers
- ✅ Teaching artifact v22 stranger-run passes on fresh Colab
- ✅ Premiere five channels launched atomically with URL receipts
- ✅ `verify-claims = 0`, 223 tests pass, ruff clean, blocking mypy clean
- ✅ ADR-0028 at zero unstamped rows
- ✅ `dev == main`, home wired to MP-91

Then the continuum law executes: ADR-0029 opens with exactly one new research question from frozen candidate set (C1: solution-regime phase diagram; C2: scaled R1 induction; C3: SAE on confirmed-head checkpoint; C4: ACDC on real circuit). Unchosen three close with dated reasons in same sitting.

## Links

- MP-90 release report — `00_meta/90_micro-phase-90-release-report.md`
- MP-89 retune verdict — `07_capstone/notes/mp-89-retune-verdict.md`
- MP-88 shakedown verdict — `07_capstone/notes/mp-88-shakedown-verdict.md`
- ADR-0028 — `docs/adr/0028-continuum-ledger-23.md`
- Portfolio RESULTS — `portfolio/RESULTS.md`
- Paper scaffold — `portfolio/paper/main.tex`
- Capstone README — `07_capstone/README.md`
- Research plan — `07_capstone/research-plan.md`

---

**Written**: 2026-09-09  
**Perspective**: My personal study notes, learning log, and portfolio showcase  
**Status**: PLANNING — Session 0 complete, candidate set frozen