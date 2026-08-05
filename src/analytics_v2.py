from src.db import get_conn


def rank_within_type(limit: int = 50) -> list[dict]:
    """Rank each event's severity within its own event_type group."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT
                event_type, source_ip, severity_score,
                ROW_NUMBER() OVER (
                    PARTITION BY event_type
                    ORDER BY severity_score DESC
                ) AS rank_in_type
            FROM security_events
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def escalation_detector(limit: int = 100) -> list[dict]:
    """Compare each event's severity against the previous one from the same IP."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT
                source_ip, event_time, severity_score,
                LAG(severity_score, 1) OVER (
                    PARTITION BY source_ip
                    ORDER BY event_time
                ) AS prev_severity
            FROM security_events
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def initial_attack_vector(limit: int = 100) -> list[dict]:
    """Show each event alongside the FIRST event_type this IP ever tried."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT
                source_ip, event_time, event_type,
                FIRST_VALUE(event_type) OVER (
                    PARTITION BY source_ip
                    ORDER BY event_time
                ) AS first_ever_vector
            FROM security_events
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
