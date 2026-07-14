import streamlit as st

st.title("📑 Reports & Documents")

st.markdown("""
Access annual reports, company documents, and generated analytics exports.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Documents",
        1457
    )

with col2:
    st.metric(
        "Companies",
        92
    )

with col3:
    st.metric(
        "Report Types",
        3
    )

report_type = st.selectbox(
    "Select Report Type",
    [
        "Annual Reports",
        "Investor Presentations",
        "Corporate Filings"
    ]
)

st.success(
    f"Selected: {report_type}"
)

st.info(
    "Document viewer functionality will be added in later Sprint 4 tasks."
)

st.caption("Sprint 4 - Day 22 Scaffold")