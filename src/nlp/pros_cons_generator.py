import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "data/nifty100.db"

OUTPUT_FILE = "output/pros_cons_generated.csv"


def add_record(
    company_records,
    company,
    rec_type,
    rule_id,
    text,
    confidence
):

    company_records.append(
        {
            "company_id": company,
            "type": rec_type,
            "rule_id": rule_id,
            "text": text,
            "confidence_pct": confidence
        }
    )


def latest_rows(df):

    return (
        df.sort_values("year_num")
        .groupby("company_id")
        .tail(1)
    )


def last_n(df, company, n):

    temp = (
        df[
            df["company_id"] == company
        ]
        .sort_values("year_num")
    )

    temp = (
        temp
        .drop_duplicates(
            subset=["year_num"],
            keep="last"
        )
    )

    return temp.tail(n)


def prepare_years(df):

    df = df.copy()

    df["year_num"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")
        .astype(float)
    )

    return df



def main():

    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    pl = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    bs = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    sectors = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    market = pd.read_sql(
        "SELECT * FROM market_cap",
        conn
    )

    conn.close()
    
    
    ratios = prepare_years(ratios)
    pl = prepare_years(pl)
    bs = prepare_years(bs)
    market = prepare_years(market)



    # Normalize IDs

    for df in [
        ratios,
        pl,
        bs,
        sectors,
        market
    ]:

        if "company_id" in df.columns:

            df["company_id"] = (
                df["company_id"]
                .astype(str)
                .str.strip()
                .str.upper()
            )

    latest_ratios = latest_rows(ratios)
    latest_pl = latest_rows(pl)
    latest_bs = latest_rows(bs)
    latest_market = latest_rows(market)

    companies = sorted(
        set(pl["company_id"])
    )

    records = []

    for company in companies:

        company_records = []

        # fetch latest rows safely

        ratio_row = latest_ratios[
            latest_ratios["company_id"] == company
        ]

        pl_row = latest_pl[
            latest_pl["company_id"] == company
        ]

        bs_row = latest_bs[
            latest_bs["company_id"] == company
        ]

        market_row = latest_market[
            latest_market["company_id"] == company
        ]

        sector_row = sectors[
            sectors["company_id"] == company
        ]

        sector = None

        if not sector_row.empty:
            sector = sector_row.iloc[0]["broad_sector"]

        # ------------------------------------------------
        # PRO RULES
        # ------------------------------------------------

        # PRO_01
        last3 = last_n(
            ratios,
            company,
            3
        )

        if (
            len(last3) == 3
            and
            (
                last3[
                    "return_on_equity_pct"
                ] > 20
            ).all()
        ):

            company_records.append({
                "company_id": company,
                "type": "pro",
                "rule_id": "PRO_01",
                "text":
                "Consistently high return on equity above 20% demonstrates exceptional capital efficiency",
                "confidence_pct": 90
            })

        # PRO_02

        last5 = last_n(
            ratios,
            company,
            5
        )

        if (
            len(last5) == 5
            and
            (
                last5[
                    "free_cash_flow_cr"
                ] > 0
            ).all()
        ):

            company_records.append({
                "company_id": company,
                "type": "pro",
                "rule_id": "PRO_02",
                "text":
                "Strong free cash flow generation over 5 years signals healthy business fundamentals",
                "confidence_pct": 85
            })

        #PRO_03

        if (
            not ratio_row.empty
            and
            ratio_row.iloc[0]["debt_to_equity"] == 0
        ):

         add_record(
            company_records,
            company,
            "pro",
            "PRO_03",
            "Debt-free balance sheet provides financial flexibility and eliminates interest burden",
            95
        )
        
        #PRO_04

        if (
            not ratio_row.empty
            and
            ratio_row.iloc[0]["revenue_cagr_5yr"] > 15
        ):

         add_record(
            company_records,
            company,
            "pro",
            "PRO_04",
            "Revenue growing at above 15% CAGR over 5 years reflects strong business momentum",
            85
        )
         
        #PRO_05

        if (
            not ratio_row.empty
            and
            ratio_row.iloc[0]["operating_profit_margin_pct"] > 25
        ):

         add_record(
            company_records,
            company,
            "pro",
            "PRO_05",
            "Operating profit margin above 25% indicates strong pricing power and cost discipline",
            85
        )
         
        #PRO_06

        if (
           not ratio_row.empty
           and
           ratio_row.iloc[0]["pat_cagr_5yr"] > 20
        ):

         add_record(
            company_records,
            company,
            "pro",
            "PRO_06",
            "Net profit compounding at above 20% over 5 years creates significant shareholder value",
            90
        )
         
        #PRO_07

        if (
           not ratio_row.empty
           and
           (
               ratio_row.iloc[0]["interest_coverage"] > 10
               or
               ratio_row.iloc[0]["debt_to_equity"] == 0
            )
        ):

         add_record(
            company_records,
            company,
            "pro",
            "PRO_07",
            "Very high interest coverage ratio reflects negligible financial stress from debt servicing",
            85
        )
         
        #PRO_08

        if (
           not ratio_row.empty
           and
           not market_row.empty
           and
           market_row.iloc[0]["dividend_yield_pct"] > 2
           and
           ratio_row.iloc[0]["free_cash_flow_cr"] > 0
        ):

         add_record(
            company_records,
            company,
            "pro",
            "PRO_08",
            "Consistent dividend yield above 2% backed by positive free cash flow",
            80
        )
         
        #PRO_09

        if (
           not ratio_row.empty
           and
           ratio_row.iloc[0]["eps_cagr_5yr"] > 15
        ):

         add_record(
            company_records,
            company,
            "pro",
            "PRO_09",
            "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding",
            85
        )
         
        #PRO_10

        roe = last3["return_on_equity_pct"]

        if (
           len(roe) == 3
           and
           roe.iloc[0] < roe.iloc[1] < roe.iloc[2]
        ):

         add_record(
            company_records,
            company,
            "pro",
            "PRO_10",
            "Return on equity improving for 3 consecutive years shows strengthening business quality",
            80
        )
         
        #PRO_11

        if (
           not ratio_row.empty
           and
           ratio_row.iloc[0]["pat_cagr_5yr"]
           >
           ratio_row.iloc[0]["revenue_cagr_5yr"]
        ):

         add_record(
            company_records,
            company,
            "pro",
            "PRO_11",
            "Revenue growing slower than profits shows improving operating leverage and scale benefits",
            80
        )
         
        #PRO_12

        last3_bs = last_n(
            bs,
            company,
            3
        )

        if len(last3_bs) == 3:

           assets = last3_bs["total_assets"]
           debt = last3_bs["borrowings"]

           if (
               assets.iloc[0] < assets.iloc[-1]
               and
               debt.iloc[0] > debt.iloc[-1]
            ):

             add_record(
                company_records,
                company,
                "pro",
                "PRO_12",
                "Growing asset base funded by internal accruals reflects self-sustaining growth",
                85
            )
             
        # ------------------------------------------------
        # CON RULES
        # ------------------------------------------------

        #CON_01

        if (
            not ratio_row.empty
            and
            sector != "Financials"
            and
            ratio_row.iloc[0]["debt_to_equity"] > 2
        ):

         add_record(
            company_records,
            company,
            "con",
            "CON_01",
            f"Debt-to-equity ratio of {round(ratio_row.iloc[0]['debt_to_equity'],2)} is elevated for a non-financial company and warrants monitoring",
            85
        )
         
        #CON_02

        last3 = last_n(
        ratios,
        company,
        3
        )

        if (
            len(last3) == 3
            and
            (
                last3["free_cash_flow_cr"] < 0
            ).all()
        ):

         add_record(
            company_records,
            company,
            "con",
            "CON_02",
            "Free cash flow negative for 3 consecutive years raises concern about cash generation quality",
            85
        )
         
        #CON_03

        opm = last3[
            "operating_profit_margin_pct"
        ]

        if (
            len(opm) == 3
            and
            opm.iloc[0] > opm.iloc[1] > opm.iloc[2]
        ):

            add_record(
               company_records,
               company,
               "con",
               "CON_03",
               "Operating margins declining for 3 consecutive years suggest pricing or cost pressure",
               80
            )

        #CON_04

        if (
           not pl_row.empty
           and
           pl_row.iloc[0]["net_profit"] < 0
        ):

         add_record(
            company_records,
            company,
            "con",
            "CON_04",
            "Company reported a net loss in the most recent financial year",
            90
        )
         
        #CON_05

        last2_pl = last_n(
            pl,
            company,
            2
        )

        if len(last2_pl) == 2:

            sales = last2_pl["sales"]

            if sales.iloc[0] > sales.iloc[1]:

                add_record(
                    company_records,
                    company,
                    "con",
                    "CON_05",
                    "Revenue contraction over 2 consecutive years indicates demand weakness or market share loss",
                    80
                )

        #CON_06       

        if (
           not ratio_row.empty
           and
           ratio_row.iloc[0]["interest_coverage"] < 1.5
        ):

           add_record(
              company_records,
              company,
              "con",
              "CON_06",
              "Interest coverage ratio below 1.5x indicates the company is at risk of not meeting its debt obligations",
              90
            )
        
        #CON_07

        if (
           not ratio_row.empty
           and
           ratio_row.iloc[0]["dividend_payout_ratio_pct"] > 100
        ):

           add_record(
              company_records,
              company,
              "con",
              "CON_07",
              "Dividend payout ratio above 100% means the company is paying dividends from reserves, which is unsustainable",
               85
            )
           
        #CON_08

        de = last3["debt_to_equity"]

        if (
           len(de) == 3
           and
           de.iloc[0] < de.iloc[1] < de.iloc[2]
        ):

         add_record(
            company_records,
            company,
            "con",
            "CON_08",
            "Rising debt-to-equity ratio over 3 years suggests increasing financial leverage risk",
            80
        )
         
        #CON_09

        eps = last3["earnings_per_share"]

        if (
           len(eps) == 3
           and
           eps.iloc[0] > eps.iloc[1] > eps.iloc[2]
        ):

         add_record(
            company_records,
            company,
            "con",
            "CON_09",
            "Earnings per share declining for 3 consecutive years reflects deteriorating profitability",
            85
        )
         
        #Add CON_10

        if (
           not ratio_row.empty
           and
           ratio_row.iloc[0]["return_on_capital_employed_pct"] < 10
        ):

         add_record(
            company_records,
            company,
            "con",
            "CON_10",
            "Return on capital employed below 10% suggests the business is not generating sufficient returns on invested capital",
            85
        )
         
        #Add CON_11

        if (
           not ratio_row.empty
           and
           ratio_row.iloc[0]["cash_from_operations_cr"] > 0
           and
           ratio_row.iloc[0]["total_debt_cr"]
           >
           (
              3
              *
              ratio_row.iloc[0]["cash_from_operations_cr"]
            )
        ):

         add_record(
            company_records,
            company,
            "con",
            "CON_11",
            "High debt burden relative to cash generation limits financial flexibility",
            80
        )
         
        #CON_12

        if (
            not ratio_row.empty
            and
            ratio_row.iloc[0]["revenue_cagr_5yr"] < 5
        ):

         add_record(
            company_records,
            company,
            "con",
            "CON_12",
            "Revenue growing at below 5% over 5 years lags inflation and suggests limited business momentum",
            80
        )

        # ------------------------------------------------
        # FALLBACKS
        # ------------------------------------------------

        pros = [
            r
            for r in company_records
            if r["type"] == "pro"
        ]

        cons = [
            r
            for r in company_records
            if r["type"] == "con"
        ]

        if len(pros) == 0:

            company_records.append({
                "company_id": company,
                "type": "pro",
                "rule_id": "PRO_FALLBACK",
                "text":
                "Company continues to maintain an active operating business with reported financial disclosures.",
                "confidence_pct": 65
            })

        if len(cons) == 0:

            company_records.append({
                "company_id": company,
                "type": "con",
                "rule_id": "CON_FALLBACK",
                "text":
                "Limited available financial signals reduce confidence in a comprehensive assessment.",
                "confidence_pct": 65
            })

        records.extend(
            company_records
        )

    output_df = pd.DataFrame(records)

    Path("output").mkdir(
        exist_ok=True
    )

    output_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nRows: {len(output_df)}"
    )

    print(
        f"Companies: {output_df['company_id'].nunique()}"
    )

    print(
        "\nType Distribution:"
    )

    print(
        output_df[
            "type"
        ].value_counts()
    )

    print(
        f"\nSaved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()