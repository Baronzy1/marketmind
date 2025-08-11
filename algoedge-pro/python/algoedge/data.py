from __future__ import annotations
import datetime as dt
from typing import Optional

import numpy as np
import pandas as pd

try:
    import ccxt  # type: ignore
except Exception:  # pragma: no cover - optional
    ccxt = None

try:
    import yfinance as yf  # type: ignore
except Exception:  # pragma: no cover - optional
    yf = None


TIMEFRAME_TO_MIN = {
    "1m": 1,
    "5m": 5,
    "15m": 15,
    "1h": 60,
    "4h": 240,
    "1d": 1440,
}


def _synthetic_ohlcv(start: pd.Timestamp, periods: int, minutes: int = 60, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dt_index = pd.date_range(start=start, periods=periods, freq=f"{minutes}T")
    price = 100 + np.cumsum(rng.normal(0, 0.5, size=periods))
    high = price + rng.normal(0.2, 0.2, size=periods)
    low = price - rng.normal(0.2, 0.2, size=periods)
    open_ = price + rng.normal(0.0, 0.1, size=periods)
    close = price
    volume = rng.integers(100, 1000, size=periods)
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": volume}, index=dt_index)


def load_ohlcv(
    symbol: str,
    market: str = "crypto",
    timeframe: str = "1h",
    years: int = 2,
    exchange: str = "binance",
    start: Optional[pd.Timestamp] = None,
) -> pd.DataFrame:
    minutes = TIMEFRAME_TO_MIN.get(timeframe, 60)
    periods = int((years * 365 * 24 * 60) / minutes)
    start = start or (pd.Timestamp.utcnow() - pd.Timedelta(days=years * 365))

    # Crypto via CCXT
    if market == "crypto" and ccxt is not None:
        try:
            ex = getattr(ccxt, exchange)()
            since_ms = int(start.timestamp() * 1000)
            batch = ex.fetch_ohlcv(symbol, timeframe=timeframe, since=since_ms, limit=min(1000, periods))
            if batch:
                df = pd.DataFrame(batch, columns=["timestamp", "open", "high", "low", "close", "volume"]).set_index("timestamp")
                df.index = pd.to_datetime(df.index, unit="ms")
                return df
        except Exception:
            pass

    # Stocks/Forex via yfinance
    if market in ("stocks", "forex") and yf is not None:
        try:
            interval = timeframe
            start_dt = (dt.datetime.utcnow() - dt.timedelta(days=years * 365)).strftime("%Y-%m-%d")
            df = yf.download(tickers=symbol, interval=interval, start=start_dt, progress=False)
            if not df.empty:
                df = df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"})
                return df[["open", "high", "low", "close", "volume"]]
        except Exception:
            pass

    # Fallback to synthetic data
    return _synthetic_ohlcv(start=start, periods=periods, minutes=minutes)