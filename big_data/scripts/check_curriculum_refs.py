#!/usr/bin/env python3
"""Check that file references listed in curriculum.yaml exist."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "curriculum.yaml"
PATH_RE = re.compile(r"^\s+path:\s+(.+?)\s*$")
COMMAND_RE = re.compile(r"^\s+command:\s+(.+?)\s*$")


def main() -> int:
    if not CURRICULUM.exists():
        print("Missing curriculum.yaml")
        return 1

    errors: list[str] = []
    text = CURRICULUM.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), 1):
        path_match = PATH_RE.match(line)
        if path_match:
            rel = path_match.group(1).strip().strip('"\'')
            if not (ROOT / rel).exists():
                errors.append(f"curriculum.yaml:{lineno}: missing path: {rel}")
        command_match = COMMAND_RE.match(line)
        if command_match:
            command = command_match.group(1).strip().strip('"\'')
            parts = command.split()
            if len(parts) >= 2 and parts[0].startswith("python"):
                script = ROOT / parts[1]
                if not script.exists():
                    errors.append(f"curriculum.yaml:{lineno}: missing command script: {parts[1]}")

    if errors:
        print("Curriculum reference check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Curriculum reference check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
