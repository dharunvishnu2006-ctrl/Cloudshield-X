# ADR 006 — Own Graph Implementation over NetworkX

## Status
Accepted

## Context
F9 needed ten graph algorithms: adjacency list/matrix
representation, BFS, DFS with backtracking, Dijkstra,
Bellman-Ford, Floyd-Warshall, Kruskal's MST, Union-Find,
and topological sort. NetworkX implements all of these,
production-tested, in a few import lines.

But NetworkX was never taught anywhere in the roadmap.
Steps 102-110 and 124 exist specifically to teach these
algorithms by building them, not by calling them. Using a
library here would satisfy the checklist on paper while
skipping the actual skill the steps were for.

I measured my own BFS against SQLite's native recursive CTE
on the same 500-host, 1500-link graph, to see whether "written
by hand" also meant "written slow":
- Python BFS (my adjacency-list graph, in memory): 2.27 ms
- Recursive CTE (SQLite, same reachability question): 2.51 ms

My own code was not the slow option.

## Decision
Write attack_graph.py entirely by hand — adjacency list,
BFS, DFS+backtracking, Dijkstra, Bellman-Ford, Floyd-Warshall,
Kruskal's MST via Union-Find, topological sort. No graph
library, anywhere in v2.

## Consequences
- Can explain every algorithm line by line under questioning —
  "the library does it" is not an answer I can give
- test_dijkstra_beats_bfs_on_weights and test_no_path_when_isolated
  test my own logic directly, not a wrapper around someone else's
- More code, more edge cases to handle myself — Union-Find needed
  path compression and union by rank written by hand, not imported
- No NetworkX hardening for pathological graphs — acceptable at
  the host counts this version targets (design.md §6 covers the
  memory limit at scale)
- My own BFS measured faster than SQLite's recursive CTE on the
  same question — being handwritten did not mean being slow

## Rejected Alternative
**NetworkX** — mature, well-tested, and would have made F9
trivial to "complete." Rejected because it was never taught,
and because completing the checklist without writing the
algorithms defeats the entire purpose of Steps 102-110 and 124.
This version exists to prove I can build these myself.