import os
import plotly.graph_objects as go
import sqlite3
import pandas as pd

def create_company_radar(
    company_id,
    df,
    merged_df
):

    metrics = get_radar_metrics()

    company_row = df[
        df["company_id"] == company_id
    ]

    if company_row.empty:
        return

    company_row = company_row.iloc[0]

    company_values = [
        company_row[m]
        for m in metrics
    ]

    peer_values = get_peer_average(
    company_id,
    df,
    merged_df
    )

    categories = [
        "ROE",
        "ROCE",
        "NPM",
        "D/E",
        "FCF",
        "PAT CAGR",
        "Revenue CAGR",
        "Composite Score"
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=company_values,
            theta=categories,
            fill="toself",
            name=company_id
        )
    )
    
    if peer_values is not None:

       fig.add_trace(
           go.Scatterpolar(
              r=peer_values,
              theta=categories,
              mode="lines",
              name="Peer Average",
              line=dict(
                dash="dash"
            )
        )
    )
       
    fig.update_layout(
        title=f"{company_id} Radar Chart",
        polar=dict(
            radialaxis=dict(
                visible=True
            )
        ),
        width=900,
        height=700
    )

    os.makedirs(
        "reports/radar_charts",
        exist_ok=True
    )

    fig.write_image(
        f"reports/radar_charts/{company_id}_radar.png"
    )


def load_latest_data():

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

    df["numeric_year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(float)
    )

    latest = (
        df.groupby("company_id")
        ["numeric_year"]
        .transform("max")
    )

    df = df[
        df["numeric_year"] == latest
    ]

    df = (
        df.sort_values("id")
        .drop_duplicates(
            subset=["company_id"],
            keep="last"
        )
    )

    return df


def load_peer_groups():

    peer_df = pd.read_excel(
        "data/raw/peer_groups.xlsx"
    )

    return peer_df


def get_radar_metrics():

    return [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "composite_quality_score"
    ]


def prepare_radar_data(df):

    metrics = get_radar_metrics()

    temp = df.copy()

    for metric in metrics:

        temp[metric] = (
            temp[metric]
            .fillna(
                temp[metric].median()
            )
        )

    return temp


def normalize_radar_metrics(df):

    metrics = get_radar_metrics()

    temp = df.copy()

    for metric in metrics:

        min_val = temp[metric].min()
        max_val = temp[metric].max()

        if max_val > min_val:

            temp[metric] = (
                (
                    temp[metric] - min_val
                )
                /
                (
                    max_val - min_val
                )
            ) * 100

    return temp


def get_peer_average(
    company_id,
    df,
    merged_df
):

    metrics = get_radar_metrics()

    peer_group = (
        merged_df.loc[
            merged_df["company_id"] == company_id,
            "peer_group_name"
        ]
        .iloc[0]
    )

    if pd.isna(peer_group):
        return None

    peer_companies = (
        merged_df[
            merged_df["peer_group_name"]
            == peer_group
        ]["company_id"]
    )

    peer_df = df[
        df["company_id"]
        .isin(peer_companies)
    ]

    return (
        peer_df[metrics]
        .mean()
        .tolist()
    )


def generate_all_radar_charts():

    df = load_latest_data()

    df = prepare_radar_data(df)

    df = normalize_radar_metrics(df)

    peer_df = load_peer_groups()

    merged_df = df.merge(
        peer_df[
            [
                "company_id",
                "peer_group_name"
            ]
        ],
        on="company_id",
        how="left"
    )

    companies = (
        df["company_id"]
        .unique()
    )

    for company in companies:

        try:

            create_company_radar(
                company,
                df,
                merged_df
            )

            print(
                f"Generated: {company}"
            )

        except Exception as e:

            print(
                f"Failed: {company}"
            )

            print(e)