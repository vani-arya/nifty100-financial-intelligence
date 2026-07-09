import pandas as pd
import numpy as np


def winsorize_series(series):

    p10 = series.quantile(0.10)

    p90 = series.quantile(0.90)

    return series.clip(
        lower=p10,
        upper=p90
    )


def scale_0_100(series):

    minimum = series.min()

    maximum = series.max()

    if minimum == maximum:

        return pd.Series(
            50,
            index=series.index
        )

    return (
        (series - minimum)
        /
        (maximum - minimum)
    ) * 100


def calculate_de_score(de):

    if pd.isna(de):
        return np.nan

    if de <= 0:
        return 100

    elif de <= 0.5:
        return 100 - ((de / 0.5) * 15)

    elif de <= 1:
        return 85 - (((de - 0.5) / 0.5) * 15)

    elif de <= 2:
        return 70 - (((de - 1) / 1) * 20)

    elif de <= 5:
        return 50 - (((de - 2) / 3) * 50)

    else:
        return 0


def calculate_icr_score(icr):

    if pd.isna(icr):
        return np.nan

    if icr < 1.5:
        return 0

    elif icr <= 3:
        return ((icr - 1.5) / 1.5) * 50

    elif icr <= 5:
        return 50 + (((icr - 3) / 2) * 25)

    elif icr <= 10:
        return 75 + (((icr - 5) / 5) * 25)

    else:
        return 100
    

def calculate_fcf_cagr(df):

    temp = df.copy()

    temp["numeric_year"] = (
        temp["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(float)
    )

    temp = temp.sort_values(
        ["company_id", "numeric_year"]
    )

    temp["fcf_cagr_5yr"] = np.nan

    for company in temp["company_id"].unique():

        company_df = temp[
            temp["company_id"] == company
        ]

        for idx in range(
            5,
            len(company_df)
        ):

            current_fcf = company_df.iloc[idx][
                "free_cash_flow_cr"
            ]

            base_fcf = company_df.iloc[idx - 5][
                "free_cash_flow_cr"
            ]

            if (
                pd.isna(current_fcf)
                or pd.isna(base_fcf)
                or base_fcf <= 0
                or current_fcf <= 0
            ):
                continue

            cagr = (
                (
                    current_fcf
                    / base_fcf
                ) ** (1 / 5)
                - 1
            ) * 100

            temp.loc[
                company_df.index[idx],
                "fcf_cagr_5yr"
            ] = cagr

    return temp
    
def calculate_composite_score(df):

    temp = df.copy()

    temp["cfo_pat_ratio"] = (
        temp["cash_from_operations_cr"]
        / temp["net_profit"]
    )

    temp.loc[
        temp["net_profit"] <= 0,
        "cfo_pat_ratio"
    ] = np.nan

    temp["fcf_positive_flag"] = np.where(
        temp["free_cash_flow_cr"] > 0,
        100,
        0
    )

    return temp


def calculate_cfo_pat_ratio(df):

    df["cfo_pat_ratio"] = (
        df["cash_from_operations_cr"]
        /
        df["net_profit"]
    )

    return df

def calculate_composite_score(df):

    result = df.copy()

    # --------------------
    # Profitability
    # --------------------

    result["roe_score"] = scale_0_100(
        winsorize_series(
            result["return_on_equity_pct"]
        )
    )

    result["roce_score"] = scale_0_100(
        winsorize_series(
            result[
                "return_on_capital_employed_pct"
            ]
        )
    )

    result["npm_score"] = scale_0_100(
        winsorize_series(
            result["net_profit_margin_pct"]
        )
    )

    result["profitability_score"] = (
        result["roe_score"] * 0.15
        +
        result["roce_score"] * 0.10
        +
        result["npm_score"] * 0.10
    )

    # --------------------
    # Cash Quality
    # --------------------

    result = calculate_fcf_cagr(result)

    result["cfo_pat_ratio"] = (
        result["cash_from_operations_cr"]
        /
        result["net_profit"]
    )

    result["fcf_cagr_score"] = scale_0_100(
    winsorize_series(
        result["fcf_cagr_5yr"]
    )
)

    result["fcf_cagr_score"] = (
        result["fcf_cagr_score"]
        .fillna(0)
)
    
    result["cfo_pat_score"] = scale_0_100(
        winsorize_series(
            result["cfo_pat_ratio"]
        )
    )

    result["cfo_pat_score"] = (
        result["cfo_pat_score"]
        .fillna(0)
)  
    
    result["fcf_positive_flag"] = np.where(
        result["free_cash_flow_cr"] > 0,
        100,
        0
    )

    result["cash_quality_score"] = (
        result["fcf_cagr_score"] * 0.15
        +
        result["cfo_pat_score"] * 0.10
        +
        result["fcf_positive_flag"] * 0.05
    )

    # --------------------
    # Growth
    # --------------------

    result["revenue_cagr_score"] = scale_0_100(
        winsorize_series(
            result["revenue_cagr_5yr"]
        )
    )

    result["cfo_pat_score"] = (
        result["cfo_pat_score"]
        .fillna(0)
)  
    
    result["pat_cagr_score"] = scale_0_100(
        winsorize_series(
            result["pat_cagr_5yr"]
        )
    )
    
    result["pat_cagr_score"] = (
        result["pat_cagr_score"]
       .fillna(0)
)
    
    result["cfo_pat_score"] = (
        result["cfo_pat_score"]
        .fillna(0)
)  
    
    result["growth_score"] = (
        result["revenue_cagr_score"].fillna(0) * 0.10
        +
        result["pat_cagr_score"].fillna(0) * 0.10
)

    # --------------------
    # Leverage
    # --------------------

    result["de_score"] = (
        result["debt_to_equity"]
        .apply(calculate_de_score)
    )

    result["icr_score"] = (
        result["interest_coverage"]
        .apply(calculate_icr_score)
    )

    result["leverage_score"] = (
        result["de_score"] * 0.10
        +
        result["icr_score"] * 0.05
    )

    # --------------------
    # Final Score
    # --------------------

    result["composite_quality_score"] = (
        result["profitability_score"]
        +
        result["cash_quality_score"]
        +
        result["growth_score"]
        +
        result["leverage_score"]
    )

    return result


def calculate_sector_relative_score(df):

    temp = df.copy()

    temp["sector_relative_score"] = (
        temp.groupby("broad_sector")
        ["composite_quality_score"]
        .transform(scale_0_100)
    )

    return temp