---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-07
---

# Micro-Phase 12 — The Resilient Flagship Run (roadmap + record)

Micro-Phase 11 pulled the trigger on the standard-scale Rung 1 domino and left it
running unattended overnight. It went silent — no process, no log, no checkpoint,
seventeen hours of CPU time gone without evidence either way. That incident is what
opened this phase. But the first thing this phase actually had to fix wasn't the run —
it was a wrong diagnosis of the run's own aftermath, written by me, on this machine,
before I'd checked it against the repository. This document's opening section is that
correction, made before the wrong version ever got committed. Written from my own
perspective as a learning log — a self-caught misdiagnosis gets the same honest
treatment as a wrong scientific hypothesis.

## Where this started (state review, 2026-08-07) — corrected

An earlier draft of this document (never committed) opened with a crisis: 24 files of
uncommitted work "at risk," a checkpoint/resume system "started ad hoc under pressure"
and still unstaged, `main` "37 commits behind." I wrote that from memory of the MP11
session, not from the repository. Checking each claim against `git` directly:

| Claim in the earlier draft | What the repository actually shows |
|---|---|
| "24 files staged, +2,380/−153 lines, at risk" | The working tree is **byte-identical to `origin/dev`** except one file (`00_home.md`, the merge conflict itself). `git diff origin/dev --name-only` returns three paths total. Everything else already landed via PRs #33–#36. |
| Checkpoint/resume "started ad hoc, uncommitted" | `save_training_checkpoint`, `load_training_checkpoint`, `--checkpoint-every`, `--resume`, `--resume-from`, and `TestCheckpointResume` are all **already committed on `origin/dev`** (`src/experiments/exp1_induction_heads.py:283,314,1086,1092,1100`; `tests/test_induction_heads.py:387`). |
| "`dev` → `main` gap: 37 commits behind, this phase should close it" | `origin/main == origin/dev`, both at `3ec43ba`. The gap was **already zero**. |
| (carried from MP8) manifests flagged `git_dirty: true` | All three manifests (`results/exp1_*.json`, `exp3_*.json`, `exp4_*.json`) report `"git_dirty": false`. Already fixed, days ago. |

None of that was a lie — it was a snapshot of a session that ended mid-merge, reasoned
about from memory instead of from a fresh `git status` / `git diff origin/dev`. The
correction cost one terminal session. Believing it and spending this phase "rescuing"
already-pushed work would have cost the phase.

**What the corrected check actually found:**

1. **A documentation fork, not lost work.** `00_home.md`'s conflict is a link-list
   collision between two *parallel, non-overlapping* roadmap lines: local
   `08_micro-phase-09-the-flagship-runs.md` + `09_micro-phase-10-consolidation-and-paper.md`
   (written 2026-08-02, forward-looking, each carrying a dated
   `## Predicted Outcomes (Pre-Registration)` section) versus the remote's
   `08_micro-phase-09-flagship-sprint.md` + `09_micro-phase-10-evidence-run.md`
   (2026-08-05/06, written as executed records). The *filenames* never collided — only
   the wiki-links naming them in `00_home.md` did, because both lines were written
   locally, one of them also got pushed and merged by a different session, and this
   branch never pulled it before adding its own. See Step 0 below for the resolution
   and [[00_meta/00_home]] for the result.
2. **`figures/` is gitignored** (`.gitignore:11`, "Generated figures (regenerated with
   `make reproduce`)"). Every figure `RESULTS.md` and the paper scaffold cite is
   invisible to anyone who clones this repo — for a project whose entire premise is
   evidence-backed claims, the evidence itself doesn't ship. Worse: on this disk,
   `figures/` currently holds only **2026-07-26 PNGs**. None of the MP10/MP11-era
   artifacts exist locally — no pentagon-geometry figure, no K-composition diagnostic
   plot, no real-activation SAE figures, no head-ablation figure — and
   `exp6_automated_vs_manual.png` still sits there from Rung 6, which was **deleted
   2026-08-01 for containing fabricated `rng.poisson`/`rng.beta` data**. This was not
   named as a gap by any prior micro-phase.
