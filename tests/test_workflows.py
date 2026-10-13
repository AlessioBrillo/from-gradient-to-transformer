"""CI workflow wiring guards.

Issue #171 was "the paper never reaches the site": `pages.yml` built the
site without ever compiling `portfolio/paper/main.tex`, and
`build_site.py` copies the PDF to the site only when it exists — so the
live site shipped no paper, silently, for the repo's entire public life.
`paper.yml` compiled it, but only as a downloadable artifact.

These tests pin the wiring, because the failure mode of that class of bug
is silence: every step succeeds, and the artifact is simply absent.
"""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = REPO_ROOT / ".github" / "workflows"


def _steps(workflow: str) -> list[dict]:
    data = yaml.safe_load((WORKFLOWS / workflow).read_text(encoding="utf-8"))
    return list(data["jobs"]["build"]["steps"])


def _step_names(workflow: str) -> list[str]:
    return [s.get("name", s.get("uses", "?")) for s in _steps(workflow)]




class TestPagesDeploysThePaper:
    def test_pages_compiles_latex_before_building_site(self) -> None:
        names = _step_names("pages.yml")
        compile_idx = next(
            (i for i, n in enumerate(names) if "LaTeX" in n or "paper" in n.lower()), None
        )
        build_idx = next(
            (i for i, n in enumerate(names) if "Build site" in n), None
        )
        assert compile_idx is not None, (
            f"pages.yml has no LaTeX compile step; steps: {names}"
        )
        assert build_idx is not None, f"pages.yml lost its build step: {names}"
        assert compile_idx < build_idx, (
            "the paper must be compiled BEFORE build_site.py copies it"
        )

    def test_pages_verifies_the_pdf_reached_the_site(self) -> None:
        """The assertion step is the difference between 'compiled' and
        'shipped' — the original bug had neither."""
        text = (WORKFLOWS / "pages.yml").read_text(encoding="utf-8")
        assert "_site/paper.pdf" in text, (
            "pages.yml never asserts the compiled paper reached the site"
        )

    def test_pages_triggers_on_paper_sources(self) -> None:
        data = yaml.safe_load((WORKFLOWS / "pages.yml").read_text(encoding="utf-8"))
        # portfolio/** already covers portfolio/paper/**, but the paper path
        # must not have been dropped from a narrower filter.
        push_paths = data[True]["push"]["paths"]  # 'on:' parses as True
        assert any(p.startswith("portfolio") for p in push_paths)


class TestPaperWorkflow:
    def test_paper_workflow_guards_empty_bibliography(self) -> None:
        text = (WORKFLOWS / "paper.yml").read_text(encoding="utf-8")
        assert "bibliography is empty" in text, (
            "paper.yml lost its empty-bibliography guard"
        )
