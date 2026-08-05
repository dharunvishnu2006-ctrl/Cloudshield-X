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


def insert_events(rows: list[dict]) -> int:
    """Insert many events at once. Each row needs an 'ip' key.
    Returns the number of events inserted."""
    conn = get_conn()
    try:
        prepared = []
        for row in rows:
            ip_id = upsert_ip(row["ip"], row.get("event_time", ""))
            prepared.append(
                (
                    row["event_time"],
                    ip_id,
                    row.get("event_type"),
                    row.get("request"),
                    row.get("status"),
                    row.get("severity_score"),
                )
            )

        conn.executemany(
            "INSERT INTO security_events "
            "(event_time, source_ip, event_type, request, status, severity_score) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            prepared,
        )
        conn.commit()
        return len(prepared)
    finally:
        conn.close()
