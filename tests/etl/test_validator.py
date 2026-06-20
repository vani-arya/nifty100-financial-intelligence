import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.loader import load_dataset
from src.etl.validator import (
    validate_not_empty,
    validate_required_columns,
    validate_primary_key_not_null,
    validate_primary_key_unique,
    validate_foreign_key
)


def test_companies_not_empty():
    df = load_dataset("companies.xlsx")

    assert validate_not_empty(df)


def test_companies_required_columns():
    df = load_dataset("companies.xlsx")

    required = [
        "id",
        "company_name",
        "website"
    ]

    assert validate_required_columns(df, required) == []


def test_company_id_not_null():
    df = load_dataset("companies.xlsx")

    assert validate_primary_key_not_null(df, "id")


def test_company_id_unique():
    df = load_dataset("companies.xlsx")

    assert validate_primary_key_unique(df, "id")


def test_profitandloss_company_fk():
    companies = load_dataset("companies.xlsx")

    profitandloss = load_dataset(
        "profitandloss.xlsx"
    )

    invalid = validate_foreign_key(
        profitandloss,
        "company_id",
        companies,
        "id"
    )

    assert isinstance(invalid, set)


def test_balancesheet_company_fk():
    companies = load_dataset("companies.xlsx")

    balancesheet = load_dataset(
        "balancesheet.xlsx"
    )

    invalid = validate_foreign_key(
        balancesheet,
        "company_id",
        companies,
        "id"
    )

    assert isinstance(invalid, set)


def test_cashflow_company_fk():
    companies = load_dataset("companies.xlsx")

    cashflow = load_dataset(
        "cashflow.xlsx"
    )

    invalid = validate_foreign_key(
        cashflow,
        "company_id",
        companies,
        "id"
    )

    assert isinstance(invalid, set)


def test_financial_ratios_company_fk():
    companies = load_dataset("companies.xlsx")

    financial_ratios = load_dataset(
        "financial_ratios.xlsx"
    )

    invalid = validate_foreign_key(
        financial_ratios,
        "company_id",
        companies,
        "id"
    )

    assert isinstance(invalid, set)


def test_market_cap_company_fk():
    companies = load_dataset("companies.xlsx")

    market_cap = load_dataset(
        "market_cap.xlsx"
    )

    invalid = validate_foreign_key(
        market_cap,
        "company_id",
        companies,
        "id"
    )

    assert len(invalid) == 0


def test_sectors_company_fk():
    companies = load_dataset("companies.xlsx")

    sectors = load_dataset(
        "sectors.xlsx"
    )

    invalid = validate_foreign_key(
        sectors,
        "company_id",
        companies,
        "id"
    )

    assert len(invalid) == 0