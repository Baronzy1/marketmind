from __future__ import annotations
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from python.algoedge.backtester import run_backtest
from python.algoedge.optimizer import optimize_strategy
from python.algoedge.strategy_dsl import normalize_strategy

router = APIRouter()


class StrategyPayload(BaseModel):
    strategy: Dict[str, Any]
    symbol: str = "BTC/USDT"
    market: str = "crypto"  # crypto | stocks | forex
    timeframe: str = "1h"
    years: int = 2


class OptimizePayload(BaseModel):
    strategy: Dict[str, Any]
    param_space: Dict[str, Any]
    objective: str = "roi_pct"
    symbol: str = "BTC/USDT"
    market: str = "crypto"
    timeframe: str = "1h"
    years: int = 2
    samples: int = 20


@router.post("/validate")
async def validate_strategy(payload: StrategyPayload):
    try:
        normalized = normalize_strategy(payload.strategy)
        return {"ok": True, "strategy": normalized}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/backtest")
async def backtest_strategy(payload: StrategyPayload):
    try:
        result = run_backtest(
            payload.strategy,
            symbol=payload.symbol,
            market=payload.market,
            timeframe=payload.timeframe,
            years=payload.years,
        )
        return {
            "metrics": result.metrics,
            "num_trades": len(result.trades),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/optimize")
async def optimize(payload: OptimizePayload):
    try:
        best_strategy, best_metrics = optimize_strategy(
            payload.strategy,
            param_space=payload.param_space,
            objective=payload.objective,
            symbol=payload.symbol,
            market=payload.market,
            timeframe=payload.timeframe,
            years=payload.years,
            samples=payload.samples,
        )
        return {"best_strategy": best_strategy, "metrics": best_metrics}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))