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

## v2 Update — Threat Intelligence Engine

### New Data Model (v2)
- `ip_addresses`, `threat_actors`, `security_events` — normalised,
  foreign-key linked (F1)
- `host_links` — attack graph edges, used by F5's recursive CTE
  and F9's graph algorithms

### New Known Limits (v2)
- **SQLite on an ephemeral filesystem** — verified directly: deleting
  the database file and restarting rebuilds cleanly with no crash,
  but every row of data is genuinely lost. On a free hosting tier,
  this happens automatically on every restart. Fixed in v3 with a
  managed PostgreSQL instance.
- `host_links` has no weight column — every edge defaults to weight
  1.0, so Dijkstra's "cheapest route" currently equals BFS's "fewest
  hops." A real CVSS-based weight column is a genuine future addition.