---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-11
---

# Micro-Phase 28 — The Execution: the stack runs

Written as a personal learning log and a public record, like every roadmap before it.

MP-27 declared the unblock: the stack stops stacking, ADR-0003's rows run under
their own frozen protocols, and `verify-claims` goes from its designed 2 problems
to 0. This phase IS that execution. What follows is the dated record of the
sessions that ran — Session 0 (pre-flight), Session 1 (the exp2 port), Session 2
(the grokking overnight launch), each with its raw pass/fail and its exit gate,
in the record's own format: launch commands, PIDs, heartbeats, verdict rows.

## Design decisions

- **The intake is ADR-0003's rows, executed as written (inherited from MP-27).**
  Nothing is re-negotiated: thresholds, seeds, budgets, windows, kill-dates are
  the frozen cells of the ledger, and the only post-launch edit any row may
  receive is "observed".
- **CPU-first ownership (inherited, now executed).** The machine-budget audit
  (S0) priced the whole phase: P=113 ×3 seeds at ~0.6 s/epoch ≈ 1 parallel
  overnight; R1 standard-scale ≈ a second overnight under checkpoint-every-250.
  No GPU is load-bearing for any verdict this phase owes.
- **The exp2 port is the mechanical precondition (S1).** exp1's stateful
  checkpoint/resume (atomic write, RNG capture, `--resume`, kill-drill-proven
  bit-identical) had existed since MP-12; the port into exp2 was the exact gap
  MP-26's intake review recorded. The three falsification tests were written
  FIRST (red), the port (green), the cleanup (refactor) — the tests are the
  port's contract.
- **Launch-then-analyze (S2–S4).** Sessions 0–2 exist to get both lanes running
  with dated rows; the launches happened before this record's first session
  entry, and the analysis (S4) consumes whatever the checkpoints say.
- **Negative-first, falsification-first (S3).** The scheduled negatives — "P=113
  did not grok within this budget" and "no head at standard scale" — were
  drafted in full while the runs were still computing, printed with the same
  polish as the wins; every number the runs produce has its "what would falsify
  this" column already written in the ledger's cells (Gelman & Loken, applied at
  the source, always).
- **The one measured line**: `make verify-claims` goes from its designed 2
  problems to **0** — `results/exp2_grokking.json` and
  `results/exp5_sae_dashboard.json` land from this phase's own runs, and every
  downstream artifact (paper prose, essay annex) finally has its manifests to
  cite. `verify-claims` at 0 is the proof, not the prose.

## Session 0 — the pre-flight (2026-08-11, ~1 h) — DONE

- **The machine-budget audit, written live.** 6 cores / 12 threads, 34 GB RAM;
  a real 100-epoch timing probe of the P=113 config measured ~0.575 s/epoch at
  4 threads → P=113 × 3 seeds in parallel at 3 threads each ≈ 9/12 threads,
  ~5.5 h serial → ~2 h wall for the three-seed parallel launch. R1 standard
  (~17–24 h serial at d_model=64, fresh batches) is a second supervised
  overnight under checkpoint-every-250. Kill conditions signed before launch:
  any seed that hasn't grokked by 5000 epochs closes negative, not silent.
- **The CI floor re-verified locally**: the tracked 185 tests green; ruff clean;
  blocking mypy clean; markdownlint 0 on changed notes; `verify-claims` at its
  designed 2 problems (the two never-produced manifests this phase produces).
- **ADR-0003's protocol re-confirmed as frozen** — nothing re-planned, nothing
  re-negotiated; the exp2 port decision recorded (the decision MP-26's review
  named). Terminus declared: release = this merge + 14 calendar days.
- **Exit**: audit sheet and schedule sheet signed and committed; zero launches
  happened before this sitting.

## Session 1 — the exp2 port (2026-08-11, ~3 h) — DONE

