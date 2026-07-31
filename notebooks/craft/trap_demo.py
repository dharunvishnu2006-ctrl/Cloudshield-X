def add_alert(alert, alerts=[]):
    alerts.append(alerts)
    return alerts


result1 = add_alert("IP: 203.0.113.45")
print("Call 1:", result1)

result2 = add_alert("IP: 117.55.8.20")
print("Call 2:", result2)

print("Same list?", result1 is result2)


def add_alert_fixed(alert, alerts=None):
    if alerts is None:
        alerts = []
    alerts.append(alert)
    return alerts


result3 = add_alert_fixed("IP: 203.0.113.45")
print("Fixed Call 1:", result3)

result4 = add_alert_fixed("IP: 117.55.8.20")
print("Fixed Call 2:", result4)

print("Same list?", result3 is result4)

from src.models import Alert
from dataclasses import dataclass

alerts = [
    Alert(
        ip="203.0.113.45",
        reason="brute force",
        count=5,
        severity="high",
        at="2026-07-29",
    ),
    Alert(
        ip="117.55.8.20", reason="scanning", count=2, severity="low", at="2026-07-29"
    ),
    Alert(
        ip="49.205.10.8",
        reason="rate limit",
        count=8,
        severity="critical",
        at="2026-07-29",
    ),
]

severity_order = {"low": 1, "medium": 2, "high": 3, "critical": 4}

sorted_alerts = sorted(alerts, key=lambda a: severity_order[a.severity], reverse=True)

for a in sorted_alerts:
    print(f"{a.severity}: {a.ip}")

# RECURSION (Step 17)
import json
from pathlib import Path

config = {
    "thresholds": {"brute_force": 3, "rate_limit": 100},
    "paths": {"logs": {"apache": "/var/log/apache2", "nginx": "/var/log/nginx"}},
}


def walk_config(data, prefix=""):
    if not isinstance(data, dict):
        print(f"{prefix} = {data}")
        return
    for key, value in data.items():
        walk_config(value, prefix=f"{prefix}.{key}")


walk_config(config)

from src.models import LogEvent

events = [
    LogEvent(
        ip="203.0.113.45",
        timestamp="2026-07-29",
        method="POST",
        path="/api/login",
        status=401,
        user_agent="Mozilla",
    ),
    LogEvent(
        ip="49.205.10.8",
        timestamp="2026-07-29",
        method="GET",
        path="/api/orders",
        status=200,
        user_agent="Chrome",
    ),
    LogEvent(
        ip="117.55.8.20",
        timestamp="2026-07-29",
        method="POST",
        path="/api/login",
        status=403,
        user_agent="curl",
    ),
]

failed_v1 = []
for e in events:
    if e.status in (401, 403):
        failed_v1.append(e.ip)
print("v1 style:", failed_v1)

failed_v11 = [e.ip for e in events if e.status in (401, 403)]
print("v1.1 style:", failed_v11)
