import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.loader import load_dataset

for file in [
    "financial_ratios.xlsx",
    "peer_groups.xlsx"
]:
    df = load_dataset(file)

    print("\n" + "=" * 60)
    print(file)
    print(df.columns.tolist())