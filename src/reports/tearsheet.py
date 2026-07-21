from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

OUTPUT_DIR = "reports/tearsheets"


def create_revenue_chart(
    company_id
):
    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    query = f"""
    SELECT year, sales
    FROM profitandloss
    WHERE company_id='{company_id}'
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    df = df[
        ~df["year"]
        .str.contains(
            "TTM",
            na=False
        )
    ]
    
    df = (
        df
        .drop_duplicates(
            subset=["year"]
        )
        .tail(10)
    )

    plt.figure(
        figsize=(4, 3)
    )

    plt.bar(
        df["year"],
        df["sales"]
    )

    plt.title(
        "Revenue"
    )

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    path = (
        f"temp/{company_id}_revenue.png"
    )

    Path("temp").mkdir(
        exist_ok=True
    )

    plt.savefig(path)

    plt.close()

    return path


def create_profit_chart(
    company_id
):
    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    query = f"""
    SELECT year, net_profit
    FROM profitandloss
    WHERE company_id='{company_id}'
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    df = df[
        ~df["year"]
        .str.contains(
            "TTM",
            na=False
        )
    ]

    df = (
        df
        .drop_duplicates(
            subset=["year"]
        )
        .tail(10)
    )

    plt.figure(
        figsize=(4, 3)
    )

    plt.bar(
        df["year"],
        df["net_profit"]
    )

    plt.title(
        "Net Profit"
    )

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    path = (
        f"temp/{company_id}_profit.png"
    )

    plt.savefig(path)

    plt.close()

    return path


def create_roe_roce_chart(
    company_id
):

    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    query = f"""
    SELECT
        year,
        return_on_equity_pct,
        return_on_capital_employed_pct
    FROM financial_ratios
    WHERE company_id='{company_id}'
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    df = (
        df
        .drop_duplicates(
            subset=["year"]
        )
        .tail(10)
    )

    plt.figure(
        figsize=(8, 3)
    )

    plt.plot(
        df["year"],
        df["return_on_equity_pct"],
        marker="o",
        label="ROE"
    )

    plt.plot(
        df["year"],
        df["return_on_capital_employed_pct"],
        marker="o",
        label="ROCE"
    )

    plt.title(
        "ROE vs ROCE"
    )

    plt.xticks(
        rotation=45
    )

    plt.legend()

    plt.tight_layout()

    path = (
        f"temp/{company_id}_roe_roce.png"
    )

    plt.savefig(path)

    plt.close()

    return path


def create_balance_sheet_chart(
    company_id
):

    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    query = f"""
    SELECT
        year,
        equity_capital,
        borrowings,
        other_liabilities
    FROM balancesheet
    WHERE company_id='{company_id}'
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    df = (
        df
        .drop_duplicates(
            subset=["year"]
        )
        .tail(10)
    )

    plt.figure(
        figsize=(7, 3)
    )

    plt.bar(
        df["year"],
        df["equity_capital"],
        label="Equity"
    )

    plt.bar(
        df["year"],
        df["borrowings"],
        bottom=df["equity_capital"],
        label="Borrowings"
    )

    plt.bar(
        df["year"],
        df["other_liabilities"],
        bottom=(
            df["equity_capital"]
            +
            df["borrowings"]
        ),
        label="Other Liabilities"
    )

    plt.title(
        "Balance Sheet Composition"
    )

    plt.xticks(
        rotation=45
    )

    plt.legend()

    plt.tight_layout()

    path = (
        f"temp/{company_id}_balance_sheet.png"
    )

    plt.savefig(path)

    plt.close()

    return path


def create_cashflow_waterfall(
    company_id
):

    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    query = f"""
    SELECT
        operating_activity,
        investing_activity,
        financing_activity,
        net_cash_flow
    FROM cashflow
    WHERE company_id='{company_id}'
    ORDER BY year DESC
    LIMIT 1
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    if df.empty:

        return None

    row = df.iloc[0]

    labels = [
        "CFO",
        "CFI",
        "CFF",
        "Net CF"
    ]

    values = [
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"],
        row["net_cash_flow"]
    ]

    plt.figure(
        figsize=(6, 3)
    )

    bars = plt.bar(
        labels,
        values
    )

    plt.axhline(
        y=0,
        linewidth=1
    )

    plt.title(
        "Cash Flow Waterfall"
    )

    plt.tight_layout()

    path = (
        f"temp/{company_id}_cashflow.png"
    )

    plt.savefig(path)

    plt.close()

    return path


def get_latest_ratios(company_id):

    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    query = f"""
    SELECT *
    FROM financial_ratios
    WHERE company_id='{company_id}'
    ORDER BY year DESC
    LIMIT 1
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    if df.empty:

       return pd.Series({

           "return_on_equity_pct": None,

           "return_on_capital_employed_pct": None,

           "debt_to_equity": None,

           "interest_coverage": None,

           "revenue_cagr_5yr": None,

           "net_profit_margin_pct": None

        })

    return df.iloc[0]


