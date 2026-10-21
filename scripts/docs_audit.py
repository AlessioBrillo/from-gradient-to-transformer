#!/usr/bin/env python3
"""The record audit: the current-facing documents must say what the manifests say.

Why this script exists
----------------------
`make verify-claims` checks that the manifests exist, that they were
recorded against a clean tree, and that every ``<!-- manifest: ... -->``
tag resolves. It does **not** check the prose around the tags, and that is
where this repository's record drifted.

On 2026-10-20 the paper's limitations still read "SAE on real activations:
53% L0 indicates dense reconstruction" and "Path patching unvalidated
against a real head: implementation is unit-tested only", while the
manifests said 3.0% and 0.8215. The writeup said "no induction head has
ever been confirmed". The skill tree said grokking was "not yet
reproduced". `make verify-claims` was green the whole time, because every
*number* in those sentences was untagged — and an untagged number is
invisible to a checker that only reads tags.

So this script is a ratchet with two parts:

1. **Stale claims** — a list of statements that are known to be false,
   each with the measurement that made it false. If one of them comes
   back, the audit fails. This is not a style rule: every entry is a
   sentence this repository published and then retracted, and the whole
   point of the Honesty Ledger is that the retraction stays visible.
2. **Required manifests** — every current-facing document that states a
   rung's status has to carry the tag of the manifest that status comes
   from. A document that cannot name its evidence cannot be checked by
   anybody, and that is how the drift of 2026-10-20 happened.

Run: ``make docs-audit`` (also a CI step, and part of ``make ci-check``).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MANIFEST_TAG_RE = re.compile(
    r"<!--\s*manifest:\s*(\S+)\s*-->|^[ \t]*%[ \t]*manifest:[ \t]*(\S+)[ \t]*$",
    re.MULTILINE,
)

# ---------------------------------------------------------------------------
# The manifests the current-facing documents have to name
# ---------------------------------------------------------------------------
RUNG_MANIFESTS = {
    "rung1": "results/induction_standard.json",
    "rung2": "results/grokking_nanda_p113.json",
    "rung3": "results/exp3_superposition.json",
    "rung4": "results/exp4_standard.json",
    "rung5": "results/exp5_real_activations.json",
}

REQUIRED_MANIFESTS: dict[str, list[str]] = {
    "README.md": list(RUNG_MANIFESTS.values()),
    "CONTEXT.md": list(RUNG_MANIFESTS.values()),
    "07_capstone/writeup.md": list(RUNG_MANIFESTS.values()),
    "07_capstone/README.md": [RUNG_MANIFESTS["rung2"], RUNG_MANIFESTS["rung3"]],
    "portfolio/README.md": [RUNG_MANIFESTS["rung2"]],
    "portfolio/model-card.md": [
        RUNG_MANIFESTS["rung2"],
        RUNG_MANIFESTS["rung4"],
        RUNG_MANIFESTS["rung5"],
    ],
    "portfolio/paper/main.tex": list(RUNG_MANIFESTS.values()),
    "00_meta/02_skill-tree.md": [RUNG_MANIFESTS["rung2"], RUNG_MANIFESTS["rung3"]],
}

# ---------------------------------------------------------------------------
# Statements that are known to be false, and why
# ---------------------------------------------------------------------------
# (file, the sentence, what replaced it, the date of the measurement)
STALE_CLAIMS: list[tuple[str, str, str, str]] = [
    (
        "07_capstone/writeup.md",
        "path patching unit-tested only",
        "the end-to-end path-patching result on Rung 1's own checkpoint "
        "(effect 0.8215, results/exp4_standard.json)",
        "2026-10-20",
    ),
    (
        "07_capstone/writeup.md",
        "No induction head has ever been confirmed here",
        "a prefix-copying head was confirmed at standard scale on "
        "2026-10-20 (results/induction_standard.json); the honest wording "
        "is 'no *content-based* induction head'",
        "2026-10-20",
    ),
    (
        "07_capstone/writeup.md",
        "real activations are dense",
        "the real-activation SAE is sparse (L0 3.0%, FVE 99.998%) — its "
        "dictionary is 8x oversized and 78% of its features are dead, "
        "which is the open question, not density",
        "2026-10-20",
    ),
    (
        "07_capstone/writeup.md",
        "Six audits have caught real bugs",
        "seven audits have caught real bugs (the seventh reversed a negative "
        "verdict its own metric had manufactured)",
        "2026-10-20",
    ),
    (
        "CONTEXT.md",
        "path patching unit-tested only",
        "the end-to-end path-patching result on Rung 1's own checkpoint "
        "(effect 0.8215, results/exp4_standard.json)",
        "2026-10-20",
    ),
    (
        "CONTEXT.md",
        "real activations dense (53% active)",
        "the real-activation SAE is sparse (L0 3.0%, FVE 99.998%)",
        "2026-10-20",
    ),
    (
        "README.md",
        "reconstruction is good but dense (53% of features active)",
        "the real-activation SAE is sparse (L0 3.0%); its dictionary is 8x "
        "oversized, which is the open question",
        "2026-10-20",
    ),
    (
        "portfolio/paper/main.tex",
        "Path patching unvalidated against a real head",
        "the end-to-end path-patching result on Rung 1's own checkpoint "
        "(effect 0.8215, results/exp4_standard.json)",
        "2026-10-20",
    ),
    (
        "portfolio/paper/main.tex",
        "No induction heads at standard scale",
        "a prefix-copying head forms at standard scale; the *content-based* "
        "claim is the open question (results/induction_standard.json)",
        "2026-10-20",
    ),
    (
        "portfolio/paper/main.tex",
        "53\\% L0 indicates dense",
        "the real-activation SAE is sparse (L0 3.0%); the dictionary is 8x "
        "oversized, which is the open question",
        "2026-10-20",
    ),
    (
        "portfolio/paper/main.tex",
        "The strongest verified result remains Rung 3",
        "Rung 2 is the flagship and it is reproduced (val accuracy 0.9999, "
        "sparse circuit, 3/3 seeds, results/grokking_nanda_p113.json)",
        "2026-10-20",
    ),
    (
        "portfolio/paper/main.tex",
        "metric-suspect",
        "the P=59 control was re-measured with the energy metric on "
        "2026-10-19: 2 of 3 seeds sparse, MIXED "
        "(results/grokking_p59_repo_energy.json)",
        "2026-10-20",
    ),
    (
        "portfolio/paper/main.tex",
        "3 seeds planned, 1 completed",
        "the capstone ran 3 seeds x 20k steps (results/capstone_20k.json)",
        "2026-10-20",
    ),
    (
        "00_meta/02_skill-tree.md",
        "not yet reproduced",
        "Rung 2 is reproduced (val accuracy 0.9999, sparse circuit, 3/3 "
        "seeds, results/grokking_nanda_p113.json)",
        "2026-10-20",
    ),
    (
        "00_meta/02_skill-tree.md",
        "path patching is still validated only by unit tests",
        "the end-to-end path-patching result on Rung 1's own checkpoint "
        "(effect 0.8215, results/exp4_standard.json)",
        "2026-10-20",
    ),
    (
        "00_meta/02_skill-tree.md",
        "no prose yet",
        "the mini-paper is written from the manifests "
        "(portfolio/paper/main.tex)",
        "2026-10-20",
    ),
    (
        "07_capstone/README.md",
        "Rung 2 still pending",
        "Rung 2 is reproduced (results/grokking_nanda_p113.json)",
        "2026-10-20",
    ),
    (
        "07_capstone/README.md",
        "Every manifest committed in this repository reports",
        "the GPU manifests (results/grokking_nanda_p113.json, "
        "results/induction_standard.json, results/capstone_20k.json) report "
        "device: cuda",
        "2026-10-20",
    ),
    (
        "07_capstone/checklist.md",
        "GPU run in flight",
        "issue #169 is closed: the run happened on 2026-10-20 "
        "(results/induction_standard.json)",
        "2026-10-20",
    ),
    (
        "portfolio/README.md",
        "needs a confirmed induction-head checkpoint before real-activation "
        "SAE is meaningful (issue #169)",
        "issue #169 is closed and the checkpoint exists; the dashboard is "
        "descoped for want of a browsable artifact, not for want of a head",
        "2026-10-20",
    ),
]


def _tracked(path: Path) -> bool:
    """Is the file tracked by git? An untracked file is not evidence."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(path)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        return out.returncode == 0
    except OSError:  # pragma: no cover - git is a hard dependency of the repo
        return False


