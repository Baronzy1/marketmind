from __future__ import annotations
from typing import Optional

try:
    import ccxt  # type: ignore
except Exception:  # pragma: no cover
    ccxt = None


class BinanceConnector:
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        if ccxt is None:
            raise RuntimeError("ccxt not available")
        self.ex = ccxt.binance({
            "apiKey": api_key or "",
            "secret": api_secret or "",
            "enableRateLimit": True,
        })

    def fetch_balance(self):
        return self.ex.fetch_balance()

    def create_order(self, symbol: str, side: str, type_: str, amount: float, price: Optional[float] = None):
        return self.ex.create_order(symbol, type_, side, amount, price)