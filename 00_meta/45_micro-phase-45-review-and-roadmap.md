---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-17
---

# Micro-Phase 45 — State Review and Roadmap: the fourteenth question, written from the thirteenth release report

> **STATUS: REVIEW + ROADMAP, NOT A PRE-REGISTRATION.** This note is the
> companion review to [[00_meta/44_micro-phase-44-review-and-roadmap]], the
> thirteenth question's review and roadmap: it opens no rows, launches no
> runs, claims no window, and is wired into home only as a companion pointer
> — it is not a pre-registration and it is not counted against any cap,
> because the cap is spent. It is my personal state review and my
> step-by-step plan for the phase that starts at MP-45's Session 0, written
> in the same first-person register as my progress log so it doubles as the
> public record of how I reasoned about the program's steady state before I
> executed through it. Everything factual in this file was re-verified
> against the repository on 2026-08-17: working tree clean, `dev` reconciled
> with `main` at the MP-44 squash (PR #78, main at `063339f`, dev at
> `759024c`), 190 tracked tests, ruff clean, blocking mypy clean,
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
  re-verified in the MP-44 drafting sitting and again in this one
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
post-record arc's own successor?* (MP-44's sitting). By MP-45's Session 0 the
record will hold thirteen dated directions, a characterized dense regime, a
causal reading (or its evidence lane), whichever of C49–C52 ADR-0018's
sitting chose — and the answer to the question MP-44's Session 0 owned more
deeply than any phase before it: **whether the post-record arc governs and,
if it does, what the third post-record question was.** The fourteenth
question is the second one I choose with the second-generation arc
consumption *stamped* — or the fourth question past the record's closing
sentence.

### What I found walking the shelf while drafting (five dated intake facts, re-verified)

Drafted and re-verified against the repository on 2026-08-17. These are the
facts the hostile-webmaster walk would catch — MP-44's dated intake, walked
again, each cell stamped with its 2026-08-17 state so the intake is a
re-verification, never a memory:

