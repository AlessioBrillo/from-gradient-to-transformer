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

So this script is a ratchet with several parts:

1. **Stale claims** — a list of statements that are known to be false,
   each with the measurement that made it false. If one of them comes
   back, the audit fails. This is not a style rule: every entry is a
   sentence this repository published and then retracted, and the whole
   point of the Honesty Ledger is that the retraction stays visible.
2. **Required manifests** — every current-facing document that states a
   rung's status has to carry the tag of the manifest that status comes
   from. A document that cannot name its evidence cannot be checked by
   anybody, and that is how the drift of 2026-10-20 happened.
3. **Numbers against manifests** (added 2026-11-11) — the numbers in the
   tables of a current-facing document are checked against the values in
   the manifests that document cites. A tag proves that *some* evidence
   exists; it does not prove that the number next to it is that evidence.
   This is the check that would have caught the content-task table of
   2026-11-11, whose "NOT MEASURED" cells contradicted the addendum
   manifest that measured them.
4. **The results index** (added 2026-11-11) — every tracked manifest must
   have a row in ``results/INDEX.md`` with its citation status, and every
   row must point at a tracked manifest. The index was introduced on
   2026-11-10 and nothing ever checked it: a manifest that landed without
   a row was invisible.
5. **Referenced manifests exist** — a document that names a
   ``results/<file>.json`` must name one that exists, whether it is
   written as a tag or in prose. This is what catches a paragraph that
   describes the cells of a sweep that has never run.

