# ADR 004 — Dashboard calls the engine directly, not through the API

## Context
v2 built a full REST API (Phase 8) exposing every engine
function — /threats, /graph/paths, /plan, and more. The
Streamlit dashboard (Phase 10) also needs this same data.
There are two ways to connect them: the dashboard could make
HTTP requests to the Flask API, or it could import the engine
functions directly, the same way the API routes do.

## Decision
The dashboard imports and calls engine functions directly
(`top_attackers()`, `graph.dijkstra()`, `prioritize()`, etc.),
the same functions the API routes call. It does not make HTTP
requests to `localhost:5000` or any deployed API URL.

## Rejected — and why
Running the Flask API as a second, separately deployed service
(e.g. on Render or Railway) was considered. Rejected for v2
specifically because: it requires a second hosting account and
a second live URL to keep working; on a free tier, if that
second service sleeps, the dashboard would silently break even
though the dashboard's own engine calls would still work fine;
and it adds real deployment complexity for no functional gain,
since the dashboard and the API already share the exact same
Python engine code in the exact same repository.

## Consequences
The API is genuinely real, tested (33+ tests), and fully
documented at /apidocs — it is not decorative. It exists so
other systems and developers could integrate with CloudShield
X, and it is demonstrated with curl and the Swagger UI, exactly
as this decision requires. What this decision makes harder:
if the dashboard and the API were ever split onto separate
hosts in a later version, the dashboard's data-fetching code
would need to change from direct function calls to HTTP
requests — a real migration cost, accepted deliberately here
in exchange for a simpler, working v2.

## Status
Accepted for v2. Revisit in v4, where FastAPI and Docker make
running two properly separated services genuinely practical.