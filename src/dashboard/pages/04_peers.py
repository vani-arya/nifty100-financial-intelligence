import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.dashboard.utils.db import (
    get_peer_group_data
)

st.title("👥 Peer Comparison")

peer_df = get_peer_group_data()

# ==========================
# Peer Group Selection
# ==========================

peer_groups = sorted(
    peer_df[
        "peer_group_name"
    ]
    .dropna()
    .unique()
)

selected_group = st.selectbox(
    "Select Peer Group",
    peer_groups
)

group_df = peer_df[
    peer_df["peer_group_name"]
    == selected_group
]

# ==========================
# Company Selection
# ==========================

selected_company = st.selectbox(
    "Select Company",
    sorted(
        group_df[
            "company_id"
        ].unique()
    )
)

# ==========================
# Radar Chart
# ==========================

metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "interest_coverage"
]

company_row = group_df[
    group_df["company_id"]
    == selected_company
]

peer_avg = (
    group_df[metrics]
    .mean()
)

company_values = (
    company_row[metrics]
    .iloc[0]
)

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values.tolist(),
        theta=metrics,
        fill="toself",
        name=selected_company
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_avg.tolist(),
        theta=metrics,
        fill="toself",
        name="Peer Average"
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),
    showlegend=True
)

st.subheader(
    "Company vs Peer Average"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ==========================
# KPI Table
# ==========================

table_cols = [
    "company_id",
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "composite_quality_score",
    "is_benchmark"
]

display_df = (
    group_df[
        table_cols
    ]
    .copy()
)

st.subheader(
    "Peer Group KPI Table"
)

def highlight_benchmark(row):

    if row["is_benchmark"] == 1:

        return [
            "background-color: lightgreen"
        ] * len(row)

    return [
        ""
    ] * len(row)

st.dataframe(
    display_df
    .style
    .apply(
        highlight_benchmark,
        axis=1
    ),
    width="stretch"
)