.PHONY: sync test test-cov lint lint-fix typecheck typecheck-strict typecheck-new \
	ci-check reproduce reproduce-quick reproduce-grokking reproduce-induction \
	reproduce-superposition reproduce-patching reproduce-sae \
	reproduce-multiseed verify-claims clean paper \
	reproduce-grokking-probe reproduce-induction-standard reproduce-induction-1layer \
	reproduce-exp3-geometry commitlint-head

# --- Shell ---
# The recipes are POSIX verbatim (the CI mirror); Windows GNU Make defaults
# to cmd.exe, which cannot run `code=$$?; if [ ... ]` recipes and misruns the
# `typecheck` target ("unrecognized arguments" passed to mypy). Git ships
# sh.exe at C:\Program Files\Git\bin; resolved at runtime so the documented
# prerequisite ("Git's bin/ on PATH", see the MP-21 incident in the progress
# log) is all that is needed. Linux/macOS keep the platform default.
ifneq ($(OS),Windows_NT)
SHELL := /bin/sh
else
SHELL := $(subst \,/,$(firstword $(shell where sh.exe 2>/dev/null)))
endif

# --- Environment ---
# All targets run through `uv run` so they work from any fresh shell after
# `uv sync`, regardless of whether the project venv is activated or not.
# Without it, `make reproduce` / `make verify-claims` silently invoked the
# system interpreter (missing the pinned runtime deps) and `make ci-check`
# invoked system pytest/ruff/mypy. `uv run` is a no-op passthrough inside an
# already-activated venv, so this is safe both ways.
sync:
	uv sync

# --- Testing ---
test:
	uv run pytest -v --tb=short

test-cov:
	uv run pytest -v --tb=short --cov=src --cov-report=term-missing

# --- Linting ---
lint:
	uv run ruff check src/ tests/

lint-fix:
	uv run ruff check --fix src/ tests/

# Non-blocking: strict mode currently reports 154+ errors (2026-08-01 count,
# after fixing a python_version mismatch that previously made mypy crash on
# numpy's stubs before checking a single line of src/ — see pyproject.toml
# [tool.mypy]). Mostly missing-generic-args pedantry (dict -> dict[str,
# Any], DataLoader -> DataLoader[Any]), not caught bugs, but 154 is real
# work, not something to silently claim fixed. Tracked as follow-up. Unlike
# `|| true`, this still fails on a genuine mypy crash (exit 2) — see
# .github/workflows/python-ci.yml for why that distinction matters.
typecheck:
	@uv run mypy src/ --ignore-missing-imports; code=$$?; \
	if [ $$code -eq 2 ]; then echo "mypy crashed (exit 2) — failing."; exit 1; fi; \
	exit 0

typecheck-strict:
	uv run mypy src/ --ignore-missing-imports

# Blocking: a small, deliberately-growing allowlist of modules held to
# `mypy --strict` with zero tolerance from the day they were written. New
# modules land here; existing modules move here as their error count is
# paid down — a ratchet, not a someday-fix-it-all pass. (src/reproducibility.py
# and src/models/ were considered for this list and turned out NOT to be
# clean — real pre-existing errors, not yet fixed — so they stay in the
# non-blocking full-tree check instead of being wrongly promised here.)
# --follow-imports=silent: without it, mypy also fails this target on
# errors in whatever these two files transitively import (caught in CI —
# see .github/workflows/python-ci.yml's blocking step comment).
typecheck-new:
	uv run mypy src/results.py src/experiments/runner.py --ignore-missing-imports --follow-imports=silent

# --- CI mirror (local replica of .github/workflows/python-ci.yml) ---
# commitlint-head is part of the mirror since 2026-08-08: the PR-only
# Conventional Commits workflow never runs on a local push, and that gap let
# the micro-phase-20 step-0 commit ship with a >200-char body line (caught by
# GitHub's PR check, exactly like micro-18/19). The mirror lints the HEAD
# commit against the same config:
#   npx --yes commitlint --from HEAD~1 --to HEAD --config commitlint.config.mjs
ci-check: lint typecheck-new typecheck test-cov commitlint-head

commitlint-head:
	@echo "=== commitlint (HEAD commit vs parent, mirror of the PR-only check) ==="
	@npx --yes commitlint --from HEAD~1 --to HEAD --config commitlint.config.mjs
	@echo "commitlint: HEAD commit message conforms."

# --- Reproducibility ---
# Full-scale run of every surviving rung (Rung 6 was descoped — see
# 07_capstone/research-plan.md). This is hours, not minutes; use
# reproduce-quick for a fast smoke pass.
reproduce:
	@echo "=== Regenerating all experiment figures ==="
	uv run python -m src.experiments.exp1_induction_heads
	uv run python -m src.experiments.exp2_grokking
	uv run python -m src.experiments.exp3_superposition
	uv run python -m src.experiments.exp4_circuit_patching
	uv run python -m src.experiments.exp5_sae_dashboard
	@echo "Done. See figures/ and portfolio/RESULTS.md"

