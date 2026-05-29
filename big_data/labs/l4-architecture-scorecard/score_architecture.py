#!/usr/bin/env python3
"""Score architecture options with weighted criteria."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def score(data: dict[str, Any]) -> dict[str, Any]:
    criteria: dict[str, float] = data["criteria"]
    ranked = []
    for option in data["options"]:
        total = 0.0
        for criterion, weight in criteria.items():
            total += float(option["scores"].get(criterion, 0)) * weight
        ranked.append({"name": option["name"], "score": round(total, 3), "risks": option.get("risks", [])})
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return {"criteria": criteria, "recommendation": ranked[0], "ranked_options": ranked}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score architecture options.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/decision.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = score(json.loads(args.input.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Recommended: {report['recommendation']['name']} ({report['recommendation']['score']})")


if __name__ == "__main__":
    main()
