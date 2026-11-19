---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-08
---

# Micro-Phase 16 — The Execution (roadmap)

Written as a personal learning log and a public record, like every roadmap before it.
The previous two phases (MP-14, MP-15) are roadmaps — written before the verdicts,
pre-registered, Step 0 shipped. This phase is the one that must **execute** their steps.
Its design principle: **the verdicts are a dependency, not a gate.** Everything that does
not need the two flagship runs executes now, and the compute-gated items get a launch
decision, not another deferral.

## Where this phase starts (state review, verified against the repo)

Checked `git status` / `git log` / the manifests before writing a single claim.

- **MP-15 Step 0 is shipped** (`28ca961`, merged to `main` via PR #40; `dev == main`, tree
  clean): 185 tests passing, ruff clean, blocking mypy clean
  (`src/results.py`, `src/experiments/runner.py`), markdownlint clean, GitHub CI green,
  `make verify-claims` at its designed 2 problems (Rung 2, Rung 5 — no manifests have ever
  existed).
- **MP-15 Steps 1–7 are unexecuted.** No watchdog driver exists, no clean-clone dry-run
  transcript, no mypy de-drift, no paper spine prose, no verdict lanes consumed, no release.
- **MP-14 Steps 1–7 are unexecuted.** `checkpoints/` contains only `kill_drill` artifacts;
  `results/` contains exactly three manifests (exp1 tiny multi-seed, exp3, exp4 quick). No
  R1 `--standard` run, no P=113 run, no R3 full-scale geometry re-run, no R4/R5 cascade,
  no clean-clone transcript.
- **The strongest result stands and needs no verdict**: Rung 3's superposition phase
  transition (10/20 → 20/20 features, pentagon geometry 70.2–73.8° gaps), backed by a
  committed manifest and 12 curated, tracked figures in `portfolio/figures/`.
- **The committed fallback is real**: the K-composition detector
  (`k_composition_scores` → `plot_composition_diagnostic`,
  `src/experiments/exp1_induction_heads.py`) means a headless R1 verdict still ends in a
  figure, not a hole.
- **Full-tree mypy slipped: 154 → 171** tracked errors (lockfile rebuild to numpy 2.5.0 /
  torch 2.12.1+cpu). Non-blocking per CI policy, but a drift this phase pays down in
  bounded steps.
