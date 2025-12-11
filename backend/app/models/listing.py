from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.session import Base
from datetime import datetime


class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    currency = Column(String, nullable=False, default="USD")
    stock = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    media_path = Column(String, nullable=True)

    store = relationship("Store", back_populates="listings")
