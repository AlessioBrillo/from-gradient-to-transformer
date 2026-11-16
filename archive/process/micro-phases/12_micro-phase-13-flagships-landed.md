---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-07
---

# Micro-Phase 13 — The Flagships, Landed (roadmap)

Written before the runs, as a personal learning log and a public record.
[[11_micro-phase-12-resilient-flagship-run]] answered the infrastructure question —
"can this machine be trusted with a seventeen-hour run again?" — with a mechanically
enforced evidence gate and a checkpoint/resume path that survived a real hard kill,
bit-identical. This phase answers the two questions no amount of preparation can: **does a
real induction head form at standard scale, and does P=113 actually grok?**

Everything downstream is waiting on those two verdicts: Rung 4's path patching on a real
head, Rung 5's real-activation SAE, the clean-clone gate, and the first paper prose. That
upstream is the entire point of this phase — it launches both flagships for real, under
supervision, and records whatever comes back as honestly as every previous phase did.

## Where this phase starts (state review, verified against the repo)

Checked with `git status` / `git diff origin/dev` first — the standing lesson of MP-12 is
that memory is not evidence.

- **MP-12 Steps 0–2 are committed and pushed** (`d5c6fc0`, `c7a3df1`); the working tree is
  byte-identical to `origin/dev`. The "crisis" was real for exactly as long as it was
  unverified; the corrected record is in
  [[11_micro-phase-12-resilient-flagship-run]].
- **The evidence gate is enforced, not optional.** `make verify-claims` now checks figure
  existence, git tracking, and per-section manifest tags. The 12 curated figures in
  `portfolio/figures/` are already committed (with `c7a3df1`); the only things the gate
  still flags are the two sections that genuinely have no manifest of their own yet —
  Rung 2 and Rung 5 — which is correct behavior until their runs land. The three figures
  that cannot be honestly backed yet (`exp4_head_ablation.png`, `exp5_sparsity_tradeoff_real.png`,
  `exp5_feature_histogram_real.png`) have been struck from `RESULTS.md`, not faked.
- **Kill drill passed.** A real `Stop-Process -Force` mid-run, resumed, diffed against an
  uninterrupted reference: `max_abs_diff = 0.000e+00` for every tracked metric and every
  parameter tensor — exact equality, across a real process boundary. Known limits are
  recorded in [[06_production_ai/notes/checkpoint-resume-durability]]: the drill ran
  30 epochs (not 3000), with no other process contending for CPU at kill time, and the
  figure-generation failure class remains undrilled.
- **Both flagships are instrumented and unpulled.** Rung 1 `--standard` (vocab 2048,
  seq 64, d_model 64, 2 layers / 4 heads, 3000 epochs, fresh batches) has the K-composition
  detector, checkpoint/resume, and a progress-measure suite. Grokking P=113 (d_model 128,
  4 heads, d_mlp 512) has `--seeds`, the Fourier-sparsity progress measure, and a hardened
  Colab notebook (`notebooks/colab_grokking_full_run.ipynb`) with `scripts/pin_colab_run.py`
  guarding the SHA contract.
- **Gaps carried into this phase.** Rung 3's pentagon geometry is currently backed only by a
  `--quick` regeneration (the full-scale job died silently twice, ~50 minutes in, with zero
  output — the same silent-death class MP-11 exposed for training runs). The clean-clone gate
  (`scripts/clean_clone_check.sh`) has never run end-to-end. The paper scaffold has zero
  prose. These decide part of this plan's shape.

## Dependency chain — what has to happen and in what order

```
Step 0: Ship the evidence base (commit the 12 figures, fix the one platform-dependent test)
                                      │
            ┌─────────────────────────┼────────────────────────────┐
            ▼                         ▼                            ▼
  Step 1: R1 --standard   Step 2: P=113 x3 seeds    Step 3: R3 geometry
  supervised, ~17-20 h     Colab GPU, async          FULL regeneration
  with heartbeat           with Drive checkpoints    under a watchdog
            └───────────────┬──────────────────────────────┘
                            ▼
            head formed? ──► no: K-composition "how far" figure IS the deliverable
                            │yes
   Step 4: R4 E2E (path patching on a real head) + R5 SAE re-test on the head checkpoint
                            ▼
   Step 5: clean-clone gate → Step 6: paper prose in evidence order
                            ▼
   Step 7: reconcile RESULTS.md, ledger entry, merge dev→main on green CI
```

