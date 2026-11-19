---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-08
---

# Micro-Phase 17 — The Closure (roadmap)

Written as a personal learning log and a public record, like every roadmap before it.
MP-16 promised to execute; MP-16 shipped only its Step 0. MP-14, MP-15, and MP-16 all
pre-registered the same two flagship verdicts, and after four consecutive phases nobody
has launched them. This phase's design principle is therefore **closure over
continuation**: every open item either lands under a date, or is closed with one named
reason — including the decision to declare an item closed-not-verified. There is no
third pre-registration. This is the last planned roadmap of the execution arc; anything
still open when it ends is closed by decision, not by another document.

## Where this phase starts (state review, verified against the repo)

Checked `git status` / `git log` / the manifests before writing a single claim.

- **MP-16 Step 0 is shipped** (`fd433a1`, merged to `main` via PR #41; `dev == main`,
  tree clean): 185 tests passing, ruff clean, blocking mypy clean
  (`src/results.py`, `src/experiments/runner.py`), markdownlint clean, GitHub CI green,
  `make verify-claims` at its designed 2 problems (Rung 2, Rung 5 — no manifests have
  ever existed). The doc drift MP-16's state review found (missing `make paper`, stale
  `portfolio/mini-paper/` path, stale Phase-5/6/7 gate rows) is fixed.
- **MP-16 Steps 1–7 are unexecuted.** No launch decision recorded, no watchdog driver,
  no clean-clone dry-run transcript, mypy still at 171 full-tree errors (the blocking
  allowlist is still exactly two modules), the paper spine is still ~100% `% TODO`
  (`portfolio/paper/main.tex` — only the abstract and a bullet-list Limitations exist).
- **The two flagships have survived four consecutive unlaunched phases.** MP-13, 14, 15,
  and 16 each said "launch"; `checkpoints/` still contains only `kill_drill` artifacts;
  `results/` still contains exactly three manifests (exp1 tiny multi-seed, exp3, exp4
  quick). Both runs are fully instrumented and pinned: R1 `--standard`
  (`vocab_size=2048, seq_len=64, d_model=64, 2L/4H, 3000 epochs`, fresh batches,
  ~17–20 h supervised CPU) and P=113 ×3 seeds via the hardened Colab notebook
  (`notebooks/colab_grokking_full_run.ipynb` + `scripts/pin_colab_run.py`).
- **The strongest verified result stands and needs no verdict**: Rung 3's superposition
  phase transition (10/20 → 20/20 features, pentagon geometry 70.2–73.8° gaps), backed
  by a committed manifest and 12 curated, tracked figures in `portfolio/figures/`.
- **The committed fallback is real**: the K-composition detector
  (`k_composition_scores` → `plot_composition_diagnostic` in
  `src/experiments/exp1_induction_heads.py`) means a headless R1 verdict still ends in a
  figure, not a hole.
- **Known residue, by design**: R4's path patching is still validated only by its unit
  tests (no real head to target); R5's real-activation numbers need a
  checkpoint with a confirmed head to mean anything conclusive; the Phase 6
  clean-clone gate proof has never gone green; the full-tree mypy ratchet stands at 171
  (drifted from 154 after the numpy 2.5.0 / torch 2.12.1+cpu lockfile rebuild).

### The uncomfortable truth this phase is built around

The bottleneck stopped being instrumentation several phases ago. MP-10 and MP-11
finished the CPU-side de-risking; everything the two verdicts need exists — pinned
configs, checkpoints, resumes they survive, provenance that refuses a mismatched
SHA-1, a notebook that clones, applies the fix, runs, and downloads. What has been
missing for four phases is a launch. This phase makes that the explicit Step 1, with
the discipline that an item with no date is an item that has been *decided*, by
inaction, to be abandoned — and this ledger refuses silent decisions.

### Bottleneck diagnosis (ranked by what blocks what)

1. **The two verdicts stay the critical path** — R1 `--standard`'s domino
   controls R4's E2E page, R5's real-activation re-test, paper, model card, and the
   release itself. But note the inversion this phase exploits: with lane 6d
   (closed-not-verified) defined, *nothing* any single verdict can do — including
   never running — is allowed to block the showcase anymore.
2. **The release gate is verdict-gated by design**: `verify-claims` will block
   `dev → main` until Rung 2 and Rung 5 manifests exist (or their claims are
   honestly struck). The gate is the correct behavior; the closure ledger is how the
   phase's eventual merge passes it without faking a number.
