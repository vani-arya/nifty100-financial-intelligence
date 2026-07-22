import sqlite3
import pandas as pd
from pathlib import Path

conn = sqlite3.connect(
    "data/nifty100.db"
)

df = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)

conn.close()

df = (
    df.sort_values("year")
      .groupby("company_id")
      .tail(1)
)

kpis = [

    "return_on_equity_pct",

    "return_on_capital_employed_pct",

    "net_profit_margin_pct",

    "operating_profit_margin_pct",

    "debt_to_equity",

    "interest_coverage",

    "asset_turnover",

    "revenue_cagr_5yr",

    "pat_cagr_5yr",

    "composite_quality_score"
]

kpi_caps = {

    "return_on_equity_pct": (-50, 100),

    "return_on_capital_employed_pct": (-50, 100),

    "operating_profit_margin_pct": (-100, 100),

    "net_profit_margin_pct": (-100, 100),

    "debt_to_equity": (0, 10),

    "interest_coverage": (0, 500),

    "asset_turnover": (0, 10),

    "revenue_cagr_5yr": (-50, 100),

    "pat_cagr_5yr": (-50, 200),

    "composite_quality_score": (0, 100)
}

for col, (low, high) in kpi_caps.items():

    df[col] = df[col].clip(
        lower=low,
        upper=high
    )

stats = []

for metric in kpis:

    s = df[metric].dropna()

    stats.append({

        "Metric":
        metric,

        "P10":
        round(
            s.quantile(0.10),
            2
        ),

        "P25":
        round(
            s.quantile(0.25),
            2
        ),

        "P50":
        round(
            s.quantile(0.50),
            2
        ),

        "P75":
        round(
            s.quantile(0.75),
            2
        ),

        "P90":
        round(
            s.quantile(0.90),
            2
        ),

        "Mean":
        round(
            s.mean(),
            2
        ),

        "Std":
        round(
            s.std(),
            2
        )
    })

Path("output").mkdir(
    exist_ok=True
)

pd.DataFrame(
    stats
).to_csv(
    "output/portfolio_stats.csv",
    index=False
)

print(
    "Generated: output/portfolio_stats.csv"
)