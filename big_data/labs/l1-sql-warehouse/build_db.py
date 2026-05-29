#!/usr/bin/env python3
"""Build a deterministic SQLite ecommerce warehouse for the L1 lab."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

SCHEMA = """
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  city TEXT NOT NULL,
  signup_date TEXT NOT NULL
);

CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  category TEXT NOT NULL,
  product_name TEXT NOT NULL,
  price REAL NOT NULL
);

CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  order_date TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_items (
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  unit_price REAL NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);
"""

USERS = [
    (1, "Hangzhou", "2026-05-01"),
    (2, "Shanghai", "2026-05-02"),
    (3, "Beijing", "2026-05-04"),
    (4, "Shenzhen", "2026-05-05"),
    (5, "Hangzhou", "2026-05-07"),
]
PRODUCTS = [
    (101, "digital", "keyboard", 299.0),
    (102, "digital", "mouse", 99.0),
    (201, "book", "ddia", 128.0),
    (202, "book", "spark-guide", 88.0),
    (301, "home", "chair", 399.0),
]
ORDERS = [
    (1001, 1, "2026-05-20", "paid"),
    (1002, 2, "2026-05-20", "paid"),
    (1003, 1, "2026-05-21", "cancelled"),
    (1004, 3, "2026-05-21", "paid"),
    (1005, 4, "2026-05-22", "paid"),
    (1006, 5, "2026-05-22", "paid"),
]
ORDER_ITEMS = [
    (1001, 101, 1, 299.0),
    (1001, 201, 2, 128.0),
    (1002, 102, 2, 99.0),
    (1003, 301, 1, 399.0),
    (1004, 202, 3, 88.0),
    (1005, 301, 1, 399.0),
    (1006, 101, 1, 299.0),
    (1006, 102, 1, 99.0),
]


def build(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    with sqlite3.connect(output) as conn:
        conn.executescript(SCHEMA)
        conn.executemany("INSERT INTO users VALUES (?, ?, ?)", USERS)
        conn.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", PRODUCTS)
        conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", ORDERS)
        conn.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?)", ORDER_ITEMS)
        conn.commit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the ecommerce SQLite database.")
    parser.add_argument("--output", type=Path, default=Path("data/ecommerce.db"), help="Output database path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build(args.output)
    print(f"Built SQLite warehouse at {args.output}")


if __name__ == "__main__":
    main()
