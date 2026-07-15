import streamlit as st
import plotly.graph_objects as go

from src.dashboard.utils.db import (
    get_companies,
    get_trend_data
)

st.title("📈 Trend Analysis")

# =====================================================
# Company Selection
# =====================================================

companies = get_companies()

ticker = st.selectbox(
    "Select Company",
    companies["id"].tolist()
)

pl, ratios = get_trend_data(ticker)

# =====================================================
# Metric Selection
# =====================================================

metric_options = {
    "Revenue": ("pl", "sales"),
    "Net Profit": ("pl", "net_profit"),
    "Operating Profit": ("pl", "operating_profit"),
    "EPS": ("pl", "eps"),

    "ROE": ("ratios", "return_on_equity_pct"),
    "ROCE": ("ratios", "return_on_capital_employed_pct"),
    "Net Profit Margin": ("ratios", "net_profit_margin_pct"),
    "Free Cash Flow": ("ratios", "free_cash_flow_cr")
}

selected_metrics = st.multiselect(
    "Select up to 3 Metrics",
    list(metric_options.keys()),
    default=["Revenue"],
    max_selections=3
)

# =====================================================
# Plotly Figure
# =====================================================

fig = go.Figure()

for metric_name in selected_metrics:

    source, column = metric_options[metric_name]

    if source == "pl":

        df = pl.copy()

    else:

        df = ratios.copy()

    if df.empty:
        continue

    df = df.sort_values("numeric_year")

    fig.add_trace(
        go.Scatter(
            x=df["numeric_year"],
            y=df[column],
            mode="lines+markers+text",
            name=metric_name
        )
    )

    # ---------------------------------------------
    # YoY %
    # ---------------------------------------------

    yoy = (
        df[column]
        .pct_change()
        * 100
    )

    labels = []

    for value in yoy:

        if value != value:
            labels.append("")
        else:
            labels.append(
                f"{value:.1f}%"
            )

    fig.add_trace(
        go.Scatter(
            x=df["numeric_year"],
            y=df[column],
            mode="text",
            text=labels,
            showlegend=False
        )
    )

# =====================================================
# Layout
# =====================================================

fig.update_layout(
    title=f"{ticker} - 10 Year Trend Analysis",
    xaxis_title="Year",
    yaxis_title="Value",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# =====================================================
# Data Preview
# =====================================================

st.subheader("Underlying Data")

col1, col2 = st.columns(2)

with col1:
    st.write("Profit & Loss")
    st.dataframe(
        pl.tail(10),
        width="stretch"
    )

with col2:
    st.write("Financial Ratios")
    st.dataframe(
        ratios.tail(10),
        width="stretch"
    )