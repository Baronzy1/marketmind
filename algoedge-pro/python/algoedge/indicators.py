from __future__ import annotations
import pandas as pd
import pandas_ta as ta


def ensure_column(df: pd.DataFrame, source: str) -> pd.Series:
    if source in df.columns:
        return df[source]
    # Fallback to close
    return df[df.columns[0]] if df.columns else pd.Series(dtype=float)


def ema(df: pd.DataFrame, length: int = 20, source: str = "close") -> pd.Series:
    s = ensure_column(df, source)
    return ta.ema(s, length=length)


def sma(df: pd.DataFrame, length: int = 20, source: str = "close") -> pd.Series:
    s = ensure_column(df, source)
    return ta.sma(s, length=length)


def rsi(df: pd.DataFrame, length: int = 14, source: str = "close") -> pd.Series:
    s = ensure_column(df, source)
    return ta.rsi(s, length=length)


def macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9, source: str = "close") -> pd.DataFrame:
    s = ensure_column(df, source)
    macd_df = ta.macd(s, fast=fast, slow=slow, signal=signal)
    return macd_df


def bollinger_bands(df: pd.DataFrame, length: int = 20, std: float = 2.0, source: str = "close") -> pd.DataFrame:
    s = ensure_column(df, source)
    bb = ta.bbands(s, length=length, std=std)
    return bb


def vwap(df: pd.DataFrame) -> pd.Series:
    if {"high", "low", "close", "volume"}.issubset(df.columns):
        return ta.vwap(high=df["high"], low=df["low"], close=df["close"], volume=df["volume"])
    return pd.Series(index=df.index, dtype=float)