import streamlit as st

st.title("💰 Capital Allocation")

st.markdown("""
Analyze how companies allocate capital across:
- Growth
- Dividends
- Buybacks
- Debt Reduction
- Reinvestment
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Capital Categories",
        5
    )

with col2:
    st.metric(
        "Years Covered",
        12
    )

with col3:
    st.metric(
        "Companies",
        92
    )

st.info(
    "Capital allocation maps will be integrated from Sprint 2 outputs."
)

st.caption("Sprint 4 - Day 22 Scaffold")