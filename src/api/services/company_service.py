from src.api.database import get_connection
import pandas as pd

def get_companies(
    sector=None,
    market_cap_category=None,
    search=None
):

    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        MAX(r.return_on_equity_pct) AS return_on_equity_pct,
        MAX(r.return_on_capital_employed_pct)
            AS return_on_capital_employed_pct

    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN financial_ratios r
        ON c.id = r.company_id

    GROUP BY
        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector
    """

    params = []

    if sector:

        query += """
        AND s.broad_sector = ?
        """

        params.append(
            sector
        )

    if market_cap_category:

        query += """
        AND s.market_cap_category = ?
        """

        params.append(
            market_cap_category
        )

    if search:

        query += """
        AND (
            c.company_name LIKE ?
            OR c.id LIKE ?
        )
        """

        params.extend([
            f"%{search}%",
            f"%{search}%"
        ])

    df = conn.execute(
        query,
        params
    ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in df
    ]



def get_company_profile(
    ticker
):

    conn = get_connection()

    query = """
    SELECT
        c.*,
        s.*,
        r.*
    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN financial_ratios r
        ON c.id = r.company_id

    WHERE c.id = ?

    AND r.year = (
        SELECT MAX(year)
        FROM financial_ratios fr
        WHERE fr.company_id = c.id
    )
    """

    row = conn.execute(
        query,
        (ticker,)
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


def get_profit_loss_history(
    ticker,
    from_year=None,
    to_year=None
):

    conn = get_connection()

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(
        query,
        conn,
        params=[ticker]
    )

    conn.close()

    if df.empty:
        return []

    df = df[
        df["year"]
        .str.contains(r"\d{4}")
    ].copy()

    df["year_num"] = (
        df["year"]
        .str.extract(r"(\d{4})")
        .astype(int)
    )

    if from_year:

        df = df[
            df["year_num"] >= int(from_year)
        ]

    if to_year:

        df = df[
            df["year_num"] <= int(to_year)
        ]

    df = df.sort_values(
        "year_num"
    )

    df = df.drop(
        columns=["year_num"]
    )
    
    return df.to_dict(
        orient="records"
    )


def get_balance_sheet_history(
    ticker,
    from_year=None,
    to_year=None
):

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

    if df.empty:
        return []

    df = df[
        df["year"].str.contains(r"\d{4}")
    ].copy()

    df["year_num"] = (
        df["year"]
        .str.extract(r"(\d{4})")
        .astype(int)
    )

    if from_year:
        df = df[df["year_num"] >= int(from_year)]

    if to_year:
        df = df[df["year_num"] <= int(to_year)]

    df = df.sort_values("year_num")

    df = df.drop(columns=["year_num"])

    return df.to_dict(
        orient="records"
    )


def get_cashflow_history(
    ticker,
    from_year=None,
    to_year=None
):

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

    if df.empty:
        return []

    df = df[
        df["year"].str.contains(r"\d{4}")
    ].copy()

    df["year_num"] = (
        df["year"]
        .str.extract(r"(\d{4})")
        .astype(int)
    )

    if from_year:
        df = df[df["year_num"] >= int(from_year)]

    if to_year:
        df = df[df["year_num"] <= int(to_year)]

    df = df.sort_values("year_num")

    df = df.drop(columns=["year_num"])

    return df.to_dict(
        orient="records"
    )


def get_ratios_history(
    ticker,
    year=None
):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    if df.empty:
        return []

    if year:

        df = df[
            df["year"].str.contains(
                str(year)
            )
        ]

    import numpy as np

    df = df.replace(
        [np.nan],
        None
    )

    return df.to_dict(
       orient="records"
    )
