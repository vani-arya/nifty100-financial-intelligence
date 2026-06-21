import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from src.etl.loader import load_dataset
from src.etl.validator import validate_foreign_key

companies = load_dataset("companies.xlsx")
profitandloss = load_dataset("profitandloss.xlsx")

invalid = validate_foreign_key(
    profitandloss,
    "company_id",
    companies,
    "id"
)

print("Invalid company IDs:")
print(invalid)
print("Count:", len(invalid))