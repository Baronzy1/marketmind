from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import strategies, webhooks, live, leaderboard, auth, marketplace, payments
from .core.database import engine
from .models import base  # noqa: F401 - ensures Base is imported
from .models.base import Base

app = FastAPI(title="AlgoEdge Pro API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(strategies.router, prefix="/strategies", tags=["strategies"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
app.include_router(live.router, prefix="/live", tags=["live"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(marketplace.router, prefix="/marketplace", tags=["marketplace"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])


@app.get("/")
async def root():
    return {"status": "ok", "service": "algoedge-pro-api"}