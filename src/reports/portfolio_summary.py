from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = "data/nifty100.db"


def trend_arrow(latest, previous):

    if pd.isna(previous) or previous == 0:
        return "→"

    pct_change = abs(
        (latest - previous)
        / abs(previous)
    ) * 100

    if pct_change <= 2:
        return "→"

    if latest > previous:
        return "↑"

    return "↓"


conn = sqlite3.connect(DB_PATH)

sectors = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector
    FROM sectors
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

conn.close()

Path(
    "reports/portfolio"
).mkdir(
    parents=True,
    exist_ok=True
)

pdf_path = (
    "reports/portfolio/"
    "portfolio_summary.pdf"
)

c = canvas.Canvas(
    pdf_path,
    pagesize=A4
)

companies = sorted(
    sectors["company_id"].unique()
)

for company in companies:

    sector = sectors[
        sectors["company_id"] == company
    ]["broad_sector"].iloc[0]

    company_df = ratios[
        ratios["company_id"] == company
    ].sort_values("year")

    c.setFont(
        "Helvetica-Bold",
        20
    )

    c.drawString(
        40,
        800,
        company
    )

    c.setFont(
        "Helvetica",
        12
    )

    c.drawString(
        40,
        775,
        f"Sector: {sector}"
    )

    if len(company_df) >= 2:

        latest = company_df.iloc[-1]
        previous = company_df.iloc[-2]

        metrics = [

            (
                "ROE",
                "return_on_equity_pct"
            ),

            (
                "ROCE",
                "return_on_capital_employed_pct"
            ),

            (
                "Revenue CAGR",
                "revenue_cagr_5yr"
            ),

            (
                "Debt/Equity",
                "debt_to_equity"
            ),

            (
                "Net Margin",
                "net_profit_margin_pct"
            ),

            (
                "Interest Coverage",
                "interest_coverage"
            )
        ]

        y = 700

        for label, col in metrics:

            latest_val = latest.get(col)

            prev_val = previous.get(col)

            arrow = trend_arrow(
                latest_val,
                prev_val
            )

            c.drawString(
                60,
                y,
                f"{label}: {latest_val:.2f} {arrow}"
            )

            y -= 40

    else:

        c.drawString(
            60,
            700,
            "Insufficient history"
        )

    c.showPage()

c.save()

print(
    f"Generated: {pdf_path}"
)