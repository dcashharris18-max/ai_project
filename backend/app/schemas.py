from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    dob: Optional[str] = None
    kyc_status: Optional[str] = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class KYCUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    country: Optional[str]
    address: Optional[str]
    dob: Optional[str]


class WalletCreate(BaseModel):
    address: str
    currency: Optional[str] = "BTC"


class WalletOut(BaseModel):
    id: int
    address: str
    currency: str
    balance: float
    created_at: datetime

    class Config:
        orm_mode = True


class StoreCreate(BaseModel):
    name: str
    description: Optional[str] = None
    country: Optional[str] = None
    currency: Optional[str] = "USD"


class StoreOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    country: Optional[str]
    currency: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class ListingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    currency: Optional[str] = "USD"
    stock: Optional[int] = 1


class ListingOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    currency: str
    stock: int
    media_path: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class OrderItemCreate(BaseModel):
    listing_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    store_id: int
    items: list[OrderItemCreate]
    currency: Optional[str] = "USD"


class OrderOut(BaseModel):
    id: int
    user_id: int
    store_id: int
    total_amount: float
    currency: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    content: Optional[str]


class PostOut(BaseModel):
    id: int
    content: Optional[str]
    media_path: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
