import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "data/nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def get_companies():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM companies
        ORDER BY company_name
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):

    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    """

    params = [ticker]

    if year:

        query += " AND year = ?"

        params.append(year)

    df = pd.read_sql(
        query,
        conn,
        params=params
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sectors():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM sectors
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM peer_percentiles
        WHERE peer_group_name = ?
        """,
        conn,
        params=[group_name]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_valuation(ticker):

    return pd.DataFrame()


@st.cache_data(ttl=600)
def get_home_metrics(year=None):

    conn = get_connection()

    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )

    conn.close()

    if year:

        ratios = ratios[
            ratios["year"]
            .astype(str)
            .str.contains(str(year))
        ]

    # Remove unrealistic ROE outliers
    roe = ratios["return_on_equity_pct"]

    roe = roe[
        (roe > -100) &
        (roe < 100)
    ]

    metrics = {
        "avg_roe":
            round(
                roe.mean(),
                2
            ),

        "median_de":
            round(
                ratios[
                    "debt_to_equity"
                ].median(),
                2
            ),

        "median_rev_cagr":
            round(
                ratios[
                    "revenue_cagr_5yr"
                ].median(),
                2
            ),

        "debt_free":
            (
                ratios[
                    "debt_to_equity"
                ] == 0
            ).sum()
    }

    return metrics


@st.cache_data(ttl=600)
def get_sector_breakdown():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT broad_sector,
               COUNT(*) as company_count
        FROM sectors
        GROUP BY broad_sector
        ORDER BY company_count DESC
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_top_companies():

    conn = get_connection()

    ratios = pd.read_sql(
        """
        SELECT company_id,
               composite_quality_score
        FROM financial_ratios
        """,
        conn
    )

    companies = pd.read_sql(
        """
        SELECT id,
               company_name
        FROM companies
        """,
        conn
    )

    conn.close()

    ratios = (
        ratios
        .sort_values(
            "composite_quality_score",
            ascending=False
        )
        .drop_duplicates(
            "company_id"
        )
        .head(5)
    )

    top = ratios.merge(
        companies,
        left_on="company_id",
        right_on="id",
        how="left"
    )

    return top


@st.cache_data(ttl=600)
def get_company_profile(ticker):

    conn = get_connection()

    company = pd.read_sql(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        conn,
        params=[ticker]
    )

    sector = pd.read_sql(
        """
        SELECT *
        FROM sectors
        WHERE company_id = ?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return company, sector


@st.cache_data(ttl=600)
def get_company_latest_ratios(ticker):

    df = get_ratios(ticker)

    if df.empty:
        return df

    df["numeric_year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(float)
    )

    latest_year = (
        df["numeric_year"]
        .max()
    )

    return df[
        df["numeric_year"]
        == latest_year
    ]


@st.cache_data(ttl=600)
def get_company_timeseries(ticker):

    pl = get_pl(ticker)

    ratios = get_ratios(ticker)

    return pl, ratios


@st.cache_data(ttl=600)
def search_company(search_text):

    companies = get_companies()

    if not search_text:
        return companies

    search_text = search_text.lower()

    return companies[
        companies["company_name"]
        .str.lower()
        .str.contains(search_text, na=False)
        |
        companies["id"]
        .str.lower()
        .str.contains(search_text, na=False)
    ]


@st.cache_data(ttl=600)
def get_pros_cons(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT pros,
               cons
        FROM prosandcons
        WHERE company_id = ?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df