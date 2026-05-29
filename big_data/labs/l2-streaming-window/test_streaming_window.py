#!/usr/bin/env python3
"""Tests for the L2 streaming window lab."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from generate_events import generate
from window_aggregate import aggregate


class StreamingWindowTest(unittest.TestCase):
    def test_window_aggregation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            events_path = Path(tmpdir) / "events.jsonl"
            generate(rows=30, output=events_path, seed=7)
            report = aggregate(events_path)

        self.assertEqual(report["total_events"], 30)
        self.assertEqual(report["window_seconds"], 60)
        self.assertGreaterEqual(len(report["windows"]), 2)
        self.assertEqual(sum(w["event_count"] for w in report["windows"]), 30)
        self.assertTrue(all("gmv" in window for window in report["windows"]))


if __name__ == "__main__":
    unittest.main()
