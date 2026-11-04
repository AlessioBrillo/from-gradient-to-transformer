#!/usr/bin/env python3
"""Write a zip archive of manifest files without shell quoting.

Why this exists
---------------
The remote notebooks used ``!zip -j results.zip $manifests``. IPython expands
a Python list to its repr, so ``zip`` received a single token that looked like
``['results/a.json', 'results/b.json']`` -- brackets and quotes included. It
found no such file, wrote no archive, and the session's manifests were lost on
Colab (the separate verdict download still worked, which made the failure easy
to miss).

This helper takes the paths directly. It refuses an empty list, a missing
file, and two files with the same basename (a zip cannot hold both under one
name), so a partial or silently-overwritten archive is impossible.

Usage:
    python scripts/zip_manifests.py --output results.zip results/a.json ...
"""

from __future__ import annotations

import argparse
import zipfile
from collections.abc import Iterable, Sequence
from pathlib import Path


def _existing_files(paths: Iterable[str | Path]) -> list[Path]:
    files = [Path(path) for path in paths]
    if not files:
        raise ValueError("no files to zip")
    missing = [str(path) for path in files if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing file(s): " + ", ".join(missing))
    names = [path.name for path in files]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(
            "cannot zip files with the same basename: " + ", ".join(duplicates)
        )
    return files


def write_manifest_zip(paths: Iterable[str | Path], archive: str | Path) -> Path:
    """Write ``paths`` into ``archive`` under their basenames; return the archive."""
    files = _existing_files(paths)
    target = Path(archive)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in files:
            bundle.write(path, arcname=path.name)
    return target


def append_to_zip(paths: Iterable[str | Path], archive: str | Path) -> Path:
    """Append ``paths`` to an existing archive, creating it when absent.

    Refuses a name that is already in the archive: appending a second
    ``content_verdict.json`` would silently shadow the first one.
    """
    files = _existing_files(paths)
    target = Path(archive)
    if not target.is_file():
        return write_manifest_zip(files, target)
    with zipfile.ZipFile(target, "a", compression=zipfile.ZIP_DEFLATED) as bundle:
        present = set(bundle.namelist())
        for path in files:
            if path.name in present:
                raise ValueError(f"{path.name} is already in {target}")
            bundle.write(path, arcname=path.name)
    return target


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Write a zip of manifest files without shell expansion."
    )
    parser.add_argument("--output", required=True, help="archive to write")
    parser.add_argument("files", nargs="+", help="files to include (by basename)")
    args = parser.parse_args(argv)
    archive = write_manifest_zip(args.files, args.output)
    print(f"wrote {archive} ({len(args.files)} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
