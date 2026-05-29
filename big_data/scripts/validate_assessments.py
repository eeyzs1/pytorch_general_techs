#!/usr/bin/env python3
"""Validate structured assessment JSON files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "assessments"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    question_ids: set[str] = set()

    for path in sorted((ASSESSMENTS / "questions").glob("*.json")):
        data = load_json(path)
        questions = data.get("questions")
        if not isinstance(questions, list) or not questions:
            errors.append(f"{path.relative_to(ROOT)}: questions must be a non-empty list")
            continue
        for question in questions:
            qid = question.get("id")
            if not qid:
                errors.append(f"{path.relative_to(ROOT)}: question missing id")
                continue
            if qid in question_ids:
                errors.append(f"duplicate question id: {qid}")
            question_ids.add(qid)
            for key in ["type", "prompt", "answer"]:
                if key not in question:
                    errors.append(f"{path.relative_to(ROOT)}:{qid}: missing {key}")

    for path in sorted((ASSESSMENTS / "exams").glob("*.json")):
        data = load_json(path)
        for section in data.get("sections", []):
            for ref_key in ["source", "rubric"]:
                rel = section.get(ref_key)
                if rel and not (ROOT / rel).exists():
                    errors.append(f"{path.relative_to(ROOT)}: missing {ref_key}: {rel}")

    if errors:
        print("Assessment validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Assessment validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
