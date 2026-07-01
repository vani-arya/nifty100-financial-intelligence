import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.ratios import (
    calculate_npm,
    calculate_opm,
    validate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa,
    calculate_debt_to_equity,
    get_high_leverage_flag,
    calculate_interest_coverage,
    get_icr_label,
    get_icr_warning_flag,
    calculate_net_debt,
    calculate_asset_turnover
)


def test_npm_normal():

    assert calculate_npm(
        net_profit=100,
        sales=1000
    ) == 10.0


def test_npm_zero_sales():

    assert calculate_npm(
        net_profit=100,
        sales=0
    ) is None


def test_opm_normal():

    assert calculate_opm(
        operating_profit=200,
        sales=1000
    ) == 20.0


def test_opm_validation_pass():

    assert validate_opm(
        computed_opm=20,
        source_opm=20.5
    ) is True


def test_opm_validation_fail():

    assert validate_opm(
        computed_opm=20,
        source_opm=17
    ) is False


def test_roe_normal():

    assert calculate_roe(
        net_profit=100,
        equity_capital=300,
        reserves=200
    ) == 20.0


def test_roe_negative_equity():

    assert calculate_roe(
        net_profit=100,
        equity_capital=-300,
        reserves=100
    ) is None


def test_roce_normal():

    assert calculate_roce(
        operating_profit=150,
        depreciation=30,
        equity_capital=300,
        reserves=200,
        borrowings=100
    ) == 20.0


def test_roa_zero_assets():

    assert calculate_roa(
        net_profit=100,
        total_assets=0
    ) is None



def test_debt_to_equity_normal():

    assert calculate_debt_to_equity(
        borrowings=500,
        equity_capital=300,
        reserves=200
    ) == 1.0


def test_debt_free_returns_zero():

    assert calculate_debt_to_equity(
        borrowings=0,
        equity_capital=500,
        reserves=200
    ) == 0


def test_negative_equity_returns_none():

    assert calculate_debt_to_equity(
        borrowings=100,
        equity_capital=-300,
        reserves=100
    ) is None


def test_high_leverage_flag():

    assert get_high_leverage_flag(
        debt_to_equity=6,
        broad_sector="Industrials"
    ) is True


def test_financials_excluded_from_leverage_flag():

    assert get_high_leverage_flag(
        debt_to_equity=10,
        broad_sector="Financials"
    ) is False


def test_icr_interest_zero():

    assert calculate_interest_coverage(
        operating_profit=100,
        other_income=50,
        interest=0
    ) is None


def test_icr_label_debt_free():

    assert get_icr_label(None) == "Debt Free"


def test_asset_turnover_zero_assets():

    assert calculate_asset_turnover(
        sales=1000,
        total_assets=0
    ) is None