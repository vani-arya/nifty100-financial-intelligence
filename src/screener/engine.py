import sqlite3
import pandas as pd
import yaml

def load_config():

    with open(
        "config/screener_config.yaml",
        "r"
    ) as f:

        return yaml.safe_load(f)
    

def load_data():

    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    pnl = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            sales,
            net_profit,
            opm_percentage
        FROM profitandloss
        """,
        conn
    )

    market = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            market_cap_crore,
            pe_ratio,
            pb_ratio,
            dividend_yield_pct
        FROM market_cap
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

    # Extract numeric year from "Mar 2024"
    ratios["join_year"] = (
        ratios["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(float)
    )

    pnl["join_year"] = (
        pnl["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(float)
    )

    market["join_year"] = market["year"].astype(float)

    # Merge P&L
    df = ratios.merge(
        pnl[
            [
                "company_id",
                "join_year",
                "sales",
                "net_profit",
                "opm_percentage"
            ]
        ],
        on=["company_id", "join_year"],
        how="left"
    )

    # Merge Market Cap
    df = df.merge(
        market[
            [
                "company_id",
                "join_year",
                "market_cap_crore",
                "pe_ratio",
                "pb_ratio",
                "dividend_yield_pct"
            ]
        ],
        on=["company_id", "join_year"],
        how="left"
    )

    # Merge Sector
    df = df.merge(
        sectors,
        on="company_id",
        how="left"
    )

    print("\nPE populated:", df["pe_ratio"].notna().sum())
    print("PB populated:", df["pb_ratio"].notna().sum())
    print("Dividend populated:", df["dividend_yield_pct"].notna().sum())

    print(
    df[
        [
            "company_id",
            "year",
            "pe_ratio",
            "pb_ratio",
            "dividend_yield_pct"
        ]
    ].dropna().head(10)
)


    duplicates = (
         df.groupby(
        ["company_id", "year"]
    )
    .size()
    .reset_index(name="count")
)

    print(
    duplicates[
        duplicates["count"] > 1
    ].head(20)
)

    return df


def apply_filters(
    df,
    filters
):

    # Financials carve-out for D/E

    if filters.get("max_de") is not None:

        financials = df[
            df["broad_sector"] == "Financials"
        ]

        others = df[
            df["broad_sector"] != "Financials"
        ]

        others = others[
            others["debt_to_equity"]
            <= filters["max_de"]
        ]

        df = pd.concat(
            [financials, others]
        )

    # Debt-free ICR handling

    df["interest_coverage"] = (
        df["interest_coverage"]
        .fillna(float("inf"))
    )

    if filters.get("min_icr") is not None:

        df = df[
            df["interest_coverage"]
            >= filters["min_icr"]
        ]

    if filters.get("min_roe") is not None:

        df = df[
            df["return_on_equity_pct"]
            >= filters["min_roe"]
        ]

    if filters.get("min_fcf") is not None:

        df = df[
            df["free_cash_flow_cr"]
            >= filters["min_fcf"]
        ]

    if filters.get("min_revenue_cagr_5yr") is not None:

        df = df[
            df["revenue_cagr_5yr"]
            >= filters["min_revenue_cagr_5yr"]
        ]

    if filters.get("min_pat_cagr_5yr") is not None:

        df = df[
            df["pat_cagr_5yr"]
            >= filters["min_pat_cagr_5yr"]
        ]

    if filters.get("min_opm") is not None:

        df = df[
            df["opm_percentage"]
            >= filters["min_opm"]
        ]

    if filters.get("max_pe") is not None:

        df = df[
            df["pe_ratio"]
            <= filters["max_pe"]
        ]

    if filters.get("max_pb") is not None:

        df = df[
            df["pb_ratio"]
            <= filters["max_pb"]
        ]

    if filters.get("min_dividend_yield") is not None:

        df = df[
            df["dividend_yield_pct"]
            >= filters["min_dividend_yield"]
        ]

    if filters.get("min_market_cap") is not None:

        df = df[
            df["market_cap_crore"]
            >= filters["min_market_cap"]
        ]

    if filters.get("min_net_profit") is not None:

        df = df[
            df["net_profit"]
            >= filters["min_net_profit"]
        ]

    if filters.get("min_eps_cagr") is not None:

        df = df[
            df["eps_cagr_5yr"]
            >= filters["min_eps_cagr"]
        ]

    if filters.get("min_asset_turnover") is not None:

        df = df[
            df["asset_turnover"]
            >= filters["min_asset_turnover"]
        ]

    if filters.get("min_sales") is not None:

        df = df[
            df["sales"]
            >= filters["min_sales"]
        ]

    df = df.sort_values(
        "composite_quality_score",
        ascending=False
    )

    return df



def run_screener():

    config = load_config()

    df = load_data()

    result = apply_filters(
        df,
        config["filters"]
    )

    return result

if __name__ == "__main__":

    result = run_screener()

    print("\nRows:", len(result))
    
    print("\nColumns:")
    print(result.columns.tolist())

    print(
    "\nDividend Yield Nulls:",
    result["dividend_yield_pct"].isna().sum()
)

   
    print(result.head())

    print(
        "\nRows:",
        len(result)
    )