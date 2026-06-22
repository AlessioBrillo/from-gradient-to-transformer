.PHONY: sync test lint reproduce clean paper reproduce-grokking reproduce-induction reproduce-sae

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

typecheck:
	mypy src/ --ignore-missing-imports || true

# --- Reproducibility ---
reproduce:
	@echo "=== Regenerating all experiment figures and tables ==="
	python -m src.experiments.exp2_grokking
	python -m src.experiments.exp1_induction_heads
	@echo "Done. See figures/ and portfolio/RESULTS.md"

reproduce-grokking:
	@echo "=== Rung 2: Grokking modular addition (FLAGSHIP) ==="
	python -m src.experiments.exp2_grokking

reproduce-induction:
	@echo "=== Rung 1: Induction heads ==="
	python -m src.experiments.exp1_induction_heads

reproduce-sae:
	@echo "=== Rung 5: SAE feature dashboard ==="
	python -m src.experiments.exp5_sae_dashboard

# --- Mini-paper ---
paper:
	cd portfolio/mini-paper && latexmk -pdf paper.tex

paper-clean:
	cd portfolio/mini-paper && latexmk -C

# --- Cleanup ---
clean:
	@echo "=== Cleaning temporary artifacts ==="
	-python -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]" 2>nul || true
	-python -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]" 2>nul || true
	-rm -rf .pytest_cache .ruff_cache .mypy_cache 2>nul || true
