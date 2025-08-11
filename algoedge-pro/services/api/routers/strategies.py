from __future__ import annotations
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from python.algoedge.backtester import run_backtest
from python.algoedge.optimizer import optimize_strategy
from python.algoedge.strategy_dsl import normalize_strategy

from ..core.database import SessionLocal
from ..models.strategy import Strategy
from ..models.runs import BacktestRun
from ..schemas.strategy import StrategyIn, StrategyOut
from .auth import get_current_user

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/validate")
async def validate_strategy(payload: StrategyPayload):
    try:
        normalized = normalize_strategy(payload.strategy)
        return {"ok": True, "strategy": normalized}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/backtest")
async def backtest_strategy(payload: StrategyPayload, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        result = run_backtest(
            payload.strategy,
            symbol=payload.symbol,
            market=payload.market,
            timeframe=payload.timeframe,
            years=payload.years,
        )
        # Persist a run linked to a temporary strategy record for user
        strat = Strategy(user_id=user.id, name=payload.strategy.get("name", "Untitled"), dsl=payload.strategy, is_public=False)
        db.add(strat)
        db.flush()
        run = BacktestRun(strategy_id=strat.id, symbol=payload.symbol, market=payload.market, timeframe=payload.timeframe, years=payload.years, metrics=result.metrics)
        db.add(run)
        db.commit()
        return {
            "metrics": result.metrics,
            "num_trades": len(result.trades),
            "run_id": run.id,
            "strategy_id": strat.id,
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


@router.post("")
async def create_strategy(body: StrategyIn, db: Session = Depends(get_db), user=Depends(get_current_user)) -> StrategyOut:
    strat = Strategy(user_id=user.id, name=body.name, dsl=body.dsl, is_public=body.is_public)
    db.add(strat)
    db.commit()
    db.refresh(strat)
    return StrategyOut.model_validate(strat)


@router.get("")
async def list_strategies(db: Session = Depends(get_db), user=Depends(get_current_user)) -> List[StrategyOut]:
    items = db.query(Strategy).filter(Strategy.user_id == user.id).all()
    return [StrategyOut.model_validate(i) for i in items]