from __future__ import annotations
import random
from typing import Any, Dict, List, Tuple

from .backtester import run_backtest


def _iter_param_candidates(param_spec: Dict[str, Any], num_samples: int = 20) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    for _ in range(num_samples):
        params = {}
        for key, spec in param_spec.items():
            if isinstance(spec, list):
                params[key] = random.choice(spec)
            elif isinstance(spec, dict) and {"min", "max"}.issubset(spec.keys()):
                if spec.get("type") == "int":
                    params[key] = random.randint(int(spec["min"]), int(spec["max"]))
                else:
                    params[key] = random.uniform(float(spec["min"]), float(spec["max"]))
        candidates.append(params)
    return candidates


def optimize_strategy(
    strategy: Dict[str, Any],
    param_space: Dict[str, Any],
    objective: str = "roi_pct",
    symbol: str = "BTC/USDT",
    market: str = "crypto",
    timeframe: str = "1h",
    years: int = 2,
    samples: int = 25,
) -> Tuple[Dict[str, Any], Dict[str, float]]:
    best_strategy = strategy
    best_metrics = {objective: float("-inf")}

    nodes = strategy.get("blocks", [])
    entry = next((n for n in nodes if n.get("type") == "entry"), None)

    for params in _iter_param_candidates(param_space, num_samples=samples):
        trial = {**strategy}
        trial_nodes = []
        for n in nodes:
            n2 = dict(n)
            if n2.get("type") == "indicator" and n2.get("id") in params:
                n2["params"] = {**n2.get("params", {}), **params[n2["id"]]}
            trial_nodes.append(n2)
        trial["blocks"] = trial_nodes
        result = run_backtest(trial, symbol=symbol, market=market, timeframe=timeframe, years=years)
        if result.metrics.get(objective, float("-inf")) > best_metrics.get(objective, float("-inf")):
            best_strategy = trial
            best_metrics = result.metrics

    return best_strategy, best_metrics