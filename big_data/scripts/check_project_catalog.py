#!/usr/bin/env python3
"""Validate project_catalog.json and prevent known project-number regressions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "project_catalog.json"
FORBIDDEN_PATTERNS = [
    re.compile(r"项目11[：:]云原生"),
    re.compile(r"项目11_云原生"),
    re.compile(r"云原生迁移项目11"),
]


def iter_markdown_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts and ".site" not in p.parts)


def main() -> int:
    errors: list[str] = []
    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("Missing project_catalog.json")
        return 1

    seen: set[str] = set()
    for project in data.get("projects", []):
        pid = project.get("id")
        if not pid:
            errors.append("project missing id")
            continue
        if pid in seen:
            errors.append(f"duplicate project id: {pid}")
        seen.add(pid)
        rel = project.get("path", "")
        if not rel or not (ROOT / rel).exists():
            errors.append(f"{pid}: missing path: {rel}")

    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)}: forbidden project-number pattern: {pattern.pattern}")

    if errors:
        print("Project catalog check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Project catalog check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