def _tags(text: str) -> list[str]:
    return [a or b for a, b in MANIFEST_TAG_RE.findall(text)]


def check_stale_claims() -> list[str]:
    """Every known-false statement must stay gone."""
    problems: list[str] = []
    for rel, sentence, replacement, when in STALE_CLAIMS:
        path = REPO_ROOT / rel
        if not path.exists():
            problems.append(f"{rel}: file not found — the audit list is stale")
            continue
        text = path.read_text(encoding="utf-8")
        if sentence in text:
            problems.append(
                f"{rel}: still says '{sentence}' — retracted {when} by "
                f"{replacement}"
            )
    return problems


def check_required_manifests() -> list[str]:
    """Every current-facing document has to name the manifest behind its status."""
    problems: list[str] = []
    for rel, required in REQUIRED_MANIFESTS.items():
        path = REPO_ROOT / rel
        if not path.exists():
            problems.append(f"{rel}: file not found — the audit list is stale")
            continue
        text = path.read_text(encoding="utf-8")
        cited = set(_tags(text))
        for manifest in required:
            if manifest not in cited:
                problems.append(
                    f"{rel}: does not cite {manifest} — a status without its "
                    "manifest cannot be checked by anybody"
                )
                continue
            manifest_path = REPO_ROOT / manifest
            if not manifest_path.exists():
                problems.append(f"{rel}: cites {manifest}, which does not exist")
            elif not _tracked(manifest_path):
                problems.append(
                    f"{rel}: cites {manifest}, which is not tracked by git"
                )
    return problems


def main() -> int:
    problems = check_stale_claims() + check_required_manifests()
    if problems:
        print(f"docs-audit: {len(problems)} problem(s) found:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(
        f"docs-audit: OK ({len(STALE_CLAIMS)} retracted statements stay retracted, "
        f"{len(REQUIRED_MANIFESTS)} current-facing documents name their manifests)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
