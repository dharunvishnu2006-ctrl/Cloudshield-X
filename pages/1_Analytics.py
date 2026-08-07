import streamlit as st
from src.attack_graph import load_graph_from_db

st.title("📊 Analytics — Attack Graph Viewer")
st.caption("Every host and path below comes from host_links, live")

graph = load_graph_from_db()
available_hosts = sorted(graph.adjacency.keys())

if not available_hosts:
    st.info("No hosts in host_links yet — seed some connections first.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    source = st.selectbox("Source host", available_hosts)
with col2:
    target = st.selectbox(
        "Target host", available_hosts, index=len(available_hosts) - 1
    )

if st.button("Find Attack Paths"):
    st.divider()

    dfs_path = graph.dfs(source, target)
    st.subheader("🔍 A Valid Path (DFS)")
    if dfs_path:
        st.success(" → ".join(dfs_path))
    else:
        st.warning(f"No path found from {source} to {target}.")

    dijkstra_path, cost = graph.dijkstra(source, target)
    st.subheader("💰 Cheapest Path (Dijkstra)")
    if dijkstra_path:
        st.success(" → ".join(dijkstra_path))
        st.metric("Total Cost", cost)
    else:
        st.warning(f"No path found from {source} to {target}.")
