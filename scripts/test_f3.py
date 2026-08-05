import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.db import get_conn, insert_events  # noqa: E402

insert_events(
    [
        {
            "ip": "6.6.6.6",
            "event_time": "2026-08-05T12:00",
            "status": 403,
            "severity_score": 9.5,
        }
    ]
)

conn = get_conn()
conn.execute("UPDATE ip_addresses SET is_blocklisted = 1 WHERE ip = ?", ("6.6.6.6",))
conn.commit()
conn.close()

from src.reports import above_average_blocklisted_threats  # noqa: E402

print(above_average_blocklisted_threats())
