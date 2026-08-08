---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-08
---

# Micro-Phase 18 — The Verdict Window (roadmap)

Written as a personal learning log and a public record, like every roadmap before it.
MP-17 declared itself the last planned roadmap of the execution arc — this phase honors
that promise by never re-planning anything. MP-17 defined *what* must happen (closure
decision, watchdog, clean-clone transcript, mypy de-drift, paper spine, verdict lanes,
release) and the Verdict Closure Ledger that makes waiting visible as a decision. What
MP-18 adds is the one thing those seven steps lack: a **calendar**. Four consecutive
roadmaps shipped their Step 0 and ended the session; the failure mode was never
instrumentation, it was *session shaping* — plans without clocks get planned again.
This phase's design principle is therefore **sessions with clocks, a ledger with no
silent rows**: every step is bound to a named session with a wall-clock budget and an
exit criterion, and the ledger gates the session, not the phase.

## Where this phase starts (state review, verified against the repo)

Checked `git status` / `git log` / the manifests before writing a single claim.

- **MP-17 Step 0 is shipped** (`121cb1b`, merged to `main` via PR #41; `dev == main`, tree
  clean): 185 tests passing, ruff clean, blocking mypy clean
  (`src/results.py`, `src/experiments/runner.py`), markdownlint clean, GitHub CI green,
  `make verify-claims` at its designed 2 problems (Rung 2, Rung 5 — no manifests have ever
  existed).
- **MP-17 Steps 1–7 are unexecuted.** No closure decision exists, the Verdict Closure
  Ledger has no rows, no watchdog driver, no clean-clone dry-run transcript, mypy still at
  171 full-tree errors (blocking allowlist still exactly two modules), the paper spine is
  still ~100% `% TODO` (`portfolio/paper/main.tex`).
- **The two flagships have now survived five consecutive unlaunched phases.** MP-13,
  MP-14, MP-15, MP-16, MP-17 each said "launch"; `checkpoints/` still contains only
  `kill_drill` artifacts; `results/` still holds exactly three manifests (exp1 tiny
  multi-seed, exp3, exp4 quick). Both runs remain fully instrumented and pinned: R1
  `--standard` (`vocab_size=2048, seq_len=64, d_model=64, 2L/4H, 3000 epochs`, fresh
  batches, ~17–20 h supervised CPU) and P=113 × 3 seeds via the hardened Colab notebook
  (`notebooks/colab_grokking_full_run.ipynb` + `scripts/pin_colab_run.py`).
- **The strongest verified result stands and needs no verdict**: Rung 3's superposition
  phase transition (10/20 → 20/20 features, pentagon geometry 70.2–73.8° gaps), backed by
  a committed manifest and 12 curated, tracked figures in `portfolio/figures/`.
- **The committed fallback is real**: the K-composition detector
  (`k_composition_scores` → `plot_composition_diagnostic` in
  `src/experiments/exp1_induction_heads.py`) means a headless R1 verdict still ends in a
  figure, not a hole.
- **Known residue, by design**: R4's path patching is validated only by unit tests; R5's
  real-activation numbers need a head-bearing checkpoint; the Phase 6 clean-clone gate
  proof has never gone green; the full-tree mypy ratchet stands at 171.

### Bottleneck diagnosis (ranked by what blocks what)

1. **Launch discipline is the critical path, and its unit is the session, not the
   step.** Everything the verdicts need exists; the missing resource is a supervised
   wall-clock window. MP-18 therefore opens with S1 — the closure session — and defines
   the phase's gate as *zero un-decided ledger rows when the session ends*, a promise
   this roadmap can enforce mechanically because the ledger file exists before the
   session starts (ADR-0001).
2. **The release is verdict-gated by design**: `verify-claims` will block `dev → main`
   until Rung 2 and Rung 5 manifests exist (or their claims are honestly struck). The
   ledger is how the phase's release passes the gate without faking a number: rows
   closed-not-verified re-scope the expected-claims set explicitly.
3. **The paper is still ~100% `% TODO`** — Related Work, Methods/Setup, Superposition and
   the refined Limitations are writable today from evidence that already exists. Four
   phases have said this; MP-18's writing sessions (S3, S4) are clocked, so the writing
   happens, not just the intention.
4. **mypy's 171 full-tree errors** — code-quality debt held at one remove by the
   non-blocking tier; paid down one module at a time in a clocked session (S5).
5. **The clean-clone gate has never run once** — it is a transcript away from being a
   formality (S2, S6).
