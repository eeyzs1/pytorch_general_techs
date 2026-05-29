#!/usr/bin/env python3
"""Build a simple technology radar from weighted strategy factors."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def quadrant(score: float) -> str:
    if score >= 7.5:
        return "Adopt"
    if score >= 6.0:
        return "Trial"
    if score >= 4.5:
        return "Assess"
    return "Hold"


def build(path: Path) -> dict[str, Any]:
    items = []
    with path.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            impact = float(row["impact"])
            confidence = float(row["confidence"])
            cost = float(row["cost"])
            risk = float(row["risk"])
            score = impact * 0.4 + confidence * 0.3 + (10 - cost) * 0.15 + (10 - risk) * 0.15
            items.append({"name": row["name"], "score": round(score, 2), "quadrant": quadrant(score)})
    items.sort(key=lambda item: item["score"], reverse=True)
    summary: dict[str, int] = {"Adopt": 0, "Trial": 0, "Assess": 0, "Hold": 0}
    for item in items:
        summary[item["quadrant"]] += 1
    return {"items": items, "summary": summary}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build technology radar.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/radar.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Radar built with {len(report['items'])} technologies")


if __name__ == "__main__":
    main()
