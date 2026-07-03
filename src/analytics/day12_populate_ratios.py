import sqlite3
import pandas as pd

from src.analytics.cagr import calculate_cagr

conn = sqlite3.connect("data/nifty100.db")

pl = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        sales,
        net_profit,
        eps
    FROM profitandloss
    """,
    conn
)

ratios = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)


pl = pl[
    pl["year"] != "TTM"
].copy()


pl["year_num"] = (
    pl["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)


pl = pl.sort_values(
    ["company_id", "year_num"]
)


revenue_cagr = {}
pat_cagr = {}
eps_cagr = {}


for company_id, group in pl.groupby("company_id"):

    group = group.sort_values(
        "year_num"
    ).reset_index(drop=True)

    for i in range(len(group)):

        if i < 5:
            continue

        current_row = group.iloc[i]
        base_row = group.iloc[i - 5]

        rev_value, _ = calculate_cagr(
            base_row["sales"],
            current_row["sales"],
            5
        )

        pat_value, _ = calculate_cagr(
            base_row["net_profit"],
            current_row["net_profit"],
            5
        )

        eps_value, _ = calculate_cagr(
            base_row["eps"],
            current_row["eps"],
            5
        )

        key = (
            current_row["company_id"],
            current_row["year"]
        )

        revenue_cagr[key] = rev_value
        pat_cagr[key] = pat_value
        eps_cagr[key] = eps_value


        ratios["revenue_cagr_5yr"] = ratios.apply(
    lambda row:
    revenue_cagr.get(
        (row["company_id"], row["year"])
    ),
    axis=1
)

ratios["pat_cagr_5yr"] = ratios.apply(
    lambda row:
    pat_cagr.get(
        (row["company_id"], row["year"])
    ),
    axis=1
)

ratios["eps_cagr_5yr"] = ratios.apply(
    lambda row:
    eps_cagr.get(
        (row["company_id"], row["year"])
    ),
    axis=1
)


ratios["composite_quality_score"] = (
    ratios["return_on_equity_pct"].fillna(0) * 0.4
    +
    ratios["revenue_cagr_5yr"].fillna(0) * 0.3
    +
    ratios["pat_cagr_5yr"].fillna(0) * 0.3
).round(2)


ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)


count = pd.read_sql(
    """
    SELECT COUNT(*) AS rows
    FROM financial_ratios
    """,
    conn
)

print(count)


sample = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        revenue_cagr_5yr,
        pat_cagr_5yr,
        eps_cagr_5yr,
        composite_quality_score
    FROM financial_ratios
    WHERE revenue_cagr_5yr IS NOT NULL
    LIMIT 10
    """,
    conn
)

print(sample)
conn.close()