Facts that shaped the sequencing:

1. **The two flagships interrogate different machines.** R1 burns local CPU and needs
   supervision; P=113 needs Colab GPU and runs async. Launching both in the same
   wall-clock window is how the phase stays at two runs, not four.
2. **The cascade stays conditional, but no longer optional.** If no head forms, the
   K-composition "how far" figure is a first-class deliverable — MP-11's diagnostic means
   the only bad outcome is silence.
3. **Evidence a reviewer can't re-produce isn't evidence.** Every result lands as a
   manifest plus a committed figure under Step 0's gate, or it isn't a result yet.
4. **Supervision is a control, and it now covers figures too.** The kill drill proved out
   training checkpoints; the figure generator is a long unattended job of the same family,
   and Step 3 extends the same discipline to it before the paper needs that figure.

## Steps

### Step 0 — Ship the evidence base

The 12 curated figures that back real claims are already committed (`c7a3df1`); what
remains here is the one pre-existing, platform-dependent red test:
`test_results.py::test_non_json_safe_args_are_stringified` hard-codes a POSIX path literal
and only passes on CI. Root cause: `src/results.py` stringifies non-JSON-safe args with
`str(value)`, which renders `Path` values using the host separator. On Windows that is
`\some\path`, not `/some/path`. Fix is to stringify explicitly (via `os.fspath`) and assert
platform-neutrally. Also track the agent docs in `docs/agents/` (referenced from CLAUDE.md)
so the tree is fully under version control. This is Step 0 because it removes the only
known red test on this disk before anything new enlarges the surface.

### Step 1 — Rung 1 `--standard`, supervised (CPU, ~17-20 h)

Launch `python -m src.experiments.exp1_induction_heads --standard --seeds 0` with the
kill-drilled checkpoint interval. Use a real supervision pattern — a heartbeat log appended
at a fixed cadence by a watchdog, and an active check-in — not MP-11's detached-and-forgotten.
A deliberate mid-run kill + `--resume` rehearses the durability drill at a scale that is no
longer a toy. Only two outcomes are acceptable: **confirmed head, causally verified**, or a
**K-composition "how far" figure** with the honest verdict. Silence is failure; the verdict
must land in the manifest and in `RESULTS.md`.

### Step 2 — Colab P=113 × 3 seeds (GPU track, async)

Supervised launch of `notebooks/colab_grokking_full_run.ipynb`. Drive-checkpointed — the
GPU-side analogue of the kill drill, because free-tier Colab disconnects are a documented
failure class. `scripts/pin_colab_run.py` refuses to record results against a mismatched
commit SHA. Success targets, pre-decided: mean `final_val_acc > 0.9`,
`generalization_epoch` well under 5000, `k_99_percent` in the 10–20 band, sane progress
measures. Seed budget is fixed at 3 *before the run*: a genuine negative is recorded as
evidence, not as a license to p-hack.

### Step 3 — Rung 3 geometry at full scale (the silent-death fix)

The pentagon-geometry claim is currently backed only by the `--quick` regeneration. Regenerate
`make reproduce-exp3-geometry` at full scale under a supervision script that logs a heartbeat,
detects an abnormal exit, and relaunches — the job is stateless, so recovery is retry, and the
supervision is what must be durable. The paper's Rung 3 section then cites a full-scale result
instead of a reduced-budget stand-in, and the watchdog pattern is documented as reusable infra.

### Step 4 — The cascade (conditional, only if a head formed)

- **Rung 4 end-to-end**: activation patching, path patching at the named (layer, head), head
  ablation — the first time `run_path_patching_to_logits()` runs against a real head instead
  of only its unit tests. Treat the first number with suspicion and re-derive one by hand if
  it comes out too clean. New standard-scale manifest.
- **Rung 5 re-test**: `--activations-from` on the head-bearing checkpoint; the L0 / FVE delta
  against the dense 53%-L0 reading is reported honestly, whichever way it lands.

