# From Gradient to Transformer — CLAUDE.md

## Project
Obsidian vault + research codebase for AI engineering: from gradient descent (Phases 1-3) to Transformer (Phase 4), LLM Engineering (Phase 5), Production AI (Phase 6), and micro-LLM capstone (Phase 7). All content in English. Primary research thesis: quantifying the "Italian tokenization tax" at micro scale.

## Rules
- Work on `dev` branch. Never push directly to `main`.
- All commits GPG-signed (configured globally).
- Conventional Commits: `type(scope): message`
  - types: feat | fix | docs | refactor | test | chore
  - scopes: meta | phase1..7 | ci | portfolio | templates | scripts | research | infra | paper
- **CI must pass before merging dev -> main. Never bypass failed checks.**
- Every note links at least 2 other notes. No orphan notes.
- Tags: `#phase/N`, `#type/lesson|exercise|proof|moc`, `#state/review|consolidated`, `#question`

## Layout
- `00_meta/` — home, roadmap, skill-tree, conventions, glossary, progress-log, obsidian-setup
- `01..06_*/notes/ exercises/ proofs/` — phase content (each has `_MOC.md` + `checklist.md`)
- `07_capstone/src/` — micro-LLM source code
- `src/` — shared research code (models, experiments, training, generation, reproducibility)
- `tests/` — unit tests (pytest)
- `figures/` — programmatically generated figures for the paper
- `portfolio/` — RESULTS.md, mini-paper (LaTeX), model card
- `checklists/` — reproducibility checklist, datasets
- `scripts/new_note.sh` — create notes from templates
- `templates/` — note.md, exercise.md, proof.md, project.md

## Available commands

```bash
bash scripts/new_note.sh <phase> <kind> "<Title>"
# phase: 01_foundations | 02_classical_ml | 03_deep_learning | 04_nlp_and_transformers | 05_llm_engineering | 06_production_ai | 07_capstone
# kind: notes | exercises | proofs | projects

pytest              # run all tests
ruff check src/     # lint
uv sync             # sync pinned environment
```

## Skills
- `study-session` — full study workflow (research, create note/exercise/proof, update skill-tree, commit)
- `phase-release` — complete a phase (verify checklist, update progress log, PR, wait for CI, tag, release)