1. **Local `main` is reconciled.** Verified: local `main` sits at `063339f`
   = `origin/main` (the MP-44 squash, PR #78) and `dev` = `origin/dev` at
   `759024c` (the reconcile merge). MP-44's intake fact #1 is **RESOLVED** —
   the MP-44 merge itself closed it; Session 1's walk re-verifies with the
   branch list as the transcript.
2. **`portfolio/README.md` is still stale.** Re-verified: it still reads
   "Mini-paper (LaTeX PDF) not yet written", "Interactive demo … not built
   yet", "Experiment tracking … not set up yet" — contradicted by the
   record: the paper has lived through the v8–v14 arc, the site and Space
   have been live since the premiere, and the manifest machinery has been
   tracking results since Micro-Phase 8. MP-44's Session 1 owns the dated
   fix; this phase's Session 1 re-verifies the closure with the dated file
   itself.
3. **No `essay-annex-*.md` exists on disk.** Re-verified: `portfolio/`
   holds `RESULTS.md`, `README.md` and `model-card.md` and nothing else.
   The annexes live on the live shelf (site and Space), not in this
   repository. The v15 annex contract must state the artifact's home with a
   date instead of implying the repo holds it.
4. **Rung 6 residue still survives on disk.** Re-verified: the deleted
   Rung 6 (2026-08-01, fabricated data) left
   `src/experiments/__pycache__/exp6_automated_circuit.cpython-312.pyc` and
   `figures/exp6_automated_vs_manual.png` in the gitignored directories
   (both confirmed present 2026-08-17). A hygiene row for Session 1's walk
   — removal with a transcript.
5. **`checklists/gate-debt.md` still does not exist.** Re-verified:
   `checklists/` holds `reproducibility-checklist.md` and nothing else. The
   debt ledger is promised by named MP-30/31 rows; row 8's re-verification
   must record its absence with a date rather than claim a file that is not
   there.

One further verified shelf fact, carried from MP-44's sitting: **`figures/`
holds zero tracked files** — the entire showcase corpus is gitignored build
product, regenerated by `make reproduce` and provenanced by the manifests,
never by git. The 2026-08-17 walk confirmed `git ls-files figures/` is
empty while `portfolio/figures/` holds the twelve tracked figures; the
provenance story lives in `src/results.py`, and that is exactly where the
hostile-webmaster walk verifies it.

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no
phase. MP-37 through MP-44 are the un-cap executed exactly once each — their
drafts and reviews on disk, conditioned on their predecessors' releases.
**ADR-0018's eight rows are the rows MP-44 will fill**; **ADR-0019's eight
rows are the rows this roadmap will fill** — exactly once, under the
continuum law, fourteenth execution, written from MP-44's release report
rather than from the habit of pre-registering.

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

12+ provenance-guarded figures, the paper at v8/v14 (the v15 rule is this
phase's), the site and Space live since the premiere, the essay annex at
v8/v14, thirteen runnable teaching artifacts with stranger-run transcripts
(the receipts land only if the stack ships: the thirteenth ships in MP-44,
**the fourteenth in this phase**). My teaching lane ships the fourteenth
artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The intake is now a consumption of a consumption of a consumption of a
   consumption.** MP-40's Ex-N defined the terminal state; MP-41's Session 0
   executed it; MP-42's Session 0 consumed that execution and chose;
   MP-43's Session 0 consumed that choice with dates; MP-44's Session 0
   consumed that decision and adjudicated C49–C52 or continued the
   post-record arc. MP-45's Session 0 must **consume MP-44's Session-0
   decision with dates** — the single most dangerous drift is re-litigating
   a thrice-consumed decision: re-opening candidates the thirteenth question
   already closed with dated reasons, or treating "the post-record arc
   governs" as a mood instead of as a stamped verdict. The decision chain is
   now five generations deep; a sitting stamps, it never re-decides.
2. **The stacked execution is still the critical path.** MP-45's Session 0
   consumes MP-44's release report, which consumes ADR-0018's, which awaits
   MP-29 through MP-40. A slip at any link slides the whole chain; **my
   highest-leverage act is unchanged: protect MP-29's window** — its release
   report is the artifact everything downstream consumes. Nothing in this
   phase may borrow a minute from it, and this draft is written
   verdict-agnostic by law: it re-plans not a single row of MP-29–MP-44.
3. **The steady state is the un-cap's end state, and it must not become
   ceremony.** MP-45 is the eighth roadmap written from an *executed*
   roadmap's release report — the program's normal, confirmed eight times.
   The drift risk inverts and deepens: the machinery (ledgers, sessions,
   gate criteria) is now fourteen executions deep, so the law's
   countermeasure is that rows must still be dated in the sitting that owns
   them, verdicts still consumed as artifacts, and zero UNDECIDED rows at
   Session 8 — the machinery is the guardrail, never the goal, and a
   stamped row with no science behind it is ceremony by another name.
4. **The paper's compile gate is the hardest artifact in the stack.** No TeX
   on this machine — verified again in this sitting; MP-31's own canon
   applies early: *toolchains are pinned in Session 0, never discovered at
   Session 7.* The paper v15 rule ("opens only for new numbers, else the
   v14 is the record") is my insurance — a dated sentence, never a silence.
5. **The standing debt is undated by design and must not survive the
   stack.** exp5 1000-epoch ×3-seed (~15 h), clean-clone proof, graduation
   proof, `reproduce-multiseed`, W&B, the gate-debt transcript — each owned
   by a named row in MP-30–MP-36 and re-verified in MP-37's through MP-44's
   row 8. Row 8 of this phase re-verifies those closures with transcripts;
   a pending item cannot outlive a ledger — and a re-verification cannot
   claim a file that is not there (`gate-debt.md`'s absence is a dated
   fact, not a silence).
6. **The science's next fork is one verdict deeper.** MP-44 adjudicates
   C49–C52 — or continues the post-record arc — from ADR-0017's verdicts;
   MP-45's candidate set is conditioned on *that* verdict — C53 opens only
   on C49's positive reading, C54 only on C50's named driver, C55 only on
   C51's dated third drift, C56 only on C52's shipped course — and the
   post-record continuation overrides the set if MP-44's Session 0
   continued the arc. The redemption (a sparse cell found anywhere)
   overrides both. My candidate set is frozen precisely so this fork is
   adjudicated at Session 0, never improvised.
7. **The showcase's receipts are still future, one deeper.** The fourteenth
   stranger-run transcript lands only if the lanes execute; C55 (the third
   drift's diagnosis) is conditioned on ≥ 14 transcripts on disk at Session
   0 — the receipt compounds only if the lanes execute.
8. **Stop-and-publish is a row, not a threat — and the post-record
   criterion is now four questions deep.** ADR-0004's row 5 (the record
   releases as-is) stays open as the program's honest exit: a phase is
   worth doing only if its candidate set can earn a paragraph the record
   does not already have. Every candidate below must beat that row in the
   sitting that chooses it. The fourteenth execution sharpens this to its
   edge: if MP-44's Session 0 continued the post-record arc, the deepest
   candidate this phase can choose is the one that earns the post-record
   arc's *third new paragraph* — the record's closing sentence consumed
   four times, never repeated. The deepest form of laziness is not
   building what the record has already said.

## Part III — The roadmap, step by step (the continuum law, fourteenth execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C53 | **The boundary's mechanism** (C49's successor) — the boundary law *explains its own break*: the second unseen task family's failure cells root-caused at per-head resolution, the boundary's failure modes traced causally (activation patching at the boundary's own edge), the domain-of-validity statement upgraded from a map to a mechanism — a boundary that explains why it breaks is a mechanism; a boundary that merely maps its break is a map, and the map is the result | ADR-0018 row 3 = C49 with a positive verdict and boundary fingerprints on disk | C49 closed negative, or the post-record arc governs → the boundary's successor belongs to the post-record arc, or the record already has its closing sentence |
| C54 | **The driver's mechanism** (C50's successor) — the named driver *root-caused*: the loss-landscape → weight-norm → sharpening chain verified causally (each link ablated, the dated negatives as verdicts), why the driver predicts what it predicts, and whether the mechanism survives across two architecture families — a driver that explains why it predicts is a mechanism; a driver that predicts without cause is a correlation, and the correlation is the result | ADR-0018 row 3 = C50 with the driver named as a quantity on disk | C50 never opened, or its verdict was negative → no principle to root-cause, this closes with that verdict |
| C55 | **The drift root-caused** (C51's successor) — the eighth reproducibility study: the third drift's components *attributed* before any fix (harness change vs protocol drift vs codebase aging), the top root-cause fixed with a dated change, the rate re-measured a fourth time, the receipt system's rate written as a function of codebase age — a drift that explains its own drift is a diagnosis; a drift measured without cause is a number, and the number is the result | ADR-0018 row 3 = C51 with a dated third drift on disk AND ≥ 14 stranger-run transcripts at S0 | Fewer than 14 transcripts, or C51 never opened → the receipt system hasn't earned an eighth study |
| C56 | **The course's second edition** (C52's successor) — the measured pedagogy *re-measured*: the feature-complete circuit course's feedback-to-fixes matrix executed with dates (every rubric cell below threshold lands a dated fix), the outcome re-measured with a second stranger cohort, the verdict a curriculum with two measured cohorts — a course revised from its measurements is a curriculum; a course re-shown is a poster | ADR-0018 row 3 = C52 with the course and its measured outcome on disk | C52 never opened, or a sparse regime exists → the sparse reading owns the question |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥
3 checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The terminal-state override stands, now five generations deep: **if MP-44's
Session 0 consumed MP-43's decision with dates and the post-record arc
governs, then MP-45's Session 0 consumes the third post-record question's
verdict from ADR-0018 row 3 and continues the post-record arc, choosing the
fourth post-record question from the pre-registered continuation set below.**
The rule is executed with dates at Session 0; it is never improvised and
never re-negotiated in the sitting that consumes it.

### The post-record continuation set (chosen only if MP-44 continued the post-record arc)

| # | Candidate | Why it would open | Why it would close |
|---|---|---|---|
| PR-10 | **The new harness's first reproducibility datum** (PR-7's successor) — the second recipe at the new address *replicated across seeds*: the record's complete dense law as the specification, the recipe run under the record's laws at ×3 seeds, the verdict read from fresh manifests — a second recipe replicated across seeds is the harness's first reproducibility datum; a recipe run once is an anecdote | The post-record arc continued at MP-44 with PR-7's verdict on disk | The record never closed, or the redemption fired first → the sparse question belongs to the old arc |
| PR-11 | **The law at the record's edge, fourth task** (PR-8's successor) — the frozen-checkpoint predictions tested at the fourth unseen task family: a law that predicts four times is a law with a measured domain; a law that breaks is a boundary with a map | The post-record arc continued at MP-44 with PR-8's verdict on disk | The record never closed → the law's successors are C53's, not the post-record arc's |
| PR-12 | **The record as a course, third edition** (PR-9's successor) — the closed record's teaching corpus revised from its second intake: the feedback-to-fixes matrix executed with dates, the thirteen runnable artifacts assembled, the third edition measured as a learning instrument with two cohorts — a course revised from its receipts twice is a curriculum; a course re-shown is a poster | The post-record arc continued at MP-44 with PR-9's verdict on disk | The record never closed → the teaching lane continues as the continuum's row 8 |

The likely survivor, written as a condition chain, never a prediction: if
MP-44's Session 0 continued the post-record arc → **the post-record
continuation** — the fourth question past the record, chosen in the consuming
sitting from PR-10/PR-11/PR-12; else if C49 landed positive → **C53** — the
boundary's mechanism, always CPU-runnable on checkpoints that exist today;
else if C50's driver verdict landed → **C54**; else **C55** (always-runnable,
the showcase's own science, receipts now fourteen deep); C56 is the evidence
lane and the teaching lane's anchor.

### The nine sessions

1. **Session 0 (~1 h) — the gate truthing + the thrice-consumed arc + the
   continuum choice.** Consume MP-44's release report row by row:
   ADR-0018 at zero UNDECIDED rows, the live URL re-clicked in the sitting,
   `verify-claims` at its actual count, the thirteenth teaching transcript on
   disk, `dev == main`. Commit the intake table before a single continuum
   row opens. Then **Ex-P: consume MP-44's Session-0 decision with dates** —
   the fourth-generation consumption: if the post-record arc continued, the
   third post-record question's verdict is read from ADR-0018 row 3 and the
   fourth post-record question chosen from the pre-registered continuation
   set (PR-10/PR-11/PR-12), each opening-or-closure memo in three sentences
   with a falsifier; if not, the C53–C56 adjudication: exactly one opens as
   row 3, the unchosen close with one dated reason each, stamped in the same
   sitting. Open ADR-0019 with its eight rows, windows and kill-dates;
   declare the terminus (release = merge + 14 calendar days); promote this
   roadmap from MP-44's release report, deviations recorded as dated ledger
   notes. *Exit: intake signed; the thrice-consumed arc stamped; row 3
   chosen (or the post-record continuation row opened); ledger open.*
2. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — extended to the repo's own shelf: local `main`
   re-verified reconciled to `origin/main` (branch list as the transcript),
   `portfolio/README.md`'s staleness verified closed (MP-44's Session 1
   owned the first fix; this sitting verifies the file is current), the
   exp6 residue removed with a transcript, the annexes' location verified.
   Row 8: MP-44's stamped closures re-verified (W&B, clean-clone proof,
   graduation proof, `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch
   resolution, the README fix, the residue removal) — each cell
   LAUNCHED-with-transcript or CLOSED-with-one-reason; a claimed closure
   without its transcript stays open and blocks Session 8; `gate-debt.md`'s
   absence, if still absent, recorded with a date. *Exit: rows 5 and 8
   stamped.*
3. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the thirteenth research question's verdict (ADR-0018 row 3) becomes the
   paper-v15 section, the annex table, or the results-page row — every
   number manifest-tagged, consumed in the sitting that owns it; if the
   post-record arc governs, the post-record statement is framed from
   MP-44's release, never rewritten. Row 2: v15 opens only if row 1 lands
   new numbers; else "the v14 is the record" is the dated reason and `make
   paper` is re-verified against v14. Row 6's substitute filed from the
   visitor's chair, before the window opens (Ex-G); the fork drill (Ex-H)
   and the arc consumption (Ex-N, Ex-O, Ex-P) land here. *Exit: rows 1 and 2
   dated; substitute filed; Ex-P's execution memo on disk.*
4. **Session 3 (~2–3 h) — the essay annex v15.** `portfolio/essay-annex-15.md`
   (its home on the live shelf, dated): the thirteenth question's verdict set
   and the teaching lane's thirteenth receipt distilled into one dated annex;
   the reverse claims audit at zero (prose → manifest → command); each
   claim's "what would falsify this" column filled at writing time. The
   annex is amended, never rewritten. *Exit: row 4 dated; audit at zero.*
5. **Session 4 (~1 h) — the stranger round 15 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. *Exit: window open,
   kill-date declared.*
6. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat — or, if the post-record
   arc governs, the continuation row's protocol opened under the same
   discipline. If C53: the boundary's failure cells and the expected
   per-head mechanism at the second unseen task family written as
   falsifiable predictions before a single number is read (Ex-C, Ex-I,
   Ex-J). Row 6's kill-date honored (feedback → matrix drafted; silence →
   substitute closes it). Row 7: the fourteenth teaching artifact's skeleton
   drafted — walkthrough v14, 10-minute talk v14, or Colab grokking
   notebook v12 — with its ship-date. *Exit: row 3 pre-registered and
   launched (or the post-record protocol opened); row 6 dated either way;
   row 7's skeleton drafted.*
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
   fourteenth artifact runs end to end on a stranger's machine (fresh
   clone / Colab session); the run transcript is the receipt; the teaching
   distillation (Ex-F) lands here. *Exit: rows 5, 6, 7 dated; the artifact
   shipped with its transcript.*
9. **Session 8 (~1 h) — the release.** ADR-0019 at zero UNDECIDED rows; the
   merge green locally and on GitHub; `dev == main`; home wired — this
   roadmap's companion status retired; the roadmap archived with its
   deviations, every deviation a dated ledger note. If the post-record arc
   governs, this sitting stamps the post-record arc's fourth dated
   direction — the record's closing sentence consumed four times, never
   repeated. *Exit: the merge; the program's fourteenth dated direction —
   or the post-record arc's fourth.*

### The one measured line

ADR-0019 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row (or the post-record continuation row) whose verdict (or
scheduled negative) re-derives from a manifest; `verify-claims` at 0 with
every public number re-derivable from one command line; the hostile-webmaster
walk at zero on the live shelf and on the repo's own shelf (local `main`
reconciled, README current, residue removed, the debt ledger present or
absent-with-date); the fourteenth teaching artifact shipped with a
stranger-runnable transcript; `dev == main` and the program's fourteenth
dated direction — or, if the post-record arc governs, its fourth dated
direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk.

1. **The boundary's mechanism (the C53 reading).** Elhage et al.,
   *A Mathematical Framework for Transformer Circuits* (2021) for the
   QK/OV machinery the causal claim is made over; Wang et al.,
   *Interpretability in the Wild* (2022) for activation-patching methodology
   at per-head resolution; Chughtai et al., *A Toy Model of Universality*
   (2023) for what "the same algorithm" can honestly mean *across unseen
   tasks*; Olsson et al., *In-context Learning and Induction Heads* (2022)
   for what transfers across task families — now read at the *mechanism*
   axis: what it takes to root-cause *why* a boundary law breaks where it
   breaks, patching at the failure cells themselves, and where mechanism
   claims over dense circuits have been shown to overreach. My C49 verdict
   and its boundary fingerprints frame the reading. **Prediction to write
   before the analysis**: which per-head roles fail first at the second
   unseen task's structure, and what the patching at those cells reveals;
   the null hypothesis every measured fingerprint is compared against.
   **Primary sources**: the frozen checkpoints, C49's boundary-fingerprint
   table, the S3 note.
2. **The driver's mechanism (the C54 reading).** Morwani et al. (2024) on
   the edge-of-numerical-stability regime, Gromov, *Grokking: A Memory
   Perspective* (2023), Power et al. (2022), Nanda et al. (2023) — now read
   at the *causality* axis: whether the loss-landscape → weight-norm →
   sharpening chain can be ablated link by link, what a dated negative at
   any link means for the driver, and where "the driver" is really a
   loss-landscape artifact that does not survive ablation. **Prediction**:
   the order-parameter dynamics at two unseen cells with the causal chain's
   expected ablation signature written before the analysis; C50's named
   driver is this reading's admission ticket.
3. **The drift's diagnosis (the C55 reading).** Gelman & Loken, *The Garden
   of Forking Paths*; Pineau et al. (2021); the ML reproducibility line
   (NASEM's five pillars) — now read at the *attribution* axis: what it
   takes to attribute a measured drift's components on an aging codebase
   (harness change vs protocol drift vs aging), and what a fourth
   measurement claims when the top root-cause has been fixed with a dated
   change. My fourteen stranger-run transcripts are the data; the seventh
   study defined the third drift, I must decide what counts as the fourth
   before I measure any.
4. **Measured pedagogy, second edition (the C56 reading).** Bricken et al.
   (2023); Cunningham et al. (2024); the dictionary-circuit and
   feature-universality line — plus the education-measurement line (rubric
   validity, test-retest reliability) for what a *second cohort's* measured
   outcome claims that a first cohort's does not. My Rung-5 datum (99.97%
   FVE, L0 = 136/256, 0% dead features), C48's shipped course and C52's
   measured outcome are the record's first data points.
5. **The post-record program, fourth generation (new, deepest).** Lakatos,
   *The Methodology of Scientific Research Programmes* (1978) — read a fifth
   time, now for the *fourth* question past a completed program: progressive
   vs degenerating problem shifts when the *third* post-record verdict
   lands, Kuhn's normal science as the post-record arc's axioms, and the
   honest criterion for the fourth post-record question — a question that
   must earn the post-record arc's third *new* paragraph. This reading feeds
   Ex-P and the Session-0 question MP-45 owns more deeply than any phase
   before it: *what does the record's third post-record verdict open?* The
   answer can be the post-record arc's fourth dated row — Lakatos' point is
   that the decision is made on the record, never as a mood.
6. **The record teaches, round fourteen.** The fourteenth verdict in four
   registers — the paper's sentence, the annex's sentence, the 30-second
   spoken claim, and the 5-minute teaching explanation with a worked toy a
   stranger can run; the gap between the last two is where my teaching
   leaks, and I will measure it deliberately by writing all four registers
   for the same verdict (Ex-F).
7. **The redemption reading, or negative results as maps, the fourteenth
   pass.** If a sparse cell exists by S0: Nanda et al.'s full per-frequency
   reading on the first sparse solution this harness ever produced. If not:
   how the *completed* law is reported honestly — the boundary's mechanism
   traced at its own edge, the driver root-caused as a predicting quantity,
   the drift numbers dated four deep, the negative as a contribution — and
   how the post-record harness (if PR-10 governs) would be designed from
   the dated negatives instead of from hope. Either way, the paper's
   hardest paragraph is the one that claims the dense solution *computes
   something*; I will draft it against this reading and let the manifest
   referee it.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-44's release report, deviations recorded as dated ledger
  notes.
- **ADR-0019**, the fourteenth continuum ledger — eight rows pre-stamped
  with windows and kill-dates; rows 1–2 consumed from ADR-0018's verdicts;
  row 3 the fourteenth research question with its protocol note and
  heartbeat (or the post-record continuation row's protocol); rows 4–8 the
  continuum's decisions.
- **`portfolio/essay-annex-15.md`** — the v15 annex, manifest-tagged,
  amended never rewritten; the annexes' home (the live shelf) recorded with
  a date.
- **The paper v15 diff** (`portfolio/paper/main.tex` v15 + diff log) or the
  dated "the v14 is the record" memo; `make paper` re-verified in the CI
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
  if C53: the boundary-mechanism figure spec written before the analysis,
  the figure itself manifest-tagged after. If the post-record arc governs:
  the continuation row's protocol note instead.
- **The fourteenth teaching artifact + its stranger-run transcript**
  (fresh-clone or Colab session receipt).
- **Ex-P's execution memo** — MP-44's arc decision run with dates: the
  post-record verdict consumed or the C53–C56 adjudication executed, the
  criteria cited, the decision that follows (the fourth post-record
  question, or the continuation), written verdict-agnostic in Session 2 and
  executed at Session 0.
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C53–C56 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting — preceded by the arc consumption (Ex-N, Ex-O, Ex-P), which may
   make the whole set close with the post-record verdict.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0018's row-3 verdict traced to its manifest and its command; the
   rest struck with a reason — the hostile-webmaster test of my own prose,
   thirteenth run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C53 or C54 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the boundary's failure cells and the expected per-head
   mechanism at the second unseen task's structure, the driver's predicted
   order-parameter dynamics at unseen cells with its ablation signature —
   the "what would falsify this" column filled at writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v15 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, with the repo's own shelf added: branches reconciled, README
   current, residue removed.
6. **Ex-F · The teaching distillation, round fourteen (S7):** the
   fourteenth question's verdict in four registers — the paper's sentence,
   the annex's sentence, the 30-second spoken claim, the 5-minute teaching
   explanation with a worked toy a stranger can run; the gap between the
   last two is where my teaching leaks.
7. **Ex-G · The stranger substitute from the visitor's chair (S2):** the
   self-review written from the chair a stranger would occupy — friction
   points → fixes → re-check row — filed before S4, so the S5 kill-date can
   never close the row with a skip.
8. **Ex-H · The fork drill, deepest form (S2, verdict-agnostic):** the
   continuing state (C53–C56) vs the post-record state (PR-10/PR-11/PR-12)
   written as two one-page paths — what each verdict changes downstream,
   including the C53-vs-C54 choice and the post-record continuation choice —
   so next phase's S0 decision is a stamping, not a discovery.
9. **Ex-I · The boundary hand-roll, round three (S5, C53 only, before any
   number is read):** the expected per-head mechanism at the second unseen
   task's failure cells written by hand from the C49 boundary law — which
   per-head roles must transfer unchanged, which may re-tune, which should
   fail first, and what patching at those cells should reveal — the null
   hypothesis every measured fingerprint is compared against. One runnable
   check: the hand-rolled fingerprints printed and saved next to Ex-J's
   observed ones, so the S6 comparison is a diff, not a memory.
10. **Ex-J · The transfer reader, round three (S5, C53 only):** the script
    that loads the frozen checkpoints at every P (including the second
    unseen task's), runs C49's per-head extraction and patching machinery,
    and emits the failure-cell table as a manifest-tagged JSON. One
    runnable check: the reader runs on the frozen checkpoints and its
    output is committed before the verdict paragraph is drafted.
11. **Ex-K · The sparse-recovery toy, revisited an eighth time (my
    foundation challenge, mechanism pass):** the one-file toy that recovers
    the addition table's DFT coefficients under L2 vs L1 penalties, now
    extended to the mechanism question: *can the L2-minimal solution's
    sharpening be ablated link by link, and does the ablation signature
    survive across two architecture families?* One runnable check: the toy
    prints both reconstructions' sparsity and error plus the ablation table
    on a fixed seed, across two architectures. This is the micro-scale
    intuition C54's verdict must not contradict.
12. **Ex-L · The "what does the dense solution compute?" sprint, round
    eight (S5, C53 only):** the paper's hardest paragraph drafted at S5,
    then audited against the mechanism reading at S6 — prose that must
    survive contact with the manifest, the "computes something" claim
    earned or struck with one reason.
13. **Ex-M · The stranger-run drill on my own receipt (S1):** I execute the
    previous phase's shipped artifact (the thirteenth) on a fresh clone as
    if I were the stranger — the transcript becomes the baseline against
    which the fourteenth artifact's transcript is compared. One runnable
    check: the baseline transcript saved beside the new one.
14. **Ex-N · The arc consumption, second generation (S0):** MP-40's Ex-N
    defined the terminal state; MP-41 executed it; MP-42 consumed that
    execution and chose; MP-43 consumed that choice with dates; MP-44
    consumed that Session-0 decision. This drill executes that
    second-generation consumption exactly as MP-44's memo stamped it.
15. **Ex-O · The arc consumption, third generation (S0):** MP-44's
    Session-0 decision becomes the object of the consumption — the third
    post-record question's verdict read from ADR-0018 row 3 if the arc
    governs, the criteria cited, the release that follows (the fourth
    post-record question, or the C53–C56 adjudication). One runnable check:
    the execution memo exists, names the decision rule, cites the criteria
    from MP-44's release report.
16. **Ex-P · The arc consumption, fourth generation (S0, new,
    verdict-agnostic):** the consumption chain's deepest run — MP-44's
    Session-0 decision consumed with dates as MP-45's intake, the
    second-generation post-record verdict read from ADR-0018 row 3 if the
    arc governs, the criteria cited, the release that follows (the fourth
    post-record question, or the C53–C56 adjudication), and what each of
    ADR-0018's possible verdicts changes in that execution. One runnable
    check: the execution memo exists, names the decision rule that closes
    or continues the program's science, and cites the criteria from MP-44's
    release report — the chain now five generations deep, a sitting stamps,
    it never re-decides.
17. **Ex-Q · The drift-attribution drill (S5, C55 only):** the third drift's
    components attributed before any fix — harness change vs protocol drift
    vs codebase aging — each component's contribution estimated from the
    fourteen transcripts, the top root-cause's fix dated in the same
    sitting. One runnable check: the attribution table saved beside the
    drift numbers, so the S6 verdict is a diff, not a memory.
18. **Habit · The clock check (every session):** ADR-0019's undated rows,
    the open PR's CI status line, the shelf's health — all three before
    any new prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, fourteenth execution.** A phase that opens two
  research questions is drift by another name; the unchosen candidates close
  in the same sitting as the choice — and the arc consumption may close all
  of them with the post-record verdict. The continuum law is the mechanical
  refusal of this drift — proven executable thirteen times, it must simply
  be executed again.
- **The candidate set is frozen before S0, never improvised at it.** C53–C56
  are conditions, not predictions; a sitting decides, it never invents — and
  the terminal-state object is the hardest frozen object on the record:
  written by MP-40, executed by MP-41, consumed by MP-42, consumed again by
  MP-43, consumed a third time by MP-44, *consumed a fourth time* by MP-45 —
  never re-negotiated in the consuming sitting.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0018's row-3 verdict in the sitting that owns
  it — or the post-record statement, if the arc governs.
- **The receipt compounds.** The fourteenth runnable artifact is only worth
  shipping because the first thirteen transcripts proved the format — and if
  C55 opens, the receipts are a drift-of-drift-of-drift number measured
  four times in a row, tested by people I did not choose, across an aging
  codebase. My showcase's story is now "read it, run it, watch me be wrong
  on the record," fourteen receipts deep.
- **The steady state is the reward, not the ceremony.** MP-45 is the eighth
  roadmap written from an *executed* roadmap's release report — the program
  at its normal, confirmed eight times. The cap's lesson was that promises
  without dates drift; the steady state's discipline is that the machinery
  never becomes the goal: rows are dated in the sitting that owns them, or
  they are not rows.
- **Stop-and-publish stays open, and the post-record criterion is now four
  questions deep.** ADR-0004's row 5 is the honest exit; a candidate set
  that cannot earn a paragraph the record lacks is a phase that should close
  itself. If the post-record arc governs, the deepest candidate earns the
  post-record arc's *third new paragraph* — the record's closing sentence
  consumed four times, never repeated. This is the deepest form of
  laziness: do not build what the record has already said.
- **Toolchains are pinned in S0, never discovered at S7.** The paper's
  compile gate is the hardest artifact in the stack; the v15 rule ("opens
  only for new numbers") is the insurance that makes a missing toolchain a
  dated reason, not a crisis.
- **Protect the release report.** The serialized stack means MP-29's release
  is the artifact everything downstream consumes; a slip at any link slides
  the whole chain. The deepest law still applies: a promise can be
  re-planned forever, but a dated row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0018 at zero, the live
  URL, `verify-claims` at 0, the thirteenth teaching transcript on disk — a
  condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; the R1 no-head negative — 0/8
  heads, stamped 2026-08-14 — is the record's newest dated signature, and
  the chain I am building toward is the strongest form of the signature: a
  negative that became a map, a map that became a characterization, a
  characterization that became a mechanism, a mechanism that earned its
  causal verdict, a circuit that earned its complete reading, a circuit
  that earned its law, a law that predicted an unseen point, a boundary
  that earned its own second out-of-sample point, a boundary that earns its
  mechanism — or a record that knew when to end.
- **The debt row re-verifies; it never re-does.** A stamped closure is
  re-checked with its transcript; a genuinely new debt cell is a NEW row,
  never a revision. A pending item cannot outlive a ledger — and a
  re-verification cannot claim a file that is not there.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED
  rows at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story:** *the program's fourteenth dated
  direction was written from its own release report — the cap honored, the
  stack executed, the steady state kept honest eight times, the record
  taught fourteen times in runnable artifacts, every public number still
  re-derives from one command line, and the record consumed — four times,
  with dates — its own terminal-state decision, and answered it in a
  release.* Every artifact this phase launches is written to that standard.

## Links

- [[00_meta/44_micro-phase-44-review-and-roadmap]] · [[00_meta/43_micro-phase-43-review-and-roadmap]] —
  the thirteenth question's review and roadmap; this roadmap's intake is
  ADR-0018's release report, the rows this review conditions on, and MP-44's
  Ex-O consumption of MP-43's Session-0 decision, which Session 0 consumes
  again.
- [[00_meta/42_micro-phase-42-review-and-roadmap]] · [[00_meta/41_micro-phase-41-review-and-roadmap]] —
  the eleventh and tenth questions' reviews and roadmaps, the un-cap's
  steady state confirmed eight times.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat — and the
  row the terminal state executes.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/positive-control-protocol]] ·
  [[06_production_ai/notes/microscope-trial-table]] — the science C53–C56
  adjudicate over, whose pending verdicts are the intake.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.
