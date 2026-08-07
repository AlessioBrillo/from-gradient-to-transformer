---
tags: [type/lesson, phase/6, state/review]
---

# Figure Provenance and Evidence Gates

## What it is

A two-tier contract for figures: `figures/` is regenerable scratch (gitignored, rebuilt by
`make reproduce`); `portfolio/figures/` is a small, committed, curated set. A figure backing
a claim in `portfolio/RESULTS.md` lives in the latter, or the claim doesn't cite one. The
contract is enforced mechanically — not just documented — by two checks added to
`verify_claims()` (`src/results.py`): every cited figure must exist on disk *and* be tracked
by git, and every results section that shows figures must carry its own
`<!-- manifest: ... -->` tag.

## Why it exists / what problem it solves

This is the third time this exact failure mode has hit this repository. 2026-07-26: `figures/`
didn't exist at all despite being cited throughout `RESULTS.md`. 2026-08-01: three Rung 4
numbers were retracted after an audit found the causal patch behind them never landed. This
time (Micro-Phase 12, 2026-08-07): `RESULTS.md` cited four figures that had never been
generated (`exp3_pentagon_geometry.png`, `exp4_head_ablation.png`,
`exp5_sparsity_tradeoff_real.png`, `exp5_feature_histogram_real.png`), and the twelve figures
that *did* exist were only ever in `figures/` — which `.gitignore` excludes from every clone.
[[06_production_ai/notes/results-manifests-and-provenance]] closed the "no manifest behind
this number" gap in 2026-08-02; it never touched figures, which is exactly the gap that
reopened.

The original plan for Step 1 of Micro-Phase 12 was "no new automation target yet; a
documented copy step is proportionate." I overrode that on the way through: a documented
copy step is a fourth instance of the same control that already failed three times, and the
fix is about 25 lines inside a function that already runs in `make verify-claims` and already
has a test file (`tests/test_results.py`). Cheaper than the prose defending the manual
alternative, and it closes the loop the same way `results-manifests-and-provenance.md`
already closed it for numbers.

## How it works

Two new checks inside `verify_claims()`, reusing its existing `problems: list[str]`
accumulator — no new function signature, no new CLI surface:

```python
FIGURE_CITATION_RE = re.compile(r"`([^`]*figures/[^`]*\.png)`")

for rel in sorted(set(FIGURE_CITATION_RE.findall(text))):
    fig_path = Path(rel)
    if not fig_path.exists():
        problems.append(f"... cites figure '{rel}' which does not exist on disk.")
    elif not _git_tracked(fig_path):
        problems.append(f"... cites figure '{rel}' which exists on disk but is not "
                         "tracked by git -- invisible to anyone who clones the repo.")
```

`_git_tracked()` shells out to `git ls-files --error-unmatch <path>` — the same pattern
`git_provenance()` already uses for the commit SHA, just checking a different fact. A second
check splits `RESULTS.md` on `## ` headings and flags any section whose body contains a
`**Figures**:` or `**Outputs**:` line but no manifest tag of its own — this is what let the
whole-file "any tags at all?" check stay quiet while Rung 2 and Rung 5 cited results with
nothing behind them, because *some other* section elsewhere in the file happened to have a
tag.

**Two bugs surfaced just from trying to run this for real**, before a single figure was
curated:
1. `.gitignore`'s `figures/` rule was unanchored — it also matched `portfolio/figures/`, the
   destination this whole step exists to populate. `git add` would have silently skipped
   every curated figure. Anchored to `/figures/`.
2. `claims_file.read_text()` had no explicit encoding, defaulting to the Windows locale
   codepage instead of UTF-8, and crashed on `RESULTS.md`'s non-ASCII characters. Neither bug
   would show up from reading the code — only from running it.

The first real run against the actual repository found **17 problems** — more than expected
even having gone looking for this. See
[[06_production_ai/exercises/ex-05-falsify-the-figure-gate]] for the full transcript,
including the falsification test that reconstructs this exact state as a permanent pytest
fixture.

## Links
- [[06_production_ai/notes/results-manifests-and-provenance]]
- [[06_production_ai/exercises/ex-05-falsify-the-figure-gate]]
- [[00_meta/11_micro-phase-12-resilient-flagship-run]]
- Code: `src/results.py` (`verify_claims`, `_git_tracked`, `FIGURE_CITATION_RE`)
- Pineau et al., *Improving Reproducibility in Machine Learning Research*, JMLR 2021

## Open questions
- #question Two `RESULTS.md` sections (Rung 2, Rung 5) genuinely have no manifest behind
  them — no `results/exp2_grokking.json` or `results/exp5_sae_dashboard.json` has ever been
  produced. The gate correctly still reports these as problems. Does `make verify-claims`
  become a CI-blocking gate once every rung has a real manifest, or does that just create
  pressure to keep a stale manifest around past when a rerun is actually warranted — the
  same open question `results-manifests-and-provenance.md` already raised, now sharper.