3. **The genuinely open items are exactly what they were before the misdiagnosis**:
   `results/exp1_induction_heads.json` is still the 150-epoch tiny manifest — the
   standard-scale verdict from MP11's overnight run never landed, because the run
   itself never survived. P=113 has never been executed. The paper scaffold
   (`portfolio/paper/main.tex`, 103 lines) has zero sentences of prose — every section
   is `% TODO`. `scripts/clean_clone_check.sh` exists and is committed but has never
   been run end to end. These are unchanged by the correction above; they were never
   about git hygiene.

## Bottleneck analysis — the dependency chain

```
 Step 0: Resolve the documentation fork, correct the state review, land one commit
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼                                                     ▼
 Step 1: Publish the evidence                        Step 2: The kill drill
 (curate portfolio/figures/,                          (hard-kill --standard for real,
  bind figures to manifests,                          not the in-process unit test,
  drop the fabricated-data                            prove --resume survives it)
  Rung-6 artifact)                                                │
        └─────────────────────────┬─────────────────────────┘
                                  ▼
        ┌─────────────────────────┴─────────────────────────┐
        ▼                                                     ▼
 Step 3a: Colab P=113 ×3 seeds (GPU, async,          Step 3b: Rung 1 --standard,
          launch first)                                       supervised + checkpointed
        └─────────────────────────┬─────────────────────────┘
                                  ▼
                    head formed? ──no──► K-composition "how far" figure is the deliverable
                                  │yes
              Step 4: Rung 4 E2E (path patching) + Rung 5 SAE re-test on the head checkpoint
                                  ▼
        Step 5: Clean-clone gate → Step 6: paper in evidence order → Step 7: close phase
```

Facts that shape the sequencing:

1. **Verify the state before planning against it.** This phase's own opening mistake
   is now the standing example: a plausible-sounding crisis narrative that one
   `git diff origin/dev` disproves. Step 0 is "resolve the fork," not "recover lost
   work," because there was never lost work to recover.
2. **Evidence a reviewer can't see isn't evidence.** Step 1 is promoted to a first-class
   step, not a footnote, because a gitignored `figures/` directory quietly turned every
   visual claim in `RESULTS.md` into an unverifiable promise — the same category of
   problem the 2026-07-26 audit found when `figures/` didn't exist on disk at all.
3. **Durability has to be proven against the real failure mode before it's trusted with
   17 hours again.** `TestCheckpointResume` proves the *logic* by calling `train_model()`
   twice in one process on an 8-epoch toy config. It says nothing about disk-flush
   timing, signal handling, or terminal-close behavior on this machine — that's an
   operational question, and Step 2 answers it before Step 3b risks anything real.
4. **GPU scheduling keeps the MP11 lesson**: launch Colab first since it's the only
   resource that runs in parallel with everything else.
5. **The K-composition detector already removes the worst-case outcome.** Even an
   unwatched Rung 1 run can no longer end in "we don't know" — MP11's diagnostic means
   the only two outcomes are "confirmed" or "diagnosed."

## Steps

### Step 0 — Resolve the fork, land the tree

Reconcile `00_home.md` as a deliberate union: both roadmap lines stay linked, each
labeled honestly (pre-registration vs. executed record) rather than one being deleted
to win the merge. Rewrite this document's own state review with the corrected numbers
above. Commit as one coherent change, then fast-forward the local branch onto
`origin/dev`. This step produces no research result — it produces a tree worth building
on, and a documented correction of the mistake that could have wasted the rest of the
phase.

### Step 1 — Publish the evidence

Establish `portfolio/figures/` as a small, **committed**, curated set — the figures
`RESULTS.md` and `portfolio/paper/main.tex` actually cite, copied there deliberately
after regeneration. `figures/` itself stays gitignored as regenerable scratch (`make
reproduce` output); the contract is that a figure backing a claim is committed
alongside the manifest that produced it, or the claim doesn't get to cite one. Delete
`exp6_automated_vs_manual.png` — it documents a rung removed for fabricated data and
has no reason to survive in any figures directory. No new automation target yet; a
documented copy step is proportionate until the curated set is larger than a handful of
files.

