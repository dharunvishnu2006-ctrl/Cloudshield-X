import sqlite3
from pathlib import Path

DB_PATH = Path("cloudshield.db")
SCHEMA_PATH = Path("sql/schema.sql")


def get_conn() -> sqlite3.Connection:
    """Open a connection with foreign key enforcement turned on."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn
