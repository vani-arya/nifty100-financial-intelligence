import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE financial_ratios
    ADD COLUMN return_on_capital_employed_pct REAL
    """)
except:
    pass

conn.commit()


pl = pd.read_sql("""
SELECT
    company_id,
    year,
    operating_profit,
    depreciation
FROM profitandloss
""", conn)

bs = pd.read_sql("""
SELECT
    company_id,
    year,
    equity_capital,
    reserves,
    borrowings
FROM balancesheet
""", conn)

companies = pd.read_sql("""
SELECT
    id,
    company_name,
    roce_percentage,
    roe_percentage
FROM companies
""", conn)

ratios = pd.read_sql("""
SELECT *
FROM financial_ratios
""", conn)


print("\nBEFORE DROP:")
print(
    [col for col in ratios.columns
     if "return_on_capital" in col]
)

if "return_on_capital_employed_pct" in ratios.columns:
    ratios = ratios.drop(
        columns=["return_on_capital_employed_pct"]
    )

print("\nAFTER DROP:")
print(
    [col for col in ratios.columns
     if "return_on_capital" in col]
)


sectors = pd.read_sql("""
SELECT
    company_id,
    broad_sector
FROM sectors
""", conn)


def calculate_roce(
    operating_profit,
    depreciation,
    equity_capital,
    reserves,
    borrowings
):

    ebit = operating_profit - depreciation

    capital_employed = (
        equity_capital +
        reserves +
        borrowings
    )

    if capital_employed <= 0:
        return None

    return round(
        (ebit / capital_employed) * 100,
        2
    )


roce_df = pl.merge(
    bs,
    on=["company_id", "year"],
    how="inner"
)


# Create ROCE column
roce_df["computed_roce"] = roce_df.apply(
    lambda row: calculate_roce(
        row["operating_profit"],
        row["depreciation"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    ),
    axis=1
)

# Check columns
print("\nROCE_DF COLUMNS:")
print(roce_df.columns.tolist())

# Check sample values
print(
    roce_df[
        ["company_id", "year", "computed_roce"]
    ].head()
)

# Create mapping dataframe
roce_map = (
    roce_df[
        [
            "company_id",
            "year",
            "computed_roce"
        ]
    ]
    .drop_duplicates(
        subset=["company_id", "year"]
    )
)

print("ROCE rows after dedupe:", len(roce_map))

print("Ratios rows before merge:", len(ratios))
print("ROCE rows:", len(roce_map))

duplicates = (
    roce_df
    .groupby(["company_id", "year"])
    .size()
    .reset_index(name="count")
)

duplicates = duplicates[
    duplicates["count"] > 1
]

print(duplicates.head(20))
print("\nDuplicate groups:", len(duplicates))


# Merge into financial_ratios
ratios = ratios.merge(
    roce_map,
    on=["company_id", "year"],
    how="left"
)


print("Ratios rows after merge:", len(ratios))


# Rename column
ratios.rename(
    columns={
        "computed_roce":
        "return_on_capital_employed_pct"
    },
    inplace=True
)

# Verify merge worked
print(
    ratios[
        [
            "company_id",
            "year",
            "return_on_capital_employed_pct"
        ]
    ].head()
)


log_file = open(
    "output/ratio_edge_cases.log",
    "w",
    encoding="utf-8"
)


#Create Validation Dataset
latest_ratios = (
    ratios
    .sort_values("year")
    .drop_duplicates(
        subset=["company_id"],
        keep="last"
    )
)

validation_df = latest_ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)


#Create Log File
log_file = open(
    "output/ratio_edge_cases.log",
    "w",
    encoding="utf-8"
)


#ROCE Validation

#temporary check
high_roce = roce_df[
    roce_df["computed_roce"] > 100
]

print(
    high_roce[
        [
            "company_id",
            "year",
            "operating_profit",
            "depreciation",
            "equity_capital",
            "reserves",
            "borrowings",
            "computed_roce"
        ]
    ].head(20)
)


for _, row in validation_df.iterrows():

    computed_roce = row[
        "return_on_capital_employed_pct"
    ]

    source_roce = row[
        "roce_percentage"
    ]

    if (
        pd.notna(computed_roce)
        and pd.notna(source_roce)
    ):

        difference = abs(
            computed_roce - source_roce
        )

        if difference > 5:

            log_file.write(
                f"ROCE_ANOMALY | "
                f"{row['company_id']} | "
                f"Computed={computed_roce:.2f} | "
                f"Source={source_roce:.2f} | "
                f"Difference={difference:.2f} | "
                f"CATEGORY=VERSION_DIFFERENCE\n"
            )


# ROE Validation
for _, row in validation_df.iterrows():

    computed_roe = row[
        "return_on_equity_pct"
    ]

    source_roe = row[
        "roe_percentage"
    ]

    if (
        pd.notna(computed_roe)
        and pd.notna(source_roe)
    ):

        difference = abs(
            computed_roe - source_roe
        )

        if difference > 5:

            category = (
                "DATA_SOURCE_ISSUE"
                if source_roe < 1
                else "VERSION_DIFFERENCE"
            )

            log_file.write(
                f"ROE_ANOMALY | "
                f"{row['company_id']} | "
                f"Computed={computed_roe:.2f} | "
                f"Source={source_roe:.2f} | "
                f"Difference={difference:.2f} | "
                f"CATEGORY={category}\n"
            )


#Financial Sector Carve-Out
financial_count = len(
    sectors[
        sectors["broad_sector"]
        == "Financials"
    ]
)

log_file.write(
    f"\nFINANCIAL_SECTOR_CARVEOUT | "
    f"{financial_count} companies excluded "
    f"from D/E warning flags\n"
)

log_file.close()



ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("\nfinancial_ratios table updated successfully")
print("\nDAY 13 SCRIPT REACHED END SUCCESSFULLY")