import sqlite3
import time

from fastapi import APIRouter

router = APIRouter()

START_TIME = time.time()

DB_PATH = "data/nifty100.db"


@router.get("/health")
def health_check():

    conn = sqlite3.connect(DB_PATH)

    tables = [

        "analysis",
        "balancesheet",
        "cashflow",
        "companies",
        "documents",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "peer_percentiles",
        "profitandloss",
        "prosandcons",
        "sectors",
        "stock_prices"
    ]

    counts = {}

    for table in tables:

        try:

            count = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            counts[table] = count

        except Exception:

            counts[table] = "ERROR"

    conn.close()

    return {

        "status": "ok",

        "version": "1.0.0",

        "uptime_seconds":
        round(
            time.time() - START_TIME,
            2
        ),

        "db_row_counts":
        counts
    }