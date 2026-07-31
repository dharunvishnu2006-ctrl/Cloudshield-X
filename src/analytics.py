import numpy as np
import pandas as pd
from src.models import LogEvent
from src.logging_setup import get_logger

logger = get_logger("analytics")


def compute_request_stats(events: list[LogEvent]) -> dict:
    if not events:
        return {}

    counts_by_ip: dict = {}
    for e in events:
        counts_by_ip[e.ip] = counts_by_ip.get(e.ip, 0) + 1

    counts_array = np.array(list(counts_by_ip.values()))

    stats = {
        "mean": float(np.mean(counts_array)),
        "median": float(np.median(counts_array)),
        "p95": float(np.percentile(counts_array, 95)),
        "max": float(np.max(counts_array)),
        "total_ips": len(counts_array),
    }

    logger.info(f"Request stats: {stats}")
    return stats


def flag_suspicious_numpy(
    events: list[LogEvent], threshold: float | None = None
) -> list[str]:
    if not events:
        return []

    counts_by_ip: dict = {}
    for e in events:
        counts_by_ip[e.ip] = counts_by_ip.get(e.ip, 0) + 1

    ips = np.array(list(counts_by_ip.keys()))
    counts = np.array(list(counts_by_ip.values()))

    if threshold is None:
        threshold = float(np.percentile(counts, 95))
        logger.info(f"Auto threshold (p95): {threshold}")

    mask = counts > threshold
    suspicious_ips = ips[mask].tolist()

    logger.info(f"Flagged {len(suspicious_ips)} IPs " f"above threshold {threshold}")
    return suspicious_ips


def analyse_events(events: list[LogEvent]) -> pd.DataFrame:
    if not events:
        return pd.DataFrame()

    rows = []
    for e in events:
        rows.append(
            {
                "ip": e.ip,
                "status": e.status,
                "path": e.path,
                "method": e.method,
                "timestamp": e.timestamp,
            }
        )

    df = pd.DataFrame(rows)

    grouped = (
        df.groupby("ip")
        .agg(
            count=("ip", "count"),
            distinct_paths=("path", "nunique"),
            max_status=("status", "max"),
        )
        .reset_index()
    )

    grouped = grouped.sort_values("count", ascending=False)

    logger.info(f"Analysed {len(df)} events, " f"{len(grouped)} unique IPs")
    return grouped


def merge_with_allowlist(grouped: pd.DataFrame, allowlist: list[str]) -> pd.DataFrame:
    if grouped.empty:
        return grouped

    allow_df = pd.DataFrame({"ip": allowlist, "allowed": True})

    merged = grouped.merge(allow_df, on="ip", how="left")
    merged["allowed"] = merged["allowed"].fillna(False)

    suspicious = merged[merged["allowed"]]

    logger.info(f"After allowlist: {len(suspicious)} " f"suspicious IPs remain")
    return suspicious
