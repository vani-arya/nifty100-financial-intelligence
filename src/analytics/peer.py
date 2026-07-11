import sqlite3
import pandas as pd


def load_peer_groups():

    peer_df = pd.read_excel(
        "data/raw/peer_groups.xlsx"
    )

    return peer_df


def load_financial_data():

    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )

    conn.close()

    return df


def get_latest_year_data(df):

    temp = df.copy()

    temp["numeric_year"] = (
        temp["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(float)
    )

    latest = (
        temp.groupby("company_id")
        ["numeric_year"]
        .transform("max")
    )

    temp = temp[
        temp["numeric_year"] == latest
    ]

    temp = (
        temp.sort_values("id")
        .drop_duplicates(
            subset=["company_id"],
            keep="last"
        )
    )

    return temp


def merge_peer_groups():

    peer_df = load_peer_groups()

    financial_df = load_financial_data()

    financial_df = get_latest_year_data(
        financial_df
    )

    merged = financial_df.merge(
        peer_df,
        on="company_id",
        how="left"
    )

    return merged


def calculate_percentile_rank(
    df,
    metric,
    ascending=True
):

    temp = df.copy()

    temp["percentile_rank"] = (
        temp.groupby(
            "peer_group_name"
        )[metric]
        .rank(
            pct=True,
            ascending=ascending
        )
    )

    return temp


def calculate_peer_percentiles():

    df = merge_peer_groups()

    df = df[
        df["peer_group_name"]
        .notna()
    ]

    metrics = {
        "return_on_equity_pct": True,
        "return_on_capital_employed_pct": True,
        "net_profit_margin_pct": True,
        "debt_to_equity": False,
        "free_cash_flow_cr": True,
        "pat_cagr_5yr": True,
        "revenue_cagr_5yr": True,
        "eps_cagr_5yr": True,
        "interest_coverage": True,
        "asset_turnover": True
    }

    all_results = []

    for metric, ascending in metrics.items():

        temp = df.copy()

        temp["percentile_rank"] = (
            temp.groupby(
                "peer_group_name"
            )[metric]
            .rank(
                pct=True,
                ascending=ascending
            )
        )

        if metric == "debt_to_equity":

            temp["percentile_rank"] = (
                1
                -
                temp["percentile_rank"]
            )

        temp = temp[
            [
                "company_id",
                "peer_group_name",
                "year"
            ]
        ].copy()

        temp["metric"] = metric

        temp["value"] = df[metric]

        temp["percentile_rank"] = (
            temp.index.map(
                lambda x:
                calculate_percentile_rank(
                    df,
                    metric,
                    ascending
                )
                .loc[x, "percentile_rank"]
            )
        )

        all_results.append(temp)

    result = pd.concat(
        all_results,
        ignore_index=True
    )

    return result


def save_peer_percentiles():

    result = calculate_peer_percentiles()

    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    result.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print(
        "peer_percentiles saved"
    )





