from fastapi import APIRouter, Depends, UploadFile, File
from backend.app.api.utils import parse_model_factory
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app import crud, schemas, auth_utils
from pathlib import Path
import os

router = APIRouter()


@router.post("/posts", response_model=schemas.PostOut)
def create_post(
    post_in: schemas.PostCreate = Depends(parse_model_factory(schemas.PostCreate)),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    media_path = None
    if file:
        storage_dir = Path(
            os.path.join(os.path.dirname(__file__), "..", "..", "storage", "media")
        ).resolve()
        storage_dir.mkdir(parents=True, exist_ok=True)
        filename = f"user_{current_user.id}_{file.filename}"
        dest = storage_dir / filename
        with open(dest, "wb") as f:
            f.write(file.file.read())
        media_path = str(dest)
    post = crud.create_post(db, current_user.id, post_in, media_path=media_path)
    return post


@router.get("/feed")
def feed(db: Session = Depends(get_db)):
    posts = crud.get_posts_feed(db)
    return {"posts": posts}
