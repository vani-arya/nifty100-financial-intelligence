from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path

import sqlite3
import pandas as pd
from datetime import datetime

def load_sector_data():

    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    query = """
    SELECT
        s.broad_sector,
        r.*
    FROM financial_ratios r
    JOIN sectors s
        ON r.company_id =
           s.company_id
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    return df


df = load_sector_data()

df = (
    df.sort_values(
        "year"
    )
    .groupby(
        "company_id"
    )
    .tail(1)
)


metrics = [

    "return_on_equity_pct",

    "return_on_capital_employed_pct",

    "revenue_cagr_5yr",

    "debt_to_equity",

    "operating_profit_margin_pct",

    "net_profit_margin_pct",

    "interest_coverage",

    "asset_turnover"
]


for sector in sorted(
    df["broad_sector"].unique()
):
    

    sector_df = df[
        df["broad_sector"] == sector
    ]

    Path(
        "reports/sector"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    today = datetime.now().strftime(
        "%Y%m%d"
    )

    pdf_path = (
        f"reports/sector/"
        f"{sector}_report_{today}.pdf"
    )

    c = canvas.Canvas(
        pdf_path,
        pagesize=A4
    )

    c.setFont(
        "Helvetica-Bold",
        20
    )

    c.drawString(
       40,
       800,
        f"{sector} Sector Report"
    )

    c.drawString(
        40,
        770,
        f"Companies: {len(sector_df)}"
    )

    y = 720
    
    for metric in metrics:

        value = round(
           sector_df[
               metric
            ].median(),
            2
        )

        c.drawString(
            40,
            y,
            f"{metric}: {value}"
        )

        y -= 20

    best = sector_df.loc[
        sector_df[
            "return_on_equity_pct"
        ].idxmax()
    ]

    worst = sector_df.loc[
       sector_df[
           "return_on_equity_pct"
       ].idxmin()
    ]
 
    c.drawString(
        40,
        520,
       f"Best ROE: "
       f"{best['company_id']}"
    )

    c.drawString(
        40,
        500,
       f"Worst ROE: "
       f"{worst['company_id']}"
    )

    y = 440

    c.setFont(
        "Helvetica-Bold",
       8
    )

    c.drawString(
       40,
       y,
       "Company"
    )

    c.drawString(
        120,
        y,
       "ROE"
    )

    c.drawString(
       170,
       y,
       "ROCE"
    )

    c.drawString(
        230,
       y,
       "Rev CAGR"
    )
      
    c.drawString(
      300,
       y,
       "Debt/Equity"
    )

    c.drawString(
       390,
        y,
       "NPM"
    )

    y -= 20

    c.setFont(
       "Helvetica",
        7
    )

    c.showPage()


    for _, row in sector_df.iterrows():

        c.drawString(
           40,
           y,
            str(row["company_id"])
        )

        c.drawString(
           120,
           y,
           str(round(
               row["return_on_equity_pct"],
               2
           ))
        )

        c.drawString(
           170,
           y,
           str(round(
               row[
                  "return_on_capital_employed_pct"
               ],
               2
           ))
        )

        c.drawString(
           230,
           y,
           str(round(
               row["revenue_cagr_5yr"],
               2
           ))
        )

        c.drawString(
           300,
           y,
           str(round(
               row["debt_to_equity"],
               2
           ))
        )

        c.drawString(
            390,
            y,
            str(round(
                row["net_profit_margin_pct"],
                2
           ))
        )

        y -= 15

        if y < 50:

          c.showPage()

          y = 800

          c.setFont(
              "Helvetica",
               7
          )
          
    c.save()

    print(
          f"Generated: {pdf_path}"
    )