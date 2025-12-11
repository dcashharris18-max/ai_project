from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app import schemas
from backend.app.auth_utils import get_password_hash

from backend.app.models.wallet import Wallet
from backend.app.models.store import Store
from backend.app.models.listing import Listing
from backend.app.models.post import Post
from backend.app.models.order import Order, OrderItem


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_in: schemas.UserCreate):
    hashed = get_password_hash(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_user_kyc(
    db: Session,
    user_id: int,
    kyc_data: schemas.KYCUpdate,
    document_path: str | None = None,
):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    for field, value in kyc_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    if document_path:
        user.kyc_document_path = document_path
        user.kyc_status = "pending"
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_wallet(db: Session, user_id: int, wallet_in: schemas.WalletCreate):
    # Basic creation; no blockchain integration here.
    wallet = Wallet(
        user_id=user_id, address=wallet_in.address, currency=wallet_in.currency
    )
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet


def get_wallets_for_user(db: Session, user_id: int):
    return db.query(Wallet).filter(Wallet.user_id == user_id).all()


def create_store(db: Session, user_id: int, store_in: schemas.StoreCreate):
    store = Store(
        owner_id=user_id,
        name=store_in.name,
        description=store_in.description,
        country=store_in.country,
        currency=store_in.currency,
    )
    db.add(store)
    db.commit()
    db.refresh(store)
    return store


def get_stores_for_user(db: Session, user_id: int):
    return db.query(Store).filter(Store.owner_id == user_id).all()


def create_listing(
    db: Session,
    store_id: int,
    listing_in: schemas.ListingCreate,
    media_path: str | None = None,
):
    listing = Listing(
        store_id=store_id,
        title=listing_in.title,
        description=listing_in.description,
        price=listing_in.price,
        currency=listing_in.currency,
        stock=listing_in.stock,
        media_path=media_path,
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


def get_listings_for_store(db: Session, store_id: int):
    return db.query(Listing).filter(Listing.store_id == store_id).all()


def create_post(
    db: Session,
    user_id: int,
    post_in: schemas.PostCreate,
    media_path: str | None = None,
):
    post = Post(user_id=user_id, content=post_in.content, media_path=media_path)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_posts_feed(db: Session, limit: int = 50):
    return db.query(Post).order_by(Post.created_at.desc()).limit(limit).all()


def create_order(db: Session, user_id: int, order_in: schemas.OrderCreate):
    # Simplified order creation: calculate total and create order + items
    total = 0.0
    for item in order_in.items:
        listing = db.query(Listing).filter(Listing.id == item.listing_id).first()
        if not listing:
            raise ValueError(f"Listing {item.listing_id} not found")
        total += listing.price * item.quantity

    order = Order(
        user_id=user_id,
        store_id=order_in.store_id,
        total_amount=total,
        currency=order_in.currency,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in order_in.items:
        listing = db.query(Listing).filter(Listing.id == item.listing_id).first()
        oi = OrderItem(
            order_id=order.id,
            listing_id=listing.id,
            quantity=item.quantity,
            price=listing.price,
        )
        db.add(oi)
    db.commit()
    db.refresh(order)
    return order
