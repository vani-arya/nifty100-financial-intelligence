import streamlit as st

from src.dashboard.utils.db import (
    get_companies,
    get_reports
)

st.title("📄 Annual Reports")

companies = get_companies()

def company_name(ticker):

    rows = companies.loc[
        companies["id"] == ticker,
        "company_name"
    ]

    if rows.empty:
        return ticker

    return rows.iloc[0]

selected_company = st.selectbox(
    "Select Company",
    companies["id"].tolist(),
    format_func=company_name
)

reports = get_reports(
    selected_company
)

if reports.empty:

    st.warning(
        "No annual reports available."
    )

else:

    st.success(
        f"{len(reports)} reports found"
    )

    for _, row in reports.iterrows():

        year = row["Year"]
        url = row["Annual_Report"]

        if (
            url is None
            or str(url).strip() == ""
        ):

            st.error(
                f"{year} - Report unavailable"
            )

        else:

            st.markdown(
                f"📘 **{year}** - "
                f"[Open Annual Report]({url})"
            )