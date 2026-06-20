import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.loader import load_dataset

datasets = [
    "profitandloss.xlsx",
    "balancesheet.xlsx"
]

for dataset in datasets:
    df = load_dataset(dataset)

    print("\n" + "=" * 60)
    print(dataset)

    anomalies = df[
        (
            df["year"].astype(str).str.contains("9m", na=False)
        )
        |
        (
            df["year"].astype(str).str.contains(
                "\\.5",
                regex=True,
                na=False
            )
        )
        |
        (
            df["year"].astype(str) == "Mar 2023 15"
        )
    ]

    print(anomalies[["company_id", "year"]])