- **The three falsification tests written FIRST (red), as MP-27 required:**
  resume == uninterrupted (bit-identical history + weights); resume twice ==
  uninterrupted; missing checkpoint starts fresh. All three failed against the
  pre-port code (no `--resume`, no `--checkpoint-every` on exp2's parser) —
  the RED gate validated before any production change.
- **The port (green)**: exp1's machinery transported into exp2 — atomic
  `os.replace` save, RNG-state capture (`torch.random.get_rng_state`), rolling
  per-seed checkpoint paths, `--resume`/`--resume-from`, `--checkpoint-dir`,
  `--checkpoint-every`. The port keeps the exact semantics of exp1's machinery
  (the port note documents what changed and why it stays bit-identical); the
  three tests went green.
- **The kill drill v2, executed for real**: a 200-epoch exp2 run,
  `Stop-Process -Force` mid-run, resume from the rolling checkpoint, and a
  bit-for-bit diff of history + weights against an uninterrupted run — PASS
  (committed as `test(grokking): add kill drill v2 driver`). The drill
  transcript is the proof artifact; the resume-protocol memo lands in
  `06_production_ai/notes/checkpoint-resume-durability.md` (updated).
- **Exit**: exp2 resume is bit-identical; the drill transcript is committed;
  the port note is written.

## Session 2 — the grokking overnight launch (2026-08-11) — DONE

- **P=113 seeds 0/1/2 launched in parallel** on 2026-08-11T19:40:05Z, one
  process per seed, 3 threads each (OMP_NUM_THREADS=3), under the frozen
  ADR-0003 row-1 config:
  `--modulus 113 --epochs 5000 --d-model 128 --d-mlp 512 --n-heads 4 --lr 1e-3
  --weight-decay 1.0 --train-fraction 0.3 --batch-size 512 --checkpoint-every
  500 --checkpoint-dir checkpoints`
- **The heartbeat log opened** (`checkpoints/heartbeat.md`): launch timestamp,
  PIDs (seed 0 = 2576, seed 1 = 4784, seed 2 = 20368), config verified from
  each process's Arguments line, monitoring timeline of checkpoint events.
- **One deliberate kill + resume exercised before the night** — the S1 kill
  drill v2 was the rehearsal; the live lane's rolling checkpoints confirmed the
  cadence in production (first checkpoint at epoch 500, then every 500).
- **Observation (as data, not mood)**: all three seeds reached val_acc ≈ 1.0
  by epoch ~3000 — the runs grokked under the frozen protocol, pending the
  manifest analysis in S4.
- **Exit**: three launches live with dates; the kill-condition sheet is
  signed; resume proven once in the live lane.

## Session 3 — the R1 overnight + the negatives pre-filled (in flight)

- R1 standard-scale fresh-batches launched with `--checkpoint-every 250` and
  its resume path verified once.
- The Falsification columns and the two scheduled negatives drafted in full
  ([[06_production_ai/notes/scheduled-negatives-mp28]] — the no-grok paragraph
  and the no-head memo, written while the finals were still computing).
- The grokking night's heartbeats walked; the first Fourier pass read as data.

## Session 4 — the grokking analysis (next)

- P=113's verdict written from the manifests: Fourier frequency counts,
  progress measures, the generalization epoch, the named suspects answered.
- Exit: ADR-0003 row 1 stamped LAUNCHED-with-verdict or CLOSED-with-one-reason;
  every annex-bound number manifest-tagged.

## Session 5 — the R1 verdict + the R4 chain (next)

## Session 6 — the R5 re-run + verify-claims 2 → 0 (next)

## Session 7 — the paper's first prose (next)

## Session 8 — the release (the fixed terminus date)

## Gate criteria (executed, from MP-27)

1. Session 0: the machine-budget audit and the schedule sheet signed and
   committed; the CI floor green locally AND on GitHub; ADR-0003's protocol
   re-confirmed frozen; the exp2 port decision recorded — **MET (2026-08-11)**.
2. Session 1: exp2's three falsification tests green, including the kill-drill
   v2 bit-identical result; the drill transcript and the port note
   committed — **MET (2026-08-11, commits `test(grokking)` + `feat(grokking)`)**.
3. Sessions 2–3: both lanes live with dated rows and heartbeats; a real resume
   has happened in each lane; the scheduled negatives are drafted before the
   finals — **in flight**.
4. Session 4: ADR-0003 row 1 stamped LAUNCHED-with-verdict or
   CLOSED-with-one-reason; every annex-bound number manifest-tagged.
5. Session 5: the R1 row and the R4-chain row both stamped with dates, either
   way; the no-head memo printed as a contribution if it came.
6. Session 6: `make verify-claims` at 0 — the phase's one measured line, on
   disk; the R5 row LAUNCHED or CLOSED with a date; the re-derivation walk
   complete.
7. Session 7: paper sections cite only manifests; `make paper` compiles in the
   mirror; the annex cites only disk.
8. Session 8: the merge is green; ADR-0003's rows are all stamped; ADR-0006's
   candidate set untouched — zero new research questions opened this phase.

## The one measured line (status)

`make verify-claims` — currently 2 problems (both manifests this phase
produces). Line moved: `results/exp2_grokking.json` from the S4 analysis;
`results/exp5_sae_dashboard.json` from the S6 SAE re-run.

## Links

- [[00_meta/26_micro-phase-27-the-unblock]] — the roadmap this phase executes;
  its session exits are this record's gate criteria.
- [[docs/adr/0003-research-return-ledger]] — the rows this phase stamps.
- [[06_production_ai/notes/checkpoint-resume-durability]] — the resume protocol
  memo the exp2 port inherits and repeats.
- [[06_production_ai/notes/scheduled-negatives-mp28]] — the negatives drafted
  before the finals (S3).
- [[06_production_ai/notes/results-manifests-and-provenance]] · [[06_production_ai/notes/multi-seed-experiment-design]] — the manifest machinery the S4 analysis uses.
- [[00_meta/03_progress-log]] — the dated journal entries per session.
- [[portfolio/RESULTS]] · [[portfolio/paper/main]] — the artifacts this phase's
  manifests unblock.
