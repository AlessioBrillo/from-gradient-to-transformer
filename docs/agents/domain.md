# Domain Docs

How agents should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root — single-context domain map for this repo: vocabulary, rung→module map, repo map, and the conventions that bite. Read it first; it is short and it is canonical.
- **`docs/adr/`** — read the ADRs that touch the area you're about to work in.

`CONTEXT.md` exists and is maintained. If it is ever missing, proceed silently rather than blocking on it.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids — **Rung**, **Manifest**, **Ledger**, **Claim**, **Backed**, **Grokking (NO-GROK)**, **k₉₀/k₉₉**, **Superposition** and **Induction head** all have precise meanings here.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap. Raise it; don't silently coin a term.

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_

## Where status lives

Current status lives in `portfolio/RESULTS.md` (the Honesty Ledger) and the `v1.0` GitHub milestone. The ADRs numbered 0001–0030 are historical ledgers and are **closed** — read them as a dated record of what was planned, not as current status. See `docs/adr/0031-closure.md`.
