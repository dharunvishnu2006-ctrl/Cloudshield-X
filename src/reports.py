from src.db import get_conn


def top_attackers(min_hits: int = 5, limit: int = 10) -> list[dict]:
    """Return the top attacking IPs, ranked by number of hits."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT ip.ip, COUNT(*) AS hits, AVG(e.severity_score) AS avg_sev
            FROM security_events e
            JOIN ip_addresses ip ON ip.id = e.source_ip
            WHERE e.status IN (401, 403)
            GROUP BY ip.ip
            HAVING COUNT(*) > ?
            ORDER BY hits DESC
            LIMIT ?
            """,
            (min_hits, limit),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def readable_events(limit: int = 20) -> list[dict]:
    """Return events with cleaned IPs, actor names, and severity labels."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT
                UPPER(TRIM(ip.ip)) AS ip,
                COALESCE(a.name, 'Unknown') AS actor,
                CASE
                    WHEN e.severity_score > 8 THEN 'CRITICAL'
                    WHEN e.severity_score > 5 THEN 'HIGH'
                    ELSE 'LOW'
                END AS severity_label
            FROM security_events e
            JOIN ip_addresses ip ON ip.id = e.source_ip
            LEFT JOIN threat_actors a ON a.id = e.actor_id
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def monthly_trend() -> list[dict]:
    """Return event counts grouped by month."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT STRFTIME('%Y-%m', event_time) AS month, COUNT(*) AS events
            FROM security_events
            GROUP BY month
            ORDER BY month
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def days_since_last_seen(ip: str) -> float | None:
    """Return how many days ago this IP was last seen, or None if never seen."""
    conn = get_conn()
    try:
        row = conn.execute(
            """
            SELECT JULIANDAY('now') - JULIANDAY(MAX(e.event_time)) AS days_ago
            FROM security_events e
            JOIN ip_addresses ip ON ip.id = e.source_ip
            WHERE ip.ip = ?
            """,
            (ip,),
        ).fetchone()
        return row["days_ago"]
    finally:
        conn.close()
