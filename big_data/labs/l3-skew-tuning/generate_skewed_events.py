#!/usr/bin/env python3
"""Generate skewed key/value events for the L3 tuning lab."""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

HOT_KEY = "sku-hot"
COLD_KEYS = [f"sku-{i:03d}" for i in range(1, 101)]


def generate(rows: int, output: Path, seed: int = 20260529) -> None:
    random.seed(seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["event_id", "sku", "amount"])
        writer.writeheader()
        for i in range(rows):
            sku = HOT_KEY if random.random() < 0.65 else random.choice(COLD_KEYS)
            writer.writerow({"event_id": i + 1, "sku": sku, "amount": random.randint(1, 20)})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate skewed events.")
    parser.add_argument("--rows", type=int, default=5000)
    parser.add_argument("--output", type=Path, default=Path("data/events.csv"))
    parser.add_argument("--seed", type=int, default=20260529)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate(args.rows, args.output, args.seed)
    print(f"Generated {args.rows} skewed rows at {args.output}")


if __name__ == "__main__":
    main()
