---
tags: [checklist, phase/6]
---

# Checklist — Phase 6 · Production AI (reframed: Reproducible Research Infra)

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

**Reframing:** The infrastructure serves the research goal — making every result auditable, extendable, and trustworthy. "Production AI" here means production-quality *research*, not product deployment.

## Phase gate
- [ ] **Proof passed** → I can move to the capstone.

## Research Infrastructure
- [ ] **Reproducibility harness:** global seed control, deterministic flags, pinned env (`uv.lock`)
- [ ] **Experiment tracking:** W&B for loss curves, progress measures, hyperparameter sweeps
- [ ] **`make reproduce` for every experiment** — one command regenerates all figures and tables
- [ ] **CI for research:** GitHub Actions running fast smoke tests on every push
- [ ] **Figure generation scripts:** every figure committed with its deterministic generator
- [ ] **Feature dashboard deployment:** Hugging Face Spaces for SAE feature browser
- [ ] **Mini-paper workflow:** LaTeX template, `make paper`, citation management

## Light Touch (context)
- [ ] Data versioning (DVC / lakeFS) — for large activation datasets
- [ ] Containerization (Docker) — for reproducible experiment environments
- [ ] System design doc — for the capstone pipeline
- [ ] Security / privacy / governance — GDPR compliance, PII handling in datasets
