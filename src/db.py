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


def init_db() -> None:
    """Create all tables and the index, safe to run more than once."""
    schema_sql = SCHEMA_PATH.read_text()
    conn = get_conn()
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()
