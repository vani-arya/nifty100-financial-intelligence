import pandas as pd


def validate_not_empty(df):
    """
    Dataset must contain at least one row.
    """
    return len(df) > 0


def validate_required_columns(df, required_columns):
    """
    Check whether required columns exist.
    """
    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    return missing


def validate_primary_key_not_null(df, key_column):
    """
    Primary key cannot contain null values.
    """
    return df[key_column].isnull().sum() == 0


def validate_primary_key_unique(df, key_column):
    """
    Primary key must be unique.
    """
    return df[key_column].nunique() == len(df)


def validate_foreign_key(
    child_df,
    child_column,
    parent_df,
    parent_column
):
    invalid_keys = (
        set(child_df[child_column])
        - set(parent_df[parent_column])
    )

    return invalid_keys


def validate_no_duplicate_rows(df):
    return df.duplicated().sum() == 0


def validate_null_percentage(
    df,
    threshold=20
):
    result = {}

    for column in df.columns:
        null_pct = (
            df[column]
            .isnull()
            .mean()
            * 100
        )

        if null_pct > threshold:
            result[column] = round(
                null_pct,
                2
            )

    return result


def find_reporting_period_anomalies(df):
    anomalies = df[
        (
            df["year"].astype(str) == "Mar 2023 15"
        )
    ]

    return anomalies


def validate_positive_values(df, columns):
    failures = {}

    for column in columns:
        if column in df.columns:
            invalid = df[df[column] < 0]

            if not invalid.empty:
                failures[column] = len(invalid)

    return failures


def validate_min_row_count(
    df,
    expected_min
):
    return len(df) >= expected_min


def validate_company_id_format(df):
    invalid = []

    for company_id in df["id"]:
        if not str(company_id).strip():
            invalid.append(company_id)

    return invalid


def validate_annual_pk_unique(
    df,
    company_col="company_id",
    year_col="year"
):
    duplicates = df.duplicated(
        subset=[company_col, year_col]
    )

    return df[duplicates]


import re

def validate_year_format(df):
    valid_patterns = [
        r"^(Mar|Jun|Sep|Dec)\s\d{4}$",
        r"^(Mar|Jun|Sep|Dec)-\d{2}$",
        r"^\d{4}$",
        r"^TTM$",
        r"^(Mar|Jun|Sep|Dec)\s\d{4}\s9m$",
        r"^\d{4}\.5$"
    ]

    invalid = []

    for value in (
        df["year"]
        .dropna()
        .astype(str)
        .unique()
    ):
        if not any(
            re.match(pattern, value)
            for pattern in valid_patterns
        ):
            invalid.append(value)

    return invalid


def validate_ticker_format(
    df,
    column="company_id"
):
    invalid = []

    for value in df[column].dropna():
        if value != value.strip().upper():
            invalid.append(value)

    return invalid


def validate_balance_sheet_balance(
    df,
    tolerance=0.01
):
    invalid_rows = []

    for _, row in df.iterrows():

        assets = row["total_assets"]
        liabilities = row["total_liabilities"]

        if pd.isna(assets) or pd.isna(liabilities):
            continue

        if assets == 0:
            continue

        diff_pct = abs(
            assets - liabilities
        ) / assets

        if diff_pct > tolerance:
            invalid_rows.append(
                {
                    "company_id": row["company_id"],
                    "year": row["year"],
                    "difference_pct": round(
                        diff_pct * 100,
                        2
                    )
                }
            )

    return invalid_rows


def validate_opm_cross_check(
    df,
    tolerance=1.0
):
    invalid_rows = []

    for _, row in df.iterrows():

        sales = row["sales"]
        operating_profit = row["operating_profit"]
        reported_opm = row["opm_percentage"]

        if pd.isna(sales):
            continue

        if pd.isna(operating_profit):
            continue

        if pd.isna(reported_opm):
            continue

        if sales == 0:
            continue

        calculated_opm = (
            operating_profit / sales
        ) * 100

        diff = abs(
            calculated_opm - reported_opm
        )

        if diff > tolerance:

            invalid_rows.append(
                {
                    "company_id": row["company_id"],
                    "year": row["year"],
                    "reported_opm": reported_opm,
                    "calculated_opm": round(
                        calculated_opm,
                        2
                    )
                }
            )

    return invalid_rows


def validate_positive_sales(df):
    invalid = df[
        df["sales"] <= 0
    ]

    return invalid


def validate_net_cash_check(
    df,
    tolerance=1
):
    invalid_rows = []

    for _, row in df.iterrows():

        operating = row["operating_activity"]
        investing = row["investing_activity"]
        financing = row["financing_activity"]
        reported = row["net_cash_flow"]

        if pd.isna(operating):
            continue

        if pd.isna(investing):
            continue

        if pd.isna(financing):
            continue

        if pd.isna(reported):
            continue

        calculated = (
            operating
            + investing
            + financing
        )

        if abs(calculated - reported) > tolerance:

            invalid_rows.append(
                {
                    "company_id": row["company_id"],
                    "year": row["year"]
                }
            )

    return invalid_rows


def validate_fixed_assets(df):
    invalid = df[
        df["fixed_assets"] < 0
    ]

    return invalid


def validate_tax_rate(df):
    invalid = df[
        (
            df["tax_percentage"] < 0
        )
        |
        (
            df["tax_percentage"] > 60
        )
    ]

    return invalid


def validate_dividend_payout(df):
    invalid = df[
        df["dividend_payout"] > 200
    ]

    return invalid


def validate_url_format(df):
    invalid = []

    for url in df["Annual_Report"].dropna():

        url = str(url)

        if not (
            url.startswith("http://")
            or
            url.startswith("https://")
        ):
            invalid.append(url)

    return invalid


def validate_eps_consistency(df):
    invalid = []

    for _, row in df.iterrows():

        net_profit = row["net_profit"]
        eps = row["eps"]

        if pd.isna(net_profit):
            continue

        if pd.isna(eps):
            continue

        if net_profit > 0 and eps < 0:
            invalid.append(row["company_id"])

        if net_profit < 0 and eps > 0:
            invalid.append(row["company_id"])

    return invalid


def validate_coverage(
    df,
    min_years=5
):
    counts = (
        df.groupby("company_id")
        .size()
    )

    return counts[
        counts < min_years
    ]


def validate_strict_balance_sheet(df):
    invalid = df[
        df["total_assets"]
        !=
        df["total_liabilities"]
    ]

    return invalid


