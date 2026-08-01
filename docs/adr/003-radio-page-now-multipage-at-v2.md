# ADR 003 — Radio Page Now, Multipage at v2

## Status
Accepted

## Context
v2's guide puts the Evolution page in pages/3_Evolution.py because v2 converts the whole app to Streamlit multipage. v1.1's app is a single app.py with a sidebar radio. Building multipage now means restructuring the entire app for one new page.

## Decision
Build the Evolution page as a fifth radio branch in v1.1. Write the page body as one function, render_evolution(), so v2 moves it by moving one function. Record this as ADR 003.

## Consequences
- Evolution page ships in v1.1 without restructuring the whole app
- render_evolution() is isolated — v2 lifts it into pages/ with one move
- Consistent with how Dashboard, About pages are structured today
- v2 must do the multipage migration for all pages at once

## Rejected Alternative
Multipage now — would restructure the entire app for one new page, risk breaking Dashboard and About, delay v1.1 shipping.