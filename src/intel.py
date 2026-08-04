import requests  # type: ignore[import-untyped]
import os
from datetime import datetime, timezone
from src.logging_setup import get_logger
from src.store import get_connection

logger = get_logger("intel")

TIMEOUT = 5
UNAVAILABLE = "UNAVAILABLE"


def get_ip_reputation(ip: str) -> str:
    cached = _check_cache(ip)
    if cached:
        logger.info(f"Cache hit for {ip}")
        return cached
    result = _fetch_reputation(ip)
    _save_cache(ip, result)
    return result


def _check_cache(ip: str) -> str | None:
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT result FROM intel_cache "
                "WHERE ip = ? AND cached_at >= "
                "datetime('now', '-1 day')",
                (ip,),
            )
            row = cursor.fetchone()
            if row:
                return row["result"]
    except Exception as e:
        logger.error(f"Cache check failed: {e}")
    return None


def _save_cache(ip: str, result: str) -> None:
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO intel_cache "
                "(ip, result, cached_at) VALUES (?, ?, ?)",
                (ip, result, datetime.now(timezone.utc).isoformat()),
            )
    except Exception as e:
        logger.error(f"Cache save failed: {e}")


def _fetch_reputation(ip: str) -> str:
    try:
        api_key = os.environ.get("ABUSEIPDB_KEY", "")
        if not api_key:
            logger.warning("No API key found — " "returning UNAVAILABLE")
            return UNAVAILABLE

        url = "https://api.abuseipdb.com/api/v2/check"
        headers = {"Key": api_key, "Accept": "application/json"}
        params: dict[str, str | int] = {"ipAddress": ip, "maxAgeInDays": 90}

        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            score = data["data"]["abuseConfidenceScore"]
            return "MALICIOUS" if score > 50 else "CLEAN"
        else:
            logger.warning(f"API returned " f"{response.status_code} for {ip}")
            return UNAVAILABLE

    except Exception as e:
        logger.error(f"Reputation fetch failed: {e}")
        return UNAVAILABLE