3. **The paper is still ~100% `% TODO`** — Related Work, Methods/Setup, Superposition,
   and the refined Limitations are writable today from evidence that already exists.
   This is the single largest parallelizable artifact left, and the phase must not
   defer on it while compute waits.
4. **mypy's 171 full-tree errors** — code-quality debt held at one remove by the
   non-blocking tier; de-drifted one module to the blocking allowlist at a time.
5. **The clean-clone gate has never run once** — Phase 6's gate proof
   (`06_production_ai/proofs/reproducible-from-clean-clone`) is not green because
   the run was never made; it is a dry run away from being a formality.
6. **Roadmap inflation is now the meta-risk**: four "launch" roadmaps with zero
   launches is a pattern, not a delay. The ledger in this note is the counter —
   the artifact a reviewer can read to see that waiting was a *decision*, not drift.

## 2. Deep-dive study and research topics

1. **Zhang & Nanda, "Towards Best Practices of Activation Patching" (ICLR 2024)** —
   *before* the first real use of `run_path_patching_to_logits()`. This repository has
   committed that paper's patch-site and metric errors twice on activation patching;
   the first real run of path patching must demonstrate it is not a third.
   Deliverable: a per-site audit table mapped onto our `exp4` code — the table itself
   becomes paper Methods material.
2. **Olsson et al. 2022, the K-composition curriculum** — read with *our* numbers:
   which ingredient (d_model, seq_len, vocab, loss) most plausibly gates head
   formation at our scale, so that the "how far" figure can be interrogated rather
   than merely rendered.
