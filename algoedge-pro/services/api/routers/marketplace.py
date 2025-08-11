from __future__ import annotations
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..models.marketplace import MarketplaceListing
from ..models.strategy import Strategy
from .auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/listings")
def list_listings(db: Session = Depends(get_db)):
    listings = db.query(MarketplaceListing).filter(MarketplaceListing.is_active == True).all()  # noqa: E712
    return [{"id": l.id, "strategy_id": l.strategy_id, "price_usd": str(l.price_usd)} for l in listings]


@router.post("/listings")
def create_listing(strategy_id: int, price_usd: float, db: Session = Depends(get_db), user=Depends(get_current_user)):
    strat = db.get(Strategy, strategy_id)
    if not strat or strat.user_id != user.id:
        raise HTTPException(status_code=404, detail="Strategy not found or not owned")
    listing = MarketplaceListing(strategy_id=strategy_id, price_usd=Decimal(str(price_usd)))
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return {"id": listing.id, "strategy_id": listing.strategy_id, "price_usd": str(listing.price_usd)}