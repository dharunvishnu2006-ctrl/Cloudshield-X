# ADR 005 — SQLite over PostgreSQL for v2

## Status
Accepted

## Context
v2 needed a real relational store for normalised threat data —
three tables, foreign keys, indexes, joins, recursive CTEs.
PostgreSQL is a natural fit for that on paper. But PostgreSQL
is Step 155 and SQLAlchemy is Step 158 — both taught after v2's
boundary at Step 153. Using either here would mean defending a
tool in an interview that this version never actually taught me.

Before ruling it out on that basis alone, I measured whether
SQLite could actually carry the load v2 needed:
- 50,000 event inserts completed in 0.199 s
- A single-IP profile query (F1/F3's core lookup) dropped from
  2.925 ms (full SCAN) to 0.098 ms (SEARCH USING INDEX) once the
  (source_ip, event_time) index existed — a real 30x

SQLite's limits also showed up honestly during the build:
it has no FULL OUTER JOIN, so F3's feed reconciliation had to
emulate one with two LEFT JOINs and a UNION. And it is a
single-writer database — fine for one scanner process, not
fine for concurrent writers.

## Decision
Stay on SQLite for the whole of v2. Move to PostgreSQL in v3,
once SQLAlchemy is actually taught (Step 158).

## Consequences
- No new tool introduced before it was taught — defensible
- Measured proof the choice wasn't just "the only thing I know" —
  it held up under 50k rows with real query-time evidence
- No FULL OUTER JOIN — emulated with UNION, documented as a
  known limit (design.md §6)
- Single writer — acceptable for one scanner, not for concurrent
  ingestion; this becomes v3's reason to move on
- SQLite's file is ephemeral on free hosting tiers — found and
  documented during Phase 12 deployment

## Rejected Alternative
**PostgreSQL, via SQLAlchemy** — both taught after Step 153.
Using them now would violate the availability rule this whole
roadmap is built on, and I could not defend the choice under
questioning about how connection pooling or migrations work,
because I have not been taught either yet. v3 is exactly the
version that adds this properly.