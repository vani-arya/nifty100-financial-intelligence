import streamlit as st
from src.dashboard.utils.db import (
    get_companies,
    get_sectors
)

st.title("🏠 Nifty 100 Analytics")

st.markdown(
    """
    Welcome to the Nifty 100 Financial Intelligence Platform.

    This dashboard provides:
    - Company financial analysis
    - KPI benchmarking
    - Stock screening
    - Peer comparison
    - Trend analytics
    - Capital allocation insights
    - Valuation analytics
    """
)

# -----------------------------
# Load Data
# -----------------------------

companies = get_companies()
sectors = get_sectors()

# -----------------------------
# KPI Cards
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Companies",
        len(companies)
    )

with col2:
    st.metric(
        "Total Sectors",
        sectors["broad_sector"].nunique()
    )

# -----------------------------
# Dataset Overview
# -----------------------------

st.subheader("Dataset Overview")

st.write(
    f"""
    Database currently contains
    **{len(companies)} companies**
    available for analysis.
    """
)

# -----------------------------
# Company Preview
# -----------------------------

st.subheader("Company Preview")

preview_cols = [
    col
    for col in [
        "id",
        "company_name",
        "roe_percentage",
        "roce_percentage"
    ]
    if col in companies.columns
]

st.dataframe(
    companies[preview_cols].head(10),
    use_container_width=True
)

# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "Sprint 4 • Day 22 Dashboard Scaffold"
)