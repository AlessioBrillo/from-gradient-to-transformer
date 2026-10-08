---
adr: 0031
title: Freeze the continuum-ledger process; v1.0 is tracked in GitHub Issues
date: 2026-10-08
status: ACCEPTED
phase: 7
tags: [type/ledger, phase/7]
consumes: [ADR-0030]
---

## Context

ADR-0001 to ADR-0030 are "ledgers": one per micro-phase, each pre-stamping rows that a later
session closes. They were useful while the question was "what do I do next", but they now cost
more than they return:

- the work left is finishing, not choosing, so a new ledger per step adds no decision;
- ADR-0028 to ADR-0030 are all marked OPEN although every row is stamped or closed;
- ADR-0030 promised a phase diagram. Its sweep produced no valid data, and the paper section
  built on it was removed on 2026-10-08 (Honesty Ledger, `portfolio/RESULTS.md`).

## Decision

1. No new micro-phase roadmaps and no new `continuum-ledger` ADRs. ADR-0001 to ADR-0030 stay in
   place as history and are marked CLOSED.
2. Remaining v1.0 work is tracked as GitHub Issues under a `v1.0` milestone
   (see `docs/agents/issue-tracker.md`), each closed by a merged PR with CI green.
3. ADR-0030's phase diagram is replaced by a smaller protocol-ablation, started from a
   Nanda-faithful positive control. It runs only after the positive control groks
   (`notebooks/kaggle_grokking_p113.ipynb`).
4. `checklists/gate-debt.md` and `00_meta/9x_*` are archived as of this date.

## Notes

Numbers 0011 to 0022 and 0026 do not exist: `git log --diff-filter=D -- docs/adr` shows no
deleted ADR. They were reserved or skipped, never written.

ADRs after this one record architecture or research decisions only, when a decision has
alternatives worth keeping.
