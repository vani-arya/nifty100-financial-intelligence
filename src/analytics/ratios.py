import logging

logger = logging.getLogger(__name__)


def calculate_npm(
    net_profit: float,
    sales: float
) -> float | None:
    """
    Calculate Net Profit Margin (%).
    """

    if sales <= 0:
        return None

    return round((net_profit / sales) * 100, 2)


def calculate_opm(
    operating_profit: float,
    sales: float
) -> float | None:
    """
    Calculate Operating Profit Margin (%).
    """

    if sales <= 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def validate_opm(
    computed_opm: float | None,
    source_opm: float | None,
    company_id: str = "",
    year: str = ""
) -> bool:
    """
    Compare calculated OPM with source OPM.
    Log warning if difference exceeds 1%.
    """

    if computed_opm is None or source_opm is None:
        return False

    difference = abs(computed_opm - source_opm)

    if difference > 1:

        logger.warning(
            f"OPM mismatch | "
            f"Company={company_id} "
            f"Year={year} "
            f"Computed={computed_opm:.2f} "
            f"Source={source_opm:.2f}"
        )

        return False

    return True


def calculate_roe(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> float | None:
    """
    Calculate Return on Equity (%).
    """

    equity_base = equity_capital + reserves

    if equity_base <= 0:
        return None

    return round((net_profit / equity_base) * 100, 2)


def calculate_roce(
    operating_profit: float,
    depreciation: float,
    equity_capital: float,
    reserves: float,
    borrowings: float
) -> float | None:
    """
    Calculate Return on Capital Employed (%).

    EBIT = Operating Profit - Depreciation
    Capital Employed = Equity + Reserves + Borrowings
    """

    ebit = operating_profit - depreciation

    capital_employed = (
        equity_capital
        + reserves
        + borrowings
    )

    if capital_employed <= 0:
        return None

    return round(
        (ebit / capital_employed) * 100,
        2
    )


def calculate_roa(
    net_profit: float,
    total_assets: float
) -> float | None:
    """
    Calculate Return on Assets (%).
    """

    if total_assets <= 0:
        return None

    return round(
        (net_profit / total_assets) * 100,
        2
    )