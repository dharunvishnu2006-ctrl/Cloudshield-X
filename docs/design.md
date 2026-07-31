# CloudShield X — Design Document

## §1 Problem

Every UPI app, Zomato/Swiggy backend, and bank server writes
millions of log lines daily. Hidden in them are brute-force
logins and attackers probing endpoints. CloudShield X reads
those logs and catches them automatically.

## §2 Requirements (with measured numbers)

- Parse Apache/nginx Combined Log Format correctly
- Detect brute-force IPs above p95 threshold
- Persist all detections across restarts (SQLite)
- Stream files larger than RAM (generator pipeline)
- Dashboard readable in light AND dark theme

## §3 Data Model

- `scans` table — one row per scan run
- `events` table — one row per log line (FK to scans)
- `alerts` table — one row per suspicious IP (FK to scans)
- `intel_cache` table — reputation cache (1 day TTL)

## §4 Trade-offs

1. **regex over split()** — correctness over simplicity
2. **SQLite over memory** — history over speed
3. **generators over readlines()** — memory over simplicity
4. **p95 over fixed threshold** — data-driven over guessing
5. **async for I/O** — measured, not assumed

## §5 Known Limits

- One log format only — new server needs new regex
- Detection is threshold-based — no ML (v4)
- SQLite single-writer — fine for one scanner (v2 moves on)
- No graph of related addresses yet (v2's attack graph)
- Dashboard reads whole table — no pagination