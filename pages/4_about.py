import streamlit as st

st.subheader("ℹ️ About CloudShield X")
st.write(
    """
    **CloudShield X** is an open-source Cloud Security
    Posture Management (CSPM) platform, built from
    scratch in Python — every line typed by hand.

    **v1.1** closed the audit: 80 of 80 roadmap steps
    built, three real defects fixed.

    **v2** adds the threat intelligence engine: a
    normalised SQLite schema, ten graph algorithms,
    dynamic programming, and a real REST API.
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
    "`SQLite` `Streamlit` `pytest` `Flask`"
)

st.markdown("### 🔗 Links")
st.markdown("[GitHub](https://github.com/dharunvishnu2006-ctrl/Cloudshield-X)")
