# From Gradient to Transformer to Circuit — CLAUDE.md

## Project
Obsidian vault + mechanistic interpretability research codebase: from gradient descent (Phases 1-3) to Transformer (Phase 4), LLM instrumentation (Phase 5), reproducible research infra (Phase 6), and a capstone that trains a decoder-only transformer and reverse-engineers its internals (Phase 7). All content in English. Primary research direction: mechanistic interpretability at micro scale — grokking modular addition, induction heads, superposition, circuit discovery, and sparse autoencoder feature extraction.

## Rules
- Work on `dev` branch. Never push directly to `main`.
- All commits GPG-signed (configured globally).
- Conventional Commits: `type(scope): message`
  - types: feat | fix | docs | refactor | test | chore
  - scopes: meta | phase1..7 | ci | portfolio | templates | scripts | research | infra | paper | grokking | induction-heads | superposition | circuit-patching | sae
- **CI must pass before merging dev -> main. Never bypass failed checks.**
- Every note links at least 2 other notes. No orphan notes.
- Tags: `#phase/N`, `#type/lesson|exercise|proof|moc`, `#state/review|consolidated`, `#question`, `#research/experiment`

## Layout
- `00_meta/` — home, roadmap, skill-tree, conventions, glossary, progress-log, obsidian-setup
- `01..06_*/notes/ exercises/ proofs/` — phase content (each has `_MOC.md` + `checklist.md`)
- `07_capstone/` — capstone: train + reverse-engineer a decoder-only transformer
- `src/` — shared research code (experiments, reproducibility, circuits, SAE)
- `tests/` — unit tests (pytest) including per-experiment smoke tests
- `figures/` — programmatically generated figures for the paper
- `portfolio/` — RESULTS.md, mini-paper (LaTeX), model card
- `checklists/` — reproducibility checklist, datasets
- `scripts/new_note.sh` — create notes from templates
- `templates/` — note.md, exercise.md, proof.md, project.md, paper-note.md

## Available commands

```bash
bash scripts/new_note.sh <phase> <kind> "<Title>"
# phase: 01_foundations | 02_classical_ml | 03_deep_learning | 04_nlp_and_transformers | 05_llm_engineering | 06_production_ai | 07_capstone
# kind: notes | exercises | proofs | projects

pytest              # run all tests
ruff check src/     # lint
uv sync             # sync pinned environment

# Experiment-specific reproducibility
make reproduce              # regenerate all figures and tables
make reproduce-grokking     # Rung 2: grokking modular addition (FLAGSHIP)
make reproduce-induction    # Rung 1: induction heads
make reproduce-sae          # Rung 5: SAE feature dashboard
```

## Skills
- `study-session` — full study workflow (research, create note/exercise/proof, update skill-tree, commit)
- `phase-release` — complete a phase (verify checklist, update progress log, PR, wait for CI, tag, release)
