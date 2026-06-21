.PHONY: sync test lint reproduce clean paper

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
	python -m src.experiments.exp1_tokenizer_fertility
	@echo "Done. See figures/ and portfolio/RESULTS.md"

# --- Mini-paper ---
paper:
	cd portfolio/mini-paper && latexmk -pdf paper.tex

paper-clean:
	cd portfolio/mini-paper && latexmk -C

# --- Cleanup ---
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
