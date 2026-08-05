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


def upsert_ip(ip: str, first_seen: str = "") -> int:
    """Insert a new IP or return the id of the existing one."""
    conn = get_conn()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO ip_addresses (ip, first_seen) VALUES (?, ?)",
            (ip, first_seen),
        )
        conn.commit()
        row = conn.execute("SELECT id FROM ip_addresses WHERE ip = ?", (ip,)).fetchone()
        return row["id"]
    finally:
        conn.close()
