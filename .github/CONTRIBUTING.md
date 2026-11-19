# Contributing

This is a personal learning vault and research codebase, and contributions are
welcome. Until 2026-11-16 this file said pull requests would be closed without
review; that policy is withdrawn.

## What helps most

- **Independent reproductions.** Run an experiment on your hardware and report
  what you got, whether or not it matches. A reproduction that disagrees is the
  most valuable contribution this repository can receive.
- **Errata.** A wrong derivation in a note, a number that overstates its
  manifest, a broken link, a command that does not run.
- **Bug fixes** in `src/`, `scripts/` or `tests/`.

New experiments and new curriculum content are better discussed in an issue
first: the repository follows one person's study path, and not everything fits.

## How to report a number that does not reproduce

Open an issue with:

1. the command you ran and the commit you ran it on;
2. the manifest it wrote (`results/*.json`), attached or pasted;
3. your hardware and library versions (they are in the manifest).

A confirmed discrepancy is recorded as a dated entry in the Honesty Ledger
(`portfolio/RESULTS.md`), with credit.

## Pull requests

- Branch from `dev` and open the pull request against `dev`. `main` only
  receives merges from `dev`.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/):
  `type(scope): message`, with the types and scopes listed in
  `commitlint.config.mjs`.
- The merge gate is the Woodpecker pipeline in `.woodpecker/ci.yml`. The same
  commands run locally:

  ```bash
  uv sync --all-extras
  make lint vault-check typecheck-new typecheck test-cov check-refs docs-audit
  make verify-claims
  ```

- **No public number without a manifest.** If your change adds or alters a
  number in a document, the section must carry a
  `<!-- manifest: results/<name>.json -->` tag that resolves to a committed
  manifest. `make verify-claims` and `make docs-audit` enforce this.
- No test may write into `results/`; use `tmp_path` or `--manifest-path`.
- A note must link to at least two other notes (`make vault-check`).
- Do not edit `archive/process/`: it is frozen history.

## Questions and ideas

Use Issues for bugs and errata, and Discussions for questions, ideas and
resources. See also the [Code of Conduct](CODE_OF_CONDUCT.md).
