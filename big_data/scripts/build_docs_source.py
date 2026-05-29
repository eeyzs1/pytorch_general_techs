#!/usr/bin/env python3
"""Build a temporary MkDocs source tree from repository Markdown files."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_SRC = ROOT / ".docs_src"
EXCLUDE_DIRS = {".git", ".site", ".docs_src", "site"}


STATIC_SUFFIXES = {".csv", ".json", ".sample", ".yaml", ".yml"}


def should_copy(path: Path) -> bool:
    rel_parts = path.relative_to(ROOT).parts
    if any(part in EXCLUDE_DIRS for part in rel_parts):
        return False
    return path.suffix == ".md" or path.suffix in STATIC_SUFFIXES


def main() -> None:
    if DOCS_SRC.exists():
        shutil.rmtree(DOCS_SRC)
    DOCS_SRC.mkdir(parents=True)
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if not should_copy(path):
            continue
        rel = path.relative_to(ROOT)
        dest = DOCS_SRC / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    print(f"Prepared MkDocs source at {DOCS_SRC}")


if __name__ == "__main__":
    main()
