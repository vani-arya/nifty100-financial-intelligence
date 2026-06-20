import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.loader import load_dataset
from src.etl.validator import validate_foreign_key

companies = load_dataset("companies.xlsx")

datasets = [
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "financial_ratios.xlsx"
]

for dataset in datasets:
    df = load_dataset(dataset)

    invalid = validate_foreign_key(
        df,
        "company_id",
        companies,
        "id"
    )

    print("\n" + "=" * 50)
    print(dataset)
    print(sorted(invalid))