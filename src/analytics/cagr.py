TURNAROUND = "TURNAROUND"
DECLINE_TO_LOSS = "DECLINE_TO_LOSS"
BOTH_NEGATIVE = "BOTH_NEGATIVE"
ZERO_BASE = "ZERO_BASE"
INSUFFICIENT = "INSUFFICIENT"


def calculate_cagr(
    start_value: float,
    end_value: float,
    years: int
) -> tuple[float | None, str | None]:
    """
    Calculate CAGR with edge-case handling.
    """

    if years <= 0:
        return None, INSUFFICIENT

    if start_value == 0:
        return None, ZERO_BASE

    if start_value > 0 and end_value < 0:
        return None, DECLINE_TO_LOSS

    if start_value < 0 and end_value > 0:
        return None, TURNAROUND

    if start_value < 0 and end_value < 0:
        return None, BOTH_NEGATIVE

    cagr = (
        (end_value / start_value) ** (1 / years) - 1
    ) * 100

    return round(cagr, 2), None


def calculate_period_cagr(
    values: list[float],
    years: int
) -> tuple[float | None, str | None]:
    """
    Calculate CAGR from historical series.
    """

    if len(values) < years + 1:
        return None, INSUFFICIENT

    start_value = values[0]
    end_value = values[-1]

    return calculate_cagr(
        start_value,
        end_value,
        years
    )


def calculate_revenue_cagr(
    values: list[float],
    years: int
) -> tuple[float | None, str | None]:
    """
    Revenue CAGR.
    """
    return calculate_period_cagr(
        values,
        years
    )


def calculate_pat_cagr(
    values: list[float],
    years: int
) -> tuple[float | None, str | None]:
    """
    PAT CAGR.
    """
    return calculate_period_cagr(
        values,
        years
    )


def calculate_eps_cagr(
    values: list[float],
    years: int
) -> tuple[float | None, str | None]:
    """
    EPS CAGR.
    """
    return calculate_period_cagr(
        values,
        years
    )