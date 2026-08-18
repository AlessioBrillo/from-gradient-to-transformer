---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-18
---

# Micro-Phase 50 — State Review and Roadmap: the nineteenth question, written from the eighteenth release report

> **STATUS: REVIEW + ROADMAP, NOT A PRE-REGISTRATION.** This note is the
> companion review to [[00_meta/49_micro-phase-49-review-and-roadmap]], the
> eighteenth question's review and roadmap: it opens no rows, launches no
> runs, claims no window, and is wired into home only as a companion pointer —
> it is not a pre-registration and it is not counted against any cap, because
> the cap is spent. It is my personal state review and my step-by-step plan
> for the phase that starts at MP-50's Session 0, written in the same
> first-person register as my progress log so it doubles as the public record
> of how I reasoned about the program's steady state while MP-49's waiting
> window was still open. Everything factual in this file was re-verified
> against the repository on 2026-08-18: working tree clean, local `main`
> reconciled to `origin/main` at `f678fe4` (the MP-49 squash, PR #84), `dev`
> at the reconcile merge, `git diff main dev` empty, 190 tracked tests
> collected, ruff clean, blocking mypy clean, `verify-claims` at 0.

## Part I — Where I stand (state review, verified against the repo)

### The scientific ledger

The record's deepest fact has not changed and still has eleven dated
confirmations behind it, re-verified in this drafting sitting: **no run in
this repository's history has ever produced a sparse Fourier solution.** The
count advances only with a new verdict; between MP-49's sitting and this one,
no new Fourier cell landed — the microscope's trials 2 and 3 remain pending
in ADR-0003's budget.

- P=59 drills dense 59/59; P=113's three-seed verdict is NO-GROK (val 1.0,
  k_99 = 111/113); the positive-control scan stamped **ALL-DENSE** at
  P=59/67/97 (harness-level negative, val 0.0000–0.0006, gen −1); microscope
  trial 1 **FALSIFIED** (embedding re-normalization is not the suppressor:
  k_99 = 112/113, val 0.7176); trials 2 (`--schedule constant`) and 3
  (wd 1.5×) pending in ADR-0003's budget; and the R1 standard-scale ×3-seed
  run COMPLETED 2026-08-14 with the scheduled no-head negative as its verdict
  (0/8 heads, peak diag+1 mass 0.075 at epoch 499, peak val accuracy 0.5083
  near epoch 1950, K-composition max 0.056). The R1 verdict remains the
  newest dated fact on the record's negative side.
- All five manifests are on disk (`results/exp1…exp5`), and `verify-claims`
  is at **0** — re-verified in this sitting: `uv run python -m src.results
  verify` → "all manifests and RESULTS.md tags check out".

