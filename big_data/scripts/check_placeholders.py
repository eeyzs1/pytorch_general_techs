#!/usr/bin/env python3
"""Detect placeholder links and unresolved maintenance markers in prose."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {".git", ".site", "site"}
CHECK_SUFFIXES = {".md", ".yaml", ".yml"}
PATTERNS = [
    re.compile(r"\]\((?:link|todo|tbd|待补充)\)", re.IGNORECASE),
    re.compile(r"\b(?:FIXME|TBD)\b", re.IGNORECASE),
    re.compile(r"待补充|占位链接"),
]


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in CHECK_SUFFIXES:
            continue
        rel_parts = path.relative_to(ROOT).parts
        if any(part in EXCLUDE_DIRS for part in rel_parts):
            continue
        files.append(path)
    return sorted(files)


def non_code_lines(path: Path) -> list[tuple[int, str]]:
    if path.suffix not in {".md"}:
        return list(enumerate(path.read_text(encoding="utf-8").splitlines(), 1))
    in_fence = False
    result: list[tuple[int, str]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            result.append((lineno, line))
    return result


def main() -> int:
    errors: list[str] = []
    for path in iter_files():
        for lineno, line in non_code_lines(path):
            for pattern in PATTERNS:
                if pattern.search(line):
                    errors.append(f"{path.relative_to(ROOT)}:{lineno}: {line.strip()}")
                    break
    if errors:
        print("Placeholder check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Placeholder check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