### Step 2 — The kill drill

Launch `--standard` for real, on this machine, with `--checkpoint-every` set to a short
interval. At a known epoch, kill the process the way the MP11 run actually died — not a
clean `Ctrl+C`, a hard kill, ideally a terminal/session close. Confirm: a checkpoint
file exists on disk with the epoch it claims; `--resume` picks it up without re-asking
for the seed; the final manifest is consistent with what `TestCheckpointResume` already
proved in-process. This is the first time the checkpoint code touches a real process
boundary. Record the outcome in the progress log even if it fails — a broken checkpoint
caught in a 10-minute drill is worth more than one discovered 16 hours into the real
run.

### Step 3 — The flagships, launched for real

- **P=113 ×3 seeds on Colab**, launched first and async. Results pinned via
  `scripts/pin_colab_run.py` (refuses to record against a mismatched commit SHA);
  Fourier and frequency-ablation figures committed under Step 1's contract.
- **Rung 1 `--standard`, relaunched under supervision** — a `--checkpoint-every` value
  that's actually been kill-drilled in Step 2, and an active check-in cadence instead
  of "detached and forgotten." Verdict: head confirmed + causally verified, or the
  K-composition "how far" figure.

### Step 4 — The cascade (conditional on a head)

Rung 4 end-to-end: activation patching, path patching, head ablation at the named
(layer, head) — the first time path patching runs against a real head instead of only
its unit tests. Rung 5 re-test via `--activations-from` on the head-bearing checkpoint;
compare L0/FVE against the dense 53%-L0 reading and report the delta honestly either
way.

### Step 5 — Clean-clone gate (Phase 6 completion)

`scripts/clean_clone_check.sh` run end to end for the first time, transcript captured,
`06_production_ai/proofs/reproducible-from-clean-clone.md` written from the actual
output — not from what the script is supposed to do.

### Step 6 — Paper prose

First real prose in `portfolio/paper/main.tex`: Methods, and Rung 3's results (the
strongest, most reproducible finding), in evidence order. Every paragraph ties back to
a manifest or a committed figure from Step 1 — no claim in the paper that isn't already
in `RESULTS.md`.

### Step 7 — Close the phase

One honesty-ledger entry, including the state-review misdiagnosis this phase opened
with — that gets recorded the same as a wrong hypothesis, not quietly dropped now that
it's corrected. `dev` merged into `main`. Roadmap archived in the progress log with
deviations from this plan noted explicitly.

## Deep-dive study and research topics

1. **Process supervision and job durability for unattended long-running compute.** Why
   "detached" is not "supervised": the difference between backgrounding a process and
   giving it a supervisor that notices when it dies. Read the minimal version of this
   pattern (a watchdog loop, `systemd`/Task Scheduler auto-restart, or a cron heartbeat
   appending to a log every N minutes) before reaching for anything heavier — this is
   now a recurring failure mode in this vault, not a one-off.
2. **Idempotent, resumable training-loop design**, beyond this repo's own rolling
   checkpoint. What state actually has to round-trip for a resume to be bit-identical
   (model, optimizer, LR scheduler, RNG state, epoch/step counter, dataloader position)
   — read how PyTorch's own recipes handle this and how a framework like PyTorch
   Lightning or Composer implements `Trainer.fit(ckpt_path=...)`, to sanity-check this
   repo's hand-rolled version against a design that's been through more edge cases.
3. **Colab session durability**, applying the same lesson to the GPU side — free-tier
   Colab sessions disconnect too; checkpoint-to-Drive patterns so a P=113 run isn't also
   one disconnect away from a second silent loss.
