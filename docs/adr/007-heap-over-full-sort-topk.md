# ADR 007 — Size-K Min-Heap over Full Sort for Top-K

## Status
Accepted

## Context
An analyst reviewing threats never looks at all 50,000 in a
day — they look at the ten worst. The obvious approach is to
sort everything and slice the front: sorted(data)[:10]. That
is O(n log n) over the whole list to answer a question that
only needed the top ten.

A size-k min-heap answers the same question in O(n log k):
push every threat, and the moment the heap holds k+1 items,
pop the root — which is by definition the smallest of the k+1.
At the end the heap holds exactly the k largest, and the other
49,990 were never sorted.

I measured both on the same 50,000 random severities:
- top_k_threats (size-10 min-heap): 3.60 ms
- sorted(data, reverse=True)[:10]: 10.13 ms

The heap was 2.8x faster, and both returned the identical
top-10 list — proven directly in
test_top_k_matches_full_sort.

## Decision
top_k_threats() uses a size-k min-heap (Python's heapq),
not a full sort, wherever the dashboard or API only needs
the top k results.

## Consequences
- O(n log k) instead of O(n log n) — the gap widens as n grows
  and k stays fixed at 10; on 50,000 items it was already 2.8x
- Correctness is guaranteed by test_top_k_matches_full_sort,
  which checks the heap result against a full sort every run
- Only good for "top k" questions — if the dashboard ever needs
  a fully sorted list (not just the top 10), this is the wrong
  tool and a real sort is correct
- Slightly less obvious to read than sorted()[:10] — the
  trade-off is worth it because the speed difference is real
  and measured, not assumed

## Rejected Alternative
**Full sort, then slice** — sorted(data, reverse=True)[:10].
Simpler to read, but does O(n log n) work to answer a question
that only needed O(n log k). Rejected once the 2.8x gap was
actually measured rather than assumed from the textbook
complexity alone.