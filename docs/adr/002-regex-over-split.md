# ADR 002 — Regex over split()

## Status
Accepted

## Context
v1 parsed log lines using split() on spaces. Every
real log format (Apache Combined, nginx) wraps the
user agent and request in quotes — and those quoted
fields contain spaces. The columns shift and every
value after the quoted field is wrong — silently.

This is a live bug. Running both parsers over the
same file, they disagreed on multiple lines.

## Decision
Use a compiled regex with named groups:
- (?P<ip>\S+) — correct regardless of field position
- (?P<request>[^"]+) — captures quoted fields correctly
- Compiled once at module level — not per line

## Consequences
- Parses real Apache/nginx logs correctly ✅
- Named groups = self-documenting code ✅
- Position-independent = format changes safe ✅
- Slightly more complex than split() — worth it

## Rejected Alternative
**split() on spaces**
- Broke on any quoted field containing spaces
- Disagreed with regex on lines in our own test log
- Silent wrong counts — worst kind of bug