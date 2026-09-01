---
tags: [type/lesson, phase/7, research/experiment, state/roadmap]
state: review
created: 2026-09-01
---

# MP-78 Session 0 Preparation: Capstone Integration & Publication Roadmap

## What it is

Personal study notes and execution roadmap for Micro-Phase 78 — the capstone integration and publication phase where I train a decoder-only transformer, reverse-engineer its circuits, and ship the complete portfolio.

## Why it exists / what problem it solves

MP-77 (GPU unblock + execution cascade) resolved the three hard blockers: P=113 GPU grokking launched, 10k-epoch induction run launched, clean-clone proof GREEN. MP-78 consumes MP-74's release report (ADR-0024 at zero UNDECIDED rows) and executes the 21st continuum ledger (ADR-0027) — training the unified model, producing the paper, deploying the portfolio, and releasing the 21st dated direction.

## How it works

### The Frozen Candidate Set (ADR-0027, 8 rows, chosen at Session 0, never improvised)

| # | Candidate | Opens Only If | Window | Kill-Date | Status |
|---|-----------|---------------|--------|-----------|--------|
| 1 | **Capstone Research Plan Execution** | Clean-clone proof GREEN (Phase 6 gate) | Session 1–5 | 2026-09-12 | **READY** |
| 2 | **Paper Prose from Manifests** | Paper v21 diff exists (new numbers from MP-74) | Session 2 | 2026-09-10 | **GATED** |
| 3 | **W&B Integration + Dashboard** | Always (Phase 6 residue) | Session 1–2 | 2026-09-08 | **READY** |
| 4 | **HF Spaces SAE Browser Deploy** | R5 executed with confirmed head (MP-74) | Session 3 | 2026-09-11 | **GATED** |
| 5 | **Portfolio Project Write-ups (×5)** | Figures exist for all 5 rungs | Session 3–4 | 2026-09-11 | **READY** |
| 6 | **Pages Deploy Workflow** | Paper v21 compiles | Session 5 | 2026-09-12 | **GATED** |
| 7 | **Capstone Teaching Artifact v21** | Capstone training complete + circuit discovery | Session 6 | 2026-09-13 | **GATED** |
| 8 | **Gate-Debt Closure + Final Release** | Rows 1–6 complete | Session 7–8 | 2026-09-14 | **GATED** |

### Universal Override

If MP-74 GPU run (R1) produced **SPARSE-FOURIER**:
- Row 2 (Paper) prioritizes per-frequency reading on the first sparse solution this harness ever produced
- Row 4 (SAE Browser) uses the sparse-regime checkpoint
- Row 7 (Teaching Artifact) centers the sparse circuit discovery narrative
- Kill-dates adjusted in the same session

If MP-74 GPU run produced **NO-GROK** (current expectation):
- Row 2 (Paper) writes the "dense attractor" derivation from R3 neuron ablation
- Row 4 (SAE Browser) stays on synthetic + best-available real checkpoint
- Row 7 (Teaching Artifact) centers "sometimes the model finds a different algorithm"

### Post-Record Override

If MP-74 Session 0 continued the post-record arc (it did not per ADR-0024 intake):
- Row 1 becomes "Post-Record Harness Design from Dated Negatives"
- Row 2 becomes "Ninth Post-Record Question"
- Row 3 becomes "Tenth Post-Record Question"
- etc.

## Session 0 Actions (This Sitting)

### 1. Consume MP-74 Release Report (ADR-0024 Final State)
- [ ] Read ADR-0024 at zero UNDECIDED rows
- [ ] Extract R1 verdict (SPARSE-FOURIER or NO-GROK)
- [ ] Extract R2/R3/R5 verdicts
- [ ] Extract teaching artifact v20 transcript location
- [ ] Extract paper v20 decision (diff or "v19 is record" memo)

### 2. Adjudicate ADR-0027 Candidate Set
- [ ] Row 1: Capstone execution — **OPEN** (clean-clone proof GREEN)
- [ ] Row 2: Paper prose — **OPEN** if new numbers, else **CLOSED** "v20 is record"
- [ ] Row 3: W&B integration — **OPEN** (always)
- [ ] Row 4: HF SAE Browser — **OPEN** if MP-74 R5 produced confirmed head, else **CLOSED** "no real head"
- [ ] Row 5: Portfolio write-ups — **OPEN** (figures exist)
- [ ] Row 6: Pages deploy — **OPEN** if paper compiles, else **CLOSED** "no TeX"
- [ ] Row 7: Capstone teaching artifact — **OPEN** (capstone training runs)
- [ ] Row 8: Gate-debt closure — **OPEN** (ledger exists)

### 3. Toolchain Verification (Pinned in S0, Never Discovered at S7)
```bash
# LaTeX
which pdflatex || echo "MISSING: will use graceful fallback"
# W&B
wandb login --verify || echo "NEEDS: wandb login"
# HF CLI
hf auth status || echo "NEEDS: hf auth login"
# Pages workflow
test -f .github/workflows/pages.yml || echo "MISSING: will create in Session 5"
```

### 4. Write Ex-T31 Execution Memo
- Document: MP-74 verdict consumed, ADR-0027 rows adjudicated, conditions cited
- Stamp: date, session, decision rule

## Exit Criteria
- ADR-0027 eight rows stamped PENDING/GATED/CLOSED-with-reason
- Ex-T31 memo committed
- Toolchain status recorded

## Links
- [[00_meta/78_micro-phase-78-execution-roadmap]]
- [[docs/adr/0027-continuum-ledger-21]]
- [[07_capstone/execution-log]]

## Open questions
- #question: MP-74 GPU run verdict timing — will results be available by Session 0?
- #question: W&B entity and HF username for deployment configs
- #question: LaTeX toolchain availability for paper compile