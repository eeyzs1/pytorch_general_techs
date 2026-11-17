"""Behavioral tests for replay, stale revisions, tombstones, and recovery."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from replay_cdc import initialize, read_events, replay_batch, snapshot


def event(offset, revision, value=None, *, key="order-A", partition=0, op="upsert"):
    return {
        "partition": partition, "offset": offset, "key": key,
        "revision": revision, "op": op,
        "value": {"status": "paid"} if value is None and op == "upsert" else value,
    }


class ReplayTest(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        initialize(self.connection)
        self.addCleanup(self.connection.close)

    def test_sample_and_full_replay(self):
        events = list(read_events(Path(__file__).parent / "data/events.jsonl.sample"))
        stats = replay_batch(self.connection, events)
        self.assertEqual(stats, {"received": 10, "applied": 6, "duplicates": 2, "stale": 2})
        before = snapshot(self.connection)
        self.assertEqual(before["current"]["order-A"]["value"]["status"], "paid")
        self.assertEqual(before["tombstones"], {"order-B": 3})
        self.assertEqual(before["checkpoints"], {0: 5, 1: 4})
        self.assertEqual(before["receipt_count"], 8)
        self.assertEqual(replay_batch(self.connection, events)["duplicates"], 10)
        self.assertEqual(snapshot(self.connection), before)

    def test_delete_blocks_late_upsert_and_newer_revision_can_recreate(self):
        replay_batch(self.connection, [event(0, 3, op="delete"), event(1, 2)])
        self.assertEqual(snapshot(self.connection)["current"], {})
        replay_batch(self.connection, [event(2, 4)])
        self.assertEqual(snapshot(self.connection)["tombstones"], {})
        self.assertEqual(snapshot(self.connection)["current"]["order-A"]["revision"], 4)

    def test_offsets_can_have_gaps_and_are_partition_local(self):
        replay_batch(self.connection, [event(5, 1), event(0, 1, key="other", partition=1)])
        self.assertEqual(snapshot(self.connection)["checkpoints"], {0: 5, 1: 0})

    def test_same_offset_different_content_rolls_back_entire_batch(self):
        replay_batch(self.connection, [event(0, 1)])
        before = snapshot(self.connection)
        with self.assertRaisesRegex(ValueError, "same partition and offset"):
            replay_batch(self.connection, [event(1, 2), event(0, 3)])
        self.assertEqual(snapshot(self.connection), before)

    def test_same_business_revision_cannot_have_conflicting_content(self):
        replay_batch(self.connection, [event(0, 1)])
        with self.assertRaisesRegex(ValueError, "business revision"):
            replay_batch(self.connection, [event(1, 1, {"status": "cancelled"})])
        self.assertEqual(snapshot(self.connection)["checkpoints"], {0: 0})

    def test_unseen_transport_reordering_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "behind the partition checkpoint"):
            replay_batch(self.connection, [event(2, 1), event(1, 2)])
        self.assertEqual(snapshot(self.connection)["receipt_count"], 0)

    def test_invalid_event_rolls_back_state_receipts_and_checkpoint(self):
        invalid = event(1, 2)
        invalid["op"] = "unknown"
        with self.assertRaises(ValueError):
            replay_batch(self.connection, [event(0, 1), invalid])
        self.assertEqual(snapshot(self.connection), {
            "current": {}, "tombstones": {}, "checkpoints": {}, "receipt_count": 0,
        })

    def test_reader_failure_also_rolls_back(self):
        def interrupted():
            yield event(0, 1)
            raise OSError("simulated source failure")

        with self.assertRaises(OSError):
            replay_batch(self.connection, interrupted())
        self.assertEqual(snapshot(self.connection)["receipt_count"], 0)

    def test_reopen_database_and_replay_after_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sink.db"
            connection = sqlite3.connect(path)
            try:
                initialize(connection)
                replay_batch(connection, [event(0, 1)])
            finally:
                connection.close()
            reopened = sqlite3.connect(path)
            try:
                self.assertEqual(replay_batch(reopened, [event(0, 1)])["duplicates"], 1)
                self.assertEqual(snapshot(reopened)["checkpoints"], {0: 0})
            finally:
                reopened.close()


if __name__ == "__main__":
    unittest.main()
