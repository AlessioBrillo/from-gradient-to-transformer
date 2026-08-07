---
tags: [type/exercise, phase/6]
skill: results-manifests
created: 2026-08-07
---

# Exercise: Falsify the Figure Gate

## Goal / skill it demonstrates

Same discipline as [[06_production_ai/exercises/ex-01-falsify-your-own-metric]], applied to
infrastructure instead of a research metric: before trusting a new checker, prove it
actually catches the failure it was built for. A gate that would have passed the exact
broken state it was designed to catch isn't a gate, it's decoration.

## Setup

Micro-Phase 12's state review found `portfolio/RESULTS.md` citing figures that don't exist
on disk, and citing figures that exist only in the local working tree (`figures/` is
gitignored) — invisible to anyone who clones the repo. `make verify-claims`
(`src.results.verify_claims`) checked manifest-tag existence and manifest internal
consistency, but never looked at a figure path at all. Two checks were added: figure
existence + git-tracking, and per-section manifest-tag coverage (so a section can't hide
behind a tag that lives in a *different* section of the same file).

## Solution

**1. Ran the un-patched checker against the real repository state, before touching
`RESULTS.md` or `.gitignore` — this is the RED evidence:**

```
$ python -m src.results verify
verify-claims: 17 problem(s) found:
  - portfolio\RESULTS.md: cites figure 'figures/exp1_training_bump.png' which exists on disk but is not tracked by git — invisible to anyone who clones the repo.
  ... (10 more "not tracked by git")
  - portfolio\RESULTS.md: cites figure 'figures/exp3_pentagon_geometry.png' which does not exist on disk.
  - portfolio\RESULTS.md: cites figure 'figures/exp4_head_ablation.png' which does not exist on disk.
  - portfolio\RESULTS.md: cites figure 'figures/exp5_feature_histogram_real.png' which does not exist on disk.
  - portfolio\RESULTS.md: cites figure 'figures/exp5_sparsity_tradeoff_real.png' which does not exist on disk.
  - portfolio\RESULTS.md: section 'Rung 2 — Grokking Modular Addition (Primary Flagship — NOT YET VERIFIED)' cites figures/outputs but has no <!-- manifest: ... --> tag of its own.
  - portfolio\RESULTS.md: section 'Rung 5 — Sparse Autoencoder Feature Dashboard' cites figures/outputs but has no <!-- manifest: ... --> tag of its own.
```

17 problems, on the first run, against the file as it actually stood — not a synthetic
example. This is the falsification test the doctrine asks for, done against production
data instead of a fixture, before the fixture-based unit test was even written.

**2. A second, real bug turned up before the figures could even be curated**: getting to
this point required two prerequisite fixes, both caught by trying to actually run the tool
rather than reasoning about it:
- `.gitignore`'s `figures/` rule was unanchored, so it also matched `portfolio/figures/` —
  the destination for the curated set MP12 Step 1 asks for. Verified directly:
  `git check-ignore -v portfolio/figures/probe.png` returned `.gitignore:9:figures/` before
  the fix. Anchored to `/figures/`.
- `claims_file.read_text()` had no explicit encoding, defaulting to the platform locale
  (`cp1252` on this Windows machine) instead of UTF-8. `RESULTS.md` contains non-ASCII
  characters and the read crashed with `UnicodeDecodeError` before any check could run.

**3. Wrote `test_falsifies_against_the_2026_08_07_state`
(`tests/test_results.py::TestVerifyClaims`) to reconstruct this exact shape as a permanent
regression fixture** — a missing figure citation plus an untagged section carrying figures,
inside a file that the *pre-existing* checks (manifest-tag-exists, manifest-internally-
consistent) would have called clean:

```python
def test_falsifies_against_the_2026_08_07_state(self, tmp_path, monkeypatch):
    ...
    problems = verify_claims(results_dir, claims_file)
    assert any("does not exist on disk" in p for p in problems)
    assert any("Rung 2: Grokking" in p and "no <!-- manifest:" in p for p in problems)
```

**4. After curating `portfolio/figures/`, fixing the two prerequisite bugs, and rewriting
the affected `RESULTS.md` sections honestly (striking citations to figures that genuinely
don't exist yet rather than fabricating them), re-ran the checker:**

```
$ python -m src.results verify
verify-claims: 14 problem(s) found:
  ... (12 "not tracked by git" — git add pending, not yet committed)
  - portfolio\RESULTS.md: section 'Rung 2 — Grokking Modular Addition ...' cites figures/outputs but has no <!-- manifest: ... --> tag of its own.
  - portfolio\RESULTS.md: section 'Rung 5 — Sparse Autoencoder Feature Dashboard' cites figures/outputs but has no <!-- manifest: ... --> tag of its own.
```

17 → 14. The "does not exist on disk" problems are gone (regenerated or struck honestly).
The two remaining section warnings are **correct, not a bug** — no `results/exp2_grokking.json`
or `results/exp5_sae_dashboard.json` has ever been produced, so those sections genuinely have
no manifest to tag. The gate staying red here is it working as designed, not a false positive.

## What I learned doing it

The falsification test almost didn't get written *first* — it was tempting to write the
checks, see them look reasonable, and move on. Running the un-patched checker against the
real file before writing a single line of the fix produced a more convincing artifact (17
real problems, in the actual repository, dated) than any fixture I could have invented. The
fixture-based test in step 3 exists to keep that property permanent — so the next accidental
regression gets caught by `pytest`, not by a state review a phase later.

The second lesson was unplanned: the gate itself was blocked by two bugs I didn't know
existed (`.gitignore` anchoring, read-encoding) until I tried to run it for real, on this
machine, against real data. Neither would have surfaced from reading the code.

## Linked skill
- [[00_meta/02_skill-tree]] → item: Reproducibility harness (Phase 6)
- [[06_production_ai/notes/results-manifests-and-provenance]]
- [[06_production_ai/notes/figure-provenance-and-evidence-gates]]
- [[06_production_ai/exercises/ex-01-falsify-your-own-metric]]