reproduce-quick:
	@echo "=== Smoke-testing all rungs in --quick mode ==="
	uv run python -m src.experiments.exp1_induction_heads --quick
	uv run python -m src.experiments.exp2_grokking --quick
	uv run python -m src.experiments.exp3_superposition --quick
	uv run python -m src.experiments.exp4_circuit_patching --quick
	uv run python -m src.experiments.exp5_sae_dashboard --quick
	@echo "Done."

reproduce-grokking:
	@echo "=== Rung 2: Grokking modular addition (FLAGSHIP) ==="
	uv run python -m src.experiments.exp2_grokking

# Micro-Phase 10 (the Evidence Run) pinned canonical configs. The names
# below are the single source of truth for what "standard scale" means —
# Rungs 1/4/5 must use the exp1 --standard config so the cascade measures
# one shared model. The grokking probe is the CPU de-risk step that runs
# BEFORE any GPU hours are spent on P=113.
reproduce-grokking-probe:
	@echo "=== Rung 2: P=59 CPU de-risk probe (canonical hyperparams) ==="
	uv run python -m src.experiments.exp2_grokking --probe

reproduce-induction-standard:
	@echo "=== Rung 1: standard-scale fresh-batches (the domino) ==="
	uv run python -m src.experiments.exp1_induction_heads --standard

reproduce-induction-1layer:
	@echo "=== Rung 1: 1-layer headless lower bound (matched config) ==="
	uv run python -m src.experiments.exp1_induction_heads --standard --n-layers 1

reproduce-exp3-geometry:
	@echo "=== Rung 3: pentagon geometry check (5 features -> 2 dims) ==="
	uv run python -m src.experiments.exp3_superposition --geometry-check

reproduce-induction:
	@echo "=== Rung 1: Induction heads ==="
	uv run python -m src.experiments.exp1_induction_heads

reproduce-superposition:
	@echo "=== Rung 3: Superposition geometry ==="
	uv run python -m src.experiments.exp3_superposition

reproduce-patching:
	@echo "=== Rung 4: Circuit verification via activation/path patching ==="
	uv run python -m src.experiments.exp4_circuit_patching

reproduce-sae:
	@echo "=== Rung 5: SAE feature dashboard ==="
	uv run python -m src.experiments.exp5_sae_dashboard

# --- Multi-seed provenance (Micro-Phase 8, the Evidence Pass) ---
# `--seeds` support lands per-experiment as each rung is re-verified. exp2
# (grokking) has it but its standard-scale manifest comes from the Colab run
# via scripts/pin_colab_run.py — running P=113 x3 seeds here would burn CPU
# hours. exp5 (SAE) gained --seeds in Micro-Phase 10 but is left out of this
# target to keep the clean-clone gate fast; its manifest is produced by the
# explicit `--seeds` invocation when the real-activation re-test runs.
# IMPORTANT (fixed 2026-08-05): these must reproduce the exact configs behind
# the committed manifests / portfolio/RESULTS.md, NOT blanket `--quick`.
# exp1's Tiny multi-seed table is the 150-epoch fresh-batches config and exp3's
# is single_sparsity=0.01 at 600 epochs/8000 samples; `--quick` silently
# swapped both for the reduced config (500/2000 epochs, no single_sparsity),
# producing numbers that did not match the claims. exp4's quick config is the
# one its committed manifest actually used, so it stays `--quick`.
reproduce-multiseed:
	@echo "=== Multi-seed runs -> results/*.json ==="
	uv run python -m src.experiments.exp1_induction_heads --fresh-batches --vocab-size 256 --seq-len 16 --d-model 24 --n-layers 2 --n-heads 4 --epochs 150 --lr 0.001 --weight-decay 0.1 --batch-size 32 --num-train 256 --seeds 0,1,2
	uv run python -m src.experiments.exp3_superposition --epochs 600 --num-samples 8000 --batch-size 512 --single-sparsity 0.01 --seeds 0,1,2
	uv run python -m src.experiments.exp4_circuit_patching --quick --seeds 0,1,2
	@echo "Done. See results/*.json"

# Fails if a headline number in portfolio/RESULTS.md has no manifest
# backing it (no <!-- manifest: results/<exp>.json --> tag, or a tag
# pointing at a manifest that doesn't exist / doesn't match its own seed
# count). See src/results.py.
verify-claims:
	uv run python -m src.results verify

# --- Paper (Micro-Phase 16: the drift fix) ---
# Compiles portfolio/paper/main.tex. Graceful when no LaTeX toolchain is
# installed (common on CI/dev machines): the source is the artifact, the PDF
# is a build product, so a missing toolchain is a message, not a failure.
paper:
	@echo "=== Compiling portfolio/paper/main.tex ==="
	@if command -v latexmk >/dev/null 2>&1; then \
		cd portfolio/paper && latexmk -pdf main.tex; \
	elif command -v pdflatex >/dev/null 2>&1; then \
		cd portfolio/paper && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex; \
	else \
		echo "No LaTeX toolchain found (latexmk/pdflatex). The paper source is portfolio/paper/main.tex; install TeX Live/MiKTeX or compile on Overleaf."; \
	fi

# --- Cleanup ---
clean:
	@echo "=== Cleaning temporary artifacts ==="
	-python -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
	-python -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]"
	-rm -rf .pytest_cache .ruff_cache .mypy_cache
