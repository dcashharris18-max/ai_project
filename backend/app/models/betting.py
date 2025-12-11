"""Betting and casino game models with fairness verification."""
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    Text,
    Boolean,
)
from sqlalchemy.orm import relationship
import enum

from backend.app.db.session import Base


class GameType(str, enum.Enum):
    """Game categories."""

    SLOTS = "slots"
    BLACKJACK = "blackjack"
    ROULETTE = "roulette"
    DICE = "dice"
    CRASH = "crash"  # Popular crypto game


class GameStatus(str, enum.Enum):
    """Game session states."""

    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"
    CANCELED = "canceled"


class BetStatus(str, enum.Enum):
    """Individual bet states."""

    PENDING = "pending"
    WON = "won"
    LOST = "lost"
    PUSHED = "pushed"  # Draw
    CASHOUT = "cashout"


class Game(Base):
    """Casino/betting game definition."""

    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    game_type = Column(Enum(GameType), nullable=False)
    description = Column(Text)
    min_bet = Column(Float, nullable=False, default=0.01)
    max_bet = Column(Float, nullable=False, default=10000.00)
    house_edge_percent = Column(
        Float, default=2.5
    )  # House edge percentage (transparent)
    rules = Column(Text)  # Game rules in markdown
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sessions = relationship("GameSession", back_populates="game")
    bets = relationship("Bet", back_populates="game")


class GameSession(Base):
    """Single game session for a user."""

    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)

    # Wager details
    initial_wager = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")

    # Result
    result_amount = Column(Float)  # Winnings or loss amount
    status = Column(Enum(GameStatus), default=GameStatus.IN_PROGRESS)

    # Fairness
    seed_client = Column(String(256))  # Client-provided seed
    seed_server = Column(String(256))  # Server seed (revealed after)
    result_hash = Column(String(256))  # Hash of result for verification
    random_value = Column(Float)  # 0-1 result value (deterministic from seeds)

    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationships
    user = relationship("User", backref="game_sessions")
    game = relationship("Game", back_populates="sessions")
    bets = relationship("Bet", back_populates="session")


class Bet(Base):
    """Individual bet within a session (card in blackjack, number in roulette, etc)."""

    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)

    # Bet details
    amount = Column(Float, nullable=False)
    odds = Column(Float)  # Payout multiplier (1.5x, 2x, etc)
    winnings = Column(Float)  # Actual winnings if won

    # Selection
    selection = Column(String(255))  # "red", "17", "hit", "crash_at_2.5x", etc

    status = Column(Enum(BetStatus), default=BetStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    settled_at = Column(DateTime)

    # Relationships
    user = relationship("User", backref="bets")
    session = relationship("GameSession", back_populates="bets")
    game = relationship("Game", back_populates="bets")


class ResponsibleGamblingLimit(Base):
    """Self-imposed gambling limits for user."""

    __tablename__ = "responsible_gambling_limits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    daily_loss_limit = Column(Float)  # Max loss per day
    daily_spend_limit = Column(Float)  # Max spend per day
    session_time_limit_minutes = Column(Integer)  # Max session duration
    is_self_excluded = Column(Boolean, default=False)  # Self-exclusion period
    self_excluded_until = Column(DateTime)  # End of self-exclusion
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="gambling_limits")
