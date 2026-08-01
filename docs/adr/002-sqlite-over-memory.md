# ADR 002 — SQLite over In-Memory Storage

## Status
Accepted

## Context
v1 stored all detections in Python dicts in memory. Restart the app and every detection is gone. An IP probing slowly across a week is invisible — and that is exactly the attack a log analyser exists to catch. v2's first feature is a SQLite schema — this step also unblocks v2.

## Decision
Use SQLite (standard library, no server needed) for all scan results, events and alerts.

## Consequences
- History survives restart
- Multi-scan queries possible
- First query v1 could never answer: which IPs appear in more than one scan this week?
- Slightly slower per scan (disk write) — measured, acceptable
- SQLite is single-writer — fine for one scanner, v2 moves to PostgreSQL

## Rejected Alternative
Memory only (Python dict) — loses all history on restart, slow probe across days invisible, the attack that matters most.