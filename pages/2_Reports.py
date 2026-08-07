import streamlit as st
import pandas as pd
from src.planner import prioritize, greedy_plan

st.title("📋 Reports — Response Planner")
st.caption("Edit the threats below with your own numbers, then compare DP vs greedy")

default_threats = pd.DataFrame(
    [
        {"name": "sql_injection", "risk": 9, "effort": 3},
        {"name": "port_scan", "risk": 4, "effort": 1},
        {"name": "brute_force", "risk": 6, "effort": 2},
    ]
)

edited = st.data_editor(default_threats, num_rows="dynamic", use_container_width=True)

budget = st.slider("Analyst Hours Available", min_value=1, max_value=20, value=5)

if st.button("Compute Response Plan"):
    threats = [
        (row["name"], row["risk"], row["effort"]) for _, row in edited.iterrows()
    ]

    st.divider()
    col1, col2 = st.columns(2)

    dp_total, dp_chosen = prioritize(threats, budget)
    with col1:
        st.subheader("🧠 Dynamic Programming")
        st.metric("Total Risk Reduced", dp_total)
        st.write("Chosen:", ", ".join(dp_chosen))

    greedy_total, greedy_chosen = greedy_plan(threats, budget)
    with col2:
        st.subheader("⚡ Greedy (highest-risk-first)")
        st.metric("Total Risk Reduced", greedy_total)
        st.write("Chosen:", ", ".join(greedy_chosen))

    if dp_total > greedy_total:
        st.warning(
            f"DP found {dp_total - greedy_total} more risk reduction "
            "than greedy — exactly the F11 counterexample in practice."
        )
    else:
        st.info("On this data, greedy happened to match DP.")
