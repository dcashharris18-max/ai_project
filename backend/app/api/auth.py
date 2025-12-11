from fastapi import APIRouter, Depends, HTTPException, status, Form
from backend.app import schemas, crud, auth_utils
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from typing import Optional
from pydantic import ValidationError

router = APIRouter()


@router.post("/register", response_model=schemas.UserOut)
def register(
    user_in: Optional[schemas.UserCreate] = None,
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    # Accept either JSON body (UserCreate) or form-encoded fields for tests
    if user_in is None:
        if not email or not password:
            raise HTTPException(status_code=422, detail="Invalid request")
        try:
            user_in = schemas.UserCreate(email=email, password=password)
        except ValidationError:
            raise HTTPException(status_code=422, detail="Invalid email format")

    # Basic password strength: minimum length and contains a digit
    pw = user_in.password or ""
    if len(pw) < 8 or not any(ch.isdigit() for ch in pw):
        raise HTTPException(status_code=422, detail="Password too weak")

    user = crud.get_user_by_email(db, user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created = crud.create_user(db, user_in)
    return created


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = auth_utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = auth_utils.create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}