def get_company_name(company_id):

    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    row = conn.execute(
        """
        SELECT company_name
        FROM companies
        WHERE id = ?
        """,
        (company_id,)
    ).fetchone()

    conn.close()

    if row:
        return row[0]

    return company_id


def fmt(value, suffix=""):

    if pd.isna(value):

        return "NA"

    return f"{value:.2f}{suffix}"


def draw_kpi_tile(
    c,
    x,
    y,
    width,
    height,
    title,
    value
):

    c.setFillColor(
        colors.HexColor("#F5F5F5")
    )

    c.roundRect(
        x,
        y,
        width,
        height,
        8,
        fill=1,
        stroke=0
    )

    c.setFillColor(
        colors.HexColor("#0A2342")
    )

    c.setFont(
        "Helvetica-Bold",
        10
    )

    c.drawString(
        x + 10,
        y + height - 20,
        title
    )

    c.setFont(
        "Helvetica-Bold",
        16
    )

    c.drawString(
        x + 10,
        y + 15,
        str(value)
    )


def get_pros_cons(company_id):

    df = pd.read_csv(
        "output/pros_cons_generated.csv"
    )

    company_df = df[
        df["company_id"] == company_id
    ]

    pros = (
        company_df[
            company_df["type"] == "pro"
        ]["text"]
        .tolist()
    )

    cons = (
        company_df[
            company_df["type"] == "con"
        ]["text"]
        .tolist()
    )

    return pros, cons


def get_capital_allocation_label(
    company_id
):

    df = pd.read_excel(
        "output/cashflow_intelligence.xlsx"
    )

    row = df[
        df["company_id"] == company_id
    ]

    if row.empty:

       return "Unknown"

    value = row.iloc[0][
        "capital_allocation_label"
    ]

    if pd.isna(value):

       return "Unknown"

    return str(value)


