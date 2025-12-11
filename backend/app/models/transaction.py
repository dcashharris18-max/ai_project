from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from backend.app.db.session import Base
from datetime import datetime


class Transfer(Base):
    __tablename__ = "transfers"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False, default="BTC")
    status = Column(String, default="completed")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)


class AILog(Base):
    __tablename__ = "ai_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    message = Column(String, nullable=False)
    log_type = Column(String, default="action")  # action, trade, transfer, system
    created_at = Column(DateTime, default=datetime.utcnow)
