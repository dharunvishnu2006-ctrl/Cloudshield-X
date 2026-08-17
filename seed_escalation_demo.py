from src.db import insert_events

rows = [
    {
        "ip": "203.0.113.99",
        "event_time": "2026-08-17T10:00:00",
        "event_type": "probe",
        "status": 200,
        "severity_score": 3.0,
    },
    {
        "ip": "203.0.113.99",
        "event_time": "2026-08-17T10:05:00",
        "event_type": "probe",
        "status": 401,
        "severity_score": 5.0,
    },
    {
        "ip": "203.0.113.99",
        "event_time": "2026-08-17T10:10:00",
        "event_type": "exploit",
        "status": 403,
        "severity_score": 9.0,
    },
]

n = insert_events(rows)
print(f"Inserted {n} escalating demo events for 203.0.113.99")
