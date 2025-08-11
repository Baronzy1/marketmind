from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import strategies, webhooks, live, leaderboard

app = FastAPI(title="AlgoEdge Pro API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(strategies.router, prefix="/strategies", tags=["strategies"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
app.include_router(live.router, prefix="/live", tags=["live"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])


@app.get("/")
async def root():
    return {"status": "ok", "service": "algoedge-pro-api"}