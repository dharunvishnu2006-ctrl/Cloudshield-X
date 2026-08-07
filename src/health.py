import time

_start_time = time.time()


def _cache_hit_rate() -> float:
    """Return the real hit rate from the shared profile cache."""
    from src.api import profile_cache

    total = profile_cache.hits + profile_cache.misses
    if total == 0:
        return 0.0
    return round(profile_cache.hits / total, 3)


def _log_file_writable() -> bool:
    log_path = "logs/app.log"
    try:
        with open(log_path, "a"):
            pass
        return True
    except Exception:
        return False


def build_health_report() -> dict:
    from src.db import get_conn

    report: dict = {"version": "v2.0"}

    try:
        conn = get_conn()
        conn.execute("SELECT 1")
    except Exception:
        report["database"] = "down"
        return report

    report["database"] = "connected"

    table_counts = {}
    table_counts["ip_addresses"] = conn.execute(
        "SELECT COUNT(*) as n FROM ip_addresses"
    ).fetchone()["n"]
    table_counts["threat_actors"] = conn.execute(
        "SELECT COUNT(*) as n FROM threat_actors"
    ).fetchone()["n"]
    table_counts["security_events"] = conn.execute(
        "SELECT COUNT(*) as n FROM security_events"
    ).fetchone()["n"]
    table_counts["host_links"] = conn.execute(
        "SELECT COUNT(*) as n FROM host_links"
    ).fetchone()["n"]
    report["tables"] = table_counts

    index_row = conn.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='index' AND name='idx_events_ip_time'"
    ).fetchone()
    report["indexes"] = {"idx_events_ip_time": index_row is not None}

    graph_row = conn.execute(
        "SELECT COUNT(*) as n FROM ("
        "SELECT src_host AS h FROM host_links "
        "UNION "
        "SELECT dst_host AS h FROM host_links"
        ")"
    ).fetchone()
    report["graph_hosts"] = graph_row["n"]

    conn.close()

    report["log_file"] = _log_file_writable()
    report["cache_hit_rate"] = _cache_hit_rate()
    report["uptime_s"] = round(time.time() - _start_time, 1)

    return report
