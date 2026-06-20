from pathlib import Path
import pandas as pd

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx"
]

for file in files:
    print("\n" + "="*80)
    print(file)

    df = pd.read_excel(
        Path("data/raw") / file,
        header=1
    )

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 3 rows:")
    print(df.head(3))