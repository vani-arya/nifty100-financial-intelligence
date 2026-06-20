from pathlib import Path
import pandas as pd

RAW_PATH = Path("data/raw")

for file in RAW_PATH.glob("*.xlsx"):
    print("\n" + "=" * 60)
    print(f"FILE: {file.name}")

    excel = pd.ExcelFile(file)

    print("Sheets:", excel.sheet_names)

    for sheet in excel.sheet_names:
        df = pd.read_excel(file, sheet_name=sheet)

        print(f"\nSheet: {sheet}")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        print("Columns:")
        print(df.columns.tolist())