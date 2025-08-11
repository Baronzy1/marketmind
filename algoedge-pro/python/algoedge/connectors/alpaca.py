from __future__ import annotations
from typing import Optional

try:
    import alpaca_trade_api as tradeapi  # type: ignore
except Exception:  # pragma: no cover
    tradeapi = None


class AlpacaConnector:
    def __init__(self, api_key: str, api_secret: str, base_url: Optional[str] = None):
        if tradeapi is None:
            raise RuntimeError("alpaca-trade-api not available")
        self.api = tradeapi.REST(api_key, api_secret, base_url or "https://paper-api.alpaca.markets")

    def get_account(self):
        return self.api.get_account()._raw

    def submit_order(self, symbol: str, qty: float, side: str, type_: str = "market"):
        return self.api.submit_order(symbol=symbol, qty=qty, side=side, type=type_)