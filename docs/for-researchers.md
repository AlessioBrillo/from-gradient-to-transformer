# For researchers

What is reproduced, what is not, how to re-run it, and how to check or dispute a
number.

## What is and is not established

| Rung | Status | Read |
|---|---|---|
| 2 Grokking on modular addition | Reproduced on the Nanda et al. protocol and on this repository's own protocol, three seeds each, GPU | [Rung 2](../portfolio/projects/rung-2-grokking/index.md) |
| 3 Superposition | Phase transition and pentagon geometry reproduced; three-seed sparsity sweep | [Rung 3](../portfolio/projects/rung-3-superposition/index.md) |
| 4 Circuit patching | The ablation and path-patching cascade runs end to end on a real head. That head copies by position, so this validates the method, not an induction circuit | [Rung 4](../portfolio/projects/rung-4-circuit-patching/index.md) |
| 1 Prefix copying | Heads form, but the dissociation probe shows a fixed-offset copy: the periodic task admits a positional shortcut | [Rung 1](../portfolio/projects/rung-1-induction-heads/index.md), [ADR-0032](adr/0032-induction-detector-and-the-positional-shortcut.md) |
| 1b Content-based copying | Behaviour is content-based on three seeds of three; the pre-registered per-head rule confirms a head on one. Two verdicts are published and kept apart | [ADR-0033](adr/0033-content-based-induction-task.md), [Honesty Ledger](../portfolio/RESULTS.md) |
| 5 Sparse autoencoder | Reproduces on synthetic activations. On real activations the dictionary is sparse but most features are dead | [Rung 5](../portfolio/projects/rung-5-sae/index.md) |

Not attempted: automated circuit discovery (descoped), and anything on a
natural-language model.

## Known defects that are still open

- **Seeding.** In `exp1`, `exp3` and `exp4` the model is constructed before the
  per-seed `set_seed` call, so a seed pins the data and the batch order but not
  the initial weights. Each command still reproduces its own manifest exactly;
  what is not valid is comparing two code paths at the same nominal
  configuration. See the 2026-11-12 entry of the
  [Honesty Ledger](../portfolio/RESULTS.md). The fix and the re-measurement are
  planned work.
- **Open question on Rung 1b.** One head carries the copy causally, yet it does
  not put its attention mass on the content key. Why is not known.
- **Phase diagram.** The protocol-ablation sweep (issue #168) has not produced a
  tracked manifest. No claim about it appears in the record.

## How a claim is backed

1. An experiment writes a **manifest** to `results/<name>.json`: seeds,
   arguments, per-seed metrics, aggregate statistics, wall clock, git SHA and
   dirty flag, device and library versions. The schema is `ResultsManifest` in
   [`src/results.py`](../src/results.py).
2. A document that states a number carries a tag in the same section:
   `<!-- manifest: results/<name>.json -->`.
3. `make verify-claims` fails if a tag does not resolve to a tracked manifest,
   if a manifest was recorded on a dirty tree, or if a tracked manifest is cited
   nowhere.
4. `make docs-audit` fails if a number in a table is not in the manifests its
   section cites, or if a sentence that was retracted reappears.

Neither check parses free prose. A number in a sentence, outside a table, is
checked only by the retracted-sentence list. That is a real limit of the method.

## Re-running

```bash
uv sync
make reproduce-quick            # every rung, reduced configuration, CPU, minutes
make reproduce-superposition    # Rung 3, full scale, CPU
make reproduce-grokking         # Rung 2, full scale; hours on CPU, use a GPU
```

The GPU rungs run on free Kaggle or Colab through one driver: see
[GPU runs](agents/gpu-runs.md). `--quick` runs write to
`results/probe_<name>_quick.json`, which is untracked on purpose, so a smoke run
cannot overwrite the record.

To check one published number: open the manifest named by the tag next to it and
read `aggregate.<metric>.mean` and `.std`, or the per-seed rows in
`per_seed_metrics`. The index of every tracked manifest, with what cites it, is
[`results/INDEX.md`](../results/INDEX.md).

## Disputing a number

If a number does not reproduce, or a sentence overstates its manifest, open an
issue with the command you ran, the commit, and the manifest you obtained. A
confirmed discrepancy becomes a dated entry in the Honesty Ledger, with credit,
and the false sentence joins the ratchet in
[`scripts/docs_audit.py`](../scripts/docs_audit.py). Independent reproductions on
different hardware are especially welcome; see
[CONTRIBUTING](../.github/CONTRIBUTING.md).

## Reusing the method

The manifest and the two checks do not depend on this project's experiments.
Extracting them into a standalone library is planned; until then,
`src/results.py` and `scripts/docs_audit.py` can be copied under the MIT license.
