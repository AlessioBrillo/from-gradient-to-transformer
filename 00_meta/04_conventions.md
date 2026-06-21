---
tags: [meta, conventions]
---

# Conventions

Simple rules, always applied. Consistency is what makes the vault navigable 6 months from now.

## File naming
- Phase folders: `NN_name` (numeric prefix → guaranteed order).
- Atomic notes: `kebab-case`, title = concept (e.g., `self-attention.md`, `bias-variance.md`).
- Exercises: `ex-NN-description.md`. Proofs: `proof-concept.md`.
- Python modules: `snake_case.py`, one class or logical group per file.

## Tags (few and useful)
- `#phase/1` … `#phase/7` — phase membership.
- `#type/lesson` `#type/exercise` `#type/proof` `#type/moc`.
- `#state/review` `#state/consolidated`.
- `#question` — for what you haven't understood yet (then search all open `#question`).

## Links (the heart of Obsidian)
- Every note links **at least 2** other notes. No orphan notes.
- Use `[[wikilink]]`. For key concepts, create the note *before* writing it (red link): it is a shopping list of what you are missing.
- Each phase has a `_MOC.md` that acts as an index and collects internal links.

## Anatomy of a lesson note
1. **What it is** in one sentence.
2. **Why it exists / what problem it solves.**
3. **How it works** (with an example or diagram).
4. **Links.**
5. **Open questions.**

> If you cannot write point 2 ("why it exists"), you haven't yet understood the concept.

## Anatomy of a research note
Every research note (experiment, derivation, result) should make a **claim** supported by evidence:
1. **Claim** — one sentence hypothesis or finding.
2. **Method** — how it was tested.
3. **Evidence** — numbers, figures, code output.
4. **Limitations** — what the evidence does *not* prove.
5. **Links** — to the code, to related concepts, to primary literature.

## Study → note workflow
1. Study the resource. 2. Close everything. 3. Rewrite the concept **in your own words** (this is the moment you learn). 4. Do the exercise. 5. Do the proof. 6. Check the skill.

## Git commit
One commit per study session, descriptive message:
`phase3: note on backprop + micrograd exercise solved`. The git history becomes the objective proof of your journey — valuable for the portfolio.

## Python code conventions
- Type hints everywhere (enforced by `mypy --strict` where practical).
- All experiments accept a `--seed` argument and call `set_seed()` at entry.
- Every experiment script reports mean ± std over ≥3 seeds.
- Import from `src.*` package paths, not relative imports.
