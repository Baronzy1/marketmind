from __future__ import annotations
import numpy as np
import pandas as pd


def compute_returns(equity_curve: pd.Series) -> pd.Series:
    return equity_curve.pct_change().fillna(0.0)


def win_rate(trades: pd.DataFrame) -> float:
    if trades.empty:
        return 0.0
    return float((trades["pnl"] > 0).mean())


def profit_factor(trades: pd.DataFrame) -> float:
    gains = trades.loc[trades["pnl"] > 0, "pnl"].sum()
    losses = -trades.loc[trades["pnl"] < 0, "pnl"].sum()
    if losses == 0:
        return float("inf") if gains > 0 else 0.0
    return float(gains / losses)


def max_drawdown(equity_curve: pd.Series) -> float:
    cumulative_max = equity_curve.cummax()
    drawdown = (equity_curve - cumulative_max) / cumulative_max
    return float(drawdown.min())


def sharpe_ratio(equity_curve: pd.Series, risk_free_rate: float = 0.0, periods_per_year: int = 252) -> float:
    rets = compute_returns(equity_curve)
    excess = rets - risk_free_rate / periods_per_year
    std = excess.std()
    if std == 0:
        return 0.0
    return float(np.sqrt(periods_per_year) * excess.mean() / std)