6. **The meta-risk is now named and final-miles**: five unlaunched verdict phases is a
   pattern. The counter is no longer a better document — it is the ledger with rows
   signed under dates, and the release rehearsal (S6) that makes the real release a
   formality.

## 2. Deep-dive study and research topics

Inherited whole from MP-17 — MP-18 adds nothing to the reading list, it binds it to
sessions so the reading lands as deliverables:

| Topic | Session | Deliverable that proves the reading |
|---|---|---|
| Zhang & Nanda, "Towards Best Practices of Activation Patching" (ICLR 2024) | S3 | Per-site audit table mapped onto `exp4` code — becomes paper Methods material |
| Olsson et al. 2022, the K-composition curriculum | S4 | The interpolation commentary for the "how far" figure |
| Nanda et al. ICLR 2023 (re-read with weights in hand) | S4/S7 | Freq^k sparsity hand-verification protocol; named suspect list if P=113 fails |
| Power et al. 2022, the hyperparameter landscape | S3 | One-variable retry dials, pre-budgeted on paper |
| Predictability self-audit (MP-9/10/14 predictions vs outcomes) | S7 | A calibration table in the progress log |
| Process supervision (heartbeat, watchdog, `PYTHONUNBUFFERED`) | S2 | The watchdog driver script itself |
| Model-card craft (HF guide) | S6 | The rewritten `portfolio/model-card.md` |
| Pre-mortem decision discipline (Kahneman et al., HBR 2011) | S1 | Pre-registered "evidence that would change my belief + the date I stop waiting" per flagship |
| The reproducibility checklist (Pineau et al., JMLR 2021) | S3 | The claims audit applying it to three headline numbers |

*"I do not add topics this phase; I bind the ones I had to sessions so that every topic
ends in a file, not in another plan."*

## 3. Documentation requirements

- **Progress log**: one dated entry per session, raw pass/fail before interpretation —
  including S1's own decision and any misstep it makes.
