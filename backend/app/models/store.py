from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.session import Base
from datetime import datetime


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    country = Column(String, nullable=True)
    currency = Column(String, nullable=True, default="USD")
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User")
    listings = relationship("Listing", back_populates="store")
