import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.loader import load_dataset
from src.etl.validator import (
validate_foreign_key,
validate_annual_pk_unique,
validate_year_format,
validate_ticker_format,
validate_opm_cross_check,
validate_positive_sales,
validate_net_cash_check,
validate_tax_rate,
validate_dividend_payout,
validate_url_format,
validate_eps_consistency,
validate_coverage
)

failures = []

companies = load_dataset("companies.xlsx")
profitandloss = load_dataset("profitandloss.xlsx")
balancesheet = load_dataset("balancesheet.xlsx")
cashflow = load_dataset("cashflow.xlsx")
financial_ratios = load_dataset("financial_ratios.xlsx")
documents = load_dataset("documents.xlsx")

# DQ-02 Annual PK Uniqueness

duplicates = validate_annual_pk_unique(profitandloss)

failures.append({
"rule": "DQ-02",
"dataset": "profitandloss",
"failure_count": len(duplicates)
})

# DQ-03 FK Integrity

invalid_fk = validate_foreign_key(
profitandloss,
"company_id",
companies,
"id"
)

failures.append({
"rule": "DQ-03",
"dataset": "profitandloss",
"failure_count": len(invalid_fk)
})

# DQ-05 OPM Cross Check

opm_failures = validate_opm_cross_check(
profitandloss
)

failures.append({
"rule": "DQ-05",
"dataset": "profitandloss",
"failure_count": len(opm_failures)
})

# DQ-06 Positive Sales

sales_failures = validate_positive_sales(
profitandloss
)

failures.append({
"rule": "DQ-06",
"dataset": "profitandloss",
"failure_count": len(sales_failures)
})

# DQ-07 Year Format

year_failures = validate_year_format(
profitandloss
)

failures.append({
"rule": "DQ-07",
"dataset": "profitandloss",
"failure_count": len(year_failures)
})

# DQ-09 Net Cash Check

cash_failures = validate_net_cash_check(
cashflow
)

failures.append({
"rule": "DQ-09",
"dataset": "cashflow",
"failure_count": len(cash_failures)
})

# DQ-11 Tax Rate

tax_failures = validate_tax_rate(
profitandloss
)

failures.append({
"rule": "DQ-11",
"dataset": "profitandloss",
"failure_count": len(tax_failures)
})

# DQ-12 Dividend Payout

dividend_failures = validate_dividend_payout(
profitandloss
)

failures.append({
"rule": "DQ-12",
"dataset": "profitandloss",
"failure_count": len(dividend_failures)
})

# DQ-13 URL Validity

url_failures = validate_url_format(
documents
)

failures.append({
"rule": "DQ-13",
"dataset": "documents",
"failure_count": len(url_failures)
})

# DQ-14 EPS Consistency

eps_failures = validate_eps_consistency(
profitandloss
)

failures.append({
"rule": "DQ-14",
"dataset": "profitandloss",
"failure_count": len(eps_failures)
})

# DQ-16 Coverage

coverage_failures = validate_coverage(
profitandloss
)

failures.append({
"rule": "DQ-16",
"dataset": "profitandloss",
"failure_count": len(coverage_failures)
})

report = pd.DataFrame(failures)

Path("output").mkdir(exist_ok=True)

report.to_csv(
"output/validation_failures.csv",
index=False
)

print(report)
