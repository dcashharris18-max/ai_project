from fastapi import APIRouter, Depends, HTTPException
from backend.app.api.utils import parse_model_factory
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app import crud, schemas, auth_utils
from fastapi import UploadFile, File
import os
from pathlib import Path

router = APIRouter()


@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user=Depends(auth_utils.get_current_active_user)):
    return current_user


@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@router.post("/me/kyc", response_model=schemas.UserOut)
def submit_kyc(
    kyc: schemas.KYCUpdate,
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """Submit KYC information and optional document upload."""
    document_path = None
    if file:
        storage_dir = Path(
            os.path.join(os.path.dirname(__file__), "..", "..", "storage", "kyc")
        ).resolve()
        storage_dir.mkdir(parents=True, exist_ok=True)
        filename = f"user_{current_user.id}_{file.filename}"
        dest = storage_dir / filename
        with open(dest, "wb") as f:
            f.write(file.file.read())
        document_path = str(dest)

    updated = crud.update_user_kyc(
        db, current_user.id, kyc, document_path=document_path
    )
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.post("/me/wallets", response_model=schemas.WalletOut)
def add_wallet(
    wallet_in: schemas.WalletCreate = Depends(
        parse_model_factory(schemas.WalletCreate)
    ),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    w = crud.create_wallet(db, current_user.id, wallet_in)
    return w


@router.get("/me/wallets", response_model=list[schemas.WalletOut])
def list_wallets(
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    return crud.get_wallets_for_user(db, current_user.id)
