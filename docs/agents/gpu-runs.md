# GPU runs: Kaggle / Colab

The repository's remaining v1.1 work (issues #200 and #168) needs GPU
hours. This repo has no GPU; the free tiers cover it. Both runtimes share
**one contract**, so which one you use changes nothing downstream:

```
1. pick a notebook:   notebooks/kaggle_*.ipynb
2. validate locally:  make remote-dry-grokking  (checks everything, pushes nothing)
3. run remotely:      make remote-run-<job> GPU_USER=<you>
                      — or open the same notebook in Colab (link printed by dry-run)
4. download:          the driver fetches the kernel output; on Colab the notebook
                      zips the manifests and files.download()s them
5. pin:               python scripts/pin_remote_run.py --from <dir> --only <records>
6. cite:              add <!-- manifest: results/... --> tags, make verify-claims
7. commit by hand:    results/*.json on a branch, PR with CI green
```

`--only` names the records explicitly. A long multi-seed run also writes
one `results/<experiment>_seed<N>.json` per finished seed, and the content
task writes `results/content_verdict.json`; those are valid JSON but they
are **not** the record, so the pinner must be told which files are. If a
session died before the last seed, rebuild the multi-seed record first with
`python -m src.experiments.merge_manifests --inputs <dir> --output
results/<experiment>.json --expected-seeds 0,1,2 --allow-optional`.

## Zip the manifests without shell expansion

Never use `!zip -j ... $manifests` in a notebook cell: IPython expands a
Python list to its repr, so `zip` receives a single token like
`['results/a.json', 'results/b.json']`, finds no such file, and writes an
empty archive - the session's manifests are then lost on Colab. Use the
tested helper instead (the notebooks already do):

```python
from scripts.zip_manifests import write_manifest_zip
import glob

manifests = sorted(glob.glob("results/induction_content*.json"))
archive = write_manifest_zip(manifests, "induction_content_results.zip")
```

`write_manifest_zip` refuses an empty file list, a missing file, and two
files with the same basename, so a partial or silently-overwritten archive
is impossible. The content notebook appends `results/content_verdict.json`
to the same archive with `append_to_zip`, which refuses a name already
present. See `tests/test_zip_manifests.py`.

## Split a long sweep across sessions with `--cells`

The phase diagram sweep names every cell in its config, in pre-registered
order, so a long sweep can be split across GPU sessions without re-ordering
the grid. Name the cells explicitly rather than taking a prefix:

```bash
python scripts/phase_diagram_sweep.py --cells p113_wd1,p29_wd1 \
  --manifest-path results/phase_diagram.json
```

`--cells` refuses unknown ids and keeps the config's order; `--max-cells`
still takes a prefix for quick tests. A resumed session re-reads its
manifest and skips completed cells.

## One-time host setup

- `python -m pip install kaggle` into the project venv (the driver invokes it
  as `sys.executable -m kaggle`, so no PATH gymnastics are needed).
- Credentials: kaggle.com → Settings → Account → **Create New Token** →
  save the `KGAT_...` token to `~/.kaggle/access_token`
  (Windows: `C:\Users\<you>\.kaggle\access_token`), or export
  `KAGGLE_API_TOKEN`. The legacy username/key pair (`~/.kaggle/kaggle.json`)
  is still accepted. The driver's preflight checks for all of these before
  anything is pushed.
- On Kaggle itself: the notebook needs **Internet On** and a **GPU
  accelerator** (Settings → Accelerator → GPU T4/P100), and the account
  needs phone verification before GPU/Internet access is granted.

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
- **A cascade must name the model it analysed.** exp4 and exp5 record the
  loaded checkpoint in `source_provenance` (path, seed, epoch, commit,
  dirty flag), and the content verdict refuses a checkpoint from another
  seed, another commit, a dirty tree, or an epoch before exp1 finished.
  `--source-epochs` / `--source-git-sha` (exp4) and `--source-model-seed`
  (exp5) are the flags the notebook fills from exp1's manifest; they are
  not optional discipline, they are checks the experiments enforce.
- **A distributed circuit is reported, not promoted.** The content task's
  verdict is the seven frozen per-head criteria. When no head is confirmed
  but the behaviour copies, the report describes the group circuit as a
  pre-specified secondary finding and the verdict stays NEGATIVE. The
  headline is not rewritten to "a circuit".
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
| Phase sweep | `kaggle_phase_sweep.ipynb` | The protocol ablation from the Nanda-faithful baseline (issue #168) | ~1.5–2h |
| Content induction | `kaggle_induction_content.ipynb` | Does a **content-based** induction head form when the fixed-offset shortcut is removed (issue #200)? Full-budget run (it records `confirmed_epoch`), then the exp4/exp5 cascade on the same checkpoint, with the checkpoint's epoch/commit/seed checked. Writes per-seed recovery manifests and the verdict artifact. The 2026-10-25 addendum removed the separate emergence run; the 2026-11-01 addendum made the distributed circuit a secondary finding | ~3-4h |

Kaggle free: ~30 GPU-hours/week, ~9h sessions. Colab free: T4, variable
sessions. Every long step is resumable — re-run its cell after a
disconnect and it continues from its checkpoints (exp1/exp2 rolling
checkpoints; exp6 per-step files with the resume step computed by the
notebook).

## W&B

Optional (the 2026-09-08 close stands: no credentials ever worked). The
capstone notebook runs manifest-only unless a `WANDB_API_KEY` is pasted
into its setup cell. The manifests are the record; the dashboard is not.
