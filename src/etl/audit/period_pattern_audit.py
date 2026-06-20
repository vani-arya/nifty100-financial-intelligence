import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.loader import load_dataset

datasets = [
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "financial_ratios.xlsx"
]

for dataset in datasets:
    df = load_dataset(dataset)

    print("\n" + "=" * 60)
    print(dataset)

    unique_values = sorted(
        df["year"]
        .dropna()
        .astype(str)
        .unique()
    )

    print("Total unique values:", len(unique_values))
    print(unique_values)