# ADR 001 — SQLite over In-Memory Storage

## Status
Accepted

## Context
v1 stored all detections in Python dicts in memory.
Restart the app and every detection is gone. An IP
probing slowly across a week is invisible — and that
is exactly the attack a log analyser exists to catch.

## Decision
Use SQLite (standard library, no server needed) for
all scan results, events and alerts.

## Consequences
- History survives restart ✅
- Multi-scan queries possible ✅
- First query v1 could never answer: which IPs appear
  in more than one scan this week? ✅
- Slightly slower per scan (disk write) — measured,
  acceptable

## Rejected Alternative
**Memory only (Python dict)**
- Gave up: all history on restart
- A slow probe across days is invisible
- This is the attack that matters most