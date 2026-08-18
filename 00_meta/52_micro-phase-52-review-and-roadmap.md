---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-18
---

# Micro-Phase 52 — State Review and Roadmap: the twenty-first question, written from the twentieth release report

> **STATUS: REVIEW + ROADMAP, NOT A PRE-REGISTRATION.** This note is the
> companion review to [[00_meta/51_micro-phase-51-review-and-roadmap]], the
> twentieth question's review and roadmap: it opens no rows, launches no
> runs, claims no window, and is wired into home only as a companion pointer —
> it is not a pre-registration and it is not counted against any cap, because
> the cap is spent. It is my personal state review and my step-by-step plan
> for the phase that starts at MP-52's Session 0, written in the same
> first-person register as my progress log so it doubles as the public record
> of how I reasoned about the program's steady state while MP-51's waiting
> window was still open. Everything factual in this file was re-verified
> against the repository on 2026-08-18: working tree clean, local `dev` at
> `6f57ed4` (reconciled after the MP-51 squash, PR #86), `git diff main dev`
> empty, 190 tracked tests collected, ruff clean, blocking mypy clean,
> `verify-claims` at 0.

## Part I — Where I stand (state review, verified against the repo)

### The scientific ledger

The record's deepest fact has not changed and still has twelve dated
confirmations behind it, re-verified in this drafting sitting: **no run in
this repository's history has ever produced a sparse Fourier solution.** The
count advances only with a new verdict; between MP-51's sitting and this one,
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
(MP-38 through MP-50's sittings) → *which of C77–C80 does the consumed
twentieth verdict open — or is the tenth post-record question the post-record
arc's own successor?* (MP-51's sitting). By MP-52's Session 0 the record will
hold twenty dated directions, a characterized dense regime (or the sparse
redemption), whichever of C77–C80 ADR-0025's sitting chose — and the answer
to the question MP-51's Session 0 owned more deeply than any phase before it:
**whether the post-record arc governs and, if it does, what the tenth
post-record question was.** The twenty-first question is the eighth I choose
with the seventh-generation arc consumption *stamped* — or the eleventh
question past the record's closing sentence.

### What I found walking the shelf while drafting (verified intake facts)

Drafted and re-verified against the repository on 2026-08-18 — the facts a
hostile-webmaster walk would catch, each stamped with its state in this
sitting so the intake is a re-verification, never a memory:

1. **MP-51's roadmap is merged.** Verified: local `dev` sits at `6f57ed4`,
   reconciled after the MP-51 squash (PR #86), and `git diff main dev` is
   empty. MP-51's own intake facts are closed by its merge; Session 1's walk
   re-verifies with the branch list as the transcript.
2. **`portfolio/README.md` is still stale.** Re-verified: it still reads
   "Mini-paper (LaTeX PDF) not yet written", "Interactive demo … not built
   yet", "Experiment tracking … not set up yet" — contradicted by the record:
   the paper has lived through the v8–v20 arc (the v21 rule is MP-51's, the
   v22 rule is this phase's), the site and Space have been live since the
   premiere, and the manifest machinery has been tracking results since
   Micro-Phase 8. MP-51's Session 1 owns the dated fix; this phase's
   Session 1 re-verifies the closure with the dated file itself.
3. **No `essay-annex-*.md` exists on disk.** Re-verified: `portfolio/` holds
   `RESULTS.md`, `README.md`, `model-card.md`, `paper/` and `projects/` and
   nothing else. The annexes live on the live shelf (site and Space), not in
   this repository. The v22 annex contract must state the artifact's home
   with a date instead of implying the repo holds it — and this phase adds
   the repo-side snapshot rule (Ex-Φ) so the record survives the shelf.
4. **Rung 6 residue still survives on disk.** Re-verified: the deleted
   Rung 6 (2026-08-01, fabricated data) left
   `src/experiments/__pycache__/exp6_automated_circuit.cpython-312.pyc` and
   `figures/exp6_automated_vs_manual.png` in the gitignored directories
   (both confirmed present 2026-08-18). MP-51's Session 1 owns the removal
   with a transcript; this phase re-verifies the absence.
5. **`checklists/gate-debt.md` still does not exist.** Re-verified:
   `checklists/` holds `reproducibility-checklist.md` and nothing else. Row
   8's re-verification must record the absence with a date rather than claim
   a file that is not there.

Two further verified shelf facts. First: **`figures/` holds zero tracked
files** (`git ls-files figures/` empty) while `portfolio/figures/` holds the
twelve tracked figures — the showcase corpus is gitignored build product,
regenerated by `make reproduce` and provenanced by the manifests, never by
git; this phase's Session 1 adds the figure-regeneration audit (Ex-Ω) so the
corpus is re-derived, never assumed. Second: **`docs/adr/` holds 0001–0010
and nothing else** — the stacked phases' ledgers (ADR-0011 through ADR-0025)
do not exist on disk because they open at their own Session 0s; **ADR-0026's
eight rows are the rows this roadmap will fill**, and this phase's Session 0
opens it exactly once.

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no phase.
MP-37 through MP-51 are the un-cap's roadmap drafts executed exactly once
each. **MP-51's review and roadmap are merged, its Session −1 study lane owns
the waiting window, and its Session 0 awaits the stack's release.**
**ADR-0025's eight rows are the rows MP-51 will fill**; **ADR-0026's eight
rows are the rows this roadmap will fill** — exactly once, under the
continuum law, twenty-first execution, written from MP-51's release report
rather than from the habit of pre-registering.

### The CI floor and the toolchains

190 tracked tests, ruff, blocking mypy and markdownlint are green at the last
release; `verify-claims` at 0 — re-verified in this drafting sitting
(2026-08-18): 190 collected, ruff clean on `src/` and `tests/`, blocking mypy
clean on the allowlist, `verify-claims` at 0. The verified gaps, stated as
facts not hopes: no LaTeX toolchain on this machine (`make paper` is
graceful, not green), no Pages deploy workflow in `.github/workflows/`, no
`publish:` frontmatter policy, `portfolio/projects/` holds figures but no
project write-ups, W&B never connected. Each is a dated row owned by named
rows of earlier phases — their residue, never my re-planning. The
`typecheck-new` ratchet remains the house rule for all new research code — a
module that touches the manifest machinery lands in the strict allowlist
(`src/results.py`, `src/experiments/runner.py`) or it stays out of the
blocking gate with its error count recorded.

### The showcase corpus at intake

12+ provenance-guarded figures, the paper through the v20 arc (the v21 rule
is MP-51's, the v22 rule is this phase's), the site and Space live since the
premiere, the essay annex through the v20 arc, twenty runnable teaching
artifacts with stranger-run transcripts (the receipts land only if the stack
ships: the twentieth ships in MP-51, **the twenty-first in this phase**). My
teaching lane ships the twenty-first artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The intake is a consumption twelve generations deep.** MP-52's Session 0
   must **consume MP-51's Session-0 decision with dates** — the single most
   dangerous drift is re-litigating a decision already consumed eleven times:
   re-opening candidates the twentieth question already closed with dated
   reasons, or treating "the post-record arc governs" as a mood instead of as
   a stamped verdict. The decision chain is now twelve generations deep; a
   sitting stamps, it never re-decides.
2. **The stacked execution is still the critical path — and its head is
   still MP-29.** MP-52's Session 0 consumes MP-51's release report, which
   awaits the stack. A slip at any link slides the whole chain; **my
   highest-leverage act is unchanged: protect MP-29's window** — its release
   report is the artifact everything downstream consumes. Nothing in this
   phase may borrow a minute from it, and this draft is written
   verdict-agnostic by law: it re-plans not a single row of MP-29 through
   MP-51.
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
   negative drafted while the run is live. The pending-run budget stands:
   trial 2 and trial 3 at ~2.5 s/epoch × 5000 epochs ≈ 3.5 h wall each, the
   characterization reads from frozen checkpoints at ~1–2 h, the SAE re-run
   at ~1 h — all three fit overnight windows if launched before the window
   opens, none fit a weekday morning.
6. **The steady state must not become ceremony.** MP-52 will be the
   fifteenth roadmap written from an *executed* roadmap's release report —
   the program's normal, confirmed fourteen times. The countermeasure is
   concrete: **every session's exit names at least one artifact changed on
   disk, and every row is dated in the sitting that owns it** — a stamped row
   with no science behind it is ceremony by another name.
7. **The paper's compile gate finally becomes executable — which makes its
   drift subtler.** By this phase's Session 0, MP-51's Session 0 should have
   pinned the toolchain (the MiKTeX + CI-mirror TeX Live recommendation).
   The new risk is not a missing toolchain but a *ceremonial* one: the gate
   "passes" because `make paper` is graceful-by-design, and the v22 rule
   ("opens only for new numbers, else the v21 is the record") becomes a way
   to never compile. The countermeasure: Session 1 verifies `make paper`
   green on this machine **and** in the CI mirror with a dated transcript — a
   compile that produces a PDF, not a message.
8. **Stop-and-publish is a row, not a threat — and the post-record criterion
   is now eleven questions deep.** ADR-0004's row 5 stays open as the
   program's honest exit: a phase is worth doing only if its candidate set
   can earn a paragraph the record does not already have. If MP-51's Session
   0 continued the post-record arc, the deepest candidate this phase can
   choose earns the post-record arc's *tenth new paragraph* — the record's
   closing sentence consumed eleven times, never repeated. The deepest form
   of laziness is building what the record has already said.
9. **Path patching may still be validated only by unit tests.** The R1
   no-head negative means the R4/R5 chain closes with scheduled negatives;
   head ablation and path patching remain unvalidated end-to-end until a
   confirmed head exists anywhere on the record. If C77 opened in MP-51, its
   patching verdicts were the first chance to close this gap — the intake
   tells me which. If the gap persists, C81's/C82's patching verdicts are the
   next chance; the protocol note must state explicitly which patching
   machinery is being validated for the first time, so the verdict doubles
   as an instrument validation or a dated instrument negative.
10. **The annexes live only on the live shelf — a hosting-side loss would
    erase part of the record (new this sitting).** The v21 annex contract
    states the artifact's home with a date; the risk is that "the live shelf"
    is a single point of failure. This phase adds a dated snapshot rule: each
    annex is mirrored into the repo's `portfolio/` as a dated, read-only copy
    at the annex's own writing session (Ex-Φ), so the record survives the
    shelf — and `verify-claims` can check the pair.
11. **Figure provenance is silently re-derivable, never re-derived (new this
    sitting).** The twelve tracked figures in `portfolio/figures/` are
    provenanced by manifests, but nothing re-runs `make reproduce` on a
    schedule; a figure that no longer regenerates from the committed config
    is a silent lie wearing a manifest tag. Session 1's shelf walk adds the
    figure-regeneration audit (Ex-Ω) to the hostile-webmaster transcript.

## Part III — The roadmap, step by step (the continuum law, twenty-first execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C81 | **The paradigm confirmed, or its boundary mapped** (C77's successor) — the failure-cell theory *predicted a fifth time*: the per-head mechanism at the sixth unseen task family's and the fifth architecture family's failure cells written as falsifiable predictions before any number is read, causally verified by patching, the theory's domain statement extended from "predicts unseen cells four times" to "predicts unseen cells five times" — a paradigm that survives a fifth prediction is a theory with a confirmed domain; a paradigm that breaks on its fifth round is a boundary with a map, and the map is the result | ADR-0025 row 3 = C77 with a positive verdict (the fourth prediction on disk) | C77 closed negative, or the post-record arc governs → the theory's fifth round belongs to the post-record arc |
| C82 | **The equation of state's first transfer** (C78's successor) — the full P×wd×recipe×architecture space *used*: the root-cause map closed at four recipes now asked what it can do — the fifth recipe's failure cells *predicted from the map before the recipe runs*, each prediction ablated or mapped, the equation of state earning its name by transfer, not by accumulation — a boundary that predicts its own fifth recipe is an equation of state; a boundary that re-measures is a phase diagram, and the diagram is the result | ADR-0025 row 3 = C78 with the fourth-recipe closure on disk | C78 never opened, or its verdict was negative → no equation of state to transfer |
| C83 | **The institution, fifteenth study** (C79's successor) — the tenth drift measurement after the ninth dated fix, the rate function's parameters re-estimated from the receipt system's history, the next measurement's schedule *predicted before it happens* and the policy *enforced* across the stack's own execution window a fourth time — an institution that survived four enforcement windows is a constitution that keeps its own schedule; a discipline that predicted three times and kept its date is an institution, and the institution is the result | ADR-0025 row 3 = C79 with the ninth measurement and attribution on disk AND ≥ 21 stranger-run transcripts at S0 | Fewer than 21 transcripts, or C79 never opened → the receipt system hasn't earned a fifteenth study |
| C84 | **The standard, seventh cohort** (C80's successor) — the sixth-edition course *validated a seventh time by the uninvited* under the rubric *already released as a standalone artifact others can run*: the scoring rule's fifth prediction round checked against the seventh cohort's friction, the feedback-to-fixes matrix's fifth prediction round executed — an instrument validated six times by the uninvited is the standard others cite; an instrument validated five times is a standard with a track record | ADR-0025 row 3 = C80 with the seventh cohort's measured outcome on disk | C80 never opened, or a sparse regime exists → the sparse reading owns the question |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥
3 checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The terminal-state override stands, now twelve generations deep: **if MP-51's
Session 0 consumed MP-50's decision with dates and the post-record arc
governs, then MP-52's Session 0 consumes the tenth post-record question's
verdict from ADR-0025 row 3 and continues the post-record arc, choosing the
eleventh post-record question from the pre-registered continuation set below.**
The rule is executed with dates at Session 0; it is never improvised and
never re-negotiated in the sitting that consumes it.

### The post-record continuation set (chosen only if MP-51 continued the post-record arc)

| # | Candidate | Why it would open | Why it would close |
|---|---|---|---|
| PR-31 | **The new harness's sixth cross-recipe law** (PR-28's successor) — the *eighth* recipe at the new address replicated across seeds and compared to the first seven under the record's laws: eight recipes compared across seeds is the harness's sixth law datum; seven recipes compared once is a fifth datum, and the datum is the result | The post-record arc continued at MP-51 with PR-28's verdict on disk | The record never closed, or the redemption fired first → the sparse question belongs to the old arc |
| PR-32 | **The law at the record's edge, eleventh task** (PR-29's successor) — the frozen-checkpoint predictions tested at the eleventh unseen task family: a law that predicts eleven times is a law with a predictive record; a law that breaks is a boundary with a map | The post-record arc continued at MP-51 with PR-29's verdict on disk | The record never closed → the law's successors are C81's, not the post-record arc's |
| PR-33 | **The record as a course, tenth edition** (PR-30's successor) — the ninth edition revised from its eighth intake: the feedback-to-fixes matrix executed with dates, the twenty-one runnable artifacts assembled, the tenth edition measured as a learning instrument with nine cohorts — a course revised from its receipts nine times is a curriculum; a course re-shown is a poster | The post-record arc continued at MP-51 with PR-30's verdict on disk | The record never closed → the teaching lane continues as the continuum's row 8 |

The likely survivor, written as a condition chain, never a prediction: if
MP-51's Session 0 continued the post-record arc → **the post-record
continuation** — the eleventh question past the record, chosen in the
consuming sitting from PR-31/PR-32/PR-33; else if C77 landed positive →
**C81** — the paradigm's fifth prediction, always CPU-runnable on checkpoints
that exist today; else if C78's fourth-recipe closure landed → **C82**; else
**C83** (always-runnable, the showcase's own science, receipts now
twenty-one deep); C84 is the evidence lane and the teaching lane's anchor.

### The pending-run wall-clock budget (verified against observed rates)

The runs the stack still owns, budgeted from observed wall-clock rates so no
launch is ever a discovery:

| Run | Observed rate | Budget | Window discipline |
|---|---|---|---|
| Microscope trial 2 (`--schedule constant`, P=113, seed 0) | ~2.5 s/epoch (micro1) | ~3.5 h for 5000 epochs | Launch at window open; heartbeat; checkpoint-every-500 |
| Microscope trial 3 (wd 1.5×, P=113, seed 0) | same | ~3.5 h | Drafted in the waiting window; verdict forces the choice, never the schedule |
| Dense characterization (per-head dictionaries, ablations on frozen checkpoints) | reads only | ~1–2 h | Session 3, reads from disk, no training |
| SAE re-run on a confirmed-head checkpoint (ADR-0003 row 5) | exp5 rates | ~1 h | Only if a head exists; else the scheduled negative is the result |

### The sessions

1. **Session −1 (~1 h/day, now → the stack's release) — the waiting-window
   study lane.** The days before MP-51's Session 0 are owned, not idle. Each
   day: one study block from Part IV (reading → prediction written *before*
   the reading → one-page memo filed in the study log — each memo linking at
   least two notes, per the vault's orphan law), the clock-check habit, and
   one waiting-window exercise (Ex-α5 through Ex-ε5). Deliverables: the
   trial-3 pre-registration drafted verdict-agnostic with its falsifier
   column filled; the R4/R5 scheduled-negative prose pre-drafted; the S0
   intake checklist pre-built with empty date cells; the C81–C84
   opening-or-closure memo skeletons; the Ex-T5 execution-memo skeleton; the
   annex-snapshot rule drafted as a one-pager (Ex-Φ's pre-draft). All saved
   beside MP-51's lanes, never inside them. *Exit: the study log has one
   dated entry per day; the pre-drafts exist on disk; no row of MP-29
   through MP-51 was touched.*
2. **Session 0 (~1 h) — the gate truthing + the twelve-generations-deep arc +
   the continuum choice.** Consume MP-51's release report row by row:
   ADR-0025 at zero UNDECIDED rows, the live URL re-clicked in the sitting,
   `verify-claims` at its actual count, the twentieth teaching transcript
   on disk, `dev == main` (branch list as the transcript). Commit the intake
   table before a single continuum row opens. Then **Ex-T5: consume MP-51's
   Session-0 decision with dates** — the eleventh-generation consumption: if
   the post-record arc continued, the tenth post-record question's verdict
   is read from ADR-0025 row 3 and the eleventh post-record question chosen
   from the pre-registered continuation set (PR-31/PR-32/PR-33), each
   opening-or-closure memo in three sentences with a falsifier; if not, the
   C81–C84 adjudication: exactly one opens as row 3, the unchosen close with
   one dated reason each, stamped in the same sitting. Open ADR-0026 with its
   eight rows, windows and kill-dates; declare the terminus (release = merge + 14 calendar days);
   promote this roadmap from MP-51's release report, deviations recorded as
   dated ledger notes. **The toolchain decision is ratified here** — MP-51's
   Session 0 pinned it; this sitting verifies the pin survives contact with
   the record and re-checks `make paper` in the CI mirror. *Exit: intake
   signed; the twelve-generations-deep arc stamped; row 3 chosen (or the
   post-record continuation row opened); ledger open.*
3. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — extended to the repo's own shelf: local `main`
   re-verified reconciled to `origin/main` (branch list as the transcript),
   `portfolio/README.md`'s staleness verified closed (MP-51's Session 1 owned
   the first fix; this sitting verifies the file is current), the exp6
   residue removed with a transcript, the annexes' location verified **and
   the new snapshot rule executed (Ex-Φ)**, the twelve tracked figures
   re-derived from `make reproduce` (Ex-Ω). Row 8: MP-51's stamped closures
   re-verified (W&B, clean-clone proof, graduation proof, `reproduce-multiseed`
   exp2/exp5, the exp5 1000-epoch resolution, the README fix, the residue
   removal, the toolchain decision — **now executed, so `make paper` is
   verified green to a PDF, not graceful**) — each cell
   LAUNCHED-with-transcript or CLOSED-with-one-reason; a claimed closure
   without its transcript stays open and blocks Session 8; `gate-debt.md`'s
   absence, if still absent, recorded with a date. *Exit: rows 5 and 8
   stamped.*
4. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the twentieth research question's verdict (ADR-0025 row 3) becomes the
   paper-v22 section, the annex table, or the results-page row — every number
   manifest-tagged, consumed in the sitting that owns it; if the post-record
   arc governs, the post-record statement is framed from MP-51's release,
   never rewritten. Row 2: v22 opens only if row 1 lands new numbers; else
   "the v21 is the record" is the dated reason and `make paper` is re-verified
   against v21 — **green, with the PDF on disk**. Row 6's substitute filed
   from the visitor's chair, before the window opens (Ex-G); the fork drill
   (Ex-H) and the arc consumption (Ex-N through Ex-T5) land here. *Exit: rows
   1 and 2 dated; substitute filed; Ex-T5's execution memo on disk.*
5. **Session 3 (~2–3 h) — the essay annex v22.**
   `portfolio/essay-annex-22.md` (its home on the live shelf, dated, **with
   the repo-side snapshot written in the same sitting per Ex-Φ**): the
   twentieth question's verdict set and the teaching lane's twentieth receipt
   distilled into one dated annex; the reverse claims audit at zero (prose →
   manifest → command); each claim's "what would falsify this" column filled
   at writing time. The annex is amended, never rewritten. *Exit: row 4
   dated; audit at zero; snapshot on disk.*
6. **Session 4 (~1 h) — the stranger round 22 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. The recruitment plan
   for the uninvited cohort is executed with dates — the channels that
   produced the first twenty-one transcripts are re-used and one new channel
   is added (a public post on the showcase's own shelf), so the "uninvited"
   property is re-earned, never assumed. *Exit: window open, kill-date
   declared.*
7. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat — or, if the post-record
   arc governs, the continuation row's protocol opened under the same
   discipline. If C81: the failure cells at the sixth unseen task family and
   the fifth architecture family, and the expected per-head mechanism written
   as falsifiable predictions before a single number is read (Ex-C, Ex-I5,
   Ex-J5, Ex-S5, Ex-U5, Ex-W5) — and the patching-validity note appended
   (Part II, item 9), so the run doubles as the instrument's end-to-end
   validation or its dated negative. If C82: the fifth recipe's failure cells
   *predicted from the completed map* (Ex-X5). The scheduled negative is
   drafted *while the run is live* (Ex-D), so the S6 verdict sitting is a
   stamping, not a discovery. Row 6's kill-date honored (feedback → matrix
   drafted; silence → substitute closes it). Row 7: the twenty-first teaching
   artifact's skeleton drafted — walkthrough v21, 10-minute talk v21, or
   Colab grokking notebook v19 — with its ship-date. *Exit: row 3
   pre-registered and launched (or the post-record protocol opened); row 6
   dated either way; row 7's skeleton drafted.*
8. **Session 6 (~1–2 h) — the research verdict sitting.** Row 3's verdict
   read from the manifest: completed and dated, or window closed and the
   scheduled negative is the result — drafted while the run was live (Ex-D),
   so this sitting is a stamping, not a discovery. *Exit: row 3 dated either
   way.*
9. **Session 7 (~2–3 h) — the shelf rehearsal + the re-check row + the
   teaching polish.** Row 5: the hostile-webmaster walk at zero beside the
   browser, every public number clicked back to disk; the repo-shelf findings
   re-checked (local `main` reconciled, README current, residue gone, annexes'
   home verified, snapshots current, figures re-derived). Row 6's re-check
   row dated. Row 7: the twenty-first artifact runs end to end on a stranger's
   machine (fresh clone / Colab session); the run transcript is the receipt;
   the teaching distillation (Ex-F) lands here. *Exit: rows 5, 6, 7 dated;
   the artifact shipped with its transcript.*
10. **Session 8 (~1 h) — the release.** ADR-0026 at zero UNDECIDED rows; the
    merge green locally and on GitHub; `dev == main`; home wired — this
    roadmap's companion status retired; the roadmap archived with its
    deviations, every deviation a dated ledger note. If the post-record arc
    governs, this sitting stamps the post-record arc's eleventh dated
    direction — the record's closing sentence consumed eleven times, never
    repeated. *Exit: the merge; the program's twenty-first dated direction —
    or the post-record arc's eleventh.*

### The one measured line

ADR-0026 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row (or the post-record continuation row) whose verdict (or
scheduled negative) re-derives from a manifest; `verify-claims` at 0 with
every public number re-derivable from one command line; the hostile-webmaster
walk at zero on the live shelf and on the repo's own shelf (local `main`
reconciled, README current, residue removed, the debt ledger present or
absent-with-date, the annex snapshots current, the figures re-derived); **the
paper compiled to a PDF on this machine and in the CI mirror, or the dated
v21 rule recorded**; the twenty-first teaching artifact shipped with a
stranger-runnable transcript; `dev == main` and the program's twenty-first
dated direction — or, if the post-record arc governs, its eleventh dated
direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk. Filed as one dated
memo each in the study log.

1. **The paradigm confirmed, or its boundary (the C81 reading).** Elhage et
   al., *A Mathematical Framework for Transformer Circuits* (2021) for the
   QK/OV machinery the causal claim is made over; Wang et al.,
   *Interpretability in the Wild* (2022) for activation-patching methodology
   at per-head resolution; Conmy et al., *Towards Automated Circuit
   Discovery* (2023) for turning a hand-traced mechanism into a scalable,
   testable procedure (read, never re-implemented — ACDC stays descoped);
   Varma et al., *Explaining grokking through circuit efficiency* (2023) for
   why circuits grow sharp and where that sharpness is measurable; Olsson et
   al., *In-context Learning and Induction Heads* (2022) for what transfers
   across task families; Chughtai et al., *A Toy Model of Universality*
   (2023) for why the sixth unseen task family's and the fifth architecture
   family's failure cells fail the way they do — now read at the
   *fifth-prediction* axis: what a theory earns by predicting unseen cells
   five times, where four-round paradigms overreach on their fifth round,
   and what Popperian corroboration and Lakatosian progressivity say about a
   law whose fifth out-of-sample round lands. My C77 verdict and its measured
   theory frame the reading. **Prediction to write**: which per-head role's
   failure mechanism is the boundary's root cause at the sixth unseen task's
   structure and at the fifth architecture family's, and what the patching
   at those cells reveals; the null hypothesis every measured fingerprint is
   compared against. **Primary sources**: the frozen checkpoints, C77's
   theory table, the S3 note.
2. **The equation of state's first transfer (the C82 reading).** Lyu et al.,
   *Understanding the training dynamics of transformers on modular
   arithmetic* (2024) for the loss-landscape structure of grokking and its
   phase transitions; Morwani et al. (2024) on the edge-of-numerical-
   stability regime; Gromov, *Grokking: A Memory Perspective* (2023); Power
   et al. (2022); Nanda et al. (2023) — now read at the *transfer* axis:
   what a full-cell root-cause map *predicts* about a recipe it has never
   seen, and where "the driver" is really an optimization artifact that does
   not survive its first out-of-map recipe. **Prediction**: the fifth
   recipe's failure cells written before the analysis; C78's completed
   equation of state is this reading's admission ticket.
3. **The institution, fifteenth study (the C83 reading).** Gelman & Loken,
   *The Garden of Forking Paths*; Pineau et al. (2021); Kapoor & Narayanan,
   *Reproducibility in Machine Learning: A Systematic Literature Review*
   (2023); the ML reproducibility line (NASEM's five pillars); Lakens,
   *The Value of Preregistration for Psychological Science* — now read at the
   *constitution* axis: what a policy gains when its next measurement is
   predicted *before* it happens a fourth time and kept on its own schedule,
   and what a discipline can honestly claim that a model cannot. My
   twenty-one stranger-run transcripts are the data; the fourteenth study
   defined the tenth drift, I must decide what counts as the fifteenth
   measurement before I measure any.
4. **The standard, seventh cohort (the C84 reading).** Bricken et al. (2023);
   Cunningham et al. (2024); the dictionary-circuit and feature-universality
   line — plus the education-measurement line (rubric validity, inter-rater
   reliability, external assessment, instrument release norms) for what a
   *seventh, uninvited cohort* under a *released standard others can run*
   claims that a sixth's does not. My Rung-5 datum (99.97% FVE, L0 =
   136/256, 0% dead features) and C80's seventh-cohort outcome are the
   record's first data points.
5. **The post-record program, eleventh generation (new, deepest).** Lakatos,
   *The Methodology of Scientific Research Programmes* (1978) — read a
   twelfth time, now for the *eleventh* question past a completed program:
   progressive vs. degenerating problem shifts when the *tenth* post-record
   verdict lands, Kuhn's normal science as the post-record arc's axioms, and
   the honest criterion for the eleventh post-record question — a question
   that must earn the post-record arc's tenth *new* paragraph. This reading
   feeds Ex-T5 and the Session-0 question MP-52 owns more deeply than any
   phase before it: *what does the record's tenth post-record verdict open?*
   The answer can be the post-record arc's eleventh dated row — Lakatos'
   point is that the decision is made on the record, never as a mood.
6. **The record teaches, round twenty-one.** The twenty-first verdict in
   four registers — the paper's sentence, the annex's sentence, the 30-second
   spoken claim, and the 5-minute teaching explanation with a worked toy a
   stranger can run; the gap between the last two is where my teaching
   leaks, and I will measure it deliberately by writing all four registers
   for the same verdict (Ex-F). **Waiting-window rehearsal**: run the four
   registers on the R1 no-head negative — a stamped verdict, safe to
   practice on.
7. **The redemption reading, or negative results as maps, the twenty-first
   pass.** If a sparse cell exists by S0: Nanda et al.'s full per-frequency
   reading on the first sparse solution this harness ever produced. If not:
   how the *completed* law is reported honestly — the law's domain closed
   with its measured boundaries and its failure cells explained or mapped,
   the driver a principle or a case study with a dated exception map, the
   drift numbers ten deep, the negative as a contribution — and how the
   post-record harness (if PR-31 governs) would be designed from the dated
   negatives instead of from hope. Either way, the paper's hardest paragraph
   is the one that claims the dense solution *computes something*; I will
   draft it against this reading and let the manifest referee it.
8. **The mathematical bedrock, fifth pass (new).** The DFT-of-addition
   derivation I hand-rolled in the waiting windows extended to the *fifth
   architecture family's* geometry: what changes in the embedding's spectral
   support, the QK/OV factorization and the convolution theorem when the
   family changes a fourth time — the derivation that makes every
   fifth-family fingerprint interpretable rather than decorative. **Primary
   sources**: Nanda et al. (2023) and its appendix; my own `01_foundations`
   linear-algebra proofs; the exp2 Fourier instrument on disk. **One
   runnable check**: the hand derivation reproduced in a one-file script
   whose DFT output matches `results/exp2_grokking.json`'s k_99 = 111/113 at
   P=113, then re-run at the fifth family's geometry.
9. **The paradigm's sociology (new).** Kuhn, *The Structure of Scientific
   Revolutions* read against my own record for the first time: when does a
   "paradigm" claim require a community rather than a track record, what
   does normal science look like for a one-person program, and how should
   the paper say "paradigm" without overclaiming the collective — the
   reading that keeps C81's victory honest in its own terms, and the
   threshold at which the record's "theory" line stops being a research
   programme and becomes a paradigm others must engage.
10. **The released instrument's law (new).** Artifact-release norms for the
    C84 lane: research-artifact licensing, artifact-evaluation badges,
    data-release ethics, and the practical line between "release a rubric"
    and "release a claim" — read so the seventh cohort's rubric release is
    an artifact with a license and an adjudication procedure, never a
    gesture.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-51's release report, deviations recorded as dated ledger
  notes.
- **ADR-0026**, the twenty-first continuum ledger — eight rows pre-stamped
  with windows and kill-dates; rows 1–2 consumed from ADR-0025's verdicts;
  row 3 the twenty-first research question with its protocol note and
  heartbeat (or the post-record continuation row's protocol); rows 4–8 the
  continuum's decisions.
- **`portfolio/essay-annex-22.md`** — the v22 annex, manifest-tagged,
  amended never rewritten; the annexes' home (the live shelf) recorded with
  a date **and the repo-side snapshot written in the same sitting (Ex-Φ)**.
- **The paper v22 diff** (`portfolio/paper/main.tex` v22 + diff log) or the
  dated "the v21 is the record" memo; **`make paper` verified green to a PDF
  on this machine and in the CI mirror**, with the toolchain pin ratified at
  Session 0 (MiKTeX + TeX Live CI action per Part II, item 7).
- **The shelf health sheet + hostile-webmaster transcript** (site + Space at
  zero), extended to the repo's own shelf: local `main` reconciled to
  `origin/main`, `portfolio/README.md` current, the exp6 residue removed, the
  annexes' location verified, the snapshots current, **the twelve figures
  re-derived (`make reproduce` transcript attached, Ex-Ω)**; the claims gate
  re-run on every merge.
- **`checklists/gate-debt.md`** — each cell's transcript or one-line reason,
  dated in Session 1; the file's absence, if still absent, recorded with a
  date.
- **The research row's pre-registration note** (site, metric, negative
  control, kill-date) in `06_production_ai/notes/` + the heartbeat artifact;
  if C81: the fifth-prediction figure spec written before the analysis, the
  figure itself manifest-tagged after, and the patching-validity appendix
  (Part II, item 9). If C82: the fifth recipe's predicted failure-cell table
  (Ex-X5) committed before the analysis. If the post-record arc governs: the
  continuation row's protocol note instead.
- **The twenty-first teaching artifact + its stranger-run transcript**
  (fresh-clone or Colab session receipt).
- **Ex-T5's execution memo** — MP-51's arc decision run with dates, written
  verdict-agnostic and executed at Session 0.
- **The study log** (now a standing lane, its third phase): one dated memo
  per reading, each linking at least two notes — the vault's orphan law
  applied to the study lane itself.
- **The waiting-window pre-drafts** (alongside MP-51's Session −1): the S0
  intake checklist pre-built with empty date cells, the C81–C84
  opening-or-closure memo skeletons, the Ex-T5 execution-memo skeleton, the
  annex-snapshot one-pager (Ex-Φ's pre-draft) — saved beside MP-51's lanes,
  never inside them.
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C81–C84 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting — preceded by the arc consumption (Ex-N through Ex-T5), which may
   close the whole set with the post-record verdict.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0025's row-3 verdict traced to its manifest and its command; the rest
   struck with a reason — the hostile-webmaster test of my own prose,
   twenty-first run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C81 or C82 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the failure cells and the expected per-head mechanism at the
   sixth unseen task's structure and the fifth architecture family's (C81),
   or the fifth recipe's predicted failure cells from the completed map
   (C82) — the "what would falsify this" column filled at writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v22 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, with the repo's own shelf added: branches reconciled, README
   current, residue removed, snapshots current, figures re-derived.
6. **Ex-F · The teaching distillation, round twenty-one (S7):** the
   twenty-first question's verdict in four registers — the paper's sentence,
   the annex's sentence, the 30-second spoken claim, the 5-minute teaching
   explanation with a worked toy a stranger can run; the gap between the
   last two is where my teaching leaks.
7. **Ex-G · The stranger substitute from the visitor's chair (S2):** the
   self-review written from the chair a stranger would occupy — friction
   points → fixes → re-check row — filed before S4, so the S5 kill-date can
   never close the row with a skip.
8. **Ex-H · The fork drill, deepest form (S2, verdict-agnostic):** the
   continuing state (C81–C84) vs. the post-record state (PR-31/PR-32/PR-33)
   written as two one-page paths — what each verdict changes downstream,
   including the C81-vs-C82 choice and the post-record continuation choice —
   so next phase's S0 decision is a stamping, not a discovery.
9. **Ex-I5 · The boundary hand-roll, round ten (S5, C81 only, before any
   number is read):** the expected per-head mechanism at the sixth unseen
   task's and the fifth architecture family's failure cells written by hand
   from C77's theory table — which per-head roles must transfer unchanged,
   which may re-tune, which should fail first, and what patching at those
   cells should reveal — the null hypothesis every measured fingerprint is
   compared against. One runnable check: the hand-rolled fingerprints printed
   and saved next to Ex-J5's observed ones, so the S6 comparison is a diff,
   not a memory.
10. **Ex-J5 · The transfer reader, round ten (S5, C81 only):** the script
    that loads the frozen checkpoints at every P (including the sixth unseen
    task's and the fifth family's), runs the per-head extraction and patching
    machinery, and emits the failure-cell table as a manifest-tagged JSON —
    with the patching-validity appendix of Part II, item 9 attached, so the
    run's verdict doubles as the instrument's end-to-end validation or its
    dated negative. One runnable check: the reader runs on the frozen
    checkpoints and its output is committed before the verdict paragraph is
    drafted.
11. **Ex-K5 · The sparse-recovery toy, revisited a fifteenth time (my
    foundation challenge, fifth-family pass):** the one-file toy that
    recovers the addition table's DFT coefficients under L2 vs L1 penalties,
    now extended to the completion question: *does the sharpening ablation
    signature survive across five architecture families and five recipes,
    and where does it break?* One runnable check: the toy prints both
    reconstructions' sparsity and error plus the ablation table on a fixed
    seed, across five architectures. This is the micro-scale intuition
    C82's verdict must not contradict.
12. **Ex-L5 · The "what does the dense solution compute?" sprint, round
    fifteen (S5, C81 only):** the paper's hardest paragraph drafted at S5,
    then audited against the mechanism reading at S6 — prose that must
    survive contact with the manifest, the "computes something" claim earned
    or struck with one reason.
13. **Ex-M5 · The stranger-run drill on my own receipt (S1):** I execute
    MP-51's shipped artifact (the twentieth) on a fresh clone as if I were
    the stranger — the transcript becomes the baseline against which the
    twenty-first artifact's transcript is compared. One runnable check: the
    baseline transcript saved beside the new one.
14. **Ex-N · The arc consumption, second generation (S0):** MP-40's Ex-N
    defined the terminal state; MP-41 executed it; MP-42 through MP-51
    consumed it ten times. This drill executes that second-generation
    consumption exactly as MP-51's memo stamped it.
15. **Ex-O · The arc consumption, third generation (S0):** MP-51's
    Session-0 decision becomes the object of the consumption — the tenth
    post-record question's verdict read from ADR-0025 row 3 if the arc
    governs, the criteria cited, the release that follows. One runnable
    check: the execution memo exists, names the decision rule, cites the
    criteria from MP-51's release report.
16. **Ex-P … Ex-R, Ex-T · The arc consumption, generations 4–9 (S0):** the
    consumption chain's deepest runs as MP-51 stamped them — each memo cites
    the criteria from the release report it consumes. One runnable check per
    drill: the execution memo exists and cites the criteria from the release
    report.
17. **Ex-T5 · The arc consumption, eleventh generation (S0, new,
    verdict-agnostic):** the consumption chain's deepest run — MP-51's
    Session-0 decision consumed with dates as MP-52's intake, the
    tenth-generation post-record verdict read from ADR-0025 row 3 if the
    arc governs, the criteria cited, the release that follows (the eleventh
    post-record question, or the C81–C84 adjudication), and what each of
    ADR-0025's possible verdicts changes in that execution. One runnable
    check: the execution memo exists, names the decision rule that closes or
    continues the program's science, and cites the criteria from MP-51's
    release report — the chain now twelve generations deep, a sitting stamps,
    it never re-decides.
18. **Ex-S5 · The out-of-sample sprint, round ten (S5, C81 only):** the
    mechanism's predictions at the sixth unseen task family written as a
    dated table before any number is read — task family, expected failing
    head role, expected order of failure, expected patching signature — with
    the falsifier column filled at writing time; the observed table compared
    at S6 as a diff, not a memory.
19. **Ex-U5 · The architecture-family sprint, round ten (S5, C81 only):**
    the law's predictions at the fifth architecture family written as a dated
    table before any number is read — family, expected per-head role transfer
    or re-tuning, expected failure order, expected patching signature — with
    the falsifier column filled at writing time; the observed table compared
    at S6 as a diff, not a memory.
20. **Ex-V5 · The drift-attribution drill, round seven (S5, C83 only):**
    the rate function's parameters re-estimated from the twenty-one
    transcripts before any fix, the tenth drift's components attributed —
    harness change vs. protocol drift vs. codebase aging — each component's
    contribution re-estimated, the top root-cause's fix dated in the same
    sitting. One runnable check: the re-estimated parameter table saved
    beside the drift numbers, so the S6 verdict is a diff, not a memory.
21. **Ex-W5 · The theory's falsifier column, round five (S5, C81 only):**
    each fifth-round failure-cell explanation written with its own falsifier
    — the single observation that would refute the explanation of why this
    cell fails — filled at writing time, before the analysis; the S6 verdict
    is a diff between prediction and observation, never a memory.
22. **Ex-X5 · The equation-of-state prediction table, round five (S5, C82
    only, new):** the fifth recipe's failure cells *predicted from the
    completed map* before any number is read — cell, predicted root cause,
    predicted ablation signature, predicted failure order — with the
    falsifier column filled at writing time; the observed map compared at S6
    as a diff, not a memory. This is the moment the phase diagram stops
    being a description and becomes a law.
23. **Ex-Y5 · The policy allocation drill, round five (S5, C83 only):**
    the fifteenth measurement's schedule derived from the rate model before
    the run — the next measurement, its budget, its predicted outcome, its
    falsifier — so the S6 verdict compares the schedule against what the
    receipt system actually did, as a diff, not a memory.
24. **Ex-Z5 · The public rubric draft, round five (S5, C84 only, new):**
    the seventh cohort's rubric written as a public artifact — scoring rule,
    evidence requirements, adjudication procedure, release license — before
    recruitment, so the seventh measurement is taken under the published
    rule, never after it.
25. **Ex-Φ · The annex snapshot (S3, new, new artifact class):** the v22
    annex written on the live shelf *and* mirrored into the repo as a dated,
    read-only copy in the same sitting — the record's first protection
    against a hosting-side loss; the snapshot's own manifest tag, so
    `verify-claims` can check the pair. One runnable check: the repo
    snapshot's hash matches the shelf's dated copy at S7.
26. **Ex-Ω · The figure-regeneration audit (S1, new):** `make reproduce`
    run against the frozen configs and every tracked figure in
    `portfolio/figures/` re-derived — a figure that cannot be re-derived
    from the committed command is struck from the showcase with one dated
    reason. One runnable check: the re-derived figures' manifest tags match
    the committed ones.
27. **The waiting-window drills (Session −1):** Ex-α5 the DFT hand-roll,
    fifth pass (the derivation extended to the fifth family's geometry);
    Ex-β5 the four-registers rehearsal on the R1 no-head negative; Ex-γ5 the
    scheduled-negative drafting drill (ADR-0003 rows 4–5 prose + trial 3's
    pre-registration, falsifier columns filled); Ex-δ5 the stranger-run drill
    on the twentieth artifact once it ships (the transcript becomes the
    twenty-first's baseline); Ex-ε5 the trial-3 falsifier decision tree
    written before trial 2's verdict is read.
28. **Habit · The clock check (every session):** ADR-0026's undated rows, the
    open PR's CI status line, the shelf's health — all three before any new
    prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, twenty-first execution.** A phase that opens two
  research questions is drift by another name; the unchosen candidates close
  in the same sitting as the choice — and the arc consumption may close all
  of them with the post-record verdict. The continuum law is the mechanical
  refusal of this drift — proven executable twenty times, it must simply be
  executed again.
- **The candidate set is frozen before S0, never improvised at it.** C81–C84
  are conditions, not predictions; a sitting decides, it never invents — and
  the terminal-state object is the hardest frozen object on the record:
  written by MP-40, executed by MP-41, consumed ten more times since —
  *consumed an eleventh time* by MP-52, never re-negotiated in the consuming
  sitting.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0025's row-3 verdict in the sitting that owns it
  — or the post-record statement, if the arc governs.
- **The receipt compounds.** The twenty-first runnable artifact is only worth
  shipping because the first twenty transcripts proved the format — and if
  C83 opens, the receipts are a drift-of-drift-of-drift-of-drift-of-
  drift-of-drift-of-drift-of-drift-of-drift-of-drift number measured ten
  times in a row, tested by people I did not choose, across an aging
  codebase. My showcase's story is now "read it, run it, watch me be wrong
  on the record," twenty-one receipts deep.
- **The waiting window belongs to MP-51's Session −1 — and this draft is a
  companion written inside it.** The days between this draft and the stack's
  release are owned lanes: readings with predictions written before the
  reading, hand-derivations, pre-drafted scheduled negatives, the S0 intake
  checklist pre-built with empty date cells. A day with no dated entry is a
  row without a date. The study log itself follows the vault's orphan law:
  a memo that links nothing is a note that proves nothing was understood.
- **Budget the wall-clock at launch, never at Session 7.** The CPU is the
  binding constraint; every run gets a budget row (Part III's table), a
  heartbeat, a checkpoint-every-500, and a scheduled negative drafted while
  it is live. This is the architecture law that protects the release date.
- **A pinned toolchain is a promise; a compiled PDF is a receipt.** The
  toolchain decision lands in MP-51's Session 0; this phase's Session 1
  turns the pin into a verified artifact — `make paper` green on this machine
  and in the CI mirror. Graceful failure was the bridge; green is the
  destination. The v22 rule ("opens only for new numbers") remains the
  insurance either way.
- **The record must survive its own shelf.** The annexes live on the live
  shelf; this phase makes them durable with a dated repo snapshot (Ex-Φ) —
  the record's first defense against a hosting-side loss, cheap enough to be
  a habit and strict enough to be a row.
- **Figures must be re-derivable, not just provenance-tagged.** A manifest
  tag on a stale figure is a silent lie; the figure-regeneration audit
  (Ex-Ω) makes "the showcase regenerates" a verified sentence instead of an
  assumption.
- **Protect the release report.** The serialized stack means MP-29's release
  is still the artifact everything downstream consumes; a slip at any link
  slides the whole chain. A promise can be re-planned forever, but a dated
  row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0025 at zero, the live
  URL, `verify-claims` at 0, the twentieth teaching transcript on disk — a
  condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; the R1 no-head negative — 0/8
  heads, stamped 2026-08-14 — is the record's newest dated signature. The
  strongest form of the signature is the chain: negative → map →
  characterization → mechanism → causal verdict → circuit → law → theory →
  second prediction → third prediction → fourth prediction → *fifth
  prediction* — or a record that knew when to end.
- **The steady state is the reward, not the ceremony.** MP-52 will be the
  fifteenth roadmap written from an *executed* roadmap's release report —
  the program at its normal, confirmed fourteen times. The machinery is the
  guardrail, never the goal: rows are dated in the sitting that owns them, or
  they are not rows.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED rows
  at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story:** *the program's twenty-first dated
  direction was written from its own release report — the cap honored, the
  stack executed, the steady state kept honest fifteen times, the record
  taught twenty-one times in runnable artifacts, every public number still
  re-derives from one command line, the paper compiled to a PDF on the
  record, and the record consumed — eleven times, with dates — its own
  terminal-state decision, and answered it in a release.* Every artifact
  this phase launches is written to that standard.

## Links

- [[00_meta/51_micro-phase-51-review-and-roadmap]] — the twentieth
  question's review and roadmap; this roadmap's intake is ADR-0025's release
  report and MP-51's Session-0 decision, which Session 0 consumes again.
- [[00_meta/50_micro-phase-50-review-and-roadmap]] — the nineteenth
  question's review and roadmap, the intake chain's previous link.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat — and the
  row the terminal state executes.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/microscope-trial-table]] ·
  [[06_production_ai/notes/positive-control-protocol]] — the science C81–C84
  adjudicate over, whose pending verdicts are the intake.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/checkpoint-resume-durability]] ·
  [[06_production_ai/notes/scheduled-negatives-mp28]] — the CPU-budget canon
  the phase's runs are specified against.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.
