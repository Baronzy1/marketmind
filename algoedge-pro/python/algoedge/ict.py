from __future__ import annotations
import pandas as pd


def detect_fvg(df: pd.DataFrame, lookback: int = 3) -> pd.Series:
    # Simple placeholder: gap between prior high and next low
    if not {"high", "low"}.issubset(df.columns):
        return pd.Series(False, index=df.index)
    prev_high = df["high"].shift(1)
    next_low = df["low"].shift(-1)
    fvg = next_low > prev_high
    return fvg.fillna(False)


def detect_bos(df: pd.DataFrame, lookback: int = 20) -> pd.Series:
    # Placeholder: price closes above max high of N bars
    rolling_max = df["close"].rolling(lookback).max()
    bos = df["close"] > rolling_max.shift(1)
    return bos.fillna(False)


def detect_order_blocks(df: pd.DataFrame, lookback: int = 20) -> pd.Series:
    # Placeholder: bullish OB = down candle before up break
    ob = (df["close"] > df["open"]) & (df["close"].shift(1) < df["open"].shift(1))
    return ob.fillna(False)