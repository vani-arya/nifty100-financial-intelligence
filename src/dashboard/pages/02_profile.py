import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.dashboard.utils.db import (
    get_companies,
    get_company_profile,
    get_company_latest_ratios,
    get_company_timeseries,
    get_pros_cons
)

st.title("📊 Company Profile")

companies = get_companies()

search_text = st.text_input(
    "Search Company Name or Ticker"
)

filtered = companies.copy()

if search_text:

    filtered = companies[
        companies["company_name"]
        .str.contains(search_text, case=False, na=False)
        |
        companies["id"]
        .str.contains(search_text, case=False, na=False)
    ]

if filtered.empty:

    st.warning(
        "Ticker not found — please try another."
    )

    st.stop()

selected_company = st.selectbox(
    "Select Company",
    filtered["company_name"]
)

company_row = filtered[
    filtered["company_name"]
    == selected_company
].iloc[0]

ticker = company_row["id"]

company_df, sector_df = get_company_profile(ticker)

ratios = get_company_latest_ratios(ticker)

pl_df, ratio_history = get_company_timeseries(ticker)

pros_cons = get_pros_cons(ticker)

# --------------------------------------------------
# COMPANY CARD
# --------------------------------------------------

st.header(company_row["company_name"])

col1, col2 = st.columns(2)

with col1:

    if not sector_df.empty:

        st.markdown(
            f"**Sector:** {sector_df.iloc[0]['broad_sector']}"
        )

        st.markdown(
            f"**Sub Sector:** {sector_df.iloc[0]['sub_sector']}"
        )

    st.markdown(
        f"**Ticker:** {ticker}"
    )

with col2:

    if (
        not company_df.empty
        and
        "about_company" in company_df.columns
    ):

        st.markdown(
            company_df.iloc[0]["about_company"]
        )

# --------------------------------------------------
# KPI TILES
# --------------------------------------------------
def safe_metric(value):
    if pd.isna(value):
        return "N/A"
    return round(value, 2)


if not ratios.empty:

    latest = ratios.iloc[0]

    c1, c2, c3 = st.columns(3)

    c4, c5, c6 = st.columns(3)

    c1.metric(
    "ROE %",
    safe_metric(
        latest["return_on_equity_pct"]
    )
)

    c2.metric(
        "ROCE %",
        safe_metric(
            latest[
                "return_on_capital_employed_pct"]
        )
    )

    c3.metric(
        "Net Profit Margin %",
        safe_metric(
            latest[
                "net_profit_margin_pct"]
        )
    )

    c4.metric(
        "Debt / Equity",
        safe_metric(
            latest["debt_to_equity"]
        )
    )

    c5.metric(
        "Revenue CAGR 5Y %",
        safe_metric(
            latest["revenue_cagr_5yr"]
        )
    )

    c6.metric(
        "Free Cash Flow",
        safe_metric(
            latest["free_cash_flow_cr"]
        )
    )

# --------------------------------------------------
# REVENUE VS PROFIT
# --------------------------------------------------

st.subheader(
    "Revenue vs Net Profit (10 Years)"
)

if not pl_df.empty:

    fig = go.Figure()

    fig.add_bar(
        x=pl_df["year"],
        y=pl_df["sales"],
        name="Revenue"
    )

    fig.add_bar(
        x=pl_df["year"],
        y=pl_df["net_profit"],
        name="Net Profit"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# ROE VS ROCE
# --------------------------------------------------

st.subheader(
    "ROE vs ROCE Trend"
)

if not ratio_history.empty:

    fig2 = go.Figure()

    fig2.add_scatter(
        x=ratio_history["year"],
        y=ratio_history[
            "return_on_equity_pct"
        ],
        mode="lines+markers",
        name="ROE"
    )

    fig2.add_scatter(
        x=ratio_history["year"],
        y=ratio_history[
            "return_on_capital_employed_pct"
        ],
        mode="lines+markers",
        name="ROCE"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# --------------------------------------------------
# PROS & CONS
# --------------------------------------------------
st.subheader("Pros & Cons")

if pros_cons.empty:

    st.warning(
        "Pros & Cons not available for this company."
    )

else:

    pros_text = str(
        pros_cons.iloc[0]["pros"]
    )

    cons_text = str(
        pros_cons.iloc[0]["cons"]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.success("Pros")

        if (
            pros_text == "None"
            or pros_text.strip() == ""
            or pros_text.lower() == "nan"
        ):
            st.info(
                "No pros available."
            )
        else:
            st.markdown(
                f"✅ {pros_text}"
            )

    with col2:

        st.error("Cons")

        if (
            cons_text == "None"
            or cons_text.strip() == ""
            or cons_text.lower() == "nan"
        ):
            st.info(
                "No cons available."
            )
        else:
            st.markdown(
                f"❌ {cons_text}"
            )


