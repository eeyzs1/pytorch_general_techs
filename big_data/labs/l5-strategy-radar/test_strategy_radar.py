#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

from build_radar import build


class StrategyRadarTest(unittest.TestCase):
    def test_radar_outputs_quadrants(self) -> None:
        report = build(Path("data/technologies.csv"))
        self.assertEqual(len(report["items"]), 5)
        self.assertEqual(sum(report["summary"].values()), 5)
        self.assertIn(report["items"][0]["quadrant"], {"Adopt", "Trial", "Assess", "Hold"})


if __name__ == "__main__":
    unittest.main()
