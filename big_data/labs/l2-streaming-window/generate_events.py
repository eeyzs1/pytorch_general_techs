#!/usr/bin/env python3
"""Generate deterministic JSONL transaction events for the L2 streaming lab."""

from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

TZ = timezone(timedelta(hours=8))


def generate(rows: int, output: Path, seed: int = 20260529) -> None:
    random.seed(seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    start = datetime(2026, 5, 29, 9, 0, 0, tzinfo=TZ)
    with output.open("w", encoding="utf-8") as fh:
        for i in range(rows):
            event_time = start + timedelta(seconds=i * 5 + random.randint(0, 3))
            amount = round(random.choice([29, 59, 99, 199, 499]) * random.uniform(0.8, 1.2), 2)
            risk_score = round(random.random(), 4)
            event = {
                "event_id": f"evt-{i + 1:06d}",
                "event_time": event_time.isoformat(),
                "user_id": f"u{random.randint(1, 30):03d}",
                "amount": amount,
                "risk_score": risk_score,
            }
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate transaction events.")
    parser.add_argument("--rows", type=int, default=240, help="Number of events.")
    parser.add_argument("--output", type=Path, default=Path("data/events.jsonl"), help="Output JSONL path.")
    parser.add_argument("--seed", type=int, default=20260529, help="Random seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate(args.rows, args.output, args.seed)
    print(f"Generated {args.rows} events at {args.output}")


if __name__ == "__main__":
    main()
