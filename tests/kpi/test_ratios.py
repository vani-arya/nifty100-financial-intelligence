import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.ratios import (
    calculate_npm,
    calculate_opm,
    validate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa
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