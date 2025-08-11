from __future__ import annotations
from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def get_leaderboard():
    # TODO: fetch from DB aggregated performance of public strategies
    return {
        "leaders": [
            {"user": "alice", "roi_pct": 124.5},
            {"user": "bob", "roi_pct": 98.1},
        ]
    }