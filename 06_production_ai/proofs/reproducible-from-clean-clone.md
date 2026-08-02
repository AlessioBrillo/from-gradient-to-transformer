---
tags: [type/proof, phase/6]
created: 2026-08-02
---

# Proof to myself: Reproducible From a Clean Clone

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate

That the reproducibility infrastructure built in Micro-Phase 8 (the Evidence Pass) —
`--seeds`, `src/results.py`'s manifests, `make verify-claims` — actually functions as a
gate, not just as code that exists. The Phase 6 checklist's own rule is the same one the
skill tree states: a claim without verification against the actual running code is not
trustworthy. I have deliberately **not** faked this proof against work that is still
uncommitted — a "clean clone" of `dev` right now would clone the code as it stood *before*
this micro-phase and would prove nothing about what I actually built.

## What I produced from memory

**What I verified in this working tree, today, against the code as written:**

- `pytest -v --cov=src` — 145 tests passed (up from 110 at the start of this micro-phase),
  including every falsification test for the Rung 3 rewrite, the multi-seed harness, and
  the induction-task-ambiguity guard.
- `ruff check src/ tests/` — clean.
- `python -m src.results verify` (no manifests committed yet) correctly reports 2 problems
  — proof the checker isn't a no-op that passes trivially before there is anything to check.
- `python -m src.experiments.exp3_superposition --n-features 20 --n-dimensions 5 --seeds 0,1,2 --single-sparsity 0.01 --epochs 600 --num-samples 8000` produced a real
  `results/exp3_superposition.json` with genuine seed-to-seed spread
  (`n_represented: 19.67 ± 0.47`).
- `python -m src.experiments.exp3_superposition` (full sweep, no `--quick`) produced a
  confirmed phase transition (10/20 → 20/20 features represented as sparsity dropped from
  0.5 to 0.01) and both figures regenerated without error.
- `python -m src.experiments.exp{1,4}_induction_heads / _circuit_patching --seeds 0,1
  <tiny explicit config>` each produced a manifest end-to-end with no crashes.

**What this proof does *not* yet demonstrate**, and why it is marked incomplete rather than
padded out with a fabricated clean-clone log:

1. **No clean-clone run has happened.** This session's changes are uncommitted on `dev`.
   `uv sync && make reproduce-quick && make verify-claims` from a fresh `git clone` needs to
   run *after* this work is committed and pushed — running it now would silently test old
   code and report a false pass.
2. **`make verify-claims` will fail against `portfolio/RESULTS.md`** even after commit,
   until the reconciliation pass (tracked separately) adds `<!-- manifest: ... -->` tags
   next to the numbers each manifest backs. That is intentional — the gate should fail
   until the tags exist, not be relaxed to pass early.
3. **Not every rung has a manifest yet.** `exp2_grokking`'s standard-scale, multi-seed
   manifest depends on the Colab GPU run (`notebooks/colab_grokking_full_run.ipynb`), which
   is outside this environment's compute budget. `exp5_sae_dashboard` doesn't have `--seeds`
   wired yet.

## What "gate green" will require, concretely

```bash
cd /tmp && git clone <repo> clean-check && cd clean-check
uv sync
make reproduce-quick     # all rungs, --quick, must exit 0
make reproduce-multiseed # rungs 1/3/4, --quick --seeds 0,1,2, must exit 0
make verify-claims       # must exit 0 -- requires RESULTS.md manifest tags
```

If any step needs a manual intervention not captured in the commands above, the gate is not
green and the intervention gets written down here, not silently worked around.

## Links
- [[06_production_ai/notes/results-manifests-and-provenance]]
- [[06_production_ai/notes/multi-seed-experiment-design]]
- [[06_production_ai/checklist]]
- [[portfolio/RESULTS]]

## Outcome
- [ ] Passed → check the skill in [[00_meta/02_skill-tree]]
- [x] Retry needed (what was missing): the actual clean-clone run, performed after commit +
  push, with `RESULTS.md` manifest tags in place. This proof documents the state of
  everything that can be verified pre-commit; the clone step itself is the remaining gap.
