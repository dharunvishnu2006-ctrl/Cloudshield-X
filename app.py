import streamlit as st
from src.logging_setup import setup_logging, generate_run_id
from src.reader import read_events
from src.analytics import (
    compute_request_stats,
    flag_suspicious_numpy,
    analyse_events,
)
from src.charts import plot_request_distribution, plot_interactive_top_ips
from src.store import init_db
from src.versions import load_versions, feature_lines, bug_lines, total_roadmap_steps


def render_evolution():
    st.title("🗺️ How CloudShield X Grew")
    st.caption("Every number on this page comes from versions.json")

    try:
        versions = load_versions()
    except FileNotFoundError as e:
        st.error(f"versions.json missing: {e}")
        return

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
    st.markdown(
        "- [ADR 001 — Regex over split()]"
        "(docs/adr/001-regex-parser-over-split.md)\n"
        "- [ADR 002 — SQLite over memory]"
        "(docs/adr/002-sqlite-over-memory.md)\n"
        "- [ADR 003 — Radio page now, multipage at v2]"
        "(docs/adr/003-radio-page-now-multipage-at-v2.md)\n"
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
    """
    )


setup_logging()
init_db()

st.set_page_config(page_title="CloudShield X v1.1", page_icon="🛡️", layout="wide")

st.title("🛡️ CloudShield X — Security Log Analyzer")
st.caption("v1.1 | CSPM Platform | Built by J. Dharun Vishnu")

st.sidebar.title("🛡️ CloudShield X")
st.sidebar.caption("CSPM Platform - v1.1")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "📊 Analytics", "📄 Reports", "🗺️ Evolution", "ℹ️ About"],
)

st.sidebar.divider()
threshold = st.sidebar.slider("Detection Threshold", min_value=1, max_value=20, value=3)

if page == "🏠 Dashboard":
    st.subheader("📁 Upload Server Log")
    uploaded_file = st.file_uploader("Choose a .log file", type=["log", "txt"])

    if uploaded_file is not None:
        run_id = generate_run_id()
        temp_path = "data/uploaded_log.log"

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Scanning..."):
            events = list(read_events(temp_path, run_id))
            stats = compute_request_stats(events)
            grouped = analyse_events(events)
            suspicious = flag_suspicious_numpy(events, threshold=threshold)

        st.divider()
        st.subheader("📊 Live Stats")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Events", len(events))
        col2.metric("Unique IPs", len(grouped))
        col3.metric("Suspicious IPs", len(suspicious))
        col4.metric("p95 Threshold", f"{stats.get('p95', 0):.1f}")

        st.divider()
        st.subheader("🔍 Top Offending IPs")
        plotly_fig = plot_interactive_top_ips(grouped)
        if plotly_fig:
            st.plotly_chart(plotly_fig, use_container_width=True)

        st.divider()
        st.subheader("📈 Distribution Analysis")
        dist_fig = plot_request_distribution(grouped)
        if dist_fig:
            st.pyplot(dist_fig, transparent=True)

        if suspicious:
            st.divider()
            st.subheader("🚨 Suspicious IPs Detected")
            st.error(f"⚠️ {len(suspicious)} suspicious IPs found!")
            for ip in suspicious:
                st.write(f"🔴 `{ip}`")

elif page == "🗺️ Evolution":
    render_evolution()

elif page == "ℹ️ About":
    st.subheader("ℹ️ About CloudShield X")
    st.write(
        """
        **CloudShield X** is an open-source Cloud Security
        Posture Management (CSPM) platform, built from
        scratch in Python — every line typed by hand.

        **v1.1** closes the audit: 80 of 80 roadmap steps
        built, three real defects fixed.
        """
    )

    st.markdown("### 🐛 Bugs Fixed in v1.1")
    st.markdown(
        """
        - **Parser bug** — `split()` broke on quoted fields;
          regex with named groups fixed it
        - **No persistence** — restart lost all detections;
          SQLite now survives restarts
        - **print() logging** — replaced with structured
          JSON logging + run_id tracing
        """
    )

    st.markdown("### 🔧 Tech Stack")
    st.markdown(
        "`Python` `Pydantic` `NumPy` `Pandas` "
        "`Matplotlib` `Seaborn` `Plotly` "
        "`SQLite` `Streamlit` `pytest`"
    )

    st.markdown("### 🔗 Links")
    st.markdown("[GitHub](https://github.com/dharunvishnu2006-ctrl/Cloudshield-X)")