4. **Artifact provenance and figure↔manifest binding.** How research repos keep binary
   evidence honest without bloating history: `git-lfs`, DVC, or a small curated
   committed set are the three real options; understand the tradeoffs before picking
   Step 1's approach, and why "the script that regenerates it exists" is not the same
   claim as "the evidence is reviewable from a clone."
5. **Nanda & Jacobsen, "Attention as a Step Towards the Emergence of the Induction
   Head" (2023)** — re-read before interpreting whatever the relaunched `--standard`
   run produces; the K-composition detector built in MP11 is the operational form of
   this paper's argument.
6. **Zhang & Nanda, "Towards Best Practices of Activation Patching" (ICLR 2024)** —
   re-read immediately before Step 4, since this is the first time path patching runs
   against a real head and site/aggregation mistakes are exactly what this paper
   catalogs.
7. **Solo-repo git workflow hygiene.** Why a documentation fork — not lost work — went
   unnoticed for two roadmap passes, and more importantly, why the *first* diagnosis of
   it this session was also wrong. A genuine process question: what convention (pull
   before drafting a new roadmap doc? a single "current phase" pointer instead of an
   append-only list?) would have prevented both the fork and the misdiagnosis.

## Documentation requirements

- **Progress log**: one dated entry per session, including the kill drill's raw outcome
  (pass or fail) before any interpretation of it, and this phase's own opening
  state-review correction.
- **New note**: `06_production_ai/notes/checkpoint-resume-durability.md` — what state
  round-trips, what the kill drill actually tested, and the gap between "unit-tested"
  and "kill-drilled" made explicit as a durability note, not just a code comment.
- **Notes**: induction-heads note updated with the standard-scale verdict either way; a
  short git-hygiene retro note on the documentation fork and its misdiagnosis.
- **Skill tree**: flips only with proof, as before — `induction-head reproduction` on a
  confirmed head + causal verification; `grokking reproduction` on P=113 manifests;
  `reproducible-from-clean-clone` on a passed gate; a new **reproducible job durability**
  line item if the kill drill produces a real, checked pattern worth keeping visible.
- **RESULTS.md**: new manifests, ledger entry, figure citations reconciled against
  Step 1's curated set, reconciled with `make verify-claims`.
- **Paper**: Methods + Rung 3 written for the first time this phase, every paragraph
  tied to a manifest or committed figure — no exceptions.

## Practical exercises and hands-on challenges

1. **Exercise — score the 2026-08-02 pre-registration.**
   `08_micro-phase-09-the-flagship-runs.md` and
   `09_micro-phase-10-consolidation-and-paper.md` both contain dated predictions written
   before MP9–MP11 ran. Grade each prediction against what actually happened. Costs
   nothing but honesty, and is exactly the kind of self-check this phase's opening
   correction shows the value of.
2. **Exercise — merge archaeology (Step 0).** One sentence per commit on the 13 that
   landed via PRs #33–#36 before resolving anything; decide the `00_home.md` resolution
   deliberately, not by picking "ours" or "theirs" reflexively.
3. **Exercise — figure audit (Step 1).** For every figure path cited in `RESULTS.md`,
   answer three questions: does the file exist on disk right now? is it tracked in git?
   which manifest backs its numbers? Fix or delete each row that fails any of the three.
4. **Challenge — the kill drill (Step 2).** Launch `--standard`, hard-kill it mid-run,
   resume it, verify the manifest matches what an uninterrupted run would have
   produced. Do this *before* trusting it with the real multi-hour run.
5. **Challenge — Colab P=113 ×3 seeds (Step 3a).** Launch, monitor, download, verify
   checksums, pin, update RESULTS.md — the flagship, actually completed this time.
6. **Challenge — supervised standard-scale relaunch (Step 3b).** Not "fire and forget"
   — an active check-in cadence, using the kill-drilled checkpoint as a safety net
   rather than a substitute for attention.
7. **Exercise — path patching's first real head (Step 4, conditional).** If a head
   forms, this is the first time an implementation that has only ever been unit-tested
   runs against real data — treat the first result with appropriate suspicion and
   re-derive one number by hand if it looks too clean.
