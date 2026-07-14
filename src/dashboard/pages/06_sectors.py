import streamlit as st
from src.dashboard.utils.db import get_sectors

st.title("🏭 Sector Analysis")

sectors = get_sectors()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Companies",
        len(sectors)
    )

with col2:
    st.metric(
        "Broad Sectors",
        sectors["broad_sector"].nunique()
    )

st.subheader("Sector Distribution")

sector_counts = (
    sectors["broad_sector"]
    .value_counts()
)

st.bar_chart(sector_counts)

st.caption(
    "Sector comparison analytics will be implemented later in Sprint 4."
)

st.caption("Sprint 4 - Day 22 Scaffold")