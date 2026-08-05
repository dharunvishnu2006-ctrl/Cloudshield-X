import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.db import insert_events  # noqa: E402
from src.analytics_v2 import rank_within_type  # noqa: E402

insert_events(
    [
        {
            "ip": "50.50.50.1",
            "event_time": "2026-08-05T13:00",
            "event_type": "sql_injection",
            "severity_score": 7.0,
        },
        {
            "ip": "50.50.50.2",
            "event_time": "2026-08-05T13:01",
            "event_type": "sql_injection",
            "severity_score": 9.0,
        },
        {
            "ip": "50.50.50.3",
            "event_time": "2026-08-05T13:02",
            "event_type": "port_scan",
            "severity_score": 3.0,
        },
        {
            "ip": "50.50.50.4",
            "event_time": "2026-08-05T13:03",
            "event_type": "port_scan",
            "severity_score": 5.0,
        },
    ]
)

for row in rank_within_type(limit=100):
    if row["event_type"] in ("sql_injection", "port_scan"):
        print(row)
