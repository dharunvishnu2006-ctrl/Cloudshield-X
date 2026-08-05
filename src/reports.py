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


def full_profile(limit: int = 20) -> list[dict]:
    """Return event + IP + actor joined into one row per event."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT e.id, e.event_time, ip.ip, a.name AS actor, e.severity_score
            FROM security_events e
            INNER JOIN ip_addresses ip ON ip.id = e.source_ip
            INNER JOIN threat_actors a ON a.id = e.actor_id
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def never_attacked_ips() -> list[str]:
    """Return IPs that exist in our records but have zero events."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT ip.ip
            FROM ip_addresses ip
            LEFT JOIN security_events e ON ip.id = e.source_ip
            WHERE e.id IS NULL
            """
        ).fetchall()
        return [row["ip"] for row in rows]
    finally:
        conn.close()


def reconcile_feeds() -> list[dict]:
    """Emulate FULL OUTER JOIN: show IPs unique to either the blocklist
    or the observed-events side, since SQLite has no FULL OUTER JOIN."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT ip.ip AS ip, ip.is_blocklisted, e.id AS event_id
            FROM ip_addresses ip
            LEFT JOIN security_events e ON ip.id = e.source_ip

            UNION

            SELECT ip.ip AS ip, ip.is_blocklisted, e.id AS event_id
            FROM security_events e
            LEFT JOIN ip_addresses ip ON ip.id = e.source_ip
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def repeat_endpoint_hits(within_minutes: int = 5) -> list[dict]:
    """Find the same IP hitting two different events within a short window."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT
                e1.id AS event1, e2.id AS event2,
                ip.ip, e1.event_time AS time1, e2.event_time AS time2
            FROM security_events e1
            JOIN security_events e2
                ON e1.source_ip = e2.source_ip
                AND e1.id < e2.id
            JOIN ip_addresses ip ON ip.id = e1.source_ip
            WHERE (JULIANDAY(e2.event_time) - JULIANDAY(e1.event_time)) * 1440
                  <= ?
            """,
            (within_minutes,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def above_average_blocklisted_threats() -> list[dict]:
    """Return events with above-average severity, from blocklisted IPs."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT id, event_time, source_ip, severity_score
            FROM security_events
            WHERE severity_score > (
                SELECT AVG(severity_score) FROM security_events
            )
            AND EXISTS (
                SELECT 1 FROM ip_addresses
                WHERE id = source_ip AND is_blocklisted = 1
            )
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def propagation_trace(start_host: str, max_hops: int = 6) -> list[dict]:
    """Trace every host reachable from start_host, with the shortest hop count."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            WITH RECURSIVE reached(host, depth) AS (
                SELECT ?, 0

                UNION

                SELECT l.dst_host, r.depth + 1
                FROM host_links l
                JOIN reached r ON l.src_host = r.host
                WHERE r.depth < ?
            )
            SELECT host, MIN(depth) AS hops
            FROM reached
            GROUP BY host
            ORDER BY hops
            """,
            (start_host, max_hops),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
