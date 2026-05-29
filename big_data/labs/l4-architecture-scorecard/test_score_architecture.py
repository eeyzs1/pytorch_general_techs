#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

from score_architecture import score


class ArchitectureScorecardTest(unittest.TestCase):
    def test_recommendation_is_ranked(self) -> None:
        data = json.loads(Path("data/options.json").read_text(encoding="utf-8"))
        report = score(data)
        self.assertEqual(report["recommendation"], report["ranked_options"][0])
        self.assertGreaterEqual(report["ranked_options"][0]["score"], report["ranked_options"][-1]["score"])
        self.assertTrue(report["recommendation"]["risks"])


if __name__ == "__main__":
    unittest.main()
