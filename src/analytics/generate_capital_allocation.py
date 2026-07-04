import sqlite3
import pandas as pd

from src.analytics.cashflow_kpis import (
    calculate_cfo_pat_ratio,
    classify_capital_allocation
)

conn = sqlite3.connect("data/nifty100.db")

cashflow = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        operating_activity,
        investing_activity,
        financing_activity
    FROM cashflow
    """,
    conn
)

pl = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        net_profit
    FROM profitandloss
    """,
    conn
)

df = cashflow.merge(
    pl,
    on=["company_id", "year"],
    how="left"
)

patterns = []

for _, row in df.iterrows():

    cfo = row["operating_activity"]
    cfi = row["investing_activity"]
    cff = row["financing_activity"]
    pat = row["net_profit"]

    cfo_pat_ratio = calculate_cfo_pat_ratio(
        cfo,
        pat
    )

    pattern = classify_capital_allocation(
        cfo,
        cfi,
        cff,
        cfo_pat_ratio
    )

    patterns.append(pattern)

df["cfo_sign"] = df["operating_activity"].apply(
    lambda x: "+" if x > 0 else "-"
)

df["cfi_sign"] = df["investing_activity"].apply(
    lambda x: "+" if x > 0 else "-"
)

df["cff_sign"] = df["financing_activity"].apply(
    lambda x: "+" if x > 0 else "-"
)

df["pattern_label"] = patterns

output = df[
    [
        "company_id",
        "year",
        "cfo_sign",
        "cfi_sign",
        "cff_sign",
        "pattern_label"
    ]
]

output.to_csv(
    "output/capital_allocation.csv",
    index=False
)

print(output.head())
print(f"\nRows exported: {len(output)}")

conn.close()