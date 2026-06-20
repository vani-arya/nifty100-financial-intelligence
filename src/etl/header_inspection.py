from pathlib import Path
import pandas as pd

FILES_TO_CHECK = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
]

for file_name in FILES_TO_CHECK:
    file_path = Path("data/raw") / file_name

    print("\n" + "=" * 80)
    print(file_name)

    df = pd.read_excel(file_path, header=None)

    print(df.head(10))