8. **Challenge — clean-clone gate (Step 5).** Fresh clone → sync → CI → reproduce →
   verify-claims, end to end, for the first time; the proof gets written from the
   actual transcript, not from what the script is supposed to do.
9. **Exercise — Methods section draft (Step 6).** First paper prose grounded entirely
   in already-committed manifests and figures — a good test of whether the evidence
   base is actually sufficient to write from, or whether it just looks that way.

## Strategic tips and architectural best practices

- **Verify the state against the repository, not against memory of the last session.**
  This phase's own first draft is the cautionary example: a detailed, plausible crisis
  narrative that one `git diff origin/dev` disproved in seconds. The fix was cheap
  because it was caught before commit — the lesson generalizes to every future roadmap
  pass.
- **Evidence a reviewer can't see from a clone isn't evidence, no matter how real the
  underlying run was.** A gitignored `figures/` directory is functionally the same
  failure as the 2026-07-26 audit's "figures/ doesn't exist at all" — just quieter,
  because the script that regenerates them still runs locally.
- **Never trust an unattended multi-hour run with a checkpoint path that hasn't been
  kill-drilled against a real process death.** A unit test that calls the training
  function twice in the same Python process proves the *logic*; it says nothing about
  disk flush timing, signal handling, or terminal-close behavior on the actual machine.
- **Pull before drafting a new roadmap document, not after.** The documentation fork
  this phase resolves exists because a new roadmap pass started locally before the
  previous pass's remote commits were pulled in — the same root cause as any merge
  conflict, just in prose instead of code.
- **Quick scale is a smoke test, never a result** — unchanged from MP11, still true.
- **One variable per experiment, one honesty-ledger entry per phase, regardless of
  outcome** — including entries about the roadmap process itself, not only the science.
- **A supervised run that finishes with a "no head" diagnosis is a stronger portfolio
  artifact than an unattended run that vanishes without a trace** — this phase's whole
  premise, unchanged by the correction above.
- **Falsification tests for every new instrument, including infrastructure.** The
  checkpoint/resume system got exactly this treatment in code; the kill drill extends
  the same standard from "tested in-process" to "tested against reality."

## Gate criteria — what green looks like

1. Documentation fork resolved, `00_home.md` links every roadmap document honestly,
   `dev` synced with `origin/dev` (zero behind), one clean commit records the
   correction.
2. Every figure cited by `RESULTS.md` exists on disk, is tracked in git, and is bound
   to a named manifest; the Rung-6 artifact is gone.
3. Kill drill passed: a hard-killed `--standard` process resumes to a manifest
   indistinguishable from an uninterrupted run.
4. P=113: ≥2 seeds grokked, manifests pinned, Fourier + ablation figures committed.
5. Rung 1 standard-scale verdict landed for real this time: confirmed head + causal
   verification, or a committed K-composition "how far" figure — not silence.
6. If a head formed: Rung 4 E2E and Rung 5 re-test manifests exist.
7. Clean-clone gate run end to end at least once, proof written from the transcript.
8. Paper: Methods + Rung 3 written, every paragraph tied to a manifest or figure.
9. Tests ≥185 passing (was 177 at phase start; already met by Step 1's figure-gate tests —
   restated so this stays a real gate, not one satisfied by adding nothing), local CI mirror
   green, GitHub CI green on `dev`, `dev → main` merged.

## Links

- [[00_meta/10_micro-phase-11-flagship-run]] — where the checkpoint/resume need was
  discovered and the K-composition detector was built.
- [[00_meta/08_micro-phase-09-flagship-sprint]] — the parent roadmap this phase still
  executes.
- [[00_meta/08_micro-phase-09-the-flagship-runs]] — the 2026-08-02 pre-registration,
  worth scoring against what actually happened.
- [[00_meta/09_micro-phase-10-consolidation-and-paper]] — the 2026-08-02 consolidation
  plan; still mostly open (Steps 5 and 6 here pick most of it back up).
