---
tags: [checklist, phase/6]
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
- [ ] **Experiment tracking:** W&B for loss curves, progress measures, hyperparameter sweeps
- [~] **`make reproduce` for every experiment** — pre-existing target regenerates all
  figures; `make reproduce-multiseed` (exp1/exp3/exp4) added 2026-08-02, not yet exp2/exp5.
- [~] **CI for research:** GitHub Actions running fast smoke tests on every push —
  pre-existing; 2026-08-02 fixed a `python-version` mismatch (3.11 pinned vs. 3.12
  resolved) and split the mypy step so a genuine crash (exit 2) fails the build instead of
  being swallowed by `|| true` alongside ordinary reported errors (exit 1).
- [~] **Figure generation scripts:** every figure has a deterministic generating script;
  `portfolio/figures/` established as the committed curated set, enforced mechanically by
  `make verify-claims` (existence + git-tracking check added 2026-08-07, Micro-Phase 12 Step
  1, falsified against the real pre-fix state — see
  [[06_production_ai/notes/figure-provenance-and-evidence-gates]],
  [[06_production_ai/exercises/ex-05-falsify-the-figure-gate]]). Not yet flipped to `[x]`:
  the curated figures aren't committed yet (`make verify-claims` still reports them
  untracked), and two sections (Rung 2, Rung 5) have no manifest to tag at all — a real gap,
  not a bug in the check.
- [ ] **Feature dashboard deployment:** Hugging Face Spaces for SAE feature browser
- [~] **Mini-paper workflow:** LaTeX template, `make paper`, citation management —
  `portfolio/paper/main.tex` + `references.bib` scaffold added 2026-08-02; structure only,
  no prose.

## Light Touch (context)
- [ ] Data versioning (DVC / lakeFS) — for large activation datasets
- [ ] Containerization (Docker) — for reproducible experiment environments
- [ ] System design doc — for the capstone pipeline
- [ ] Security / privacy / governance — GDPR compliance, PII handling in datasets
