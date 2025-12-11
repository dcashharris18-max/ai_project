"""Payments skeleton: Stripe (fiat) + crypto placeholders.

This file provides minimal wrappers for charging via Stripe
and for recording crypto payment intents. Replace with production
grade code and secret management before using in live environments.
"""
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

try:
    import stripe

    if STRIPE_API_KEY:
        stripe.api_key = STRIPE_API_KEY
except Exception:
    stripe = None


def create_stripe_payment(
    amount_cents: int,
    currency: str = "usd",
    description: str = "",
    return_url: str | None = None,
):
    if not stripe:
        raise RuntimeError("Stripe library not available or API key not configured")
    # Create a PaymentIntent (server-side)
    payment_intent = stripe.PaymentIntent.create(
        amount=amount_cents,
        currency=currency,
        description=description,
    )
    return payment_intent


def create_crypto_payment_intent(
    amount: float, currency: str = "BTC", address: str | None = None
):
    """Placeholder for creating an on-chain payment intent.

    In production you'd create a unique deposit address or a payment request
    and monitor blockchain confirmations.
    """
    return {
        "amount": amount,
        "currency": currency,
        "address": address or "blockchain-generated-address-placeholder",
        "status": "pending",
    }
