import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from src.logging_setup import get_logger

logger = get_logger("store")
DB_PATH = Path("cloudshield.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                scanned_at TEXT NOT NULL,
                log_file TEXT NOT NULL
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER NOT NULL,
                ip TEXT NOT NULL,
                status INTEGER NOT NULL,
                path TEXT NOT NULL,
                at TEXT NOT NULL,
                FOREIGN KEY (scan_id) REFERENCES scans(id)
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER NOT NULL,
                ip TEXT NOT NULL,
                count INTEGER NOT NULL,
                severity TEXT NOT NULL,
                at TEXT NOT NULL,
                FOREIGN KEY (scan_id) REFERENCES scans(id)
            )
        """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_events_ip
            ON events(ip)
        """
        )
        logger.info("Database initialized")


def save_scan(run_id: str, log_file: str) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO scans (run_id, scanned_at, log_file) " "VALUES (?, ?, ?)",
            (run_id, datetime.now(timezone.utc).isoformat(), log_file),
        )
        return cursor.lastrowid or 0


def save_alert(scan_id: int, ip: str, count: int, severity: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO alerts (scan_id, ip, count, severity, at) "
            "VALUES (?, ?, ?, ?, ?)",
            (scan_id, ip, count, severity, datetime.now(timezone.utc).isoformat()),
        )


def get_repeat_offenders() -> list:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT ip, COUNT(DISTINCT scan_id) as scan_count,
                   SUM(count) as total_attempts
            FROM alerts
            WHERE at >= datetime('now', '-7 days')
            GROUP BY ip
            HAVING COUNT(DISTINCT scan_id) > 1
            ORDER BY total_attempts DESC
            """
        )
        return [dict(row) for row in cursor.fetchall()]
