from __future__ import annotations
from typing import Any, Dict

from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/tradingview")
async def tradingview_webhook(request: Request):
    payload: Dict[str, Any] = await request.json()
    # TODO: Map payload to strategy signals and enqueue execution
    return {"ok": True, "received": payload.get("ticker") or payload.get("symbol")}