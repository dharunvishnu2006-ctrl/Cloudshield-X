import streamlit as st
from src.versions import load_versions, feature_lines, bug_lines
from src.versions import total_roadmap_steps

st.title("🗺️ How CloudShield X Grew")
st.caption("Every number on this page comes from versions.json")

try:
    versions = load_versions()
except FileNotFoundError as e:
    st.error(f"versions.json missing: {e}")
    st.stop()

shipped = [v for v in versions if v["status"] == "shipped"]

st.divider()
st.subheader("📅 Version Timeline")
grand_total = total_roadmap_steps(versions)
st.caption(f"Total roadmap: {grand_total} steps across {len(versions)} versions")

cols = st.columns(len(versions))
for i, v in enumerate(versions):
    is_shipped = v["status"] == "shipped"
    with cols[i]:
        if is_shipped:
            st.markdown(
                f"<div style='background-color:{v['colour']};"
                f"padding:8px;border-radius:6px;"
                f"text-align:center;color:white;'>"
                f"<b>{v['version']}</b><br/>"
                f"{v['completion']}%<br/>"
                f"<span style='font-size:0.75em'>"
                f"{v['steps_covered']}/{grand_total} steps</span></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='border:3px dashed {v['colour']};"
                f"padding:8px;border-radius:6px;"
                f"text-align:center;color:{v['colour']};'>"
                f"<b>{v['version']}</b><br/>"
                f"{v['steps']}</div>",
                unsafe_allow_html=True,
            )
st.divider()
st.caption(
    "🟦 v1 + v1.1 shipped · 🟩 v2 · 🟧 v3 · 🩷 v4 · 🟪 v5 · 🟢 v6 · dashed = planned"
)

st.divider()
st.subheader("🔍 Version Detail")

for v in shipped:
    n_feat = len(v["features"])
    n_bugs = len(v["bugs_fixed"])
    header = (
        f"{v['version']} — {v['steps_covered']} steps, "
        f"{n_feat} features, {v['tests']} tests, {n_bugs} bugs fixed"
    )
    with st.expander(header):
        st.markdown("**Features:**")
        st.markdown("\n".join(feature_lines(v)))
        if v["bugs_fixed"]:
            st.markdown("**Bugs Fixed:**")
            st.markdown("\n".join(bug_lines(v)))

st.divider()
st.subheader("📝 Decisions (ADRs)")
repo_url = "https://github.com/dharunvishnu2006-ctrl/Cloudshield-X/blob/main"
adrs = [
    ("001", "Regex over split()", "001-regex-parser-over-split.md"),
    ("002", "SQLite over memory", "002-sqlite-over-memory.md"),
    ("003", "Radio page now, multipage at v2", "003-radio-page-now-multipage-at-v2.md"),
    (
        "004",
        "Dashboard calls engine directly",
        "004-dashboard-calls-engine-directly.md",
    ),
    ("005", "SQLite over PostgreSQL for v2", "005-sqlite-over-postgresql.md"),
    ("006", "Own graph implementation over NetworkX", "006-own-graph-over-networkx.md"),
    ("007", "Size-k heap over full sort for top-K", "007-heap-over-full-sort-topk.md"),
    (
        "008",
        "DP over greedy for response planner",
        "008-dp-over-greedy-response-planner.md",
    ),
]
for number, title, filename in adrs:
    st.markdown(f"- [ADR {number} — {title}]({repo_url}/docs/adr/{filename})")

st.divider()
st.subheader("⚠️ Known Limits")
st.markdown(
    """
- One log format only — new server needs new regex
- No FULL OUTER JOIN in SQLite — F3 emulates it with two
  LEFT JOINs and a UNION; native in v3's PostgreSQL
- SQLite on an ephemeral filesystem — verified directly,
  data is lost on every restart on a free hosting tier
- host_links has no weight column — Dijkstra's cheapest
  route currently equals BFS's fewest hops
- Attack graph held entirely in memory — fine at this
  version's scale, not built for 100,000 hosts
- Floyd-Warshall is O(V³) — unusable past ~2,000 hosts
- No authentication on the API — a natural fit for v4
- Severity is rule-based, not learned — fixed in v4
- Dashboard reads whole table — no pagination yet
"""
)
