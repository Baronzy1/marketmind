from __future__ import annotations
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, Numeric, Boolean
from .base import Base

class MarketplaceListing(Base):
    __tablename__ = "marketplace_listings"

    id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False, index=True)
    price_usd = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())