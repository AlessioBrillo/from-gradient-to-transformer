---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-15
---

# Micro-Phase 38 — State Review and Roadmap: the seventh question, written from the sixth release report

> **STATUS: REVIEW + ROADMAP, NOT A PRE-REGISTRATION.** This note is the
> companion review to [[00_meta/36_micro-phase-37-the-sixth-question]], the
> binding conditional draft of the sixth question, and to the MP-37 review
> itself: it opens no rows, launches no runs, claims no window, and is wired
> into home only as a companion pointer — it is not a pre-registration and it
> is not counted against any cap, because the cap is spent. It is my personal
> state review and my step-by-step plan for the phase that starts at MP-38's
> Session 0, written in the same first-person register as my progress log so
> it doubles as the public record of how I reasoned about the program's
> steady state before I executed through it. Everything factual in this file
> was re-verified against the repository on 2026-08-15.

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
  `verify-claims` at **0**, re-verified in the MP-37 drafting sitting.

The arc my science has taken is the strongest thing I own: *will grokking
reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what
is the dense solution's structure?* (MP-29 S3's characterization, on disk) →
*which open question is deepest?* (C17/C18, MP-36's sitting) → *what does my
own phase map say about the boundary?* (C21–C24, MP-37's sitting). By MP-38's
Session 0 the record will hold six dated directions, a characterized dense
regime, and whichever of C21–C24 MP-37's sitting opened — so the seventh
question is the first one I choose with the mechanism reading (or its
evidence lane) already on the record.

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no
phase. MP-37 is the un-cap executed exactly once — the draft and its review
are on disk, conditioned on ADR-0010's release. **ADR-0011's eight rows are
the rows MP-37 will fill**; **ADR-0012's eight rows are the rows this
roadmap will fill** — exactly once, under the continuum law, seventh
execution, written from MP-37's release report rather than from the habit of
pre-registering.

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
ships: four exist only if MP-33–MP-36 execute, the fifth ships in MP-37). My
teaching lane ships the sixth artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The stacked execution is still the critical path.** MP-38's Session 0
   consumes MP-37's release report, which itself consumes ADR-0010's release,
   which awaits MP-29 through MP-36. A slip at any link slides the whole
   chain; **my highest-leverage act is unchanged: protect MP-29's window** —
   its release report is the artifact everything downstream consumes.
   Nothing in this phase may borrow a minute from it, and this draft is
   written verdict-agnostic by law: it re-plans not a single row of
   MP-29–MP-37.
2. **The steady state is the un-cap's end state, and it must not become
   ceremony.** MP-37 was the first roadmap written from a release report;
   MP-38 is the first roadmap written from an *executed* roadmap's release —
   the program's normal. The drift risk inverts: the machinery (ledgers,
   sessions, gate criteria) is now the habit, so the law's countermeasure is
   that rows must still be dated in the sitting that owns them, verdicts
   still consumed as artifacts, and zero UNDECIDED rows at Session 8 — the
   machinery is the guardrail, never the goal.
3. **The paper's compile gate is the hardest artifact in the stack.** No TeX
   on this machine; MP-31's own canon applies early: *toolchains are pinned
   in Session 0, never discovered at Session 7.* The paper v8 rule ("opens
   only for new numbers, else the v7 is the record") is my insurance — a
   dated sentence, never a silence.
4. **The standing debt is undated by design and must not survive the
   stack.** exp5 1000-epoch ×3-seed (~15 h), clean-clone proof, graduation
   proof, `reproduce-multiseed`, W&B, the gate-debt transcript — each owned
   by a named row in MP-30–MP-36 and re-verified in MP-37's row 8. Row 8 of
   this phase re-verifies those closures with transcripts; a pending item
   cannot outlive a ledger.
5. **The science's next fork is already visible, one verdict deeper.** MP-37
   adjudicates C21–C24 from MP-36's verdicts; MP-38's candidate set is
   conditioned on *that* verdict — C25 opens only on C21's positive reading,
   C26 only on C22's monotone curves, C27 only on C23's dated rate, C28 only
   on C24's regime map. The redemption (a sparse cell found anywhere)
   overrides the set. My candidate set is frozen precisely so this fork is
   adjudicated at Session 0, never improvised.
6. **The showcase's receipts are still future, one deeper.** Five
   stranger-run transcripts exist only if the stack ships; the sixth lands
   in MP-38. C27 (the rate re-measured) is conditioned on ≥ 4 transcripts on
   disk at Session 0 — the receipt compounds only if the lanes execute.
7. **Stop-and-publish is a row, not a threat.** ADR-0004's row 5 (the record
   releases as-is) stays open as the program's honest exit: a phase is worth
   doing only if its candidate set can earn a paragraph the record does not
   already have. Every candidate below must beat that row in the sitting
   that chooses it.