Run: ``make docs-audit`` (also a CI step, and part of ``make ci-check``).
"""

from __future__ import annotations

import json
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
        "ten audits have caught real bugs (they include a negative verdict "
        "its own metric had manufactured, the content-task experiment that "
        "could not produce a verdict until its instrument was fixed, and the "
        "2026-11-04 finalization audit)",
        "2026-11-04",
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
    (
        "portfolio/paper/main.tex",
        "Sparsity sweep (single seed)",
        "the sweep is three seeds (results/exp3_superposition_sweep.json)",
        "2026-11-12",
    ),
    (
        "portfolio/paper/main.tex",
        "The drop to 16/20 at sparsity 0.001",
        "the extreme-sparsity limit is a three-seed mean +- spread "
        "(17.00 +- 0.82 of 20 at sparsity 0.001, "
        "results/exp3_superposition_sweep.json)",
        "2026-11-12",
    ),
    (
        "portfolio/projects/rung-3-superposition/index.md",
        "Capacity limit at extreme sparsity (0.001): 16/20 features "
        "represented",
        "the extreme-sparsity limit is a three-seed mean +- spread "
        "(17.00 +- 0.82 of 20 at sparsity 0.001, "
        "results/exp3_superposition_sweep.json)",
        "2026-11-12",
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


# ---------------------------------------------------------------------------
# 3. Numbers against manifests
# ---------------------------------------------------------------------------
#: The documents whose tables carry public numbers. The vault's own notes
#: are excluded on purpose: they are the working notes, and the record the
#: reader is shown is the current-facing set.
CURRENT_FACING = (
    "README.md",
    "CONTEXT.md",
    "07_capstone/writeup.md",
    "07_capstone/README.md",
    "07_capstone/checklist.md",
    "portfolio/README.md",
    "portfolio/RESULTS.md",
    "portfolio/model-card.md",
    "portfolio/paper/main.tex",
    "portfolio/projects/rung-1-induction-heads/index.md",
    "portfolio/projects/rung-2-grokking/index.md",
    "portfolio/projects/rung-3-superposition/index.md",
    "portfolio/projects/rung-4-circuit-patching/index.md",
    "portfolio/projects/rung-5-sae/index.md",
)

#: Numbers that are structural, not measurements: dates, seed counts, and
#: ranges of counts. They are never checked against a manifest.
NUMBER_ALLOWLIST = (
    re.compile(r"^\d{4}-\d{2}-\d{2}$"),  # a date
    re.compile(r"^\d+$"),  # a count (3 seeds, 2 layers, 8 heads)
    re.compile(r"^\d+/\d+$"),  # a ratio of counts (3/3)
    re.compile(r"^\d+–\d+$"),  # a range of counts (2–3)
    re.compile(r"^\d+-\d+$"),
)

#: The pre-registered thresholds and the structural constants of the
#: experiments: they are *definitions*, not measurements, so no manifest
#: carries them.
NUMBER_ALLOW_VALUES = frozenset(
    {
        0.10,  # ablation drop / margin thresholds
        0.20,  # path-patching and margin thresholds
        0.30,  # the content-mass screen
        0.40,  # the K-composition bar
        0.50,  # the non-modal accuracy threshold
        0.60,  # the copy-accuracy threshold
        0.80,  # the "top 80% of the content mass" group definition
        0.90,  # the k_energy_90 criterion
        0.99,  # the generalization gate
    }
)

#: A number in a table cell: 0.9999, 53.5%, 15.5–16.5%, 0.945.
#: The optional second group is the upper end of a range, the third the
#: percent sign (which applies to both ends of a range). The negative
#: lookahead keeps a version string ("torch 2.11.0+cu128") from being read
#: as the number 2.11.
CELL_NUMBER_RE = re.compile(
    r"(\d+(?:\.\d+)?)(?![.\d])\s*(?:[–-]\s*(\d+(?:\.\d+)?))?\s*(%)?"
)

#: Unit divisors a document may use on a manifest value: seconds to hours,
#: seconds to minutes, milliseconds to seconds, and the percent sign.
UNIT_DIVISORS = (3600.0, 60.0, 1000.0, 100.0)

#: A row that says so is exempt: some numbers in the record are historical
#: (a superseded measurement that no manifest was ever written for) and
#: the row has to say that out loud for the reader. The exemption is
#: counted and printed, never silent.
NO_MANIFEST_MARKER = "no tracked manifest"


def _manifest_values(path: Path) -> tuple[set[float], set[float]]:
    """The numbers a manifest carries: its raw values, and its aggregate stats.

    Returns ``(values, stats)``: the first is every per-seed value (used
    for the "this seed's number" reading), the second is every mean/std of
    every aggregated key (used for the "mean ± std" reading).
    """
    values: set[float] = set()
    stats: set[float] = set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return values, stats
    for row in data.get("per_seed_metrics", []) or []:
        for value in row.values():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                values.add(float(value))
    for entry in (data.get("aggregate") or {}).values():
        if not isinstance(entry, dict):
            continue
        for key in ("mean", "std", "min", "max"):
            value = entry.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                stats.add(float(value))
    return values, stats


def _matches(candidate: float, decimals: int, pool: set[float]) -> bool:
    """Is ``candidate`` one of the manifest's numbers?

    Two readings, both of which must hold for a document to be faithful:

    * **rounding-faithful** — the document's number is the manifest value
      rounded to the precision the document used. The tolerance is three
      quarters of the last decimal place, so a value a reader would round
      the same way matches.
    * **within tolerance** — the two agree to within 0.5% (never less than
      5e-4), for the documents that quote a rounded value in a sentence.
    """
    tolerance = 0.75 * (10.0**-decimals)
    for value in pool:
        if abs(candidate - value) <= tolerance:
            return True
        if round(value, decimals) == round(candidate, decimals):
            return True
    return False


def _derivable(candidate: float, decimals: int, pool: set[float], table: set[float]) -> bool:
    """Is ``candidate`` a simple quotient of a manifest value and a number
    the table itself carries?

    Documents legitimately publish derived numbers: "96.60 / 512 (18.9%)"
    is the manifest's L0 count divided by the dictionary size, and "5 / 29"
    is a per-seed frequency count divided by the number of frequencies. Both
    are backed by the manifest even though neither number is *in* it.
    """
    tolerance = 0.75 * (10.0**-decimals)
    denominators = {d for d in table if abs(d) > 1e-9}
    denominators.update(UNIT_DIVISORS)
    for numerator in pool:
        for denominator in denominators:
            quotient = numerator / denominator
            if abs(candidate - quotient) <= tolerance:
                return True
    return False


def _numbers_in_cell(cell: str) -> list[tuple[float, int, bool]]:
    """The numbers of one table cell: (value, decimals, is_percent)."""
    out: list[tuple[float, int, bool]] = []
    for match in CELL_NUMBER_RE.finditer(cell):
        raw = match.group(1)
        try:
            value = float(raw)
        except ValueError:  # pragma: no cover - the regex only matches numbers
            continue
        decimals = len(raw.split(".")[1]) if "." in raw else 0
        is_percent = match.group(3) == "%"
        if is_percent:
            value = value / 100.0
            decimals += 2
        out.append((value, decimals, is_percent))
        upper = match.group(2)
        if upper:
            try:
                upper_value = float(upper)
            except ValueError:  # pragma: no cover - the regex only matches numbers
                continue
            upper_decimals = len(upper.split(".")[1]) if "." in upper else 0
            if is_percent:
                upper_value = upper_value / 100.0
                upper_decimals += 2
            out.append((upper_value, upper_decimals, is_percent))
    return out


def _split_row(row: str) -> list[str]:
    """The cells of one markdown table row.

    A pipe escaped as ``\\|`` (how a wikilink with an alias is written
    inside a table) is **not** a cell separator: splitting on it blindly
    produced an empty cell, which then looked like a table separator and
    made the audit skip the whole header row — the row that carries the
    "no tracked manifest" marker.
    """
    placeholder = "\x00ESCAPED_PIPE\x00"
    cleaned = row.replace("\\|", placeholder)
    cells = [c.strip().replace(placeholder, "|") for c in cleaned.strip("|").split("|")]
    return cells


def _is_separator(cells: list[str]) -> bool:
    """Is this the ``|---|---|`` line between a header and its body?"""
    return bool(cells) and all(set(c) <= set("-: ") for c in cells)


def check_numbers_against_manifests() -> list[str]:
    """Every number in a current-facing table must be in the manifest it cites.

    A tag says "this section has evidence"; this check says "and the
    numbers next to it are that evidence". Without it, the content-task
    table of 2026-11-11 could claim "NOT MEASURED" for a criterion the
    addendum manifest measured (and measured as a pass) while still
    carrying the right tag.
    """
    problems: list[str] = []
    declared = 0
    for rel in CURRENT_FACING:
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        # Section by section: a table inherits the manifests of the section
        # it lives in.
        sections = re.split(r"(?=^##\s)", text, flags=re.MULTILINE)
        for section in sections:
            tags = _tags(section)
            if not tags:
                continue
            pools: list[set[float]] = []
            for tag in tags:
                manifest = REPO_ROOT / tag
                if not manifest.exists():
                    continue
                values, stats = _manifest_values(manifest)
                pools.append(values | stats)
            if not pools:
                continue
            # Table by table: the numbers of a table are the legitimate
            # denominators of its derived numbers (a count divided by a
            # dictionary size, a frequency count divided by the number of
            # frequencies, a wall clock in hours).
            table_rows: list[str] = []
            for line in section.splitlines():
                stripped = line.strip()
                if not stripped.startswith("|") or not stripped.endswith("|"):
                    if table_rows:
                        problems.extend(_check_table(rel, table_rows, pools, tags))
                        if any(NO_MANIFEST_MARKER in row for row in table_rows):
                            declared += 1
                        table_rows = []
                    continue
                cells = _split_row(stripped)
                if _is_separator(cells):
                    continue  # a table separator
                table_rows.append(stripped)
            if table_rows:
                problems.extend(_check_table(rel, table_rows, pools, tags))
                if any(NO_MANIFEST_MARKER in row for row in table_rows):
                    declared += 1
    if declared:
        print(
            f"docs-audit: {declared} table row(s) declare "
            f"'{NO_MANIFEST_MARKER}' and are exempt from the number check."
        )
    return problems


# ---------------------------------------------------------------------------
# 4. The results index
# ---------------------------------------------------------------------------
def _check_table(
    rel: str,
    rows: list[str],
    pools: list[set[float]],
    tags: list[str],
) -> list[str]:
    """Check every number of one table against the manifests of its section."""
    problems: list[str] = []
    if any(NO_MANIFEST_MARKER in row for row in rows):
        # An explicitly declared historical table: not backed by a
        # manifest, and it says so. The count is printed by the audit, so
        # these cannot accumulate unnoticed.
        return problems
    table_numbers: set[float] = set()
    for row in rows:
        for cell in _split_row(row):
            for value, _decimals, is_percent in _numbers_in_cell(cell):
                table_numbers.add(value if not is_percent else value * 100.0)
    for row in rows:
        for cell in _split_row(row):
            if not cell or cell.startswith("<!--"):
                continue
            for value, decimals, _is_percent in _numbers_in_cell(cell):
                raw = f"{value:g}"
                if any(pattern.match(raw) for pattern in NUMBER_ALLOWLIST):
                    continue
                if round(value, 6) in NUMBER_ALLOW_VALUES:
                    continue
                if any(_matches(value, decimals, pool) for pool in pools):
                    continue
                if any(_derivable(value, decimals, pool, table_numbers) for pool in pools):
                    continue
                problems.append(
                    f"{rel}: the number {raw} in a table is not in any of "
                    f"the manifests this section cites ({', '.join(tags)})"
                )
    return problems


def check_results_index() -> list[str]:
    """Every tracked manifest has a row in ``results/INDEX.md``, and back.

    The index is the reverse of the citations: it says which tracked
    manifests are public evidence and which are kept as history. Nothing
    checked it between 2026-11-10 (when it was written) and 2026-11-11
    (when `results/exp4_content.json` landed without a row).
    """
    problems: list[str] = []
    index = REPO_ROOT / "results/INDEX.md"
    if not index.exists():
        return ["results/INDEX.md: file not found — the manifest index is missing"]
    text = index.read_text(encoding="utf-8")
    rows = set(re.findall(r"^\|\s*`results/([^`]+\.json)`", text, re.M))

    tracked = subprocess.run(
        ["git", "ls-files", "results/*.json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.split()
    tracked_names = {Path(name).name for name in tracked if name.endswith(".json")}

    for name in sorted(tracked_names - rows):
        problems.append(
            f"results/INDEX.md: the tracked manifest results/{name} has no row "
            "(every tracked manifest must be listed with its citation status)"
        )
    for name in sorted(rows - tracked_names):
        problems.append(
            f"results/INDEX.md: the row for results/{name} points at a manifest "
            "that is not tracked by git"
        )
    return problems


# ---------------------------------------------------------------------------
# 5. Referenced manifests exist
# ---------------------------------------------------------------------------
#: A ``results/<file>.json`` mentioned in prose (not only as a tag).
PROSE_MANIFEST_RE = re.compile(r"results/([A-Za-z0-9_\-]+\.json)")


def _is_gitignored(rel_path: str) -> bool:
    """Is this path excluded from the repository by .gitignore?

    Some ``results/*.json`` files are **deliberately** not tracked: they are
    derived artifacts (the content-task verdict) or scratch from a probe
    run. A document may name them — `results/INDEX.md` says the verdict is
    "gitignored, derived, regenerated by `make content-verdict`" — and that
    naming is not a claim that a manifest exists.

    The distinction that matters for the audit is: a name that *should* be a
    tracked manifest but is not on disk is an error (the 2026-11-11 paper
    paragraph describing a sweep that never ran); a name that is gitignored
    is scratch by design, and on a clean clone it is simply absent.
    """
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", rel_path],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    # 0 = ignored, 1 = not ignored, 128 = not a git repo
    return result.returncode == 0


def check_referenced_manifests_exist() -> list[str]:
    """A document may only name a manifest that exists.

    The tag contract already covers tagged citations; this covers the prose
    ("the sweep's manifests", "results/phase_diagram_p113_nanda_wd10.json"),
    which is where the 2026-11-11 audit found a paper paragraph describing
    the cells of a sweep that has never run.

    A name that is gitignored is exempt: derived artifacts and probe scratch
    are absent from a clean clone by design, and naming them is not a claim
    that they are evidence.
    """
    problems: list[str] = []
    for rel in CURRENT_FACING:
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for name in sorted(set(PROSE_MANIFEST_RE.findall(text))):
            manifest = REPO_ROOT / "results" / name
            if not manifest.exists() and not _is_gitignored(f"results/{name}"):
                problems.append(
                    f"{rel}: names results/{name}, which does not exist — a "
                    "document may only cite a manifest that is on disk"
                )
    return problems



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


# The ledger's opening sentence is the count of record. The other
# current-facing documents must not disagree with it: on 2026-11-04 the
# ledger said "Ten audits" while README, writeup and checklist still said
# "nine", and no checker noticed because each number was untagged prose.
AUDIT_COUNT_DOCS = (
    "README.md",
    "07_capstone/writeup.md",
    "07_capstone/checklist.md",
)
AUDIT_HEADER_RE = re.compile(
    r"\b([A-Za-z]+)\s+audits\s+have\s+now\s+caught\b", re.IGNORECASE
)
AUDIT_ANY_RE = re.compile(r"\b([A-Za-z]+)\s+audits\b", re.IGNORECASE)
NUMBER_WORDS = {
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
}


def check_audit_count() -> list[str]:
    """The public documents agree on how many audits the ledger records."""
    problems: list[str] = []
    ledger = REPO_ROOT / "portfolio/RESULTS.md"
    if not ledger.exists():
        return ["portfolio/RESULTS.md: file not found - cannot read the audit count"]
    text = ledger.read_text(encoding="utf-8")
    match = AUDIT_HEADER_RE.search(text)
    if match is None:
        return [
            "portfolio/RESULTS.md: no '<N> audits have now caught' header "
            "- the audit count has no single source of truth"
        ]
    expected = match.group(1).lower()
    if expected not in NUMBER_WORDS:
        problems.append(
            f"portfolio/RESULTS.md: '{match.group(1)} audits' is not a number word"
        )
    for rel in AUDIT_COUNT_DOCS:
        path = REPO_ROOT / rel
        if not path.exists():
            problems.append(f"{rel}: file not found - the audit count cannot be checked")
            continue
        body = path.read_text(encoding="utf-8")
        found = {m.group(1).lower() for m in AUDIT_ANY_RE.finditer(body)}
        wrong = sorted(word for word in found if word != expected)
        if wrong:
            problems.append(
                f"{rel}: says '{wrong[0]} audits', but portfolio/RESULTS.md "
                f"says '{expected} audits'"
            )
        elif expected not in found:
            problems.append(
                f"{rel}: does not name the audit count ('{expected} audits')"
            )
    return problems


def main() -> int:
    problems = (
        check_stale_claims()
        + check_required_manifests()
        + check_audit_count()
        + check_numbers_against_manifests()
        + check_results_index()
        + check_referenced_manifests_exist()
    )
    if problems:
        print(f"docs-audit: {len(problems)} problem(s) found:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(
        f"docs-audit: OK ({len(STALE_CLAIMS)} retracted statements stay retracted, "
        f"{len(REQUIRED_MANIFESTS)} current-facing documents name their manifests, "
        "the numbers match the manifests, and every tracked manifest is indexed)."
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
