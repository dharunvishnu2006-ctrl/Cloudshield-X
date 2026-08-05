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
