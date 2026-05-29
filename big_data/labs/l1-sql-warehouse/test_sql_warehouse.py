#!/usr/bin/env python3
"""Tests for the L1 SQL warehouse lab."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from build_db import build
from run_analytics import analyze


class SqlWarehouseTest(unittest.TestCase):
    def test_analytics_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "ecommerce.db"
            build(db_path)
            report = analyze(db_path)

        self.assertEqual(report["paid_orders"], 5)
        self.assertEqual(report["active_users"], 5)
        self.assertEqual(report["gmv"], 1814.0)
        self.assertEqual(report["avg_order_value"], 362.8)
        self.assertEqual(report["top_categories"][0]["category"], "digital")
        self.assertEqual(len(report["daily_gmv"]), 3)


if __name__ == "__main__":
    unittest.main()