3. **Nanda et al., ICLR 2023 — re-read with weights in hand** — the P=113 recipe the
   way it should be read: weight decay as the Fourier-dial, the embedding-normalization
   detail I deviated from (named suspect #1 if P=113 fails), and the `Freq^k`
   sparsity of the progress measure as the thing to hand-verify once the model
   exists.
4. **Power et al. 2022, the hyperparameter landscape** — weight decay is the grokking
   dial; LR and optimizer are supports. Keep the landscape visible when interpreting a
   possible P=113 negative, and keep the retry budget at one variable.
5. **Pineau et al., reproducibility checklist (JMLR 2021)** — evidence-ordered paper
   craft: Methods → strongest result → each manifest-backed rung; no sentence whose
   evidence is not already in `RESULTS.md`.
6. **The predictability self-audit** — score my MP-9/MP-10/MP-14 predictions against
   what actually happens once the verdicts land (or don't). A calibration drill before
   interpreting either outcome keeps the narrative honest when the numbers arrive.
7. **Process supervision as a research skill** — heartbeat logs, watchdog restart
   semantics, `python -u` / `PYTHONUNBUFFERED`: the silent-death class that killed
   full-scale jobs twice is a buffering bug plus a supervision gap, both fixable with
   a small driver script.
8. **Model-card craft** (Hugging Face model-card guide) — what a genuinely useful
   model card for a research artifact looks like: honest scope, named failure modes,
   evidence tied to artifacts. The current card predates the multi-seed harness and
   must be rewritten once the verdicts land — or once the closure lanes decide they
   never will.
9. **NEW — Decision discipline under uncertainty**: the pre-mortem (Kahneman et al.,
   "Before You Make That Big Decision...", HBR 2011) applied to both flagships —
   for each, write the specific evidence that would change my belief and the specific
   date I no longer wait for it. This is the academic framing for the ledger rows in
   Steps 1 and 6.

## 3. Documentation requirements

- **Progress log**: one dated entry per session, raw pass/fail before interpretation.
  MP-17's own missteps go to the `RESULTS.md` ledger, not into silence.
- **NEW — the Verdict Closure Ledger** (created in this roadmap, maintained in
  Step 1): a single table holding every open item from MP-14/15/16 and each item's
  status — `launched (date, window, heartbeat)` or `closed (date, one named reason)`.
  Step 1's gate is `since this table has zero un-decided rows by the end of that
  session`, not "by the end of the phase". The ledger makes the promise
  mechanical: a reviewer can open one note and see what is real, what is waiting,
  and what I decided.
- **New notes**: a *figure supervision + watchdog* note under
  `06_production_ai/notes/` once the driver is real (standing pattern, not a
  one-off); a **Fourier progress measures** note if P=113 lands; the mypy de-drift
  record as a short `conventions` footnote (what signed the blocking allowlist and
  why). The **Verdict Closure Ledger** note (`docs/adr/verdict-closure-ledger.md`)
  becomes the living home of Step 1's table once it outgrows the roadmap.
- **Updated notes**: `04_nlp_and_transformers/notes/induction-heads.md` gets
  whatever the verdict says — the lane always writes; `path-patching.md` gets its
  first real end-to-end numbers; the grokking note gets the P=113 manifest or the
  honest negative.
- **Paper spine**: Sections 2 (Related Work), 4 (Methods/Setup), 9 (Superposition)
  and the refined Limitations become prose *first* — each paragraph cites a file in
  this repo, nothing dangling. The verdict-gated sections (Grokking, Induction,
  Patching, SAE) stay gated on their lanes in Step 6.
- **Fixed drift, this phase**: nothing known remains from MP-16's audit. The new
  drift class is the ledger rows themselves — a row that says "awaiting window" two
  phases in a row is drift in the ledger's own terms and gets flagged as such.
- **Skill tree**: flips only with proofs and exercises, following the vault's law —
  a checked box without proof is a lie, including the negative outcomes, which get
  their own lines (an honest record writes "headless at this scale" as a result,
  not a gap).
- **RESULTS.md**: reconciled with each new manifest; the ledger entry for this phase
  includes its own departures; the Rung 2/5 numbers come from manifests, or the
  sections are struck honestly with the strike recorded in the ledger.

## 4. Practical exercises and hands-on challenges

1. **Challenge — the R3 watchdog regeneration**: driver script (heartbeat +
   restart-on-abnormal-exit, `python -u`) around the full-scale `--geometry-check`
   regeneration; pentagon confirmed at the canonical budget; the silent-death class
   drilled with a deliberate abnormal exit mid-run.
2. **Challenge — the clean-clone dry run**: `scripts/clean_clone_check.sh` on a
   fresh temp clone, full transcript produced now; every manual step encountered is a
   failed gate — fix it now so the post-verdict real run is a formality, not an
   exercise.
3. **Exercise — the claims audit**: take three headline numbers from `RESULTS.md`
   (pentagon gaps 70.2–73.8°; fresh-batches 52.2%; real-activation 99.97% FVE) and
   re-derive each from its manifest + code by hand. The calibration drill for "what
   would my own gate catch".
4. **Exercise — the Zhang–Nanda audit table**: map the paper's patch-site / metrics
   checklist onto our `exp4` implementation line by line; any deviation gets a named
   justification or an issue. The deliverable is the table, not agreement.
5. **Challenge — the mypy de-drift**: pay down 171 → ≤160 full-tree errors and move
   ONE module (candidate: `src/experiments/exp3_superposition.py` — the strongest
   result's own module) onto the blocking allowlist, with its errors-at-move count
   recorded.
6. **Exercise — one Fourier product, verified by hand** (contingent
   P=113 groks): take the top-frequency component, write the trig expression it
   implies for `logits[(a+b)]` from the embeddings by hand, verify against the trained
   weights — a proof at the weight level, not the plot level.
7. **Habit — figure provenance at commit time**: ask the three gate questions one
   commit earlier — figure on disk? tracked in git? bound to a manifest? That habit
   cost the ledger more than any single fault class in earlier phases.
8. **Habit — prose-source discipline**: every sentence written in Step 5 carries a
   `(file:line)` source note in the markdown draft; nothing survives into the TeX
   that didn't originate from an artifact.
9. **Pre-registration exercise — the "how far" estimate**: from the model
   hyperparameters, write down the K-composition threshold expected and the figure
   I'd accept as evidence — before any verdict exists. Post-verdict, score it
   (topic 6 above).
10. **NEW — Challenge — the closure drill**: for every row of the Verdict Closure
    Ledger, produce either a launch with a date and a heartbeat, or a closure with
    one named reason — *in one sitting*. The drill ends with zero un-decided rows.
    This is the exercise the phase confesses four roadmaps never finished.
11. **NEW — Challenge — the release rehearsal**: the entire Step 7 sequence on a
    branch (verify-claims, clean-clone, `make paper`, README + model card refresh,
    PR) executed once *before* the verdict lanes land, so the real release is a
    formality with no surprises and no untested grep.
12. **NEW — Exercise — write the honest negative, in 300 words**: draft the
    "headless at this scale, causally verified" or "grokking not reproduced within
    this budget" text as a contribution — the exact words a lane 6b/6d writeup needs.
    This is not a loss-avoidance drill; it is the skill that makes either verdict
    release-ready.

## 5. Strategic tips and architectural best practices

- **A closure decision beats a launch decision beats a deferral.** After four
  pre-registration phases, the cost of waiting exceeds the cost of a named
  negative. If no Colab session exists, R1 `--standard` is still launchable
   tonight on this machine, supervised — and the P=113 lane gets a budgeted
  alternative (extended CPU drills at P=59/P=113 with recorded budgets) or a
  written closure.
- **Parallelize the critical path, and the non-critical path**: the verdicts own the
  critical path; the paper spine, the watchdog, the clean-clone transcript, and the
  mypy de-drift are the parallelizable artifacts that keep this phase producing
  while compute waits — or never arrives.
- **Pre-commit the branches before the numbers**: lane A vs lane B differs only in
  interpretation, never in whether a deliverable exists — the fallback figure is
  implemented before its verdict.
- **A named negative is a contribution**: "no induction head forms at scale X under
  fresh batches, causally verified" is paper-quality when declared as such and
  accompanied by the "how far" K-composition figure. The same is true for "grokking
  not reproduced within the budget".
- **The release gate stays mechanical**: `verify-claims` is the last word — a merge
  that carries a dangling number is not a release, it is a regression. But honest
  scoping is how the gate turns green: striking a claim that has no manifest is the
  discipline, not faking a manifest.
- **Never trust an unattended long job that hasn't survived a real death**: the
  watchdog gets drilled against an abnormal exit on this machine, before any real
  run leans on it. Equally: never launch a 17–20 h job from a session that will
  end — a supervised window is part of the launch, not optional.
- **The paper is the last artifact, not the first**: prose is written from
  manifests; the scaffold I keep turning real is exactly that order.
- **One variable per retry, one ledger per verdict**: if P=113 fails, the retry dials
  (weight decay; embedding normalization; LR scheduling) are changed *one at a
  time*, with a pre-set budget, and every failure lands in the ledger.
- **Roadmap inflation is the anti-pattern**: three consecutive "launch" roadmaps was
  the warning sign this phase exists to stop. After this phase, open items are
  closed by decision, not by document.
- **Documentation drift gets a session, not a lifetime**: stale paths in a portfolio
  repo are a credibility cost; the ledger rows are the new front where this
  discipline must apply.

## 6. Step-by-step execution roadmap

Steps 0–5 need nothing but this machine. Step 6 consumes the verdict closure
into whichever lane prevails; Step 7 is the release and the last word of the
execution arc.

```
Step 0: Pre-flight (this note, ~15 min) — CI mirror green locally (≥185 tests,
        blocking mypy, ruff, markdownlint), ledger + home wired, pushed on dev,
        GitHub CI green. Found drift gets fixed in the same pass.
Step 1: THE CLOSURE DECISION (the phase's Step 1, one sitting) — every row of the
        Verdict Closure Ledger gets launched (date + window + heartbeat) or closed
        (one named reason). R1 --standard is launchable the same night on this
        machine. Zero un-decided rows when the session ends — the ledger has no
        "awaiting" state without a date and a named owner.
Step 2: R3 watchdog regeneration (infra that survives a real death, ~2-3 h CPU),
        deliberate abnormal-exit drill; clean-clone dry run with transcript;
        the claims audit (Exercise 3) lands in the same session.
Step 3: mypy de-drift 171 -> ≤160, move ONE module onto the blocking allowlist
        (candidate: exp3_superposition.py) with the count recorded at move time.
Step 4: Paper spine — Related Work, Methods, Superposition, refined Limitations
        as prose, every paragraph citing a file; the claims audit + Zhang-Nanda
        table. Nothing here waits on the verdicts: the write is fully
        parallelizable off the decision path.
Step 5: Pre-verdict gates — verify-claims at its expected 2 problems; every
        artifact tracked; the ledger entry written including its departures.
        ┌──────────────────────────────┬──────────────────────────────┐
        ▼ (verdicts land, or are closed — lane 6d fires)             ▼
Step 6a (head):   R1 --standard manifest, R4 E2E run on the real head, R5
                  re-test on the head-bearing checkpoint, path-patching
                  numbers -> paper sections 5-7, MODEL-CARD update,
                  skill flips.
Step 6b (headless): K-composition "how far" figure + writeup, R4 sensitivity
                  bound published as the honest negative, paper sections 5-7
                  framed as a declared bound, skill tree records the
                  negative.
Step 6c (grokked): exp2 manifest, Fourier figures, hand-verified frequency
                  product (Exercise 3), Fourier note; if not grokked on
                  sweep #1: one-variable retry dials (weight decay /
                  embedding normalization) with the pre-set budget.
Step 6d (closed-not-verified): if a verdict lane is closed, its paper
                  section is struck or reframed as an explicitly declared
                  bound, the model card names the gap with the date, and the
                  abstract carries the honest scope line. The release
                  proceeds with the record, not in spite of it, and the
                  closure ledger re-scopes verify-claims' expected set to
                  exactly the documented residue: the struck sections'
                  manifests absent by decision, visible in the ledger.
Step 7: Showcase & release — paper full draft v0.1, RESULTS.md reconciled
        with every manifest, verify-claims at zero unexpected problems (the
        expected set re-scoped explicitly by the closure ledger), clean-clone
        real transcript, model card and portfolio README refreshed, home
        wired, ledger final entry, PR dev→main on green CI; merge; cleanup;
        archive this roadmap's own file, with its deviations noted — the
        ledger remains the public record.
```

## 7. Gate criteria

1. Step 0 green: ≥185 tests, ruff clean, blocking mypy clean, markdownlint clean,
   GitHub CI green on `dev` — nothing below is attempted on a red floor.
2. Step 1: the Verdict Closure Ledger has zero un-decided rows — every item is
   launched with a date and a heartbeat, or closed with one named reason. No
   "awaiting" row survives the session.
3. Step 2: watchdog survives a *real* abnormal exit and regenerates the canonical
   pentagon at the full-scale budget — recorded at durability; clean-clone
   dry-run transcript with zero required manual steps.
4. Step 3: full-tree mypy ≤ 160 and one more module on the blocking allowlist
   (candidate: exp3_superposition.py) with its count recorded at move time.
5. Step 4: four paper sections written in evidence order; every paragraph carries
   a file citation; the audit table committed.
6. Step 5: `verify-claims` at its expected 2 maximum; every artifact tracked; the
   ledger entry written — including this phase's own departures.
7. Verdict lanes: whichever lane fires, a verifiable artifact exists within the
   phase — head → the path results; headless → "how far" figure; grokked → the
   manifest + Fourier write-up; not-grokked → named suspects + budgeted retry
   protocol; closed-not-verified → the ledger row itself is the artifact,
   with the declared bound printed alongside the struck claim.
8. Step 7 release: `verify-claims` at zero unexpected issues, real clean-clone
   transcript, `RESULTS.md` reconciled, model card genuinely refreshed, CI green
   on the PR, merge, tree clean, roadmap archived with its departures noted.

## Links

- [[15_micro-phase-16-the-execution]] — the phase this one executes; its Steps 1–7
  become this phase's Steps 2–7, and its pre-registered lanes (6a/6b/6c) are this
  phase's verdicts with the new closure excess lane.
- [[14_micro-phase-15-from-verdicts-to-showcase]] — the synthesis roadmap whose
  Steps 1–7 are this phase's inputs; its "no idle time" principle is inherited
  whole.
- [[13_micro-phase-14-the-verdicts]] — the verdicts phase whose lanes this phase
  consumes; after MP-17, no roadmap need ever point at it as "in flight" again.
- [[09_micro-phase-10-evidence-run]] — the run instruments and pinned configs this
  phase's Step 4 paper spine builds on.
- [[portfolio/RESULTS]] — the ledger this phase changes; the source of every paper
  number.
- [[portfolio/README]] — the showcase surface this phase's release pass refreshes.
- [[06_production_ai/proofs/reproducible-from-clean-clone]] — the Phase 6 gate
  proof whose real transcript Steps 2 and 7 produce.
- [[04_nlp_and_transformers/notes/induction-heads]] and
  [[04_nlp_and_transformers/notes/path-patching]] — the working notes that absorb
  the verdicts and the Zhang–Nanda audit.

## 8. Showcase note

This roadmap is my public record of judgment under uncertainty — including the
uncertainty about my own ability to close a loop I declared open in four previous
phases. Whatever the verdicts say, or don't say, the phase closes with a
demonstrable artifact and a ledger with no unanswered rows, and the "no silent
deferral" promise becomes a mechanical table instead of prose. That is the
portfolio's contract, and it is why this roadmap is written *before* the runs,
not after them.