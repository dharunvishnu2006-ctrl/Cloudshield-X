import streamlit as st
import pandas as pd
import altair as alt
from src.scanner import CloudShieldScanner
from src.log_reader import read_logs
from src.ip_detector import detect_suspicious_ips
from src.alert_system import raise_alerts
from src.report_generator import generate_report

st.set_page_config(
    page_title="CloudShield X",
    page_icon="",
    layout="wide"
)

st.title("CloudShield X — Security Log Analyzer")
st.caption("v1 of 6 | CSPM Platform | Built by J. Dharun Vishnu")
st.sidebar.title("CloudShield X")
st.sidebar.caption("CSPM Platform — v1")

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Analytics", "Reports", "About"]
)

if page == "Dashboard":
    st.subheader("Live Stats")
    col1, col2, col3 = st.columns(3)
    m1 = col1.empty()
    m2 = col2.empty()
    m3 = col3.empty()

    m1.metric("Total Logs Scanned", "0")
    m2.metric("Suspicious IPs", "0")
    m3.metric("Alerts Raised", "0")

    st.divider()
    st.subheader("Upload server Log")
    uploaded_file = st.file_uploader("choose a .log file", type=["log", "txt"])

    if uploaded_file is not None:
        temp_path = "data/uploaded_log.log"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File uploaded! Scanning...")
        logs = read_logs(temp_path)
        suspicious = detect_suspicious_ips(logs, threshold=3)
        alerts = raise_alerts(suspicious)
        report_path = generate_report(suspicious)

        st.success(f"Scan Completed! Report saved to: {report_path}")

        m1.metric("Total Logs Scanned", len(logs))
        m2.metric("Suspicious IPs", len(suspicious))
        m3.metric("Alerts Raised", len(alerts))

        with open(report_path, "rb") as f:
            st.download_button(
                label="Download Security Report (CSV)",
                data=f,
                file_name="security_report.csv",
                mime="text/csv"
        )    

        if suspicious:
            st.divider()
            st.subheader("Failed Login Attempts by IP")

            chart_data = pd.DataFrame({
                "IP": list(suspicious.keys()),
                "Failed Attempts": list(suspicious.values())
            })

            chart = alt.Chart(chart_data).mark_bar().encode(
                x="IP",
                y="Failed Attempts"
                
            )
            st.altair_chart(chart, use_container_width=True)

elif page == "About":
    st.subheader("About Cloudshield X")
    st.write("""
    **CloudShield X** is an open-source Cloud Security Posture 
    Management (CSPM) platform, built from scratch in Python.
    
    This is **v1 of 6** — the foundation layer, focused on 
    server log analysis and brute-force detection.
    """)

    st.markdown("### Tech Stack")
    st.markdown("`Python` `Pandas` `NumPy` `Streamlit` `pytest` `Git`")

    st.markdown("### Links")
    st.markdown("[GitHub Repo](https://github.com/dharunvishnu2006-ctrl/cloudshield-x-v1)")