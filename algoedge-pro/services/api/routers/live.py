from __future__ import annotations
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from python.algoedge.connectors.binance import BinanceConnector
from python.algoedge.connectors.alpaca import AlpacaConnector
from python.algoedge.connectors.ib import IBConnector

router = APIRouter()


@router.post("/start")
async def start_live(payload: Dict[str, Any]):
    return {"ok": True, "session_id": "demo-session"}


@router.post("/stop")
async def stop_live(payload: Dict[str, Any]):
    return {"ok": True}


@router.post("/order")
async def place_order(broker: str, symbol: str, side: str, qty: float):
    try:
        if broker == "binance":
            import os
            conn = BinanceConnector(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_API_SECRET"))
            order = conn.create_order(symbol=symbol, side=side, type_="market", amount=qty)
            return {"ok": True, "order": order}
        if broker == "alpaca":
            import os
            conn = AlpacaConnector(api_key=os.getenv("ALPACA_API_KEY", ""), api_secret=os.getenv("ALPACA_API_SECRET", ""))
            order = conn.submit_order(symbol=symbol, qty=qty, side=side)
            return {"ok": True, "order": str(order.id) if hasattr(order, 'id') else True}
        if broker == "ib":
            conn = IBConnector()
            status = conn.place_market_order(symbol=symbol, qty=qty, side=side.upper())
            return {"ok": True, "status": status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=400, detail="Unknown broker")