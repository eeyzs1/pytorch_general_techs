#!/usr/bin/env python3
"""Tests for the L0 web log analysis lab."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from analyze_logs import analyze
from generate_logs import generate


class AnalyzeLogsTest(unittest.TestCase):
    def test_generated_log_report_has_expected_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "access.log"
            generate(rows=50, output=log_path, seed=1)
            report = analyze(log_path)

        self.assertEqual(report["total_requests"], 50)
        self.assertEqual(report["malformed_rows"], 0)
        self.assertGreaterEqual(report["error_requests"], 0)
        self.assertTrue(report["status_counts"])
        self.assertTrue(report["top_ips"])
        self.assertTrue(report["top_paths"])

    def test_malformed_rows_are_counted(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "bad.log"
            log_path.write_text("not a valid log\n", encoding="utf-8")
            report = analyze(log_path)

        self.assertEqual(report["total_requests"], 0)
        self.assertEqual(report["malformed_rows"], 1)


if __name__ == "__main__":
    unittest.main()