- [[00_meta/03_progress-log]] — the journal this phase is recorded in.
- [[portfolio/RESULTS]] — the ledger this phase must change.
- [[04_nlp_and_transformers/notes/induction-heads]] — Rung 1's working note.
- [[06_production_ai/proofs/reproducible-from-clean-clone]] — the Phase 6 gate this
  phase attempts to close for the first time.

---

## Execution record (appended as results land)

### 2026-08-07 — Step 1: the evidence gate

Overrode the step's own "no new automation target yet; a documented copy step is
proportionate" call. A documented copy step is a fourth instance of the control that already
failed three times (2026-07-26, 2026-08-01, and this session's own discovery); the fix was
~25 lines inside `verify_claims()`, which already runs in `make verify-claims` and already
had a test file.

**RED, captured before any fix** (`python -m src.results verify` against the real
repository, unpatched):

```
verify-claims: 17 problem(s) found:
  - 11 figures cited that exist on disk but aren't tracked by git (figures/ is gitignored)
  - 4 figures cited that don't exist on disk at all:
      exp3_pentagon_geometry.png, exp4_head_ablation.png,
      exp5_sparsity_tradeoff_real.png, exp5_feature_histogram_real.png
  - 2 sections (Rung 2, Rung 5) cite figures/outputs with no manifest tag of their own
```

More than the plan's own ≥6 estimate. Two prerequisite bugs surfaced just from trying to run
the tool for real, neither visible from reading the code: `.gitignore`'s unanchored
`figures/` rule also matched the destination directory (`portfolio/figures/`) this step
exists to populate; `claims_file.read_text()` had no explicit encoding and crashed on
Windows against `RESULTS.md`'s non-ASCII characters. Both fixed.

**What changed**: `src/results.py::verify_claims` gained figure-existence + git-tracking and
per-section manifest-tag checks (`_git_tracked`, `FIGURE_CITATION_RE`); 8 new tests in
`tests/test_results.py`, including a falsification test reconstructing this exact state as a
permanent fixture (177 -> 185 tests collected — confirmed via `pytest --collect-only`, not
estimated). `.gitignore` anchored to `/figures/`. `portfolio/figures/` created and populated with the 11 pre-existing figures that
back a real claim, plus a freshly regenerated `exp3_pentagon_geometry.png`. `RESULTS.md`
repointed to `portfolio/figures/`; the three citations that can't be honestly backed yet
(`exp4_head_ablation.png`, both `_real` SAE figures) were struck with an explanation, not
left dangling or faked. `04_conventions.md`'s figures line rewritten to match what's
actually enforced.

**GREEN-minus-commit**: 17 -> 14 problems, and — after the pentagon-geometry figure landed
(see below) — **zero** "does not exist on disk" problems remain. The 14 that's left is
exactly the honest residue: all 12 "not tracked by git" (curated figures exist locally,
pending `git add`) plus the 2 untagged sections, which stay flagged **correctly** — no
`results/exp2_grokking.json` or `results/exp5_sae_dashboard.json` has ever been produced, so
there is genuinely nothing to tag yet. See
[[06_production_ai/exercises/ex-05-falsify-the-figure-gate]] for the full transcript,
[[06_production_ai/notes/figure-provenance-and-evidence-gates]] for the writeup.

**The pentagon-geometry regeneration died silently, twice, at full scale** — a small,
ironic, real instance of the exact failure class this whole phase exists to fix. Full-scale
`--geometry-check` (the Makefile's canonical `reproduce-exp3-geometry` invocation: 6
sparsity levels x 5000 epochs x 50,000 samples) was launched as a tracked background job
twice. Both times it ran for 50+ minutes, genuinely accumulating CPU time (confirmed via
`Get-Process`, not just assumed), then was terminated by something outside this session's
control — no crash trace, no partial output (Python fully buffers stdout when not a TTY, so
nothing was visible even while it ran), no error. The first death's own task notification
said as much: "may have been stopped via the UI, Monitor timeout, or agent teardown... these
leave no transcript marker." After the second death, rather than attempt a third
multi-hour unattended run, relaunched with `--quick` (2000 epochs, 10,000 samples —
~10x less compute), which completed cleanly in ~2.5 minutes:

```
0.0100 | 5/5 | 70.7 | 73.6 | 0.9 | True
CONFIRMED: learned directions are approximately equiangular (gaps 70.7-73.6°, std 0.9° vs ideal 72.0°)
```

Closely matches the previously-documented full-scale numbers (70.2-73.8°, std <=1.4° across
the sweep; 71.6-73.0°, std 0.5° at the tightest point) — the qualitative claim (pentagon
geometry emerges in the sparse regime) reproduces at reduced budget too. Named honestly as a
known simplification, not silently passed off as the canonical run: `portfolio/RESULTS.md`'s
Rung 3 section should eventually cite a full-scale regeneration once unattended long runs on
this machine are trusted again (a second entry in the same durability question Step 2 opened,
just for figure-generation jobs instead of training checkpoints).

Not committed in this session (commits happen only when explicitly requested) — the fully
green state (0 "untracked" problems) requires `git add portfolio/figures/ .gitignore
src/results.py tests/test_results.py 00_meta/04_conventions.md portfolio/RESULTS.md` and a
commit before a fresh clone would actually see any of it.

### 2026-08-07 — Step 2: the kill drill — PASSED

First real test of checkpoint/resume against an actual process death, not the in-process
8-epoch toy config `TestCheckpointResume` already covers. Full transcript in
[[06_production_ai/exercises/ex-04-kill-drill]]; the writeup in
[[06_production_ai/notes/checkpoint-resume-durability]]; the reconstructed-from-memory
proof in [[06_production_ai/proofs/kill-drill-checkpoint-resume]].

Standard-scale hyperparameters (`vocab_size=2048, seq_len=64, d_model=64, fresh-batches`),
seed 0, `--checkpoint-every 5`, scaled to 30 epochs (not the full ~17-20h 3000-epoch run —
de-risking the mechanism before committing that much wall-clock time to it). Launched via a
real OS process (`Start-Process -PassThru`), let 2 checkpoints land plus 12 more seconds so
the kill would hit mid-epoch, then `Stop-Process -Force` — an actual hard kill, not `Ctrl+C`.
Resumed with `--resume`, ran to completion, diffed every `history` array and every final
model tensor against an uninterrupted reference run of the same config and seed:

```
train_loss / val_loss / val_acc / attn_entropy / diag1_mass: max_abs_diff = 0.000e+00 (all, n=30)
max abs param diff across all tensors: 0.000e+00
=== VERDICT: BIT-IDENTICAL (pass) ===
```

Bit-identical, not approximately equal, on the first drill. The design choice that made this
a clean pass rather than a coin flip: `_make_fresh_batches_fn` derives each epoch's data from
`(seed, epoch)` directly, not from carried RNG state — a resumed run recomputes the same
deterministic function instead of needing to reconstruct an RNG stream's history. The only
state that genuinely needed to survive the kill was the model/optimizer/scheduler weights and
the shuffling RNG, both captured by `save_training_checkpoint` and restored intact.

**What this drill does not cover** (tracked as open, not glossed over): the full 3000-epoch
duration (disk pressure, reboots, thermal throttling over hours are untested); no other
process was contending for CPU/BLAS threads at the moment of the kill, so the
cross-process-nondeterminism hypothesis I actually expected to fail on never got exercised
under load. Checked "Reproducible job durability" in [[00_meta/02_skill-tree]] on the
strength of what was actually demonstrated, with those limitations stated in the proof itself
rather than folded into an unqualified "passed."

**Next**: Step 3 (P=113 on Colab GPU, Rung 1 `--standard` supervised) is now unblocked on the
mechanism side. Neither leg can run from inside this environment — P=113 needs a Colab
session, and `--standard` is ~17-20h of CPU time not suited to an unattended background
launch from this session. Launch commands prepared, execution left to a supervised session.
