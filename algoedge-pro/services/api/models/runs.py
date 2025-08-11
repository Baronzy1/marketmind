from __future__ import annotations
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
from .base import Base

class BacktestRun(Base):
    __tablename__ = "backtest_runs"

    id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    symbol = Column(String(100), nullable=False)
    market = Column(String(50), nullable=False)
    timeframe = Column(String(20), nullable=False)
    years = Column(Integer, nullable=False)
    metrics = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    strategy = relationship("Strategy", backref="runs")