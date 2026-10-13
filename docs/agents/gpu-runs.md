# GPU runs: Kaggle / Colab

The repository's remaining v1.0 work (issues #167, #169, #170) needs GPU
hours. This repo has no GPU; the free tiers cover it. Both runtimes share
**one contract**, so which one you use changes nothing downstream:

```
1. pick a notebook:   notebooks/kaggle_*.ipynb
2. push dev:          git push origin dev     (the remote run pins a ref)
3. validate locally:  make remote-dry-grokking  (checks everything, pushes nothing)
4. run remotely:      make remote-run-<job> GPU_BRANCH=dev GPU_USER=<you>
                      — or open the same notebook in Colab (link printed by dry-run)
5. download:          the driver fetches the kernel output; on Colab the notebook
                      zips the manifests and files.download()s them
6. pin:               python scripts/pin_remote_run.py --from <dir>
7. cite:              add <!-- manifest: results/... --> tags, make verify-claims
8. commit by hand:    results/*.json on a branch, PR with CI green
```

## Why the contract is this strict

- **A run is only reproducible if its manifest names a real commit.** The
  driver refuses any ref that is not on `origin`; the pinner refuses any
  manifest whose `git_sha` does not exist locally or whose `git_dirty` is
  true (a remote run clones a clean pinned ref — a dirty flag means the
  provenance is wrong).
- **A manifest is only evidence if it loads as one.** The pinner checks the
  structural contract `verify-claims` enforces (seeds == per-seed records,
  aggregate n == seeds, non-empty aggregate) and installs **nothing** if any
  file fails. Fail-closed, by refusal.
- **Nothing is ever auto-committed.** The pinner prints the exact citation
  snippet to add; the commit stays human, after `verify-claims` is green.
- **The notebooks are linted in CI** (`tests/test_remote_notebooks.py`)
  even though they cannot be *executed* there: modules must import, flags
  must exist in the parsers they claim, manifests must route under
  `results/`, the download cell must serve both runtimes, and a pinned
  `BRANCH` must be present. The teaching artifact v22 rotted because
  nothing checked it; these notebooks are checked.

## The jobs

| Job | Notebook | What it answers | Budget |
|-----|----------|-----------------|--------|
| Grokking audit | `kaggle_grokking_p113.ipynb` | Does the Nanda-faithful protocol grok (job A)? Does the energy metric re-judge NO-GROK (job B)? | ~1–1.5h |
| Induction cascade | `kaggle_induction_standard.ipynb` | Does a head emerge at large scale, then standard (issue #169)? With a confirmed head: exp4 ablation + path patching, exp5 real-activation SAE | ~2–3h |
| Capstone | `kaggle_capstone_20k.ipynb` | The planned 3×20k-step joint run with full instrumentation (issue #170) | ~30–40 min + resume |

Kaggle free: ~30 GPU-hours/week, ~9h sessions. Colab free: T4, variable
sessions. Every long step is resumable — re-run its cell after a
disconnect and it continues from its checkpoints (exp1/exp2 rolling
checkpoints; exp6 per-step files with the resume step computed by the
notebook).

## W&B

Optional (the 2026-09-08 close stands: no credentials ever worked). The
capstone notebook runs manifest-only unless a `WANDB_API_KEY` is pasted
into its setup cell. The manifests are the record; the dashboard is not.