## Part III — The roadmap, step by step (the continuum law, seventh execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C25 | **The dense mechanism, verified causally** (C21's successor) — the characterized dense algorithm read as a circuit: per-head ablation and patching on the dense P=113 solution, the frequency-ablation effect profile, the K-composition's causal role, and the shortcut-vs-canonical adjudication (Liu et al., Chughtai et al.) with the data in hand | ADR-0011 row 3 = C21 with a positive verdict on disk (per-head dictionaries, norm structure, manifest-tagged) | C21 closed negative → the mechanism reading lacks its data, this closes with that verdict |
| C26 | **The boundary law completed** (C22's successor) — the dense→memorized boundary as a quantitative statement: critical wd vs P, boundary width, sharpening exponents, the Morwani edge-of-numerical-stability check across the full diagram; predictive scaling written before the analysis | ADR-0011 row 3 = C22 with monotone order-parameter curves and sharpening on disk | C22 never opened, or its curves not monotone → closes with that verdict |
| C27 | **The receipts measured at depth** (C23's successor) — the reproducibility rate re-measured with artifacts 5–6 in the register, the per-step failures root-caused and fixed with dates; the verdict is a dated reproducibility report with a rate, not a mood | ADR-0011 row 3 = C23 with a dated rate on disk | Fewer than 4 transcripts at S0, or C23 never opened → the receipt system hasn't earned a second study |
| C28 | **The dense-regime feature study** (C24's successor) — what the dense solution's SAE features actually are (K-composition, frequency-tuned features), converting "dense but reconstructable" into "dense and interpretable this way" | ADR-0011 row 3 = C24 with a regime-labeled map on disk | C24 never opened, or a sparse regime exists → the sparse reading owns the question |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥
3 checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The likely survivor, written as a condition chain, never a prediction: if
C21 landed positive → **C25** — the record's signature arc completed
(negative → map → characterization → mechanism → causal proof), always
CPU-runnable on checkpoints that exist today; else if C22's boundary law
landed → **C26**; else **C27** (always-runnable, the showcase's own science,
receipts now five deep); C28 is the evidence lane.

### The nine sessions

1. **Session 0 (~1 h) — the gate truthing + the continuum choice.** Consume
   MP-37's release report row by row: ADR-0011 at zero UNDECIDED rows, the
   live URL re-clicked in the sitting, `verify-claims` at its actual count,
   the fifth teaching transcript on disk, `dev == main`. Commit the intake
   table before a single continuum row opens. Then the C25–C28 adjudication:
   each candidate's opening-or-closure memo in three sentences with a
   falsifier; exactly one opens as row 3; the unchosen close with one dated
   reason each, stamped in the same sitting. Open ADR-0012 with its eight
   rows, windows and kill-dates; declare the terminus (release = merge + 14
   calendar days); promote this roadmap from MP-37's release report,
   deviations recorded as dated ledger notes. *Exit: intake signed; row 3
   chosen; ledger open.*
2. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — year six begins with a baseline. Row 8: MP-37's
   stamped closures re-verified (W&B, clean-clone proof, graduation proof,
   `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch resolution) — each
   cell LAUNCHED-with-transcript or CLOSED-with-one-reason; a claimed closure
   without its transcript stays open and blocks Session 8. *Exit: rows 5 and
   8 stamped.*
3. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the sixth research question's verdict (ADR-0011 row 3) becomes the
   paper-v8 section, the annex table, or the results-page row — every number
   manifest-tagged, consumed in the sitting that owns it. Row 2: v8 opens
   only if row 1 lands new numbers; else "the v7 is the record" is the dated
   reason and `make paper` is re-verified against v7. Row 6's substitute
   filed from the visitor's chair, before the window opens (Ex-G). *Exit:
   rows 1 and 2 dated; substitute filed.*
4. **Session 3 (~2–3 h) — the essay annex v8.** `portfolio/essay-annex-8.md`:
   the sixth question's verdict set and the teaching lane's fifth receipt
   distilled into one dated annex; the reverse claims audit at zero (prose →
   manifest → command); each claim's "what would falsify this" column filled
   at writing time. The annex is amended, never rewritten. *Exit: row 4
   dated; audit at zero.*
5. **Session 4 (~1 h) — the stranger round 8 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. *Exit: window open,
   kill-date declared.*
6. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat. If C25: the per-head
   ablation effect profile, the K-composition's causal role, and the
   shortcut-vs-canonical adjudication all written as falsifiable predictions
   before a single number is read (Ex-C, Ex-I, Ex-J). Row 6's kill-date
   honored (feedback → matrix drafted; silence → substitute closes it). Row
   7: the sixth teaching artifact's skeleton drafted — walkthrough v6,
   10-minute talk v6, or Colab grokking notebook v4 — with its ship-date.
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
   dated. Row 7: the sixth artifact runs end to end on a stranger's machine
   (fresh clone / Colab session); the run transcript is the receipt; the
   teaching distillation (Ex-F) lands here. *Exit: rows 5, 6, 7 dated; the
   artifact shipped with its transcript.*
9. **Session 8 (~1 h) — the release.** ADR-0012 at zero UNDECIDED rows; the
   merge green locally and on GitHub; `dev == main`; home wired — this
   roadmap's companion status retired; the roadmap archived with its
   deviations, every deviation a dated ledger note. *Exit: the merge; the
   program's seventh dated direction, stamped in the same sitting.*

### The one measured line

ADR-0012 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row whose verdict (or scheduled negative) re-derives from a
manifest; `verify-claims` at 0 with every public number re-derivable from one
command line; the hostile-webmaster walk at zero on the live shelf, year
six; the sixth teaching artifact shipped with a stranger-runnable transcript;
`dev == main` and the program's seventh dated direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk.

1. **Causal verification of dense circuits (the C25 reading).** Elhage et
   al., *A Mathematical Framework for Transformer Circuits* (2021) — per-head
   QK/OV decomposition, virtual weights, the residual stream as a
   communication channel — plus Wang et al., *Interpretability in the Wild*
   (2023) for the patching vocabulary, and Zhang & Nanda (2024) on
   attribution patching's limits: the tools to claim "this dense circuit
   computes X" *causally*, not just correlationally. My C21 verdict and
   MP-29's S3 characterization note frame the reading. **Prediction to write
   before the analysis**: the per-head ablation effect profile; the
   K-composition's causal share; the shortcut-vs-canonical verdict.
   **Primary sources**: `exp2_checkpoint_seed{0,1,2}.pt`, the S3 note, C21's
   manifest.
2. **Statistical mechanics of the grokking boundary (the C26 reading).**
   Morwani et al. (2024) on the edge-of-numerical-stability regime, Gromov,
   *Grokking: A Memory Perspective* (2023), Power et al. (2022), Nanda et al.
   (2023) — order parameters, critical lines, boundary width, finite-size
   scaling, studied as theory **before** the order-parameter analysis is
   fixed. **Prediction**: critical wd vs P and sharpening exponents, written
   with falsifiers; C22's monotone curves on disk are this reading's
   admission ticket.
3. **Shortcut learning and universality, applied to my own dense solution.**
   Liu et al., *Transformers Learn Shortcuts to Automata* (2023); Chughtai
   et al., *A Toy Model of Universality* (2023) — the vocabulary to say *why*
   the dense solution is dense honestly: is it a shortcut, or the canonical
   algorithm computed by a low-weight solution? This is the sentence C25's
   verdict must earn, and I will draft it against this reading (Ex-L).
4. **SAE interpretability in dense regimes (the C28 reading).** Bricken et
   al. (2023); Cunningham et al. (2024); the SAE scaling and architecture
   line (Gao et al. 2024; Rajamanoharan et al., JumpReLU, 2024) — L0/FVE/
   dead-features as regime labels, not just diagnostics. My Rung-5 datum
   (99.97% FVE, L0 = 136/256, 0% dead features on the 32-dimensional
   residual stream) is the record's first data point: dense-but-reconstructable
   is not sparse-but-interpretable, and I will write down what distinguishes
   the two before the map is drawn.
5. **Reproducibility science, the second pass (the C27 reading).** Gelman &
   Loken, *The Garden of Forking Paths*; Pineau et al. (2021) — how a rate
   is *re*-measured honestly: failure-rate baselines, per-step pass/fail
   definitions, what a reproducibility rate actually claims when the receipts
   are five deep. My five stranger-run transcripts are the data; I must
   decide what counts as a "step" and a "pass" before I count any.
6. **The record teaches, round six.** The seventh verdict in four registers —
   the paper's sentence, the annex's sentence, the 30-second spoken claim,
   and the 5-minute teaching explanation with a worked toy a stranger can
   run; the gap between the last two is where my teaching leaks, and I will
   measure it deliberately by writing all four registers for the same
   verdict (Ex-F).
7. **The redemption reading, or negative results as maps, the seventh
   pass.** If a sparse cell exists by S0: Nanda et al.'s full per-frequency
   reading on the first sparse solution this harness ever produced. If not:
   how a characterized boundary is reported honestly — critical lines, order
   parameters, falsified predictions, the mapped negative as a contribution.
   Either way, the paper's hardest paragraph is the one that claims the
   dense solution *computes something*; I will draft it against this reading
   and let the manifest referee it.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-37's release report, deviations recorded as dated ledger
  notes.
- **ADR-0012**, the seventh continuum ledger — eight rows pre-stamped with
  windows and kill-dates; rows 1–2 consumed from ADR-0011's verdicts; row 3
  the seventh research question with its protocol note and heartbeat; rows
  4–8 the continuum's decisions.
- **`portfolio/essay-annex-8.md`** — the v8 annex, manifest-tagged, amended
  never rewritten.
- **The paper v8 diff** (`portfolio/paper/main.tex` v8 + diff log) or the
  dated "the v7 is the record" memo; `make paper` re-verified in the CI
  mirror.
- **The shelf health sheet + hostile-webmaster transcript** (site + Space at
  zero, year six); the claims gate re-run on every merge.
- **`checklists/gate-debt.md`** — each cell's transcript or one-line reason,
  dated in Session 1, including the exp5 1000-epoch resolution's receipt
  re-checked.
- **The research row's pre-registration note** (site, metric, negative
  control, kill-date) in `06_production_ai/notes/` + the heartbeat artifact;
  if C25: the per-head ablation figure spec written before the analysis, the
  figure itself manifest-tagged after.
- **The sixth teaching artifact + its stranger-run transcript** (fresh-clone
  or Colab session receipt).
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C25–C28 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0011's row-3 verdict traced to its manifest and its command; the rest
   struck with a reason — the hostile-webmaster test of my own prose, sixth
   run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C25 or C26 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the ablation effect profile, the K-composition's causal share,
   sharpening exponents — the "what would falsify this" column filled at
   writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v8 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, year six.
6. **Ex-F · The teaching distillation, round six (S7):** the seventh
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
   each verdict changes downstream, including the C25-vs-C26 choice — so
   next phase's S0 choice is a stamping, not a discovery.
9. **Ex-I · The causal-ablation hand-roll (S5, C25 only, before any number
   is read):** the expected effect profile of removing one frequency from
   the dense circuit, written by hand from the ideal-expansion theory — the
   null hypothesis every ablation result is measured against. One runnable
   check: the hand-rolled profile printed and saved next to Ex-J's observed
   profile, so the S6 comparison is a diff, not a memory.
10. **Ex-J · The per-head causal reader (S5, C25 only):** a small script
    that loads `exp2_checkpoint_seed{0,1,2}.pt`, runs per-head ablations and
    activation patches on the dense circuit, and emits effect profiles as a
    manifest-tagged JSON — the raw material the S6 verdict reads. One
    runnable check: the reader runs on the frozen checkpoint and its output
    is committed before the verdict paragraph is drafted.
11. **Ex-K · The sparse-recovery toy (my foundation challenge, extended):**
    the one-file toy that recovers the addition table's DFT coefficients
    under L2 vs L1 penalties — seeing with my own eyes why the L2-minimal
    solution is dense while the L1-minimal one is sparse, on the exact
    function the whole program has been chasing. One runnable check: the toy
    prints both reconstructions' sparsity and error on a fixed seed. This is
    the micro-scale intuition C25's verdict must not contradict.
12. **Ex-L · The "what does the dense solution compute?" sprint (S5, C25
    only):** the paper's hardest paragraph drafted at S5, then audited
    against the mechanism reading at S6 — prose that must survive contact
    with the manifest, the "computes something" claim earned or struck with
    one reason.
13. **Habit · The clock check (every session):** ADR-0012's undated rows,
    the open PR's CI status line, the shelf's health — all three before any
    new prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, seventh execution.** A phase that opens two
  research questions is drift by another name; the unchosen candidates close
  in the same sitting as the choice. The continuum law is the mechanical
  refusal of this drift — proven executable six times, it must simply be
  executed again.
- **The candidate set is frozen before S0, never improvised at it.** C25–C28
  are conditions, not predictions; a sitting decides, it never invents.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0011's row-3 verdict in the sitting that owns
  it.
- **The receipt compounds.** The sixth runnable artifact is only worth
  shipping because the first five transcripts proved the format — and if C27
  opens, the receipts stop being anecdotes and become a measured rate. My
  showcase's story is now "read it, run it, watch me be wrong on the
  record," six receipts deep.
- **The steady state is the reward, not the ceremony.** MP-38 is the first
  roadmap written from an *executed* roadmap's release report — the program
  at its normal. The cap's lesson was that promises without dates drift;
  the steady state's discipline is that the machinery never becomes the
  goal: rows are dated in the sitting that owns them, or they are not rows.
- **Stop-and-publish stays open, and every candidate beats it.** ADR-0004's
  row 5 is the honest exit; a candidate set that cannot earn a paragraph the
  record lacks is a phase that should close itself. This is the deepest
  form of laziness: do not build what the record has already said.
- **Toolchains are pinned in S0, never discovered at S7.** The paper's
  compile gate is the hardest artifact in the stack; the v8 rule ("opens
  only for new numbers") is the insurance that makes a missing toolchain a
  dated reason, not a crisis.
- **Protect the release report.** The serialized stack means MP-29's release
  is the artifact everything downstream consumes; a slip at any link slides
  the whole chain. The deepest law still applies: a promise can be re-planned
  forever, but a dated row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0011 at zero, the live
  URL, `verify-claims` at 0, the fifth teaching transcript on disk — a
  condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; if C25 opens, the causal proof of
  the dense mechanism is the strongest form of the record's signature: a
  negative that became a map, a map that became a characterization, a
  characterization that became a mechanism, a mechanism that earned its
  causal verdict.
- **The debt row re-verifies; it never re-does.** A stamped closure is
  re-checked with its transcript; a genuinely new debt cell is a NEW row,
  never a revision. A pending item cannot outlive a ledger.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED
  rows at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story:** *the program's seventh dated direction
  was written from its own release report — the cap honored, the stack
  executed, the steady state kept honest, the record taught six times in
  runnable artifacts, and every public number still re-derives from one
  command line.* Every artifact this phase launches is written to that
  standard.

## Links

- [[00_meta/37_micro-phase-37-review-and-roadmap]] · [[00_meta/36_micro-phase-37-the-sixth-question]] —
  the sixth question's review and binding draft; this roadmap's intake is
  ADR-0011's release report, the rows this review conditions on.
- [[00_meta/35_micro-phase-36-the-fifth-question]] · [[docs/adr/0010-continuum-ledger-5]] —
  the fifth ledger, whose release MP-37 consumes; ADR-0011 and ADR-0012
  succeed it in series.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/positive-control-protocol]] ·
  [[06_production_ai/notes/microscope-trial-table]] — the science C25–C28
  adjudicate over, whose pending verdicts are the intake.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.