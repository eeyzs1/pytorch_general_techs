#!/usr/bin/env python3
"""Aggregate JSONL transaction events into event-time tumbling windows."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

WINDOW_SECONDS = 60
HIGH_RISK_THRESHOLD = 0.8


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def window_start(ts: datetime) -> datetime:
    seconds = int(ts.timestamp())
    return datetime.fromtimestamp(seconds - seconds % WINDOW_SECONDS, tz=ts.tzinfo)


def aggregate(path: Path) -> dict[str, Any]:
    windows: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"event_count": 0, "gmv": 0.0, "high_risk_count": 0, "unique_users": set()}
    )
    total_events = 0
    max_event_time: datetime | None = None

    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            event = json.loads(line)
            total_events += 1
            ts = parse_time(event["event_time"])
            max_event_time = ts if max_event_time is None or ts > max_event_time else max_event_time
            key = window_start(ts).isoformat()
            bucket = windows[key]
            bucket["event_count"] += 1
            bucket["gmv"] += float(event["amount"])
            bucket["high_risk_count"] += int(float(event["risk_score"]) >= HIGH_RISK_THRESHOLD)
            bucket["unique_users"].add(event["user_id"])

    result_windows = []
    for key in sorted(windows):
        bucket = windows[key]
        result_windows.append(
            {
                "window_start": key,
                "event_count": bucket["event_count"],
                "gmv": round(bucket["gmv"], 2),
                "high_risk_count": bucket["high_risk_count"],
                "unique_users": len(bucket["unique_users"]),
            }
        )

    return {
        "total_events": total_events,
        "window_seconds": WINDOW_SECONDS,
        "high_risk_threshold": HIGH_RISK_THRESHOLD,
        "max_event_time": max_event_time.isoformat() if max_event_time else None,
        "windows": result_windows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate transaction events by event-time window.")
    parser.add_argument("input", type=Path, help="Input JSONL events.")
    parser.add_argument("--output", type=Path, default=Path("output/window_report.json"), help="Output report path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = aggregate(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Aggregated {report['total_events']} events into {len(report['windows'])} windows")


if __name__ == "__main__":
    main()
