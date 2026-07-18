import logging

logger = logging.getLogger(__name__)


def calculate_fcf(
    operating_activity: float,
    investing_activity: float
) -> float:
    """
    Calculate Free Cash Flow.
    """

    return round(
        operating_activity + investing_activity,
        2
    )


def calculate_cfo_pat_ratio(
    operating_activity: float,
    net_profit: float
) -> float | None:
    """
    Calculate CFO/PAT ratio.
    """

    if net_profit == 0:
        return None

    return round(
        operating_activity / net_profit,
        2
    )


def classify_cfo_quality(
    ratio: float | None
) -> str | None:
    """
    Classify earnings quality.
    """

    if ratio is None:
        return None

    if ratio > 1:
        return "High Quality"

    if ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def calculate_capex_intensity(
    investing_activity: float,
    sales: float
) -> float | None:
    """
    Calculate CapEx intensity.
    """

    if sales <= 0:
        return None

    return round(
        abs(investing_activity) / sales * 100,
        2
    )


def classify_capex_intensity(
    intensity: float | None
) -> str | None:
    """
    Classify CapEx intensity.
    """

    if intensity is None:
        return None

    if intensity < 3:
        return "Asset Light"

    if intensity <= 8:
        return "Moderate"

    return "Capital Intensive"


def calculate_fcf_conversion_rate(
    free_cash_flow: float,
    cash_from_operations: float
) -> float | None:
    """
    Calculate FCF conversion rate.
    """

    if cash_from_operations == 0:
        return None

    return round(
        free_cash_flow /
        cash_from_operations *
        100,
        2
    )


def classify_capital_allocation(
    cfo: float,
    cfi: float,
    cff: float,
    cfo_pat_ratio: float | None = None
) -> str:
    """
    Classify capital allocation pattern
    based on CFO, CFI and CFF signs.
    """

    cfo_positive = cfo > 0
    cfi_positive = cfi > 0
    cff_positive = cff > 0

    # (+,-,-)
    if (
        cfo_positive
        and not cfi_positive
        and not cff_positive
    ):

        if (
            cfo_pat_ratio is not None
            and cfo_pat_ratio > 1
        ):
            return "Shareholder Returns"

        return "Reinvestor"

    # (+,+,-)
    if (
        cfo_positive
        and cfi_positive
        and not cff_positive
    ):
        return "Liquidating Assets"

    # (-,+,+)
    if (
        not cfo_positive
        and cfi_positive
        and cff_positive
    ):
        return "Distress Signal"

    # (-,-,+)
    if (
        not cfo_positive
        and not cfi_positive
        and cff_positive
    ):
        return "Growth Funded by Debt"

    # (+,+,+)
    if (
        cfo_positive
        and cfi_positive
        and cff_positive
    ):
        return "Cash Accumulator"

    # (-,-,-)
    if (
        not cfo_positive
        and not cfi_positive
        and not cff_positive
    ):
        return "Pre-Revenue"

    # (+,-,+)
    if (
        cfo_positive
        and not cfi_positive
        and cff_positive
    ):
        return "Mixed"

    return "Unknown"