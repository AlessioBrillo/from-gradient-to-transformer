---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-16
---

# Micro-Phase 42 — State Review and Roadmap: the eleventh question, written from the tenth release report

> **STATUS: REVIEW + ROADMAP, NOT A PRE-REGISTRATION.** This note is the
> companion review to [[00_meta/41_micro-phase-41-review-and-roadmap]], the
> tenth question's review and roadmap, and to the MP-41 review itself: it
> opens no rows, launches no runs, claims no window, and is wired into home
> only as a companion pointer — it is not a pre-registration and it is not
> counted against any cap, because the cap is spent. It is my personal
> state review and my step-by-step plan for the phase that starts at MP-42's
> Session 0, written in the same first-person register as my progress log so
> it doubles as the public record of how I reasoned about the program's
> steady state before I executed through it. Everything factual in this file
> was re-verified against the repository on 2026-08-16: working tree clean,
> `dev` reconciled with `main` at the MP-41 squash (PR #75, main at
> `7f6e06d`), 190 tracked tests, ruff clean, `verify-claims` at 0.

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
  scheduled no-head negative is now the verdict: 0/8 heads, peak diag+1 mass
  0.075 at epoch 499, peak val accuracy 0.5083 near epoch 1950,
  K-composition max 0.056.
- The exp2 and exp5 manifests are clean on disk; `verify-claims` at **0**,
  re-verified in the MP-41 drafting sitting and again in this one.

