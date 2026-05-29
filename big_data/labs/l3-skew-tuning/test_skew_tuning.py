#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from compare_strategies import analyze
from generate_skewed_events import generate


class SkewTuningTest(unittest.TestCase):
    def test_salted_strategy_matches_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "events.csv"
            generate(rows=1000, output=path, seed=3)
            report = analyze(path)
        self.assertEqual(report["total_rows"], 1000)
        self.assertGreater(report["hot_ratio"], 0.5)
        self.assertTrue(report["results_match"])


if __name__ == "__main__":
    unittest.main()
