def detect_suspicious_ips(logs: list, threshold: int = 3) -> dict:
    """Return {ip: fail_count} for IPs over the threshold."""
    counts: dict[str, int] = {}
    result: dict[str, int] = {}
    for log in logs:
        if log["status"] == "401" or log["status"] == "403":
            ip = log["ip"]
            counts[ip] = counts.get(ip, 0) + 1
    for ip, count in counts.items():
        if count >= threshold:
            result[ip] = count
    return result
