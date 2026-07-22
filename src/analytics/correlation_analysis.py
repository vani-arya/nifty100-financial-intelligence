import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

conn = sqlite3.connect("data/nifty100.db")

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

corr = df[kpis].corr(
    method="pearson"
)

Path("reports").mkdir(
    exist_ok=True
)

plt.figure(
    figsize=(12,10)
)

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)

plt.title(
    "KPI Correlation Heatmap"
)

plt.tight_layout()

plt.savefig(
    "reports/correlation_heatmap.png"
)

plt.close()

print(
    "Generated: reports/correlation_heatmap.png"
)