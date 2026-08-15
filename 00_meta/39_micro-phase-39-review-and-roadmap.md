---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-15
---

# Micro-Phase 39 — State Review and Roadmap: the eighth question, written from the seventh release report

> **STATUS: REVIEW + ROADMAP, NOT A PRE-REGISTRATION.** This note is the
> companion review to [[00_meta/38_micro-phase-38-review-and-roadmap]], the
> binding conditional draft of the seventh question, and to the MP-38 review
> itself: it opens no rows, launches no runs, claims no window, and is wired
> into home only as a companion pointer — it is not a pre-registration and it
> is not counted against any cap, because the cap is spent. It is my personal
> state review and my step-by-step plan for the phase that starts at MP-39's
> Session 0, written in the same first-person register as my progress log so
> it doubles as the public record of how I reasoned about the program's
> steady state before I executed through it. Everything factual in this file
> was re-verified against the repository on 2026-08-15: working tree clean,
> `dev == main` at `05837e0`, 190 tracked tests, ruff clean, blocking mypy
> clean, `verify-claims` at 0.

## Part I — Where I stand (state review, verified against the repo)

### The scientific ledger

The record's deepest fact has not changed and now has seven dated
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
- The exp2 and exp5 manifests are clean on disk (git_sha 9a67b10, a50f943);
  `verify-claims` at **0**, re-verified in the MP-38 drafting sitting and
  again in this one.

