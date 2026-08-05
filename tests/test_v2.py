import sqlite3
import pytest
from src.db import get_conn, init_db


def test_schema_and_fk():
    init_db()
    conn = get_conn()
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    table_names = [t["name"] for t in tables]
    assert "ip_addresses" in table_names
    assert "threat_actors" in table_names
    assert "security_events" in table_names
    conn.close()


def test_bad_foreign_key_rejected():
    conn = get_conn()
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO security_events (event_time, source_ip)" "VALUES (?, ?)",
                ("2026-08-05T10:00:00", 99999),
            )
    finally:
        conn.close()


def test_index_is_used():
    conn = get_conn()
    plan = conn.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM security_events WHERE source_ip = 1"
    ).fetchall()
    conn.close()
    plan_text = " ".join(row["detail"] for row in plan)
    assert "USING INDEX" in plan_text
