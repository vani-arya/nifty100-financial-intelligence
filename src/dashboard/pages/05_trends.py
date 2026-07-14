import streamlit as st
from src.dashboard.utils.db import get_companies

st.title("📈 Trend Analysis")

companies = get_companies()

ticker = st.selectbox(
    "Select Company",
    companies["id"]
)

metric = st.selectbox(
    "Select KPI",
    [
        "ROE",
        "ROCE",
        "Net Profit Margin",
        "Revenue CAGR",
        "PAT CAGR",
        "Debt To Equity"
    ]
)

st.info(
    f"Trend analysis for {ticker} | KPI: {metric}"
)

st.subheader("Historical KPI Trends")

st.empty()

st.caption(
    "Charts will be implemented in upcoming dashboard tasks."
)

st.caption("Sprint 4 - Day 22 Scaffold")