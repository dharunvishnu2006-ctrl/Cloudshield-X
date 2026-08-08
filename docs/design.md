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

### Trade-offs (v2)

1. **SQLite over PostgreSQL** — chose SQLite because it needed no
   new tool before its teaching step (155), and it measured well:
   50,000 inserts in 0.199 s, single-IP lookup 30x faster once
   indexed. Gave up: real concurrent writers, FULL OUTER JOIN.
   (ADR 005)

2. **Own graph code over NetworkX** — chose to write BFS, Dijkstra,
   Bellman-Ford, Floyd-Warshall and Union-Find by hand because
   Steps 102-110 and 124 exist to teach the algorithms, not a
   library's API. Gave up: NetworkX's battle-tested edge-case
   handling at large scale. (ADR 006)

3. **Size-k heap over full sort for top-K** — chose the heap
   because it only does O(n log k) work for a question that only
   needed the top 10. Measured 3.60 ms vs 10.13 ms on 50,000
   items — 2.8x faster. Gave up: a little readability next to
   sorted(...)[:10]. (ADR 007)

4. **Recursive CTE (F5) vs Python BFS (F9) for reachability** —
   both answer "what can this host reach," from two different
   layers. Measured on the same 500-host graph: Python BFS 2.27 ms,
   recursive CTE 2.51 ms — BFS won, by a small margin. Kept both:
   the CTE lives inside SQL for F5's propagation trace, the BFS
   lives in Python for F9 because it needs to feed Dijkstra and
   Union-Find, which are not SQL's job. Neither replaces the other.

### Known Limits (v2)

- **No FULL OUTER JOIN in SQLite** — F3's feed reconciliation
  emulates it with two LEFT JOINs and a UNION. Fixed in v3 with
  PostgreSQL, which has FULL OUTER JOIN natively.
- **SQLite on an ephemeral filesystem** — verified directly: deleting
  the database file and restarting rebuilds cleanly with no crash,
  but every row of data is genuinely lost. On a free hosting tier,
  this happens automatically on every restart. Fixed in v3 with a
  managed PostgreSQL instance.
- **`host_links` has no weight column** — every edge defaults to
  weight 1.0, so Dijkstra's "cheapest route" currently equals BFS's
  "fewest hops." A real CVSS-based weight column is a genuine
  future addition.
- **Attack graph held entirely in memory** — fine at the host
  counts this version targets, but would not scale to 100,000
  hosts without a different storage strategy. Not yet scheduled
  in the roadmap — revisit if a project's host count grows that
  large.
- **Floyd-Warshall is O(V³)** — measured fine on this version's
  graphs, but becomes unusable past roughly 2,000 hosts. Same
  status as above — a real algorithmic ceiling, not currently
  scheduled to be replaced.
- **No authentication on the API** — anyone who can reach an
  endpoint can call it. Not yet scheduled by name, but a natural
  fit once v4 formalises deployment with FastAPI and Docker.
- **Severity is rule-based, not learned** — `stage_enrich` assigns
  severity from a fixed if/else on status code, not from data.
  Fixed in v4, which is exactly where ML models enter the roadmap.

### Deployment Lessons (v2)

- **Case-sensitive filenames** — `pages/4_about.py` (lowercase) was
  staged and pushed as `pages/4_About.py` (capital A) in git commands.
  Windows' case-insensitive filesystem hid this locally; GitHub's
  Linux servers are case-sensitive, so the file silently never
  reached the repository. Found only through real cloud deployment.
  Lesson: verify a file's exact real name with `dir`/`ls` before
  trusting a git command that references it by a typed path.
- **v1.1 and v2 schemas both need initializing on startup** —
  `app.py` originally called only `src.store.init_db()` (v1.1's
  alerts table). `src.db.init_db()` (v2's real schema) was never
  called at all, invisible locally because the dev database already
  had v2's tables from manual testing. A genuinely fresh cloud
  deployment exposed the missing call immediately.