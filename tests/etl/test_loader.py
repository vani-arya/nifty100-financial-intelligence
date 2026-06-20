import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.loader import load_dataset


def test_load_companies():
    df = load_dataset("companies.xlsx")

    assert len(df) > 0
    assert "company_name" in df.columns


def test_load_profitandloss():
    df = load_dataset("profitandloss.xlsx")

    assert len(df) > 0
    assert "sales" in df.columns


def test_load_balancesheet():
    df = load_dataset("balancesheet.xlsx")

    assert len(df) > 0
    assert "total_assets" in df.columns