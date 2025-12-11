from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from backend.app.api.utils import parse_model_factory
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app import crud, schemas, auth_utils
from pathlib import Path
import os

router = APIRouter()


@router.post("/stores", response_model=schemas.StoreOut)
def create_store(
    store_in: schemas.StoreCreate = Depends(parse_model_factory(schemas.StoreCreate)),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    s = crud.create_store(db, current_user.id, store_in)
    return s


@router.get("/stores", response_model=list[schemas.StoreOut])
def list_my_stores(
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    return crud.get_stores_for_user(db, current_user.id)


@router.post("/stores/{store_id}/listings", response_model=schemas.ListingOut)
def create_listing(
    store_id: int,
    listing_in: schemas.ListingCreate = Depends(
        parse_model_factory(schemas.ListingCreate)
    ),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    # minimal authorization: check store ownership
    store = (
        db.query(crud.Store if hasattr(crud, "Store") else None)
        .filter_by(id=store_id)
        .first()
    )
    # fallback: query directly
    from backend.app.models.store import Store as StoreModel

    store = db.query(StoreModel).filter(StoreModel.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not store owner")

    media_path = None
    if file:
        storage_dir = Path(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "storage", "product_images"
            )
        ).resolve()
        storage_dir.mkdir(parents=True, exist_ok=True)
        filename = f"store_{store_id}_{file.filename}"
        dest = storage_dir / filename
        with open(dest, "wb") as f:
            f.write(file.file.read())
        media_path = str(dest)

    listing = crud.create_listing(db, store_id, listing_in, media_path=media_path)
    return listing


@router.get("/stores/{store_id}/listings")
def get_listings(store_id: int, db: Session = Depends(get_db)):
    listings = crud.get_listings_for_store(db, store_id)
    return {"listings": listings}
