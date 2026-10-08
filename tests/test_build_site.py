"""The Pages site used to be the raw `portfolio/` folder: markdown files and no
index.html, so the public URL returned 404 (found 2026-10-08)."""

from pathlib import Path

import pytest

from scripts.build_site import REPO_URL, build_site, out_path, rewrite_href


def test_out_path_maps_markdown_to_html() -> None:
    assert out_path(Path("README.md")) == Path("index.html")
    assert out_path(Path("portfolio/README.md")) == Path("portfolio/index.html")
    assert out_path(Path("portfolio/RESULTS.md")) == Path("portfolio/RESULTS.html")
    assert out_path(Path("portfolio/projects/rung-1/index.md")) == Path(
        "portfolio/projects/rung-1/index.html"
    )


def test_published_links_become_relative_html() -> None:
    published = {Path("README.md"), Path("portfolio/RESULTS.md")}
    assert (
        rewrite_href("portfolio/RESULTS.md", Path("README.md"), published, Path("."))
        == "portfolio/RESULTS.html"
    )
    assert (
        rewrite_href(
            "../../RESULTS.md#rung-3", Path("portfolio/projects/x/index.md"), published, Path(".")
        )
        == "../../RESULTS.html#rung-3"
    )


def test_unpublished_repo_files_link_to_github(tmp_path: Path) -> None:
    (tmp_path / "07_capstone").mkdir()
    (tmp_path / "07_capstone" / "_MOC.md").write_text("x")
    href = rewrite_href("../07_capstone/_MOC.md", Path("portfolio/README.md"), set(), tmp_path)
    assert href == f"{REPO_URL}/blob/main/07_capstone/_MOC.md"


def test_external_and_anchor_links_are_untouched() -> None:
    for href in ("https://example.org/a.md", "#section", "mailto:a@b.c"):
        assert rewrite_href(href, Path("README.md"), set(), Path(".")) == href


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("site")
    build_site(out, Path("."))
    return out


def test_site_has_an_index_and_the_results_page(site: Path) -> None:
    assert (site / "index.html").stat().st_size > 1000
    assert (site / "portfolio" / "RESULTS.html").exists()
    assert (site / ".nojekyll").exists()


def test_site_ships_curated_figures_and_not_the_draft_launch_posts(site: Path) -> None:
    assert any((site / "portfolio" / "figures").glob("*.png"))
    for draft in ("threads", "space", "walkthrough"):
        assert not (site / "portfolio" / draft).exists()


def test_no_published_page_links_to_a_markdown_file(site: Path) -> None:
    import re

    for page in site.rglob("*.html"):
        hrefs = re.findall(r'href="([^"]+)"', page.read_text(encoding="utf-8"))
        local_md = [h for h in hrefs if not h.startswith(("http", "#", "mailto")) and ".md" in h]
        assert local_md == [], f"{page.relative_to(site)} links to {local_md[:3]}"
