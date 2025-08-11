from __future__ import annotations
from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter()


@router.post("/start")
async def start_live(payload: Dict[str, Any]):
    # TODO: spin up live execution session with selected broker and risk settings
    return {"ok": True, "session_id": "demo-session"}


@router.post("/stop")
async def stop_live(payload: Dict[str, Any]):
    # TODO: stop live execution session
    return {"ok": True}