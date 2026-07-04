import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

companies = [
    "ABB",
    "SIEMENS",
    "TCS",
    "RELIANCE",
    "HDFCBANK"
]

frames = []

for company in companies:

    df = pd.read_sql(
        f"""
        SELECT
            company_id,
            year,
            net_profit_margin_pct,
            return_on_equity_pct,
            return_on_capital_employed_pct,
            debt_to_equity,
            interest_coverage,
            asset_turnover,
            free_cash_flow_cr,
            revenue_cagr_5yr,
            pat_cagr_5yr,
            eps_cagr_5yr,
            composite_quality_score
        FROM financial_ratios
        WHERE company_id = '{company}'
        ORDER BY id DESC
        LIMIT 1
        """,
        conn
    )

    frames.append(df)

demo = pd.concat(frames)

demo.to_csv(
    "output/demo_companies.csv",
    index=False
)

print(demo)

conn.close()