import re
import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

ANALYSIS_FILE = BASE_DIR / "data" / "raw" / "analysis.xlsx"
DB_FILE = BASE_DIR / "data" / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

PARSED_FILE = OUTPUT_DIR / "analysis_parsed.csv"
FAILURES_FILE = OUTPUT_DIR / "parse_failures.csv"
DIVERGENCE_FILE = OUTPUT_DIR / "cagr_divergence_review.csv"


PATTERN = re.compile(
    r"(TTM|Last Year|\d+\s*Years?|\d+\s*Year):?\s*(-?[\d.]+)%",
    re.IGNORECASE
)


METRIC_MAP = {
    "compounded_sales_growth": "sales_growth",
    "compounded_profit_growth": "profit_growth",
    "stock_price_cagr": "stock_price_cagr",
    "roe": "roe"
}


#Add Parsing Function
def parse_text(text):

    if pd.isna(text):
        return None

    text = str(text).strip()

    match = PATTERN.search(text)

    if not match:
        return None

    period = match.group(1).strip()
    value = float(match.group(2))

    if period.upper() == "TTM":
        years = 0

    elif period.upper() == "LAST YEAR":
        years = 1

    else:
        years = int(
            re.search(r"\d+", period).group()
        )

    return years, value


#Parse Analysis Sheet
def build_parsed_dataset():

    df = pd.read_excel(
        ANALYSIS_FILE,
        header=1
    )

    df["company_id"] = (
        df["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    parsed_rows = []
    failure_rows = []

    for _, row in df.iterrows():

        company = row["company_id"]

        for col, metric_type in METRIC_MAP.items():

            raw_text = row[col]

            result = parse_text(raw_text)

            if result is None:

                failure_rows.append(
                    {
                        "company_id": company,
                        "metric_type": metric_type,
                        "raw_text": raw_text,
                        "reason": "NO_REGEX_MATCH"
                    }
                )

                continue

            years, value = result

            parsed_rows.append(
                {
                    "company_id": company,
                    "metric_type": metric_type,
                    "period_years": years,
                    "value_pct": value
                }
            )

    parsed_df = pd.DataFrame(parsed_rows)
    failures_df = pd.DataFrame(failure_rows)

    if failures_df.empty:

       failures_df = pd.DataFrame(
        columns=[
            "company_id",
            "metric_type",
            "raw_text",
            "reason"
        ]
    )

    parsed_df.to_csv(
       PARSED_FILE,
       index=False
)

    failures_df.to_csv(
    FAILURES_FILE,
    index=False
)

    return parsed_df


#CAGR Validation
def validate_against_ratios(parsed_df):

    conn = sqlite3.connect(DB_FILE)

    ratios = pd.read_sql(
        """
        SELECT
            company_id,
            revenue_cagr_5yr,
            pat_cagr_5yr
        FROM financial_ratios
        """,
        conn
    )

    conn.close()

    ratios["company_id"] = (
        ratios["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    review_rows = []

    parsed_5yr = parsed_df[
        parsed_df["period_years"] == 5
    ]

    for _, row in parsed_5yr.iterrows():

        company = row["company_id"]

        ratio_row = ratios[
            ratios["company_id"] == company
        ]

        if ratio_row.empty:
            continue

        metric = row["metric_type"]

        if metric == "sales_growth":

            computed = ratio_row[
                "revenue_cagr_5yr"
            ].iloc[0]

        elif metric == "profit_growth":

            computed = ratio_row[
                "pat_cagr_5yr"
            ].iloc[0]

        else:
            continue

        parsed_value = row["value_pct"]

        diff = abs(
            parsed_value - computed
        )

        if diff > 5:

            review_rows.append(
                {
                    "company_id": company,
                    "metric_type": metric,
                    "parsed_value_pct": parsed_value,
                    "computed_value_pct": computed,
                    "difference_pct": round(diff, 2)
                }
            )

    review_df = pd.DataFrame(review_rows)

    if review_df.empty:

     review_df = pd.DataFrame(
        columns=[
            "company_id",
            "metric_type",
            "parsed_value_pct",
            "computed_value_pct",
            "difference_pct"
        ]
    )

    review_df.to_csv(
        DIVERGENCE_FILE,
        index=False
    )


#Main Block
if __name__ == "__main__":

    parsed_df = build_parsed_dataset()

    validate_against_ratios(parsed_df)

    print("\nDay 29 NLP Parser Complete\n")

    print(
        f"Parsed Rows: {len(parsed_df)}"
    )

    print(
        f"Output: {PARSED_FILE}"
    )

    print(
        f"Output: {FAILURES_FILE}"
    )

    print(
        f"Output: {DIVERGENCE_FILE}"
    )


