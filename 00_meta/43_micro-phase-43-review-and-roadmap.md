---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-16
---

# Micro-Phase 43 — State Review and Roadmap: the twelfth question, written from the eleventh release report

> **STATUS: REVIEW + ROADMAP, NOT A PRE-REGISTRATION.** This note is the
> companion review to [[00_meta/42_micro-phase-42-review-and-roadmap]], the
> eleventh question's review and roadmap, and to the MP-42 review itself: it
> opens no rows, launches no runs, claims no window, and is wired into home
> only as a companion pointer — it is not a pre-registration and it is not
> counted against any cap, because the cap is spent. It is my personal
> state review and my step-by-step plan for the phase that starts at MP-43's
> Session 0, written in the same first-person register as my progress log so
> it doubles as the public record of how I reasoned about the program's
> steady state before I executed through it. Everything factual in this file
> was re-verified against the repository on 2026-08-16: working tree clean,
> `dev` reconciled with `main` at the MP-42 squash (PR #76, main at
> `4863d66`), 190 tracked tests, ruff clean, `verify-claims` at 0.

## Part I — Where I stand (state review, verified against the repo)

### The scientific ledger

The record's deepest fact has not changed and now has nine dated
confirmations behind it: **no run in this repository's history has ever
produced a sparse Fourier solution.**

- P=59 drills dense 59/59; P=113's three-seed verdict is NO-GROK (val 1.0,
  k_99 = 111/113); the positive-control scan stamped **ALL-DENSE** at
  P=59/67/97 (harness-level negative, val 0.0000–0.0006, gen −1); microscope
  trial 1 **FALSIFIED** (embedding re-normalization is not the suppressor:
  k_99 = 112/113, val 0.7176); trials 2 (`--schedule constant`, the enabler
  landed TDD-first) and 3 (wd 1.5×) are pending in ADR-0003's budget; and the
  R1 standard-scale ×3-seed run COMPLETED 2026-08-14 04:07 local — the
  scheduled no-head negative is the verdict: 0/8 heads, peak diag+1 mass
  0.075 at epoch 499, peak val accuracy 0.5083 near epoch 1950,
  K-composition max 0.056. The R1 verdict is the newest dated fact on the
  record's negative side, re-verified in this drafting sitting.
- The exp2 and exp5 manifests are clean on disk; `verify-claims` at **0**,
  re-verified in the MP-42 drafting sitting and again in this one.

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
record's own successor?* (MP-42's sitting). By MP-43's Session 0 the record
will hold eleven dated directions, a characterized dense regime, a causal
reading (or its evidence lane), whichever of C41–C44 ADR-0016's sitting
chose — and the answer to the question MP-42's Session 0 owned more deeply
than any phase before it: **whether the record's arc reached its terminal
state and, if it did, what the first post-record question was.** The twelfth
question is the first one I choose with the post-record decision itself
*consumed* — or the second question past the record's closing sentence.

### What I found walking the shelf while drafting (five dated intake facts)

Drafted and re-verified against the repository on 2026-08-16. These are
facts the hostile-webmaster walk would catch, recorded here as intake so
they are owned rows, never surprises:

1. **Local `main` is stale.** Verified: local `main` sits at `1acba9e`
   while `origin/main` is at `4863d66` (the MP-42 squash, PR #76) and `dev`
   = `origin/dev` at `d533aa4` (the reconcile merge). The remote is
   reconciled; the local tracking copy lags two squashes. Owned by Session
   1's repo-shelf walk: `git fetch` + `--ff-only`, transcript = the branch
   list before and after.
2. **`portfolio/README.md` is stale.** It still reads "Mini-paper (LaTeX
   PDF) not yet written", "Interactive demo … not built yet", "Experiment
   tracking not set up yet" — contradicted by the record: the paper has
   lived through the v8–v11 arc, the site and Space have been live since
   the premiere, and the manifest machinery has been tracking results since
   Micro-Phase 8. This is exactly the class of drift the shelf baseline
   exists to catch; owned by Session 1 with a dated fix.
3. **No `essay-annex-*.md` exists on disk.** The annexes live on the live
   shelf (site and Space), not in this repository. The v13 annex contract
   must state the artifact's home with a date instead of implying the repo
   holds it.
