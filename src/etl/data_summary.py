import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from src.etl.loader import load_all_sources


datasets = load_all_sources()

for name, df in datasets.items():
    print(
        f"{name}: "
        f"{df.shape[0]} rows, "
        f"{df.shape[1]} columns"
    )