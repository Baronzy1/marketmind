from __future__ import annotations
from typing import Any, Dict, Optional
from pydantic import BaseModel

class StrategyIn(BaseModel):
    name: str
    dsl: Dict[str, Any]
    is_public: bool = False

class StrategyOut(BaseModel):
    id: int
    name: str
    is_public: bool

    class Config:
        from_attributes = True

class BacktestRunOut(BaseModel):
    id: int
    strategy_id: int
    metrics: Dict[str, float]

    class Config:
        from_attributes = True