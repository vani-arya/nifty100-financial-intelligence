from pathlib import Path
import sqlite3
import traceback
import pandas as pd

from src.reports.tearsheet import (
    generate_tearsheet
)


DB_PATH = "data/nifty100.db"


def get_all_companies():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT company_id
        FROM sectors
        ORDER BY company_id
        """,
        conn
    )

    conn.close()

    return df["company_id"].unique().tolist()


def has_minimum_history(
    company_id
):

    conn = sqlite3.connect(DB_PATH)

    query = f"""
    SELECT COUNT(DISTINCT year)
    AS years
    FROM profitandloss
    WHERE company_id='{company_id}'
    """

    years = pd.read_sql(
        query,
        conn
    ).iloc[0]["years"]

    conn.close()

    return years >= 3


def main():

    skipped = []

    companies = get_all_companies()

    print(
        f"Companies Found: {len(companies)}"
    )

    for company in companies:

        try:

            if not has_minimum_history(
                company
            ):

                skipped.append({

                    "company_id":
                    company,

                    "reason":
                    "Less than 3 years data"
                })

                continue

            generate_tearsheet(
                company
            )

        except Exception as e:

            print(
                f"\nERROR: {company}"
            )

            traceback.print_exc()

            skipped.append({
                "company_id":
                company,

                "reason":
                str(e)
            })

    Path("output").mkdir(
        exist_ok=True
    )

    pd.DataFrame(
        skipped
    ).to_csv(
        "output/skipped_tearsheets.csv",
        index=False
    )

    print(
        f"\nSkipped: {len(skipped)}"
    )


if __name__ == "__main__":

    main()