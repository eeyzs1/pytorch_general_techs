#!/usr/bin/env python3
"""Check relative Markdown links without scanning fenced code blocks."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
EXCLUDE_DIRS = {".git", ".site", "site"}


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if any(part in EXCLUDE_DIRS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def non_code_lines(path: Path) -> list[tuple[int, str]]:
    in_fence = False
    result: list[tuple[int, str]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            result.append((lineno, line))
    return result


def is_external(target: str) -> bool:
    parsed = urlparse(target)
    return parsed.scheme in {"http", "https", "mailto", "tel"}


def normalize_target(target: str) -> str:
    target = target.strip().strip("<>")
    if " " in target and not target.startswith("#"):
        target = target.split()[0]
    target = target.split("#", 1)[0].split("?", 1)[0]
    return unquote(target)


def main() -> int:
    errors: list[str] = []
    for path in iter_markdown_files():
        for lineno, line in non_code_lines(path):
            for match in LINK_RE.finditer(line):
                raw_target = match.group(1).strip()
                if not raw_target or raw_target.startswith("#") or is_external(raw_target):
                    continue
                target = normalize_target(raw_target)
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    errors.append(f"{path.relative_to(ROOT)}:{lineno}: link escapes repo: {raw_target}")
                    continue
                if not resolved.exists():
                    errors.append(f"{path.relative_to(ROOT)}:{lineno}: missing link target: {raw_target}")
    if errors:
        print("Markdown link check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Markdown link check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
