## Summary

<!-- What changes and why. Link the issue if there is one. -->

## Evidence

- [ ] `uv run pytest` and `uv run ruff check src/ tests/` pass
- [ ] `uv run python -m src.results verify` passes: every number in `portfolio/RESULTS.md`
      or the paper points at a committed `results/*.json` manifest
- [ ] No test writes into `results/` (use `tmp_path` or `--manifest-path`)
- [ ] Commits follow Conventional Commits and are signed

## Claims touched

<!-- Which headline numbers or verdicts change? If a result is negative or uncertain, say so here. -->
