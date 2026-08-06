#!/usr/bin/env bash
# Clean-clone reproducibility gate (Micro-Phase 10, Step 7).
#
# Proves Phase 6's "reproducible from a clean clone" claim by doing exactly
# what the proof note (06_production_ai/proofs/reproducible-from-clean-clone.md)
# demands, as a script instead of a hand-run transcript: fresh clone -> uv
# sync -> ci-check -> reproduce-quick -> reproduce-multiseed -> verify-claims.
#
# Usage:
#     bash scripts/clean_clone_check.sh [source-repo]
#
# `source-repo` defaults to this repo's origin URL; pass the local repo path
# to run the gate against un-pushed-but-committed work without a network:
#     bash scripts/clean_clone_check.sh ./
#
# Exit 0 only if every step is green. Any manual intervention needed to get
# a step to pass is a failed gate, not a workaround to file away.

set -euo pipefail

SOURCE="${1:-$(git remote get-url origin)}"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

echo "==> Cloning $SOURCE (dev branch) into $WORKDIR/check"
git clone --quiet --branch dev --single-branch "$SOURCE" "$WORKDIR/check"
cd "$WORKDIR/check"

echo "==> uv sync --frozen"
uv sync --frozen --all-extras

echo "==> make ci-check (ruff + blocking mypy + pytest with coverage)"
make ci-check

echo "==> make reproduce-quick (all five rungs, --quick)"
make reproduce-quick

echo "==> make reproduce-multiseed (exp1/exp3/exp4, --seeds 0,1,2)"
make reproduce-multiseed

echo "==> make verify-claims"
make verify-claims

echo
echo "CLEAN-CLONE GATE PASSED: identical commands, identical numbers, no manual steps."