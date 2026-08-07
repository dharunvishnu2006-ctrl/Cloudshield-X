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
st.markdown(
    f"- [ADR 001 — Regex over split()]"
    f"({repo_url}/docs/adr/001-regex-parser-over-split.md)\n"
    f"- [ADR 002 — SQLite over memory]"
    f"({repo_url}/docs/adr/002-sqlite-over-memory.md)\n"
    f"- [ADR 003 — Radio page now, multipage at v2]"
    f"({repo_url}/docs/adr/003-radio-page-now-multipage-at-v2.md)\n"
)

st.divider()
st.subheader("⚠️ Known Limits")
st.markdown(
    """
- One log format only — new server needs new regex
- Detection threshold-based — no ML until v4
- SQLite single-writer — v2 moves to PostgreSQL
- No graph of related addresses — v2's attack graph
- Dashboard reads whole table — no pagination yet
- Test coverage — core modules (scanner, versions) tested;
  E1-E15 feature-level tests are a catch-up item for the next session
- mypy debt — charts.py (empty-data return type) and summarise.py
  (response block type narrowing) have known type errors; not fixed yet
"""
)
