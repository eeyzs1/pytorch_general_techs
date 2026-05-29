#!/usr/bin/env python3
"""Run ecommerce warehouse analytics and emit a JSON report."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any


def scalar(conn: sqlite3.Connection, sql: str) -> Any:
    return conn.execute(sql).fetchone()[0]


def rows(conn: sqlite3.Connection, sql: str) -> list[dict[str, Any]]:
    conn.row_factory = sqlite3.Row
    return [dict(row) for row in conn.execute(sql).fetchall()]


def analyze(db_path: Path) -> dict[str, Any]:
    with sqlite3.connect(db_path) as conn:
        gmv = scalar(
            conn,
            """
            SELECT ROUND(SUM(oi.quantity * oi.unit_price), 2)
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.status = 'paid'
            """,
        )
        paid_orders = scalar(conn, "SELECT COUNT(*) FROM orders WHERE status = 'paid'")
        active_users = scalar(conn, "SELECT COUNT(DISTINCT user_id) FROM orders WHERE status = 'paid'")
        top_categories = rows(
            conn,
            """
            SELECT p.category, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.status = 'paid'
            GROUP BY p.category
            ORDER BY revenue DESC
            """,
        )
        daily_gmv = rows(
            conn,
            """
            SELECT o.order_date, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gmv
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.status = 'paid'
            GROUP BY o.order_date
            ORDER BY o.order_date
            """,
        )
    return {
        "gmv": gmv,
        "paid_orders": paid_orders,
        "active_users": active_users,
        "avg_order_value": round(gmv / paid_orders, 2) if paid_orders else 0,
        "top_categories": top_categories,
        "daily_gmv": daily_gmv,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ecommerce analytics.")
    parser.add_argument("database", type=Path, help="SQLite database path.")
    parser.add_argument("--output", type=Path, default=Path("output/report.json"), help="Output report path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = analyze(args.database)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote analytics report to {args.output}")


if __name__ == "__main__":
    main()
