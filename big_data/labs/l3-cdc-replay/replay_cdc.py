#!/usr/bin/env python3
"""Replay a single synthetic CDC stream into an atomic, idempotent SQLite sink."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Iterable


def initialize(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS entity_state (
            entity_key TEXT PRIMARY KEY,
            revision INTEGER NOT NULL,
            operation TEXT NOT NULL,
            value_json TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS receipts (
            partition_id INTEGER NOT NULL,
            source_offset INTEGER NOT NULL,
            entity_key TEXT NOT NULL,
            revision INTEGER NOT NULL,
            body_json TEXT NOT NULL,
            PRIMARY KEY (partition_id, source_offset)
        );
        CREATE INDEX IF NOT EXISTS receipts_revision
            ON receipts(entity_key, revision);
        CREATE TABLE IF NOT EXISTS checkpoints (
            partition_id INTEGER PRIMARY KEY,
            source_offset INTEGER NOT NULL
        );
        """
    )


def validate_event(event: dict) -> tuple[int, int, str, int, str, str, str]:
    fields = {"partition", "offset", "key", "revision", "op", "value"}
    if not isinstance(event, dict) or set(event) != fields:
        raise ValueError(f"Event must contain exactly {sorted(fields)}")
    for name in ("partition", "offset", "revision"):
        if type(event[name]) is not int or not 0 <= event[name] < 2**63:
            raise ValueError(f"{name} must be a non-negative SQLite integer")
    if not isinstance(event["key"], str) or not event["key"].strip():
        raise ValueError("key must be a non-empty string")
    operation = event["op"]
    if operation not in ("upsert", "delete"):
        raise ValueError("op must be upsert or delete")
    if operation == "upsert" and not isinstance(event["value"], dict):
        raise ValueError("upsert requires an object value")
    if operation == "delete" and event["value"] is not None:
        raise ValueError("delete requires a null value")
    body = {key: event[key] for key in ("key", "revision", "op", "value")}
    body_json = json.dumps(body, sort_keys=True, ensure_ascii=False, allow_nan=False)
    value_json = json.dumps(event["value"], sort_keys=True, ensure_ascii=False, allow_nan=False)
    return (
        event["partition"], event["offset"], event["key"],
        event["revision"], operation, value_json, body_json,
    )


def replay_batch(connection: sqlite3.Connection, events: Iterable[dict]) -> dict:
    """Commit state, receipts, and positions together, or roll back the whole batch.

    New source offsets must increase within each partition; gaps are valid.
    Previously received offsets may be replayed, but their content must agree.
    Business revisions must be comparable across events for the same entity key.
    """
    stats = {"received": 0, "applied": 0, "duplicates": 0, "stale": 0}
    connection.execute("BEGIN IMMEDIATE")
    try:
        for event in events:
            partition, offset, key, revision, operation, value_json, body_json = validate_event(event)
            stats["received"] += 1
            receipt = connection.execute(
                "SELECT body_json FROM receipts WHERE partition_id=? AND source_offset=?",
                (partition, offset),
            ).fetchone()
            if receipt is not None:
                if receipt[0] != body_json:
                    raise ValueError("Conflicting payload for the same partition and offset")
                stats["duplicates"] += 1
                continue

            checkpoint = connection.execute(
                "SELECT source_offset FROM checkpoints WHERE partition_id=?", (partition,)
            ).fetchone()
            if checkpoint is not None and offset <= checkpoint[0]:
                raise ValueError("Unseen source offset arrived behind the partition checkpoint")
            prior_revision = connection.execute(
                "SELECT body_json FROM receipts WHERE entity_key=? AND revision=? LIMIT 1",
                (key, revision),
            ).fetchone()
            if prior_revision is not None and prior_revision[0] != body_json:
                raise ValueError("Conflicting payload for the same key and business revision")

            current = connection.execute(
                "SELECT revision FROM entity_state WHERE entity_key=?", (key,)
            ).fetchone()
            if current is None or revision > current[0]:
                connection.execute(
                    "INSERT INTO entity_state VALUES (?, ?, ?, ?) "
                    "ON CONFLICT(entity_key) DO UPDATE SET "
                    "revision=excluded.revision, operation=excluded.operation, "
                    "value_json=excluded.value_json",
                    (key, revision, operation, value_json),
                )
                stats["applied"] += 1
            else:
                stats["stale"] += 1

            connection.execute(
                "INSERT INTO receipts VALUES (?, ?, ?, ?, ?)",
                (partition, offset, key, revision, body_json),
            )
            connection.execute(
                "INSERT INTO checkpoints VALUES (?, ?) ON CONFLICT(partition_id) "
                "DO UPDATE SET source_offset=excluded.source_offset", (partition, offset)
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    return stats


def snapshot(connection: sqlite3.Connection) -> dict:
    rows = connection.execute(
        "SELECT entity_key, revision, operation, value_json FROM entity_state ORDER BY entity_key"
    ).fetchall()
    return {
        "current": {
            key: {"revision": revision, "value": json.loads(value)}
            for key, revision, operation, value in rows if operation == "upsert"
        },
        "tombstones": {key: revision for key, revision, operation, _ in rows if operation == "delete"},
        "checkpoints": dict(connection.execute(
            "SELECT partition_id, source_offset FROM checkpoints ORDER BY partition_id"
        )),
        "receipt_count": connection.execute("SELECT COUNT(*) FROM receipts").fetchone()[0],
    }


def read_events(path: Path) -> Iterable[dict]:
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path)
    parser.add_argument("--database", type=Path, default=Path("output/cdc.db"))
    parser.add_argument("--output", type=Path, default=Path("output/report.json"))
    args = parser.parse_args()
    args.database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(args.database)
    try:
        initialize(connection)
        report = {"batch": replay_batch(connection, read_events(args.events)), **snapshot(connection)}
    finally:
        connection.close()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
