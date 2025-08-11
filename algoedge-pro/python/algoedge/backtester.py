from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

from . import indicators as I
from . import metrics as M
from . import data as Data
from .strategy_dsl import normalize_strategy


@dataclass
class BacktestResult:
    equity_curve: pd.Series
    trades: pd.DataFrame
    metrics: Dict[str, float]


def _resolve_indicator(df: pd.DataFrame, node: Dict[str, Any]) -> pd.Series | pd.DataFrame:
    name = node.get("indicator", "").upper()
    params = node.get("params", {})
    if name == "EMA":
        return I.ema(df, **{k: v for k, v in params.items() if k in {"length", "source"}})
    if name == "SMA":
        return I.sma(df, **{k: v for k, v in params.items() if k in {"length", "source"}})
    if name == "RSI":
        return I.rsi(df, **{k: v for k, v in params.items() if k in {"length", "source"}})
    if name == "MACD":
        return I.macd(df, **{k: v for k, v in params.items() if k in {"fast", "slow", "signal", "source"}})
    if name in {"BBANDS", "BOLLINGER", "BOLLINGER BANDS"}:
        return I.bollinger_bands(df, **{k: v for k, v in params.items() if k in {"length", "std", "source"}})
    if name == "VWAP":
        return I.vwap(df)
    # Unknown -> passthrough
    return pd.Series(index=df.index, dtype=float)


def _evaluate_logic_row(row: pd.Series, logic: List[Dict[str, Any]], values: Dict[str, Any]) -> bool:
    for cond in logic:
        op = cond.get("op")
        a = cond.get("a")
        b = cond.get("b")
        a_val = values.get(a, row.get(a, a)) if isinstance(a, str) else a
        b_val = values.get(b, row.get(b, b)) if isinstance(b, str) else b
        if op == "gt" and not (a_val > b_val):
            return False
        if op == "lt" and not (a_val < b_val):
            return False
        if op == "cross_over" and not (a_val > b_val and row.get(f"{a}_prev", a_val) <= row.get(f"{b}_prev", b_val)):
            return False
        if op == "cross_under" and not (a_val < b_val and row.get(f"{a}_prev", a_val) >= row.get(f"{b}_prev", b_val)):
            return False
    return True


def run_backtest(
    strategy: Dict[str, Any],
    symbol: str = "BTC/USDT",
    market: str = "crypto",
    timeframe: str = "1h",
    years: int = 2,
    initial_cash: float = 10_000.0,
) -> BacktestResult:
    strategy = normalize_strategy(strategy)
    df = Data.load_ohlcv(symbol=symbol, market=market, timeframe=timeframe, years=years)

    values: Dict[str, Any] = {
        "open": df.get("open"),
        "high": df.get("high"),
        "low": df.get("low"),
        "close": df.get("close"),
        "volume": df.get("volume"),
    }

    # Compute indicators
    for node in strategy.get("blocks", []):
        if node.get("type") == "indicator":
            out = _resolve_indicator(df, node)
            key = node.get("id") or node.get("indicator")
            if isinstance(out, pd.Series):
                values[key] = out
            elif isinstance(out, pd.DataFrame):
                for col in out.columns:
                    values[f"{key}_{col}"] = out[col]

    # Prepare signals
    entry_node = next((b for b in strategy.get("blocks", []) if b.get("type") == "entry"), None)
    exit_node = next((b for b in strategy.get("blocks", []) if b.get("type") == "exit"), None)
    risk_node = next((b for b in strategy.get("blocks", []) if b.get("type") == "risk"), {"params": {}})
    risk = risk_node.get("params", {})
    sl_pct = float(risk.get("stop_loss_pct", 0.02))
    tp_pct = float(risk.get("take_profit_pct", 0.04))
    risk_per_trade_pct = float(risk.get("risk_per_trade_pct", 1.0))

    df_calc = pd.DataFrame(index=df.index)
    for k, v in values.items():
        if isinstance(v, (pd.Series, pd.DataFrame)):
            df_calc[k] = v if isinstance(v, pd.Series) else v.iloc[:, 0]

    # Add prev values for cross detection
    for key in list(df_calc.columns):
        df_calc[f"{key}_prev"] = df_calc[key].shift(1)

    entries: List[Tuple[pd.Timestamp, float]] = []
    exits: List[Tuple[pd.Timestamp, float]] = []

    position_open = False
    entry_price = 0.0

    for ts, row in df_calc.iterrows():
        price = row.get("close")
        if price is None or np.isnan(price):
            continue

        if not position_open and entry_node:
            if _evaluate_logic_row(row, entry_node.get("logic", []), row.to_dict()):
                entries.append((ts, float(price)))
                position_open = True
                entry_price = float(price)
                continue

        if position_open:
            # Stop loss / Take profit
            if price <= entry_price * (1 - sl_pct) or price >= entry_price * (1 + tp_pct):
                exits.append((ts, float(price)))
                position_open = False
                entry_price = 0.0
                continue

            if exit_node and _evaluate_logic_row(row, exit_node.get("logic", []), row.to_dict()):
                exits.append((ts, float(price)))
                position_open = False
                entry_price = 0.0
                continue

    # Close any open position at last price
    if position_open:
        last_ts = df_calc.index[-1]
        last_price = float(df_calc.loc[last_ts, "close"])
        exits.append((last_ts, last_price))

    # Build trades
    trades_records: List[Dict[str, Any]] = []
    cash = initial_cash
    equity_curve = []
    eq_index = []

    for i in range(min(len(entries), len(exits))):
        e_ts, e_price = entries[i]
        x_ts, x_price = exits[i]
        risk_cash = cash * (risk_per_trade_pct / 100.0)
        qty = risk_cash / e_price if e_price > 0 else 0
        pnl = (x_price - e_price) * qty
        cash += pnl
        trades_records.append({
            "entry_time": e_ts,
            "entry_price": e_price,
            "exit_time": x_ts,
            "exit_price": x_price,
            "qty": qty,
            "pnl": pnl,
            "return_pct": (x_price - e_price) / e_price if e_price else 0.0,
        })
        eq_index.append(x_ts)
        equity_curve.append(cash)

    if not eq_index:
        eq_index = [df.index[0]]
        equity_curve = [initial_cash]

    equity_series = pd.Series(equity_curve, index=pd.Index(eq_index))
    trades_df = pd.DataFrame(trades_records)

    metrics = {
        "win_rate": M.win_rate(trades_df),
        "profit_factor": M.profit_factor(trades_df),
        "max_drawdown": M.max_drawdown(equity_series),
        "sharpe_ratio": M.sharpe_ratio(equity_series),
        "num_trades": float(len(trades_df)),
        "final_equity": float(equity_series.iloc[-1] if len(equity_series) else initial_cash),
        "roi_pct": float(((equity_series.iloc[-1] / initial_cash) - 1) * 100 if len(equity_series) else 0.0),
    }

    return BacktestResult(equity_curve=equity_series, trades=trades_df, metrics=metrics)