### Step 5 — Clean-clone gate (Phase 6 closure, for the first time)

`scripts/clean_clone_check.sh` run end-to-end, transcript captured, and the proof
`06_production_ai/proofs/reproducible-from-clean-clone.md` written from the *actual* output —
not from what the script is supposed to do. Any manual step required is a failed gate.

### Step 6 — Paper prose in evidence order

Methods, then Rung 3 (the strongest, fully-reproduced result), then each additional rung whose
manifest has landed. Every paragraph cites a manifest or a committed figure; nothing is written
that isn't already in `RESULTS.md`. Figures struck in Step 0 are rebuilt by a real run first —
there is no "quote it back in" without new evidence.

### Step 7 — Close the phase

Reconcile `RESULTS.md` with every new manifest; run `make verify-claims` to zero
does-not-exist/untracked problems; one honesty-ledger entry including this phase's own
missteps; merge `dev` → `main` only on green CI; archive this roadmap in the progress log with
deviations noted.

## Deep-dive study and research topics

1. **Process supervision as a research skill, not an OS quirk.** Watchdog loops, heartbeat
   logs, restart semantics — this vault has now had the "detached and forgotten = dead run"
   failure twice, so this is a standing competency to actually acquire.
2. **Cross-process floating-point determinism (the untested hypothesis).** The kill drill ran
   with no CPU contention. PyTorch determinism docs, plus a deliberate under-load drill, are
   the way to close the one gap the drill honestly logged.
3. **The Fourier decomposition of modular addition — from theory to weights.** Re-read
   Nanda et al. (ICLR 2023) and Power et al. (2022) before Step 2, and re-derive
   `cos(2πk(a+b)/P)` so the frequencies in the plots are recognized from theory, not trusted
   from the axis labels.
4. **Path-patching correctness (before first real use).** Zhang & Nanda, "Towards Best
   Practices of Activation Patching" (ICLR 2024) — the site/aggregation mistakes it catalogs
   are exactly the ones this repo already committed twice on activation patching, and Step 4
   is path patching's first time on a real head.
5. **Colab session durability, applied this time.** Checkpoint-to-Drive, keep-alive, and the
   `pin_colab_run.py` SHA contract — the GPU-side version of everything the kill drill proved
   for local processes.
6. **Watchdog infrastructure for long figure-generation jobs.** A small driver script, a log
   heartbeat, an abnormal-exit restart — the same supervision class one layer down. This is
   now a standing pattern in the repo, not a one-off (see Step 3).

## Documentation requirements

- **Progress log**: one dated entry per session, raw pass/fail recorded before any
  interpretation — including for a failed run.
