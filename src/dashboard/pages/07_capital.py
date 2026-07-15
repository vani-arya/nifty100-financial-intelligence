import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard.utils.capital import get_capital_patterns

st.title("🏛️ Capital Allocation Map")

df = get_capital_patterns()

# ==================================
# KPI CARDS
# ==================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Companies",
        len(df)
    )

with col2:
    st.metric(
        "Patterns",
        df["pattern"].nunique()
    )

with col3:

    largest_pattern = (
        df["pattern"]
        .value_counts()
        .idxmax()
    )

    st.metric(
        "Largest Pattern",
        largest_pattern
    )

# ==================================
# TREEMAP
# ==================================

st.subheader(
    "Capital Allocation Patterns"
)

df["treemap_size"] = (
    df["free_cash_flow_cr"]
    .abs()
)

fig = px.treemap(
    df,
    path=[
        "pattern",
        "company_name"
    ],
    values="treemap_size",
    color="pattern"
)

fig.update_layout(
    height=700
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ==================================
# PATTERN SELECTOR
# ==================================

st.subheader(
    "Explore Pattern"
)

selected_pattern = st.selectbox(
    "Select Pattern",
    sorted(
        df["pattern"]
        .unique()
    )
)

pattern_df = df[
    df["pattern"]
    == selected_pattern
]

st.success(
    f"{len(pattern_df)} companies belong to {selected_pattern}"
)

# ==================================
# COMPANY TABLE
# ==================================

display_cols = [
    "company_id",
    "company_name",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "cash_from_operations_cr",
    "dividend_payout_ratio_pct"
]

st.dataframe(
    pattern_df[
        display_cols
    ].sort_values(
        "return_on_equity_pct",
        ascending=False
    ),
    width="stretch"
)