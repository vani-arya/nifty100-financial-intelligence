import streamlit as st
from src.dashboard.utils.db import get_companies

st.title("🔍 Financial Screener")

st.markdown("""
Screen companies based on financial metrics and quality filters.
""")

companies = get_companies()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Available Companies", len(companies))

with col2:
    st.metric("Preset Screeners", 6)

with col3:
    st.metric("Financial KPIs", 20)

preset = st.selectbox(
    "Select Preset",
    [
        "Quality Compounder",
        "Value Pick",
        "Growth Accelerator",
        "Dividend Champion",
        "Debt Free Bluechip",
        "Turnaround Watch"
    ]
)

st.info(
    f"Selected Preset: {preset}"
)

st.subheader("Company Universe")

st.dataframe(
    companies[
        ["id", "company_name"]
    ].head(15),
    use_container_width=True
)

st.caption("Sprint 4 - Day 22 Scaffold")