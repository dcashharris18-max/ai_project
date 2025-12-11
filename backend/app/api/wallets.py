from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.app.api.utils import parse_model_factory
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app import crud, schemas, auth_utils
from backend.app.models.transaction import Transfer, AILog

router = APIRouter()


class TransferCreate(BaseModel):
    recipient_user_id: int
    amount: float
    currency: str = "BTC"


@router.post("/transfer")
def transfer_funds(
    transfer_in: TransferCreate = Depends(parse_model_factory(TransferCreate)),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """Transfer funds to another user by user_id (Binance-style)."""
    recipient_id = int(transfer_in.recipient_user_id)
    recipient = crud.get_user_by_id(db, recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    # Create transfer record
    transfer = Transfer(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        amount=transfer_in.amount,
        currency=transfer_in.currency,
        status="completed",
    )
    db.add(transfer)

    # Create AI logs for both users
    log_sender = AILog(
        user_id=current_user.id,
        message=f"Sent {transfer_in.amount} {transfer_in.currency} to user {recipient_id}",
        log_type="transfer",
    )
    log_recipient = AILog(
        user_id=recipient_id,
        message=f"Received {transfer_in.amount} {transfer_in.currency} from user {current_user.id}",
        log_type="transfer",
    )
    db.add(log_sender)
    db.add(log_recipient)
    db.commit()

    return {"status": "success", "transfer_id": transfer.id}


@router.get("/logs")
def get_logs(
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """Get AI activity logs for current user."""
    logs = (
        db.query(AILog)
        .filter(AILog.user_id == current_user.id)
        .order_by(AILog.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "timestamp": log.created_at.isoformat(),
            "message": log.message,
            "type": log.log_type,
        }
        for log in logs
    ]
