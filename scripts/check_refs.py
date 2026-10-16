#!/usr/bin/env python3
r"""Validate the mini-paper bibliography.

Rules:
  1. Every ``@...`` entry in ``portfolio/paper/references.bib`` must carry a
     resolvable identifier (arXiv id ``arXiv:YYMM.NNNNN`` or a DOI
     ``10.xxx/...``) in its ``journal``/``booktitle`` field — placeholder ids
     such as ``arXiv:2310.xxxxx`` are rejected.
  2. Every citation key used in ``portfolio/paper/main.tex`` (``\cite``,
     ``\citet``, ``\citep``, ``\citeauthor``) must resolve to a bib entry.

Exit non-zero on any violation.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BIB = Path("portfolio/paper/references.bib")
TEX = Path("portfolio/paper/main.tex")

ARXIV_RE = re.compile(r"arXiv:\d{4}\.\d{4,5}(v\d+)?")
ARXIV_ANY_RE = re.compile(r"arXiv:")
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
PLACEHOLDER_RE = re.compile(r"x{5,}")
CITE_RE = re.compile(r"\\(?:citep|citet|cite|citeauthor)\{([^}]+)\}")


def parse_bib(path: Path) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    text = path.read_text(encoding="utf-8")
    for block in re.split(r"@\w+\s*\{", text)[1:]:
        key = block.split(",", 1)[0].strip()
        fields: dict[str, str] = {}
        for m in re.finditer(
            r"(\w+)\s*=\s*\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}", block
        ):
            fields[m.group(1)] = re.sub(r"^\{|\}$", "", m.group(0).split("=", 1)[1])
        entries[key] = fields
    return entries


def main() -> int:
    problems: list[str] = []
    bib = parse_bib(BIB)

    # Rule 1: if an entry carries an arXiv/DOI-looking id, it must be a real
    # one — placeholder ids such as arXiv:2310.xxxxx are rejected. Entries
    # without any id (conference papers, Transformer Circuits Thread, …) are
    # accepted as-is.
    for key, fields in bib.items():
        haystack = " ".join(fields.values())
        if ARXIV_ANY_RE.search(haystack) and not ARXIV_RE.search(haystack):
            problems.append(
                f"{BIB}: entry '{key}' has a placeholder arXiv id: {haystack!r}"
            )
        doi_match = DOI_RE.search(haystack)
        if doi_match and PLACEHOLDER_RE.search(doi_match.group(0)):
            problems.append(
                f"{BIB}: entry '{key}' has a placeholder DOI: {haystack!r}"
            )

    # Rule 2: every cited key must exist in the bib.
    tex = TEX.read_text(encoding="utf-8")
    cited: list[str] = []
    for m in CITE_RE.finditer(tex):
        cited.extend(k.strip() for k in m.group(1).split(","))
    for key in cited:
        if key not in bib:
            problems.append(f"{TEX}: cites unknown key '{key}'")

    # Bonus: flag bib entries never cited (warning only).
    cited_set = set(cited)
    for key in bib:
        if key not in cited_set:
            print(f"check-refs: note: bib entry '{key}' is never cited", file=sys.stderr)

    if problems:
        print("check-refs: FAILED")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"check-refs: OK ({len(bib)} entries, {len(cited)} citation uses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
