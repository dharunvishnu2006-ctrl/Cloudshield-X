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
