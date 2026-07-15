import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_sector_analysis_data
)

st.title("🏭 Sector Analysis")

df = get_sector_analysis_data()

sector = st.selectbox(
    "Select Sector",
    sorted(
        df["broad_sector"]
        .dropna()
        .unique()
    )
)

sector_df = df[
    df["broad_sector"] == sector
]

# =====================================================
# Bubble Chart
# =====================================================

st.subheader(
    f"{sector} Sector Landscape"
)

fig = px.scatter(
    sector_df,
    x="sales",
    y="return_on_equity_pct",
    size="market_cap_crore",
    color="sub_sector",
    hover_name="company_name",
    title="Revenue vs ROE vs Market Cap"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# =====================================================
# Sector Median KPIs
# =====================================================

st.subheader(
    "Sector Median KPIs"
)

kpi_df = sector_df[
    [
        "return_on_equity_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "free_cash_flow_cr",
        "debt_to_equity"
    ]
].median()

kpi_df = (
    kpi_df
    .reset_index()
)

kpi_df.columns = [
    "Metric",
    "Median"
]

bar_fig = px.bar(
    kpi_df,
    x="Metric",
    y="Median",
    title="Sector Median Metrics"
)

st.plotly_chart(
    bar_fig,
    width="stretch"
)

# =====================================================
# Companies
# =====================================================

st.subheader(
    "Companies in Sector"
)

st.dataframe(
    sector_df[
        [
            "company_id",
            "company_name",
            "sub_sector",
            "sales",
            "return_on_equity_pct",
            "market_cap_crore"
        ]
    ],
    width="stretch"
)