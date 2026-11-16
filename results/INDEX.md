# results/INDEX — the orphan-manifest ratchet

This file is the traceability contract for `results/`. Every tracked manifest
listed here is a piece of public evidence: a reader who clones the repository
must be able to find it, verify it (`make verify-claims`) and connect it to the
document that cites it.

## Convention

- A manifest is **cited** if it appears as `<!-- manifest: results/<file>.json -->`
  in `portfolio/RESULTS.md`, `portfolio/paper/main.tex` or `07_capstone/writeup.md`.
- An **orphan** manifest is tracked but cited by no current-facing document.
  Orphans are not errors by definition, but each must be listed here with a
  reason, so that `docs_audit.py` sees them and no orphan hides by silence.

## Tracked manifests

| Manifest | Cited by | Status | Notes |
|---|---|---|---|
| `results/capstone_20k.json` | RESULTS.md, writeup.md | active | Capstone, 3 seeds x 20k steps |
| `results/capstone_20k_energy.json` | RESULTS.md | active | Capstone energy re-analysis |
| `results/exp1_induction_fixed_batches.json` | RESULTS.md | active | Rung 1 arm A |
| `results/exp1_induction_fresh_batches.json` | RESULTS.md | active | Rung 1 arm B |
| `results/exp1_induction_heads.json` | RESULTS.md | active | Rung 1 standard |
| `results/exp2_grokking.json` | RESULTS.md | active | Rung 2 grokking |
| `results/exp3_superposition.json` | paper, RESULTS.md | active | Rung 3 |
| `results/exp3_superposition_sweep.json` | paper, RESULTS.md, writeup.md | active | Rung 3 sparsity sweep |
| `results/exp4_circuit_patching.json` | paper, RESULTS.md | active | Rung 4 |
| `results/exp4_content.json` | RESULTS.md, writeup.md, checklist.md, paper | active | Causal addendum of the content task (criterion 7), executed after the run (`88147ee`), at commit `891ef46`; the two verdicts are published separately |
| `results/exp4_standard.json` | paper, RESULTS.md | active | Rung 4 standard |
| `results/exp5_real_activations.json` | paper, RESULTS.md | active | Rung 5 |
| `results/exp5_sae_dashboard.json` | RESULTS.md | active | Rung 5 SAE |
| `results/exp6_capstone.json` | — | **ORPHAN** | Old run of 2026-09-04, git_sha=c9f9df1, P=17, 100 steps; probably superseded by capstone_20k. Do not delete: it is historical evidence. |
| `results/grokking_nanda_p113.json` | paper, RESULTS.md | active | Rung 2 flagship |
| `results/grokking_p113_gpu_reanalysis.json` | RESULTS.md | active | GPU re-analysis |
| `results/grokking_p59_repo_energy.json` | paper | active | Positive control P=59, 2/3 seeds sparse (MIXED) |
| `results/grokking_repo_p113_energy.json` | paper | active | Repo protocol P=113 |
| `results/induction_content.json` | RESULTS.md, writeup.md, checklist.md, paper (§content-task) | active | Content task run, 3 seeds x 3000 epochs — pre-registered verdict |
| `results/induction_content_derisk.json` | — | orphan (scratch) | CPU smoke run, not a record |
| `results/induction_content_derisk_fixed.json` | — | orphan (scratch) | CPU de-risk, fixed batches |
| `results/induction_content_derisk_standard.json` | paper (§content-task) | active | CPU de-risk, standard |
| `results/induction_standard.json` | paper, RESULTS.md | active | Rung 1 standard scale |
| `results/induction_standard_emergence.json` | paper | active | Emergence probe |
| `results/phase_diagram_positive_control.json` | writeup.md | active | Positive control P=59 (cited only in the writeup; if a check ignores the writeup it is an orphan too) |
| `results/probe_capstone_ab_control.json` | — | orphan (scratch) | Retune A/B, control arm |
| `results/probe_capstone_ab_offset.json` | — | orphan (scratch) | Retune A/B, offset arm |
| `results/probe_capstone_ab_reweight.json` | — | orphan (scratch) | Retune A/B, reweight arm |
| `results/probe_capstone_fixcheck.json` | 03_progress-log.md:333 | **ORPHAN (allowlist)** | Kill-drill fixcheck, cited in 03_progress-log.md:333. Not in RESULTS.md, the paper or the writeup. |
| `results/probe_capstone_resume.json` | 03_progress-log.md:335 | **ORPHAN (allowlist)** | Kill-drill resume, cited in 03_progress-log.md:335. Not in RESULTS.md, the paper or the writeup. |
| `results/probe_capstone_shakedown.json` | — | orphan (scratch) | Capstone shakedown |

## Explicit allowlist (capstone / probe)

The following manifests are orphans with respect to `RESULTS.md`,
`paper/main.tex` and `writeup.md`, but are kept on purpose as evidence of the
kill drill and the resume, cited from `00_meta/03_progress-log.md`:

- `results/probe_capstone_fixcheck.json` (progress-log:333)
- `results/probe_capstone_resume.json` (progress-log:335)

The P=59 positive control (`results/grokking_p59_repo_energy.json`) is cited by
the paper (near `\S\ref{sec:content-task}`). The manifest
`results/phase_diagram_positive_control.json` is cited only by
`07_capstone/writeup.md:72`; if a citation check ignores the writeup, this
manifest is an orphan too and must be added to the appropriate current-facing
document.

## content_verdict.json

`results/content_verdict.json` is **gitignored** (`.gitignore`): it is a
derived artifact, regenerated with `make content-verdict` from its input
manifests (`induction_content.json`, and `exp4_content.json` when it exists).
It is not a `ResultsManifest`, it is not pinned, and it has no row in this
index.

## How to use this file

`make docs-audit` checks that every current-facing document declaring a status
carries the tag of the manifest behind it. This index is the reverse register:
it lists the tracked manifests and states which ones are orphans and why. If a
new manifest appears in `results/` without a row here, the ratchet fails.
