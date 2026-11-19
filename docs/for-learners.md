# For learners

A path from gradient descent to reading circuits out of a trained transformer.
These are one person's notes, exercises and proofs, published so that you can
follow the same route or take the parts you need.

## How the vault works

Each phase folder has the same shape:

```
NN_name/
├── _MOC.md        the phase's map: start here
├── notes/         one concept per note, derived rather than transcribed
├── exercises/     problems solved and verified, most with runnable Python
├── proofs/        a concept reconstructed from memory, without looking
└── checklist.md   the phase's skills, with the evidence for each
```

The rule the vault sets for itself: a skill counts as learned only when there
is an exercise **and** a proof for it. Use the same rule for yourself. Reading a
note is not the same as being able to rebuild the idea on a blank page.

The notes are plain Markdown and read fine on GitHub. For the linked graph, open
the repository folder as a vault in [Obsidian](https://obsidian.md/); the map is
[`00_meta/00_home.md`](../00_meta/00_home.md).

## The path

| Phase | You need first | You come out able to | Start at |
|---|---|---|---|
| 1 Foundations | School mathematics, basic Python | Derive a gradient and check it numerically; explain cross-entropy from first principles; use SVD | [`01_foundations/_MOC.md`](../01_foundations/_MOC.md) |
| 2 Classical ML | Phase 1 | Implement regression, trees and PCA; diagnose bias and variance | [`02_classical_ml/_MOC.md`](../02_classical_ml/_MOC.md) |
| 3 Deep learning | Phases 1 and 2 | Write reverse-mode autodiff from scratch; explain why weight decay matters for grokking | [`03_deep_learning/_MOC.md`](../03_deep_learning/_MOC.md) |
| 4 Transformers | Phase 3 | Build a decoder-only transformer; read QK and OV circuits; run activation patching | [`04_nlp_and_transformers/_MOC.md`](../04_nlp_and_transformers/_MOC.md) |
| 5 Instrumentation | Phase 4 | Hook a model, cache activations, make inference deterministic | [`05_llm_engineering/_MOC.md`](../05_llm_engineering/_MOC.md) |
| 6 Reproducible research | Any of the above | Make a result re-runnable and a claim checkable | [`06_production_ai/_MOC.md`](../06_production_ai/_MOC.md) |
| 7 Capstone | Phases 4 to 6 | Train a model and reverse-engineer what it learned | [`07_capstone/_MOC.md`](../07_capstone/_MOC.md) |

If you already know deep learning and want interpretability, start at Phase 4.
Phase 6 stands on its own and is useful for any machine-learning project.

The full list of topics, resources and gate proofs per phase is the
[roadmap](../00_meta/01_roadmap.md); the external material the notes draw on is
in [books and courses](../references/books_and_courses.md).

## Code you can run

The from-scratch implementations the exercises refer to live in `src/`, each
with tests in `tests/`:

| Topic | Code |
|---|---|
| Reverse-mode autodiff | [`src/training/micrograd.py`](../src/training/micrograd.py) |
| Linear and logistic regression | [`src/models/linear_model.py`](../src/models/linear_model.py) |
| Decision trees | [`src/models/tree_model.py`](../src/models/tree_model.py) |
| PCA | [`src/models/pca.py`](../src/models/pca.py) |
| BPE tokenizer | [`src/models/bpe_tokenizer.py`](../src/models/bpe_tokenizer.py) |
| Decoder-only transformer | [`src/models/decoder_only_transformer.py`](../src/models/decoder_only_transformer.py) |
| The experiments | [`src/experiments/`](../src/experiments/) |

```bash
uv sync
uv run pytest tests/test_micrograd.py       # one topic's tests
make reproduce-quick                        # every experiment, small, on CPU
```

## Read this before trusting a note

- **Notes are dated.** Some record a result that was later retracted. Where that
  happened the note says so at the top. The authority on what is currently true
  is the [Honesty Ledger](../portfolio/RESULTS.md).
- **The curriculum is uneven.** Phase 1 is the densest; Phase 3 is thin, and a
  2026-11-16 review found skills checked on a note alone, against the vault's
  own rule. Closing those gaps is open work.
- **These are a learner's notes**, not a textbook. If you find an error, an
  issue or a pull request is welcome: see
  [CONTRIBUTING](../.github/CONTRIBUTING.md).

## Use it for your own journey

Fork it. The templates in [`templates/`](../templates/) and the script
`scripts/new_note.sh` create notes, exercises and proofs in the same format, and
`make vault-check` enforces that every note links to at least two others.
