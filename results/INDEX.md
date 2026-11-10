# results/INDEX — ratchet degli orphan manifest

Questo file è il contratto di tracciabilità per `results/`. Ogni manifest
tracked qui elencato è un pezzo di evidenza pubblica: un lettore che clona
la repo deve poterlo trovare, verificare (`make verify-claims`) e collegare
al documento che lo cita.

## Convenzione

- Un manifest è **citato** se appare come `<!-- manifest: results/<file>.json -->`
  in `portfolio/RESULTS.md`, `portfolio/paper/main.tex`, o `07_capstone/writeup.md`.
- Un manifest **orfano** è tracked ma non citato da nessun documento
  current-facing. Gli orfani non sono errori per definizione, ma devono
  essere elencati esplicitamente qui con una motivazione, così il ratchet
  `docs_audit.py` li vede e nessun orfano si nasconde per silenzio.

## Manifest tracked

| Manifest | Citato da | Stato | Note |
|---|---|---|---|
| `results/capstone_20k.json` | RESULTS.md, writeup.md | attivo | Capstone 3 seed x 20k |
| `results/capstone_20k_energy.json` | RESULTS.md | attivo | Energia capstone |
| `results/exp1_induction_fixed_batches.json` | RESULTS.md | attivo | Rung 1 arm A |
| `results/exp1_induction_fresh_batches.json` | RESULTS.md | attivo | Rung 1 arm B |
| `results/exp1_induction_heads.json` | RESULTS.md | attivo | Rung 1 standard |
| `results/exp2_grokking.json` | RESULTS.md | attivo | Rung 2 grokking |
| `results/exp3_superposition.json` | paper, RESULTS.md | attivo | Rung 3 |
| `results/exp4_circuit_patching.json` | paper, RESULTS.md | attivo | Rung 4 |
| `results/exp4_standard.json` | paper, RESULTS.md | attivo | Rung 4 standard |
| `results/exp5_real_activations.json` | paper, RESULTS.md | attivo | Rung 5 |
| `results/exp5_sae_dashboard.json` | RESULTS.md | attivo | Rung 5 SAE |
| `results/exp6_capstone.json` | — | **ORFANO** | Vecchio run 2026-09-04, git_sha=c9f9df1, P=17, 100 step; probabilmente superato da capstone_20k. Non cancellare: è evidenza storica. |
| `results/grokking_nanda_p113.json` | paper, RESULTS.md | attivo | Rung 2 flagship |
| `results/grokking_p113_gpu_reanalysis.json` | RESULTS.md | attivo | Re-analisi GPU |
| `results/grokking_p59_repo_energy.json` | paper | attivo | Positive control P=59, 2/3 seed sparse (MIXED) |
| `results/grokking_repo_p113_energy.json` | paper | attivo | Repo protocol P=113 |
| `results/induction_content.json` | paper (§content-task), writeup.md | attivo | Content task run, 3 seed x 3000 epoca |
| `results/induction_content_derisk.json` | — | orfano (scratch) | CPU smoke, non record |
| `results/induction_content_derisk_fixed.json` | — | orfano (scratch) | CPU derisk fixed |
| `results/induction_content_derisk_standard.json` | paper (§content-task) | attivo | CPU derisk standard |
| `results/induction_standard.json` | paper, RESULTS.md | attivo | Rung 1 standard scale |
| `results/induction_standard_emergence.json` | paper | attivo | Emergence probe |
| `results/phase_diagram_positive_control.json` | writeup.md | attivo | Positive control P=59 (citato solo in writeup; se il check ignora il writeup è anch'esso orfano) |
| `results/probe_capstone_ab_control.json` | — | orfano (scratch) | Retune A/B control |
| `results/probe_capstone_ab_offset.json` | — | orfano (scratch) | Retune A/B offset |
| `results/probe_capstone_ab_reweight.json` | — | orfano (scratch) | Retune A/B reweight |
| `results/probe_capstone_fixcheck.json` | 03_progress-log.md:333 | **ORFANO (allowlist)** | Kill-drill fixcheck, citato in 03_progress-log.md:333. Non in RESULTS.md/paper/writeup. |
| `results/probe_capstone_resume.json` | 03_progress-log.md:335 | **ORFANO (allowlist)** | Kill-drill resume, citato in 03_progress-log.md:335. Non in RESULTS.md/paper/writeup. |
| `results/probe_capstone_shakedown.json` | — | orfano (scratch) | Capstone shakedown |

## Allowlist esplicita (capstone / probe)

I seguenti manifest sono orfani rispetto a `RESULTS.md` + `paper/main.tex` +
`writeup.md` ma sono intentionalmente conservati come evidenza del kill
drill / resume, citati da `00_meta/03_progress-log.md`:

- `results/probe_capstone_fixcheck.json` (progress-log:333)
- `results/probe_capstone_resume.json` (progress-log:335)

Il controllo positivo P=59 (`results/grokking_p59_repo_energy.json`) è
citato dal paper (`\S\ref{sec:content-task}` vicinity). Il manifest
`results/phase_diagram_positive_control.json` è citato solo da
`07_capstone/writeup.md:72`; se un check di citazione ignora il writeup,
questo manifest è anch'esso orfano e va aggiunto al documento current-facing
appropriato.

## content_verdict.json

`results/content_verdict.json` è **gitignored** (`.gitignore`): è un
artifact derivato, rigenerato con `make content-verdict` dai manifest di
input (`induction_content.json`, `exp4_content.json` quando esiste). Non è
un `ResultsManifest`, non viene pinnato, non entra in questo INDEX.

## Come usare questo file

`make docs-audit` verifica che ogni documento current-facing che dichiara
uno status porti il tag del manifest a supporto. Questo INDEX è il registro
contrario: elenca i manifest tracked e dichiara quali sono orfani e perché.
Se un nuovo manifest appare in `results/` senza essere qui elencato e senza
citare un documento, il ratchet deve fallire.
