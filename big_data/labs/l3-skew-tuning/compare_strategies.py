#!/usr/bin/env python3
"""Compare baseline and salted aggregation strategies."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def baseline(rows: Iterable[dict[str, str]]) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    for row in rows:
        totals[row["sku"]] += int(row["amount"])
    return dict(totals)


def salt_for(event_id: str, buckets: int) -> int:
    digest = hashlib.md5(event_id.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % buckets


def salted(rows: Iterable[dict[str, str]], hot_keys: set[str], buckets: int = 16) -> dict[str, int]:
    partial: dict[tuple[str, int], int] = defaultdict(int)
    for row in rows:
        key = row["sku"]
        salt = salt_for(row["event_id"], buckets) if key in hot_keys else 0
        partial[(key, salt)] += int(row["amount"])

    final: dict[str, int] = defaultdict(int)
    for (key, _salt), value in partial.items():
        final[key] += value
    return dict(final)


def timed(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 3)
    return result, elapsed_ms


def analyze(path: Path) -> dict[str, object]:
    rows = read_rows(path)
    key_counts = Counter(row["sku"] for row in rows)
    total_rows = len(rows)
    hot_key, hot_count = key_counts.most_common(1)[0]
    hot_ratio = round(hot_count / total_rows, 4) if total_rows else 0
    hot_keys = {key for key, count in key_counts.items() if count / total_rows >= 0.2}

    baseline_result, baseline_ms = timed(baseline, rows)
    salted_result, salted_ms = timed(salted, rows, hot_keys)

    return {
        "total_rows": total_rows,
        "distinct_keys": len(key_counts),
        "hot_key": hot_key,
        "hot_ratio": hot_ratio,
        "hot_keys": sorted(hot_keys),
        "results_match": baseline_result == salted_result,
        "baseline_ms": baseline_ms,
        "salted_ms": salted_ms,
        "top_totals": sorted(baseline_result.items(), key=lambda item: item[1], reverse=True)[:5],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare aggregation strategies.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/report.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = analyze(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Hot key {report['hot_key']} ratio={report['hot_ratio']}, match={report['results_match']}")


if __name__ == "__main__":
    main()
