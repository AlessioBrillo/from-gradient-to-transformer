---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-17
---

# Micro-Phase 46 — State Review and Roadmap: the fifteenth question, written from the fourteenth release report

> **STATUS: REVIEW + ROADMAP, NOT A PRE-REGISTRATION.** This note is the
> companion review to [[00_meta/45_micro-phase-45-review-and-roadmap]], the
> fourteenth question's review and roadmap: it opens no rows, launches no
> runs, claims no window, and is wired into home only as a companion pointer
> — it is not a pre-registration and it is not counted against any cap,
> because the cap is spent. It is my personal state review and my
> step-by-step plan for the phase that starts at MP-46's Session 0, written
> in the same first-person register as my progress log so it doubles as the
> public record of how I reasoned about the program's steady state before I
> executed through it. Everything factual in this file was re-verified
> against the repository on 2026-08-17: working tree clean, `dev` reconciled
> with `main` at the MP-45 squash (PR #79, `main` at `5308c9d`, `dev` at
> `34f82e8`), 190 tracked tests, ruff clean, blocking mypy clean,
> `verify-claims` at 0.

## Part I — Where I stand (state review, verified against the repo)

### The scientific ledger

The record's deepest fact has not changed and now has ten dated
confirmations behind it: **no run in this repository's history has ever
produced a sparse Fourier solution.**

- P=59 drills dense 59/59; P=113's three-seed verdict is NO-GROK (val 1.0,
  k_99 = 111/113); the positive-control scan stamped **ALL-DENSE** at
  P=59/67/97 (harness-level negative, val 0.0000–0.0006, gen −1); microscope
  trial 1 **FALSIFIED** (embedding re-normalization is not the suppressor:
  k_99 = 112/113, val 0.7176); trials 2 (`--schedule constant`) and 3
  (wd 1.5×) are pending in ADR-0003's budget; and the R1 standard-scale
  ×3-seed run COMPLETED 2026-08-14 04:07 local — the scheduled no-head
  negative is the verdict: 0/8 heads, peak diag+1 mass 0.075 at epoch 499,
  peak val accuracy 0.5083 near epoch 1950, K-composition max 0.056. The R1
  verdict remains the newest dated fact on the record's negative side,
  re-verified in this drafting sitting.
