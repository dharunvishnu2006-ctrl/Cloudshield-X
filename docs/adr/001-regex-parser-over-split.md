# ADR 001 — Regex Parser over split()

## Status
Accepted

## Context
v1 parsed log lines using `split()` on spaces. Every real log format (Apache Combined, nginx) wraps the request and user agent in quotes — and those quoted fields contain spaces.

The actual log line where they disagreed:
192.168.1.1 - - [16/Jun/2026] "GET /api/login HTTP/1.1" 401 512 "Mozilla/5.0 (compatible; MSIE 6.0)"

split() output (wrong) — 13 parts, fields shifted, status at wrong index.
Regex output (correct) — named groups, status='401', request='GET /api/login HTTP/1.1'.

## Decision
Compiled regex with named groups — compiled once at module level, not per line.

## Consequences
- Parses real Apache/nginx logs correctly
- Named groups = self-documenting, position-independent
- The bug is now a test: test_regex_parses_quoted_user_agent
- More complex than split() — regex syntax to learn
- Slightly slower per 1M lines — measured, acceptable

## Rejected Alternative
split() on spaces — broke on any quoted field, silent wrong counts, worst kind of bug.