import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.loader import load_dataset
from src.etl.validator import (
    validate_primary_key_unique,
    validate_foreign_key,
    validate_annual_pk_unique,
    validate_year_format,
    validate_ticker_format,
    validate_balance_sheet_balance,
    validate_opm_cross_check,
    validate_positive_sales,
    validate_net_cash_check,
    validate_fixed_assets,
    validate_tax_rate,
    validate_dividend_payout,
    validate_url_format,
    validate_eps_consistency,
    validate_coverage,
    validate_strict_balance_sheet
)

print("=" * 60)
print("DQ-01 Company PK Uniqueness")

companies = load_dataset("companies.xlsx")

print(
    "Passed:",
    validate_primary_key_unique(
        companies,
        "id"
    )
) 

profitandloss = load_dataset("profitandloss.xlsx")

print("=" * 60)
print("DQ-02 Annual PK Uniqueness")

duplicates = validate_annual_pk_unique(
    profitandloss
)

print("Duplicate rows:", len(duplicates))

print("=" * 60)
print("DQ-03 FK Integrity")

invalid_fk = validate_foreign_key(
    profitandloss,
    "company_id",
    companies,
    "id"
)

print(
    "Violations:",
    len(invalid_fk)
)

print("=" * 60)
print("DQ-07 Year Format")

invalid_years = validate_year_format(
    profitandloss
)

print("Invalid year values:")
print(invalid_years)

print("=" * 60)
print("DQ-08 Ticker Format")

invalid_tickers = validate_ticker_format(
    profitandloss
)

print("Invalid tickers:")
print(invalid_tickers[:20])

from src.etl.validator import (
    validate_balance_sheet_balance
)

balancesheet = load_dataset(
    "balancesheet.xlsx"
)

invalid_balance = (
    validate_balance_sheet_balance(
        balancesheet
    )
)

print("=" * 60)
print("DQ-04 Balance Sheet Balance")
print(
    "Violations:",
    len(invalid_balance)
)


from src.etl.validator import (
    validate_opm_cross_check
)

invalid_opm = (
    validate_opm_cross_check(
        profitandloss
    )
)

print("=" * 60)
print("DQ-05 OPM Cross Check")
print("Violations:", len(invalid_opm))

for row in invalid_opm[:20]:
    print(row)

invalid_sales = (
    validate_positive_sales(
        profitandloss
    )
)

print("=" * 60)
print("DQ-06 Positive Sales")
print(
    "Violations:",
    len(invalid_sales)
)

cashflow = load_dataset(
    "cashflow.xlsx"
)

invalid_cash = (
    validate_net_cash_check(
        cashflow
    )
)

print("=" * 60)
print("DQ-09 Net Cash Check")
print(
    "Violations:",
    len(invalid_cash)
)

invalid_fixed_assets = validate_fixed_assets(
    balancesheet
)

print("=" * 60)
print("DQ-10 Fixed Assets")
print(
    "Violations:",
    len(invalid_fixed_assets)
)

invalid_tax = validate_tax_rate(
    profitandloss
)

print("=" * 60)
print("DQ-11 Tax Rate")
print(
    "Violations:",
    len(invalid_tax)
)

invalid_dividend = validate_dividend_payout(
    profitandloss
)

print("=" * 60)
print("DQ-12 Dividend Payout")
print(
    "Violations:",
    len(invalid_dividend)
)


documents = load_dataset(
    "documents.xlsx"
)

invalid_urls = validate_url_format(
    documents
)

print("=" * 60)
print("DQ-13 URL Validity")
print(
    "Violations:",
    len(invalid_urls)
)


invalid_eps = validate_eps_consistency(
    profitandloss
)

print("=" * 60)
print("DQ-14 EPS Sign Consistency")
print(
    "Violations:",
    len(invalid_eps)
)

coverage_issues = validate_coverage(
    profitandloss
)

invalid_strict_balance = (
    validate_strict_balance_sheet(
        balancesheet
    )
)

print("=" * 60)
print("DQ-15 Strict Balance Sheet Check")
print(
    "Violations:",
    len(invalid_strict_balance)
)

print("=" * 60)
print("DQ-16 Coverage Check")
print(
    "Violations:",
    len(coverage_issues)
)

