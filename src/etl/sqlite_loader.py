import sqlite3
import time
import pandas as pd
from pathlib import Path
import sys
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.loader import load_dataset


DB_PATH = Path("data/nifty100.db")

AUDIT_PATH = Path(
    "src/etl/audit/load_audit.csv"
)

TABLE_FILES = {
    "companies": "companies.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "documents": "documents.xlsx",
    "prosandcons": "prosandcons.xlsx",
    "sectors": "sectors.xlsx",
    "market_cap": "market_cap.xlsx",
    "stock_prices": "stock_prices.xlsx",
    "financial_ratios": "financial_ratios.xlsx",
    "peer_groups": "peer_groups.xlsx"
}


def create_database():
    """Create SQLite database from schema.sql."""

    conn = sqlite3.connect(DB_PATH)

    conn.execute("PRAGMA foreign_keys = ON")

    schema_path = Path(__file__).parent / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as file:
        conn.executescript(file.read())

    conn.commit()

    return conn


def load_tables(conn):
    """Load all datasets into SQLite tables."""

    companies_df = load_dataset("companies.xlsx")
    valid_ids = set(companies_df["id"])

    audit_rows = []

    for table_name, file_name in TABLE_FILES.items():
        start_time = time.time()

        df = load_dataset(file_name)

        rows_in = len(df)
        rejected = 0

        if table_name != "companies" and "company_id" in df.columns:

            original_rows = len(df)

            df = df[
                df["company_id"].isin(valid_ids)
            ]

            rejected = original_rows - len(df)

            if rejected > 0:
                print(
                    f"{table_name:<20} : "
                    f"{rejected} invalid FK rows removed"
                )

        rows_out = len(df)

        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )

        print(
            f"{table_name:<20} : "
            f"{rows_out} rows loaded"
        )

        runtime_s = round(
         time.time() - start_time,
    4
)

        audit_rows.append({
    "table": table_name,
    "rows_in": rows_in,
    "rows_out": rows_out,
    "rejected": rejected,
    "timestamp": datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
    "runtime_s": runtime_s
})

    audit_df = pd.DataFrame(audit_rows)

    AUDIT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    audit_df.to_csv(
        AUDIT_PATH,
        index=False
    )

    print("\nload_audit.csv generated")

    conn.commit()


def main():
    """Build nifty100.db and load all tables."""

    DB_PATH.parent.mkdir(exist_ok=True)

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = create_database()

    load_tables(conn)

    conn.close()

    print("\nDatabase created successfully.")
    print(f"Location: {DB_PATH}")


if __name__ == "__main__":
    main()