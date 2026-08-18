---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-18
---

# Micro-Phase 49 — State Review and Roadmap: the eighteenth question, written from the seventeenth release report

> **STATUS: REVIEW + ROADMAP, NOT A PRE-REGISTRATION.** This note is the
> companion review to [[00_meta/48_micro-phase-48-review-and-roadmap]] and
> [[00_meta/48b_micro-phase-48-execution-roadmap]], the seventeenth question's
> review and roadmap: it opens no rows, launches no runs, claims no window,
> and is wired into home only as a companion pointer — it is not a
> pre-registration and it is not counted against any cap, because the cap is
> spent. It is my personal state review and my step-by-step plan for the phase
> that starts at MP-49's Session 0, written in the same first-person register
> as my progress log so it doubles as the public record of how I reasoned
> about the program's steady state while MP-48's waiting window was still
> open. Everything factual in this file was re-verified against the repository
> on 2026-08-18: working tree clean, local `main` reconciled to `origin/main`
> at `17c21a4` (the MP-48 execution-roadmap squash, PR #83), `dev` at
> `0812f7b` (the reconcile merge), `git diff main dev` empty, 190 tracked
> tests collected, ruff clean, blocking mypy clean, `verify-claims` at 0.

## Part I — Where I stand (state review, verified against the repo)

### The scientific ledger

The record's deepest fact has not changed and still has ten dated
confirmations behind it, re-verified in this drafting sitting: **no run in
this repository's history has ever produced a sparse Fourier solution.** The
count advances only with a new verdict; between MP-48's sitting and this one,
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
Session-0 decision open — or is the third post-record question the post-record
arc's own successor?* (MP-44's sitting) → *which of C53–C56 does the consumed
thirteenth verdict open — or is the fourth post-record question the post-record
arc's own successor?* (MP-45's sitting) → *which of C57–C60 does the consumed
fourteenth verdict open — or is the fifth post-record question the post-record
arc's own successor?* (MP-46's sitting) → *which of C61–C64 does the consumed
fifteenth verdict open — or is the sixth post-record question the post-record
arc's own successor?* (MP-47's sitting) → *which of C65–C68 does the
seventeenth question open — or is the seventh post-record question the
post-record arc's own successor?* (MP-48's sitting). By MP-49's Session 0 the
record will hold seventeen dated directions, a characterized dense regime, a
causal reading (or its evidence lane), whichever of C65–C68 ADR-0022's
sitting chose — and the answer to the question MP-48's Session 0 owns more
deeply than any phase before it: **whether the post-record arc governs and,
if it does, what the seventh post-record question was.** The eighteenth
question is the fifth I choose with the fifth-generation arc consumption
*stamped* — or the eighth question past the record's closing sentence.

### What I found walking the shelf while drafting (verified intake facts)

Drafted and re-verified against the repository on 2026-08-18 — the facts a
hostile-webmaster walk would catch, each stamped with its state in this
sitting so the intake is a re-verification, never a memory:

1. **MP-48's roadmaps are merged.** Verified: local `main` sits at `17c21a4`
   = `origin/main` (the MP-48 execution-roadmap squash, PR #83) with the
   review-and-roadmap merged ahead of it (PR #82, `2d3b238`), and `dev` at
   `0812f7b` (the reconcile merge); `git diff main dev` is empty. MP-48's own
   intake facts are closed by its merges; Session 1's walk re-verifies with
   the branch list as the transcript.
2. **`portfolio/README.md` is still stale.** Re-verified: it still reads
   "Mini-paper (LaTeX PDF) not yet written", "Interactive demo … not built
   yet", "Experiment tracking … not set up yet" — contradicted by the record:
   the paper has lived through the v8–v15 arc (the v16–v18 rules belong to
   MP-46/47/48), the site and Space have been live since the premiere, and
   the manifest machinery has been tracking results since Micro-Phase 8.
   MP-48's Session 1 owns the dated fix; this phase's Session 1 re-verifies
   the closure with the dated file itself.
3. **No `essay-annex-*.md` exists on disk.** Re-verified: `portfolio/` holds
   `RESULTS.md`, `README.md`, `model-card.md`, `paper/` and `projects/` and
   nothing else. The annexes live on the live shelf (site and Space), not in
   this repository. The v19 annex contract must state the artifact's home
   with a date instead of implying the repo holds it.
4. **Rung 6 residue still survives on disk.** Re-verified: the deleted
   Rung 6 (2026-08-01, fabricated data) left
   `src/experiments/__pycache__/exp6_automated_circuit.cpython-312.pyc` and
   `figures/exp6_automated_vs_manual.png` in the gitignored directories
   (both confirmed present 2026-08-18). MP-48's Session 1 owns the removal
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
phases' ledgers (ADR-0011 through ADR-0022) do not exist on disk because they
open at their own Session 0s; **ADR-0023's eight rows are the rows this
roadmap will fill**, and this phase's Session 0 opens it exactly once.

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no phase.
MP-37 through MP-47 are the un-cap's roadmap drafts executed exactly once
each — their drafts and reviews on disk, conditioned on their predecessors'
releases. **MP-48's review and execution roadmaps are merged, its Session −1
study lane owns the waiting window, and its Session 0 awaits the stack's
release.** **ADR-0022's eight rows are the rows MP-48 will fill**;
**ADR-0023's eight rows are the rows this roadmap will fill** — exactly once,
under the continuum law, eighteenth execution, written from MP-48's release
report rather than from the habit of pre-registering.

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
this phase's), the site and Space live since the premiere, the essay annex
through the v15 arc, seventeen runnable teaching artifacts with stranger-run
transcripts (the receipts land only if the stack ships: the seventeenth ships
in MP-48, **the eighteenth in this phase**). My teaching lane ships the
eighteenth artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The intake is a consumption nine generations deep.** MP-49's Session 0
   must **consume MP-48's Session-0 decision with dates** — the single most
   dangerous drift is re-litigating a decision already consumed eight times:
   re-opening candidates the seventeenth question already closed with dated
   reasons, or treating "the post-record arc governs" as a mood instead of as
   a stamped verdict. The decision chain is now nine generations deep; a
   sitting stamps, it never re-decides.
2. **The stacked execution is still the critical path — and its head is
   still MP-29.** MP-49's Session 0 consumes MP-48's release report, which
   awaits the stack. A slip at any link slides the whole chain; **my
   highest-leverage act is unchanged: protect MP-29's window** — its release
   report is the artifact everything downstream consumes. Nothing in this
   phase may borrow a minute from it, and this draft is written
   verdict-agnostic by law: it re-plans not a single row of MP-29 through
   MP-48.
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
6. **The steady state must not become ceremony.** MP-49 will be the twelfth
   roadmap written from an *executed* roadmap's release report — the
   program's normal, confirmed eleven times. The countermeasure is concrete:
   **every session's exit names at least one artifact changed on disk, and
   every row is dated in the sitting that owns it** — a stamped row with no
   science behind it is ceremony by another name.
7. **The paper's compile gate is the hardest artifact in the stack.** No TeX
   on this machine — verified again in this sitting. The v19 rule ("opens
   only for new numbers, else the v18 is the record") is my insurance; the
   toolchain decision (local MiKTeX/TeX Live vs. Overleaf) is pinned at
   Session 0, never discovered at Session 7.
8. **Stop-and-publish is a row, not a threat — and the post-record criterion
   is now eight questions deep.** ADR-0004's row 5 stays open as the
   program's honest exit: a phase is worth doing only if its candidate set
   can earn a paragraph the record does not already have. If MP-48's Session
   0 continued the post-record arc, the deepest candidate this phase can
   choose earns the post-record arc's *seventh new paragraph* — the record's
   closing sentence consumed eight times, never repeated. The deepest form
   of laziness is building what the record has already said.

## Part III — The roadmap, step by step (the continuum law, eighteenth execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C69 | **The theory's second prediction** (C65's successor) — the failure-cell theory *predicted again*: the per-head mechanism at the third unseen task family's and the third architecture family's failure cells written as falsifiable predictions before any number is read, causally verified by patching, the theory's domain statement extended from "explains its measured cells" to "predicts unseen cells twice" — a theory that predicts twice is a predictive theory; a theory that predicted once is a result with a prediction, and the result is on the record | ADR-0022 row 3 = C65 with a positive verdict (the law with its theory of failure on disk) | C65 closed negative, or the post-record arc governs → the theory's second round belongs to the post-record arc |
| C70 | **The exception map as a boundary law** (C66's successor) — the full P×wd diagram *closed*: a dated root-cause mechanism for every cell of both architecture families, each exception ablated, the break-map completed with no cell left unmapped — a complete exception map is the law's boundary; a partial map is a case study, and the case study is the result | ADR-0022 row 3 = C66 with the exception map on disk | C66 never opened, or its verdict was negative → no map to complete |
| C71 | **The policy as discipline** (C67's successor) — the twelfth reproducibility study: the seventh drift measurement after the sixth dated fix, the rate function's parameters re-estimated from the receipt system's history, and the policy *enforced* across the stack's own execution window — a policy that survives its own enforcement is a discipline; a policy that predicts is a model, and the model is the result | ADR-0022 row 3 = C67 with the sixth measurement and attribution on disk AND ≥ 18 stranger-run transcripts at S0 | Fewer than 18 transcripts, or C67 never opened → the receipt system hasn't earned a twelfth study |
| C72 | **The instrument as a public good** (C68's successor) — the fourth-edition course *validated a fourth time by the uninvited* and the rubric *released as a standalone artifact others can run*: the scoring rule published, the feedback-to-fixes matrix's third prediction round checked against the fourth cohort's friction — an instrument others can run is a standard; an instrument validated thrice is a strong observation, and the observation is the result | ADR-0022 row 3 = C68 with the fifth cohort's measured outcome on disk | C68 never opened, or a sparse regime exists → the sparse reading owns the question |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥
3 checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The terminal-state override stands, now nine generations deep: **if MP-48's
Session 0 consumed MP-47's decision with dates and the post-record arc
governs, then MP-49's Session 0 consumes the seventh post-record question's
verdict from ADR-0022 row 3 and continues the post-record arc, choosing the
eighth post-record question from the pre-registered continuation set below.**
The rule is executed with dates at Session 0; it is never improvised and
never re-negotiated in the sitting that consumes it.

### The post-record continuation set (chosen only if MP-48 continued the post-record arc)

| # | Candidate | Why it would open | Why it would close |
|---|---|---|---|
| PR-22 | **The new harness's third cross-recipe law** (PR-19's successor) — the *fifth* recipe at the new address replicated across seeds and compared to the first four under the record's laws: five recipes compared across seeds is the harness's third law datum; four recipes compared once is a second datum, and the datum is the result | The post-record arc continued at MP-48 with PR-19's verdict on disk | The record never closed, or the redemption fired first → the sparse question belongs to the old arc |
| PR-23 | **The law at the record's edge, eighth task** (PR-20's successor) — the frozen-checkpoint predictions tested at the eighth unseen task family: a law that predicts eight times is a law with a predictive record; a law that breaks is a boundary with a map | The post-record arc continued at MP-48 with PR-20's verdict on disk | The record never closed → the law's successors are C69's, not the post-record arc's |
| PR-24 | **The record as a course, seventh edition** (PR-21's successor) — the sixth edition revised from its fifth intake: the feedback-to-fixes matrix executed with dates, the eighteen runnable artifacts assembled, the seventh edition measured as a learning instrument with six cohorts — a course revised from its receipts six times is a curriculum; a course re-shown is a poster | The post-record arc continued at MP-48 with PR-21's verdict on disk | The record never closed → the teaching lane continues as the continuum's row 8 |

The likely survivor, written as a condition chain, never a prediction: if
MP-48's Session 0 continued the post-record arc → **the post-record
continuation** — the eighth question past the record, chosen in the consuming
sitting from PR-22/PR-23/PR-24; else if C65 landed positive → **C69** — the
theory's second prediction, always CPU-runnable on checkpoints that exist
today; else if C66's exception map landed → **C70**; else **C71**
(always-runnable, the showcase's own science, receipts now eighteen deep);
C72 is the evidence lane and the teaching lane's anchor.

### The nine sessions

1. **Session 0 (~1 h) — the gate truthing + the eight-generations-deep arc +
   the continuum choice.** Consume MP-48's release report row by row:
   ADR-0022 at zero UNDECIDED rows, the live URL re-clicked in the sitting,
   `verify-claims` at its actual count, the seventeenth teaching transcript
   on disk, `dev == main` (branch list as the transcript). Commit the intake
   table before a single continuum row opens. Then **Ex-T2: consume MP-48's
   Session-0 decision with dates** — the eighth-generation consumption: if
   the post-record arc continued, the seventh post-record question's verdict
   is read from ADR-0022 row 3 and the eighth post-record question chosen
   from the pre-registered continuation set (PR-22/PR-23/PR-24), each
   opening-or-closure memo in three sentences with a falsifier; if not, the
   C69–C72 adjudication: exactly one opens as row 3, the unchosen close with
   one dated reason each, stamped in the same sitting. Open ADR-0023 with its
   eight rows, windows and kill-dates; declare the terminus (release = merge + 14 calendar days);
   promote this roadmap from MP-48's release report, deviations recorded as
   dated ledger notes. **The toolchain decision is pinned here** (TeX choice;
   `make paper` re-verified in the CI mirror). *Exit: intake signed; the
   eight-generations-deep arc stamped; row 3 chosen (or the post-record
   continuation row opened); ledger open.*
2. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — extended to the repo's own shelf: local `main`
   re-verified reconciled to `origin/main` (branch list as the transcript),
   `portfolio/README.md`'s staleness verified closed (MP-48's Session 1 owned
   the first fix; this sitting verifies the file is current), the exp6
   residue removed with a transcript, the annexes' location verified. Row 8:
   MP-48's stamped closures re-verified (W&B, clean-clone proof, graduation
   proof, `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch resolution,
   the README fix, the residue removal) — each cell LAUNCHED-with-transcript
   or CLOSED-with-one-reason; a claimed closure without its transcript stays
   open and blocks Session 8; `gate-debt.md`'s absence, if still absent,
   recorded with a date. *Exit: rows 5 and 8 stamped.*
3. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the seventeenth research question's verdict (ADR-0022 row 3) becomes the
   paper-v19 section, the annex table, or the results-page row — every number
   manifest-tagged, consumed in the sitting that owns it; if the post-record
   arc governs, the post-record statement is framed from MP-48's release,
   never rewritten. Row 2: v19 opens only if row 1 lands new numbers; else
   "the v18 is the record" is the dated reason and `make paper` is re-verified
   against v18. Row 6's substitute filed from the visitor's chair, before the
   window opens (Ex-G); the fork drill (Ex-H) and the arc consumption (Ex-N
   through Ex-T2) land here. *Exit: rows 1 and 2 dated; substitute filed;
   Ex-T2's execution memo on disk.*
4. **Session 3 (~2–3 h) — the essay annex v19.** `portfolio/essay-annex-19.md`
   (its home on the live shelf, dated): the seventeenth question's verdict set
   and the teaching lane's seventeenth receipt distilled into one dated annex;
   the reverse claims audit at zero (prose → manifest → command); each
   claim's "what would falsify this" column filled at writing time. The annex
   is amended, never rewritten. *Exit: row 4 dated; audit at zero.*
5. **Session 4 (~1 h) — the stranger round 19 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. *Exit: window open,
   kill-date declared.*
6. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat — or, if the post-record
   arc governs, the continuation row's protocol opened under the same
   discipline. If C69: the failure cells at the third unseen task family and
   the third architecture family, and the expected per-head mechanism written
   as falsifiable predictions before a single number is read (Ex-C, Ex-I2,
   Ex-J2, Ex-S2, Ex-U2, Ex-W2). The scheduled negative is drafted *while the
   run is live* (Ex-D), so the S6 verdict sitting is a stamping, not a
   discovery. Row 6's kill-date honored (feedback → matrix drafted; silence →
   substitute closes it). Row 7: the eighteenth teaching artifact's skeleton
   drafted — walkthrough v18, 10-minute talk v18, or Colab grokking notebook
   v16 — with its ship-date. *Exit: row 3 pre-registered and launched (or the
   post-record protocol opened); row 6 dated either way; row 7's skeleton
   drafted.*
7. **Session 6 (~1–2 h) — the research verdict sitting.** Row 3's verdict
   read from the manifest: completed and dated, or window closed and the
   scheduled negative is the result — drafted while the run was live (Ex-D),
   so this sitting is a stamping, not a discovery. *Exit: row 3 dated either
   way.*
8. **Session 7 (~2–3 h) — the shelf rehearsal + the re-check row + the
   teaching polish.** Row 5: the hostile-webmaster walk at zero beside the
   browser, every public number clicked back to disk; the repo-shelf findings
   re-checked (local `main` reconciled, README current, residue gone, annexes'
   home verified). Row 6's re-check row dated. Row 7: the eighteenth artifact
   runs end to end on a stranger's machine (fresh clone / Colab session); the
   run transcript is the receipt; the teaching distillation (Ex-F) lands
   here. *Exit: rows 5, 6, 7 dated; the artifact shipped with its transcript.*
9. **Session 8 (~1 h) — the release.** ADR-0023 at zero UNDECIDED rows; the
   merge green locally and on GitHub; `dev == main`; home wired — this
   roadmap's companion status retired; the roadmap archived with its
   deviations, every deviation a dated ledger note. If the post-record arc
   governs, this sitting stamps the post-record arc's eighth dated direction
   — the record's closing sentence consumed eight times, never repeated.
   *Exit: the merge; the program's eighteenth dated direction — or the
   post-record arc's eighth.*

### The one measured line

ADR-0023 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row (or the post-record continuation row) whose verdict (or
scheduled negative) re-derives from a manifest; `verify-claims` at 0 with
every public number re-derivable from one command line; the hostile-webmaster
walk at zero on the live shelf and on the repo's own shelf (local `main`
reconciled, README current, residue removed, the debt ledger present or
absent-with-date); the eighteenth teaching artifact shipped with a
stranger-runnable transcript; `dev == main` and the program's eighteenth
dated direction — or, if the post-record arc governs, its eighth dated
direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk. Filed as one dated
memo each in the study log.

1. **The theory's second prediction (the C69 reading).** Elhage et al.,
   *A Mathematical Framework for Transformer Circuits* (2021) for the
   QK/OV machinery the causal claim is made over; Wang et al.,
   *Interpretability in the Wild* (2022) for activation-patching methodology
   at per-head resolution; Conmy et al., *Towards Automated Circuit
   Discovery* (2023) for turning a hand-traced mechanism into a scalable,
   testable procedure (read, never re-implemented — ACDC stays descoped);
   Varma et al., *Explaining grokking through circuit efficiency* (2023) for
   why circuits grow sharp and where that sharpness is measurable; Olsson et
   al., *In-context Learning and Induction Heads* (2022) for what transfers
   across task families; Chughtai et al., *A Toy Model of Universality*
   (2023) for why the third unseen task family's and the third architecture
   family's failure cells fail the way they do — now read at the
   *second-prediction* axis: what a theory earns by predicting unseen cells
   twice, where first-round theories overreach on their second round, and
   what Popperian corroboration and Lakatosian progressivity say about a law
   whose second out-of-sample round lands. My C65 verdict and its measured
   theory frame the reading. **Prediction to write**: which per-head role's
   failure mechanism is the boundary's root cause at the third unseen task's
   structure and at the third architecture family's, and what the patching
   at those cells reveals; the null hypothesis every measured fingerprint is
   compared against. **Primary sources**: the frozen checkpoints, C65's
   theory table, the S3 note.
2. **The exception map as a boundary law (the C70 reading).** Lyu et al.,
   *Understanding the training dynamics of transformers on modular
   arithmetic* (2024) for the loss-landscape structure of grokking and its
   phase transitions; Morwani et al. (2024) on the edge-of-numerical-
   stability regime; Gromov, *Grokking: A Memory Perspective* (2023); Power
   et al. (2022); Nanda et al. (2023) — now read at the *completeness* axis:
   what a full-cell root-cause map claims that a sampled one does not, and
   where "the driver" is really an optimization artifact that does not
   survive the second family. **Prediction**: the remaining break-map cells'
   root causes written before the analysis; C66's completed map is this
   reading's admission ticket.
3. **The policy as discipline (the C71 reading).** Gelman & Loken, *The
   Garden of Forking Paths*; Pineau et al. (2021); Kapoor & Narayanan,
   *Reproducibility in Machine Learning: A Systematic Literature Review*
   (2023); the ML reproducibility line (NASEM's five pillars) — now read at
   the *enforcement* axis: what a rate function gains when its own schedule
   is enforced across a stack's execution, and what a policy can honestly
   claim that a model cannot. My eighteen stranger-run transcripts are the
   data; the eleventh study defined the seventh drift, I must decide what
   counts as the twelfth measurement before I measure any.
4. **The instrument as a public good (the C72 reading).** Bricken et al.
   (2023); Cunningham et al. (2024); the dictionary-circuit and
   feature-universality line — plus the education-measurement line (rubric
   validity, inter-rater reliability, external assessment, instrument release
   norms) for what a *fourth, uninvited cohort* under a *published rubric
   others can run* claims that a third's does not. My Rung-5 datum (99.97%
   FVE, L0 = 136/256, 0% dead features) and C68's fifth-cohort outcome are
   the record's first data points.
5. **The post-record program, eighth generation (new, deepest).** Lakatos,
   *The Methodology of Scientific Research Programmes* (1978) — read a ninth
   time, now for the *eighth* question past a completed program: progressive
   vs. degenerating problem shifts when the *seventh* post-record verdict
   lands, Kuhn's normal science as the post-record arc's axioms, and the
   honest criterion for the eighth post-record question — a question that
   must earn the post-record arc's seventh *new* paragraph. This reading
   feeds Ex-T2 and the Session-0 question MP-49 owns more deeply than any
   phase before it: *what does the record's seventh post-record verdict
   open?* The answer can be the post-record arc's eighth dated row —
   Lakatos' point is that the decision is made on the record, never as a
   mood.
6. **The record teaches, round eighteen.** The eighteenth verdict in four
   registers — the paper's sentence, the annex's sentence, the 30-second
   spoken claim, and the 5-minute teaching explanation with a worked toy a
   stranger can run; the gap between the last two is where my teaching
   leaks, and I will measure it deliberately by writing all four registers
   for the same verdict (Ex-F). **Waiting-window rehearsal**: run the four
   registers on the R1 no-head negative — a stamped verdict, safe to
   practice on.
7. **The redemption reading, or negative results as maps, the eighteenth
   pass.** If a sparse cell exists by S0: Nanda et al.'s full per-frequency
   reading on the first sparse solution this harness ever produced. If not:
   how the *completed* law is reported honestly — the law's domain closed
   with its measured boundaries and its failure cells explained or mapped,
   the driver a principle or a case study with a dated exception map, the
   drift numbers eight deep, the negative as a contribution — and how the
   post-record harness (if PR-22 governs) would be designed from the dated
   negatives instead of from hope. Either way, the paper's hardest paragraph
   is the one that claims the dense solution *computes something*; I will
   draft it against this reading and let the manifest referee it.
8. **The mathematical bedrock, second pass (new).** The DFT-of-addition
   derivation I will hand-roll in the waiting window extended to the *second
   architecture family*: what changes in the embedding's spectral support,
   the QK/OV factorization and the convolution theorem when the architecture
   family changes — the one derivation that makes every second-family
   fingerprint interpretable rather than decorative. **Primary sources**:
   Nanda et al. (2023) and its appendix; my own `01_foundations`
   linear-algebra proofs; the exp2 Fourier instrument on disk. **One runnable
   check**: the hand derivation reproduced in a one-file script whose DFT
   output matches `results/exp2_grokking.json`'s k_99 = 111/113 at P=113,
   then re-run at the second family's geometry.
9. **The epistemology of the second prediction (new).** Popper's
   corroboration and Lakatos' problem-shift progressivity read against my own
   record: what a C69 verdict would *claim* about the law, what a falsified
   second round would *change*, and how the paper should say either — the
   reading that makes the phase's verdict honest in its own terms.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-48's release report, deviations recorded as dated ledger
  notes.
- **ADR-0023**, the eighteenth continuum ledger — eight rows pre-stamped
  with windows and kill-dates; rows 1–2 consumed from ADR-0022's verdicts;
  row 3 the eighteenth research question with its protocol note and
  heartbeat (or the post-record continuation row's protocol); rows 4–8 the
  continuum's decisions.
- **`portfolio/essay-annex-19.md`** — the v19 annex, manifest-tagged,
  amended never rewritten; the annexes' home (the live shelf) recorded with
  a date.
- **The paper v19 diff** (`portfolio/paper/main.tex` v19 + diff log) or the
  dated "the v18 is the record" memo; `make paper` re-verified in the CI
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
  if C69: the second-prediction figure spec written before the analysis, the
  figure itself manifest-tagged after. If the post-record arc governs: the
  continuation row's protocol note instead.
- **The eighteenth teaching artifact + its stranger-run transcript**
  (fresh-clone or Colab session receipt).
- **Ex-T2's execution memo** — MP-48's arc decision run with dates, written
  verdict-agnostic and executed at Session 0.
- **The waiting-window pre-drafts** (new, alongside MP-48's Session −1): the
  S0 intake checklist pre-built with empty date cells, the C69–C72
  opening-or-closure memo skeletons, the Ex-T2 execution-memo skeleton —
  saved beside MP-48's lanes, never inside them.
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C69–C72 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting — preceded by the arc consumption (Ex-N through Ex-T2), which may
   close the whole set with the post-record verdict.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0022's row-3 verdict traced to its manifest and its command; the rest
   struck with a reason — the hostile-webmaster test of my own prose,
   eighteenth run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C69 or C70 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the failure cells and the expected per-head mechanism at the
   third unseen task's structure and the third architecture family's, the
   driver's predicted exception cells with their ablation signatures — the
   "what would falsify this" column filled at writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v19 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, with the repo's own shelf added: branches reconciled, README
   current, residue removed.
6. **Ex-F · The teaching distillation, round eighteen (S7):** the eighteenth
   question's verdict in four registers — the paper's sentence, the annex's
   sentence, the 30-second spoken claim, the 5-minute teaching explanation
   with a worked toy a stranger can run; the gap between the last two is
   where my teaching leaks.
7. **Ex-G · The stranger substitute from the visitor's chair (S2):** the
   self-review written from the chair a stranger would occupy — friction
   points → fixes → re-check row — filed before S4, so the S5 kill-date can
   never close the row with a skip.
8. **Ex-H · The fork drill, deepest form (S2, verdict-agnostic):** the
   continuing state (C69–C72) vs. the post-record state (PR-22/PR-23/PR-24)
   written as two one-page paths — what each verdict changes downstream,
   including the C69-vs-C70 choice and the post-record continuation choice —
   so next phase's S0 decision is a stamping, not a discovery.
9. **Ex-I2 · The boundary hand-roll, round seven (S5, C69 only, before any
   number is read):** the expected per-head mechanism at the third unseen
   task's and the third architecture family's failure cells written by hand
   from C65's theory table — which per-head roles must transfer unchanged,
   which may re-tune, which should fail first, and what patching at those
   cells should reveal — the null hypothesis every measured fingerprint is
   compared against. One runnable check: the hand-rolled fingerprints printed
   and saved next to Ex-J2's observed ones, so the S6 comparison is a diff,
   not a memory.
10. **Ex-J2 · The transfer reader, round seven (S5, C69 only):** the script
    that loads the frozen checkpoints at every P (including the third unseen
    task's and the third family's), runs the per-head extraction and patching
    machinery, and emits the failure-cell table as a manifest-tagged JSON.
    One runnable check: the reader runs on the frozen checkpoints and its
    output is committed before the verdict paragraph is drafted.
11. **Ex-K2 · The sparse-recovery toy, revisited a twelfth time (my
    foundation challenge, second-family pass):** the one-file toy that
    recovers the addition table's DFT coefficients under L2 vs L1 penalties,
    now extended to the completion question: *does the sharpening ablation
    signature survive across two architecture families and the full
    diagram, and where does it break?* One runnable check: the toy prints
    both reconstructions' sparsity and error plus the ablation table on a
    fixed seed, across two architectures. This is the micro-scale intuition
    C70's verdict must not contradict.
12. **Ex-L2 · The "what does the dense solution compute?" sprint, round
    twelve (S5, C69 only):** the paper's hardest paragraph drafted at S5,
    then audited against the mechanism reading at S6 — prose that must
    survive contact with the manifest, the "computes something" claim
    earned or struck with one reason.
13. **Ex-M2 · The stranger-run drill on my own receipt (S1):** I execute
    MP-48's shipped artifact (the seventeenth) on a fresh clone as if I were
    the stranger — the transcript becomes the baseline against which the
    eighteenth artifact's transcript is compared. One runnable check: the
    baseline transcript saved beside the new one.
14. **Ex-N · The arc consumption, second generation (S0):** MP-40's Ex-N
    defined the terminal state; MP-41 executed it; MP-42 through MP-48
    consumed it seven times. This drill executes that second-generation
    consumption exactly as MP-48's memo stamped it.
15. **Ex-O · The arc consumption, third generation (S0):** MP-48's
    Session-0 decision becomes the object of the consumption — the seventh
    post-record question's verdict read from ADR-0022 row 3 if the arc
    governs, the criteria cited, the release that follows. One runnable
    check: the execution memo exists, names the decision rule, cites the
    criteria from MP-48's release report.
16. **Ex-P … Ex-R, Ex-T · The arc consumption, generations 4–7 (S0):** the
    consumption chain's deepest runs as MP-48 stamped them — each memo
    cites the criteria from the release report it consumes. One runnable
    check per drill: the execution memo exists and cites the criteria from
    the release report.
17. **Ex-T2 · The arc consumption, eighth generation (S0, new,
    verdict-agnostic):** the consumption chain's deepest run — MP-48's
    Session-0 decision consumed with dates as MP-49's intake, the
    seventh-generation post-record verdict read from ADR-0022 row 3 if the
    arc governs, the criteria cited, the release that follows (the eighth
    post-record question, or the C69–C72 adjudication), and what each of
    ADR-0022's possible verdicts changes in that execution. One runnable
    check: the execution memo exists, names the decision rule that closes
    or continues the program's science, and cites the criteria from MP-48's
    release report — the chain now nine generations deep, a sitting stamps,
    it never re-decides.
18. **Ex-S2 · The out-of-sample sprint, round seven (S5, C69 only):** the
    mechanism's predictions at the third unseen task family written as a
    dated table before any number is read — task family, expected failing
    head role, expected order of failure, expected patching signature — with
    the falsifier column filled at writing time; the observed table compared
    at S6 as a diff, not a memory.
19. **Ex-U2 · The architecture-family sprint, round seven (S5, C69 only):**
    the law's predictions at the third architecture family written as a dated
    table before any number is read — family, expected per-head role transfer
    or re-tuning, expected failure order, expected patching signature — with
    the falsifier column filled at writing time; the observed table compared
    at S6 as a diff, not a memory.
20. **Ex-V2 · The drift-attribution drill, round four (S5, C71 only, new):**
    the rate function's parameters re-estimated from the eighteen transcripts
    before any fix, the seventh drift's components attributed — harness
    change vs. protocol drift vs. codebase aging — each component's
    contribution re-estimated, the top root-cause's fix dated in the same
    sitting. One runnable check: the re-estimated parameter table saved
    beside the drift numbers, so the S6 verdict is a diff, not a memory.
21. **Ex-W2 · The theory's falsifier column, round two (S5, C69 only, new):**
    each second-round failure-cell explanation written with its own
    falsifier — the single observation that would refute the explanation of
    why this cell fails — filled at writing time, before the analysis; the
    S6 verdict is a diff between prediction and observation, never a memory.
22. **Ex-X2 · The exception-map hand-roll, round two (S5, C70 only, new):**
    the remaining break-map cells' root causes written by hand from C66's
    map before any number is read — which cells the chain survives, which it
    breaks at, and why, with the ablation signature each exception should
    carry; the observed map compared at S6 as a diff, not a memory.
23. **Ex-Y2 · The policy allocation drill, round two (S5, C71 only, new):**
    the twelfth measurement's schedule derived from the rate model before the
    run — the next measurement, its budget, its predicted outcome, its
    falsifier — so the S6 verdict compares the schedule against what the
    receipt system actually did, as a diff, not a memory.
24. **Ex-Z2 · The public rubric draft, round two (S5, C72 only, new):** the
    fourth cohort's rubric written as a public artifact — scoring rule,
    evidence requirements, adjudication procedure, release license — before
    recruitment, so the fourth measurement is taken under the published
    rule, never after it.
25. **Ex-Q · The drift-attribution drill (S5, C71 only):** the seventh
    drift's components attributed before any fix — harness change vs.
    protocol drift vs. codebase aging — each component's contribution
    estimated from the eighteen transcripts, the top root-cause's fix dated
    in the same sitting. One runnable check: the attribution table saved
    beside the drift numbers, so the S6 verdict is a diff, not a memory.
26. **Habit · The clock check (every session):** ADR-0023's undated rows, the
    open PR's CI status line, the shelf's health — all three before any new
    prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, eighteenth execution.** A phase that opens two
  research questions is drift by another name; the unchosen candidates close
  in the same sitting as the choice — and the arc consumption may close all
  of them with the post-record verdict. The continuum law is the mechanical
  refusal of this drift — proven executable seventeen times, it must simply
  be executed again.
- **The candidate set is frozen before S0, never improvised at it.** C69–C72
  are conditions, not predictions; a sitting decides, it never invents — and
  the terminal-state object is the hardest frozen object on the record:
  written by MP-40, executed by MP-41, consumed eight more times since —
  *consumed a ninth time* by MP-49, never re-negotiated in the consuming
  sitting.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0022's row-3 verdict in the sitting that owns it
  — or the post-record statement, if the arc governs.
- **The receipt compounds.** The eighteenth runnable artifact is only worth
  shipping because the first seventeen transcripts proved the format — and
  if C71 opens, the receipts are a drift-of-drift-of-drift-of-drift-of-
  drift-of-drift-of-drift number measured seven times in a row, tested by
  people I did not choose, across an aging codebase. My showcase's story is
  now "read it, run it, watch me be wrong on the record," eighteen receipts
  deep.
- **The waiting window belongs to MP-48's Session −1 — and this draft is a
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
  compile gate is the hardest artifact in the stack; the v19 rule ("opens
  only for new numbers") is the insurance that makes a missing toolchain a
  dated reason, not a crisis.
- **Protect the release report.** The serialized stack means MP-29's release
  is still the artifact everything downstream consumes; a slip at any link
  slides the whole chain. A promise can be re-planned forever, but a dated
  row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0022 at zero, the live
  URL, `verify-claims` at 0, the seventeenth teaching transcript on disk — a
  condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; the R1 no-head negative — 0/8
  heads, stamped 2026-08-14 — is the record's newest dated signature. The
  strongest form of the signature is the chain: negative → map →
  characterization → mechanism → causal verdict → circuit → law → theory →
  *second prediction* — or a record that knew when to end.
- **The steady state is the reward, not the ceremony.** MP-49 will be the
  twelfth roadmap written from an *executed* roadmap's release report — the
  program at its normal, confirmed eleven times. The machinery is the
  guardrail, never the goal: rows are dated in the sitting that owns them, or
  they are not rows.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED rows
  at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story:** *the program's eighteenth dated
  direction was written from its own release report — the cap honored, the
  stack executed, the steady state kept honest twelve times, the record
  taught eighteen times in runnable artifacts, every public number still
  re-derives from one command line, and the record consumed — nine times,
  with dates — its own terminal-state decision, and answered it in a
  release.* Every artifact this phase launches is written to that standard.

## Links

- [[00_meta/48_micro-phase-48-review-and-roadmap]] ·
  [[00_meta/48b_micro-phase-48-execution-roadmap]] — the seventeenth
  question's review and execution roadmap; this roadmap's intake is
  ADR-0022's release report and MP-48's Session-0 decision, which Session 0
  consumes again.
- [[00_meta/47_micro-phase-47-review-and-roadmap]] ·
  [[00_meta/46_micro-phase-46-review-and-roadmap]] — the sixteenth and
  fifteenth questions' reviews and roadmaps, the un-cap's steady state
  confirmed eleven times.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat — and the
  row the terminal state executes.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/microscope-trial-table]] ·
  [[06_production_ai/notes/positive-control-protocol]] — the science C69–C72
  adjudicate over, whose pending verdicts are the intake.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/checkpoint-resume-durability]] ·
  [[06_production_ai/notes/scheduled-negatives-mp28]] — the CPU-budget canon
  the phase's runs are specified against.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.
