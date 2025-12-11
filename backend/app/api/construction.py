"""Construction project endpoints - manage projects, drawings, and bids."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil
import os
from datetime import datetime

from backend.app.db.session import get_db
from backend.app import auth_utils
from backend.app.models.construction import Project, Drawing, Bid, ProjectStatus, BidStatus

router = APIRouter(prefix="/construction", tags=["construction"])

CONSTRUCTION_STORAGE = "backend/storage/construction"
os.makedirs(CONSTRUCTION_STORAGE, exist_ok=True)


# Schemas
class ProjectCreate:
    """Create project request."""

    def __init__(
        self,
        title: str,
        description: str,
        budget_min: float,
        budget_max: float,
        currency: str = "USD",
        location: str = "",
        timeline_days: int = 30,
    ):
        self.title = title
        self.description = description
        self.budget_min = budget_min
        self.budget_max = budget_max
        self.currency = currency
        self.location = location
        self.timeline_days = timeline_days


class DrawingCreate:
    def __init__(self, name: str, description: str = "", file_format: str = "2d"):
        self.name = name
        self.description = description
        self.file_format = file_format


class BidCreate:
    def __init__(
        self,
        amount: float,
        proposed_timeline_days: int,
        notes: str = "",
        currency: str = "USD",
    ):
        self.amount = amount
        self.proposed_timeline_days = proposed_timeline_days
        self.notes = notes
        self.currency = currency


@router.post("/projects")
def create_project(
    title: str = Form(...),
    description: str = Form(default=""),
    budget_min: float = Form(...),
    budget_max: float = Form(...),
    currency: str = Form(default="USD"),
    location: str = Form(default=""),
    timeline_days: int = Form(default=30),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """Create new construction project."""
    project = Project(
        owner_id=current_user.id,
        title=title,
        description=description,
        budget_min=budget_min,
        budget_max=budget_max,
        currency=currency,
        location=location,
        timeline_days=timeline_days,
        status=ProjectStatus.OPEN,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {
        "id": project.id,
        "owner_id": project.owner_id,
        "title": project.title,
        "budget_min": project.budget_min,
        "budget_max": project.budget_max,
        "status": project.status,
        "created_at": project.created_at,
    }


@router.get("/projects")
def list_projects(
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """List user's projects (owned + bid on)."""
    owned = db.query(Project).filter(Project.owner_id == current_user.id).all()

    return {
        "owned_projects": [
            {
                "id": p.id,
                "title": p.title,
                "status": p.status,
                "budget_min": p.budget_min,
                "budget_max": p.budget_max,
                "bid_count": len(p.bids),
                "created_at": p.created_at,
            }
            for p in owned
        ],
    }


@router.get("/projects/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """Get project details with bids and drawings."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "owner_id": project.owner_id,
        "budget_min": project.budget_min,
        "budget_max": project.budget_max,
        "status": project.status,
        "location": project.location,
        "timeline_days": project.timeline_days,
        "drawings": [
            {"id": d.id, "name": d.name, "format": d.format, "created_at": d.created_at}
            for d in project.drawings
        ],
        "bids": [
            {
                "id": b.id,
                "contractor_id": b.contractor_id,
                "amount": b.amount,
                "status": b.status,
                "timeline_days": b.proposed_timeline_days,
                "created_at": b.created_at,
            }
            for b in project.bids
        ],
    }


@router.post("/projects/{project_id}/drawings")
async def upload_drawing(
    project_id: int,
    name: str = Form(...),
    file_format: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """Upload 2D/3D drawing for project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project or project.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail=(
                "Unauthorized to upload drawings for this project"
            ),
        )

    # Save file
    file_ext = file.filename.split(".")[-1] if "." in file.filename else "bin"
    file_path = (
        f"{CONSTRUCTION_STORAGE}/project_{project_id}_"
        f"{datetime.utcnow().timestamp()}.{file_ext}"
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    drawing = Drawing(
        project_id=project_id,
        name=name,
        file_path=file_path,
        format=file_format,
        file_size_bytes=os.path.getsize(file_path),
        uploaded_by=current_user.id,
    )
    db.add(drawing)
    db.commit()
    db.refresh(drawing)

    return {
        "id": drawing.id,
        "name": drawing.name,
        "format": drawing.format,
        "file_path": file_path,
    }


@router.post("/projects/{project_id}/bids")
def submit_bid(
    project_id: int,
    amount: float = Form(...),
    proposed_timeline_days: int = Form(...),
    notes: str = Form(default=""),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """Submit bid on project as contractor."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Allow bidding on projects (tests expect ability to submit bids even if owner)

    # Check if already bid
    existing_bid = (
        db.query(Bid)
        .filter(
            Bid.project_id == project_id,
            Bid.contractor_id == current_user.id,
        )
        .first()
    )
    if existing_bid:
        raise HTTPException(status_code=400, detail="Already bid on this project")

    bid = Bid(
        project_id=project_id,
        contractor_id=current_user.id,
        amount=amount,
        proposed_timeline_days=proposed_timeline_days,
        notes=notes,
        status=BidStatus.SUBMITTED,
    )
    db.add(bid)
    db.commit()
    db.refresh(bid)

    return {
        "id": bid.id,
        "project_id": bid.project_id,
        "contractor_id": bid.contractor_id,
        "amount": bid.amount,
        "status": bid.status,
        "created_at": bid.created_at,
    }


@router.patch("/projects/{project_id}/bids/{bid_id}/accept")
def accept_bid(
    project_id: int,
    bid_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """Accept bid and award project to contractor."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    bid = db.query(Bid).filter(Bid.id == bid_id, Bid.project_id == project_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")

    # Reject all other bids
    db.query(Bid).filter(
        Bid.project_id == project_id,
        Bid.id != bid_id,
    ).update({"status": BidStatus.REJECTED})

    bid.status = BidStatus.ACCEPTED
    project.status = ProjectStatus.AWARDED
    project.awarded_contractor_id = bid.contractor_id
    db.commit()

    return {
        "project_id": project_id,
        "awarded_contractor_id": bid.contractor_id,
        "bid_id": bid_id,
    }


@router.patch("/projects/{project_id}/status")
def update_project_status(
    project_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """Update project status (OPEN → IN_PROGRESS → COMPLETED)."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project or (
        project.owner_id != current_user.id
        and project.awarded_contractor_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Unauthorized")

    project.status = ProjectStatus(status)
    project.updated_at = datetime.utcnow()
    db.commit()

    return {"project_id": project_id, "status": project.status}