The arc my science has taken is the strongest thing I own: *will grokking
reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what
is the dense solution's structure?* (MP-29 S3's characterization, on disk) →
*which open question is deepest?* (MP-36's sitting) → *what does my own
phase map say about the boundary?* (MP-37's sitting) → *which of the causal,
circuit, law, rate and instrument questions does each consumed verdict open?*
(MP-38 through MP-48's sittings) → *which of C69–C72 does the consumed
eighteenth verdict open — or is the eighth post-record question the post-record
arc's own successor?* (MP-49's sitting). By MP-50's Session 0 the record will
hold eighteen dated directions, a characterized dense regime, a causal
reading (or its evidence lane), whichever of C69–C72 ADR-0023's sitting
chose — and the answer to the question MP-49's Session 0 owned more deeply
than any phase before it: **whether the post-record arc governs and, if it
does, what the eighth post-record question was.** The nineteenth question is
the sixth I choose with the sixth-generation arc consumption *stamped* — or
the ninth question past the record's closing sentence.

### What I found walking the shelf while drafting (verified intake facts)

Drafted and re-verified against the repository on 2026-08-18 — the facts a
hostile-webmaster walk would catch, each stamped with its state in this
sitting so the intake is a re-verification, never a memory:

1. **MP-49's roadmap is merged.** Verified: local `main` sits at `f678fe4`
   = `origin/main` (the MP-49 squash, PR #84), and `git diff main dev` is
   empty. MP-49's own intake facts are closed by its merge; Session 1's walk
   re-verifies with the branch list as the transcript.
2. **`portfolio/README.md` is still stale.** Re-verified: it still reads
   "Mini-paper (LaTeX PDF) not yet written", "Interactive demo … not built
   yet", "Experiment tracking … not set up yet" — contradicted by the record:
   the paper has lived through the v8–v15 arc (the v16–v18 rules belong to
   MP-46/47/48, the v19 rule to MP-49), the site and Space have been live
   since the premiere, and the manifest machinery has been tracking results
   since Micro-Phase 8. MP-49's Session 1 owns the dated fix; this phase's
   Session 1 re-verifies the closure with the dated file itself.
3. **No `essay-annex-*.md` exists on disk.** Re-verified: `portfolio/` holds
   `RESULTS.md`, `README.md`, `model-card.md`, `paper/` and `projects/` and
   nothing else. The annexes live on the live shelf (site and Space), not in
   this repository. The v20 annex contract must state the artifact's home
   with a date instead of implying the repo holds it.
4. **Rung 6 residue still survives on disk.** Re-verified: the deleted
   Rung 6 (2026-08-01, fabricated data) left
   `src/experiments/__pycache__/exp6_automated_circuit.cpython-312.pyc` and
   `figures/exp6_automated_vs_manual.png` in the gitignored directories
   (both confirmed present 2026-08-18). MP-49's Session 1 owns the removal
   with a transcript; this phase re-verifies the absence.
5. **`checklists/gate-debt.md` still does not exist.** Re-verified:
   `checklists/` holds `reproducibility-checklist.md` and nothing else. Row
   8's re-verification must record the absence with a date rather than claim
   a file that is not there.

Two further verified shelf facts. First: **`figures/` holds zero tracked
files** (`git ls-files figures/` empty) while `portfolio/figures/` holds the
twelve tracked figures — the showcase corpus is gitignored build product,
regenerated by `make reproduce` and provenanced by the manifests, never by
git. Second: **`docs/adr/` holds 0001–0010 and nothing else** — the stacked
phases' ledgers (ADR-0011 through ADR-0023) do not exist on disk because
they open at their own Session 0s; **ADR-0024's eight rows are the rows this
roadmap will fill**, and this phase's Session 0 opens it exactly once.

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no phase.
MP-37 through MP-48 are the un-cap's roadmap drafts executed exactly once
each. **MP-49's review and roadmap are merged, its Session −1 study lane owns
the waiting window, and its Session 0 awaits the stack's release.**
**ADR-0023's eight rows are the rows MP-49 will fill**; **ADR-0024's eight
rows are the rows this roadmap will fill** — exactly once, under the
continuum law, nineteenth execution, written from MP-49's release report
rather than from the habit of pre-registering.

### The CI floor and the toolchains

190 tracked tests, ruff, blocking mypy and markdownlint are green at the last
release; `verify-claims` at 0 — re-verified in this drafting sitting
(2026-08-18): 190 collected, ruff clean on `src/`, `verify-claims` at 0. The
verified gaps, stated as facts not hopes: no LaTeX toolchain on this machine
(`make paper` is graceful, not green), no Pages deploy workflow in
`.github/workflows/`, no `publish:` frontmatter policy, `portfolio/projects/`
holds figures but no project write-ups, W&B never connected. Each is a dated
row owned by named rows of earlier phases — their residue, never my
re-planning.

### The showcase corpus at intake

12+ provenance-guarded figures, the paper through the v15 arc (the v16 rule
is MP-46's, the v17 rule is MP-47's, the v18 rule is MP-48's, the v19 rule is
MP-49's, the v20 rule is this phase's), the site and Space live since the
premiere, the essay annex through the v15 arc, eighteen runnable teaching
artifacts with stranger-run transcripts (the receipts land only if the stack
ships: the eighteenth ships in MP-49, **the nineteenth in this phase**). My
teaching lane ships the nineteenth artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The intake is a consumption ten generations deep.** MP-50's Session 0
   must **consume MP-49's Session-0 decision with dates** — the single most
   dangerous drift is re-litigating a decision already consumed nine times:
   re-opening candidates the eighteenth question already closed with dated
   reasons, or treating "the post-record arc governs" as a mood instead of as
   a stamped verdict. The decision chain is now ten generations deep; a
   sitting stamps, it never re-decides.
2. **The stacked execution is still the critical path — and its head is
   still MP-29.** MP-50's Session 0 consumes MP-49's release report, which
   awaits the stack. A slip at any link slides the whole chain; **my
   highest-leverage act is unchanged: protect MP-29's window** — its release
   report is the artifact everything downstream consumes. Nothing in this
   phase may borrow a minute from it, and this draft is written
   verdict-agnostic by law: it re-plans not a single row of MP-29 through
   MP-49.
3. **ADR-0003 still carries UNDECIDED rows, and the ledger is the schedule.**
   The R1 run *completed* 2026-08-14, but rows 3–5 have not been stamped with
   their verdicts (the no-head negative for row 3; the scheduled negatives
   for rows 4–5), and rows 6–7 (paper prose, graduation proof) remain
   undated. MP-29's Session 8 requires zero UNDECIDED rows; a slip here
   stalls the entire stack. I do not re-plan those rows — but the waiting
   window pre-drafts the *prose* of those scheduled negatives so the stamping
   sitting is a stamping, never a discovery.
4. **The microscope budget is one failure away from exhaustion.** Trial 2's
   verdict forces trial 3's choice (the ledger's "my own third"); three
   failures close row 2 and make the dense characterization the phase's
   headline. Verdict-agnostic readiness means: **trial 3's pre-registration
   is drafted in the waiting window, with its falsifier column already
   filled** — so no sitting ever chooses an improvised third trial.
5. **The CPU wall is the science's binding constraint.** Every pending run
   (trial 2, trial 3, the characterization's per-head dictionaries and
   ablations) shares one CPU and overnight windows. Wall-clock is budgeted at
   launch, never at Session 7 — heartbeat, checkpoint-every-500, scheduled
   negative drafted while the run is live.
6. **The steady state must not become ceremony.** MP-50 will be the
   thirteenth roadmap written from an *executed* roadmap's release report —
   the program's normal, confirmed twelve times. The countermeasure is
   concrete: **every session's exit names at least one artifact changed on
   disk, and every row is dated in the sitting that owns it** — a stamped row
   with no science behind it is ceremony by another name.
7. **The paper's compile gate is the hardest artifact in the stack.** No TeX
   on this machine — verified again in this sitting. The v20 rule ("opens
   only for new numbers, else the v19 is the record") is my insurance; the
   toolchain decision (local MiKTeX/TeX Live vs. Overleaf) is pinned at
   Session 0, never discovered at Session 7.
8. **Stop-and-publish is a row, not a threat — and the post-record criterion
   is now nine questions deep.** ADR-0004's row 5 stays open as the program's
   honest exit: a phase is worth doing only if its candidate set can earn a
   paragraph the record does not already have. If MP-49's Session 0 continued
   the post-record arc, the deepest candidate this phase can choose earns the
   post-record arc's *eighth new paragraph* — the record's closing sentence
   consumed nine times, never repeated. The deepest form of laziness is
   building what the record has already said.

## Part III — The roadmap, step by step (the continuum law, nineteenth execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C73 | **The theory as a research programme** (C69's successor) — the failure-cell theory *predicted a third time*: the per-head mechanism at the fourth unseen task family's and the third architecture family's failure cells written as falsifiable predictions before any number is read, causally verified by patching, the theory's domain statement extended from "predicts unseen cells twice" to "predicts unseen cells three times" — a theory that predicts three times is a research programme; a theory that predicted twice is a predictive theory, and the prediction is on the record | ADR-0023 row 3 = C69 with a positive verdict (the second prediction on disk) | C69 closed negative, or the post-record arc governs → the theory's third round belongs to the post-record arc |
| C74 | **The boundary law as a phase diagram** (C70's successor) — the full P×wd×recipe×architecture space *closed*: a dated root-cause mechanism for every cell of both architecture families across three recipes, each exception ablated, no cell left unmapped — a complete exception map is the law's boundary; a boundary complete across two families and three recipes is the law's phase diagram | ADR-0023 row 3 = C70 with the exception map on disk | C70 never opened, or its verdict was negative → no diagram to complete |
| C75 | **The discipline as the institution** (C71's successor) — the thirteenth reproducibility study: the eighth drift measurement after the seventh dated fix, the rate function's parameters re-estimated from the receipt system's history, the next measurement's schedule *predicted before it happens* and the policy *enforced* across the stack's own execution window — a policy that survives its own enforcement is a discipline; a discipline that predicts its next measurement and keeps its date is an institution | ADR-0023 row 3 = C71 with the seventh measurement and attribution on disk AND ≥ 19 stranger-run transcripts at S0 | Fewer than 19 transcripts, or C71 never opened → the receipt system hasn't earned a thirteenth study |
| C76 | **The instrument as the standard** (C72's successor) — the fifth-edition course *validated a fifth time by the uninvited* under the rubric *already released as a standalone artifact others can run*: the scoring rule's third prediction round checked against the fifth cohort's friction, the feedback-to-fixes matrix's third prediction round executed — an instrument others can run is a standard; an instrument validated four times by the uninvited is a standard with a track record | ADR-0023 row 3 = C72 with the fifth cohort's measured outcome on disk | C72 never opened, or a sparse regime exists → the sparse reading owns the question |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥
3 checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The terminal-state override stands, now ten generations deep: **if MP-49's
Session 0 consumed MP-48's decision with dates and the post-record arc
governs, then MP-50's Session 0 consumes the eighth post-record question's
verdict from ADR-0023 row 3 and continues the post-record arc, choosing the
ninth post-record question from the pre-registered continuation set below.**
The rule is executed with dates at Session 0; it is never improvised and
never re-negotiated in the sitting that consumes it.

### The post-record continuation set (chosen only if MP-49 continued the post-record arc)

| # | Candidate | Why it would open | Why it would close |
|---|---|---|---|
| PR-25 | **The new harness's fourth cross-recipe law** (PR-22's successor) — the *sixth* recipe at the new address replicated across seeds and compared to the first five under the record's laws: six recipes compared across seeds is the harness's fourth law datum; five recipes compared once is a third datum, and the datum is the result | The post-record arc continued at MP-49 with PR-22's verdict on disk | The record never closed, or the redemption fired first → the sparse question belongs to the old arc |
| PR-26 | **The law at the record's edge, ninth task** (PR-23's successor) — the frozen-checkpoint predictions tested at the ninth unseen task family: a law that predicts nine times is a law with a predictive record; a law that breaks is a boundary with a map | The post-record arc continued at MP-49 with PR-23's verdict on disk | The record never closed → the law's successors are C73's, not the post-record arc's |
| PR-27 | **The record as a course, eighth edition** (PR-24's successor) — the seventh edition revised from its sixth intake: the feedback-to-fixes matrix executed with dates, the nineteen runnable artifacts assembled, the eighth edition measured as a learning instrument with seven cohorts — a course revised from its receipts seven times is a curriculum; a course re-shown is a poster | The post-record arc continued at MP-49 with PR-24's verdict on disk | The record never closed → the teaching lane continues as the continuum's row 8 |

The likely survivor, written as a condition chain, never a prediction: if
MP-49's Session 0 continued the post-record arc → **the post-record
continuation** — the ninth question past the record, chosen in the consuming
sitting from PR-25/PR-26/PR-27; else if C69 landed positive → **C73** — the
theory's third prediction, always CPU-runnable on checkpoints that exist
today; else if C70's exception map landed → **C74**; else **C75**
(always-runnable, the showcase's own science, receipts now nineteen deep);
C76 is the evidence lane and the teaching lane's anchor.

### The sessions

1. **Session −1 (~1 h/day, now → the stack's release) — the waiting-window
   study lane.** The days before MP-49's Session 0 are owned, not idle. Each
   day: one study block from Part IV (reading → prediction written *before*
   the reading → one-page memo filed in the study log), the clock-check
   habit, and one waiting-window exercise (Ex-α3 through Ex-ε3). Deliverables:
   the trial-3 pre-registration drafted verdict-agnostic with its falsifier
   column filled; the R4/R5 scheduled-negative prose pre-drafted; the S0
   intake checklist pre-built with empty date cells; the C73–C76
   opening-or-closure memo skeletons; the Ex-T3 execution-memo skeleton. All
   saved beside MP-29's lanes, never inside them. *Exit: the study log has
   one dated entry per day; the pre-drafts exist on disk; no row of MP-29
   through MP-49 was touched.*
2. **Session 0 (~1 h) — the gate truthing + the nine-generations-deep arc +
   the continuum choice.** Consume MP-49's release report row by row:
   ADR-0023 at zero UNDECIDED rows, the live URL re-clicked in the sitting,
   `verify-claims` at its actual count, the eighteenth teaching transcript
   on disk, `dev == main` (branch list as the transcript). Commit the intake
   table before a single continuum row opens. Then **Ex-T3: consume MP-49's
   Session-0 decision with dates** — the ninth-generation consumption: if
   the post-record arc continued, the eighth post-record question's verdict
   is read from ADR-0023 row 3 and the ninth post-record question chosen
   from the pre-registered continuation set (PR-25/PR-26/PR-27), each
   opening-or-closure memo in three sentences with a falsifier; if not, the
   C73–C76 adjudication: exactly one opens as row 3, the unchosen close with
   one dated reason each, stamped in the same sitting. Open ADR-0024 with its
   eight rows, windows and kill-dates; declare the terminus (release = merge + 14 calendar days);
   promote this roadmap from MP-49's release report, deviations recorded as
   dated ledger notes. **The toolchain decision is pinned here** (TeX choice;
   `make paper` re-verified in the CI mirror). *Exit: intake signed; the
   nine-generations-deep arc stamped; row 3 chosen (or the post-record
   continuation row opened); ledger open.*
3. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — extended to the repo's own shelf: local `main`
   re-verified reconciled to `origin/main` (branch list as the transcript),
   `portfolio/README.md`'s staleness verified closed (MP-49's Session 1 owned
   the first fix; this sitting verifies the file is current), the exp6
   residue removed with a transcript, the annexes' location verified. Row 8:
   MP-49's stamped closures re-verified (W&B, clean-clone proof, graduation
   proof, `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch resolution,
   the README fix, the residue removal) — each cell LAUNCHED-with-transcript
   or CLOSED-with-one-reason; a claimed closure without its transcript stays
   open and blocks Session 8; `gate-debt.md`'s absence, if still absent,
   recorded with a date. *Exit: rows 5 and 8 stamped.*
4. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the eighteenth research question's verdict (ADR-0023 row 3) becomes the
   paper-v20 section, the annex table, or the results-page row — every number
   manifest-tagged, consumed in the sitting that owns it; if the post-record
   arc governs, the post-record statement is framed from MP-49's release,
   never rewritten. Row 2: v20 opens only if row 1 lands new numbers; else
   "the v19 is the record" is the dated reason and `make paper` is re-verified
   against v19. Row 6's substitute filed from the visitor's chair, before the
   window opens (Ex-G); the fork drill (Ex-H) and the arc consumption (Ex-N
   through Ex-T3) land here. *Exit: rows 1 and 2 dated; substitute filed;
   Ex-T3's execution memo on disk.*
5. **Session 3 (~2–3 h) — the essay annex v20.** `portfolio/essay-annex-20.md`
   (its home on the live shelf, dated): the eighteenth question's verdict set
   and the teaching lane's eighteenth receipt distilled into one dated annex;
   the reverse claims audit at zero (prose → manifest → command); each
   claim's "what would falsify this" column filled at writing time. The annex
   is amended, never rewritten. *Exit: row 4 dated; audit at zero.*
6. **Session 4 (~1 h) — the stranger round 20 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. *Exit: window open,
   kill-date declared.*
7. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat — or, if the post-record
   arc governs, the continuation row's protocol opened under the same
   discipline. If C73: the failure cells at the fourth unseen task family and
   the third architecture family, and the expected per-head mechanism written
   as falsifiable predictions before a single number is read (Ex-C, Ex-I3,
   Ex-J3, Ex-S3, Ex-U3, Ex-W3). The scheduled negative is drafted *while the
   run is live* (Ex-D), so the S6 verdict sitting is a stamping, not a
   discovery. Row 6's kill-date honored (feedback → matrix drafted; silence →
   substitute closes it). Row 7: the nineteenth teaching artifact's skeleton
   drafted — walkthrough v19, 10-minute talk v19, or Colab grokking notebook
   v17 — with its ship-date. *Exit: row 3 pre-registered and launched (or the
   post-record protocol opened); row 6 dated either way; row 7's skeleton
   drafted.*
8. **Session 6 (~1–2 h) — the research verdict sitting.** Row 3's verdict
   read from the manifest: completed and dated, or window closed and the
   scheduled negative is the result — drafted while the run was live (Ex-D),
   so this sitting is a stamping, not a discovery. *Exit: row 3 dated either
   way.*
9. **Session 7 (~2–3 h) — the shelf rehearsal + the re-check row + the
   teaching polish.** Row 5: the hostile-webmaster walk at zero beside the
   browser, every public number clicked back to disk; the repo-shelf findings
   re-checked (local `main` reconciled, README current, residue gone, annexes'
   home verified). Row 6's re-check row dated. Row 7: the nineteenth artifact
   runs end to end on a stranger's machine (fresh clone / Colab session); the
   run transcript is the receipt; the teaching distillation (Ex-F) lands
   here. *Exit: rows 5, 6, 7 dated; the artifact shipped with its transcript.*
10. **Session 8 (~1 h) — the release.** ADR-0024 at zero UNDECIDED rows; the
    merge green locally and on GitHub; `dev == main`; home wired — this
    roadmap's companion status retired; the roadmap archived with its
    deviations, every deviation a dated ledger note. If the post-record arc
    governs, this sitting stamps the post-record arc's ninth dated direction
    — the record's closing sentence consumed nine times, never repeated.
    *Exit: the merge; the program's nineteenth dated direction — or the
    post-record arc's ninth.*

### The one measured line

ADR-0024 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row (or the post-record continuation row) whose verdict (or
scheduled negative) re-derives from a manifest; `verify-claims` at 0 with
every public number re-derivable from one command line; the hostile-webmaster
walk at zero on the live shelf and on the repo's own shelf (local `main`
reconciled, README current, residue removed, the debt ledger present or
absent-with-date); the nineteenth teaching artifact shipped with a
stranger-runnable transcript; `dev == main` and the program's nineteenth
dated direction — or, if the post-record arc governs, its ninth dated
direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk. Filed as one dated
memo each in the study log.

1. **The theory as a research programme (the C73 reading).** Elhage et al.,
   *A Mathematical Framework for Transformer Circuits* (2021) for the QK/OV
   machinery the causal claim is made over; Wang et al., *Interpretability in
   the Wild* (2022) for activation-patching methodology at per-head
   resolution; Conmy et al., *Towards Automated Circuit Discovery* (2023) for
   turning a hand-traced mechanism into a scalable, testable procedure (read,
   never re-implemented — ACDC stays descoped); Varma et al., *Explaining
   grokking through circuit efficiency* (2023) for why circuits grow sharp
   and where that sharpness is measurable; Olsson et al., *In-context
   Learning and Induction Heads* (2022) for what transfers across task
   families; Chughtai et al., *A Toy Model of Universality* (2023) for why
   the fourth unseen task family's and the third architecture family's
   failure cells fail the way they do — now read at the *third-prediction*
   axis: what a theory earns by predicting unseen cells three times, where
   two-round theories overreach on their third round, and what Popperian
   corroboration and Lakatosian progressivity say about a law whose third
   out-of-sample round lands. My C69 verdict and its measured theory frame
   the reading. **Prediction to write**: which per-head role's failure
   mechanism is the boundary's root cause at the fourth unseen task's
   structure and at the third architecture family's, and what the patching
   at those cells reveals; the null hypothesis every measured fingerprint is
   compared against. **Primary sources**: the frozen checkpoints, C69's
   theory table, the S3 note.
2. **The boundary law as a phase diagram (the C74 reading).** Lyu et al.,
   *Understanding the training dynamics of transformers on modular
   arithmetic* (2024) for the loss-landscape structure of grokking and its
   phase transitions; Morwani et al. (2024) on the edge-of-numerical-
   stability regime; Gromov, *Grokking: A Memory Perspective* (2023); Power
   et al. (2022); Nanda et al. (2023) — now read at the
   *completeness-across-families* axis: what a full-cell root-cause map
   across two families and three recipes claims that a two-family map does
   not, and where "the driver" is really an optimization artifact that does
   not survive the third recipe. **Prediction**: the remaining diagram
   cells' root causes written before the analysis; C70's completed map is
   this reading's admission ticket.
3. **The discipline as the institution (the C75 reading).** Gelman & Loken,
   *The Garden of Forking Paths*; Pineau et al. (2021); Kapoor & Narayanan,
   *Reproducibility in Machine Learning: A Systematic Literature Review*
   (2023); the ML reproducibility line (NASEM's five pillars) — now read at
   the *institutionalization* axis: what a policy gains when its next
   measurement is predicted *before* it happens and kept on its own schedule,
   and what a discipline can honestly claim that a model cannot. My nineteen
   stranger-run transcripts are the data; the twelfth study defined the
   eighth drift, I must decide what counts as the thirteenth measurement
   before I measure any.
4. **The instrument as the standard (the C76 reading).** Bricken et al.
   (2023); Cunningham et al. (2024); the dictionary-circuit and
   feature-universality line — plus the education-measurement line (rubric
   validity, inter-rater reliability, external assessment, instrument release
   norms) for what a *fifth, uninvited cohort* under a *released standard
   others can run* claims that a fourth's does not. My Rung-5 datum (99.97%
   FVE, L0 = 136/256, 0% dead features) and C72's fifth-cohort outcome are
   the record's first data points.
5. **The post-record program, ninth generation (new, deepest).** Lakatos,
   *The Methodology of Scientific Research Programmes* (1978) — read a tenth
   time, now for the *ninth* question past a completed program: progressive
   vs. degenerating problem shifts when the *eighth* post-record verdict
   lands, Kuhn's normal science as the post-record arc's axioms, and the
   honest criterion for the ninth post-record question — a question that
   must earn the post-record arc's eighth *new* paragraph. This reading
   feeds Ex-T3 and the Session-0 question MP-50 owns more deeply than any
   phase before it: *what does the record's eighth post-record verdict
   open?* The answer can be the post-record arc's ninth dated row —
   Lakatos' point is that the decision is made on the record, never as a
   mood.
6. **The record teaches, round nineteen.** The nineteenth verdict in four
   registers — the paper's sentence, the annex's sentence, the 30-second
   spoken claim, and the 5-minute teaching explanation with a worked toy a
   stranger can run; the gap between the last two is where my teaching
   leaks, and I will measure it deliberately by writing all four registers
   for the same verdict (Ex-F). **Waiting-window rehearsal**: run the four
   registers on the R1 no-head negative — a stamped verdict, safe to
   practice on.
7. **The redemption reading, or negative results as maps, the nineteenth
   pass.** If a sparse cell exists by S0: Nanda et al.'s full per-frequency
   reading on the first sparse solution this harness ever produced. If not:
   how the *completed* law is reported honestly — the law's domain closed
   with its measured boundaries and its failure cells explained or mapped,
   the driver a principle or a case study with a dated exception map, the
   drift numbers nine deep, the negative as a contribution — and how the
   post-record harness (if PR-25 governs) would be designed from the dated
   negatives instead of from hope. Either way, the paper's hardest paragraph
   is the one that claims the dense solution *computes something*; I will
   draft it against this reading and let the manifest referee it.
8. **The mathematical bedrock, third pass (new).** The DFT-of-addition
   derivation I hand-rolled in the waiting windows extended to the *third
   architecture family's* geometry: what changes in the embedding's spectral
   support, the QK/OV factorization and the convolution theorem when the
   family changes a second time — the derivation that makes every
   third-family fingerprint interpretable rather than decorative. **Primary
   sources**: Nanda et al. (2023) and its appendix; my own `01_foundations`
   linear-algebra proofs; the exp2 Fourier instrument on disk. **One
   runnable check**: the hand derivation reproduced in a one-file script
   whose DFT output matches `results/exp2_grokking.json`'s k_99 = 111/113 at
   P=113, then re-run at the third family's geometry.
9. **The epistemology of the third prediction (new).** Popper's
   corroboration and Lakatos' problem-shift progressivity read against my own
   record: what a C73 verdict would *claim* about the theory, what a
   falsified third round would *change*, and how the paper should say either
   — the reading that makes the phase's verdict honest in its own terms,
   and the threshold at which the record's "theory" line stops being a
   hypothesis and becomes a programme.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-49's release report, deviations recorded as dated ledger
  notes.
- **ADR-0024**, the nineteenth continuum ledger — eight rows pre-stamped
  with windows and kill-dates; rows 1–2 consumed from ADR-0023's verdicts;
  row 3 the nineteenth research question with its protocol note and
  heartbeat (or the post-record continuation row's protocol); rows 4–8 the
  continuum's decisions.
- **`portfolio/essay-annex-20.md`** — the v20 annex, manifest-tagged,
  amended never rewritten; the annexes' home (the live shelf) recorded with
  a date.
- **The paper v20 diff** (`portfolio/paper/main.tex` v20 + diff log) or the
  dated "the v19 is the record" memo; `make paper` re-verified in the CI
  mirror with the toolchain decision pinned at Session 0.
- **The shelf health sheet + hostile-webmaster transcript** (site + Space at
  zero), extended to the repo's own shelf: local `main` reconciled to
  `origin/main`, `portfolio/README.md` current, the exp6 residue removed, the
  annexes' location verified; the claims gate re-run on every merge.
- **`checklists/gate-debt.md`** — each cell's transcript or one-line reason,
  dated in Session 1; the file's absence, if still absent, recorded with a
  date.
- **The research row's pre-registration note** (site, metric, negative
  control, kill-date) in `06_production_ai/notes/` + the heartbeat artifact;
  if C73: the third-prediction figure spec written before the analysis, the
  figure itself manifest-tagged after. If the post-record arc governs: the
  continuation row's protocol note instead.
- **The nineteenth teaching artifact + its stranger-run transcript**
  (fresh-clone or Colab session receipt).
- **Ex-T3's execution memo** — MP-49's arc decision run with dates, written
  verdict-agnostic and executed at Session 0.
- **The waiting-window pre-drafts** (new, alongside MP-49's Session −1): the
  S0 intake checklist pre-built with empty date cells, the C73–C76
  opening-or-closure memo skeletons, the Ex-T3 execution-memo skeleton —
  saved beside MP-49's lanes, never inside them.
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C73–C76 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting — preceded by the arc consumption (Ex-N through Ex-T3), which may
   close the whole set with the post-record verdict.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0023's row-3 verdict traced to its manifest and its command; the rest
   struck with a reason — the hostile-webmaster test of my own prose,
   nineteenth run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C73 or C74 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the failure cells and the expected per-head mechanism at the
   fourth unseen task's structure and the third architecture family's, the
   driver's predicted exception cells with their ablation signatures — the
   "what would falsify this" column filled at writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v20 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, with the repo's own shelf added: branches reconciled, README
   current, residue removed.
6. **Ex-F · The teaching distillation, round nineteen (S7):** the nineteenth
   question's verdict in four registers — the paper's sentence, the annex's
   sentence, the 30-second spoken claim, the 5-minute teaching explanation
   with a worked toy a stranger can run; the gap between the last two is
   where my teaching leaks.
7. **Ex-G · The stranger substitute from the visitor's chair (S2):** the
   self-review written from the chair a stranger would occupy — friction
   points → fixes → re-check row — filed before S4, so the S5 kill-date can
   never close the row with a skip.
8. **Ex-H · The fork drill, deepest form (S2, verdict-agnostic):** the
   continuing state (C73–C76) vs. the post-record state (PR-25/PR-26/PR-27)
   written as two one-page paths — what each verdict changes downstream,
   including the C73-vs-C74 choice and the post-record continuation choice —
   so next phase's S0 decision is a stamping, not a discovery.
9. **Ex-I3 · The boundary hand-roll, round eight (S5, C73 only, before any
   number is read):** the expected per-head mechanism at the fourth unseen
   task's and the third architecture family's failure cells written by hand
   from C69's theory table — which per-head roles must transfer unchanged,
   which may re-tune, which should fail first, and what patching at those
   cells should reveal — the null hypothesis every measured fingerprint is
   compared against. One runnable check: the hand-rolled fingerprints printed
   and saved next to Ex-J3's observed ones, so the S6 comparison is a diff,
   not a memory.
10. **Ex-J3 · The transfer reader, round eight (S5, C73 only):** the script
    that loads the frozen checkpoints at every P (including the fourth
    unseen task's and the third family's), runs the per-head extraction and
    patching machinery, and emits the failure-cell table as a manifest-tagged
    JSON. One runnable check: the reader runs on the frozen checkpoints and
    its output is committed before the verdict paragraph is drafted.
11. **Ex-K3 · The sparse-recovery toy, revisited a thirteenth time (my
    foundation challenge, third-family pass):** the one-file toy that
    recovers the addition table's DFT coefficients under L2 vs L1 penalties,
    now extended to the completion question: *does the sharpening ablation
    signature survive across three architecture families and three recipes,
    and where does it break?* One runnable check: the toy prints both
    reconstructions' sparsity and error plus the ablation table on a fixed
    seed, across three architectures. This is the micro-scale intuition
    C74's verdict must not contradict.
12. **Ex-L3 · The "what does the dense solution compute?" sprint, round
    thirteen (S5, C73 only):** the paper's hardest paragraph drafted at S5,
    then audited against the mechanism reading at S6 — prose that must
    survive contact with the manifest, the "computes something" claim earned
    or struck with one reason.
13. **Ex-M3 · The stranger-run drill on my own receipt (S1):** I execute
    MP-49's shipped artifact (the eighteenth) on a fresh clone as if I were
    the stranger — the transcript becomes the baseline against which the
    nineteenth artifact's transcript is compared. One runnable check: the
    baseline transcript saved beside the new one.
14. **Ex-N · The arc consumption, second generation (S0):** MP-40's Ex-N
    defined the terminal state; MP-41 executed it; MP-42 through MP-49
    consumed it eight times. This drill executes that second-generation
    consumption exactly as MP-49's memo stamped it.
15. **Ex-O · The arc consumption, third generation (S0):** MP-49's
    Session-0 decision becomes the object of the consumption — the eighth
    post-record question's verdict read from ADR-0023 row 3 if the arc
    governs, the criteria cited, the release that follows. One runnable
    check: the execution memo exists, names the decision rule, cites the
    criteria from MP-49's release report.
16. **Ex-P … Ex-R, Ex-T · The arc consumption, generations 4–7 (S0):** the
    consumption chain's deepest runs as MP-49 stamped them — each memo cites
    the criteria from the release report it consumes. One runnable check per
    drill: the execution memo exists and cites the criteria from the release
    report.
17. **Ex-T3 · The arc consumption, ninth generation (S0, new,
    verdict-agnostic):** the consumption chain's deepest run — MP-49's
    Session-0 decision consumed with dates as MP-50's intake, the
    eighth-generation post-record verdict read from ADR-0023 row 3 if the
    arc governs, the criteria cited, the release that follows (the ninth
    post-record question, or the C73–C76 adjudication), and what each of
    ADR-0023's possible verdicts changes in that execution. One runnable
    check: the execution memo exists, names the decision rule that closes or
    continues the program's science, and cites the criteria from MP-49's
    release report — the chain now ten generations deep, a sitting stamps,
    it never re-decides.
18. **Ex-S3 · The out-of-sample sprint, round eight (S5, C73 only):** the
    mechanism's predictions at the fourth unseen task family written as a
    dated table before any number is read — task family, expected failing
    head role, expected order of failure, expected patching signature — with
    the falsifier column filled at writing time; the observed table compared
    at S6 as a diff, not a memory.
19. **Ex-U3 · The architecture-family sprint, round eight (S5, C73 only):**
    the law's predictions at the third architecture family written as a dated
    table before any number is read — family, expected per-head role transfer
    or re-tuning, expected failure order, expected patching signature — with
    the falsifier column filled at writing time; the observed table compared
    at S6 as a diff, not a memory.
20. **Ex-V3 · The drift-attribution drill, round five (S5, C75 only, new):**
    the rate function's parameters re-estimated from the nineteen transcripts
    before any fix, the eighth drift's components attributed — harness change
    vs. protocol drift vs. codebase aging — each component's contribution
    re-estimated, the top root-cause's fix dated in the same sitting. One
    runnable check: the re-estimated parameter table saved beside the drift
    numbers, so the S6 verdict is a diff, not a memory.
21. **Ex-W3 · The theory's falsifier column, round three (S5, C73 only,
    new):** each third-round failure-cell explanation written with its own
    falsifier — the single observation that would refute the explanation of
    why this cell fails — filled at writing time, before the analysis; the
    S6 verdict is a diff between prediction and observation, never a memory.
22. **Ex-X3 · The exception-map hand-roll, round three (S5, C74 only, new):**
    the remaining diagram cells' root causes written by hand from C70's map
    before any number is read — which cells the chain survives, which it
    breaks at, and why, with the ablation signature each exception should
    carry; the observed map compared at S6 as a diff, not a memory.
23. **Ex-Y3 · The policy allocation drill, round three (S5, C75 only, new):**
    the thirteenth measurement's schedule derived from the rate model before
    the run — the next measurement, its budget, its predicted outcome, its
    falsifier — so the S6 verdict compares the schedule against what the
    receipt system actually did, as a diff, not a memory.
24. **Ex-Z3 · The public rubric draft, round three (S5, C76 only, new):**
    the fifth cohort's rubric written as a public artifact — scoring rule,
    evidence requirements, adjudication procedure, release license — before
    recruitment, so the fifth measurement is taken under the published rule,
    never after it.
25. **The waiting-window drills (Session −1):** Ex-α3 the DFT hand-roll,
    third pass (the derivation extended to the third family's geometry);
    Ex-β3 the four-registers rehearsal on the R1 no-head negative; Ex-γ3 the
    scheduled-negative drafting drill (ADR-0003 rows 4–5 prose + trial 3's
    pre-registration, falsifier columns filled); Ex-δ3 the stranger-run drill
    on the eighteenth artifact once it ships (the transcript becomes the
    nineteenth's baseline); Ex-ε3 the trial-3 falsifier decision tree written
    before trial 2's verdict is read.
26. **Habit · The clock check (every session):** ADR-0024's undated rows, the
    open PR's CI status line, the shelf's health — all three before any new
    prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, nineteenth execution.** A phase that opens two
  research questions is drift by another name; the unchosen candidates close
  in the same sitting as the choice — and the arc consumption may close all
  of them with the post-record verdict. The continuum law is the mechanical
  refusal of this drift — proven executable eighteen times, it must simply
  be executed again.
- **The candidate set is frozen before S0, never improvised at it.** C73–C76
  are conditions, not predictions; a sitting decides, it never invents — and
  the terminal-state object is the hardest frozen object on the record:
  written by MP-40, executed by MP-41, consumed nine more times since —
  *consumed a tenth time* by MP-50, never re-negotiated in the consuming
  sitting.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0023's row-3 verdict in the sitting that owns it
  — or the post-record statement, if the arc governs.
- **The receipt compounds.** The nineteenth runnable artifact is only worth
  shipping because the first eighteen transcripts proved the format — and
  if C75 opens, the receipts are a drift-of-drift-of-drift-of-drift-of-
  drift-of-drift-of-drift-of-drift number measured eight times in a row,
  tested by people I did not choose, across an aging codebase. My showcase's
  story is now "read it, run it, watch me be wrong on the record," nineteen
  receipts deep.
- **The waiting window belongs to MP-49's Session −1 — and this draft is a
  companion written inside it.** The days between this draft and the stack's
  release are owned lanes: readings with predictions written before the
  reading, hand-derivations, pre-drafted scheduled negatives, the S0 intake
  checklist pre-built with empty date cells. A day with no dated entry is a
  row without a date.
- **Budget the wall-clock at launch, never at Session 7.** The CPU is the
  binding constraint; every run gets a budget row, a heartbeat, a
  checkpoint-every-500, and a scheduled negative drafted while it is live.
  This is the architecture law that protects the release date.
- **Toolchains are pinned in S0, never discovered at S7.** The paper's
  compile gate is the hardest artifact in the stack; the v20 rule ("opens
  only for new numbers") is the insurance that makes a missing toolchain a
  dated reason, not a crisis.
- **Protect the release report.** The serialized stack means MP-29's release
  is still the artifact everything downstream consumes; a slip at any link
  slides the whole chain. A promise can be re-planned forever, but a dated
  row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0023 at zero, the live
  URL, `verify-claims` at 0, the eighteenth teaching transcript on disk — a
  condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; the R1 no-head negative — 0/8
  heads, stamped 2026-08-14 — is the record's newest dated signature. The
  strongest form of the signature is the chain: negative → map →
  characterization → mechanism → causal verdict → circuit → law → theory →
  second prediction → *third prediction* — or a record that knew when to
  end.
- **The steady state is the reward, not the ceremony.** MP-50 will be the
  thirteenth roadmap written from an *executed* roadmap's release report —
  the program at its normal, confirmed twelve times. The machinery is the
  guardrail, never the goal: rows are dated in the sitting that owns them, or
  they are not rows.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED rows
  at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story:** *the program's nineteenth dated
  direction was written from its own release report — the cap honored, the
  stack executed, the steady state kept honest thirteen times, the record
  taught nineteen times in runnable artifacts, every public number still
  re-derives from one command line, and the record consumed — ten times,
  with dates — its own terminal-state decision, and answered it in a
  release.* Every artifact this phase launches is written to that standard.

## Links

- [[00_meta/49_micro-phase-49-review-and-roadmap]] — the eighteenth
  question's review and roadmap; this roadmap's intake is ADR-0023's release
  report and MP-49's Session-0 decision, which Session 0 consumes again.
- [[00_meta/48_micro-phase-48-review-and-roadmap]] ·
  [[00_meta/48b_micro-phase-48-execution-roadmap]] — the seventeenth
  question's review and execution roadmap, the un-cap's steady state
  confirmed twelve times.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat — and the
  row the terminal state executes.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/microscope-trial-table]] ·
  [[06_production_ai/notes/positive-control-protocol]] — the science C73–C76
  adjudicate over, whose pending verdicts are the intake.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/checkpoint-resume-durability]] ·
  [[06_production_ai/notes/scheduled-negatives-mp28]] — the CPU-budget canon
  the phase's runs are specified against.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.
