import sqlite3
import pandas as pd
from scipy.stats import zscore
from pathlib import Path

conn = sqlite3.connect(
    "data/nifty100.db"
)

ratios = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)

sectors = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector
    FROM sectors
    """,
    conn
)

conn.close()

ratios = (
    ratios.sort_values("year")
          .groupby("company_id")
          .tail(1)
)

df = ratios.merge(
    sectors,
    on="company_id",
    how="left"
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

outliers = []

for sector in df["broad_sector"].unique():

    sector_df = df[
        df["broad_sector"] == sector
    ].copy()

    for metric in kpis:

        sector_df["z"] = zscore(
            sector_df[metric].fillna(
                sector_df[metric].median()
            )
        )

        flagged = sector_df[
            sector_df["z"].abs() > 3
        ]

        for _, row in flagged.iterrows():

            outliers.append({

                "company_id":
                row["company_id"],

                "broad_sector":
                sector,

                "metric":
                metric,

                "value":
                row[metric],

                "z_score":
                round(
                    row["z"],
                    2
                )
            })

Path("output").mkdir(
    exist_ok=True
)

pd.DataFrame(
    outliers
).to_csv(
    "output/outlier_report.csv",
    index=False
)

print(
    "Generated: output/outlier_report.csv"
)

print(
    "Outliers Found:",
    len(outliers)
)