def generate_tearsheet(company_id):

    Path(OUTPUT_DIR).mkdir(
        parents=True,
        exist_ok=True
    )

    pdf_path = (
        f"{OUTPUT_DIR}/{company_id}_tearsheet.pdf"
    )

    c = canvas.Canvas(
        pdf_path,
        pagesize=A4
    )

    width, height = A4

    styles = getSampleStyleSheet()

    pros_style = styles["BodyText"]
    pros_style.fontSize = 8
    pros_style.leading = 10
    pros_style.textColor = colors.green

    cons_style = styles["BodyText"]
    cons_style.fontSize = 8
    cons_style.leading = 10
    cons_style.textColor = colors.red

    company_name = get_company_name(
        company_id
    )

    # NAVY HEADER

    c.setFillColor(
        colors.HexColor("#0A2342")
    )

    c.rect(
        0,
        height - 80,
        width,
        80,
        fill=1,
        stroke=0
    )

    ratio_row = get_latest_ratios(
    company_id
    )

    tile_width = 150
    tile_height = 70

    start_y = height - 180

    #Row 1

    draw_kpi_tile(
    c,
    40,
    start_y,
    tile_width,
    tile_height,
    "ROE %",
    fmt(
        ratio_row[
            "return_on_equity_pct"
        ]
    )
    )

    draw_kpi_tile(
    c,
    220,
    start_y,
    tile_width,
    tile_height,
    "ROCE %",
    fmt(
        ratio_row[
           "return_on_capital_employed_pct"
        ]
    )
    )

    draw_kpi_tile(
    c,
    400,
    start_y,
    tile_width,
    tile_height,
    "Debt / Equity",
    fmt(
        ratio_row[
            "debt_to_equity"
        ]
    )
    )

    #Row 2

    draw_kpi_tile(
    c,
    40,
    start_y - 90,
    tile_width,
    tile_height,
    "Interest Cov.",
    fmt(
       ratio_row[
           "interest_coverage"
        ]
    )
    )

    draw_kpi_tile(
    c,
    220,
    start_y - 90,
    tile_width,
    tile_height,
    "Revenue CAGR",
    fmt(
      ratio_row[
          "revenue_cagr_5yr"
        ],
        "%"
    )
    )

    draw_kpi_tile(
    c,
    400,
    start_y - 90,
    tile_width,
    tile_height,
    "Net Margin",
    fmt(
        ratio_row[
            "net_profit_margin_pct"
        ],
        "%"
    )
    )

    #Embed Charts

    revenue_chart = create_revenue_chart(
        company_id
    )

    profit_chart = create_profit_chart(
    company_id
    )

    roe_roce_chart = create_roe_roce_chart(
    company_id
    )

    #Revenue (Left)
    c.setFont(
    "Helvetica-Bold",
    12
    )

    c.drawString(
    40,
    450,
    "Revenue Trend (10 Years)"
    )

    c.drawImage(
    revenue_chart,
    40,
    240,
    width=250,
    height=200
    )

    #Net Profit (Right)
    c.setFont(
    "Helvetica-Bold",
    12
    )

    c.drawString(
    300,
    450,
    "Net Profit Trend (10 Years)"
    )
    
    c.drawImage(
    profit_chart,
    300,
    240,
    width=250,
    height=200
    )

    #ROE vs ROCE
    c.setFont(
    "Helvetica-Bold",
    12
    )

    c.drawString(
    40,
    220,
    "ROE vs ROCE Trend (10 Years)"
    )
    
    c.drawImage(
    roe_roce_chart,
    30,
    20,
    width=510,
    height=180
    )

    # COMPANY ID

    c.setFillColor(
        colors.white
    )

    c.setFont(
        "Helvetica-Bold",
        24
    )

    c.drawString(
        40,
        height - 45,
        company_id
    )

    # COMPANY NAME

    c.setFont(
        "Helvetica",
        12
    )

    c.drawString(
        40,
        height - 65,
        str(company_name)
    )

    c.showPage()

    balance_chart = create_balance_sheet_chart(
    company_id
    )

    c.setFont(
    "Helvetica-Bold",
    14
    )

    c.drawString(
    40,
    height - 50,
    "Balance Sheet Composition"
    )

    c.drawImage(
    balance_chart,
    40,
    500,
    width=500,
    height=220
    )

    cashflow_chart = create_cashflow_waterfall(
    company_id
    )

    c.setFont(
    "Helvetica-Bold",
    12
    )

    c.drawString(
    40,
    450,
    "Cash Flow Waterfall"
    )

    if cashflow_chart:

       c.drawImage(
           cashflow_chart,
           40,
           220,
           width=500,
           height=180
        )

    pros, cons = get_pros_cons(
       company_id
    )

    capital_label = (
        get_capital_allocation_label(
           company_id
        )
    )

    c.setFont(
    "Helvetica-Bold",
    12
    )

    c.drawString(
    40,
    190,
    "Capital Allocation"
    )

    c.setFillColor(
        colors.HexColor("#D6EAF8")
    )

    c.roundRect(
        180,
        175,
        150,
        25,
        5,
        fill=1
    )

    c.setFillColor(
        colors.black
    )

    c.drawString(
        190,
        183,
        capital_label
    )

    c.setFillColor(colors.green)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 120, "Pros")

    c.setFont("Helvetica", 8)

    y = 100

    for pro in pros[:4]:

        text = pro[:55]

        c.drawString(
             40,
             y,
             f"• {text}"
        )

        y -= 15

    c.setFillColor(colors.red)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(300, 120, "Cons")

    c.setFont("Helvetica", 8)

    y = 100

    for con in cons[:4]:

        text = con[:55]

        c.drawString(
            300,
            y,
            f"• {text}"
        )

        y -= 15
    
    c.save()

    print(
       f"Generated: {pdf_path}"
    )
    
    
if __name__ == "__main__":

    test_companies = [
        "TCS",
        "HDFCBANK",
        "RELIANCE",
        "SUNPHARMA",
        "TATASTEEL"
    ]

    for company in test_companies:

        print(
            f"Generating {company}..."
        )

        generate_tearsheet(
            company
        )

    print(
        "\nDay 33 QA Complete"
    )

 