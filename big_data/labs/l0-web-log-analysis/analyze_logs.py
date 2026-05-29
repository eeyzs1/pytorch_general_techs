#!/usr/bin/env python3
"""Analyze access logs and emit a compact JSON report."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

LOG_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d{3}) (?P<size>\d+) '
)


def analyze(path: Path) -> dict[str, object]:
    total = 0
    malformed = 0
    status_counts: Counter[str] = Counter()
    ip_counts: Counter[str] = Counter()
    path_counts: Counter[str] = Counter()
    method_counts: Counter[str] = Counter()
    bytes_total = 0

    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            match = LOG_RE.match(line.strip())
            if not match:
                malformed += 1
                continue
            total += 1
            data = match.groupdict()
            status_counts[data["status"]] += 1
            ip_counts[data["ip"]] += 1
            path_counts[data["path"]] += 1
            method_counts[data["method"]] += 1
            bytes_total += int(data["size"])

    error_requests = sum(count for status, count in status_counts.items() if int(status) >= 400)
    return {
        "total_requests": total,
        "malformed_rows": malformed,
        "error_requests": error_requests,
        "error_rate": round(error_requests / total, 4) if total else 0,
        "bytes_total": bytes_total,
        "status_counts": dict(sorted(status_counts.items())),
        "method_counts": dict(sorted(method_counts.items())),
        "top_ips": ip_counts.most_common(5),
        "top_paths": path_counts.most_common(5),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze access logs.")
    parser.add_argument("input", type=Path, help="Input access log path.")
    parser.add_argument("--output", type=Path, default=Path("output/report.json"), help="Output report path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = analyze(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Analyzed {report['total_requests']} requests, report written to {args.output}")


if __name__ == "__main__":
    main()
