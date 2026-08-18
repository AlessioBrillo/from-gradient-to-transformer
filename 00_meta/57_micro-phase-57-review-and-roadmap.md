---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-18
---

# Micro-Phase 57 — State Review and Execution Roadmap (Architect's Review): the twenty-sixth question, written from the twenty-fifth release report

> **STATUS: REVIEW + EXECUTION ROADMAP, NOT A PRE-REGISTRATION.** This note is
> the architect's companion to [[00_meta/56_micro-phase-56-review-and-roadmap]],
> the twenty-fifth question's review and roadmap: it opens no rows, launches no
> runs, claims no window, and is wired into home only as a companion pointer —
> it is not counted against any cap, because the cap is spent. It is my
> step-by-step plan for the phase that starts at MP-57's Session 0, written
> from the reviewer's chair in the same first-person register as my progress
> log so it doubles as the public record of how I reasoned about the program's
> steady state while MP-56's waiting window was still open. The deepest law
> applies to my own document: this roadmap is written verdict-agnostic and
> re-plans not a single row of MP-29 through MP-56 — roadmaps are written from
> release reports, never from habit. Everything factual in this file was
> re-verified against the repository on 2026-08-18 in this drafting sitting:
> working tree clean, local `dev` at `421e471` (the MP-56 squash merge,
> PR #91), local `main` at `8b0dbf3`, `git diff main dev` empty, **190 tests
> collected in this drafting sitting (5.76 s)**, ruff clean and blocking mypy
> clean at the last release, `verify-claims` at 0, all five manifests on disk.

## Part I — Where I stand (state review, re-verified in this sitting)

### The scientific ledger

The record's deepest fact has not changed and still carries every dated
confirmation the record holds, re-verified in this drafting sitting: **no run
in this repository's history has ever produced a sparse Fourier solution.**
The count advances only with a new verdict; between MP-56's sitting and this
one, no new Fourier cell landed — the microscope's trials 2 and 3 remain
pending in ADR-0003's budget, and the dense characterization remains the
phase's headline unless one of them rescues the run.

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
  is at **0** — re-verified in this sitting.

The arc my science has taken is the strongest thing I own: *will grokking
reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what
is the dense solution's structure?* (MP-29 S3's characterization, on disk) →
*which open question is deepest?* (MP-36's sitting) → the question chain from
MP-37's sitting through MP-54's sitting → *which of C93–C96 does the consumed
twenty-fourth verdict open?* (MP-55's sitting) → *which of C97–C100 does the
consumed twenty-fifth verdict open — or is the fifteenth post-record question
the post-record arc's own successor?* (MP-56's sitting). By MP-57's Session 0
the record will hold twenty-five dated directions, a characterized dense
regime (or the sparse redemption), whichever of C97–C100 ADR-0030's sitting
chose — and the answer to the question MP-56's Session 0 owned more deeply
than any phase before it: **whether the post-record arc governs and, if it
does, what the fifteenth post-record question was.** The twenty-sixth question
is the twelfth I choose with the eleventh-generation arc consumption
*stamped* — or the sixteenth question past the record's closing sentence.

### What I verified myself in this sitting (the hostile-webmaster walk, my own transcript)

| Fact | Verified state (2026-08-18) |
|---|---|
| Test suite | **190 collected in this drafting sitting (5.76 s)** and green at the last release (64.48 s) |
| Branches | `dev` at `421e471` (the MP-56 squash merge, PR #91); `main` at `8b0dbf3`; `git diff main dev` empty |
| Working tree | Clean |
| `docs/adr/` | 0001–0010 only; ADR-0011 through ADR-0029 open at their own Session 0s; ADR-0030's eight rows are the rows MP-56 will fill; **ADR-0031 is this roadmap's ledger** |
| `figures/` | 15 untracked build products on disk, **including the Rung 6 residue** (`figures/exp6_automated_vs_manual.png` + `src/experiments/__pycache__/exp6_automated_circuit.cpython-312.pyc`) — MP-51's Session 1 owns the removal; this roadmap's Session 1 re-verifies the absence; `portfolio/figures/` holds the twelve tracked figures |
| `checklists/` | Only `reproducibility-checklist.md`; `gate-debt.md` still absent — a dated fact, never a silence |
| `portfolio/README.md` | Still stale: the three "not yet" rows contradict the record (paper through the v25 arc, site and Space live since the premiere, manifest machinery since Micro-Phase 8) — a seven-phase-standing row; this roadmap's Session 1 re-verifies the closure |
| `portfolio/projects/` | Figures only, no project write-ups (`.gitkeep` and nothing else) |
| Annexes | No `essay-annex-*.md` on disk — they live on the live shelf; the v26 snapshot pair is MP-56's; this roadmap verifies the v26 pair and writes the v27 pair |
| CI | `python-ci.yml` (ruff, blocking mypy allowlist, non-blocking full-tree mypy, pytest + coverage), `markdown-lint.yml`, `conventional-commits.yml` (with the `commitlint-new` mirror in ci-check); no Pages deploy workflow; no LaTeX toolchain locally (`make paper` graceful, not green) |
| Ledger | ADR-0003 rows 3–7 still carry UNDECIDED cells — the R1 verdict stamp, the R4/R5 scheduled negatives, the paper prose and the graduation proof must be dated before MP-29's Session 8, or the entire stack stalls; the pre-draft prose exists on disk from the prior waiting windows (Ex-Ψ5 re-verifies, never re-drafts) |
| mypy strict debt | **176 errors** in the non-blocking full-tree lane at the last count (the 2026-08-01 baseline was 154 — the +22 accumulated through new research code, verified identical under mypy 1.20.2, 2.1.0 and 2.3.0) — a real, dated, growing number, owned by no named row yet: this phase's Session 1 records the dated decision |

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no phase.
MP-37 through MP-56 are the un-cap's roadmap drafts executed exactly once
each. **MP-56's review and roadmap are merged (PR #91), its Session −1 study
lane owns the waiting window, and its Session 0 awaits the stack's release.**
**ADR-0030's eight rows are the rows MP-56 will fill**; **ADR-0031's eight
rows are the rows this roadmap will fill** — exactly once, under the continuum
law, twenty-sixth execution, written from MP-56's release report rather than
from the habit of pre-registering.

### The CI floor and the toolchains

190 tracked tests, ruff, blocking mypy and markdownlint are green at the last
release, `verify-claims` at 0. The verified gaps, stated as facts not hopes:
no LaTeX toolchain on this machine (`make paper` is graceful, not green — the
green-to-PDF verification is a standing Session 1 row), no Pages deploy
workflow in `.github/workflows/`, no `publish:` frontmatter policy,
`portfolio/projects/` holds figures but no project write-ups, W&B never
connected. The `typecheck-new` ratchet remains the house rule for all new
research code; the `commitlint-new` mirror (origin/dev..HEAD) is in ci-check
since the MP-52 footer-line incident and must be green before any push. The
MP-54 incident's process lesson is now a law: **a squash body must be
pre-wrapped to <200-char lines before the merge call** — the squash message
is never linted before it lands on main; this roadmap's own merge observes it.

### The showcase corpus at intake

12+ provenance-guarded figures (the count grows with whatever MP-56's science
adds), the paper through the v25 arc (the v26 rule is MP-56's, **the v27 rule
is this phase's**), the site and Space live since the premiere, the essay
annexes through the v25 arc (the v26 annex is MP-56's to write and this
phase's to verify; the v27 annex is this phase's), twenty-five runnable
teaching artifacts with stranger-run transcripts (the receipts land only if
the stack ships: the twenty-fifth ships in MP-56, **the twenty-sixth in this
phase**). My teaching lane ships the twenty-sixth artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The intake is a consumption sixteen generations deep.** MP-57's Session
   0 must **consume MP-56's Session-0 decision with dates** — the single most
   dangerous drift is re-litigating a decision already consumed fifteen
   times: re-opening candidates the twenty-fifth question already closed with
   dated reasons, or treating "the post-record arc governs" as a mood instead
   of as a stamped verdict. The decision chain is now sixteen generations
   deep; a sitting stamps, it never re-decides.
2. **The stacked execution is still the critical path — and its head is still
   MP-29.** MP-57's Session 0 consumes MP-56's release report, which awaits
   the stack. A slip at any link slides the whole chain; **my highest-
   leverage act is unchanged: protect MP-29's window** — its release report is
   the artifact everything downstream consumes. Nothing in this phase may
   borrow a minute from it, and this draft is written verdict-agnostic by law:
   it re-plans not a single row of MP-29 through MP-56.
3. **ADR-0003 still carries UNDECIDED rows, and the ledger is the schedule.**
   The R1 run *completed* 2026-08-14, but rows 3–5 have not been stamped with
   their verdicts (the no-head negative for row 3; the scheduled negatives
   for rows 4–5), and rows 6–7 (paper prose, graduation proof) remain
   undated. MP-29's Session 8 requires zero UNDECIDED rows; a slip here
   stalls the entire stack. I do not re-plan those rows — and the pre-draft
   prose of the scheduled negatives exists on disk from the prior waiting
   windows (Ex-Ψ5 re-verifies it with a date, never re-drafts it), so the
   stamping sitting is a stamping, never a discovery.
4. **The microscope budget is one failure away from exhaustion — and its
   verdicts will likely land long before this phase's Session 0.** Trial 2's
   verdict forces trial 3's choice (the ledger's "my own third"); three
   failures close row 2 and make the dense characterization the phase's
   headline. Verdict-agnostic readiness means: **trial 3's pre-registration
   and the dense-characterization protocol, both drafted in prior waiting
   windows, are re-verified with their falsifier columns filled (Ex-Ψ5)** —
   so no sitting ever chooses an improvised third trial, and no phase ever
   re-drafts what a lane already owns.
5. **The CPU wall is the science's binding constraint — and the budget now
   runs on observed rates, never estimates.** Every pending run (trial 2,
   trial 3, the characterization's per-head dictionaries and ablations)
   shares one CPU and overnight windows. The observed rates MP-29's runs
   produce (~2.5 s/epoch × 5000 epochs ≈ 3.5 h wall per trial, the
   characterization at ~1–2 h, the SAE re-run at ~1 h) become the budget's
   ground truth; anything this phase launches gets a budget row at launch,
   never at Session 7 — heartbeat, checkpoint-every-500, scheduled negative
   drafted while the run is live.
6. **The steady state must not become ceremony — and at generation
   twenty-six the roadmap machinery itself is the risk.** MP-57 will be the
   twentieth roadmap written from an *executed* roadmap's release report —
   the program's normal, confirmed nineteen times. The pre-draft stack has
   been re-drafted in every waiting window since MP-48; the countermeasure is
   concrete: **Ex-Ψ5, the pre-draft stack audit, fifth pass** — every
   artifact a prior lane already owns is verified on disk with its date and
   updated in place, never re-drafted from scratch — and every session's exit
   names at least one artifact changed on disk, and every row is dated in the
   sitting that owns it. A stamped row with no science behind it is ceremony
   by another name.
7. **The paper's compile gate is executable — which makes its drift subtler.**
   By this phase's Session 0, the toolchain is pinned (MiKTeX + TeX Live CI
   action per MP-51's pin) and the green-to-PDF verification a standing
   Session 1 row. The new risk is not a missing toolchain but a *ceremonial*
   one: the gate "passes" because `make paper` is graceful-by-design, and the
   v27 rule ("opens only for new numbers, else the v26 is the record")
   becomes a way to never compile. The countermeasure: Session 1 verifies
   `make paper` green on this machine **and** in the CI mirror with a dated
   transcript — a compile that produces a PDF, not a message.
8. **Stop-and-publish is a row, not a threat — and the post-record criterion
   is now sixteen questions deep.** ADR-0004's row 5 stays open as the
   program's honest exit: a phase is worth doing only if its candidate set
   can earn a paragraph the record does not already have. If MP-56's Session
   0 continued the post-record arc, the deepest candidate this phase can
   choose earns the post-record arc's *fifteenth new paragraph* — the
   record's closing sentence consumed sixteen times, never repeated. The
   deepest form of laziness is building what the record has already said.
9. **Path patching may still be validated only by unit tests.** The R1
   no-head negative means the R4/R5 chain closes with scheduled negatives;
   head ablation and path patching remain unvalidated end-to-end until a
   confirmed head exists anywhere on the record. If C97 opened in MP-56, its
   patching verdicts were the first chance to close this gap — the intake
   tells me which. If the gap persists, C101's/C102's patching verdicts are
   the next chance; the protocol note must state explicitly which patching
   machinery is being validated for the first time, so the verdict doubles
   as an instrument validation or a dated instrument negative. This is now
   the record's longest-standing instrument gap, and Part IV's new reading —
   the instrument-that-never-fired canon — is its study lane.
10. **The annexes live only on the live shelf — the snapshot rule is now a
    standing row.** Session 1 re-verifies the v26 pair (shelf copy hash vs.
    repo snapshot, `verify-claims` checking the pair), Session 3 writes the
    v27 pair — the rule is a row, never a gesture.
11. **Figure provenance is silently re-derivable, never re-derived — the
    audit is now a standing row.** This phase re-runs `make reproduce`
    against the grown corpus (Ex-Ω): a figure that no longer regenerates
    from the committed config is a silent lie wearing a manifest tag, struck
    with one dated reason. The Rung 6 residue figure
    (`exp6_automated_vs_manual.png`) is the audit's first fixed point:
    MP-51's Session 1 owns its removal, this phase's Session 1 re-verifies
    its absence.
12. **The mypy strict debt is real, growing, and unowned — and the
    showcase's narrative shelf still lags its science.** The non-blocking
    full-tree count climbed from 154 to **176** since 2026-08-01 (+22,
    verified not a tool upgrade) and no named row owns the paidown. Nothing
    this phase ships may hide behind that lane's non-blocking status: the
    `typecheck-new` ratchet stands for all new research code, and Session 1
    records a dated decision on the count (paid down, or ratcheted with its
    own row). Separately, `portfolio/README.md`'s staleness is now a
    seven-phase-standing row and `portfolio/projects/` holds no write-ups:
    the science outruns the narrative. Session 1 is the dated closure for
    both — and the write-up row has now earned its consideration as a
    standing contract of its own, not a rescue.
13. **The waiting window is now seven phases wide (new this sitting).**
    MP-51's, MP-52's, MP-53's, MP-54's, MP-55's, MP-56's and MP-57's
    Session −1 lanes share the same weeks before the stack's release. The
    collision risk is real: seven lanes drafting the same trial-3
    pre-registration, seven intake checklists, seven memo skeletons. The
    countermeasure is separation: each phase's pre-drafts live in named
    files of their own beside the lanes, never inside them, and MP-57's lane
    *verifies* the stack in place (Ex-Ψ5) instead of adding a seventh draft.
14. **New this sitting: the instrument-that-never-fired risk has become a
    standing gap, not a footnote.** Every phase since MP-23 has re-stated
    that path patching is validated only by unit tests, and every phase has
    shipped without closing it — the R1 no-head negative made the scheduled
    negative the legitimate result, but the instrument's end-to-end
    validation remains the record's oldest open instrumentation debt. This
    phase names it: if no patching verdict anywhere on the record has yet
    touched a real head, the C101/C102 protocol note *must* carry the
    patching-validity appendix (item 9), and the Part IV reading on
    instrument certification becomes a dated row of the study log.
15. **New this sitting: the showcase's write-up shelf is now the narrative's
    binding constraint.** Twelve figures, five manifests, a paper through
    the v25 arc, twenty-five teaching receipts — and `portfolio/projects/`
    holds no project write-ups. The corpus is complete; the narrative is
    not. This phase's Session 1 closes the README staleness (item 12) and
    Session 7 considers whether the write-up row becomes a standing contract
    of its own — the science outruns the narrative until the narrative is a
    row.

## Part III — The roadmap, step by step (the continuum law, twenty-sixth execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C101 | **The paradigm confirmed a tenth time, or its boundary mapped** (C97's successor) — the failure-cell theory *predicted a tenth time*: the per-head mechanism at the eleventh unseen task family's and the tenth architecture family's failure cells written as falsifiable predictions before any number is read, causally verified by patching, the theory's domain statement extended from "predicts unseen cells nine times" to "predicts unseen cells ten times" — a paradigm that survives a tenth prediction is a theory with a confirmed domain; a paradigm that breaks on its tenth round is a boundary with a map, and the map is the result | ADR-0030 row 3 = C97 with a positive verdict (the ninth prediction on disk) | C97 closed negative, or the post-record arc governs → the theory's tenth round belongs to the post-record arc |
| C102 | **The equation of state's sixth transfer** (C98's successor) — the full P×wd×recipe×architecture space *used a sixth time*: the root-cause map closed at nine recipes now asked a sixth time what it can do — the tenth recipe's failure cells *predicted from the map before the recipe runs*, each prediction ablated or mapped, the equation of state earning its name by transfer, not by accumulation — a boundary that predicts five unseen recipes is an equation of state with a five-transfer record; a boundary that re-measures is a phase diagram, and the diagram is the result | ADR-0030 row 3 = C98 with the ninth-recipe closure on disk | C98 never opened, or its verdict was negative → no equation of state to transfer |
| C103 | **The institution, twentieth study** (C99's successor) — the fifteenth drift measurement after the fourteenth dated fix, the rate function's parameters re-estimated from the receipt system's history, the next measurement's schedule *predicted before it happens* a ninth time and the policy *enforced* across the stack's own execution window a ninth time — an institution that survived nine enforcement windows is a constitution that keeps its own schedule; a discipline that predicted eight times and kept its date is an institution, and the institution is the result | ADR-0030 row 3 = C99 with the fourteenth measurement and attribution on disk AND ≥ 26 stranger-run transcripts at S0 | Fewer than 26 transcripts, or C99 never opened → the receipt system hasn't earned a twentieth study |
| C104 | **The standard, twelfth cohort** (C100's successor) — the eleventh-edition course *validated a twelfth time by the uninvited* under the rubric *already released as a standalone artifact others can run*: the scoring rule's tenth prediction round checked against the twelfth cohort's friction, the feedback-to-fixes matrix's tenth prediction round executed — an instrument validated eleven times by the uninvited is the standard others cite; an instrument validated ten times is a standard with a track record | ADR-0030 row 3 = C100 with the eleventh cohort's measured outcome on disk | C100 never opened, or a sparse regime exists → the sparse reading owns the question |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥
3 checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The terminal-state override stands, now sixteen generations deep: **if MP-56's
Session 0 consumed MP-55's decision with dates and the post-record arc
governs, then MP-57's Session 0 consumes the fifteenth post-record question's
verdict from ADR-0030 row 3 and continues the post-record arc, choosing the
sixteenth post-record question from the pre-registered continuation set
below.** The rule is executed with dates at Session 0; it is never improvised
and never re-negotiated in the sitting that consumes it.

### The post-record continuation set (chosen only if MP-56 continued the post-record arc)

| # | Candidate | Why it would open | Why it would close |
|---|---|---|---|
| PR-46 | **The new harness's eleventh cross-recipe law** (PR-43's successor) — the *thirteenth* recipe at the new address replicated across seeds and compared to the first twelve under the record's laws: thirteen recipes compared across seeds is the harness's eleventh law datum; twelve recipes compared once is a tenth datum, and the datum is the result | The post-record arc continued at MP-56 with PR-43's verdict on disk | The record never closed, or the redemption fired first → the sparse question belongs to the old arc |
| PR-47 | **The law at the record's edge, sixteenth task** (PR-44's successor) — the frozen-checkpoint predictions tested at the sixteenth unseen task family: a law that predicts sixteen times is a law with a predictive record; a law that breaks is a boundary with a map | The post-record arc continued at MP-56 with PR-44's verdict on disk | The record never closed → the law's successors are C101's, not the post-record arc's |
| PR-48 | **The record as a course, fifteenth edition** (PR-45's successor) — the fourteenth edition revised from its thirteenth intake: the feedback-to-fixes matrix executed with dates, the twenty-six runnable artifacts assembled, the fifteenth edition measured as a learning instrument with fourteen cohorts — a course revised from its receipts fourteen times is a curriculum; a course re-shown is a poster | The post-record arc continued at MP-56 with PR-45's verdict on disk | The record never closed → the teaching lane continues as the continuum's row 8 |

The likely survivor, written as a condition chain, never a prediction: if
MP-56's Session 0 continued the post-record arc → **the post-record
continuation** — the sixteenth question past the record, chosen in the
consuming sitting from PR-46/PR-47/PR-48; else if C97 landed positive →
**C101** — the paradigm's tenth prediction, always CPU-runnable on
checkpoints that exist today; else if C98's ninth-recipe closure landed →
**C102**; else **C103** (always-runnable, the showcase's own science, receipts
now twenty-six deep); C104 is the evidence lane and the teaching lane's
anchor.

### The pending-run wall-clock budget (verified against observed rates)

The runs the stack still owns, budgeted from observed wall-clock rates so no
launch is ever a discovery — and re-read by this phase as the ground truth
for whatever it launches:

| Run | Observed rate | Budget | Window discipline |
|---|---|---|---|
| Microscope trial 2 (`--schedule constant`, P=113, seed 0) | ~2.5 s/epoch (micro1) | ~3.5 h for 5000 epochs | Launch at window open; heartbeat; checkpoint-every-500 |
| Microscope trial 3 (wd 1.5×, P=113, seed 0) | same | ~3.5 h | Pre-registered in prior waiting windows (Ex-Ψ5 re-verifies); verdict forces the choice, never the schedule |
| Dense characterization (per-head dictionaries, ablations on frozen checkpoints) | reads only | ~1–2 h | Session 3, reads from disk, no training |
| SAE re-run on a confirmed-head checkpoint (ADR-0003 row 5) | exp5 rates | ~1 h | Only if a head exists; else the scheduled negative is the result |

### The sessions

1. **Session −1 (~1 h/day, now → the stack's release) — the waiting-window
   study lane.** The days before MP-56's Session 0 are owned, not idle — and
   the window is now seven phases wide: MP-51's, MP-52's, MP-53's, MP-54's,
   MP-55's, MP-56's and MP-57's lanes share the same weeks. Each day: one
   study block from Part IV (reading → prediction written *before* the
   reading → one-page memo filed in the study log — each memo linking at
   least two notes, per the vault's orphan law), the clock-check habit, and
   one waiting-window exercise (Ex-α10 through Ex-ε10). Deliverables:
   **Ex-Ψ5, the pre-draft stack audit, fifth pass** — trial 3's
   pre-registration, the R4/R5 scheduled-negative prose, the
   dense-characterization protocol, the S0 intake checklist, the C101–C104
   opening-or-closure memo skeletons, the Ex-T10 execution-memo skeleton and
   the annex-snapshot one-pager each verified on disk with its date from the
   prior lanes, updated in place, anything missing drafted once with a dated
   reason. All saved beside MP-51's through MP-56's lanes, never inside
   them. *Exit: the study log has one dated entry per day; the audit table
   dated; no row of MP-29 through MP-56 was touched.*
2. **Session 0 (~1 h) — the gate truthing + the sixteen-generations-deep
   arc + the continuum choice.** Consume MP-56's release report row by row:
   ADR-0030 at zero UNDECIDED rows, the live URL re-clicked in the sitting,
   `verify-claims` at its actual count, the twenty-fifth teaching transcript
   on disk, `dev == main` (branch list as the transcript). Commit the intake
   table before a single continuum row opens. Then **Ex-T10: consume MP-56's
   Session-0 decision with dates** — the sixteenth-generation consumption:
   if the post-record arc continued, the fifteenth post-record question's
   verdict is read from ADR-0030 row 3 and the sixteenth post-record
   question chosen from the pre-registered continuation set (PR-46/PR-47/
   PR-48), each opening-or-closure memo in three sentences with a falsifier;
   if not, the C101–C104 adjudication: exactly one opens as row 3, the
   unchosen close with one dated reason each, stamped in the same sitting.
   Open ADR-0031 with its eight rows, windows and kill-dates; declare the
   terminus (release = merge plus 14 calendar days); promote this roadmap
   from MP-56's release report, deviations recorded as dated ledger notes.
   **The toolchain decision is ratified here** — pinned by MP-51's Session 0,
   verified to a PDF in every Session 1 since; this sitting re-checks the pin
   survives contact with the record and re-checks `make paper` in the CI
   mirror. *Exit: intake signed; the sixteen-generations-deep arc stamped;
   row 3 chosen (or the post-record continuation row opened); ledger open.*
3. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — extended to the repo's own shelf: local `main`
   re-verified reconciled to `origin/main` (branch list as the transcript),
   `portfolio/README.md`'s staleness verified closed (the seven-phase-
   standing row), the exp6 residue verified absent with a transcript, the
   annexes' location verified **and the v26 snapshot pair re-verified
   (Ex-Φ)**, the tracked figures re-derived from `make reproduce` (Ex-Ω,
   against the grown corpus). Row 8: MP-56's stamped closures re-verified
   (W&B, clean-clone proof, graduation proof, `reproduce-multiseed`
   exp2/exp5, the exp5 1000-epoch resolution, the README fix, the residue
   removal, the toolchain decision — **now executed, so `make paper` is
   verified green to a PDF, not graceful**) — each cell
   LAUNCHED-with-transcript or CLOSED-with-one-reason; a claimed closure
   without its transcript stays open and blocks Session 8;
   `gate-debt.md`'s absence, if still absent, recorded with a date; **the
   mypy-count dated decision recorded** (paid down, or ratcheted with its
   own row — the `typecheck-new` ratchet stands for all new research code).
   *Exit: rows 5 and 8 stamped.*
4. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the twenty-fifth research question's verdict (ADR-0030 row 3) becomes the
   paper-v27 section, the annex table, or the results-page row — every
   number manifest-tagged, consumed in the sitting that owns it; if the
   post-record arc governs, the post-record statement is framed from MP-56's
   release, never rewritten. Row 2: v27 opens only if row 1 lands new
   numbers; else "the v26 is the record" is the dated reason and `make
   paper` is re-verified against v26 — **green, with the PDF on disk**.
   Row 6's substitute filed from the visitor's chair, before the window
   opens (Ex-G); the fork drill (Ex-H) and the arc consumption (Ex-N through
   Ex-T10) land here. *Exit: rows 1 and 2 dated; substitute filed; Ex-T10's
   execution memo on disk.*
5. **Session 3 (~2–3 h) — the essay annex v27.**
   `portfolio/essay-annex-27.md` (its home on the live shelf, dated, **with
   the repo-side snapshot written in the same sitting per Ex-Φ**): the
   twenty-fifth question's verdict set and the teaching lane's twenty-fifth
   receipt distilled into one dated annex; the reverse claims audit at zero
   (prose → manifest → command); each claim's "what would falsify this"
   column filled at writing time. The annex is amended, never rewritten.
   *Exit: row 4 dated; audit at zero; snapshot pair on disk.*
6. **Session 4 (~1 h) — the stranger round 27 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. The recruitment plan
   for the uninvited cohort is executed with dates — the channels that
   produced the first twenty-six transcripts are re-used and one new
   channel is added (a public post on the showcase's own shelf), so the
   "uninvited" property is re-earned, never assumed. *Exit: window open,
   kill-date declared.*
7. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat — or, if the post-record
   arc governs, the continuation row's protocol opened under the same
   discipline. If C101: the failure cells at the eleventh unseen task family
   and the tenth architecture family, and the expected per-head mechanism
   written as falsifiable predictions before a single number is read (Ex-C,
   Ex-I10, Ex-J10, Ex-S10, Ex-U10, Ex-W10) — and the patching-validity note
   appended (Part II, item 9), so the run doubles as the instrument's
   end-to-end validation or its dated negative. If C102: the tenth recipe's
   failure cells *predicted from the completed map* (Ex-X10). The scheduled
   negative is drafted *while the run is live* (Ex-D), so the S6 verdict
   sitting is a stamping, not a discovery. Row 6's kill-date honored
   (feedback → matrix drafted; silence → substitute closes it). Row 7: the
   twenty-sixth teaching artifact's skeleton drafted — walkthrough v26,
   10-minute talk v26, or Colab grokking notebook v24 — with its ship-date.
   *Exit: row 3 pre-registered and launched (or the post-record protocol
   opened); row 6 dated either way; row 7's skeleton drafted.*
8. **Session 6 (~1–2 h) — the research verdict sitting.** Row 3's verdict
   read from the manifest: completed and dated, or window closed and the
   scheduled negative is the result — drafted while the run was live (Ex-D),
   so this sitting is a stamping, not a discovery. *Exit: row 3 dated either
   way.*
9. **Session 7 (~2–3 h) — the shelf rehearsal + the re-check row + the
   teaching polish.** Row 5: the hostile-webmaster walk at zero beside the
   browser, every public number clicked back to disk; the repo-shelf findings
   re-checked (local `main` reconciled, README current, residue gone, annexes'
   home verified, v26 + v27 snapshot pairs current, figures re-derived).
   Row 6's re-check row dated. Row 7: the twenty-sixth artifact runs end to
   end on a stranger's machine (fresh clone / Colab session); the run
   transcript is the receipt; the teaching distillation (Ex-F) lands here;
   the write-up shelf's standing-contract decision is recorded (Part II,
   item 15). *Exit: rows 5, 6, 7 dated; the artifact shipped with its
   transcript.*
10. **Session 8 (~1 h) — the release.** ADR-0031 at zero UNDECIDED rows; the
    merge green locally and on GitHub; `dev == main`; home wired — this
    roadmap's companion status retired; the roadmap archived with its
    deviations, every deviation a dated ledger note. If the post-record arc
    governs, this sitting stamps the post-record arc's sixteenth dated
    direction — the record's closing sentence consumed sixteen times, never
    repeated. *Exit: the merge; the program's twenty-sixth dated direction —
    or the post-record arc's sixteenth.*

### The one measured line

ADR-0031 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row (or the post-record continuation row) whose verdict (or
scheduled negative) re-derives from a manifest; `verify-claims` at 0 with
every public number re-derivable from one command line; the hostile-webmaster
walk at zero on the live shelf and on the repo's own shelf (local `main`
reconciled, README current — the seven-phase-standing row closed, residue
removed, the debt ledger present or absent-with-date, the annex snapshot
pairs current, the figures re-derived); **the paper compiled to a PDF on this
machine and in the CI mirror, or the dated v27 rule recorded**; the
twenty-sixth teaching artifact shipped with a stranger-runnable transcript;
`dev == main` and the program's twenty-sixth dated direction — or, if the
post-record arc governs, its sixteenth dated direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk. Filed as one dated
memo each in the study log (Session −1), now its eighth phase as a standing
lane.

1. **The paradigm confirmed a tenth time, or its boundary (the C101
   reading).** Elhage et al., *A Mathematical Framework for Transformer
   Circuits* (2021) for the QK/OV machinery the causal claim is made over;
   Wang et al., *Interpretability in the Wild* (2022) for activation-patching
   methodology at per-head resolution; Conmy et al., *Towards Automated
   Circuit Discovery* (2023) for turning a hand-traced mechanism into a
   scalable, testable procedure (read, never re-implemented — ACDC stays
   descoped); Varma et al., *Explaining grokking through circuit efficiency*
   (2023) for why circuits grow sharp and where that sharpness is measurable;
   Olsson et al., *In-context Learning and Induction Heads* (2022) for what
   transfers across task families; Chughtai et al., *A Toy Model of
   Universality* (2023) for why the eleventh unseen task family's and the
   tenth architecture family's failure cells fail the way they do — now read
   at the *tenth-prediction* axis, and with Kuhn's *Structure of Scientific
   Revolutions* read a sixth time against my own record: what a theory earns
   by predicting unseen cells ten times, where nine-round paradigms overreach
   on their tenth round, what Popperian corroboration and Lakatosian
   progressivity say about a law whose tenth out-of-sample round lands, and
   how the paper should say "paradigm" without overclaiming the collective.
   Nosek et al., *The Preregistration Revolution* (2022) — for
   pre-registration as the tenth trial's own instrument. My C97 verdict and
   its measured theory frame the reading. **Prediction to write**: which
   per-head role's failure mechanism is the boundary's root cause at the
   eleventh unseen task's structure and at the tenth architecture family's,
   and what the patching at those cells reveals; the null hypothesis every
   measured fingerprint is compared against. **Primary sources**: the frozen
   checkpoints, C97's theory table, the S3 note.
2. **The equation of state's sixth transfer (the C102 reading).** Lyu et al.,
   *Understanding the training dynamics of transformers on modular
   arithmetic* (2024) for the loss-landscape structure of grokking and its
   phase transitions; Morwani et al. (2024) on the edge-of-numerical-
   stability regime; Gromov, *Grokking: A Memory Perspective* (2023); Power
   et al. (2022); Nanda et al. (2023) — now read at the *transfer* axis, a
   sixth pass: what a full-cell root-cause map that has already transferred
   five times *predicts* about a recipe it has never seen a sixth time, and
   where "the driver" is really an optimization artifact that does not
   survive its sixth out-of-map recipe. **Prediction**: the tenth recipe's
   failure cells written before the analysis; C98's completed equation of
   state is this reading's admission ticket.
3. **The institution, twentieth study (the C103 reading).** Gelman & Loken,
   *The Garden of Forking Paths*; Pineau et al. (2021); Kapoor & Narayanan,
   *Reproducibility in Machine Learning: A Systematic Literature Review*
   (2023); the ML reproducibility line (NASEM's five pillars); Lakens,
   *The Value of Preregistration for Psychological Science* — now read at the
   *constitution* axis: what a policy gains when its next measurement is
   predicted *before* it happens a ninth time and kept on its own schedule,
   and what a discipline can honestly claim that a model cannot. My
   twenty-six stranger-run transcripts are the data; the nineteenth study
   defined the fifteenth drift, I must decide what counts as the twentieth
   measurement before I measure any.
4. **The standard, twelfth cohort (the C104 reading).** Bricken et al.
   (2023); Cunningham et al. (2024); the dictionary-circuit and
   feature-universality line — plus the education-measurement line (rubric
   validity, inter-rater reliability, external assessment, instrument release
   norms) for what an *twelfth, uninvited cohort* under a *released
   standard others can run* claims that an eleventh's does not. My Rung-5
   datum (99.97% FVE, L0 = 136/256, 0% dead features) and C100's
   twelfth-cohort outcome are the record's first data points.
5. **The post-record program, sixteenth generation (new, deepest).**
   Lakatos, *The Methodology of Scientific Research Programmes* (1978) — read
   a seventeenth time, now for the *sixteenth* question past a completed
   program: progressive vs. degenerating problem shifts when the *fifteenth*
   post-record verdict lands, Kuhn's normal science as the post-record arc's
   axioms, and the honest criterion for the sixteenth post-record question —
   a question that must earn the post-record arc's fifteenth *new*
   paragraph. This reading feeds Ex-T10 and the Session-0 question MP-57 owns
   more deeply than any phase before it: *what does the record's fifteenth
   post-record verdict open?* The answer can be the post-record arc's
   sixteenth dated row — Lakatos' point is that the decision is made on the
   record, never as a mood.
6. **The record teaches, round twenty-six.** The twenty-sixth verdict in
   four registers — the paper's sentence, the annex's sentence, the 30-second
   spoken claim, and the 5-minute teaching explanation with a worked toy a
   stranger can run; the gap between the last two is where my teaching
   leaks, and I will measure it deliberately by writing all four registers
   for the same verdict (Ex-F). **Waiting-window rehearsal**: run the four
   registers on the R1 no-head negative — a stamped verdict, safe to
   practice on.
7. **The redemption reading, or negative results as maps, the twenty-sixth
   pass.** If a sparse cell exists by S0: Nanda et al.'s full per-frequency
   reading on the first sparse solution this harness ever produced. If not:
   how the *completed* law is reported honestly — the law's domain closed
   with its measured boundaries and its failure cells explained or mapped,
   the driver a principle or a case study with a dated exception map, the
   drift numbers fifteen deep, the negative as a contribution — and how the
   post-record harness (if PR-46 governs) would be designed from the dated
   negatives instead of from hope. Either way, the paper's hardest paragraph
   is the one that claims the dense solution *computes something*; I will
   draft it against this reading and let the manifest referee it.
8. **The mathematical bedrock, tenth pass (new).** The DFT-of-addition
   derivation I hand-rolled in the waiting windows extended to the *tenth
   architecture family's* geometry: what changes in the embedding's spectral
   support, the QK/OV factorization and the convolution theorem when the
   family changes a ninth time — the derivation that makes every
   tenth-family fingerprint interpretable rather than decorative.
   **Primary sources**: Nanda et al. (2023) and its appendix; my own
   `01_foundations` linear-algebra proofs; the exp2 Fourier instrument on
   disk. **One runnable check**: the hand derivation reproduced in a one-file
   script whose DFT output matches `results/exp2_grokking.json`'s k_99 =
   111/113 at P=113, then re-run at the tenth family's geometry.
9. **The instrument that never fired (new) — the record's oldest
   instrumentation gap.** Zhang & Nanda, *Towards Best Practices of
   Activation Patching* (2024) read against my own exp4 machinery; the
   activation-patching validation line (self-patch-is-zero, corrupt-run-diff)
   as the certification standard; and the epistemology of the scheduled
   negative: what it means to certify an instrument by its unit tests plus a
   dated negative for the entire duration of a record, and what the
   threshold is at which the record must say "this machinery has never
   touched a real head — here is what that does to the causal claims that
   rest on it." The R4/R5 chain's scheduled negatives are the record's
   first data points; the C101/C102 patching verdicts, if they open, are the
   instrument's first end-to-end validation or its dated negative — the
   reading that turns a standing gap into a dated row of the study log.
10. **The long-window discipline, fifth pass (new).** Pacing a
    seven-phases-wide waiting window: how the study lane stays a lane rather
    than becoming a ceremony factory — the spacing-effect line (Ebbinghaus
    and the modern replication of the spacing effect) for why one dated memo
    per day outlearns a crammed weekend, the daily-habit mechanics my own
    study log has proven across seven phases, and Ex-Ψ5 as the lane's own
    gate. The waiting window is the program's longest since the premiere,
    now a phase wider than MP-56's; a window with no dated entry is a row
    without a date.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-56's release report, deviations recorded as dated ledger
  notes.
- **ADR-0031**, the twenty-sixth continuum ledger — eight rows pre-stamped
  with windows and kill-dates; rows 1–2 consumed from ADR-0030's verdicts;
  row 3 the twenty-sixth research question with its protocol note and
  heartbeat (or the post-record continuation row's protocol); rows 4–8 the
  continuum's decisions.
- **`portfolio/essay-annex-27.md`** — the v27 annex, manifest-tagged,
  amended never rewritten; the annexes' home (the live shelf) recorded with
  a date **and the repo-side snapshot written in the same sitting (Ex-Φ)**;
  the v26 snapshot pair re-verified at Session 1.
- **The paper v27 diff** (`portfolio/paper/main.tex` v27 + diff log) or the
  dated "the v26 is the record" memo; **`make paper` verified green to a PDF
  on this machine and in the CI mirror**, with the toolchain pin ratified at
  Session 0 (MiKTeX + TeX Live CI action per MP-51's pin, verified in every
  Session 1 since and re-verified here).
- **The shelf health sheet + hostile-webmaster transcript** (site + Space at
  zero), extended to the repo's own shelf: local `main` reconciled to
  `origin/main`, `portfolio/README.md` current (the seven-phase-standing row
  closed), the exp6 residue removed, the annexes' location verified, the v26
  snapshot pair current, **the figures re-derived (`make reproduce`
  transcript attached, Ex-Ω)**; the claims gate re-run on every merge.
- **`checklists/gate-debt.md`** — each cell's transcript or one-line reason,
  dated in Session 1; the file's absence, if still absent, recorded with a
  date. **The mypy-count row** — the dated paidown-or-ratchet decision,
  recorded in the same sitting.
- **The research row's pre-registration note** (site, metric, negative
  control, kill-date) in `06_production_ai/notes/` + the heartbeat artifact;
  if C101: the tenth-prediction figure spec written before the analysis, the
  figure itself manifest-tagged after, and the patching-validity appendix
  (Part II, item 9). If C102: the tenth recipe's predicted failure-cell table
  (Ex-X10) committed before the analysis. If the post-record arc governs:
  the continuation row's protocol note instead.
- **The twenty-sixth teaching artifact + its stranger-run transcript**
  (fresh-clone or Colab session receipt).
- **Ex-T10's execution memo** — MP-56's arc decision run with dates, written
  verdict-agnostic and executed at Session 0.
- **The study log** (now a standing lane, its eighth phase): one dated memo
  per reading, each linking at least two notes — the vault's orphan law
  applied to the study lane itself. The instrument-that-never-fired memo
  (Part IV, reading 9) is a dated row of this lane, never a footnote.
- **The waiting-window pre-drafts** (alongside MP-51's through MP-56's
  Session −1 lanes): the S0 intake checklist pre-built with empty date
  cells, the C101–C104 opening-or-closure memo skeletons, the Ex-T10
  execution-memo skeleton, the annex-snapshot one-pager — each verified
  in place from the prior lanes' drafts (Ex-Ψ5), updated with dates, never
  re-drafted from scratch.
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C101–C104 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting — preceded by the arc consumption (Ex-N through Ex-T10), which may
   close the whole set with the post-record verdict.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0030's row-3 verdict traced to its manifest and its command; the rest
   struck with a reason — the hostile-webmaster test of my own prose,
   twenty-sixth run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C101 or C102 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the failure cells and the expected per-head mechanism at the
   eleventh unseen task's structure and the tenth architecture family's
   (C101), or the tenth recipe's predicted failure cells from the completed
   map (C102) — the "what would falsify this" column filled at writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v27 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, with the repo's own shelf added: branches reconciled, README
   current, residue removed, snapshot pairs current, figures re-derived.
6. **Ex-F · The teaching distillation, round twenty-six (S7):** the
   twenty-sixth question's verdict in four registers — the paper's sentence,
   the annex's sentence, the 30-second spoken claim, the 5-minute teaching
   explanation with a worked toy a stranger can run; the gap between the
   last two is where my teaching leaks.
7. **Ex-G · The stranger substitute from the visitor's chair (S2):** the
   self-review written from the chair a stranger would occupy — friction
   points → fixes → re-check row — filed before S4, so the S5 kill-date can
   never close the row with a skip.
8. **Ex-H · The fork drill, deepest form (S2, verdict-agnostic):** the
   continuing state (C101–C104) vs. the post-record state (PR-46/PR-47/PR-48)
   written as two one-page paths — what each verdict changes downstream,
   including the C101-vs-C102 choice and the post-record continuation choice —
   so next phase's S0 decision is a stamping, not a discovery.
9. **Ex-I10 · The boundary hand-roll, round fifteen (S5, C101 only, before
   any number is read):** the expected per-head mechanism at the eleventh
   unseen task's and the tenth architecture family's failure cells written
   by hand from C97's theory table — which per-head roles must transfer
   unchanged, which may re-tune, which should fail first, and what patching
   at those cells should reveal — the null hypothesis every measured
   fingerprint is compared against. One runnable check: the hand-rolled
   fingerprints printed and saved next to Ex-J10's observed ones, so the S6
   comparison is a diff, not a memory.
10. **Ex-J10 · The transfer reader, round fifteen (S5, C101 only):** the
    script that loads the frozen checkpoints at every P (including the
    eleventh unseen task's and the tenth family's), runs the per-head
    extraction and patching machinery, and emits the failure-cell table as a
    manifest-tagged JSON — with the patching-validity appendix of Part II,
    item 9 attached, so the run's verdict doubles as the instrument's
    end-to-end validation or its dated negative. One runnable check: the
    reader runs on the frozen checkpoints and its output is committed before
    the verdict paragraph is drafted.
11. **Ex-K10 · The sparse-recovery toy, revisited a twentieth time (my
    foundation challenge, tenth-family pass):** the one-file toy that
    recovers the addition table's DFT coefficients under L2 vs L1 penalties,
    now extended to the completion question: *does the sharpening ablation
    signature survive across ten architecture families and ten recipes, and
    where does it break?* One runnable check: the toy prints both
    reconstructions' sparsity and error plus the ablation table on a fixed
    seed, across ten architectures. This is the micro-scale intuition
    C102's verdict must not contradict.
12. **Ex-L10 · The "what does the dense solution compute?" sprint, round
    twenty (S5, C101 only):** the paper's hardest paragraph drafted at S5,
    then audited against the mechanism reading at S6 — prose that must
    survive contact with the manifest, the "computes something" claim earned
    or struck with one reason.
13. **Ex-M10 · The stranger-run drill on my own receipt (S1):** I execute
    MP-56's shipped artifact (the twenty-fifth) on a fresh clone as if I
    were the stranger — the transcript becomes the baseline against which
    the twenty-sixth artifact's transcript is compared. One runnable check:
    the baseline transcript saved beside the new one.
14. **Ex-N · The arc consumption, second generation (S0):** MP-40's Ex-N
    defined the terminal state; MP-41 executed it; MP-42 through MP-56
    consumed it fifteen times. This drill executes that second-generation
    consumption exactly as MP-56's memo stamped it.
15. **Ex-O · The arc consumption, third generation (S0):** MP-52's Ex-O
    defined the third-generation drill; MP-53 through MP-56 executed it; this
    drill consumes MP-56's Session-0 decision with dates, the criteria cited
    from the release it consumes. One runnable check: the execution memo
    exists, names the decision rule, cites the criteria from MP-56's release
    report.
16. **Ex-P … Ex-S9, Ex-T10 · The arc consumption, generations 4–16 (S0):**
    the consumption chain's deepest runs as MP-56 stamped them — each memo
    cites the criteria from the release report it consumes. One runnable
    check per drill: the execution memo exists and cites the criteria from
    the release report.
17. **Ex-T10 · The arc consumption, sixteenth generation (S0, new,
    verdict-agnostic):** the consumption chain's deepest run — MP-56's
    Session-0 decision consumed with dates as MP-57's intake, the
    fifteenth-generation post-record verdict read from ADR-0030 row 3 if
    the arc governs, the criteria cited, the release that follows (the
    sixteenth post-record question, or the C101–C104 adjudication), and what
    each of ADR-0030's possible verdicts changes in that execution. One
    runnable check: the execution memo exists, names the decision rule that
    closes or continues the program's science, and cites the criteria from
    MP-56's release report — the chain now sixteen generations deep, a
    sitting stamps, it never re-decides.
18. **Ex-S10 · The out-of-sample sprint, round fifteen (S5, C101 only):**
    the mechanism's predictions at the eleventh unseen task family written as
    a dated table before any number is read — task family, expected failing
    head role, expected order of failure, expected patching signature — with
    the falsifier column filled at writing time; the observed table compared
    at S6 as a diff, not a memory.
19. **Ex-U10 · The architecture-family sprint, round fifteen (S5, C101
    only):** the law's predictions at the tenth architecture family written
    as a dated table before any number is read — family, expected per-head
    role transfer or re-tuning, expected failure order, expected patching
    signature — with the falsifier column filled at writing time; the
    observed table compared at S6 as a diff, not a memory.
20. **Ex-V10 · The drift-attribution drill, round twelve (S5, C103 only):**
    the rate function's parameters re-estimated from the twenty-six
    transcripts before any fix, the fifteenth drift's components attributed
    — harness change vs. protocol drift vs. codebase aging — each component's
    contribution re-estimated, the top root-cause's fix dated in the same
    sitting. One runnable check: the re-estimated parameter table saved
    beside the drift numbers, so the S6 verdict is a diff, not a memory.
21. **Ex-W10 · The theory's falsifier column, round ten (S5, C101 only):**
    each tenth-round failure-cell explanation written with its own
    falsifier — the single observation that would refute the explanation of
    why this cell fails — filled at writing time, before the analysis; the
    S6 verdict is a diff between prediction and observation, never a memory.
22. **Ex-X10 · The equation-of-state prediction table, round ten (S5, C102
    only, new):** the tenth recipe's failure cells *predicted from the
    completed map* before any number is read — cell, predicted root cause,
    predicted ablation signature, predicted failure order — with the
    falsifier column filled at writing time; the observed map compared at S6
    as a diff, not a memory. This is the moment the phase diagram stops
    being a description and becomes a law with a five-transfer record.
23. **Ex-Y10 · The policy allocation drill, round ten (S5, C103 only):**
    the twentieth measurement's schedule derived from the rate model before
    the run — the next measurement, its budget, its predicted outcome, its
    falsifier — so the S6 verdict compares the schedule against what the
    receipt system actually did, as a diff, not a memory.
24. **Ex-Z10 · The public rubric draft, round ten (S5, C104 only, new):**
    the twelfth cohort's rubric written as a public artifact — scoring
    rule, evidence requirements, adjudication procedure, release license —
    before recruitment, so the twelfth measurement is taken under the
    published rule, never after it.
25. **Ex-Φ · The annex snapshot (S3, standing since MP-52):** the v27 annex
    written on the live shelf *and* mirrored into the repo as a dated,
    read-only copy in the same sitting; the v26 pair re-verified at Session 1
    (shelf copy hash vs. repo snapshot); the snapshot's own manifest tag, so
    `verify-claims` can check the pair. One runnable check: the repo
    snapshot's hash matches the shelf's dated copy at S7.
26. **Ex-Ω · The figure-regeneration audit (S1, standing since MP-52):**
    `make reproduce` run against the frozen configs and every tracked figure
    in `portfolio/figures/` re-derived — the corpus has grown by whatever
    MP-56's science added, so the audit re-runs against the grown set; a
    figure that cannot be re-derived from the committed command is struck
    from the showcase with one dated reason. One runnable check: the
    re-derived figures' manifest tags match the committed ones.
27. **Ex-Ψ5 · The pre-draft stack audit, fifth pass (Session −1, new, the
    anti-ceremony gate):** every pre-drafted artifact the prior lanes own —
    trial 3's pre-registration, the dense-characterization protocol, the
    R4/R5 scheduled-negative prose, the S0 intake checklist, the C101–C104
    memo skeletons, the annex-snapshot one-pager — verified on disk with its
    date; anything present is updated in place with a dated delta, anything
    missing is drafted once with a dated reason. The audit table is the
    transcript that keeps the waiting window a lane instead of a factory.
    One runnable check: the audit table names each artifact, its date, and
    its delta or its drafted-once reason.
28. **The waiting-window drills (Session −1):** Ex-α10 the DFT hand-roll,
    tenth pass (the derivation extended to the tenth family's geometry);
    Ex-β10 the four-registers rehearsal on the R1 no-head negative; Ex-γ10
    the scheduled-negative drafting drill — now a re-verification drill: the
    ADR-0003 rows 4–5 prose, trial 3's pre-registration and the
    dense-characterization protocol exist from prior lanes (Ex-Ψ5), this
    pass re-verifies the falsifier columns and updates in place; Ex-δ10 the
    stranger-run drill on the twenty-fifth artifact once it ships (the
    transcript becomes the twenty-sixth's baseline); Ex-ε10 the trial-3
    falsifier decision tree re-verified before trial 2's verdict is read.
29. **Habit · The clock check (every session):** ADR-0031's undated rows, the
    open PR's CI status line, the shelf's health — all three before any new
    prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, twenty-sixth execution.** A phase that opens two
  research questions is drift by another name; the unchosen candidates close
  in the same sitting as the choice — and the arc consumption may close all
  of them with the post-record verdict. The continuum law is the mechanical
  refusal of this drift — proven executable twenty-five times, it must
  simply be executed again.
- **The candidate set is frozen before S0, never improvised at it.** C101–C104
  are conditions, not predictions; a sitting decides, it never invents — and
  the terminal-state object is the hardest frozen object on the record:
  written by MP-40, executed by MP-41, consumed fifteen more times since —
  *consumed a sixteenth time* by MP-57, never re-negotiated in the
  consuming sitting.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0030's row-3 verdict in the sitting that owns
  it — or the post-record statement, if the arc governs.
- **The receipt compounds.** The twenty-sixth runnable artifact is only
  worth shipping because the first twenty-five transcripts proved the format
  — and if C103 opens, the receipts are a drift number measured fifteen
  times in a row, tested by people I did not choose, across an aging
  codebase. My showcase's story is now "read it, run it, watch me be wrong
  on the record," twenty-six receipts deep.
- **The waiting window is a lane, not a gap — and it is now seven phases
  wide.** MP-51's through MP-57's Session −1 lanes share the same weeks;
  each phase's pre-drafts live in named files of their own, and MP-57's lane
  verifies (Ex-Ψ5) instead of re-drafting. A day with no dated entry is a
  row without a date.
- **The pre-draft stack is verified, never re-drafted (fifth pass).** The
  trial-3 pre-registration, the dense-characterization protocol and the
  scheduled-negative prose have been drafted in every waiting window since
  MP-48; at generation twenty-six, drafting them again is ceremony, and
  verifying them with a date is discipline. Ex-Ψ5 is the gate, and the study
  log itself follows the vault's orphan law: a memo that links nothing is a
  note that proves nothing was understood.
- **Budget the wall-clock at launch, never at Session 7 — and from observed
  rates, never estimates.** The CPU is the binding constraint; the rates
  MP-29's runs produce become the budget's ground truth; every run gets a
  budget row, a heartbeat, a checkpoint-every-500, and a scheduled negative
  drafted while it is live. This is the architecture law that protects the
  release date.
- **A pinned toolchain is a promise; a compiled PDF is a receipt.** The
  toolchain pin landed in MP-51's Session 0 and is verified to a PDF in
  every Session 1 since; this phase re-verifies `make paper` green on this
  machine and in the CI mirror. Graceful failure was the bridge; green is
  the destination. The v27 rule ("opens only for new numbers") remains the
  insurance either way.
- **The record must survive its own shelf.** The Ex-Φ snapshot rule is now a
  standing row: verify the v26 pair, write the v27 pair, and let
  `verify-claims` check both — the record's first defense against a
  hosting-side loss, cheap enough to be a habit and strict enough to be a
  row.
- **Figures must be re-derivable, not just provenance-tagged.** A manifest
  tag on a stale figure is a silent lie; the figure-regeneration audit
  (Ex-Ω) makes "the showcase regenerates" a verified sentence instead of an
  assumption — and it re-runs as the corpus grows.
- **An instrument that never fired must say so, in the protocol note.** Path
  patching has been validated only by unit tests since MP-23; every phase
  since has re-stated it, and the R1 no-head negative made the scheduled
  negative the legitimate result. The countermeasure is not a promise of a
  head — it is the dated patching-validity appendix on every C101/C102
  protocol (Part II, item 9), so the verdict doubles as the instrument's
  end-to-end validation or its dated negative, and the Part IV reading on
  instrument certification is a dated row of the study log, not a footnote.
- **Protect the release report.** The serialized stack means MP-29's release
  is still the artifact everything downstream consumes; a slip at any link
  slides the whole chain. A promise can be re-planned forever, but a dated
  row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0030 at zero, the live
  URL, `verify-claims` at 0, the twenty-sixth teaching transcript on disk —
  a condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; the R1 no-head negative — 0/8
  heads, stamped 2026-08-14 — is the record's newest dated signature. The
  strongest form of the signature is the chain: negative → map →
  characterization → mechanism → causal verdict → circuit → law → theory →
  second prediction → third prediction → fourth prediction → fifth
  prediction → sixth prediction → seventh prediction → eighth prediction →
  ninth prediction → *tenth prediction* — or a record that knew when to end.
- **The mypy row is a row, not a mood.** The non-blocking lane is
  non-blocking by design, and the `typecheck-new` ratchet protects every new
  module — but a number that grows with every phase and belongs to no named
  row is drift in the tooling's own terms. Session 1 records the dated
  decision: paid down, or ratcheted with its own row. The same sentence
  closes the seven-phase-standing README staleness: the science outruns the
  narrative only until the narrative is a row.
- **The steady state is the reward, not the ceremony.** MP-57 will be the
  twentieth roadmap written from an *executed* roadmap's release report —
  the program at its normal, confirmed nineteen times. The machinery is the
  guardrail, never the goal: rows are dated in the sitting that owns them, or
  they are not rows. The pre-draft stack audit (Ex-Ψ5) is this phase's
  concrete refusal of the ceremony.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push (including the
  `commitlint-new` mirror); zero UNDECIDED rows at Session 8; release =
  merge plus 14 calendar days; a squash body pre-wrapped to <200-char lines
  before the merge call — the MP-54 incident's process lesson, now a law.
- **The showcase 30-second story:** *the program's twenty-sixth dated
  direction was written from its own release report — the cap honored, the
  stack executed, the steady state kept honest twenty times, the record
  taught twenty-six times in runnable artifacts, every public number still
  re-derives from one command line, the paper compiled to a PDF on the
  record, and the record consumed — sixteen times, with dates — its own
  terminal-state decision, and answered it in a release.* Every artifact
  this phase launches is written to that standard.

## Links

- [[00_meta/56_micro-phase-56-review-and-roadmap]] — the twenty-fifth
  question's review and roadmap; this roadmap's intake is ADR-0030's release
  report and MP-56's Session-0 decision, which Session 0 consumes again.
- [[00_meta/55_micro-phase-55-review-and-roadmap]] — the twenty-fourth
  question's review and roadmap, the intake chain's previous link.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat — and the row
  the terminal state executes.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/microscope-trial-table]] ·
  [[06_production_ai/notes/positive-control-protocol]] — the science C101–C104
  adjudicate over, whose pending verdicts are the intake.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/checkpoint-resume-durability]] ·
  [[06_production_ai/notes/scheduled-negatives-mp28]] — the CPU-budget canon
  the phase's runs are specified against.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.