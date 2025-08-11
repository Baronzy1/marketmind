from __future__ import annotations
import os
from fastapi import APIRouter, HTTPException, Request
import stripe as stripe_sdk

router = APIRouter()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe_sdk.api_key = STRIPE_SECRET_KEY


@router.post("/checkout")
async def create_checkout_session(amount_cents: int, currency: str = "usd"):
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=400, detail="Stripe not configured")
    session = stripe_sdk.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price_data": {"currency": currency, "product_data": {"name": "AlgoEdge Strategy"}, "unit_amount": amount_cents}, "quantity": 1}],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return {"id": session.id, "url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request):
    # TODO: verify webhook and fulfill
    payload = await request.body()
    return {"received": True}