- **New/existing notes**: update `04_nlp_and_transformers/notes/induction-heads.md` with the
  Step 1 verdict either way; add a short *figure supervision / watchdog* note under
  `06_production_ai/notes/`; `05 notes on path patching already exist and get updated from
  real numbers.
- **`02_skill-tree.md`**: flips only with proof — *induction-head reproduction* on a
  confirmed + causally verified head; *grokking reproduction* on the P=113 manifests; a new
  *reproducible job durability for long jobs* line if the watchdog (Step 3) becomes a real,
  checked pattern.
- **`portfolio/RESULTS.md`**: new manifests, ledger entry, figure citations reconciled
  against Step 0's contract.
- **Paper**: Methods + Rung 3 (and more) written in evidence order, every paragraph tied to a
  manifest or committed figure.
- **Vault conventions**: every new/exercise carries the vault's two-link minimum and proper
  tags.

## Practical exercises and challenges

1. **Challenge — the supervised R1 `--standard` run.** Heartbeat, deliberate mid-run kill,
   `--resume`, verify against the checkpoint, and the verdict: confirmed head **or** the
   "how far" figure. This is the phase in essence.
2. **Challenge — P=113 × 3 seeds on Colab.** Launch, monitor, Drive-checkpoint, download,
   pin, verify, `RESULTS.md` entry. The primary flagship — or a recorded negative with named
   suspects (embedding re-normalization, the cosine schedule: the P=113 only unknowns).
3. **Challenge — the R3 watchdog regeneration.** Driver script with heartbeat and restart,
   full-scale geometry, confirmed pentagon numbers, documented as reusable infra.
4. **Exercise — one Fourier frequency, verified by hand.** After a grokked P=113, take the
   top frequency, write the trig expression it implies for logits[a+b], and verify against
   the model's embeddings — proof end-to-end, not at the plot level.
5. **Challenge — the clean-clone gate.** `scripts/clean_clone_check.sh` end to end, proof
   written from the transcript.
6. **Exercise — score the 2026-08-02 pre-registration.** Grade the MP-9/MP-10 predictions
   against what actually happened. Costs nothing but honesty, and is exactly the practice
   that catches a roadmap that drifted from its own plan.
7. **Exercise — repeatable self-audit.** Before every commit this phase: *figure on
   disk? tracked in git? bound to a manifest?* — the same three questions the gate asks.

## Strategic tips and best practices

- **Verify the state against the repository before believing a narrative about it.**
  One `git diff origin/dev` and the whole "crisis" of MP-12 collapsed into a real but small
  fork. The lesson generalizes: mean plots before the run, audit after.
- **A supervised run that ends "no head, here's the diagnostics" is a stronger deliverable
  than an unattended run that vanishes without a trace.** Supervision is not a nice-to-have
  around real research; it is the ducting that turns a compute bill into evidence.
- **Quick scale is a smoke test, never a result.** It survives as a CI/gate tool and for
  exploratory one-variable checks, never in `RESULTS.md` as the canonical number.
- **Never trust an unattended long job with a path that hasn't survived a real death.**
  The kill drill covered training; Step 3 extends it to figure generation, because the
  figure regenerator is the same class of long, silent, killable job.
- **One variable per experiment, one ledger entry per phase.** The checkpoint/geometry
  drills follow the repo's own honesty-era rules: a negative with a named suspects wins
  over a silent gap.
- **Do not leave a "user-facing promise" in RESULTS.md that can't be regenerated.**
  Anything struck in Step 0 stays struck until real evidence (manifest + figure) exists.
- **Gate the merge on CI, never on hope.** The phase closes when `dev` CI is green and
  `dev → main` merge is clean, with the tree verified after.

## Gate criteria — what green looks like

1. Evidence base shipped: the 12 figures and `docs/` tracked, `verify-claims` at 0
   "not on disk" problems, and the platform-dependent test fixed green on Windows
   and CI alike.
2. R1 `--standard`: a verdict that is **not silence** — confirmed head + causal verification,
   or a committed K-composition "how far" figure. Both are results.
3. P=113 × 3 seeds: ≥2 seeds grokked, manifests pinned via `pin_colab_run.py`, Fourier +
   frequency-ablation figures committed — or a recorded honest negative with named suspects.
4. R3 geometry: full-scale regeneration with the watchdog, pentagon claim confirmed at the
   canonical budget, not the reduced one.
5. Clean-clone gate: run end-to-end at least once, proof written from the transcript.
6. Rung 4 end-to-end (path patching on a real head) and the R5 SAE re-test on the head
   checkpoint — or, if no head formed, the gap is named in the ledger, not silently closed.
7. Paper prose in evidence order; every paragraph tied to a manifest or committed figure.
8. Full suite green locally (ruff + blocking mypy + ≥185 tests), GitHub CI green on `dev`,
   `dev` merged to `main`, tree post-merge clean.

## Links

- [[11_micro-phase-12-resilient-flagship-run]] — the phase this builds on (fork fix, evidence
  gate, kill drill).
- [[10_micro-phase-11-flagship-run]] — the K-composition detector and probe verdicts this
  phase's Step 1 goes to verify.
- [[08_micro-phase-09-the-flagship-runs]] — the 2026-08-02 pre-registration this phase
  should score (exercise 6).
- [[09_micro-phase-10-evidence-run]] — the run instruments that make Step 2 safe to launch.
- [[04_nlp_and_transformers/notes/induction-heads]] — Rung 1's working note, updated by Step 1's verdict.
- [[portfolio/RESULTS]] — the ledger this phase must change.
- [[06_production_ai/proofs/kill-drill-checkpoint-resume]] — the durability proof this phase
  extends to the GPU and to figure generation.