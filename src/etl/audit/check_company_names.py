import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from src.etl.loader import load_dataset

companies = load_dataset("companies.xlsx")

print(companies["id"].tolist())