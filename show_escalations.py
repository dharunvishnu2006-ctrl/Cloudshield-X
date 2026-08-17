from src.db import get_conn
from src.analytics_v2 import escalation_detector

conn = get_conn()
ip_lookup = {
    row["id"]: row["ip"] for row in conn.execute("SELECT id, ip FROM ip_addresses")
}

rows = escalation_detector()
flagged = 0

for row in rows:
    prev = row["prev_severity"]
    curr = row["severity_score"]
    if prev is not None and curr > prev:
        flagged += 1
        ip = ip_lookup.get(row["source_ip"], row["source_ip"])
        print(f"{ip}: {prev} -> {curr} at {row['event_time']}")

print(f"\n{flagged} escalating events out of {len(rows)} total")
