import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_home_metrics,
    get_sector_breakdown,
    get_top_companies,
    get_companies
)

st.title("🏠 Nifty 100 Analytics")

selected_year = st.sidebar.selectbox(
    "Select Year",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5
)

metrics = get_home_metrics(selected_year)

companies = get_companies()

sector_df = get_sector_breakdown()

top_df = get_top_companies()

st.subheader("Market Overview")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Average ROE %",
    metrics["avg_roe"]
)

c2.metric(
    "Median D/E",
    metrics["median_de"]
)

c3.metric(
    "Median Revenue CAGR %",
    metrics["median_rev_cagr"]
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "Total Companies",
    len(companies)
)

c5.metric(
    "Debt Free Companies",
    metrics["debt_free"]
)

c6.metric(
    "Median P/E",
    "N/A"
)

st.divider()

st.subheader("Sector Distribution")

fig = px.pie(
    sector_df,
    names="broad_sector",
    values="company_count",
    hole=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader(
    "Top 5 Companies by Composite Quality Score"
)

display_df = top_df[
    [
        "company_id",
        "company_name",
        "composite_quality_score"
    ]
]

display_df.columns = [
    "Ticker",
    "Company",
    "Composite Score"
]

st.dataframe(
    display_df,
    use_container_width=True
)