from __future__ import annotations
from typing import Optional

try:
    from ib_insync import IB, Stock, MarketOrder  # type: ignore
except Exception:  # pragma: no cover
    IB = None  # type: ignore


class IBConnector:
    def __init__(self, host: str = "127.0.0.1", port: int = 4002, client_id: int = 1):
        if IB is None:
            raise RuntimeError("ib_insync not available")
        self.ib = IB()
        self.ib.connect(host, port, clientId=client_id)

    def place_market_order(self, symbol: str, exchange: str = "SMART", currency: str = "USD", qty: float = 1.0, side: str = "BUY"):
        contract = Stock(symbol, exchange, currency)
        order = MarketOrder(side, qty)
        trade = self.ib.placeOrder(contract, order)
        return trade.orderStatus.status