# ADR 008 — Dynamic Programming over Greedy for the Response Planner

## Status
Accepted

## Context
The response planner picks which threats to fix inside a
limited number of analyst hours — classic 0/1 knapsack: each
threat has a risk value and an effort cost, and each one is
either taken whole or left out.

Greedy — sort by risk, take the highest first, stop when the
budget runs out — is fast and simple, and it feels correct.
I tested it directly against the DP table on a real case:

    threats = [("A", risk=5, effort=4),
               ("B", risk=4, effort=3),
               ("C", risk=3, effort=2)]
    budget  = 5

Greedy sees A has the highest risk (5), takes it, and the
remaining budget (1) is too small for B or C. Total: 5.

DP checks every combination the budget allows. B + C together
cost 5 effort and are both affordable — total risk 4 + 3 = 7.
DP finds this; greedy never considers it, because once A is
taken greedy never looks back.

    dp_total = 7, greedy_total = 5, dp_total > greedy_total

This is now a permanent test — test_dp_beats_greedy — not a
one-off finding I could lose track of.

## Decision
prioritize() uses 0/1 knapsack dynamic programming as the
real response planner. greedy_plan() is kept in the codebase
as a second function, specifically so the two can be compared
and the counter-example stays runnable.

## Consequences
- Analyst gets the actual best plan under budget, not a
  plausible-looking one — 7 vs 5 is a 40% gap on this example
- DP is O(n * budget) — more expensive than greedy's O(n log n)
  sort, but the budgets here are small enough that this cost
  is not a real concern
- The table has to be walked backwards to recover which
  threats were chosen — a total number alone tells an analyst
  nothing actionable
- greedy_plan() stays in the codebase deliberately, as a
  permanent counter-example rather than dead code

## Rejected Alternative
**Greedy (highest-risk-first)** — faster, simpler, and wrong
on a case as small as three threats. Rejected with a real
counter-example in hand, not a theoretical objection — the
exact numbers are locked into test_dp_beats_greedy so this
finding cannot be forgotten or misremembered later.