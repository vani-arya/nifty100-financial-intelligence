from fastapi import (
    APIRouter,
    HTTPException
)

from fastapi.responses import FileResponse
from pathlib import Path

from src.api.services.company_service import (
    get_companies,
    get_company_profile,
    get_profit_loss_history,
    get_balance_sheet_history,
    get_cashflow_history,
    get_ratios_history
)

router = APIRouter()


@router.get(
    "/companies"
)
def companies(
    sector: str = None,
    market_cap_category: str = None,
    search: str = None
):

    return get_companies(
        sector,
        market_cap_category,
        search
    )


@router.get(
    "/companies/{ticker}"
)
def company_profile(
    ticker: str
):

    data = get_company_profile(
        ticker
    )

    if data is None:

        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return data


@router.get(
    "/companies/{ticker}/pl"
)
def company_profit_loss(
    ticker: str,
    from_year: int = None,
    to_year: int = None
):

    data = get_profit_loss_history(
        ticker,
        from_year,
        to_year
    )

    if len(data) == 0:

        raise HTTPException(
            status_code=404,
            detail="No P&L data found"
        )

    return data


@router.get(
    "/companies/{ticker}/bs"
)
def company_balance_sheet(
    ticker: str,
    from_year: int = None,
    to_year: int = None
):

    data = get_balance_sheet_history(
        ticker,
        from_year,
        to_year
    )

    if len(data) == 0:

        raise HTTPException(
            status_code=404,
            detail="No balance sheet data found"
        )

    return data


@router.get(
    "/companies/{ticker}/cashflow"
)
def company_cashflow(
    ticker: str,
    from_year: int = None,
    to_year: int = None
):

    data = get_cashflow_history(
        ticker,
        from_year,
        to_year
    )

    if len(data) == 0:

        raise HTTPException(
            status_code=404,
            detail="No cashflow data found"
        )

    return data


@router.get(
    "/companies/{ticker}/ratios"
)
def company_ratios(
    ticker: str,
    year: int = None
):

    data = get_ratios_history(
        ticker,
        year
    )

    if len(data) == 0:

        raise HTTPException(
            status_code=404,
            detail="No ratios found"
        )

    return data


@router.get(
    "/companies/{ticker}/tearsheet"
)
def company_tearsheet(
    ticker: str
):

    pdf_path = Path(
        f"reports/tearsheets/{ticker}_tearsheet.pdf"
    )

    if not pdf_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Tearsheet not found"
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=pdf_path.name
    )

