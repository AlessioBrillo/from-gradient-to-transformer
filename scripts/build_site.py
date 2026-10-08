#!/usr/bin/env python3
"""Render the public docs (README + portfolio) to a static site for GitHub Pages.

The site used to be the raw `portfolio/` folder: markdown files and no
index.html, so the public URL returned 404. Draft launch posts (threads,
space, walkthrough) and the premiere ledger are deliberately not published.
Links to repo files that are not part of the site point at GitHub.

Usage: uv run python scripts/build_site.py --out _site
"""

import argparse
import html
import os
import re
import shutil
from pathlib import Path

import markdown

REPO_URL = "https://github.com/AlessioBrillo/from-gradient-to-transformer"
PUBLISHED_GLOBS = [
    "README.md",
    "portfolio/README.md",
    "portfolio/RESULTS.md",
    "portfolio/model-card.md",
    "portfolio/projects/*/index.md",
    "portfolio/essay/*.md",
]
FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
ATTR_RE = re.compile(r'(href|src)="([^"]+)"')
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{ --bg:#fff; --fg:#1b1f24; --muted:#59636e; --line:#d1d9e0;
  --link:#0969da; --code:#f6f8fa; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --line:#30363d;
    --link:#4493f8; --code:#161b22; }}
}}
body {{ background:var(--bg); color:var(--fg); font:16px/1.6 system-ui,sans-serif; margin:0; }}
main {{ max-width:860px; margin:0 auto; padding:24px 16px 64px; }}
nav {{ border-bottom:1px solid var(--line); padding:12px 16px; font-size:14px; }}
nav a {{ margin-right:16px; }}
a {{ color:var(--link); }}
img {{ max-width:100%; height:auto; }}
table {{ border-collapse:collapse; display:block; overflow-x:auto; }}
th, td {{ border:1px solid var(--line); padding:6px 12px; }}
code, pre {{ background:var(--code); border-radius:6px; }}
code {{ padding:2px 5px; font-size:90%; }}
pre {{ padding:12px; overflow-x:auto; }} pre code {{ padding:0; }}
blockquote {{ margin:0; padding:0 16px; color:var(--muted); border-left:4px solid var(--line); }}
</style></head><body>
<nav><a href="{root}index.html">Home</a><a href="{root}portfolio/RESULTS.html">Results</a>
<a href="{root}portfolio/model-card.html">Model card</a><a href="{repo}">GitHub</a></nav>
<main>
{body}
</main></body></html>
"""


def out_path(md: Path) -> Path:
    """Site path for a published markdown file (README.md -> index.html)."""
    if md.name == "README.md":
        return md.with_name("index.html")
    return md.with_suffix(".html")


def rewrite_href(href: str, src: Path, published: set[Path], root: Path) -> str:
    """Rewrite one link found in `src` (a repo-relative path)."""
    if href.startswith(("http:", "https:", "mailto:", "#")):
        return href
    target, hash_, anchor = href.partition("#")
    resolved = Path(os.path.normpath((src.parent / target).as_posix()))
    if resolved in published:
        rel = os.path.relpath(out_path(resolved), out_path(src).parent).replace("\\", "/")
        return rel + (hash_ + anchor)
    if resolved.parts[:2] == ("portfolio", "figures"):
        return href  # figures are copied next to the pages
    if (root / resolved).exists():
        kind = "tree" if (root / resolved).is_dir() else "blob"
        return f"{REPO_URL}/{kind}/main/{resolved.as_posix()}" + (hash_ + anchor)
    return href


def _render(src: Path, published: set[Path], root: Path) -> str:
    text = FRONT_MATTER_RE.sub("", (root / src).read_text(encoding="utf-8"))
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    body = ATTR_RE.sub(
        lambda m: f'{m.group(1)}="{html.escape(rewrite_href(m.group(2), src, published, root))}"',
        body,
    )
    title_match = TITLE_RE.search(text)
    title = title_match.group(1).strip() if title_match else src.stem
    depth = len(out_path(src).parent.parts)
    return PAGE.format(
        title=html.escape(title), body=body, root="../" * depth, repo=REPO_URL
    )


def build_site(out: Path, root: Path = Path(".")) -> None:
    published = {
        p.relative_to(root) for pattern in PUBLISHED_GLOBS for p in sorted(root.glob(pattern))
    }
    for src in sorted(published):
        dest = out / out_path(src)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(_render(src, published, root), encoding="utf-8")
    figures = root / "portfolio" / "figures"
    if figures.exists():
        shutil.copytree(figures, out / "portfolio" / "figures", dirs_exist_ok=True)
    pdf = root / "portfolio" / "paper" / "main.pdf"
    if pdf.exists():
        shutil.copy(pdf, out / "paper.pdf")
    (out / ".nojekyll").write_text("")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("_site"))
    args = parser.parse_args()
    build_site(args.out)
    print(f"site written to {args.out}")


if __name__ == "__main__":
    main()
