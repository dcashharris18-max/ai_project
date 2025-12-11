from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from backend.app.db.session import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # KYC fields
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    country = Column(String, nullable=True)
    address = Column(String, nullable=True)
    dob = Column(String, nullable=True)  # ISO date string (YYYY-MM-DD)
    kyc_status = Column(String, default="pending")  # pending, approved, rejected
    kyc_document_path = Column(String, nullable=True)

    # Relationships
    wallets = relationship("Wallet", back_populates="owner")
