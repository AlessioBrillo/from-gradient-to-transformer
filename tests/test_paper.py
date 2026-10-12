"""Static checks on portfolio/paper/main.tex.

There is no LaTeX toolchain on the author's machine or on most contributors'
(see checklists/gate-debt.md's LaTeX row), so `make paper` degrades to a
message and CI is the only place the paper actually compiles. These checks
run everywhere and catch the failure classes that a compile would, without
needing texlive:

- unbalanced braces / unclosed environments,
- citation keys that do not exist in references.bib,
- escaped-backslash citation commands (`\\citep`), which LaTeX renders as a
  line break followed by the literal text "citep{...}" — i.e. silently no
  citation at all. Seven of those shipped when the reference list was first
  wired up,
- includegraphics targets that do not exist as tracked files.

This is not a substitute for compiling in CI (paper.yml does that); it is the
part that fails fast and locally.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PAPER = REPO_ROOT / "portfolio" / "paper" / "main.tex"
BIB = REPO_ROOT / "portfolio" / "paper" / "references.bib"


@pytest.fixture(scope="module")
def tex() -> str:
    assert PAPER.exists(), f"paper source missing: {PAPER}"
    return PAPER.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def bib_keys() -> set[str]:
    assert BIB.exists(), f"bibliography missing: {BIB}"
    keys = set()
    for m in re.finditer(r"@\w+\{([^,\s]+)\s*,", BIB.read_text(encoding="utf-8")):
        keys.add(m.group(1))
    return keys


def _strip_comments(text: str) -> str:
    """Drop LaTeX line comments so braces inside them do not count.

    A comment starts at an *unescaped* `%`. The naive `line.find("%")` is wrong
    here: `\\%` is a literal percent sign and this paper uses it constantly
    (`99.97\\%`), so that version truncated mid-sentence and deleted the
    closing braces that followed — reporting a phantom imbalance in a file that
    was fine. Count preceding backslashes and only cut on an odd count.
    """
    out = []
    for line in text.split("\n"):
        cut = len(line)
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                cut = i
                break
            i += 1
        out.append(line[:cut])
    return "\n".join(out)


def test_braces_are_balanced(tex: str) -> None:
    body = _strip_comments(tex)
    # Skip verbatim environments entirely: braces there are literal.
    depth = 0
    minimum = 0
    for ch in body:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            minimum = min(minimum, depth)
    assert depth == 0, f"unbalanced braces in main.tex (final depth {depth})"
    assert minimum == 0, f"main.tex closes a brace that was never opened (depth {minimum})"


def test_environments_are_closed(tex: str) -> None:
    begins = re.findall(r"\\begin\{(\w+\*?)\}", tex)
    ends = re.findall(r"\\end\{(\w+\*?)\}", tex)
    assert sorted(begins) == sorted(ends), (
        f"\\begin/\\end mismatch. begins={sorted(begins)} ends={sorted(ends)}"
    )


def test_every_citation_key_exists(tex: str, bib_keys: set[str]) -> None:
    assert bib_keys, "no entries parsed from references.bib"
    used = set()
    for m in re.finditer(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]+)\}", tex):
        for key in m.group(1).split(","):
            if key.strip():
                used.add(key.strip())
    assert used, "main.tex cites nothing — references.bib would be dead weight"
    missing = sorted(used - bib_keys)
    assert not missing, f"cited but not in references.bib: {missing}"


def test_no_bib_entry_is_uncited(tex: str, bib_keys: set[str]) -> None:
    """An entry nobody cites is a dangling promise of provenance."""
    used = set()
    for m in re.finditer(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]+)\}", tex):
        used.update(k.strip() for k in m.group(1).split(",") if k.strip())
    orphans = sorted(bib_keys - used)
    assert not orphans, f"in references.bib but never cited: {orphans}"


def test_no_escaped_backslash_citations(tex: str) -> None:
    """`\\citep{x}` renders as a line break plus the literal text "citep{x}".

    Seven of these shipped when the reference list was first wired up: the
    paper compiled cleanly and cited nothing.
    """
    bad = re.findall(r"\\\\cite[a-zA-Z]*", tex)
    assert not bad, f"escaped-backslash citation commands (silently no citation): {bad}"


def test_citation_commands_are_well_formed(tex: str) -> None:
    r"""A \cite with no argument, or an unclosed brace, is a compile error."""
    for m in re.finditer(r"\\\\cite[a-zA-Z]*\\*?", tex):
        tail = tex[m.end() : m.end() + 60]
        assert tail.lstrip().startswith(("{", "[")), (
            f"citation command with no argument at offset {m.start()}: "
            f"{tex[m.start():m.start() + 40]!r}"
        )


def test_figures_exist(tex: str) -> None:
    r"""\includegraphics targets must resolve relative to the .tex file."""
    targets = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex)
    assert targets, "the paper includes no figures at all"
    for target in targets:
        base = target.rsplit(".", 1)[0]
        for ext in (".png", ".pdf", ".jpg"):
            candidate = (PAPER.parent / (base + ext)).resolve()
            if candidate.exists():
                assert candidate.is_file()
                break
        else:
            pytest.fail(f"includegraphics target does not exist: {target}")


def test_paper_has_no_todo_scaffold(tex: str) -> None:
    body = _strip_comments(tex)
    leftovers = re.findall(r"%\s*TODO|XXX|FIXME", body)
    assert not leftovers, f"unfinished markers in the paper: {leftovers}"
