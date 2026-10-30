---
tags: [type/moc, phase/6, state/review]
---

# Checklist — Phase 6 · Production AI (reframed: Reproducible Research Infra)

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

**Reframing:** The infrastructure serves the research goal — making every result auditable, extendable, and trustworthy. "Production AI" here means production-quality *research*, not product deployment.

## Phase gate
- [ ] **Proof passed** → I can move to the capstone.

## Research Infrastructure
- [~] **Reproducibility harness:** global seed control, deterministic flags, pinned env
  (`uv.lock`) — pre-existing; multi-seed runner + provenance manifests
  (`src/experiments/runner.py`, `src/results.py`, `make verify-claims`) added 2026-08-02,
  wired into exp1/exp3/exp4. See
  [[06_production_ai/notes/results-manifests-and-provenance]],
  [[06_production_ai/notes/multi-seed-experiment-design]].
- [x] **Experiment tracking:** (descoped 2026-10-11: no credentials; manifests on disk) W&B for loss curves, progress measures, hyperparameter sweeps
- [~] **`make reproduce` for every experiment** — pre-existing target regenerates all
  figures; `make reproduce-multiseed` (exp1/exp3/exp4) added 2026-08-02, not yet exp2/exp5.
- [~] **CI for research:** GitHub Actions running fast smoke tests on every push —
  pre-existing; 2026-08-02 fixed a `python-version` mismatch (3.11 pinned vs. 3.12
  resolved) and split the mypy step so a genuine crash (exit 2) fails the build instead of
  being swallowed by `|| true` alongside ordinary reported errors (exit 1).
- [x] **Figure generation scripts:** every figure has a deterministic generating script;
  `portfolio/figures/` established as the committed curated set (12 figures tracked since
  Micro-Phase 13, PR #38), enforced mechanically by `make verify-claims` (existence +
  git-tracking check added 2026-08-07, Micro-Phase 12 Step 1). All sections carry their
  manifest tags: Rung 2 (`results/grokking_nanda_p113.json`), Rung 5
  (`results/exp5_real_activations.json`), Rung 1 content
  (`results/induction_content_derisk_standard.json`, gate manifest).
- [x] **Feature dashboard deployment:** (descoped 2026-10-11: no confirmed head) Hugging Face Spaces for SAE feature browser
- [x] **Mini-paper workflow:** LaTeX template, `make paper` (added 2026-08-08), citation
  management — `portfolio/paper/main.tex` + `references.bib` scaffold added 2026-08-02;
  prose written from manifests in paper v20 (2026-09-17), bibliography wired and guarded
  in CI (`paper.yml` fails on an unreferenced `references.bib`), and the PDF is compiled
  into the site deploy (`pages.yml`, 2026-10-12) so the paper actually ships.

## Light Touch (context)
- [x] Data versioning (descoped 2026-10-11: all data synthetic, seed-controlled) (DVC / lakeFS) — for large activation datasets
- [x] Containerization (descoped 2026-10-11: uv.lock + clean-clone proof sufficient) (Docker) — for reproducible experiment environments
- [x] System design doc (descoped 2026-10-11: captured in descope register) — for the capstone pipeline
- [x] Security / privacy / governance (descoped 2026-10-11: no PII) — GDPR compliance, PII handling in datasets