- **The Verdict Closure Ledger (ADR-0001, created in this phase's Step 0)**: the living
  home of the closure table, filled during S1, signed with dates and reasons. Its gate:
  *no row may carry an undated status*; "awaiting window" without a date is a lie in the
  ledger's own terms.
- **New notes, each bound to a session**: the *figure supervision + watchdog* note
  (S2), the *Fourier progress measures* note (S7, contingent), the *mypy de-drift*
  short record (S5), the *Zhang–Nanda audit table* as a committed artifact (S3), the
  300-word honest negative (S4, contingent).
- **Paper spine**: Sections 2 (Related Work), 4 (Methods/Setup), 9 (Superposition) and
  the refined Limitations become prose in S4, evidence-ordered, every paragraph citing a
  file. Verdict-gated sections stay gated on S7's lanes.
- **Skill tree**: flips only with proofs and exercises; negative outcomes get their own
  lines.
- **RESULTS.md**: reconciled with each new manifest; the Rung 2/5 numbers come from
  manifests, or the claims are struck honestly with the strike recorded in the ledger.
- **Home**: this roadmap is wired as current in `00_meta/00_home.md`; when the release
  lands, the ledger remains the public record.

## 4. Practical exercises and hands-on challenges

1. **Challenge — the closure session (S1, the phase's Step 1)**: every row of the
   Verdict Closure Ledger gets `launched (date, window, heartbeat)` or `closed (one
   named reason)` — in one sitting. The session is not over while a row is undecided.
2. **Challenge — the R1 supervised launch (S1, same night)**: `--standard` on this
   machine under heartbeat + `PYTHONUNBUFFERED`, checkpoint every 500 epochs, a named
   plan for every 3 h of elapsed time; a written fallback if the machine cannot be held.
3. **Launch — the P=113 Colab lane (S1, decision)**: notebook run with `pin_colab_run.py`
   provenance, or a budgeted CPU alternative, or a written closure with one named reason
   — the lane has no silent state.
4. **Challenge — the R3 watchdog regeneration (S2)**: driver script with
   restart-on-abnormal-exit; deliberate abnormal exit mid-run; pentagon confirmed at
   full-scale budget; the silent-death class drilled.
5. **Challenge — the clean-clone dry run (S2)**: `scripts/clean_clone_check.sh` on a
   fresh temp clone; full transcript; every manual step is a gate.
6. **Exercise — the claims audit (S3)**: re-derive three headline numbers from
   manifest + code by hand (pentagon gaps 70.2-73.8°; fresh-batches 52.2%;
   real-activation 99.97% FVE).
7. **Exercise — the Zhang-Nanda audit table (S4)**: map the paper's checklist onto
   `exp4` line by line; every deviation a named justification or an issue.
8. **Challenge — the mypy de-drift (S5)**: 171 → ≤160; move ONE module
   (candidate: `exp3_superposition.py`) onto the blocking allowlist with its
   errors-at-move count recorded.
9. **Habit — the 60-second clock check (every session)**: at session open, re-verify
   the clock's three visible facts — the ledger's undated rows, the heartbeat of any
   running job, the CI status line — before any planning prose.
10. **Pre-registration — the "how far" estimate (S4)**: write the expected
    K-composition threshold and the figure that would count as evidence — before any
    verdict exists; scored in S7.
11. **Challenge — the release rehearsal (S6)**: the entire Step-7 sequence on a branch
    (verify-claims, clean-clone, `make paper`, README + model card refresh, PR) once,
    before the verdicts land.
12. **Exercise — the honest negative in 300 words (S4)**: the exact words a lane 6b/6d
    writeup needs, drafted in advance; a skill, not a loss-avoidance drill.

## 5. Strategic tips and architectural best practices

- **A closure decision beats a launch decision beats a deferral.** After five
  unlaunched phases the cost of waiting exceeds the cost of a named negative. If no
  Colab session exists, R1 `--standard` is still launchable tonight on this machine,
  supervised — and the P=113 lane gets its budgeted alternative or its written closure.
- **Attach clocks to sessions, not steps.** A step without a session is a plan; the
  record of this repository shows plans reproduce themselves. Every step here has a
  named session, a wall-clock budget, and an exit criterion.
- **The ledger gates the session, not the phase.** "Zero undated rows by the end of
  this sitting" is enforceable; "by the end of the phase" is what produced four
  unlaunched phases.
- **Parallel execution is the only execution**: while R1 runs, the watchdog build, the
  clean-clone transcript and the first paper sections proceed on the same machine; the
  session clock does not wait for compute it can't control.
- **Pre-commit the branches before the numbers**: lanes A/B/C differ only in
  interpretation — the K-composition fallback figure ships before its verdict, so
  "what happens if no head forms?" is a release scenario, not a contingency.
- **A named negative is a contribution**: "no induction head forms at scale X under
  fresh batches, causally verified" is paper-quality when declared as such with the
  "how far" figure; the same holds for grokking within the budget.
- **The release gate stays mechanical.** `verify-claims` is the last word; striking a
  claim that has no manifest is a decision, faking a manifest is a regression, and the
  ledger makes the distinction visible.
- **Never trust an unattended long job that hasn't survived a real death** — and never
  launch a 17–20 h job from a session that will end. A supervised window is part of the
  launch, not optional.
- **One variable per retry, one ledger per verdict.** If P=113 fails, dials change one
  at a time with a pre-set budget.
- **Documentation drift gets a session, not a lifetime.** The ledger rows are the new
  drift front: a row saying "awaiting window" two phases in a row is drift in its own
  ledger's terms.

## 6. Step-by-step execution roadmap

Sessions S1–S6 need nothing but this machine and a clock; S7 consumes the verdict
closure into whichever lane prevails and runs the release.

```
SESSION 0 — The pre-flight (this note, ~15–20 min)
  CI mirror green locally (≥185 tests, blocking mypy, ruff, markdownlint,
  `make verify-claims` at its expected 2); ledger created (ADR-0001); this
  roadmap wired into home; pushed on `dev`; GitHub CI green.
  Exit: a green floor, and nothing after it runs on a red floor.

SESSION 1 — THE CLOSURE DECISION (the phase's Step 1, ~30–45 min, one sitting):
  every row of the Verdict Closure Ledger is either `launched (date, window,
  heartbeat)` or `closed (one named reason)`. Trigger the R1 daemon the same
  night (supervised window decided in the same sitting: `PYTHONUNBUFFERED=1`,
  checkpoint-every 500, a named reschedule rule). Write the pre-outcome
  commitment paragraph (what evidence would change my belief, by which date).
  Exit: the ledger has ZERO undated rows when the session ends.

SESSION 2 — Durability and the watch (completes while R1 burns, ~2–3 h CPU):
  the watchdog driver around the full-scale R3 `--geometry-check` regeneration,
  with a deliberate abnormal-exit drill; the clean-clone dry run with a full
  transcript; the P=113 Colab launch or its closure row. Exit: watchdog provably
  survives a real death; transcript has zero manual steps; the P=113 row is
  signed.

SESSION 3 — The claims audit (standalone, ~40 min): re-derive three headlines by
  hand; Zhang–Nanda table begun; pre-set the P=113 retry dials.

SESSION 4 — The paper spine (split into two seated sessions of ~2 h each): write
  Related Work, Methods/Setup, Superposition and refined Limitations as prose,
  every paragraph citing a file, nothing dangling. Exit: four sections written in
  evidence order; the audit table committed.

SESSION 5 — The de-drift (sequenced, ~1 h + CI): mypy 171 → ≤160; move ONE module
  onto the blocking allowlist; record the errors-at-move count.

SESSION 6 — Pre-verdict gates and the rehearsal (half-day): `verify-claims` at
  its expected 2 maximum; everything tracked; the full release sequence rehearsed
  on a branch (verify-claims, clean-clone real run, `make paper`,
  README + model-card refresh, PR) — the rehearsal catches the surprises left in
  S2–S5.

   ┌──────────────────────────────┬──────────────────────────────┐
   ▼ (the ledger rows resolve — every lane lands an artifact)    ▼
SESSION 7 — The verdict lanes and the release (each lane's
artifact on a branch, the release at the end):
   6a (head):  exp1 manifest; exp4 E2E run on the real head; exp5 re-test on the
               head-bearing checkpoint; path-patching numbers → paper §§5–7;
               model card update; skill flips.
   6b (headless): the K-composition "how far" figure + writeup; R4 sensitivity
               bound as the honest negative; paper §§5–7 framed as a declared
               bound; the skill tree records the negative.
   6c (grokked): exp2 manifest; Fourier figures; hand-verified frequency product;
               if not grokked on sweep #1, dials change ONE at a time with the
               pre-set budget.
   6d (closed-not-verified): the struck paper section or the declared bound, and
               the ledger-visible row re-scoping verify-claims' expected set.
   Then, the release: paper draft v0.1; RESULTS.md reconciled; `verify-claims`
   at zero unexpected; the real clean-clone transcript; the model card and
   portfolio README refreshed; the home wired; PR dev → main on green CI; merge;
   cleanup; archive this roadmap with its deviations noted.
```

## 7. Gate criteria

1. Session 0: ≥185 local checks + every CI workflow green on `dev` — nothing below is
   attempted on a red floor.
2. Session 1: the ledger has **zero undecided rows**, each with a date and a named
   window or a one-reason closure, before the session ends.
3. Session 2: the watchdog survives a real abnormal exit and regenerates the canonical
   pentagon at full scale; the clean-clone transcript has zero manual steps.
4. Session 4: the four spine sections exist as prose with per-file citations.
5. Session 5: full-tree mypy ≤ 160 with one more module on the blocking allowlist.
6. Session 6: `verify-claims` within its expected set; the rehearsal runs the entire
   release sequence on a branch with its transcript.
7. Session 7: whichever lane or lanes fire, a verifiable artifact exists — the released
   paper, the reconciled RESULTS, the pressable CI, the public record.

## 8. Showcase note

This roadmap is the public record of the turn from planning to execution: five
roadmaps promised the same two launches; this one binds every launch and every
closure to a date and a name — and the ledger at ADR-0001 is the artifact a reviewer
can open to see that not one row is left in "awaiting" without a clock. Whatever the
verdicts say, they arrive to a release that was rehearsed — and the showcase reads:
*the phase closed the loop it opened*.

## Links

- [[16_micro-phase-17-closure-and-release]] — the roadmap this phase executes; its
  Steps 1–7 become Sessions 1–7 here, its lanes 6a–6d are consumed whole.
- [[15_micro-phase-16-the-execution]] — the executed-begin that this phase is the
  first to genuinely finish; its watchdog, paper and gate rows are this phase's inputs.
- [[13_micro-phase-14-the-verdicts]] — the verdict definition phase whose lanes this
  phase either lands or closes by decision.
- [[09_micro-phase-10-evidence-run]] — instrumentation and pinned configs that make
  every verdict; the GPU hours are spent once, correctly.
- [[portfolio/RESULTS]] — the ledger this phase's release reconciles onto the shelf.
- [[portfolio/README]] — the showcase surface refreshed in Session 7.
- [[06_production_ai/proofs/reproducible-from-clean-clone]] — the gate proof whose
  transcripts Sessions 2 and 6 produce.
- [[04_nlp_and_transformers/notes/induction-heads]] and
  [[04_nlp_and_transformers/notes/path-patching]] — the notes that absorb the verdicts
  and the Zhang–Nanda audit.
- [[docs/adr/0001-verdict-closure-ledger]] — the living note that stores the closure
  table this phase's Sessions 1 and 7 sign.