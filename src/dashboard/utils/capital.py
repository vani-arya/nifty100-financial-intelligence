import pandas as pd
from src.dashboard.utils.db import get_connection


def get_capital_allocation_data():

    conn = get_connection()

    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )

    companies = pd.read_sql(
        """
        SELECT id,
               company_name
        FROM companies
        """,
        conn
    )

    conn.close()

    ratios["numeric_year"] = (
        ratios["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(float)
    )

    latest = (
        ratios.groupby("company_id")
        ["numeric_year"]
        .transform("max")
    )

    ratios = ratios[
        ratios["numeric_year"] == latest
    ]

    ratios = (
        ratios
        .sort_values("id")
        .drop_duplicates("company_id")
    )

    ratios = ratios.merge(
        companies,
        left_on="company_id",
        right_on="id",
        how="left"
    )

    return ratios


def classify_pattern(row):

    roe = row["return_on_equity_pct"]
    de = row["debt_to_equity"]
    fcf = row["free_cash_flow_cr"]
    cfo = row["cash_from_operations_cr"]
    capex = row["capex_cr"]
    payout = row["dividend_payout_ratio_pct"]

    if roe >= 20 and fcf > 0 and de < 1:
        return "Capital Compounder"

    elif payout >= 50:
        return "Dividend Machine"

    elif de == 0:
        return "Debt Free"

    elif de < 0.3 and roe >= 15:
        return "Debt Reducer"

    elif cfo > 0 and fcf > 0:
        return "Cash Generator"

    elif capex > fcf and roe > 15:
        return "Aggressive Reinvestor"

    elif roe < 10 and fcf > 0:
        return "Turnaround Builder"

    elif capex > cfo:
        return "Capital Intensive"

    return "Balanced Allocator"


def get_capital_patterns():

    df = get_capital_allocation_data()

    df["pattern"] = df.apply(
        classify_pattern,
        axis=1
    )

    return df