The arc my science has taken is the strongest thing I own: *will grokking
reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what
is the dense solution's structure?* (MP-29 S3's characterization, on disk) →
*which open question is deepest?* (C17/C18, MP-36's sitting) → *what does my
own phase map say about the boundary?* (C21–C24, MP-37's sitting) → *which of
C25–C28 does the mechanism reading open?* (MP-38's sitting) → *which of
C29–C32 does the causal verdict open?* (MP-39's sitting) → *which of C33–C36
does the complete circuit open?* (MP-40's sitting) → *which of C37–C40 does
the law open?* (MP-41's sitting). By MP-42's Session 0 the record will hold
ten dated directions, a characterized dense regime, a causal reading (or its
evidence lane), whichever of C37–C40 ADR-0015's sitting chose — and the
answer to the question MP-40 forced into a dated row and MP-41's Session 0
executes: **whether the record's arc has reached its terminal state.** The
eleventh question is the first one I choose with the terminal-state decision
*consumed* — or the first phase whose research row is the first question
*past* the record's closing sentence.

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no phase.
MP-37, MP-38, MP-39, MP-40 and MP-41 are the un-cap executed exactly once
each — their drafts and reviews on disk, conditioned on their predecessors'
releases. **ADR-0015's eight rows are the rows MP-41 will fill**;
**ADR-0016's eight rows are the rows this roadmap will fill** — exactly once,
under the continuum law, eleventh execution, written from MP-41's release
report rather than from the habit of pre-registering.

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

12+ provenance-guarded figures, the paper at v8/v9, the site and Space live
since the premiere, the essay annex at v8/v9, seven runnable teaching
artifacts with stranger-run transcripts (the receipts land only if the stack
ships: seven exist only if MP-33–MP-39 execute, the eighth ships in MP-40,
the ninth in MP-41, **the tenth in this phase**). My teaching lane ships the
tenth artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The intake is now a terminal-state verdict, not a candidate.** MP-40's
   deepest question — *is there a ninth question at all?* — forced the
   terminal-state fork into a dated row (Ex-N); MP-41's Session 0 **executes
   that rule with dates** — if the complete circuit (C33) and the boundary's
   mechanism (C34) both landed, the record's signature arc — negative → map →
   characterization → mechanism → causal proof → complete circuit → law — is
   complete, and the tenth question's deepest honest answer may be *there is
   no tenth question*, stamped as a verdict, not a failure. MP-42's Session 0
   is the first sitting that must **consume that execution** — and if the
   rule fired, the record is closed and the deepest honest question is no
   longer *which candidate opens* but *what is the first question past the
   record*. The single most dangerous drift is treating "the record closed"
   as an ending instead of as a verdict to consume: the post-record arc must
   be as executable as any continuing candidate.
2. **The stacked execution is still the critical path.** MP-42's Session 0
   consumes MP-41's release report, which consumes ADR-0015's, which awaits
   MP-29 through MP-40. A slip at any link slides the whole chain; **my
   highest-leverage act is unchanged: protect MP-29's window** — its release
   report is the artifact everything downstream consumes. Nothing in this
   phase may borrow a minute from it, and this draft is written
   verdict-agnostic by law: it re-plans not a single row of MP-29–MP-41.
3. **The steady state is the un-cap's end state, and it must not become
   ceremony.** MP-42 is the fifth roadmap written from an *executed*
   roadmap's release report — the program's normal, confirmed five times.
   The drift risk inverts and deepens: the machinery (ledgers, sessions,
   gate criteria) is now eleven executions deep, so the law's countermeasure
   is that rows must still be dated in the sitting that owns them, verdicts
   still consumed as artifacts, and zero UNDECIDED rows at Session 8 — the
   machinery is the guardrail, never the goal, and a stamped row with no
   science behind it is ceremony by another name.
4. **The paper's compile gate is the hardest artifact in the stack.** No TeX
   on this machine; MP-31's own canon applies early: *toolchains are pinned
   in Session 0, never discovered at Session 7.* The paper v12 rule ("opens
   only for new numbers, else the v11 is the record") is my insurance — a
   dated sentence, never a silence.
5. **The standing debt is undated by design and must not survive the
   stack.** exp5 1000-epoch ×3-seed (~15 h), clean-clone proof, graduation
   proof, `reproduce-multiseed`, W&B, the gate-debt transcript — each owned
   by a named row in MP-30–MP-36 and re-verified in MP-37's through MP-41's
   row 8. Row 8 of this phase re-verifies those closures with transcripts; a
   pending item cannot outlive a ledger.
6. **The science's next fork is the post-record arc vs. the continuing
   arc.** MP-41 adjudicates C37–C40 from ADR-0014's verdicts; MP-42's
   candidate set is conditioned on *that* verdict — C41 opens only on C37's
   positive reading, C42 only on C38's completed mechanism, C43 only on
   C39's dated rate, C44 only on C40's causal features — and the
   terminal-state rule overrides the set if MP-41's Session 0 executed the
   record's closure. The redemption (a sparse cell found anywhere) overrides
   both. My candidate set is frozen precisely so this fork is adjudicated at
   Session 0, never improvised.
7. **The showcase's receipts are still future, one deeper.** Seven
   stranger-run transcripts exist only if the stack ships; the eighth lands
   in MP-40, the ninth in MP-41, the tenth in this phase. C43 (the rate's
   first drift) is conditioned on ≥ 9 transcripts on disk at Session 0 —
   the receipt compounds only if the lanes execute.
8. **Stop-and-publish is a row, not a threat — and now it has a successor.**
   ADR-0004's row 5 (the record releases as-is) stays open as the program's
   honest exit: a phase is worth doing only if its candidate set can earn a
   paragraph the record does not already have. Every candidate below must
   beat that row in the sitting that chooses it. The eleventh execution
   sharpens this to its edge: if MP-41's Session 0 stamped the record
   complete, the strongest release this program can make is the record's
   closing release — and the deepest candidate past it is the one that earns
   the record's *first new paragraph*: the post-record question. The deepest
   form of laziness is not building what the record has already said.

## Part III — The roadmap, step by step (the continuum law, eleventh execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C41 | **The law at the unseen task** (C37's successor) — the circuit as a law becomes the circuit as a *prediction across tasks*: per-head fingerprints predicted at an unseen task family under the same harness, protocol and frozen checkpoints (modular subtraction, or a second modular task family at the same P), universality claimed across tasks or mapped where it breaks; the canonical-algorithm statement ("the dense solution is *the* algorithm this harness computes") tested at a new task, not re-confirmed at old ones | ADR-0015 row 3 = C37 with a positive verdict and transfer fingerprints on disk | C37 closed negative, or the terminal-state rule fired → no law to extend, or the record already has its closing sentence |
| C42 | **The mechanism across architectures** (C38's successor) — the dense→memorized sharpening's *driver* tested across model families (2-layer, MLP-mixed, head-count variants of the frozen recipe): is the mechanism a principle (it survives architecture change) or an architecture effect (it does not), with the dated negative as a verdict | ADR-0015 row 3 = C38 with the completed mechanism on disk (order-parameter dynamics across optimizer and schedule families, circuit-signature verdict, manifest-tagged) | C38 never opened, or its verdict was negative → no mechanism to transfer, this closes with that verdict |
| C43 | **The rate's first drift** (C39's successor) — the fifth reproducibility study: the rate re-measured with artifacts 9+ in the register at Session 0, per-step failures root-caused and fixed with dates, and the drift of the rate itself measured against the fourth study — a rate measured twice in a row is a drift number, not an anecdote (does a rate survive an aging codebase and a changing recipe?); the verdict is a dated reproducibility report with a rate and a drift, not a mood | ADR-0015 row 3 = C39 with a dated rate on disk AND ≥ 9 stranger-run transcripts at S0 | Fewer than 9 transcripts, or C39 never opened → the receipt system hasn't earned a fifth study |
| C44 | **The feature-complete circuit as pedagogy** (C40's successor) — the dense solution's SAE features mapped onto the per-head circuit *in full*: feature → head → frequency → output as a complete causal graph, every edge causally verified, then *shipped as the tenth runnable teaching artifact* — "read the circuit like source code" executed at feature resolution for a stranger, with the run-transcript as the receipt | ADR-0015 row 3 = C40 with causal feature ablations on disk | C40 never opened, or a sparse regime exists → the sparse reading owns the question |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥
3 checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The terminal-state override stands, deepened: **if MP-41's Session 0
executed MP-40's Ex-N rule and the record closed (the complete circuit and
the boundary's mechanism both landed, and the one-pager's rule declared the
arc complete), no successor opens from the old arc — MP-42's Session 0
instead opens the post-record arc: the first question past the record,
chosen in that sitting from the pre-registered set below.** The rule is
executed with dates at Session 0; it is never improvised and never
re-negotiated in the sitting that consumes it.

### The post-record pre-registered set (chosen only if MP-41 closed the record)

| # | Candidate | Why it would open | Why it would close |
|---|---|---|---|
| PR-1 | **The sparse question, next generation** — the record's complete dense law carried to a NEW harness: the microscope's dated findings (renormalization cleared, the wd × cosine interaction named, trials 2–3 stamped) as the design input for a recipe that can go sparse — because the old harness's negative is now characterized, the phenomenon's question is alive at a new address, and the record's laws are the new harness's specification, not its hope | The record closed with the dense regime characterized | The record never closed, or the redemption fired first → the sparse question belongs to the old arc |
| PR-2 | **The law at the record's edge** — the completed circuit-as-a-law claimed at a task family the record never read, on the frozen checkpoints that exist today: the record's laws as the new arc's first predictions, the same harness at a new task | The record closed with the law on disk | The record never closed → the law's successors are C41's, not the post-record arc's |
| PR-3 | **The record as a teaching corpus** — the closed record distilled into the definitive public course: the ten runnable artifacts, the eleven dated directions and the complete circuit assembled into the showcase's terminal teaching artifact, the record's closing release's deepest successor on the teaching lane | The record closed with ten receipts on disk | The record never closed → the teaching lane continues as the continuum's row 7 |

The likely survivor, written as a condition chain, never a prediction: if
MP-41's Session 0 fired the terminal-state rule → **the post-record arc
opens** — the program's first new direction, the record's laws as the
intake; else if C37 landed positive → **C41** — the law extended to
prediction across tasks, always CPU-runnable on checkpoints that exist
today; else if C38's mechanism landed → **C42**; else **C43**
(always-runnable, the showcase's own science, receipts now nine deep); C44
is the evidence lane and the teaching lane's anchor.

### The nine sessions

1. **Session 0 (~1 h) — the gate truthing + the terminal-state consumption +
   the continuum choice.** Consume MP-41's release report row by row:
   ADR-0015 at zero UNDECIDED rows, the live URL re-clicked in the sitting,
   `verify-claims` at its actual count, the ninth teaching transcript on
   disk, `dev == main`. Commit the intake table before a single continuum
   row opens. Then **Ex-N: execute the post-record rule with dates** —
   MP-41's terminal-state decision consumed: if the record closed, the first
   post-record question chosen from the pre-registered set (PR-1/PR-2/PR-3),
   each opening-or-closure memo in three sentences with a falsifier; if not,
   the C41–C44 adjudication: exactly one opens as row 3, the unchosen close
   with one dated reason each, stamped in the same sitting. Open ADR-0016
   with its eight rows, windows and kill-dates; declare the terminus (release
   = merge + 14 calendar days); promote this roadmap from MP-41's release
   report, deviations recorded as dated ledger notes. *Exit: intake signed;
   the terminal-state decision executed; row 3 chosen (or the post-record
   row opened); ledger open.*
2. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — year ten begins with a baseline. Row 8: MP-41's
   stamped closures re-verified (W&B, clean-clone proof, graduation proof,
   `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch resolution) — each
   cell LAUNCHED-with-transcript or CLOSED-with-one-reason; a claimed closure
   without its transcript stays open and blocks Session 8. *Exit: rows 5 and
   8 stamped.*
3. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the tenth research question's verdict (ADR-0015 row 3) becomes the
   paper-v12 section, the annex table, or the results-page row — every number
   manifest-tagged, consumed in the sitting that owns it; if the record
   closed, this is where the post-record statement is framed from the closing
   release, never rewritten. Row 2: v12 opens only if row 1 lands new
   numbers; else "the v11 is the record" is the dated reason and `make paper`
   is re-verified against v11. Row 6's substitute filed from the visitor's
   chair, before the window opens (Ex-G); the fork drill (Ex-H) and the
   post-record execution (Ex-N) land here. *Exit: rows 1 and 2 dated;
   substitute filed; Ex-N's execution memo on disk.*
4. **Session 3 (~2–3 h) — the essay annex v12.** `portfolio/essay-annex-12.md`:
   the tenth question's verdict set and the teaching lane's ninth receipt
   distilled into one dated annex; the reverse claims audit at zero (prose →
   manifest → command); each claim's "what would falsify this" column filled
   at writing time. The annex is amended, never rewritten. *Exit: row 4
   dated; audit at zero.*
5. **Session 4 (~1 h) — the stranger round 12 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. *Exit: window open,
   kill-date declared.*
6. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat — or, if the record
   closed, the post-record row's protocol opened under the same discipline.
   If C41: the expected fingerprints at the unseen task, the universality
   bound across tasks, and the transfer verdict all written as falsifiable
   predictions before a single number is read (Ex-C, Ex-I, Ex-J). Row 6's
   kill-date honored (feedback → matrix drafted; silence → substitute closes
   it). Row 7: the tenth teaching artifact's skeleton drafted — walkthrough
   v10, 10-minute talk v10, or Colab grokking notebook v8 — with its
   ship-date. *Exit: row 3 pre-registered and launched (or the post-record
   protocol opened); row 6 dated either way; row 7's skeleton drafted.*
7. **Session 6 (~1–2 h) — the research verdict sitting.** Row 3's verdict
   read from the manifest: completed and dated, or window closed and the
   scheduled negative is the result — drafted while the run was live (Ex-D),
   so this sitting is a stamping, not a discovery. *Exit: row 3 dated either
   way.*
8. **Session 7 (~2–3 h) — the shelf rehearsal + the re-check row + the
   teaching polish.** Row 5: the hostile-webmaster walk at zero beside the
   browser, every public number clicked back to disk. Row 6's re-check row
   dated. Row 7: the tenth artifact runs end to end on a stranger's machine
   (fresh clone / Colab session); the run transcript is the receipt; the
   teaching distillation (Ex-F) lands here. *Exit: rows 5, 6, 7 dated; the
   artifact shipped with its transcript.*
9. **Session 8 (~1 h) — the release.** ADR-0016 at zero UNDECIDED rows; the
   merge green locally and on GitHub; `dev == main`; home wired — this
   roadmap's companion status retired; the roadmap archived with its
   deviations, every deviation a dated ledger note. If the post-record arc
   opened, this sitting stamps the program's first new direction past the
   record — the record's closing sentence consumed, never repeated. *Exit:
   the merge; the program's eleventh dated direction — or the first dated
   direction of the post-record arc.*

### The one measured line

ADR-0016 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row (or the post-record row) whose verdict (or scheduled negative)
re-derives from a manifest; `verify-claims` at 0 with every public number
re-derivable from one command line; the hostile-webmaster walk at zero on the
live shelf, year ten; the tenth teaching artifact shipped with a
stranger-runnable transcript; `dev == main` and the program's eleventh dated
direction — or, if the terminal-state rule fired, the first dated direction
of the post-record arc.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk.

1. **Cross-task universality (the C41 reading).** Olsson, Elhage, Nanda et
   al., *In-context Learning and Induction Heads* (2022) for what transfers
   across task families; Elhage et al., *A Mathematical Framework for
   Transformer Circuits* (2021) for the QK/OV machinery the transfer is
   claimed over; Chughtai et al., *A Toy Model of Universality* (2023) for
   what "the same algorithm" can honestly mean *across unseen tasks*; and
   the skeptical line on where universality claims overreach, so the bound
   at the task boundary is mapped, never asserted. My C37 verdict and its
   transfer fingerprints frame the reading. **Prediction to write before
   the analysis**: the fingerprints at the unseen task; the universality
   bound across tasks; the transfer verdict. **Primary sources**:
   `exp2_checkpoint_seed{0,1,2}.pt`, C37's fingerprint table, the S3 note.
2. **The mechanism across architectures (the C42 reading).** Morwani et al.
   (2024) on the edge-of-numerical-stability regime, Gromov, *Grokking: A
   Memory Perspective* (2023), Power et al. (2022), Nanda et al. (2023) —
   now read at the *architecture* axis: what *survives* a change of model
   family, what a mechanism claims when the circuit changes shape, and where
   "the driver of the sharpening" is really an architecture effect.
   **Prediction**: the order-parameter dynamics across 1-layer vs 2-layer
   and attention-only vs MLP-mixed, and the transfer verdict (principle or
   architecture effect), written with falsifiers; C38's completed mechanism
   is this reading's admission ticket.
3. **Longitudinal reproducibility (the C43 reading).** Gelman & Loken, *The
   Garden of Forking Paths*; Pineau et al. (2021); the ML reproducibility
   line (NASEM's five pillars) — what a rate claims when it is measured
   *twice in a row on an aging codebase*: does a receipt system's rate
   drift, and what does a drift mean? My nine stranger-run transcripts are
   the data; I must decide what counts as drift before I measure any.
4. **Feature-complete circuits as pedagogy (the C44 reading).** Bricken et
   al. (2023); Cunningham et al. (2024); the dictionary-circuit and
   feature-universality line — what it takes to claim a *complete* causal
   graph at feature resolution (feature → head → frequency → output), where
   SAE readings on dense circuits have been shown to overreach, and how a
   complete feature-level graph becomes a *teachable* artifact rather than a
   poster. My Rung-5 datum (99.97% FVE, L0 = 136/256, 0% dead features) is
   the record's first data point.
5. **The post-record program (new, deepest).** Lakatos, *The Methodology of
   Scientific Research Programmes* (1978) — read a second time, now for what
   comes *after* a completed program: progressive vs degenerating problem
   shifts on the other side of the arc's end, Kuhn's normal science as the
   record's laws turned into the next arc's axioms, and the honest criterion
   for the first question past the record — a question that must earn the
   record's first *new* paragraph. This reading feeds Ex-N and the
   Session-0 question that MP-42 owns more deeply than any phase before it:
   *is the record's arc complete, and if so, what is the first question the
   record itself opens?* The answer can be the post-record arc's first dated
   row — Lakatos' point is that the decision is made on the record, never as
   a mood.
6. **The record teaches, round ten.** The eleventh verdict in four
   registers — the paper's sentence, the annex's sentence, the 30-second
   spoken claim, and the 5-minute teaching explanation with a worked toy a
   stranger can run; the gap between the last two is where my teaching
   leaks, and I will measure it deliberately by writing all four registers
   for the same verdict (Ex-F).
7. **The redemption reading, or negative results as maps, the eleventh
   pass.** If a sparse cell exists by S0: Nanda et al.'s full per-frequency
   reading on the first sparse solution this harness ever produced. If not:
   how the *completed* law is reported honestly — the transfer fingerprints,
   the dynamics across the architecture axis, the falsified predictions, the
   mapped negative as a contribution — and how the post-record harness would
   be designed from the dated negatives instead of from hope. Either way,
   the paper's hardest paragraph is the one that claims the dense solution
   *computes something*; I will draft it against this reading and let the
   manifest referee it.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-41's release report, deviations recorded as dated ledger
  notes.
- **ADR-0016**, the eleventh continuum ledger — eight rows pre-stamped with
  windows and kill-dates; rows 1–2 consumed from ADR-0015's verdicts; row 3
  the eleventh research question with its protocol note and heartbeat (or
  the post-record row's protocol); rows 4–8 the continuum's decisions.
- **`portfolio/essay-annex-12.md`** — the v12 annex, manifest-tagged,
  amended never rewritten.
- **The paper v12 diff** (`portfolio/paper/main.tex` v12 + diff log) or the
  dated "the v11 is the record" memo; `make paper` re-verified in the CI
  mirror.
- **The shelf health sheet + hostile-webmaster transcript** (site + Space at
  zero, year ten); the claims gate re-run on every merge.
- **`checklists/gate-debt.md`** — each cell's transcript or one-line reason,
  dated in Session 1, including the exp5 1000-epoch resolution's receipt
  re-checked.
- **The research row's pre-registration note** (site, metric, negative
  control, kill-date) in `06_production_ai/notes/` + the heartbeat artifact;
  if C41: the out-of-sample fingerprint figure spec written before the
  analysis, the figure itself manifest-tagged after. If the record closed:
  the post-record row's protocol note instead.
- **The tenth teaching artifact + its stranger-run transcript** (fresh-clone
  or Colab session receipt).
- **Ex-N's execution memo** — MP-41's terminal-state decision run with
  dates: closed or continuing, the criteria cited, the decision that follows
  (the first post-record question, or the C41–C44 adjudication), written
  verdict-agnostic in Session 2 and executed at Session 0.
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C41–C44 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting — preceded by the post-record execution (Ex-N), which may make
   the whole set close with the record's verdict.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0015's row-3 verdict traced to its manifest and its command; the rest
   struck with a reason — the hostile-webmaster test of my own prose, tenth
   run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C41 or C42 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the unseen-task fingerprints' expected cells, the universality
   bound across tasks, the mechanism's order-parameter dynamics across the
   architecture axis — the "what would falsify this" column filled at
   writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v12 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, year ten.
6. **Ex-F · The teaching distillation, round ten (S7):** the eleventh
   question's verdict in four registers — the paper's sentence, the annex's
   sentence, the 30-second spoken claim, the 5-minute teaching explanation
   with a worked toy a stranger can run; the gap between the last two is
   where my teaching leaks.
7. **Ex-G · The stranger substitute from the visitor's chair (S2):** the
   self-review written from the chair a stranger would occupy — friction
   points → fixes → re-check row — filed before S4, so the S5 kill-date can
   never close the row with a skip.
8. **Ex-H · The fork drill, deepest form (S2, verdict-agnostic):** the
   continuing state (C41–C44) vs the post-record state (PR-1/PR-2/PR-3)
   written as two one-page paths — what each verdict changes downstream,
   including the C41-vs-C42 choice and the post-record choice — so next
   phase's S0 decision is a stamping, not a discovery.
9. **Ex-I · The out-of-sample hand-roll (S5, C41 only, before any number is
   read):** the expected circuit fingerprint at the unseen task written by
   hand from the C37 law — which per-head roles must transfer unchanged,
   which may re-tune, which should vanish — the null hypothesis every
   measured fingerprint is compared against. One runnable check: the
   hand-rolled fingerprints printed and saved next to Ex-J's observed ones,
   so the S6 comparison is a diff, not a memory.
10. **Ex-J · The transfer reader (S5, C41 only):** the script that loads the
    frozen checkpoints at every P (including the unseen task's), runs C37's
    per-head extraction and patching machinery, and emits the fingerprint
    table as a manifest-tagged JSON. One runnable check: the reader runs on
    the frozen checkpoints and its output is committed before the verdict
    paragraph is drafted.
11. **Ex-K · The sparse-recovery toy, revisited a fifth time (my foundation
    challenge, architecture-transfer pass):** the one-file toy that recovers
    the addition table's DFT coefficients under L2 vs L1 penalties, now
    extended to the architecture question: *where in (wd, P, architecture)
    does the L2-minimal solution stop generalizing, and does its weight-norm
    trajectory at the transition change when the model family does?* One
    runnable check: the toy prints both reconstructions' sparsity and error
    plus the norm trajectory on a fixed seed, across two architectures. This
    is the micro-scale intuition C42's verdict must not contradict.
12. **Ex-L · The "what does the dense solution compute?" sprint, round five
    (S5, C41 only):** the paper's hardest paragraph drafted at S5, then
    audited against the mechanism reading at S6 — prose that must survive
    contact with the manifest, the "computes something" claim earned or
    struck with one reason.
13. **Ex-M · The stranger-run drill on my own receipt (S1):** I execute the
    previous phase's shipped artifact on a fresh clone as if I were the
    stranger — the transcript becomes the baseline against which the tenth
    artifact's transcript is compared. One runnable check: the baseline
    transcript saved beside the new one.
14. **Ex-N · The post-record execution (S0, new, verdict-agnostic):**
    MP-40's Ex-N defined the terminal state; MP-41 executed it; this drill
    *consumes that execution with dates* — the criteria cited, the verdict
    stamped (record closed or continuing), the release that follows (the
    first post-record question, or the C41–C44 adjudication), and what each
    of ADR-0015's possible verdicts changes in that execution. One runnable
    check: the execution memo exists, names the decision rule that closes or
    continues the program's science, and cites the criteria from MP-41's
    release report.
15. **Habit · The clock check (every session):** ADR-0016's undated rows,
    the open PR's CI status line, the shelf's health — all three before any
    new prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, eleventh execution.** A phase that opens two
  research questions is drift by another name; the unchosen candidates close
  in the same sitting as the choice — and the post-record rule may close all
  of them with the record's verdict. The continuum law is the mechanical
  refusal of this drift — proven executable ten times, it must simply be
  executed again.
- **The candidate set is frozen before S0, never improvised at it.** C41–C44
  are conditions, not predictions; a sitting decides, it never invents — and
  the terminal-state override is the hardest frozen object of all: written
  by MP-40, executed by MP-41, *consumed* by MP-42, never re-negotiated in
  the consuming sitting.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0015's row-3 verdict in the sitting that owns
  it — or the post-record statement, if the record ended.
- **The receipt compounds.** The tenth runnable artifact is only worth
  shipping because the first nine transcripts proved the format — and if
  C43 opens, the receipts stop being anecdotes and become a *drift number*
  measured twice in a row, tested by someone I did not choose, across an
  aging codebase. My showcase's story is now "read it, run it, watch me be
  wrong on the record," ten receipts deep.
- **The steady state is the reward, not the ceremony.** MP-42 is the fifth
  roadmap written from an *executed* roadmap's release report — the program
  at its normal, confirmed five times. The cap's lesson was that promises
  without dates drift; the steady state's discipline is that the machinery
  never becomes the goal: rows are dated in the sitting that owns them, or
  they are not rows.
- **Stop-and-publish stays open, and the post-record arc is now the deepest
  row.** ADR-0004's row 5 is the honest exit; a candidate set that cannot
  earn a paragraph the record lacks is a phase that should close itself. If
  MP-41 stamped the record complete, the strongest release this program can
  make is the record's closing release — and the deepest candidate past it
  earns the record's *first new paragraph*. This is the deepest form of
  laziness: do not build what the record has already said.
- **Toolchains are pinned in S0, never discovered at S7.** The paper's
  compile gate is the hardest artifact in the stack; the v12 rule ("opens
  only for new numbers") is the insurance that makes a missing toolchain a
  dated reason, not a crisis.
- **Protect the release report.** The serialized stack means MP-29's release
  is the artifact everything downstream consumes; a slip at any link slides
  the whole chain. The deepest law still applies: a promise can be re-planned
  forever, but a dated row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0015 at zero, the live
  URL, `verify-claims` at 0, the ninth teaching transcript on disk — a
  condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; the record's closing sentence — if
  it lands — is the strongest form of the signature: a negative that became
  a map, a map that became a characterization, a characterization that
  became a mechanism, a mechanism that earned its causal verdict, a circuit
  that earned its complete reading, a circuit that earned its law, a law
  that predicted an unseen point — or a record that knew when to end.
- **The debt row re-verifies; it never re-does.** A stamped closure is
  re-checked with its transcript; a genuinely new debt cell is a NEW row,
  never a revision. A pending item cannot outlive a ledger.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED
  rows at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story:** *the program's eleventh dated direction
  was written from its own release report — the cap honored, the stack
  executed, the steady state kept honest five times, the record taught ten
  times in runnable artifacts, every public number still re-derives from
  one command line, and the record consumed — with dates — its own
  terminal-state decision, and answered it in a release.* Every artifact
  this phase launches is written to that standard.

## Links

- [[00_meta/41_micro-phase-41-review-and-roadmap]] · [[00_meta/40_micro-phase-40-review-and-roadmap]] —
  the tenth question's review and roadmap; this roadmap's intake is
  ADR-0015's release report, the rows this review conditions on, and MP-41's
  Ex-N execution of MP-40's terminal-state rule, which Session 0 consumes.
- [[00_meta/39_micro-phase-39-review-and-roadmap]] · [[00_meta/38_micro-phase-38-review-and-roadmap]] —
  the seventh and eighth questions' reviews and roadmaps, the un-cap's
  steady state confirmed five times.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat — and the
  row the terminal state executes.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/positive-control-protocol]] ·
  [[06_production_ai/notes/microscope-trial-table]] — the science C41–C44
  adjudicate over, whose pending verdicts are the intake.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.