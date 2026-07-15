import streamlit as st
import pandas as pd

from src.dashboard.utils.db import get_screener_data

st.title("🔍 Financial Screener")

df = get_screener_data()

# =====================================================
# PRESETS
# =====================================================

presets = {
    "Custom": {},

    "Quality": {
        "roe": 15,
        "de": 1,
        "fcf": 0,
        "rev": 10
    },

    "Value": {
        "pe": 20,
        "pb": 3
    },

    "Growth": {
        "pat": 20,
        "rev": 15
    },

    "Dividend": {
        "yield": 2
    },

    "Debt-Free": {
        "de": 0
    },

    "Turnaround": {
        "rev": 10
    }
}

preset = st.sidebar.selectbox(
    "Preset Screener",
    list(presets.keys())
)

# =====================================================
# DEFAULTS
# =====================================================

roe_default = presets[preset].get("roe", 0)
de_default = presets[preset].get("de", 10)
fcf_default = presets[preset].get("fcf", 0)
rev_default = presets[preset].get("rev", 0)
pat_default = presets[preset].get("pat", 0)
opm_default = presets[preset].get("opm", 0)
pe_default = presets[preset].get("pe", 100)
pb_default = presets[preset].get("pb", 20)
yield_default = presets[preset].get("yield", 0)
icr_default = presets[preset].get("icr", 0)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Screening Filters")

min_roe = st.sidebar.slider(
    "ROE Minimum",
    0.0,
    50.0,
    float(roe_default)
)

max_de = st.sidebar.slider(
    "Debt / Equity Maximum",
    0.0,
    10.0,
    float(de_default)
)

min_fcf = st.sidebar.number_input(
    "FCF Minimum",
    value=float(fcf_default)
)

min_rev = st.sidebar.slider(
    "Revenue CAGR 5Y Minimum",
    0.0,
    50.0,
    float(rev_default)
)

min_pat = st.sidebar.slider(
    "PAT CAGR 5Y Minimum",
    0.0,
    50.0,
    float(pat_default)
)

min_opm = st.sidebar.slider(
    "OPM Minimum",
    0.0,
    100.0,
    float(opm_default)
)

max_pe = st.sidebar.slider(
    "PE Maximum",
    0.0,
    100.0,
    float(pe_default)
)

max_pb = st.sidebar.slider(
    "PB Maximum",
    0.0,
    20.0,
    float(pb_default)
)

min_yield = st.sidebar.slider(
    "Dividend Yield Minimum",
    0.0,
    20.0,
    float(yield_default)
)

min_icr = st.sidebar.slider(
    "Interest Coverage Minimum",
    0.0,
    100.0,
    float(icr_default)
)

# =====================================================
# FILTERING
# =====================================================

filtered = df.copy()

filtered = filtered[
    filtered["return_on_equity_pct"] >= min_roe
]

filtered = filtered[
    filtered["debt_to_equity"] <= max_de
]

filtered = filtered[
    filtered["free_cash_flow_cr"] >= min_fcf
]

filtered = filtered[
    filtered["revenue_cagr_5yr"] >= min_rev
]

filtered = filtered[
    filtered["pat_cagr_5yr"] >= min_pat
]

filtered = filtered[
    filtered["opm_percentage"] >= min_opm
]

filtered = filtered[
    filtered["interest_coverage"] >= min_icr
]

filtered = filtered[
    filtered["pe_ratio"].fillna(9999) <= max_pe
]

filtered = filtered[
    filtered["pb_ratio"].fillna(9999) <= max_pb
]

filtered = filtered[
    filtered["dividend_yield_pct"].fillna(0) >= min_yield
]

filtered = filtered.sort_values(
    "composite_quality_score",
    ascending=False
)

# =====================================================
# RESULT COUNT
# =====================================================

st.success(
    f"{len(filtered)} companies match your filters"
)

# =====================================================
# DISPLAY TABLE
# =====================================================

display_cols = [
    "company_id",
    "company_name",
    "broad_sector",

    "composite_quality_score",

    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",

    "revenue_cagr_5yr",
    "pat_cagr_5yr",

    "opm_percentage",

    "pe_ratio",
    "pb_ratio",

    "dividend_yield_pct",

    "interest_coverage"
]

display_df = filtered[
    display_cols
].copy()

display_df.columns = [
    "Ticker",
    "Company",
    "Sector",

    "Composite Score",

    "ROE",
    "D/E",
    "FCF",

    "Revenue CAGR 5Y",
    "PAT CAGR 5Y",

    "OPM",

    "PE",
    "PB",

    "Dividend Yield",

    "ICR"
]

st.dataframe(
    display_df,
    width="stretch"
)

# =====================================================
# CSV DOWNLOAD
# =====================================================

csv = display_df.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download Results CSV",
    data=csv,
    file_name="screener_results.csv",
    mime="text/csv"
)