from __future__ import annotations
from typing import Any, Dict

from .celery_app import celery_app
from python.algoedge.backtester import run_backtest
from python.algoedge.optimizer import optimize_strategy


@celery_app.task(name="backtest.run")
def task_backtest(payload: Dict[str, Any]) -> Dict[str, Any]:
    result = run_backtest(
        payload.get("strategy", {}),
        symbol=payload.get("symbol", "BTC/USDT"),
        market=payload.get("market", "crypto"),
        timeframe=payload.get("timeframe", "1h"),
        years=int(payload.get("years", 2)),
    )
    return {"metrics": result.metrics, "num_trades": len(result.trades)}


@celery_app.task(name="optimize.run")
def task_optimize(payload: Dict[str, Any]) -> Dict[str, Any]:
    best_strategy, best_metrics = optimize_strategy(
        payload.get("strategy", {}),
        param_space=payload.get("param_space", {}),
        objective=payload.get("objective", "roi_pct"),
        symbol=payload.get("symbol", "BTC/USDT"),
        market=payload.get("market", "crypto"),
        timeframe=payload.get("timeframe", "1h"),
        years=int(payload.get("years", 2)),
        samples=int(payload.get("samples", 20)),
    )
    return {"best_strategy": best_strategy, "metrics": best_metrics}