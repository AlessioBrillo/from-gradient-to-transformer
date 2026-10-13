"""check_links: the escaped-pipe (table) wikilink must resolve everywhere.

A wikilink with an alias inside a Markdown table must be written
`[[target\\|alias]]` (the pipe is escaped or the table breaks). The
original regex let the backslash fall into the target group, and then
resolution became OS-dependent: on Windows `Path("a\\")` drops the
trailing separator so the link resolved, on Linux the backslash is a
filename character so the same link was broken. The result was a
locally-green / CI-red check — the exact class of platform-dependent
green this repo does not accept.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from scripts import check_links  # noqa: E402


class TestWikilinkRegex:
    def test_alias_without_escape(self) -> None:
        m = check_links.WIKILINK.search("see [[phase/7/note|the note]] here")
        assert m is not None
        assert m.group(1) == "phase/7/note"

    def test_alias_with_table_escape(self) -> None:
        """The escaped pipe must NOT end up inside the target — that
        trailing backslash is what made resolution OS-dependent."""
        m = check_links.WIKILINK.search("| [[phase/7/note\\|the note]] |")
        assert m is not None
        assert m.group(1) == "phase/7/note"
        assert not m.group(1).endswith("\\")

    def test_anchor_link(self) -> None:
        m = check_links.WIKILINK.search("see [[phase/7/note#section|alias]]")
        assert m is not None
        assert m.group(1) == "phase/7/note"

    def test_plain_link(self) -> None:
        m = check_links.WIKILINK.search("see [[phase/7/note]]")
        assert m is not None
        assert m.group(1) == "phase/7/note"


class TestResolveIsPlatformIndependent:
    """A target with no trailing backslash cannot resolve differently on
    Windows and Linux — that is the regression this pins."""

    def test_escaped_pipe_link_resolves_like_plain_link(self) -> None:
        known = {"07_capstone/notes/grokking-verdict-p113"}
        for text in (
            "[[07_capstone/notes/grokking-verdict-p113]]",
            "[[07_capstone/notes/grokking-verdict-p113\\|verdict]]",
        ):
            m = check_links.WIKILINK.search(text)
            assert m is not None
            target = m.group(1).strip()
            assert check_links._resolve(target, known), (
                f"{text!r} produced target {target!r} which does not resolve"
            )

    def test_broken_link_is_still_detected(self) -> None:
        known = {"07_capstone/notes/real-note"}
        m = check_links.WIKILINK.search("[[07_capstone/notes/never-written\\|x]]")
        assert m is not None
        assert not check_links._resolve(m.group(1).strip(), known)
