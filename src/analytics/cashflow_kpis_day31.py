import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path

DB_PATH = "data/nifty100.db"

OUTPUT_FILE = "output/cashflow_intelligence.xlsx"

DISTRESS_FILE = "output/distress_alerts.csv"

def normalize_company_ids(df):

    if "company_id" in df.columns:

        df["company_id"] = (
            df["company_id"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    return df


def extract_year(year_text):

    import re

    match = re.search(
        r"(\d{4})",
        str(year_text)
    )

    if match:
        return int(match.group(1))

    return 0


def get_latest(df, company):

    company_df = (
        df[df["company_id"] == company]
        .sort_values("year_num")
    )

    if company_df.empty:
        return None

    return company_df.iloc[-1]


def get_last_n(df, company, n):

    return (
        df[df["company_id"] == company]
        .sort_values("year_num")
        .tail(n)
    )


def calculate_fcf_cagr(fcf_series):

    fcf_series = (
        fcf_series
        .dropna()
        .tolist()
    )

    if len(fcf_series) < 5:
        return None

    start = fcf_series[0]
    end = fcf_series[-1]

    if start <= 0:
        return None

    years = len(fcf_series) - 1

    try:

        cagr = (
            (
                end / start
            ) ** (1 / years)
            - 1
        ) * 100

        return round(cagr, 2)

    except:

        return None
    

def main():

    conn = sqlite3.connect(DB_PATH)

    profit = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    balance = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    sectors = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    conn.close()


    dfs = [
        profit,
        balance,
        cashflow,
        ratios,
        sectors
    ]

    for df in dfs:

        normalize_company_ids(df)

        if "year" in df.columns:

            df["year_num"] = (
                df["year"]
                .apply(extract_year)
            )

    profit = profit.drop_duplicates(
        subset=["company_id", "year"]
    )

    balance = balance.drop_duplicates(
        subset=["company_id", "year"]
    )

    cashflow = cashflow.drop_duplicates(
        subset=["company_id", "year"]
    )

    ratios = ratios.drop_duplicates(
        subset=["company_id", "year"]
    )


    output_rows = []

    distress_rows = []

    companies = sorted(
        profit["company_id"].unique()
    )


    for company in companies:

        latest_profit = get_latest(profit, company)
        latest_balance = get_latest(balance, company)
        latest_cashflow = get_latest(cashflow, company)
        latest_ratio = get_latest(ratios, company)

        sector_row = sectors[
            sectors["company_id"] == company
        ]

        sector = None

        if not sector_row.empty:
            sector = sector_row.iloc[0]["broad_sector"]

        # --------------------------------------------------
        # CFO QUALITY
        # --------------------------------------------------

        last5_cf = get_last_n(
            cashflow,
            company,
            5
        )

        last5_profit = get_last_n(
            profit,
            company,
            5
        )

        cfo_quality_score = None
        cfo_quality_label = None

        if (
            len(last5_cf) >= 3
            and
            len(last5_profit) >= 3
        ):

            merged = pd.merge(
                last5_cf[
                    [
                        "year",
                        "operating_activity"
                    ]
                ],
                last5_profit[
                    [
                        "year",
                        "net_profit"
                    ]
                ],
                on="year"
            )

            merged = merged[
                merged["net_profit"] != 0
            ]

            if not merged.empty:

                ratios_list = (
                    merged["operating_activity"]
                    /
                    merged["net_profit"]
                )

                cfo_quality_score = round(
                    ratios_list.mean(),
                    2
                )

                if cfo_quality_score > 1:

                    cfo_quality_label = (
                        "High Quality"
                    )

                elif cfo_quality_score >= 0.5:

                    cfo_quality_label = (
                        "Moderate"
                    )

                else:

                    cfo_quality_label = (
                        "Accrual Risk"
                    )

        # --------------------------------------------------
        # CAPEX INTENSITY
        # --------------------------------------------------

        capex_intensity_pct = None
        capex_label = None

        if (
            latest_cashflow is not None
            and
            latest_profit is not None
        ):

            sales = latest_profit["sales"]

            investing = abs(
                latest_cashflow[
                    "investing_activity"
                ]
            )

            if sales > 0:

                capex_intensity_pct = round(
                    investing / sales * 100,
                    2
                )

                if capex_intensity_pct < 3:

                    capex_label = (
                        "Asset Light"
                    )

                elif capex_intensity_pct <= 8:

                    capex_label = (
                        "Moderate"
                    )

                        # --------------------------------------------------
        # DISTRESS FLAG
        # --------------------------------------------------

        distress_flag = False

        if latest_cashflow is not None:

            if (
                latest_cashflow["operating_activity"] < 0
                and
                latest_cashflow["financing_activity"] > 0
            ):

                distress_flag = True

        # --------------------------------------------------
        # DELEVERAGING FLAG
        # --------------------------------------------------

        deleveraging_flag = False

        last2_balance = get_last_n(
            balance,
            company,
            2
        )

        if len(last2_balance) == 2:

            previous_borrowings = (
                last2_balance.iloc[0]["borrowings"]
            )

            latest_borrowings = (
                last2_balance.iloc[1]["borrowings"]
            )

            if (
                latest_cashflow is not None
                and
                latest_cashflow["financing_activity"] < 0
                and
                latest_borrowings < previous_borrowings
            ):

                deleveraging_flag = True

        # --------------------------------------------------
        # FCF CAGR
        # --------------------------------------------------

        fcf_cagr_5yr = None

        last5_ratios = get_last_n(
            ratios,
            company,
            5
        )

        if len(last5_ratios) >= 5:

            fcf_cagr_5yr = calculate_fcf_cagr(
                last5_ratios["free_cash_flow_cr"]
            )

        # --------------------------------------------------
        # FCF CONVERSION
        # --------------------------------------------------

        fcf_conversion_pct = None

        if latest_ratio is not None:

            cfo = latest_ratio[
                "cash_from_operations_cr"
            ]

            fcf = latest_ratio[
                "free_cash_flow_cr"
            ]

            if cfo != 0:

                fcf_conversion_pct = round(
                    fcf / cfo * 100,
                    2
                )

        # --------------------------------------------------
        # CAPITAL ALLOCATION
        # --------------------------------------------------

        capital_allocation_label = "Balanced"

        if distress_flag:

            capital_allocation_label = (
                "Distressed"
            )

        elif deleveraging_flag:

            capital_allocation_label = (
                "Deleveraging"
            )

        elif (
            capex_intensity_pct is not None
            and
            capex_intensity_pct > 8
        ):

            capital_allocation_label = (
                "Aggressive Reinvestment"
            )

        elif (
            fcf_conversion_pct is not None
            and
            fcf_conversion_pct > 70
        ):

            capital_allocation_label = (
                "Efficient Allocator"
            )

        # --------------------------------------------------
        # DISTRESS OUTPUT
        # --------------------------------------------------

        if distress_flag:

            distress_rows.append({

                "company_id":
                company,

                "sector":
                sector,

                "cfo_value":
                latest_cashflow[
                    "operating_activity"
                ],

                "cff_value":
                latest_cashflow[
                    "financing_activity"
                ],

                "latest_net_profit":
                latest_profit[
                    "net_profit"
                ]
            })


        output_rows.append({

            "company_id": company,
            "sector": sector,

            "cfo_quality_score":
            cfo_quality_score,

            "cfo_quality_label":
            cfo_quality_label,

            "capex_intensity_pct":
            capex_intensity_pct,

            "capex_label":
            capex_label,

            "fcf_cagr_5yr":
            fcf_cagr_5yr,

            "fcf_conversion_pct":
            fcf_conversion_pct,

            "distress_flag":
            distress_flag,

            "deleveraging_flag":
            deleveraging_flag,

            "capital_allocation_label":
            capital_allocation_label
        })

        print(
            company,
            cfo_quality_label,
            capital_allocation_label
        )
             

    output_df = pd.DataFrame(output_rows)

    distress_df = pd.DataFrame(distress_rows)

    Path("output").mkdir(
        exist_ok=True
    )

    output_df.to_excel(
        OUTPUT_FILE,
        index=False
    )

    distress_df.to_csv(
        DISTRESS_FILE,
        index=False
    )

    print("\nDay 31 Complete")

    print(
        f"Rows: {len(output_df)}"
    )

    print(
        f"Companies: {output_df['company_id'].nunique()}"
    )

    print(
        "\nCapital Allocation Labels:"
    )

    print(
        output_df[
            "capital_allocation_label"
        ].value_counts()
    )

    print(
        "\nDistress Flags:"
    )

    print(
        output_df[
            "distress_flag"
        ].value_counts()
    )


if __name__ == "__main__":

    print(
            "Starting Day 31 Cashflow Intelligence..."
        )

    main()

    

            