- **Documentation drift found while reviewing**: `06_production_ai/checklist.md` cites a
  `make paper` target that does not exist, still claims the curated figures are untracked
  (they have been committed since MP-13, PR #38), and describes the SAE/paper pass as
  pending; `portfolio/README.md` references `portfolio/mini-paper/` (the real scaffold is
  `portfolio/paper/`); RESULTS.md's phase-gate rows for 5/6/7 are stale relative to what
  MP-8–15 shipped. All are fixed in this phase, not waived.

### Bottleneck diagnosis (ranked by what blocks what)

1. **The two verdicts stay the critical path** — and both need compute that only I can
   launch (R1 `--standard`, ~17–20 h supervised CPU; P=113 × 3 seeds on a Colab GPU
   session). Every downstream deliverable (R4 end-to-end, R5 re-test, paper sections 5–7,
   skill flips) is gated on them. **This phase's decision**: launch both with a real
   schedule, or explicitly defer with one named reason — never silently.
2. **A negative R1 verdict is a real possibility** (0/8 heads at every scale ever run).
   The design response stays pre-registration: lane B converts “no head” into the committed
   K-composition “how far” deliverable.
3. **The release is verdict-gated by design**: `verify-claims` will block `dev → main`
   until Rung 2 and Rung 5 manifests exist. Correct behavior — and it means the showcase
   cannot fully close until the runs land. Every minute the Colab session is late is a
   minute this phase keeps accruing value in the paper spine and the clean-clone proof.
4. **The paper is 100% `% TODO`** — four sections (Related Work, Methods, Superposition,
   Limitations) are writable *today* from evidence that already exists. This is the single
   largest parallelizable artifact left.
5. **mypy's 171 full-tree errors**: code-quality debt held at one remove by the
   non-blocking tier; de-drifted one module to the blocking allowlist at a time.
6. **Small but real doc drift** — cheap to fix, expensive to leave: this is a portfolio
   repo; stale paths and dead target references are exactly what a reviewer notices.

## 2. Deep-dive study and research topics

1. **Zhang & Nanda, “Towards Best Practices of Activation Patching” (ICLR 2024)** —
   *before* the first real use of `run_path_patching_to_logits()`. This repository has
   committed that paper's site/metric errors twice on activation patching; path patching's
   first real run must not be the third. Deliverable: a per-site audit table mapped onto
   our `exp4` code — the table itself becomes paper Methods material.
2. **Olsson et al. 2022, the K-composition curriculum** — read with *our* numbers: which
   ingredient (d_model, seq_len, vocab, loss) most plausibly gates head formation at our
   scale, so that the “how far” figure can be interrogated rather than merely rendered.
3. **Nanda et al., ICLR 2023 — re-read with weights in hand** — the P=113 recipe the way
   it should be read: weight decay as the Fourier-dial, the embedding-normalization detail
   I deviated from (named suspect #1 if P=113 fails), and the `Freq^k` sparsity of the
   progress measure as the thing to hand-verify once the model exists.
4. **Power et al. 2022, the hyperparameter landscape** — weight decay is the grokking dial;
   LR and optimizer are supports. Keep the landscape visible when interpreting a possible
   P=113 negative, and keep the retry budget at one variable.
5. **Pineau et al., reproducibility checklist (JMLR 2021)** — evidence-ordered paper
   craft: Methods → strongest result → each manifest-backed rung; no sentence whose
   evidence is not already in `RESULTS.md`.
6. **The predictability self-audit** — score my own MP-9/MP-10/MP-14 predictions against
   what actually happens once the verdicts land. A calibration drill before interpreting
   either outcome keeps the narrative honest when the numbers arrive.
7. **Process supervision as a research skill** — heartbeat logs, watchdog restart
   semantics, `python -u` / `PYTHONUNBUFFERED`: the silent-death class that killed two
   real full-scale jobs is a buffering bug plus a supervision gap, both fixable with a
   small driver script.
8. **Model-card craft** (Hugging Face model-card guide) — what a genuinely useful model
   card for a research artifact looks like: honest scope, named failure modes, evidence
   tied to artifacts. The current card predates the multi-seed harness and must be
   rewritten once the verdicts land.

## 3. Documentation requirements

- **Progress log**: one dated entry per session, including raw pass/fail before
  interpretation. MP-16's own missteps go to the `RESULTS.md` ledger, not into silence.
- **New notes**: a *figure supervision + watchdog* note under `06_production_ai/notes/`
  once the driver is real (standing pattern, not a one-off); a **Fourier progress measures**
  note once P=113 lands; the mypy de-drift record as a short `conventions` footnote (what
  signed the blocking allowlist and why).
- **Updated notes**: `04_nlp_and_transformers/notes/induction-heads.md` gets whatever the
  verdict says — the lane always writes; `path-patching.md` gets its first real
  end-to-end numbers; the grokking note gets P=113 manifests or the honest negative.
- **Paper spine**: Sections 2 (Related Work), 4 (Methods/Setup), 9 (Superposition) and the
  refined Limitations become prose *first* — each paragraph cites a file in this repo,
  nothing dangling. Sections requiring verdicts (Grokking, Induction, Patching, SAE) are
  left gated on those lanes in Step 6.
- **Fixed drift, this phase**: add the missing **`make paper`** target (compile
  `portfolio/paper/main.tex` via `latexmk`/`pdflatex` with a graceful no-tool message);
  correct `portfolio/README.md`'s stale `portfolio/mini-paper/` path to
  `portfolio/paper/`; refresh `06_production_ai/checklist.md` figure-tracking status and
  the Phase-5/6/7 gate rows in `RESULTS.md` to what actually shipped.
- **Skill tree**: flips only with proofs and exercises, following the vault's law — a
  checked box without proof is a lie, including the negative outcomes, which get their
  own lines (an honest record writes “headless at this scale” as a result, not a gap).
- **RESULTS.md**: reconciled with each new manifest; the ledger entry for this phase
  includes its own missteps; the Rung 2/5 numbers come from manifests, not prose.

## 4. Practical exercises and hands-on challenges

1. **Challenge — the R3 watchdog regeneration**: driver script (heartbeat +
   restart-on-abnormal-exit, `python -u`) around the full-scale `--geometry-check`
   regeneration; pentagon confirmed at the canonical budget; the silent-death class
   drilled with a deliberate abnormal exit mid-run.
2. **Challenge — the clean-clone dry run**: `scripts/clean_clone_check.sh` on a fresh
   temp clone, full transcript produced now; every manual step encountered is a failed
   gate — fix it now so the post-verdict real run is a formality, not an exercise.
3. **Exercise — the claims audit**: take three headline numbers from `RESULTS.md`
   (pentagon gaps 70.2–73.8°; fresh-batches 52.2%; real-activation 99.97% FVE) and
   re-derive each from its manifest + code by hand. The calibration drill for “what would
   my own gate catch”.
4. **Exercise — the Zhang–Nanda audit table**: map the paper's patch-site / metrics
   checklist onto our `exp4` implementation line by line; any deviation gets a named
   justification or an issue. The deliverable is the table, not agreement.
5. **Challenge — the mypy de-drift**: pay down 171 → ≤160 full-tree errors and move ONE
   module (candidate: `src/experiments/exp3_superposition.py` — the strongest result's own
   module) onto the blocking allowlist, with its errors-at-move count recorded.
6. **Exercise — one Fourier product, verified by hand** (contingent on P=113 grokking):
   take the top-frequency component, write the trig expression it implies for
   `logits[(a+b)]` from the embeddings by hand, verify against the trained weights — a
   proof at the weight level, not the plot level.
7. **Habit — figure provenance at commit time**: ask the three gate questions one commit
   earlier — figure on disk? tracked in git? bound to a manifest? That habit cost the
   ledger more than any single fault class in earlier phases.
8. **Habit — prose-source discipline**: every sentence written in Step 5 carries a
   `(file:line)` source note in the markdown draft; nothing survives into the TeX that
   didn't originate from an artifact.
9. **Pre-registration exercise — the “how far” estimate**: from the model hyperparameters,
   write down the K-composition threshold expected and the figure I'd accept as evidence —
   before any verdict exists. Post-verdict, score it (topic 6 above).
10. **Challenge — the launch decision**: R1 `--standard` and the P=113 Colab session get a
    scheduled launch window with a heartbeat, or an explicit recorded deferral with one
    named reason each. Silence is failure, and this phase ends the two-phase silence.

## 5. Strategic tips and architectural best practices

- **Parallelize the critical path, and the non-critical path**: the verdicts own the
  critical path; the paper spine, the watchdog, the clean-clone transcript, and the mypy
  de-drift are the parallelizable artifacts that keep this phase producing while compute
  cooks.
- **A launch decision beats a deferral**: two roadmaps in a row have pre-registered and
  nobody has launched. This phase either launches or records the deferral as a decision
  with a date and a reason — the ledger accepts honesty, not silence.
- **Pre-commit the branches before the numbers**: lane A vs lane B differs only in
  interpretation, never in whether a deliverable exists — the fallback figure is
  implemented before its verdict.
- **A named negative is a contribution**: “no induction head forms at scale X under fresh
  batches, causally verified” is paper-quality when declared as such and accompanied by
  the “how far” K-composition figure.
- **The release gate stays mechanical**: `verify-claims` is the last word — a merge that
  carries a dangling number is not a release, it's a regression.
- **Never trust an unattended long job that hasn't survived a real death**: the watchdog
  gets drilled against an abnormal exit on this machine, before any real run leans on it.
- **The paper is the last artifact, not the first**: prose is written from manifests; the
  scaffold I keep turning real is exactly that order.
- **One variable per retry, one ledger per verdict**: if P=113 fails, the retry dials
  (weight decay; embedding normalization; LR scheduling) are changed *one at a time*, with
  a pre-set budget, and every failure lands in the ledger.
- **Doc drift gets a session, not a lifetime**: stale paths in a portfolio repo are a
  credibility cost; fixing them is minutes when spotted, embarrassing when found later.

## 6. Step-by-step execution roadmap

Steps 0–5 need nothing but this machine. Step 6 consumes MP-14's verdicts through the
three lanes, each pre-registered with its own deliverable. Step 7 is the release.

```
Step 0: Pre-flight (this note, ~15 min) — CI mirror green locally (≥185 tests, blocking
        mypy, ruff, markdownlint), ledger + home wired, pushed on dev, GitHub CI green.
        Fix the documentation drift in the same pass (make paper, README paths, phase
        gate rows).
Step 1: The launch decision — schedule R1 --standard (supervised, heartbeat) and the
        P=113 Colab session, or record one named deferral each with a next-attempt
        date. Both flagships get a real date on the calendar by the end of this phase.
Step 2: R3 watchdog regeneration (infra that survives a real death, ~2-3 h CPU),
        deliberate abnormal-exit drill; clean-clone dry run with transcript
Step 3: mypy de-drift 171 -> <=160, move ONE module onto the blocking allowlist
        (candidate: exp3_superposition.py)
Step 4: Paper spine — Related Work, Methods, Superposition, refined Limitations
        as prose, every paragraph citing a file; the claims audit (Exercises 3-4)
Step 5: Pre-verdict gates — verify-claims <= 2 expected; every artifact tracked;
        ledger entry written (including this phase's own missteps)
        ┌──────────────────────────────┬──────────────────────────────┐
        ▼ (verdicts land, in-flight MP14)                           ▼
Step 6a (head): R1 --standard manifest, R4 E2E run on the real head,
        R5 re-test on the head-bearing checkpoint, path-patching numbers
        -> paper sections 5-7, MODEL-CARD update, skill flips
Step 6b (headless): K-composition "how far" figure + writeup, R4 sensitivity
        bound published as the honest negative, paper sections 5-7 framed
        as a declared bound, skill tree records the negative
Step 6c (grokked): exp2 manifest, Fourier figures, hand-verified frequency
        product (Exercise 6), Fourier note; if not grokked on sweep #1:
        1-variable retry dials (weight decay / embedding normalization)
        with the pre-set budget
Step 7: Showcase & release — paper full draft v0.1, RESULTS.md reconciled
        with every manifest, verify-claims zero unexpected, clean-clone real
        transcript, model card and portfolio README refreshed, home wired,
        ledger final entry; PR dev->main on green CI; merge; cleanup;
        archive this roadmap with its deviations noted

## 7. Gate criteria

1. Step 0 green: ≥185 tests, ruff clean, blocking mypy clean, markdownlint clean, GitHub
   CI green on `dev` — nothing below is attempted on a red floor.
2. Step 1: both flagships scheduled with dates, or each deferral recorded with a named
   reason and a next-attempt date. No silent waiting.
3. Step 2: watchdog survives a *real* abnormal exit and regenerates the canonical
   pentagon figure at the full-scale budget — recorded in the durability proof; the
   clean-clone dry-run transcript with zero required manual steps.
4. Step 3: full-tree mypy ≤ 160 and one more module on the blocking allowlist with its
   count recorded at move time.
5. Step 4: four paper sections written in evidence order; every paragraph carries a file
   citation; the audit table committed.
6. Step 5: pre-verdict gates — `verify-claims` at its expected 2 issue maximum, every
   artifact tracked, ledger entry written.
7. Verdict lanes: whichever verdict lands, a public artifact exists within the phase —
   head → path results; headless → “how far” figure; grokked → exp2 manifest + Fourier
   write-up; not-grokked → named suspects + budgeted retry protocol.
8. Step 7 release: `verify-claims` at zero unexpected issues, real clean-clone
   transcript, `RESULTS.md` reconciled, model card genuinely refreshed, CI green on the
   PR, merge, tree clean, roadmap archived with its deviations.

## Links

- [[14_micro-phase-15-from-verdicts-to-showcase]] — the synthesis roadmap this phase
  executes; its Steps 1–7 become this phase's Steps 2–5, and its pre-registered lanes
  (6a/6b/6c) are this phase's verdict consumers.
- [[13_micro-phase-14-the-verdicts]] — the launch phase whose verdicts this phase
  consumes through the three lanes; its Steps 1–7 are this phase's inputs.
- [[09-micro-phase-10-evidence-run]] — the run instruments and pinned configs this
  phase's Step 4 paper spine builds on.
- [[portfolio/RESULTS]] — the ledger this phase must change; the source of every paper
  number.
- [[portfolio/README]] — the showcase surface this phase's release pass refreshes.
- [[06_production_ai/proofs/reproducible-from-clean-clone]] — the Phase 6 gate proof
  whose real transcript Steps 2 and 7 produce.
- [[04_nlp_and_transformers/notes/induction-heads]] and
  [[04_nlp_and_transformers/notes/path-patching]] — the working notes that absorb this
  phase's verdicts and the Zhang–Nanda audit.

## 8. Showcase note

This roadmap is my public record of judgment under uncertainty. Whatever MP-14's verdicts
say, the phase closes with a demonstrable artifact — a figure, a curve, a section of
prose — and an honest ledger entry. That is the portfolio's contract, and it is why the
roadmap is written *before* the runs, not after them.