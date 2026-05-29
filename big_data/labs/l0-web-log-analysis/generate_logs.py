#!/usr/bin/env python3
"""Generate deterministic sample web access logs for the L0 lab."""

from __future__ import annotations

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

IPS = [f"192.168.1.{i}" for i in range(1, 21)]
METHODS = ["GET", "POST"]
PATHS = ["/", "/index.html", "/login", "/api/products", "/api/orders", "/cart"]
STATUSES = [200, 200, 200, 200, 301, 404, 500]
USER_AGENTS = ["curl/8.0", "Mozilla/5.0", "Python-urllib/3.11"]


def generate(rows: int, output: Path, seed: int = 20260529) -> None:
    random.seed(seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    start = datetime(2026, 5, 29, 9, 0, 0)
    with output.open("w", encoding="utf-8") as fh:
        for i in range(rows):
            ts = start + timedelta(seconds=i * random.randint(1, 5))
            line = (
                f'{random.choice(IPS)} - - [{ts:%d/%b/%Y:%H:%M:%S +0800}] '
                f'"{random.choice(METHODS)} {random.choice(PATHS)} HTTP/1.1" '
                f'{random.choice(STATUSES)} {random.randint(128, 8192)} '
                f'"-" "{random.choice(USER_AGENTS)}"'
            )
            fh.write(line + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate sample access logs.")
    parser.add_argument("--rows", type=int, default=200, help="Number of log rows to generate.")
    parser.add_argument("--output", type=Path, default=Path("data/access.log"), help="Output log path.")
    parser.add_argument("--seed", type=int, default=20260529, help="Random seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate(args.rows, args.output, args.seed)
    print(f"Generated {args.rows} rows at {args.output}")


if __name__ == "__main__":
    main()
