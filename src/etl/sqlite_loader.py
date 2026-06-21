import sqlite3
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.loader import load_dataset


DB_PATH = Path("data/nifty100.db")

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

    for table_name, file_name in TABLE_FILES.items():

        df = load_dataset(file_name)

        # Remove rows with invalid company_id values
        if table_name != "companies" and "company_id" in df.columns:

            original_rows = len(df)

            df = df[
                df["company_id"].isin(valid_ids)
            ]

            removed_rows = original_rows - len(df)

            if removed_rows > 0:
                print(
                    f"{table_name:<20} : "
                    f"{removed_rows} invalid FK rows removed"
                )

        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )

        print(
            f"{table_name:<20} : "
            f"{len(df)} rows loaded"
        )

    conn.commit()


def main():
    """Build nifty100.db and load all tables."""

    DB_PATH.parent.mkdir(exist_ok=True)

    conn = create_database()

    load_tables(conn)

    conn.close()

    print("\nDatabase created successfully.")
    print(f"Location: {DB_PATH}")


if __name__ == "__main__":
    main()