The arc my science has taken is the strongest thing I own: *will grokking
reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what
is the dense solution's structure?* (MP-29 S3's characterization, on disk) →
*which open question is deepest?* (C17/C18, MP-36's sitting) → *what does my
own phase map say about the boundary?* (C21–C24, MP-37's sitting) → *which of
C25–C28 does the mechanism reading open?* (MP-38's sitting). By MP-39's
Session 0 the record will hold seven dated directions, a characterized dense
regime, a causal reading (or its evidence lane), and whichever of C25–C28
ADR-0012's sitting chose — so the eighth question is the first one I choose
with a *causal verdict* (or the lane that earns it) already on the record.

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no
phase. MP-37 is the un-cap executed exactly once — the draft and its review
are on disk, conditioned on ADR-0010's release. MP-38 is the seventh
execution: **ADR-0012's eight rows are the rows MP-38 will fill**.
**ADR-0013's eight rows are the rows this roadmap will fill** — exactly once,
under the continuum law, eighth execution, written from MP-38's release
report rather than from the habit of pre-registering.

### The CI floor and the toolchains

190+ tracked tests, ruff, blocking mypy and markdownlint are green at the
last release; `verify-claims` at 0. The verified gaps, stated as facts not
hopes: no LaTeX toolchain on this machine (`make paper` is graceful, not
green), no Pages deploy workflow in `.github/workflows/`, no `publish:`
frontmatter policy, `portfolio/projects/` holds figures but no project
write-ups, W&B never connected. Each is a dated row owned by
MP-30/31/34/35/36 — their residue, never my re-planning.

### The showcase corpus at intake

12+ provenance-guarded figures, the paper at v5/v6, the site and Space live
since the premiere, the essay annex at v5/v6, five runnable teaching
artifacts with stranger-run transcripts (the receipts land only if the stack
ships: five exist only if MP-33–MP-36 execute, the sixth ships in MP-38, the
seventh in MP-39). My teaching lane ships the seventh artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The stacked execution is still the critical path.** MP-39's Session 0
   consumes MP-38's release report, which consumes ADR-0011's, which awaits
   MP-29 through MP-36. A slip at any link slides the whole chain; **my
   highest-leverage act is unchanged: protect MP-29's window** — its release
   report is the artifact everything downstream consumes. Nothing in this
   phase may borrow a minute from it, and this draft is written
   verdict-agnostic by law: it re-plans not a single row of MP-29–MP-38.
2. **The steady state is the un-cap's end state, and it must not become
   ceremony.** MP-38 was the first roadmap written from an *executed*
   roadmap's release; MP-39 is the second — the program's normal, confirmed
   twice. The drift risk inverts: the machinery (ledgers, sessions, gate
   criteria) is now the habit, so the law's countermeasure is that rows must
   still be dated in the sitting that owns them, verdicts still consumed as
   artifacts, and zero UNDECIDED rows at Session 8 — the machinery is the
   guardrail, never the goal.
3. **The paper's compile gate is the hardest artifact in the stack.** No TeX
   on this machine; MP-31's own canon applies early: *toolchains are pinned
   in Session 0, never discovered at Session 7.* The paper v9 rule ("opens
   only for new numbers, else the v8 is the record") is my insurance — a
   dated sentence, never a silence.
4. **The standing debt is undated by design and must not survive the
   stack.** exp5 1000-epoch ×3-seed (~15 h), clean-clone proof, graduation
   proof, `reproduce-multiseed`, W&B, the gate-debt transcript — each owned
   by a named row in MP-30–MP-36 and re-verified in MP-37's and MP-38's row
   8. Row 8 of this phase re-verifies those closures with transcripts; a
   pending item cannot outlive a ledger.
5. **The science's next fork is already visible, one verdict deeper.** MP-38
   adjudicates C25–C28 from ADR-0011's verdicts; MP-39's candidate set is
   conditioned on *that* verdict — C29 opens only on C25's positive reading,
   C30 only on C26's completed boundary law, C31 only on C27's dated rate,
   C32 only on C28's regime map. The redemption (a sparse cell found
   anywhere) overrides the set. My candidate set is frozen precisely so this
   fork is adjudicated at Session 0, never improvised.
6. **The showcase's receipts are still future, one deeper.** Six
   stranger-run transcripts exist only if the stack ships; the seventh lands
   in MP-39. C31 (the rate re-measured) is conditioned on ≥ 5 transcripts on
   disk at Session 0 — the receipt compounds only if the lanes execute.
7. **Stop-and-publish is a row, not a threat.** ADR-0004's row 5 (the record
   releases as-is) stays open as the program's honest exit: a phase is worth
   doing only if its candidate set can earn a paragraph the record does not
   already have. Every candidate below must beat that row in the sitting
   that chooses it.

## Part III — The roadmap, step by step (the continuum law, eighth execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C29 | **The causal circuit, complete** (C25's successor) — the dense P=113 solution read as a fully causal circuit: every head patched, the K-composition's causal share quantified, the frequency-ablation effect profile extended to the full patch matrix, and the shortcut-vs-canonical adjudication (Liu et al., Chughtai et al.) delivered as a dated verdict with the patching data in hand | ADR-0012 row 3 = C25 with a positive verdict on disk (per-head ablation profile, causal share, manifest-tagged) | C25 closed negative → the causal reading lacks its data; this closes with that verdict |
| C30 | **The boundary law at prediction** (C26's successor) — the dense→memorized boundary as predictive science: critical wd vs P written as a scaling law *before* the analysis, boundary width and sharpening exponents measured, the Morwani edge-of-numerical-stability check across the full diagram, and one out-of-sample P predicted in advance | ADR-0012 row 3 = C26 with the completed boundary law on disk (critical line, sharpening, manifest-tagged) | C26 never opened, or its law not sharp → closes with that verdict |
| C31 | **The receipts, now a measured rate** (C27's successor) — the reproducibility rate re-measured with artifacts 6–7 in the register, per-step failures root-caused and fixed with dates; the verdict is a dated reproducibility report with a rate, not a mood | ADR-0012 row 3 = C27 with a dated rate on disk AND ≥ 5 stranger-run transcripts at S0 | Fewer than 5 transcripts, or C27 never opened → the receipt system hasn't earned a third study |
| C32 | **Dense-regime features, causally verified** (C28's successor) — the dense solution's SAE features given causal meaning: feature ablations on the dense circuit, L0/FVE/dead-features converted from regime labels into "these features compute X" claims | ADR-0012 row 3 = C28 with a regime-labeled map on disk | C28 never opened, or a sparse regime exists → the sparse reading owns the question |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥
3 checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The likely survivor, written as a condition chain, never a prediction: if
C25 landed positive → **C29** — the record's signature arc completed (negative
→ map → characterization → mechanism → causal proof → complete circuit),
always CPU-runnable on checkpoints that exist today; else if C26's boundary
law landed → **C30**; else **C31** (always-runnable, the showcase's own
science, receipts now six deep); C32 is the evidence lane.

### The nine sessions

1. **Session 0 (~1 h) — the gate truthing + the continuum choice.** Consume
   MP-38's release report row by row: ADR-0012 at zero UNDECIDED rows, the
   live URL re-clicked in the sitting, `verify-claims` at its actual count,
   the sixth teaching transcript on disk, `dev == main`. Commit the intake
   table before a single continuum row opens. Then the C29–C32 adjudication:
   each candidate's opening-or-closure memo in three sentences with a
   falsifier; exactly one opens as row 3; the unchosen close with one dated
   reason each, stamped in the same sitting. Open ADR-0013 with its eight
   rows, windows and kill-dates; declare the terminus (release = merge + 14
   calendar days); promote this roadmap from MP-38's release report,
   deviations recorded as dated ledger notes. *Exit: intake signed; row 3
   chosen; ledger open.*
2. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — year seven begins with a baseline. Row 8: MP-38's
   stamped closures re-verified (W&B, clean-clone proof, graduation proof,
   `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch resolution) — each
   cell LAUNCHED-with-transcript or CLOSED-with-one-reason; a claimed closure
   without its transcript stays open and blocks Session 8. *Exit: rows 5 and
   8 stamped.*
3. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the seventh research question's verdict (ADR-0012 row 3) becomes the
   paper-v9 section, the annex table, or the results-page row — every number
   manifest-tagged, consumed in the sitting that owns it. Row 2: v9 opens
   only if row 1 lands new numbers; else "the v8 is the record" is the dated
   reason and `make paper` is re-verified against v8. Row 6's substitute
   filed from the visitor's chair, before the window opens (Ex-G). *Exit:
   rows 1 and 2 dated; substitute filed.*
4. **Session 3 (~2–3 h) — the essay annex v9.** `portfolio/essay-annex-9.md`:
   the seventh question's verdict set and the teaching lane's sixth receipt
   distilled into one dated annex; the reverse claims audit at zero (prose →
   manifest → command); each claim's "what would falsify this" column filled
   at writing time. The annex is amended, never rewritten. *Exit: row 4
   dated; audit at zero.*
5. **Session 4 (~1 h) — the stranger round 9 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. *Exit: window open,
   kill-date declared.*
6. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat. If C29: the full patch
   matrix's expected zero cells, the causal-share bound, and the
   shortcut-vs-canonical verdict all written as falsifiable predictions
   before a single number is read (Ex-C, Ex-I, Ex-J). Row 6's kill-date
   honored (feedback → matrix drafted; silence → substitute closes it). Row
   7: the seventh teaching artifact's skeleton drafted — walkthrough v7,
   10-minute talk v7, or Colab grokking notebook v5 — with its ship-date.
   *Exit: row 3 pre-registered and launched; row 6 dated either way; row 7's
   skeleton drafted.*
7. **Session 6 (~1–2 h) — the research verdict sitting.** Row 3's verdict
   read from the manifest: completed and dated, or window closed and the
   scheduled negative is the result — drafted while the run was live (Ex-D),
   so this sitting is a stamping, not a discovery. *Exit: row 3 dated either
   way.*
8. **Session 7 (~2–3 h) — the shelf rehearsal + the re-check row + the
   teaching polish.** Row 5: the hostile-webmaster walk at zero beside the
   browser, every public number clicked back to disk. Row 6's re-check row
   dated. Row 7: the seventh artifact runs end to end on a stranger's machine
   (fresh clone / Colab session); the run transcript is the receipt; the
   teaching distillation (Ex-F) lands here. *Exit: rows 5, 6, 7 dated; the
   artifact shipped with its transcript.*
9. **Session 8 (~1 h) — the release.** ADR-0013 at zero UNDECIDED rows; the
   merge green locally and on GitHub; `dev == main`; home wired — this
   roadmap's companion status retired; the roadmap archived with its
   deviations, every deviation a dated ledger note. *Exit: the merge; the
   program's eighth dated direction, stamped in the same sitting.*

### The one measured line

ADR-0013 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row whose verdict (or scheduled negative) re-derives from a
manifest; `verify-claims` at 0 with every public number re-derivable from one
command line; the hostile-webmaster walk at zero on the live shelf, year
seven; the seventh teaching artifact shipped with a stranger-runnable
transcript; `dev == main` and the program's eighth dated direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk.

1. **Causal verification of complete circuits (the C29 reading).** Elhage et
   al., *A Mathematical Framework for Transformer Circuits* (2021) — per-head
   QK/OV decomposition, virtual weights, the residual stream as a
   communication channel — plus Wang et al., *Interpretability in the Wild*
   (2023) for the patching vocabulary, and Zhang & Nanda (2024) on
   attribution patching's limits: the tools to claim "this dense circuit
   computes X" *causally* for every head, not just the top-K. My C25 verdict
   and MP-38's ablation profile frame the reading. **Prediction to write
   before the analysis**: the full patch matrix; the causal-share bound; the
   shortcut-vs-canonical verdict. **Primary sources**:
   `exp2_checkpoint_seed{0,1,2}.pt`, C25's manifest, the S3 note.
2. **Statistical mechanics of the boundary, as predictive science (the C30
   reading).** Morwani et al. (2024) on the edge-of-numerical-stability
   regime, Gromov, *Grokking: A Memory Perspective* (2023), Power et al.
   (2022), Nanda et al. (2023) — order parameters, critical lines, boundary
   width, finite-size scaling, studied as theory **before** the scaling law
   is fixed. **Prediction**: critical wd vs P and sharpening exponents,
   written with falsifiers, plus one out-of-sample P predicted in advance;
   C26's completed boundary law on disk is this reading's admission ticket.
3. **Shortcut learning and universality, applied to my own dense solution,
   second pass.** Liu et al., *Transformers Learn Shortcuts to Automata*
   (2023); Chughtai et al., *A Toy Model of Universality* (2023) — the
   vocabulary to say *why* the dense solution is dense honestly, now at
   circuit resolution: is it a shortcut, or the canonical algorithm computed
   by a low-weight solution? This is the sentence C29's verdict must earn,
   and I will draft it against this reading (Ex-L).
4. **Feature causality in dense regimes (the C32 reading).** Bricken et al.
   (2023); Cunningham et al. (2024); the SAE scaling and architecture line
   (Gao et al. 2024; Rajamanoharan et al., JumpReLU, 2024); and the
   feature-ablation lineage (ACDC/EAP) — L0/FVE/dead-features as regime
   labels, and what it takes to claim a feature *causes* an output on a
   dense circuit. My Rung-5 datum (99.97% FVE, L0 = 136/256, 0% dead
   features on the 32-dimensional residual stream) is the record's first
   data point: dense-but-reconstructable is not sparse-but-interpretable,
   and I will write down what distinguishes the two before the map is drawn.
5. **Reproducibility science, the third pass (the C31 reading).** Gelman &
   Loken, *The Garden of Forking Paths*; Pineau et al. (2021) — how a rate
   is *re*-measured when the receipts are six deep: failure-rate baselines,
   per-step pass/fail definitions, what a reproducibility rate actually
   claims when the person running the steps is no longer me. My six
   stranger-run transcripts are the data; I must decide what counts as a
   "step" and a "pass" before I count any.
6. **The record teaches, round seven.** The eighth verdict in four registers
   — the paper's sentence, the annex's sentence, the 30-second spoken claim,
   and the 5-minute teaching explanation with a worked toy a stranger can
   run; the gap between the last two is where my teaching leaks, and I will
   measure it deliberately by writing all four registers for the same
   verdict (Ex-F).
7. **The redemption reading, or negative results as maps, the eighth pass.**
   If a sparse cell exists by S0: Nanda et al.'s full per-frequency reading
   on the first sparse solution this harness ever produced. If not: how a
   causally-verified dense circuit is reported honestly — the circuit
   diagram, the patch matrix, the falsified predictions, the mapped negative
   as a contribution. Either way, the paper's hardest paragraph is the one
   that claims the dense solution *computes something*; I will draft it
   against this reading and let the manifest referee it.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-38's release report, deviations recorded as dated ledger
  notes.
- **ADR-0013**, the eighth continuum ledger — eight rows pre-stamped with
  windows and kill-dates; rows 1–2 consumed from ADR-0012's verdicts; row 3
  the eighth research question with its protocol note and heartbeat; rows
  4–8 the continuum's decisions.
- **`portfolio/essay-annex-9.md`** — the v9 annex, manifest-tagged, amended
  never rewritten.
- **The paper v9 diff** (`portfolio/paper/main.tex` v9 + diff log) or the
  dated "the v8 is the record" memo; `make paper` re-verified in the CI
  mirror.
- **The shelf health sheet + hostile-webmaster transcript** (site + Space at
  zero, year seven); the claims gate re-run on every merge.
- **`checklists/gate-debt.md`** — each cell's transcript or one-line reason,
  dated in Session 1, including the exp5 1000-epoch resolution's receipt
  re-checked.
- **The research row's pre-registration note** (site, metric, negative
  control, kill-date) in `06_production_ai/notes/` + the heartbeat artifact;
  if C29: the full patch-matrix figure spec written before the analysis, the
  figure itself manifest-tagged after.
- **The seventh teaching artifact + its stranger-run transcript** (fresh-clone
  or Colab session receipt).
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C29–C32 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0012's row-3 verdict traced to its manifest and its command; the rest
   struck with a reason — the hostile-webmaster test of my own prose, seventh
   run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C29 or C30 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the patch matrix's zero cells, the causal-share bound, the
   scaling law's exponents — the "what would falsify this" column filled at
   writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v9 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, year seven.
6. **Ex-F · The teaching distillation, round seven (S7):** the eighth
   question's verdict in four registers — the paper's sentence, the annex's
   sentence, the 30-second spoken claim, the 5-minute teaching explanation
   with a worked toy a stranger can run; the gap between the last two is
   where my teaching leaks.
7. **Ex-G · The stranger substitute from the visitor's chair (S2):** the
   self-review written from the chair a stranger would occupy — friction
   points → fixes → re-check row — filed before S4, so the S5 kill-date can
   never close the row with a skip.
8. **Ex-H · The fork drill (S2, verdict-agnostic):** the redemption (a sparse
   cell found) vs the all-dense future written as two one-page paths — what
   each verdict changes downstream, including the C29-vs-C30 choice — so
   next phase's S0 choice is a stamping, not a discovery.
9. **Ex-I · The full-circuit patch hand-roll (S5, C29 only, before any
   number is read):** the expected patch matrix of the dense circuit written
   by hand from the mechanism reading — which patches should be null, which
   causal — the null hypothesis every measured patch is compared against.
   One runnable check: the hand-rolled matrix printed and saved next to
   Ex-J's observed matrix, so the S6 comparison is a diff, not a memory.
10. **Ex-J · The per-head causal reader v2 (S5, C29 only):** MP-38's Ex-J
    extended from ablation to full patching — the script that loads
    `exp2_checkpoint_seed{0,1,2}.pt`, runs per-head activations and path
    patches across the whole circuit, and emits the patch matrix as a
    manifest-tagged JSON. One runnable check: the reader runs on the frozen
    checkpoint and its output is committed before the verdict paragraph is
    drafted.
11. **Ex-K · The sparse-recovery toy, revisited (my foundation challenge,
    second pass):** the one-file toy that recovers the addition table's DFT
    coefficients under L2 vs L1 penalties, now extended to answer the
    boundary question: *where* in (wd, P) does the L2-minimal solution stop
    generalizing? One runnable check: the toy prints both reconstructions'
    sparsity and error on a fixed seed, plus a 2-D sweep grid. This is the
    micro-scale intuition C29's verdict must not contradict.
12. **Ex-L · The "what does the dense solution compute?" sprint, round two
    (S5, C29 only):** the paper's hardest paragraph drafted at S5, then
    audited against the mechanism reading at S6 — prose that must survive
    contact with the manifest, the "computes something" claim earned or
    struck with one reason.
13. **Ex-M · The stranger-run drill on my own receipt (S1, new):** I execute
    the previous phase's shipped artifact on a fresh clone as if I were the
    stranger — the transcript becomes the baseline against which the
    seventh artifact's transcript is compared. One runnable check: the
    baseline transcript saved beside the new one.
14. **Habit · The clock check (every session):** ADR-0013's undated rows,
    the open PR's CI status line, the shelf's health — all three before any
    new prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, eighth execution.** A phase that opens two research
  questions is drift by another name; the unchosen candidates close in the
  same sitting as the choice. The continuum law is the mechanical refusal of
  this drift — proven executable seven times, it must simply be executed
  again.
- **The candidate set is frozen before S0, never improvised at it.** C29–C32
  are conditions, not predictions; a sitting decides, it never invents.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0012's row-3 verdict in the sitting that owns
  it.
- **The receipt compounds.** The seventh runnable artifact is only worth
  shipping because the first six transcripts proved the format — and if C31
  opens, the receipts stop being anecdotes and become a measured rate, three
  studies deep. My showcase's story is now "read it, run it, watch me be
  wrong on the record," seven receipts deep.
- **The steady state is the reward, not the ceremony.** MP-39 is the second
  roadmap written from an *executed* roadmap's release report — the program
  at its normal, confirmed twice. The cap's lesson was that promises without
  dates drift; the steady state's discipline is that the machinery never
  becomes the goal: rows are dated in the sitting that owns them, or they
  are not rows.
- **Stop-and-publish stays open, and every candidate beats it.** ADR-0004's
  row 5 is the honest exit; a candidate set that cannot earn a paragraph the
  record lacks is a phase that should close itself. This is the deepest
  form of laziness: do not build what the record has already said.
- **Toolchains are pinned in S0, never discovered at S7.** The paper's
  compile gate is the hardest artifact in the stack; the v9 rule ("opens
  only for new numbers") is the insurance that makes a missing toolchain a
  dated reason, not a crisis.
- **Protect the release report.** The serialized stack means MP-29's release
  is the artifact everything downstream consumes; a slip at any link slides
  the whole chain. The deepest law still applies: a promise can be re-planned
  forever, but a dated row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0012 at zero, the live
  URL, `verify-claims` at 0, the sixth teaching transcript on disk — a
  condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; if C29 opens, the complete causal
  circuit is the strongest form of the record's signature: a negative that
  became a map, a map that became a characterization, a characterization
  that became a mechanism, a mechanism that earned its causal verdict, a
  circuit that earned its complete reading.
- **The debt row re-verifies; it never re-does.** A stamped closure is
  re-checked with its transcript; a genuinely new debt cell is a NEW row,
  never a revision. A pending item cannot outlive a ledger.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED
  rows at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story:** *the program's eighth dated direction
  was written from its own release report — the cap honored, the stack
  executed, the steady state kept honest twice, the record taught seven
  times in runnable artifacts, and every public number still re-derives from
  one command line.* Every artifact this phase launches is written to that
  standard.

## Links

- [[00_meta/38_micro-phase-38-review-and-roadmap]] · [[00_meta/36_micro-phase-37-the-sixth-question]] —
  the seventh question's review and binding draft; this roadmap's intake is
  ADR-0012's release report, the rows this review conditions on.
- [[00_meta/37_micro-phase-37-review-and-roadmap]] · [[docs/adr/0011-continuum-ledger-6]] —
  the sixth ledger, whose release MP-38 consumes; ADR-0012 and ADR-0013
  succeed it in series.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/positive-control-protocol]] ·
  [[06_production_ai/notes/microscope-trial-table]] — the science C29–C32
  adjudicate over, whose pending verdicts are the intake.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.