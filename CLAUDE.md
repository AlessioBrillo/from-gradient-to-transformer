# From Gradient to Transformer to Circuit — CLAUDE.md

## Project
Obsidian vault + mechanistic interpretability research codebase: from gradient descent to Transformer, LLM instrumentation, reproducible infra, and a capstone training a decoder-only transformer with reverse-engineered internals. Focus: micro-scale mechanistic interpretability — grokking modular addition, induction heads, superposition, circuit discovery, and sparse autoencoder feature extraction.

## Rules
- Work on `dev` branch. Never push directly to `main`.
- All commits GPG-signed (configured globally).
- Conventional Commits: `type(scope): message`
  - types: feat | fix | docs | refactor | test | chore
  - scopes: meta | phase1..7 | ci | portfolio | templates | scripts | research | infra | paper | grokking | induction-heads | superposition | circuit-patching | sae
- **CI must pass before merging dev -> main. Never bypass failed checks.**
- Every note links at least 2 other notes. No orphan notes. Enforced by `make vault-check`.
- Tags: `#phase/N`, `#type/lesson|exercise|proof|moc`, `#state/review|consolidated`, `#question`, `#research/experiment`
- Never cite a public number that has no committed manifest behind it. `make verify-claims` enforces this in CI.

## Layout
- `00_meta/` — home, roadmap, skill-tree, conventions, glossary, progress-log, obsidian-setup
- `01..06_*/notes/ exercises/ proofs/` — phase content (each has `_MOC.md` + `checklist.md`)
- `07_capstone/` — capstone: train + reverse-engineer a decoder-only transformer
- `src/` — shared research code (experiments, reproducibility, manifests, models)
- `tests/` — unit tests (pytest) including per-experiment smoke tests
- `figures/` — programmatically generated figures (scratch; gitignored)
- `portfolio/figures/` — the curated, tracked figure set (a build product: `make figures`)
- `portfolio/` — RESULTS.md (Honesty Ledger), mini-paper (LaTeX), model card
- `checklists/` — reproducibility checklist, datasets
- `CONTEXT.md` — domain map, vocabulary, rung→module map. **Read it first.**
- `scripts/new_note.sh` — create notes from templates
- `templates/` — note.md, exercise.md, proof.md, project.md, paper-note.md

## Available commands

```bash
bash scripts/new_note.sh <phase> <kind> "<Title>"
# phase: 01_foundations | 02_classical_ml | 03_deep_learning | 04_nlp_and_transformers | 05_llm_engineering | 06_production_ai | 07_capstone
# kind: notes | exercises | proofs | projects

pytest              # run all tests
make lint           # lint src/ tests/ scripts/ (all three)
uv sync             # sync pinned environment

# Experiment-specific reproducibility
make reproduce              # regenerate all figures and tables
make reproduce-grokking     # Rung 2: grokking modular addition (FLAGSHIP)
make reproduce-induction    # Rung 1: induction heads
make reproduce-sae          # Rung 5: SAE feature dashboard
make figures                # rebuild portfolio/figures/ from the manifests
make verify-claims          # every public number traces to a tracked manifest
make vault-check            # note link/orphan + tag-schema gate
make ci-check               # local mirror of .github/workflows/python-ci.yml

# Remote GPU runs (Kaggle/Colab) — see docs/agents/gpu-runs.md
make remote-dry-grokking    # validate the GPU notebook, push nothing
make remote-run-grokking GPU_USER=<you>   # Rung 2 audit (issue #167)
make remote-run-induction GPU_USER=<you>  # Rung 1/4/5 cascade (issue #169)
make remote-run-capstone GPU_USER=<you>   # capstone 3x20k (issue #170)
make remote-run-sweep GPU_USER=<you>      # phase-diagram protocol ablation (issue #168)
make remote-pin PIN_FROM=<dir>            # validate + install downloaded manifests
```

Everything runs from the repo root: `FIGURES_DIR`, `RESULTS_DIR` and
`CHECKPOINTS_DIR` are CWD-relative by design. Run experiments as
`uv run python -m src.experiments.<module>`.

This is **not** a distributable package — `pyproject.toml` has no
`[build-system]` and the code is used in place via `uv run`.

## Skills
- `study-session` — full study workflow (research, create note/exercise/proof, update skill-tree, commit)
- `phase-release` — complete a phase (verify checklist, update progress log, PR, wait for CI, tag, release)

## Agent skills

### Issue tracker

Issues live in GitHub Issues (AlessioBrillo/from-gradient-to-transformer), via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### GPU runs

The three GPU-gated issues run on free Kaggle/Colab through one contract (driver, pinner, notebook lint). See `docs/agents/gpu-runs.md`.

### Domain docs

Single-context — `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## CI gate

GitHub Actions is not the gate. The single source of truth is `.woodpecker/ci.yml`.

- **Local, no server:** `ci-local` from the repo root (Docker running). Exit 0 = green.
  Never run `woodpecker-cli exec` directly on the checkout: it bind-mounts the repo and
  install steps would overwrite host dependencies.
- **Server:** push the branch; the check is `ci/woodpecker/push/ci` (`gh pr checks <n> --watch`).
- **Not in the gate:** the two commitlint targets (commit-msg hook and conventional-commits workflow cover them), paper LaTeX build, markdown-lint.
- **Status:** first green run recorded 2026-10-16 (lint, vault-check, test-cov 393 passed,
  verify-claims=0). `typecheck-new`/mypy require the CI Docker image and are blocked on this
  host by an Application Control policy — they run in CI. If a step fails for an environment
  reason (image, network, missing tool), fix `.woodpecker/ci.yml`, not the code.
- Done / merge-ready means this gate is green on the final tree. See `~/.agents/CI.md`.
