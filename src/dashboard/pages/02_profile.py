import streamlit as st
from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_pl,
    get_bs,
    get_cf
)

st.title("📊 Company Profile")

# ---------------------------------
# Company Selector
# ---------------------------------

companies = get_companies()

company_map = dict(
    zip(
        companies["company_name"],
        companies["id"]
    )
)

selected_company = st.selectbox(
    "Select Company",
    sorted(company_map.keys())
)

ticker = company_map[selected_company]

# ---------------------------------
# Load Data
# ---------------------------------

ratios = get_ratios(ticker)
pl = get_pl(ticker)
bs = get_bs(ticker)
cf = get_cf(ticker)

# ---------------------------------
# Company Information
# ---------------------------------

company_info = companies[
    companies["id"] == ticker
].iloc[0]

st.subheader(selected_company)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "ROE %",
        company_info["roe_percentage"]
    )

with col2:

    st.metric(
        "ROCE %",
        company_info["roce_percentage"]
    )

with col3:

    st.metric(
        "Book Value",
        company_info["book_value"]
    )

# ---------------------------------
# Latest KPI Snapshot
# ---------------------------------

st.subheader("Latest Financial Ratios")

if not ratios.empty:

    latest = ratios.iloc[-1]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            "ROE",
            round(
                latest["return_on_equity_pct"],
                2
            )
        )

    with kpi2:
        st.metric(
            "ROCE",
            round(
                latest["return_on_capital_employed_pct"],
                2
            )
        )

    with kpi3:
        st.metric(
            "Debt / Equity",
            round(
                latest["debt_to_equity"],
                2
            )
        )

    with kpi4:
        st.metric(
            "NPM %",
            round(
                latest["net_profit_margin_pct"],
                2
            )
        )

# ---------------------------------
# Tabs
# ---------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Profit & Loss",
        "Balance Sheet",
        "Cash Flow",
        "Financial Ratios"
    ]
)

with tab1:

    st.dataframe(
        pl,
        use_container_width=True
    )

with tab2:

    st.dataframe(
        bs,
        use_container_width=True
    )

with tab3:

    st.dataframe(
        cf,
        use_container_width=True
    )

with tab4:

    st.dataframe(
        ratios,
        use_container_width=True
    )

st.caption(
    "Sprint 4 - Day 22 Scaffold"
)