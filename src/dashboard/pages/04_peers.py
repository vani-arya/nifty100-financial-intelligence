import streamlit as st

st.title("👥 Peer Comparison")

st.markdown("""
Compare companies against peer groups using percentile rankings.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Peer Groups", 11)

with col2:
    st.metric("Mapped Companies", 56)

with col3:
    st.metric("Percentile Records", 550)

peer_group = st.selectbox(
    "Select Peer Group",
    [
        "Automobiles",
        "Consumer Finance",
        "FMCG",
        "IT Services",
        "Life Insurance",
        "Oil & Gas",
        "Pharmaceuticals",
        "Power & Utilities",
        "Private Banks",
        "Public Sector Banks",
        "Steel"
    ]
)

st.success(
    f"Selected Group: {peer_group}"
)

st.info(
    "Radar charts and percentile benchmarking will be added in upcoming Sprint 4 tasks."
)

st.caption("Sprint 4 - Day 22 Scaffold")