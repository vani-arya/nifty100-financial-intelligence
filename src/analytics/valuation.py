import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

DB_PATH = "data/nifty100.db"


def load_data():

    conn = sqlite3.connect(DB_PATH)

    market = pd.read_sql(
        """
        SELECT *
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

    companies = pd.read_sql(
        """
        SELECT
            id,
            company_name
        FROM companies
        """,
        conn
    )

    ratios = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            free_cash_flow_cr
        FROM financial_ratios
        """,
        conn
    )

    conn.close()

    return market, sectors, companies, ratios


def get_latest_market_data(market):

    latest_year = market["year"].max()

    market_latest = market[
        market["year"] == latest_year
    ].copy()

    return market_latest


def get_latest_ratio_data(ratios):

    ratios["numeric_year"] = (
        ratios["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(float)
    )

    latest = (
        ratios.groupby("company_id")
        ["numeric_year"]
        .transform("max")
    )

    ratios = ratios[
        ratios["numeric_year"] == latest
    ].copy()

    ratios = ratios.drop_duplicates(
        subset=["company_id"]
    )

    return ratios


def calculate_sector_median_pe(df):

    sector_pe = (
        df.groupby("broad_sector")
        ["pe_ratio"]
        .median()
        .reset_index()
    )

    sector_pe.columns = [
        "broad_sector",
        "sector_median_pe"
    ]

    return sector_pe


def calculate_five_year_median_pe(market):

    median_pe = (
        market.groupby("company_id")
        ["pe_ratio"]
        .median()
        .reset_index()
    )

    median_pe.columns = [
        "company_id",
        "five_year_median_pe"
    ]

    return median_pe


def create_valuation_universe():

    market, sectors, companies, ratios = load_data()

    market_latest = get_latest_market_data(
        market
    )

    ratios_latest = get_latest_ratio_data(
        ratios
    )

    five_year_pe = (
        calculate_five_year_median_pe(
            market
        )
    )

    df = (
        market_latest
        .merge(
            sectors,
            on="company_id",
            how="left"
        )
        .merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left"
        )
        .merge(
            ratios_latest[
                [
                    "company_id",
                    "free_cash_flow_cr"
                ]
            ],
            on="company_id",
            how="left"
        )
    )

    sector_pe = calculate_sector_median_pe(df)

    df = df.merge(
        sector_pe,
        on="broad_sector",
        how="left"
    )

    df = df.merge(
        five_year_pe,
        on="company_id",
        how="left"
    )

    return df


def calculate_valuation_metrics(df):

    df["FCF_yield_pct"] = np.where(
        df["market_cap_crore"] > 0,
        (
            df["free_cash_flow_cr"]
            /
            df["market_cap_crore"]
        ) * 100,
        np.nan
    )

    df["PE_vs_sector_median_pct"] = (
        (
            df["pe_ratio"]
            -
            df["sector_median_pe"]
        )
        /
        df["sector_median_pe"]
    ) * 100

    conditions = [
        (
            df["pe_ratio"]
            >
            df["sector_median_pe"] * 1.5
        ),
        (
            df["pe_ratio"]
            <
            df["sector_median_pe"] * 0.7
        )
    ]

    choices = [
        "Caution",
        "Discount"
    ]

    df["flag"] = np.select(
        conditions,
        choices,
        default="Fair"
    )

    return df


def create_outputs(df):

    summary = df[
        [
            "company_id",
            "company_name",
            "broad_sector",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "FCF_yield_pct",
            "five_year_median_pe",
            "PE_vs_sector_median_pct",
            "flag"
        ]
    ].copy()

    summary.columns = [
        "company_id",
        "company_name",
        "sector",
        "P/E",
        "P/B",
        "EV/EBITDA",
        "FCF_yield_pct",
        "5yr_median_PE",
        "PE_vs_sector_median_pct",
        "flag"
    ]

    summary.to_excel(
        OUTPUT_DIR /
        "valuation_summary.xlsx",
        index=False
    )

    flags = df[
        df["flag"] != "Fair"
    ][
        [
            "company_id",
            "company_name",
            "broad_sector",
            "pe_ratio",
            "sector_median_pe",
            "PE_vs_sector_median_pct",
            "FCF_yield_pct",
            "flag"
        ]
    ]

    flags.to_csv(
        OUTPUT_DIR /
        "valuation_flags.csv",
        index=False
    )

    return summary, flags


def main():

    df = create_valuation_universe()

    df = calculate_valuation_metrics(
        df
    )

    summary, flags = create_outputs(df)

    print(
        "\nValuation Summary Rows:",
        len(summary)
    )

    print(
        "Unique Companies:",
        summary["company_id"].nunique()
    )

    print(
        "\nFlag Distribution:"
    )

    print(
        summary["flag"]
        .value_counts()
    )

    print(
        "\nFiles Generated:"
    )

    print(
        "output/valuation_summary.xlsx"
    )

    print(
        "output/valuation_flags.csv"
    )


if __name__ == "__main__":
    main()