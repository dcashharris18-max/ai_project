from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app import crud, schemas, auth_utils, services

router = APIRouter()


@router.post("/", response_model=schemas.OrderOut)
def create_order(
    order_in: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    try:
        order = crud.create_order(db, current_user.id, order_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # For MVP: create a placeholder payment intent (Stripe or crypto)
    # Here we use the payments service to create a payment intent
    # amount in cents for stripe
    try:
        amount_cents = int(order.total_amount * 100)
        services.payments.create_stripe_payment(
            amount_cents,
            currency=order.currency,
            description=f"Order {order.id}",
        )
        # In a real flow, we'd store payment intent id and return client secret
    except Exception:
        # If stripe not configured, create crypto placeholder
        services.payments.create_crypto_payment_intent(order.total_amount, currency="BTC")

    return order
