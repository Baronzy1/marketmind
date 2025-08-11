from __future__ import annotations
from typing import Any, Dict, List

"""
Strategy DSL (v0.1)

Example:
{
  "version": "0.1",
  "name": "EMA Cross + RSI Filter",
  "blocks": [
    {"id": "ema_fast", "type": "indicator", "indicator": "EMA", "params": {"length": 20, "source": "close"}},
    {"id": "ema_slow", "type": "indicator", "indicator": "EMA", "params": {"length": 50, "source": "close"}},
    {"id": "rsi", "type": "indicator", "indicator": "RSI", "params": {"length": 14}},
    {"id": "entry", "type": "entry", "logic": [{"op": "cross_over", "a": "ema_fast", "b": "ema_slow"}, {"op": "lt", "a": "rsi", "b": 70}]},
    {"id": "exit", "type": "exit", "logic": [{"op": "cross_under", "a": "ema_fast", "b": "ema_slow"}]},
    {"id": "risk", "type": "risk", "params": {"stop_loss_pct": 0.02, "take_profit_pct": 0.04, "risk_per_trade_pct": 1.0}}
  ]
}
"""


def normalize_strategy(strategy: Dict[str, Any]) -> Dict[str, Any]:
    strategy = dict(strategy)
    strategy.setdefault("version", "0.1")
    strategy.setdefault("name", "Unnamed Strategy")
    blocks = strategy.get("blocks", [])

    # Auto-complete: add default risk if missing
    if not any(b.get("type") == "risk" for b in blocks):
        blocks.append({
            "id": "risk_default",
            "type": "risk",
            "params": {"stop_loss_pct": 0.02, "take_profit_pct": 0.04, "risk_per_trade_pct": 1.0}
        })

    # Auto-complete: add trend filter if only one condition
    has_entry = next((b for b in blocks if b.get("type") == "entry"), None)
    if has_entry and len(has_entry.get("logic", [])) < 1:
        has_entry.setdefault("logic", [])
        has_entry["logic"].append({"op": "gt", "a": "EMA(length=50)", "b": "EMA(length=200)"})

    strategy["blocks"] = blocks
    return strategy


def extract_indicators(strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [b for b in strategy.get("blocks", []) if b.get("type") == "indicator"]


def get_block_by_id(strategy: Dict[str, Any], block_id: str) -> Dict[str, Any] | None:
    for b in strategy.get("blocks", []):
        if b.get("id") == block_id:
            return b
    return None