4. **Rung 6 residue survives on disk.** The deleted Rung 6 (2026-08-01,
   fabricated data) left `exp6_automated_circuit.cpython-312.pyc` in
   `src/experiments/__pycache__/` and `figures/exp6_automated_vs_manual.png`
   in the gitignored figures directory. A hygiene row for Session 1's walk.
5. **`checklists/gate-debt.md` does not exist yet.** The debt ledger is
   promised by named MP-30/31 rows; row 8's re-verification must record its
   absence with a date rather than claim a file that is not there.

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no
phase. MP-37, MP-38, MP-39, MP-40, MP-41 and MP-42 are the un-cap executed
exactly once each — their drafts and reviews on disk, conditioned on their
predecessors' releases. **ADR-0016's eight rows are the rows MP-42 will
fill**; **ADR-0017's eight rows are the rows this roadmap will fill** —
exactly once, under the continuum law, twelfth execution, written from
MP-42's release report rather than from the habit of pre-registering.

### The CI floor and the toolchains

190+ tracked tests, ruff, blocking mypy and markdownlint are green at the
last release; `verify-claims` at 0 — re-verified in this drafting sitting
(2026-08-16): 190 collected, ruff clean, `verify-claims` at 0. The verified
gaps, stated as facts not hopes: no LaTeX toolchain on this machine
(`make paper` is graceful, not green), no Pages deploy workflow in
`.github/workflows/`, no `publish:` frontmatter policy, `portfolio/projects/`
holds figures but no project write-ups, W&B never connected. Each is a dated
row owned by MP-30/31/34/35/36 — their residue, never my re-planning.

### The showcase corpus at intake