- The exp2 and exp5 manifests are clean on disk; `verify-claims` at **0**,
  re-verified in the MP-45 drafting sitting and again in this one
  (2026-08-17: `uv run python -m src.results verify` → "all manifests and
  RESULTS.md tags check out").

The arc my science has taken is the strongest thing I own: *will grokking
reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what
is the dense solution's structure?* (MP-29 S3's characterization, on disk) →
*which open question is deepest?* (C17/C18, MP-36's sitting) → *what does my
own phase map say about the boundary?* (C21–C24, MP-37's sitting) → *which of
C25–C28 does the mechanism reading open?* (MP-38's sitting) → *which of
C29–C32 does the causal verdict open?* (MP-39's sitting) → *which of C33–C36
does the complete circuit open?* (MP-40's sitting) → *which of C37–C40 does
the law open?* (MP-41's sitting) → *which of C41–C44 does the consumed
terminal-state verdict open — or is the first post-record question the
record's own successor?* (MP-42's sitting) → *which of C45–C48 does the
consumed choice open — or is the second post-record question the post-record
arc's own successor?* (MP-43's sitting) → *which of C49–C52 does the consumed
Session-0 decision open — or is the third post-record question the
post-record arc's own successor?* (MP-44's sitting) → *which of C53–C56 does
the consumed thirteenth verdict open — or is the fourth post-record question
the post-record arc's own successor?* (MP-45's sitting). By MP-46's Session 0
the record will hold fourteen dated directions, a characterized dense regime,
a causal reading (or its evidence lane), whichever of C53–C56 ADR-0019's
sitting chose — and the answer to the question MP-45's Session 0 owned more
deeply than any phase before it: **whether the post-record arc governs and,
if it does, what the fourth post-record question was.** The fifteenth
question is the second one I choose with the third-generation arc consumption
*stamped* — or the fifth question past the record's closing sentence.

### What I found walking the shelf while drafting (five dated intake facts, re-verified)

Drafted and re-verified against the repository on 2026-08-17. These are the
facts the hostile-webmaster walk would catch — MP-45's dated intake, walked
again, each cell stamped with its 2026-08-17 state so the intake is a
re-verification, never a memory:

1. **MP-45's roadmap is merged.** Verified: local `main` sits at `5308c9d` =
   `origin/main` (the MP-45 squash, PR #79, merged 2026-08-17) and `dev` at
   `34f82e8` (the reconcile merge that carried the squash into dev). MP-45's
   intake fact #1 is **RESOLVED** — the MP-45 merge itself closed it;
   Session 1's walk re-verifies with the branch list as the transcript.
2. **`portfolio/README.md` is still stale.** Re-verified: it still reads
   "Mini-paper (LaTeX PDF) not yet written", "Interactive demo … not built
   yet", "Experiment tracking … not set up yet" — contradicted by the
   record: the paper has lived through the v8–v14 arc, the site and Space
   have been live since the premiere, and the manifest machinery has been
   tracking results since Micro-Phase 8. MP-45's Session 1 owns the dated
   fix; this phase's Session 1 re-verifies the closure with the dated file
   itself.
3. **No `essay-annex-*.md` exists on disk.** Re-verified: `portfolio/`
   holds `RESULTS.md`, `README.md` and `model-card.md` and nothing else.
   The annexes live on the live shelf (site and Space), not in this
   repository. The v16 annex contract must state the artifact's home with a
   date instead of implying the repo holds it.
4. **Rung 6 residue still survives on disk.** Re-verified: the deleted
   Rung 6 (2026-08-01, fabricated data) left
   `src/experiments/__pycache__/exp6_automated_circuit.cpython-312.pyc` and
   `figures/exp6_automated_vs_manual.png` in the gitignored directories
   (both confirmed present 2026-08-17). MP-45's Session 1 owns the removal
   with a transcript; this phase re-verifies the absence.
5. **`checklists/gate-debt.md` still does not exist.** Re-verified:
   `checklists/` holds `reproducibility-checklist.md` and nothing else. The
   debt ledger is promised by named MP-30/31 rows; row 8's re-verification
   must record its absence with a date rather than claim a file that is not
   there.

One further verified shelf fact, carried from MP-45's sitting: **`figures/`
holds zero tracked files** — the entire showcase corpus is gitignored build
product, regenerated by `make reproduce` and provenanced by the manifests,
never by git. The 2026-08-17 walk confirmed `git ls-files figures/` is empty
while `portfolio/figures/` holds the twelve tracked figures; the provenance
story lives in `src/results.py`, and that is exactly where the
hostile-webmaster walk verifies it.

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no
phase. MP-37 through MP-45 are the un-cap's roadmap drafts executed exactly
once each — their drafts and reviews on disk, conditioned on their
predecessors' releases. **ADR-0019's eight rows are the rows MP-45 will
fill**; **ADR-0020's eight rows are the rows this roadmap will fill** —
exactly once, under the continuum law, fifteenth execution, written from
MP-45's release report rather than from the habit of pre-registering.

### The CI floor and the toolchains

190 tracked tests, ruff, blocking mypy and markdownlint are green at the
last release; `verify-claims` at 0 — re-verified in this drafting sitting
(2026-08-17): 190 collected, ruff clean, blocking mypy clean on
`src/results.py` + `src/experiments/runner.py`, `verify-claims` at 0, and
the full pytest suite passed 190/190 with coverage in the local CI mirror.
The verified gaps, stated as facts not hopes: no LaTeX toolchain on this
machine (`make paper` is graceful, not green), no Pages deploy workflow in
`.github/workflows/`, no `publish:` frontmatter policy, `portfolio/projects/`
holds figures but no project write-ups, W&B never connected. Each is a dated
row owned by MP-30/31/34/35/36 — their residue, never my re-planning.

### The showcase corpus at intake

12+ provenance-guarded figures, the paper through the v15 arc (the v16 rule
is this phase's), the site and Space live since the premiere, the essay
annex through the v15 arc, fourteen runnable teaching artifacts with
stranger-run transcripts (the receipts land only if the stack ships: the
fourteenth ships in MP-45, **the fifteenth in this phase**). My teaching
lane ships the fifteenth artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The intake is now a consumption of a consumption of a consumption of a
   consumption of a consumption.** MP-40's Ex-N defined the terminal state;
   MP-41's Session 0 executed it; MP-42's Session 0 consumed that execution
   and chose; MP-43's Session 0 consumed that choice with dates; MP-44's
   Session 0 consumed that decision and adjudicated C49–C52 or continued the
   post-record arc; MP-45's Session 0 consumed that decision with dates.
   MP-46's Session 0 must **consume MP-45's Session-0 decision with dates** —
   the single most dangerous drift is re-litigating a four-times-consumed
   decision: re-opening candidates the fourteenth question already closed
   with dated reasons, or treating "the post-record arc governs" as a mood
   instead of as a stamped verdict. The decision chain is now six generations
   deep; a sitting stamps, it never re-decides.
2. **The stacked execution is still the critical path.** MP-46's Session 0
   consumes MP-45's release report, which consumes ADR-0019's, which awaits
   MP-29 through MP-40. A slip at any link slides the whole chain; **my
   highest-leverage act is unchanged: protect MP-29's window** — its release
   report is the artifact everything downstream consumes. Nothing in this
   phase may borrow a minute from it, and this draft is written
   verdict-agnostic by law: it re-plans not a single row of MP-29–MP-45.
3. **The steady state is the un-cap's end state, and it must not become
   ceremony.** MP-46 is the ninth roadmap written from an *executed*
   roadmap's release report — the program's normal, confirmed nine times.
   The drift risk inverts and deepens: the machinery (ledgers, sessions,
   gate criteria) is now fifteen executions deep, so the law's
   countermeasure is that rows must still be dated in the sitting that owns
   them, verdicts still consumed as artifacts, and zero UNDECIDED rows at
   Session 8 — the machinery is the guardrail, never the goal, and a
   stamped row with no science behind it is ceremony by another name.
4. **The paper's compile gate is the hardest artifact in the stack.** No TeX
   on this machine — verified again in this sitting; MP-31's own canon
   applies early: *toolchains are pinned in Session 0, never discovered at
   Session 7.* The paper v16 rule ("opens only for new numbers, else the
   v15 is the record") is my insurance — a dated sentence, never a silence.
5. **The standing debt is undated by design and must not survive the
   stack.** exp5 1000-epoch ×3-seed (~15 h), clean-clone proof, graduation
   proof, `reproduce-multiseed`, W&B, the gate-debt transcript — each owned
   by a named row in MP-30–MP-36 and re-verified in MP-37's through MP-45's
   row 8. Row 8 of this phase re-verifies those closures with transcripts;
   a pending item cannot outlive a ledger — and a re-verification cannot
   claim a file that is not there (`gate-debt.md`'s absence is a dated
   fact, not a silence).
6. **The science's next fork is one verdict deeper.** MP-45 adjudicates
   C53–C56 — or continues the post-record arc — from ADR-0018's verdicts;
   MP-46's candidate set is conditioned on *that* verdict — C57 opens only
   on C53's positive reading, C58 only on C54's named driver, C59 only on
   C55's dated fourth drift, C60 only on C56's measured second cohort — and
   the post-record continuation overrides the set if MP-45's Session 0
   continued the arc. The redemption (a sparse cell found anywhere)
   overrides both. My candidate set is frozen precisely so this fork is
   adjudicated at Session 0, never improvised.
7. **The showcase's receipts are still future, one deeper.** The fifteenth
   stranger-run transcript lands only if the lanes execute; C59 (the rate
   as a function) is conditioned on ≥ 15 transcripts on disk at Session 0 —
   the receipt compounds only if the lanes execute.
8. **Stop-and-publish is a row, not a threat — and the post-record
   criterion is now five questions deep.** ADR-0004's row 5 (the record
   releases as-is) stays open as the program's honest exit: a phase is
   worth doing only if its candidate set can earn a paragraph the record
   does not already have. Every candidate below must beat that row in the
   sitting that chooses it. The fifteenth execution sharpens this to its
   edge: if MP-45's Session 0 continued the post-record arc, the deepest
   candidate this phase can choose is the one that earns the post-record
   arc's *fourth new paragraph* — the record's closing sentence consumed
   five times, never repeated. The deepest form of laziness is not
   building what the record has already said.

## Part III — The roadmap, step by step (the continuum law, fifteenth execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C57 | **The boundary's mechanism as a law** (C53's successor) — the root-caused boundary *made predictive*: the per-head failure mechanism written as a quantitative statement (which head roles fail first, in what order, under what norm budget), the failure cells patched and predicted at a *third* unseen task family before any number is read, the domain-of-validity statement upgraded from mechanism to law — a mechanism that predicts is a law; a mechanism that explains its one break is a diagnosis, and the diagnosis is the result | ADR-0019 row 3 = C53 with a positive verdict (boundary fingerprints and causal tracing on disk) | C53 closed negative, or the post-record arc governs → the mechanism's successor belongs to the post-record arc, or the record already has its closing sentence |
| C58 | **The driver across the diagram** (C54's successor) — the root-caused driver *generalized*: the loss-landscape → weight-norm → sharpening chain re-verified at unseen cells across the full P×wd diagram and across two architecture families, each link ablated, the ablation signature surviving or failing with a dated map of where it breaks — a driver that predicts across the diagram is a principle; a driver verified on one cell is a case study, and the case study is the result | ADR-0019 row 3 = C54 with the driver named and causally verified on disk | C54 never opened, or its verdict was negative → no principle to generalize, this closes with that verdict |
| C59 | **The rate as a function** (C55's successor) — the ninth reproducibility study: the fourth drift measurement after the dated root-cause fix, the receipt system's rate written as a function of codebase age and harness change, the attribution table's predictions tested against the ninth round's outcomes — a rate that explains its own aging is a model; a rate measured without cause is a statistic, and the statistic is the result | ADR-0019 row 3 = C55 with the fourth measurement and attribution on disk AND ≥ 15 stranger-run transcripts at S0 | Fewer than 15 transcripts, or C55 never opened → the receipt system hasn't earned a ninth study |
| C60 | **The course as an instrument** (C56's successor) — the second-edition course *validated externally*: the measured curriculum run by a third cohort the program did not choose, the feedback-to-fixes matrix's predictions checked against that cohort's friction, the verdict a curriculum with three measured cohorts — a course validated by the uninvited is an instrument; a course re-measured by the author is a poster | ADR-0019 row 3 = C56 with the second cohort's measured outcome on disk | C56 never opened, or a sparse regime exists → the sparse reading owns the question |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥
3 checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The terminal-state override stands, now six generations deep: **if MP-45's
Session 0 consumed MP-44's decision with dates and the post-record arc
governs, then MP-46's Session 0 consumes the fourth post-record question's
verdict from ADR-0019 row 3 and continues the post-record arc, choosing the
fifth post-record question from the pre-registered continuation set below.**
The rule is executed with dates at Session 0; it is never improvised and
never re-negotiated in the sitting that consumes it.

### The post-record continuation set (chosen only if MP-45 continued the post-record arc)

| # | Candidate | Why it would open | Why it would close |
|---|---|---|---|
| PR-13 | **The new harness's first cross-recipe check** (PR-10's successor) — the second recipe at the new address replicated across seeds, now *compared* to the first under the record's laws: the dense law's parameters transfer or diverge with dates, the verdict read from fresh manifests — two recipes replicated across seeds is the harness's first comparison datum; a recipe run once is an anecdote | The post-record arc continued at MP-45 with PR-10's verdict on disk | The record never closed, or the redemption fired first → the sparse question belongs to the old arc |
| PR-14 | **The law at the record's edge, fifth task** (PR-11's successor) — the frozen-checkpoint predictions tested at the fifth unseen task family: a law that predicts five times is a law with a measured domain; a law that breaks is a boundary with a map | The post-record arc continued at MP-45 with PR-11's verdict on disk | The record never closed → the law's successors are C57's, not the post-record arc's |
| PR-15 | **The record as a course, fourth edition** (PR-12's successor) — the third edition revised from its second intake: the feedback-to-fixes matrix executed with dates, the fourteen runnable artifacts assembled, the fourth edition measured as a learning instrument with three cohorts — a course revised from its receipts three times is a curriculum; a course re-shown is a poster | The post-record arc continued at MP-45 with PR-12's verdict on disk | The record never closed → the teaching lane continues as the continuum's row 8 |

The likely survivor, written as a condition chain, never a prediction: if
MP-45's Session 0 continued the post-record arc → **the post-record
continuation** — the fifth question past the record, chosen in the consuming
sitting from PR-13/PR-14/PR-15; else if C53 landed positive → **C57** — the
boundary's mechanism as a law, always CPU-runnable on checkpoints that exist
today; else if C54's driver verdict landed → **C58**; else **C59**
(always-runnable, the showcase's own science, receipts now fifteen deep);
C60 is the evidence lane and the teaching lane's anchor.

### The nine sessions

1. **Session 0 (~1 h) — the gate truthing + the five-generations-deep arc +
   the continuum choice.** Consume MP-45's release report row by row:
   ADR-0019 at zero UNDECIDED rows, the live URL re-clicked in the sitting,
   `verify-claims` at its actual count, the fourteenth teaching transcript on
   disk, `dev == main`. Commit the intake table before a single continuum
   row opens. Then **Ex-R: consume MP-45's Session-0 decision with dates** —
   the fifth-generation consumption: if the post-record arc continued, the
   fourth post-record question's verdict is read from ADR-0019 row 3 and the
   fifth post-record question chosen from the pre-registered continuation
   set (PR-13/PR-14/PR-15), each opening-or-closure memo in three sentences
   with a falsifier; if not, the C57–C60 adjudication: exactly one opens as
   row 3, the unchosen close with one dated reason each, stamped in the same
   sitting. Open ADR-0020 with its eight rows, windows and kill-dates;
   declare the terminus (release = merge + 14 calendar days); promote this
   roadmap from MP-45's release report, deviations recorded as dated ledger
   notes. *Exit: intake signed; the five-generations-deep arc stamped; row 3
   chosen (or the post-record continuation row opened); ledger open.*
2. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — extended to the repo's own shelf: local `main`
   re-verified reconciled to `origin/main` (branch list as the transcript),
   `portfolio/README.md`'s staleness verified closed (MP-45's Session 1
   owned the first fix; this sitting verifies the file is current), the
   exp6 residue removed with a transcript, the annexes' location verified.
   Row 8: MP-45's stamped closures re-verified (W&B, clean-clone proof,
   graduation proof, `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch
   resolution, the README fix, the residue removal) — each cell
   LAUNCHED-with-transcript or CLOSED-with-one-reason; a claimed closure
   without its transcript stays open and blocks Session 8; `gate-debt.md`'s
   absence, if still absent, recorded with a date. *Exit: rows 5 and 8
   stamped.*
3. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the fourteenth research question's verdict (ADR-0019 row 3) becomes the
   paper-v16 section, the annex table, or the results-page row — every
   number manifest-tagged, consumed in the sitting that owns it; if the
   post-record arc governs, the post-record statement is framed from
   MP-45's release, never rewritten. Row 2: v16 opens only if row 1 lands
   new numbers; else "the v15 is the record" is the dated reason and `make
   paper` is re-verified against v15. Row 6's substitute filed from the
   visitor's chair, before the window opens (Ex-G); the fork drill (Ex-H)
   and the arc consumption (Ex-N, Ex-O, Ex-P, Ex-R) land here. *Exit: rows 1
   and 2 dated; substitute filed; Ex-R's execution memo on disk.*
4. **Session 3 (~2–3 h) — the essay annex v16.** `portfolio/essay-annex-16.md`
   (its home on the live shelf, dated): the fourteenth question's verdict set
   and the teaching lane's fourteenth receipt distilled into one dated annex;
   the reverse claims audit at zero (prose → manifest → command); each
   claim's "what would falsify this" column filled at writing time. The
   annex is amended, never rewritten. *Exit: row 4 dated; audit at zero.*
5. **Session 4 (~1 h) — the stranger round 16 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. *Exit: window open,
   kill-date declared.*
6. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat — or, if the post-record
   arc governs, the continuation row's protocol opened under the same
   discipline. If C57: the failure cells at the third unseen task family and
   the expected per-head mechanism written as falsifiable predictions before
   a single number is read (Ex-C, Ex-I, Ex-J, Ex-S). Row 6's kill-date
   honored (feedback → matrix drafted; silence → substitute closes it).
   Row 7: the fifteenth teaching artifact's skeleton drafted — walkthrough
   v15, 10-minute talk v15, or Colab grokking notebook v13 — with its
   ship-date. *Exit: row 3 pre-registered and launched (or the post-record
   protocol opened); row 6 dated either way; row 7's skeleton drafted.*
7. **Session 6 (~1–2 h) — the research verdict sitting.** Row 3's verdict
   read from the manifest: completed and dated, or window closed and the
   scheduled negative is the result — drafted while the run was live
   (Ex-D), so this sitting is a stamping, not a discovery. *Exit: row 3
   dated either way.*
8. **Session 7 (~2–3 h) — the shelf rehearsal + the re-check row + the
   teaching polish.** Row 5: the hostile-webmaster walk at zero beside the
   browser, every public number clicked back to disk; the repo-shelf
   findings re-checked (local `main` reconciled, README current, residue
   gone, annexes' home verified). Row 6's re-check row dated. Row 7: the
   fifteenth artifact runs end to end on a stranger's machine (fresh
   clone / Colab session); the run transcript is the receipt; the teaching
   distillation (Ex-F) lands here. *Exit: rows 5, 6, 7 dated; the artifact
   shipped with its transcript.*
9. **Session 8 (~1 h) — the release.** ADR-0020 at zero UNDECIDED rows; the
   merge green locally and on GitHub; `dev == main`; home wired — this
   roadmap's companion status retired; the roadmap archived with its
   deviations, every deviation a dated ledger note. If the post-record arc
   governs, this sitting stamps the post-record arc's fifth dated
   direction — the record's closing sentence consumed five times, never
   repeated. *Exit: the merge; the program's fifteenth dated direction —
   or the post-record arc's fifth.*

### The one measured line

ADR-0020 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row (or the post-record continuation row) whose verdict (or
scheduled negative) re-derives from a manifest; `verify-claims` at 0 with
every public number re-derivable from one command line; the hostile-webmaster
walk at zero on the live shelf and on the repo's own shelf (local `main`
reconciled, README current, residue removed, the debt ledger present or
absent-with-date); the fifteenth teaching artifact shipped with a
stranger-runnable transcript; `dev == main` and the program's fifteenth
dated direction — or, if the post-record arc governs, its fifth dated
direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk.

1. **The mechanism as a law (the C57 reading).** Elhage et al.,
   *A Mathematical Framework for Transformer Circuits* (2021) for the
   QK/OV machinery the causal claim is made over; Wang et al.,
   *Interpretability in the Wild* (2022) for activation-patching methodology
   at per-head resolution; Conmy et al., *Towards Automated Circuit
   Discovery* (2023) for turning a hand-traced mechanism into a scalable,
   testable procedure; Varma et al., *Explaining grokking through circuit
   efficiency* (2023) for why circuits grow sharp and where that sharpness
   is measurable; Olsson et al., *In-context Learning and Induction Heads*
   (2022) for what transfers across task families — now read at the
   *prediction* axis: what it takes to convert a root-caused boundary into a
   falsifiable law with out-of-sample teeth at a *third* unseen task family,
   and where mechanism claims over dense circuits have been shown to
   overreach. My C53 verdict and its boundary fingerprints frame the
   reading. **Prediction to write before the analysis**: which per-head
   roles fail first at the third unseen task's structure, and what the
   patching at those cells reveals; the null hypothesis every measured
   fingerprint is compared against. **Primary sources**: the frozen
   checkpoints, C53's boundary-fingerprint table, the S3 note.
2. **The driver across the diagram (the C58 reading).** Lyu et al.,
   *Understanding the training dynamics of transformers on modular
   arithmetic* (2024) for the loss-landscape structure of grokking and its
   phase transitions; Morwani et al. (2024) on the edge-of-numerical-
   stability regime; Gromov, *Grokking: A Memory Perspective* (2023);
   Power et al. (2022); Nanda et al. (2023) — now read at the
   *generalization* axis: whether the loss-landscape → weight-norm →
   sharpening chain survives ablation across the full P×wd diagram and
   across two architecture families, what a dated negative at any link
   means for the driver, and where "the driver" is really an optimization
   artifact that does not survive the second family. **Prediction**: the
   order-parameter dynamics at unseen cells with the causal chain's expected
   ablation signature written before the analysis; C54's named driver is
   this reading's admission ticket.
3. **The rate as a function (the C59 reading).** Gelman & Loken, *The Garden
   of Forking Paths*; Pineau et al. (2021); Kapoor & Narayanan,
   *Reproducibility in Machine Learning: A Systematic Literature Review*
   (2023); the ML reproducibility line (NASEM's five pillars) — now read at
   the *modeling* axis: what a reproducibility rate *as a function of
   codebase age and harness change* claims, how the fourth drift measurement
   after the dated fix tests the attribution table, and what a ninth study
   can honestly say that an eighth could not. My fifteen stranger-run
   transcripts are the data; the eighth study defined the fourth drift, I
   must decide what counts as the ninth measurement before I measure any.
4. **The course as an instrument (the C60 reading).** Bricken et al.
   (2023); Cunningham et al. (2024); the dictionary-circuit and
   feature-universality line — plus the education-measurement line (rubric
   validity, test-retest reliability, external assessment) for what a
   *third, uninvited cohort's* outcome claims that two author-chosen
   cohorts' do not. My Rung-5 datum (99.97% FVE, L0 = 136/256, 0% dead
   features), C56's second-edition course and its measured outcome are the
   record's first data points.
5. **The post-record program, fifth generation (new, deepest).** Lakatos,
   *The Methodology of Scientific Research Programmes* (1978) — read a sixth
   time, now for the *fifth* question past a completed program: progressive
   vs degenerating problem shifts when the *fourth* post-record verdict
   lands, Kuhn's normal science as the post-record arc's axioms, and the
   honest criterion for the fifth post-record question — a question that
   must earn the post-record arc's fourth *new* paragraph. This reading feeds
   Ex-R and the Session-0 question MP-46 owns more deeply than any phase
   before it: *what does the record's fourth post-record verdict open?* The
   answer can be the post-record arc's fifth dated row — Lakatos' point is
   that the decision is made on the record, never as a mood.
6. **The record teaches, round fifteen.** The fifteenth verdict in four
   registers — the paper's sentence, the annex's sentence, the 30-second
   spoken claim, and the 5-minute teaching explanation with a worked toy a
   stranger can run; the gap between the last two is where my teaching
   leaks, and I will measure it deliberately by writing all four registers
   for the same verdict (Ex-F).
7. **The redemption reading, or negative results as maps, the fifteenth
   pass.** If a sparse cell exists by S0: Nanda et al.'s full per-frequency
   reading on the first sparse solution this harness ever produced. If not:
   how the *completed* law is reported honestly — the mechanism's law traced
   at its own edge, the driver a principle or a case study with a dated map,
   the drift numbers five deep, the negative as a contribution — and how
   the post-record harness (if PR-13 governs) would be designed from the
   dated negatives instead of from hope. Either way, the paper's hardest
   paragraph is the one that claims the dense solution *computes something*;
   I will draft it against this reading and let the manifest referee it.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-45's release report, deviations recorded as dated ledger
  notes.
- **ADR-0020**, the fifteenth continuum ledger — eight rows pre-stamped
  with windows and kill-dates; rows 1–2 consumed from ADR-0019's verdicts;
  row 3 the fifteenth research question with its protocol note and
  heartbeat (or the post-record continuation row's protocol); rows 4–8 the
  continuum's decisions.
- **`portfolio/essay-annex-16.md`** — the v16 annex, manifest-tagged,
  amended never rewritten; the annexes' home (the live shelf) recorded with
  a date.
- **The paper v16 diff** (`portfolio/paper/main.tex` v16 + diff log) or the
  dated "the v15 is the record" memo; `make paper` re-verified in the CI
  mirror.
- **The shelf health sheet + hostile-webmaster transcript** (site + Space at
  zero), extended to the repo's own shelf: local `main` reconciled to
  `origin/main`, `portfolio/README.md` current, the exp6 residue removed,
  the annexes' location verified; the claims gate re-run on every merge.
- **`checklists/gate-debt.md`** — each cell's transcript or one-line reason,
  dated in Session 1, including the exp5 1000-epoch resolution's receipt
  re-checked; the file's absence, if still absent, recorded with a date.
- **The research row's pre-registration note** (site, metric, negative
  control, kill-date) in `06_production_ai/notes/` + the heartbeat artifact;
  if C57: the mechanism-law figure spec written before the analysis, the
  figure itself manifest-tagged after. If the post-record arc governs:
  the continuation row's protocol note instead.
- **The fifteenth teaching artifact + its stranger-run transcript**
  (fresh-clone or Colab session receipt).
- **Ex-R's execution memo** — MP-45's arc decision run with dates: the
  post-record verdict consumed or the C57–C60 adjudication executed, the
  criteria cited, the decision that follows (the fifth post-record question,
  or the continuation), written verdict-agnostic in Session 2 and executed
  at Session 0.
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C57–C60 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting — preceded by the arc consumption (Ex-N, Ex-O, Ex-P, Ex-R),
   which may make the whole set close with the post-record verdict.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0019's row-3 verdict traced to its manifest and its command; the
   rest struck with a reason — the hostile-webmaster test of my own prose,
   fourteenth run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C57 or C58 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the failure cells and the expected per-head mechanism at the
   third unseen task's structure, the driver's predicted order-parameter
   dynamics at unseen cells with its ablation signature — the "what would
   falsify this" column filled at writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v16 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, with the repo's own shelf added: branches reconciled, README
   current, residue removed.
6. **Ex-F · The teaching distillation, round fifteen (S7):** the fifteenth
   question's verdict in four registers — the paper's sentence, the annex's
   sentence, the 30-second spoken claim, the 5-minute teaching explanation
   with a worked toy a stranger can run; the gap between the last two is
   where my teaching leaks.
7. **Ex-G · The stranger substitute from the visitor's chair (S2):** the
   self-review written from the chair a stranger would occupy — friction
   points → fixes → re-check row — filed before S4, so the S5 kill-date can
   never close the row with a skip.
8. **Ex-H · The fork drill, deepest form (S2, verdict-agnostic):** the
   continuing state (C57–C60) vs the post-record state (PR-13/PR-14/PR-15)
   written as two one-page paths — what each verdict changes downstream,
   including the C57-vs-C58 choice and the post-record continuation choice —
   so next phase's S0 decision is a stamping, not a discovery.
9. **Ex-I · The boundary hand-roll, round four (S5, C57 only, before any
   number is read):** the expected per-head mechanism at the third unseen
   task's failure cells written by hand from C53's mechanism — which per-head
   roles must transfer unchanged, which may re-tune, which should fail
   first, and what patching at those cells should reveal — the null
   hypothesis every measured fingerprint is compared against. One runnable
   check: the hand-rolled fingerprints printed and saved next to Ex-J's
   observed ones, so the S6 comparison is a diff, not a memory.
10. **Ex-J · The transfer reader, round four (S5, C57 only):** the script
    that loads the frozen checkpoints at every P (including the third
    unseen task's), runs C53's per-head extraction and patching machinery,
    and emits the failure-cell table as a manifest-tagged JSON. One
    runnable check: the reader runs on the frozen checkpoints and its
    output is committed before the verdict paragraph is drafted.
11. **Ex-K · The sparse-recovery toy, revisited a ninth time (my
    foundation challenge, generalization pass):** the one-file toy that
    recovers the addition table's DFT coefficients under L2 vs L1 penalties,
    now extended to the generalization question: *does the sharpening
    ablation signature survive across two architecture families and the
    full diagram, and where does it break?* One runnable check: the toy
    prints both reconstructions' sparsity and error plus the ablation table
    on a fixed seed, across two architectures. This is the micro-scale
    intuition C58's verdict must not contradict.
12. **Ex-L · The "what does the dense solution compute?" sprint, round
    nine (S5, C57 only):** the paper's hardest paragraph drafted at S5,
    then audited against the mechanism reading at S6 — prose that must
    survive contact with the manifest, the "computes something" claim
    earned or struck with one reason.
13. **Ex-M · The stranger-run drill on my own receipt (S1):** I execute the
    previous phase's shipped artifact (the fourteenth) on a fresh clone as
    if I were the stranger — the transcript becomes the baseline against
    which the fifteenth artifact's transcript is compared. One runnable
    check: the baseline transcript saved beside the new one.
14. **Ex-N · The arc consumption, second generation (S0):** MP-40's Ex-N
    defined the terminal state; MP-41 executed it; MP-42 consumed that
    execution and chose; MP-43 consumed that choice with dates; MP-44
    consumed that Session-0 decision; MP-45 consumed that decision with
    dates. This drill executes that second-generation consumption exactly
    as MP-45's memo stamped it.
15. **Ex-O · The arc consumption, third generation (S0):** MP-45's
    Session-0 decision becomes the object of the consumption — the fourth
    post-record question's verdict read from ADR-0019 row 3 if the arc
    governs, the criteria cited, the release that follows (the fifth
    post-record question, or the C57–C60 adjudication). One runnable check:
    the execution memo exists, names the decision rule, cites the criteria
    from MP-45's release report.
16. **Ex-P · The arc consumption, fourth generation (S0):** the consumption
    chain's deepest run as MP-45 stamped it — MP-44's decision consumed
    with dates, the criteria cited, the release that follows, and what each
    of ADR-0018's possible verdicts changed in that execution. One runnable
    check: the execution memo exists and cites the criteria from MP-44's
    release report.
17. **Ex-R · The arc consumption, fifth generation (S0, new,
    verdict-agnostic):** the consumption chain's deepest run — MP-45's
    Session-0 decision consumed with dates as MP-46's intake, the
    third-generation post-record verdict read from ADR-0019 row 3 if the
    arc governs, the criteria cited, the release that follows (the fifth
    post-record question, or the C57–C60 adjudication), and what each of
    ADR-0019's possible verdicts changes in that execution. One runnable
    check: the execution memo exists, names the decision rule that closes
    or continues the program's science, and cites the criteria from MP-45's
    release report — the chain now six generations deep, a sitting stamps,
    it never re-decides.
18. **Ex-S · The out-of-sample sprint (S5, C57 only, new):** the mechanism's
    predictions at the third unseen task family written as a dated table
    before any number is read — task family, expected failing head role,
    expected order of failure, expected patching signature — with the
    falsifier column filled at writing time; the observed table compared at
    S6 as a diff, not a memory.
19. **Ex-Q · The drift-attribution drill (S5, C59 only):** the fourth
    drift's components attributed before any fix — harness change vs
    protocol drift vs codebase aging — each component's contribution
    estimated from the fifteen transcripts, the top root-cause's fix dated
    in the same sitting. One runnable check: the attribution table saved
    beside the drift numbers, so the S6 verdict is a diff, not a memory.
20. **Habit · The clock check (every session):** ADR-0020's undated rows,
    the open PR's CI status line, the shelf's health — all three before
    any new prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, fifteenth execution.** A phase that opens two
  research questions is drift by another name; the unchosen candidates close
  in the same sitting as the choice — and the arc consumption may close all
  of them with the post-record verdict. The continuum law is the mechanical
  refusal of this drift — proven executable fourteen times, it must simply
  be executed again.
- **The candidate set is frozen before S0, never improvised at it.** C57–C60
  are conditions, not predictions; a sitting decides, it never invents — and
  the terminal-state object is the hardest frozen object on the record:
  written by MP-40, executed by MP-41, consumed by MP-42, consumed again by
  MP-43, consumed a third time by MP-44, consumed a fourth time by MP-45,
  *consumed a fifth time* by MP-46 — never re-negotiated in the consuming
  sitting.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0019's row-3 verdict in the sitting that owns
  it — or the post-record statement, if the arc governs.
- **The receipt compounds.** The fifteenth runnable artifact is only worth
  shipping because the first fourteen transcripts proved the format — and if
  C59 opens, the receipts are a drift-of-drift-of-drift-of-drift number
  measured four times in a row, tested by people I did not choose, across an
  aging codebase. My showcase's story is now "read it, run it, watch me be
  wrong on the record," fifteen receipts deep.
- **The steady state is the reward, not the ceremony.** MP-46 is the ninth
  roadmap written from an *executed* roadmap's release report — the program
  at its normal, confirmed nine times. The cap's lesson was that promises
  without dates drift; the steady state's discipline is that the machinery
  never becomes the goal: rows are dated in the sitting that owns them, or
  they are not rows.
- **Stop-and-publish stays open, and the post-record criterion is now five
  questions deep.** ADR-0004's row 5 is the honest exit; a candidate set
  that cannot earn a paragraph the record lacks is a phase that should close
  itself. If the post-record arc governs, the deepest candidate earns the
  post-record arc's *fourth new paragraph* — the record's closing sentence
  consumed five times, never repeated. This is the deepest form of
  laziness: do not build what the record has already said.
- **Toolchains are pinned in S0, never discovered at S7.** The paper's
  compile gate is the hardest artifact in the stack; the v16 rule ("opens
  only for new numbers") is the insurance that makes a missing toolchain a
  dated reason, not a crisis.
- **Protect the release report.** The serialized stack means MP-29's release
  is the artifact everything downstream consumes; a slip at any link slides
  the whole chain. The deepest law still applies: a promise can be
  re-planned forever, but a dated row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0019 at zero, the live
  URL, `verify-claims` at 0, the fourteenth teaching transcript on disk — a
  condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; the R1 no-head negative — 0/8
  heads, stamped 2026-08-14 — is the record's newest dated signature, and
  the chain I am building toward is the strongest form of the signature: a
  negative that became a map, a map that became a characterization, a
  characterization that became a mechanism, a mechanism that earned its
  causal verdict, a circuit that earned its complete reading, a circuit
  that earned its law, a law that predicted an unseen point, a boundary
  that earned its own second out-of-sample point, a boundary that earned its
  mechanism, a mechanism that earns its law — or a record that knew when to
  end.
- **The debt row re-verifies; it never re-does.** A stamped closure is
  re-checked with its transcript; a genuinely new debt cell is a NEW row,
  never a revision. A pending item cannot outlive a ledger — and a
  re-verification cannot claim a file that is not there.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED
  rows at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story:** *the program's fifteenth dated
  direction was written from its own release report — the cap honored, the
  stack executed, the steady state kept honest nine times, the record
  taught fifteen times in runnable artifacts, every public number still
  re-derives from one command line, and the record consumed — five times,
  with dates — its own terminal-state decision, and answered it in a
  release.* Every artifact this phase launches is written to that standard.

## Links

- [[00_meta/45_micro-phase-45-review-and-roadmap]] · [[00_meta/44_micro-phase-44-review-and-roadmap]] —
  the fourteenth question's review and roadmap; this roadmap's intake is
  ADR-0019's release report, the rows this review conditions on, and MP-45's
  Ex-P consumption of MP-44's Session-0 decision, which Session 0 consumes
  again.
- [[00_meta/43_micro-phase-43-review-and-roadmap]] · [[00_meta/42_micro-phase-42-review-and-roadmap]] —
  the twelfth and eleventh questions' reviews and roadmaps, the un-cap's
  steady state confirmed nine times.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat — and the
  row the terminal state executes.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/positive-control-protocol]] ·
  [[06_production_ai/notes/microscope-trial-table]] — the science C57–C60
  adjudicate over, whose pending verdicts are the intake.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.