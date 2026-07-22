import sqlite3
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.health import router as health_router

from src.api.routers.companies import router as companies_router
from src.api.routers.screener import router as screener_router
from src.api.routers.sectors import router as sectors_router
from src.api.routers.peers import router as peers_router
from src.api.routers.valuation import router as valuation_router
from src.api.routers.portfolio import router as portfolio_router
from src.api.routers.documents import router as documents_router


app = FastAPI(
    title="Nifty100 Financial Intelligence API",
    version="1.0.0"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


@app.middleware("http")
async def log_requests(
    request,
    call_next
):

    start = time.time()

    response = await call_next(
        request
    )

    duration = (
        time.time() - start
    ) * 1000

    print(

        f"{request.method} "

        f"{request.url.path} "

        f"{duration:.2f} ms"
    )

    return response


app.include_router(

    health_router,

    prefix="/api/v1",

    tags=["Health"]
)

app.include_router(
    companies_router,
    prefix="/api/v1",
    tags=["Companies"]
)

app.include_router(
    screener_router,
    prefix="/api/v1",
    tags=["Screener"]
)

app.include_router(
    sectors_router,
    prefix="/api/v1",
    tags=["Sectors"]
)

app.include_router(
    peers_router,
    prefix="/api/v1",
    tags=["Peers"]
)

app.include_router(
    valuation_router,
    prefix="/api/v1",
    tags=["Valuation"]
)

app.include_router(
    portfolio_router,
    prefix="/api/v1",
    tags=["Portfolio"]
)

app.include_router(
    documents_router,
    prefix="/api/v1",
    tags=["Documents"]
)