12+ provenance-guarded figures, the paper at v8/v11 (the v12 rule is MP-42's,
the v13 rule is this phase's), the site and Space live since the premiere,
the essay annex at v8/v11, eight runnable teaching artifacts with
stranger-run transcripts (the receipts land only if the stack ships: eight
exist only if MP-33–MP-39 execute, the ninth ships in MP-40, the tenth in
MP-41, the eleventh in MP-42, **the twelfth in this phase**). My teaching
lane ships the twelfth artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The intake is now a consumption of a consumption.** MP-40's Ex-N
   defined the terminal state; MP-41's Session 0 executed it; MP-42's
   Session 0 **consumed that execution** and made the deepest choice on the
   record: the C41–C44 adjudication, or the first post-record question from
   PR-1/PR-2/PR-3. MP-43's Session 0 must **consume that choice with
   dates** — the single most dangerous drift is re-litigating a consumed
   decision: re-opening candidates the eleventh question already closed with
   dated reasons, or treating "the post-record arc governs" as a mood
   instead of as a stamped verdict. The decision chain is now three
   generations deep; a sitting stamps, it never re-decides.
2. **The stacked execution is still the critical path.** MP-43's Session 0
   consumes MP-42's release report, which consumes ADR-0016's, which awaits
   MP-29 through MP-40. A slip at any link slides the whole chain; **my
   highest-leverage act is unchanged: protect MP-29's window** — its release
   report is the artifact everything downstream consumes. Nothing in this
   phase may borrow a minute from it, and this draft is written
   verdict-agnostic by law: it re-plans not a single row of MP-29–MP-42.
3. **The steady state is the un-cap's end state, and it must not become
   ceremony.** MP-43 is the sixth roadmap written from an *executed*
   roadmap's release report — the program's normal, confirmed six times.
   The drift risk inverts and deepens: the machinery (ledgers, sessions,
   gate criteria) is now twelve executions deep, so the law's countermeasure
   is that rows must still be dated in the sitting that owns them, verdicts
   still consumed as artifacts, and zero UNDECIDED rows at Session 8 — the
   machinery is the guardrail, never the goal, and a stamped row with no
   science behind it is ceremony by another name.
4. **The paper's compile gate is the hardest artifact in the stack.** No TeX
   on this machine — verified again in this sitting; MP-31's own canon
   applies early: *toolchains are pinned in Session 0, never discovered at
   Session 7.* The paper v13 rule ("opens only for new numbers, else the v12
   is the record") is my insurance — a dated sentence, never a silence.
5. **The standing debt is undated by design and must not survive the
   stack.** exp5 1000-epoch ×3-seed (~15 h), clean-clone proof, graduation
   proof, `reproduce-multiseed`, W&B, the gate-debt transcript — each owned
   by a named row in MP-30–MP-36 and re-verified in MP-37's through MP-42's
   row 8. Row 8 of this phase re-verifies those closures with transcripts; a
   pending item cannot outlive a ledger — and a re-verification cannot claim
   a file that is not there (`gate-debt.md`'s absence is a dated fact, not
   a silence).
6. **The science's next fork is one verdict deeper.** MP-42 adjudicates
   C41–C44 — or opens the post-record arc — from ADR-0015's verdicts;
   MP-43's candidate set is conditioned on *that* verdict — C45 opens only
   on C41's positive reading, C46 only on C42's completed transfer, C47 only
   on C43's dated drift, C48 only on C44's causal graph — and the
   post-record continuation overrides the set if MP-42's Session 0 opened
   the post-record arc. The redemption (a sparse cell found anywhere)
   overrides both. My candidate set is frozen precisely so this fork is
   adjudicated at Session 0, never improvised.
7. **The showcase's receipts are still future, one deeper.** Eight
   stranger-run transcripts exist only if the stack ships; the ninth lands
   in MP-40, the tenth in MP-41, the eleventh in MP-42, the twelfth in this
   phase. C47 (the rate's second drift) is conditioned on ≥ 10 transcripts
   on disk at Session 0 — the receipt compounds only if the lanes execute.
8. **Stop-and-publish is a row, not a threat — and the post-record
   criterion is now two questions deep.** ADR-0004's row 5 (the record
   releases as-is) stays open as the program's honest exit: a phase is worth
   doing only if its candidate set can earn a paragraph the record does not
   already have. Every candidate below must beat that row in the sitting
   that chooses it. The twelfth execution sharpens this to its edge: if
   MP-42's Session 0 opened the post-record arc, the deepest candidate this
   phase can choose is the one that earns the post-record arc's *first new
   paragraph* — the record's closing sentence consumed twice, never
   repeated. The deepest form of laziness is not building what the record
   has already said.

## Part III — The roadmap, step by step (the continuum law, twelfth execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C45 | **The law's boundary** (C41's successor) — the circuit as a law becomes the circuit as a *bounded* law: per-head fingerprints tested where transfer is predicted to fail first — task-structure ablations, P-scaling across the diagram, out-of-distribution composition — universality claimed at the boundary or mapped where it breaks, the failure mode itself the result; the canonical-algorithm statement ("the dense solution is *the* algorithm this harness computes") now carrying its domain of validity | ADR-0016 row 3 = C41 with a positive verdict and transfer fingerprints on disk | C41 closed negative, or the post-record arc governs → the law's boundary belongs to the post-record arc, or the record already has its closing sentence |
| C46 | **The mechanism's driver** (C42's successor) — the dense→memorized sharpening's *driver* isolated: if the mechanism survives architecture change, *what principle* does it express — the order parameters re-read at the norm/loss-landscape axis (weight-norm trajectory as the order parameter, edge-of-stability effects), the driver named as a quantity, not a metaphor, with the dated negative as a verdict | ADR-0016 row 3 = C42 with the completed transfer verdict on disk (principle or architecture effect, manifest-tagged) | C42 never opened, or its verdict was negative → no principle to isolate, this closes with that verdict |
| C47 | **The rate's second drift** (C43's successor) — the sixth reproducibility study: the rate re-measured with artifacts 10+ in the register at Session 0, per-step failures root-caused and fixed with dates, and the drift of the drift measured against the fifth study — a rate measured three times is a drift-of-the-drift number, not an anecdote (does the receipt system's rate keep drifting on an aging codebase?); the verdict is a dated reproducibility report with a rate, a drift and a drift-of-drift, not a mood | ADR-0016 row 3 = C43 with a dated drift on disk AND ≥ 10 stranger-run transcripts at S0 | Fewer than 10 transcripts, or C43 never opened → the receipt system hasn't earned a sixth study |
| C48 | **The feature-complete circuit as a public course** (C44's successor) — the dense solution's complete causal graph (feature → head → frequency → output, every edge causally verified) distilled into the terminal teaching artifact: one runnable lesson per rung, the circuit read like source code at feature resolution by a stranger, with the run-transcript as the receipt | ADR-0016 row 3 = C44 with the causal feature ablations and the tenth artifact's transcript on disk | C44 never opened, or a sparse regime exists → the sparse reading owns the question |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥
3 checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The terminal-state override stands, now three generations deep: **if MP-42's
Session 0 consumed MP-41's execution of MP-40's Ex-N rule and the record
closed, then MP-42's Session 0 opened the post-record arc — and no successor
opens from the old arc. MP-43's Session 0 instead consumes the first
post-record question's verdict from ADR-0016 row 3 and continues the
post-record arc, choosing the second post-record question from the
pre-registered continuation set below.** The rule is executed with dates at
Session 0; it is never improvised and never re-negotiated in the sitting
that consumes it.

### The post-record continuation set (chosen only if MP-42 opened the post-record arc)

| # | Candidate | Why it would open | Why it would close |
|---|---|---|---|
| PR-4 | **The new harness's first verdict** (PR-1's successor) — the sparse question at its new address: the record's complete dense law and the microscope's dated findings as the new harness's specification, the first recipe run under the record's laws, the verdict read from a fresh manifest — the phenomenon's question answered at the address the record's negatives opened | The post-record arc opened at MP-42 with PR-1's verdict on disk | The record never closed, or the redemption fired first → the sparse question belongs to the old arc |
| PR-5 | **The law at the record's edge, second task** (PR-2's successor) — the frozen-checkpoint predictions tested at the second unseen task family, the record's laws as the post-record arc's second out-of-sample point: a law that predicts twice is a law; a law that breaks is a boundary | The post-record arc opened at MP-42 with PR-2's verdict on disk | The record never closed → the law's successors are C45's, not the post-record arc's |
| PR-6 | **The record as a course** (PR-3's successor) — the closed record's teaching corpus distilled into the definitive public course: the twelve runnable artifacts and the complete circuit assembled into the showcase's terminal teaching artifact, one lesson per dated direction | The post-record arc opened at MP-42 with PR-3's verdict on disk | The record never closed → the teaching lane continues as the continuum's row 7 |

The likely survivor, written as a condition chain, never a prediction: if
MP-42's Session 0 opened the post-record arc → **the post-record
continuation** — the second question past the record, chosen in the
consuming sitting from PR-4/PR-5/PR-6; else if C41 landed positive → **C45**
— the law extended to its boundary, always CPU-runnable on checkpoints that
exist today; else if C42's transfer verdict landed → **C46**; else **C47**
(always-runnable, the showcase's own science, receipts now ten deep); C48 is
the evidence lane and the teaching lane's anchor.

### The nine sessions

1. **Session 0 (~1 h) — the gate truthing + the arc consumption + the
   continuum choice.** Consume MP-42's release report row by row:
   ADR-0016 at zero UNDECIDED rows, the live URL re-clicked in the sitting,
   `verify-claims` at its actual count, the tenth teaching transcript on
   disk, `dev == main`. Commit the intake table before a single continuum
   row opens. Then **Ex-N: consume MP-42's Session-0 decision with dates** —
   the second-generation consumption: if the post-record arc opened, the
   first post-record question's verdict is read from ADR-0016 row 3 and the
   second post-record question chosen from the pre-registered continuation
   set (PR-4/PR-5/PR-6), each opening-or-closure memo in three sentences
   with a falsifier; if not, the C45–C48 adjudication: exactly one opens as
   row 3, the unchosen close with one dated reason each, stamped in the
   same sitting. Open ADR-0017 with its eight rows, windows and kill-dates;
   declare the terminus (release = merge + 14 calendar days); promote this
   roadmap from MP-42's release report, deviations recorded as dated ledger
   notes. *Exit: intake signed; the arc consumption executed; row 3 chosen
   (or the post-record continuation row opened); ledger open.*
2. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — year eleven begins with a baseline — extended
   to the repo's own shelf: local `main` reconciled to `origin/main`
   (`git fetch` + `--ff-only`, transcript = the branch list before and
   after), `portfolio/README.md`'s staleness fixed with a dated edit, the
   exp6 residue removed, the annexes' location verified. Row 8: MP-42's
   stamped closures re-verified (W&B, clean-clone proof, graduation proof,
   `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch resolution) — each
   cell LAUNCHED-with-transcript or CLOSED-with-one-reason; a claimed
   closure without its transcript stays open and blocks Session 8;
   `gate-debt.md`'s absence, if still absent, recorded with a date. *Exit:
   rows 5 and 8 stamped.*
3. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the eleventh research question's verdict (ADR-0016 row 3) becomes the
   paper-v13 section, the annex table, or the results-page row — every
   number manifest-tagged, consumed in the sitting that owns it; if the
   post-record arc governs, the post-record statement is framed from MP-42's
   release, never rewritten. Row 2: v13 opens only if row 1 lands new
   numbers; else "the v12 is the record" is the dated reason and `make
   paper` is re-verified against v12. Row 6's substitute filed from the
   visitor's chair, before the window opens (Ex-G); the fork drill (Ex-H)
   and the arc consumption (Ex-N) land here. *Exit: rows 1 and 2 dated;
   substitute filed; Ex-N's execution memo on disk.*
4. **Session 3 (~2–3 h) — the essay annex v13.** `portfolio/essay-annex-13.md`
   (its home on the live shelf, dated): the eleventh question's verdict set
   and the teaching lane's tenth receipt distilled into one dated annex;
   the reverse claims audit at zero (prose → manifest → command); each
   claim's "what would falsify this" column filled at writing time. The
   annex is amended, never rewritten. *Exit: row 4 dated; audit at zero.*
5. **Session 4 (~1 h) — the stranger round 13 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. *Exit: window open,
   kill-date declared.*
6. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat — or, if the post-record
   arc governs, the continuation row's protocol opened under the same
   discipline. If C45: the expected boundary fingerprints, the
   universality bound's failure modes, and the transfer verdict all written
   as falsifiable predictions before a single number is read (Ex-C, Ex-I,
   Ex-J). Row 6's kill-date honored (feedback → matrix drafted; silence →
   substitute closes it). Row 7: the twelfth teaching artifact's skeleton
   drafted — walkthrough v12, 10-minute talk v12, or Colab grokking
   notebook v10 — with its ship-date. *Exit: row 3 pre-registered and
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
   twelfth artifact runs end to end on a stranger's machine (fresh clone /
   Colab session); the run transcript is the receipt; the teaching
   distillation (Ex-F) lands here. *Exit: rows 5, 6, 7 dated; the artifact
   shipped with its transcript.*
9. **Session 8 (~1 h) — the release.** ADR-0017 at zero UNDECIDED rows; the
   merge green locally and on GitHub; `dev == main`; home wired — this
   roadmap's companion status retired; the roadmap archived with its
   deviations, every deviation a dated ledger note. If the post-record arc
   governs, this sitting stamps the post-record arc's second dated
   direction — the record's closing sentence consumed twice, never
   repeated. *Exit: the merge; the program's twelfth dated direction — or
   the post-record arc's second.*

### The one measured line

ADR-0017 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row (or the post-record continuation row) whose verdict (or
scheduled negative) re-derives from a manifest; `verify-claims` at 0 with
every public number re-derivable from one command line; the hostile-webmaster
walk at zero on the live shelf, year eleven, and on the repo's own shelf
(local `main` reconciled, README current, residue removed); the twelfth
teaching artifact shipped with a stranger-runnable transcript; `dev == main`
and the program's twelfth dated direction — or, if the post-record arc
governs, its second dated direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk.

1. **The law's boundary (the C45 reading).** Elhage et al., *A Mathematical
   Framework for Transformer Circuits* (2021) for the QK/OV machinery the
   transfer is claimed over; Chughtai et al., *A Toy Model of Universality*
   (2023) for what "the same algorithm" can honestly mean *across unseen
   tasks*; Olsson et al., *In-context Learning and Induction Heads* (2022)
   for what transfers across task families — now read at the *failure* axis:
   where universality claims overreach, what a task-structure ablation
   changes, and the OOD/grokking line (Power et al. 2022; Nanda et al. 2023)
   for what a circuit-as-a-law predicts when the task's structure shifts. My
   C41 verdict and its transfer fingerprints frame the reading. **Prediction
   to write before the analysis**: the boundary cells — which fingerprint
   components fail first at the unseen task's structure; the mapped
   breakdown; the transfer verdict. **Primary sources**: the frozen
   checkpoints, C41's fingerprint table, the S3 note.
2. **The mechanism's driver (the C46 reading).** Morwani et al. (2024) on
   the edge-of-numerical-stability regime, Gromov, *Grokking: A Memory
   Perspective* (2023), Power et al. (2022), Nanda et al. (2023) — now read
   at the *norm/loss-landscape* axis: what quantity the sharpening follows
   across architecture families (weight-norm trajectory as the order
   parameter, edge-of-stability effects), and where "the driver" is really a
   loss-landscape artifact. **Prediction**: the order-parameter dynamics as
   functions of architecture-independent quantities, written with
   falsifiers; C42's transfer verdict is this reading's admission ticket.
3. **Longitudinal reproducibility, the drift of the drift (the C47
   reading).** Gelman & Loken, *The Garden of Forking Paths*; Pineau et al.
   (2021); the ML reproducibility line (NASEM's five pillars) — what a
   drift-of-a-drift claims when a rate is measured *three times in a row on
   an aging codebase*: does the receipt system's rate keep drifting, and
   what does a second drift mean? My ten stranger-run transcripts are the
   data; the fifth study defined the first drift, I must decide what counts
   as the second before I measure any.
4. **Feature-complete circuits as a public course (the C48 reading).**
   Bricken et al. (2023); Cunningham et al. (2024); the dictionary-circuit
   and feature-universality line — what it takes to claim a *complete*
   causal graph at feature resolution (feature → head → frequency → output),
   where SAE readings on dense circuits have been shown to overreach, and
   how a complete feature-level graph becomes a *course* — one runnable
   lesson per rung — rather than a poster. My Rung-5 datum (99.97% FVE,
   L0 = 136/256, 0% dead features) is the record's first data point.
5. **The post-record program, second generation (new, deepest).** Lakatos,
   *The Methodology of Scientific Research Programmes* (1978) — read a
   third time, now for the *second* question past a completed program:
   progressive vs degenerating problem shifts when the first post-record
   verdict lands, Kuhn's normal science as the post-record arc's axioms, and
   the honest criterion for the second post-record question — a question
   that must earn the post-record arc's first *new* paragraph. This reading
   feeds Ex-N and the Session-0 question MP-43 owns more deeply than any
   phase before it: *what does the record's first post-record verdict open?*
   The answer can be the post-record arc's second dated row — Lakatos' point
   is that the decision is made on the record, never as a mood.
6. **The record teaches, round twelve.** The twelfth verdict in four
   registers — the paper's sentence, the annex's sentence, the 30-second
   spoken claim, and the 5-minute teaching explanation with a worked toy a
   stranger can run; the gap between the last two is where my teaching
   leaks, and I will measure it deliberately by writing all four registers
   for the same verdict (Ex-F).
7. **The redemption reading, or negative results as maps, the twelfth
   pass.** If a sparse cell exists by S0: Nanda et al.'s full per-frequency
   reading on the first sparse solution this harness ever produced. If not:
   how the *completed* law is reported honestly — the boundary mapped, the
   driver named, the drift numbers dated, the negative as a contribution —
   and how the post-record harness (if PR-4 governs) would be designed from
   the dated negatives instead of from hope. Either way, the paper's hardest
   paragraph is the one that claims the dense solution *computes
   something*; I will draft it against this reading and let the manifest
   referee it.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-42's release report, deviations recorded as dated ledger
  notes.
- **ADR-0017**, the twelfth continuum ledger — eight rows pre-stamped with
  windows and kill-dates; rows 1–2 consumed from ADR-0016's verdicts; row 3
  the twelfth research question with its protocol note and heartbeat (or
  the post-record continuation row's protocol); rows 4–8 the continuum's
  decisions.
- **`portfolio/essay-annex-13.md`** — the v13 annex, manifest-tagged,
  amended never rewritten; the annexes' home (the live shelf) recorded with
  a date.
- **The paper v13 diff** (`portfolio/paper/main.tex` v13 + diff log) or the
  dated "the v12 is the record" memo; `make paper` re-verified in the CI
  mirror.
- **The shelf health sheet + hostile-webmaster transcript** (site + Space at
  zero, year eleven), extended to the repo's own shelf: local `main`
  reconciled to `origin/main`, `portfolio/README.md` current, the exp6
  residue removed, the annexes' location verified; the claims gate re-run
  on every merge.
- **`checklists/gate-debt.md`** — each cell's transcript or one-line reason,
  dated in Session 1, including the exp5 1000-epoch resolution's receipt
  re-checked; the file's absence, if still absent, recorded with a date.
- **The research row's pre-registration note** (site, metric, negative
  control, kill-date) in `06_production_ai/notes/` + the heartbeat artifact;
  if C45: the boundary-fingerprint figure spec written before the analysis,
  the figure itself manifest-tagged after. If the post-record arc governs:
  the continuation row's protocol note instead.
- **The twelfth teaching artifact + its stranger-run transcript**
  (fresh-clone or Colab session receipt).
- **Ex-N's execution memo** — MP-42's arc decision run with dates: the
  post-record verdict consumed or the C45–C48 adjudication executed, the
  criteria cited, the decision that follows (the second post-record
  question, or the continuation), written verdict-agnostic in Session 2 and
  executed at Session 0.
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C45–C48 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting — preceded by the arc consumption (Ex-N), which may make the
   whole set close with the post-record verdict.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0016's row-3 verdict traced to its manifest and its command; the rest
   struck with a reason — the hostile-webmaster test of my own prose,
   eleventh run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C45 or C46 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the boundary cells at the unseen task's structure, the
   universality bound's failure modes, the driver's order-parameter
   dynamics — the "what would falsify this" column filled at writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v13 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, year eleven, with the repo's own shelf added: branches
   reconciled, README current, residue removed.
6. **Ex-F · The teaching distillation, round twelve (S7):** the twelfth
   question's verdict in four registers — the paper's sentence, the annex's
   sentence, the 30-second spoken claim, the 5-minute teaching explanation
   with a worked toy a stranger can run; the gap between the last two is
   where my teaching leaks.
7. **Ex-G · The stranger substitute from the visitor's chair (S2):** the
   self-review written from the chair a stranger would occupy — friction
   points → fixes → re-check row — filed before S4, so the S5 kill-date can
   never close the row with a skip.
8. **Ex-H · The fork drill, deepest form (S2, verdict-agnostic):** the
   continuing state (C45–C48) vs the post-record state (PR-4/PR-5/PR-6)
   written as two one-page paths — what each verdict changes downstream,
   including the C45-vs-C46 choice and the post-record continuation choice —
   so next phase's S0 decision is a stamping, not a discovery.
9. **Ex-I · The boundary hand-roll (S5, C45 only, before any number is
   read):** the expected boundary fingerprint at the unseen task's structure
   written by hand from the C41 law — which per-head roles must transfer
   unchanged, which may re-tune, which should fail first — the null
   hypothesis every measured fingerprint is compared against. One runnable
   check: the hand-rolled fingerprints printed and saved next to Ex-J's
   observed ones, so the S6 comparison is a diff, not a memory.
10. **Ex-J · The transfer reader (S5, C45 only):** the script that loads the
    frozen checkpoints at every P (including the unseen task's), runs C41's
    per-head extraction and patching machinery, and emits the fingerprint
    table as a manifest-tagged JSON. One runnable check: the reader runs on
    the frozen checkpoints and its output is committed before the verdict
    paragraph is drafted.
11. **Ex-K · The sparse-recovery toy, revisited a sixth time (my foundation
    challenge, driver pass):** the one-file toy that recovers the addition
    table's DFT coefficients under L2 vs L1 penalties, now extended to the
    driver question: *where in (wd, P, architecture) does the L2-minimal
    solution stop generalizing, and does its weight-norm trajectory at the
    transition change when the model family does?* One runnable check: the
    toy prints both reconstructions' sparsity and error plus the norm
    trajectory on a fixed seed, across two architectures. This is the
    micro-scale intuition C46's verdict must not contradict.
12. **Ex-L · The "what does the dense solution compute?" sprint, round six
    (S5, C45 only):** the paper's hardest paragraph drafted at S5, then
    audited against the mechanism reading at S6 — prose that must survive
    contact with the manifest, the "computes something" claim earned or
    struck with one reason.
13. **Ex-M · The stranger-run drill on my own receipt (S1):** I execute the
    previous phase's shipped artifact (the tenth) on a fresh clone as if I
    were the stranger — the transcript becomes the baseline against which
    the twelfth artifact's transcript is compared. One runnable check: the
    baseline transcript saved beside the new one.
14. **Ex-N · The arc consumption, second generation (S0, new,
    verdict-agnostic):** MP-40's Ex-N defined the terminal state; MP-41
    executed it; MP-42 consumed that execution and chose; this drill
    *consumes that choice with dates* — the post-record verdict read from
    ADR-0016 row 3 if the arc opened, the criteria cited, the release that
    follows (the second post-record question, or the C45–C48
    adjudication), and what each of ADR-0016's possible verdicts changes in
    that execution. One runnable check: the execution memo exists, names
    the decision rule that closes or continues the program's science, and
    cites the criteria from MP-42's release report.
15. **Habit · The clock check (every session):** ADR-0017's undated rows,
    the open PR's CI status line, the shelf's health — all three before any
    new prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, twelfth execution.** A phase that opens two
  research questions is drift by another name; the unchosen candidates close
  in the same sitting as the choice — and the arc consumption may close all
  of them with the post-record verdict. The continuum law is the mechanical
  refusal of this drift — proven executable eleven times, it must simply be
  executed again.
- **The candidate set is frozen before S0, never improvised at it.** C45–C48
  are conditions, not predictions; a sitting decides, it never invents — and
  the terminal-state object is the hardest frozen object on the record:
  written by MP-40, executed by MP-41, consumed by MP-42, *consumed again*
  by MP-43 — never re-negotiated in the consuming sitting.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0016's row-3 verdict in the sitting that owns
  it — or the post-record statement, if the arc governs.
- **The receipt compounds.** The twelfth runnable artifact is only worth
  shipping because the first eleven transcripts proved the format — and if
  C47 opens, the receipts are a drift-of-the-drift number measured three
  times in a row, tested by someone I did not choose, across an aging
  codebase. My showcase's story is now "read it, run it, watch me be wrong
  on the record," twelve receipts deep.
- **The steady state is the reward, not the ceremony.** MP-43 is the sixth
  roadmap written from an *executed* roadmap's release report — the program
  at its normal, confirmed six times. The cap's lesson was that promises
  without dates drift; the steady state's discipline is that the machinery
  never becomes the goal: rows are dated in the sitting that owns them, or
  they are not rows.
- **Stop-and-publish stays open, and the post-record criterion is now two
  questions deep.** ADR-0004's row 5 is the honest exit; a candidate set
  that cannot earn a paragraph the record lacks is a phase that should close
  itself. If the post-record arc governs, the deepest candidate earns the
  post-record arc's *first new paragraph* — the record's closing sentence
  consumed twice, never repeated. This is the deepest form of laziness: do
  not build what the record has already said.
- **Toolchains are pinned in S0, never discovered at S7.** The paper's
  compile gate is the hardest artifact in the stack; the v13 rule ("opens
  only for new numbers") is the insurance that makes a missing toolchain a
  dated reason, not a crisis.
- **Protect the release report.** The serialized stack means MP-29's release
  is the artifact everything downstream consumes; a slip at any link slides
  the whole chain. The deepest law still applies: a promise can be
  re-planned forever, but a dated row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0016 at zero, the live
  URL, `verify-claims` at 0, the tenth teaching transcript on disk — a
  condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; the R1 no-head negative — 0/8
  heads, stamped 2026-08-14 — is the record's newest dated signature, the
  evidence lane's scheduled verdict, and the record's closing sentence — if
  it lands — is the strongest form of the signature: a negative that became
  a map, a map that became a characterization, a characterization that
  became a mechanism, a mechanism that earned its causal verdict, a circuit
  that earned its complete reading, a circuit that earned its law, a law
  that predicted an unseen point — or a record that knew when to end.
- **The debt row re-verifies; it never re-does.** A stamped closure is
  re-checked with its transcript; a genuinely new debt cell is a NEW row,
  never a revision. A pending item cannot outlive a ledger — and a
  re-verification cannot claim a file that is not there.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED
  rows at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story:** *the program's twelfth dated direction
  was written from its own release report — the cap honored, the stack
  executed, the steady state kept honest six times, the record taught twelve
  times in runnable artifacts, every public number still re-derives from
  one command line, and the record consumed — twice, with dates — its own
  terminal-state decision, and answered it in a release.* Every artifact
  this phase launches is written to that standard.

## Links

- [[00_meta/42_micro-phase-42-review-and-roadmap]] · [[00_meta/41_micro-phase-41-review-and-roadmap]] —
  the eleventh question's review and roadmap; this roadmap's intake is
  ADR-0016's release report, the rows this review conditions on, and MP-42's
  Ex-N consumption of MP-41's terminal-state execution, which Session 0
  consumes again.
- [[00_meta/40_micro-phase-40-review-and-roadmap]] · [[00_meta/39_micro-phase-39-review-and-roadmap]] —
  the eighth and ninth questions' reviews and roadmaps, the un-cap's
  steady state confirmed six times.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat — and the
  row the terminal state executes.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/positive-control-protocol]] ·
  [[06_production_ai/notes/microscope-trial-table]] — the science C45–C48
  adjudicate over, whose pending verdicts are the intake.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.