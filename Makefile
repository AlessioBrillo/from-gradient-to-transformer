.PHONY: sync test test-cov lint lint-fix typecheck typecheck-strict ci-check \
	reproduce reproduce-quick reproduce-grokking reproduce-induction \
	reproduce-superposition reproduce-patching reproduce-sae clean

# --- Environment ---
sync:
	uv sync

# --- Testing ---
test:
	pytest -v --tb=short

test-cov:
	pytest -v --tb=short --cov=src --cov-report=term-missing

# --- Linting ---
lint:
	ruff check src/ tests/

lint-fix:
	ruff check --fix src/ tests/

# Non-blocking: strict mode currently reports 154 errors (2026-08-01 count,
# after fixing a python_version mismatch that previously made mypy crash on
# numpy's stubs before checking a single line of src/ — see pyproject.toml
# [tool.mypy]). Mostly missing-generic-args pedantry (dict -> dict[str,
# Any], DataLoader -> DataLoader[Any]), not caught bugs, but 154 is real
# work, not something to silently claim fixed. Tracked as follow-up.
typecheck:
	mypy src/ --ignore-missing-imports || true

typecheck-strict:
	mypy src/ --ignore-missing-imports

# --- CI mirror (local replica of .github/workflows/python-ci.yml) ---
ci-check: lint typecheck test-cov

# --- Reproducibility ---
# Full-scale run of every surviving rung (Rung 6 was descoped — see
# 07_capstone/research-plan.md). This is hours, not minutes; use
# reproduce-quick for a fast smoke pass.
reproduce:
	@echo "=== Regenerating all experiment figures ==="
	python -m src.experiments.exp1_induction_heads
	python -m src.experiments.exp2_grokking
	python -m src.experiments.exp3_superposition
	python -m src.experiments.exp4_circuit_patching
	python -m src.experiments.exp5_sae_dashboard
	@echo "Done. See figures/ and portfolio/RESULTS.md"

reproduce-quick:
	@echo "=== Smoke-testing all rungs in --quick mode ==="
	python -m src.experiments.exp1_induction_heads --quick
	python -m src.experiments.exp2_grokking --quick
	python -m src.experiments.exp3_superposition --quick
	python -m src.experiments.exp4_circuit_patching --quick
	python -m src.experiments.exp5_sae_dashboard --quick
	@echo "Done."

reproduce-grokking:
	@echo "=== Rung 2: Grokking modular addition (FLAGSHIP) ==="
	python -m src.experiments.exp2_grokking

reproduce-induction:
	@echo "=== Rung 1: Induction heads ==="
	python -m src.experiments.exp1_induction_heads

reproduce-superposition:
	@echo "=== Rung 3: Superposition geometry ==="
	python -m src.experiments.exp3_superposition

reproduce-patching:
	@echo "=== Rung 4: Circuit verification via activation/path patching ==="
	python -m src.experiments.exp4_circuit_patching

reproduce-sae:
	@echo "=== Rung 5: SAE feature dashboard ==="
	python -m src.experiments.exp5_sae_dashboard

# --- Cleanup ---
clean:
	@echo "=== Cleaning temporary artifacts ==="
	-python -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
	-python -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]"
	-rm -rf .pytest_cache .ruff_cache .mypy_cache
