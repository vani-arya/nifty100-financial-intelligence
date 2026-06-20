import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.loader import load_dataset

datasets = [
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "financial_ratios.xlsx",
    "market_cap.xlsx"
]

for dataset in datasets:
    df = load_dataset(dataset)

    print("\n" + "=" * 60)
    print(dataset)

    if "year" in df.columns:
        print(df["year"].dropna().unique()[:20])