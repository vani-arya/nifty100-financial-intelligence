from src.analytics.cashflow_kpis import (
    calculate_cfo_pat_ratio,
    classify_cfo_quality,
    calculate_fcf,
    calculate_capex_intensity,
    classify_capex_intensity,
    calculate_fcf_conversion_rate,
    classify_capital_allocation
)


def test_fcf_positive():

    assert calculate_fcf(
        1000,
        -400
    ) == 600


def test_fcf_negative():

    assert calculate_fcf(
        500,
        -1000
    ) == -500


def test_high_quality():

    ratio = calculate_cfo_pat_ratio(
        150,
        100
    )

    assert classify_cfo_quality(
        ratio
    ) == "High Quality"


def test_moderate_quality():

    ratio = calculate_cfo_pat_ratio(
        75,
        100
    )

    assert classify_cfo_quality(
        ratio
    ) == "Moderate"


def test_accrual_risk():

    ratio = calculate_cfo_pat_ratio(
        25,
        100
    )

    assert classify_cfo_quality(
        ratio
    ) == "Accrual Risk"


def test_pat_zero():

    assert calculate_cfo_pat_ratio(
        100,
        0
    ) is None


def test_asset_light():

    value = calculate_capex_intensity(
        -20,
        1000
    )

    assert classify_capex_intensity(
        value
    ) == "Asset Light"


def test_moderate():

    value = calculate_capex_intensity(
        -50,
        1000
    )

    assert classify_capex_intensity(
        value
    ) == "Moderate"


def test_capital_intensive():

    value = calculate_capex_intensity(
        -120,
        1000
    )

    assert classify_capex_intensity(
        value
    ) == "Capital Intensive"


def test_fcf_conversion():

    assert calculate_fcf_conversion_rate(
        600,
        1000
    ) == 60


def test_operating_profit_zero():

    assert calculate_fcf_conversion_rate(
        100,
        0
    ) is None


def test_reinvestor():

    assert classify_capital_allocation(
        100,
        -50,
        -20,
        0.8
    ) == "Reinvestor"


def test_shareholder_returns():

    assert classify_capital_allocation(
        100,
        -50,
        -20,
        1.5
    ) == "Shareholder Returns"


def test_liquidating_assets():

    assert classify_capital_allocation(
        100,
        50,
        -20
    ) == "Liquidating Assets"


def test_distress_signal():

    assert classify_capital_allocation(
        -100,
        50,
        20
    ) == "Distress Signal"


def test_growth_funded_by_debt():

    assert classify_capital_allocation(
        -100,
        -50,
        20
    ) == "Growth Funded by Debt"


def test_cash_accumulator():

    assert classify_capital_allocation(
        100,
        50,
        20
    ) == "Cash Accumulator"


def test_pre_revenue():

    assert classify_capital_allocation(
        -100,
        -50,
        -20
    ) == "Pre-Revenue"


def test_mixed():

    assert classify_capital_allocation(
        100,
        -50,
        20
    ) == "Mixed"