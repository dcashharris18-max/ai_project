"""Construction project models - contractors bid on projects with drawings."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from backend.app.db.session import Base


class ProjectStatus(str, enum.Enum):
    """Project lifecycle states."""

    OPEN = "open"  # Accepting bids
    AWARDED = "awarded"  # Contractor selected
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class BidStatus(str, enum.Enum):
    """Bid states."""

    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Project(Base):
    """Construction project with drawings and contractor bids."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    budget_min = Column(Float, nullable=False)  # Minimum budget estimate
    budget_max = Column(Float, nullable=False)  # Maximum budget estimate
    currency = Column(String(10), default="USD")
    status = Column(Enum(ProjectStatus), default=ProjectStatus.OPEN)
    location = Column(String(255))  # Project location
    timeline_days = Column(Integer)  # Estimated completion days
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", foreign_keys=[owner_id], backref="projects_owned")
    drawings = relationship(
        "Drawing", back_populates="project", cascade="all, delete-orphan"
    )
    bids = relationship("Bid", back_populates="project", cascade="all, delete-orphan")
    awarded_contractor_id = Column(Integer, ForeignKey("users.id"))  # Contractor hired
    awarded_contractor = relationship(
        "User", foreign_keys=[awarded_contractor_id], backref="projects_awarded"
    )


class Drawing(Base):
    """2D/3D drawings for project."""

    __tablename__ = "drawings"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    file_path = Column(String(500), nullable=False)  # S3 or local storage
    format = Column(String(50), nullable=False)  # "2d", "3d", "pdf", "dwg", "blend"
    file_size_bytes = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(Integer, ForeignKey("users.id"))  # Who uploaded

    # Relationships
    project = relationship("Project", back_populates="drawings")
    uploader = relationship("User", foreign_keys=[uploaded_by], backref="drawings_uploaded")


class Bid(Base):
    """Contractor bid on project."""

    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    contractor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    proposed_timeline_days = Column(Integer)  # How long contractor estimates
    notes = Column(Text)  # Contractor's pitch
    status = Column(Enum(BidStatus), default=BidStatus.SUBMITTED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="bids")
    contractor = relationship("User", foreign_keys=[contractor_id], backref="bids_submitted")
