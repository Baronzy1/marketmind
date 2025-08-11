from __future__ import annotations
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    dsl = Column(JSON, nullable=False)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", backref="strategies")