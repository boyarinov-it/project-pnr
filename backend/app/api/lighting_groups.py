from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.lighting_group import LightingGroup
from app.models.project import Project
from app.models.room import Room
from app.schemas.lighting_group import LightingGroupCreate, LightingGroupRead

router = APIRouter(prefix="/projects/{project_id}/lighting-groups", tags=["lighting-groups"])

@router.post("", response_model=LightingGroupRead)
def create_lighting_group(project_id: int, payload: LightingGroupCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    room = db.query(Room).filter(Room.id == payload.room_id, Room.project_id == project_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found in project")

    existing = db.query(LightingGroup).filter(LightingGroup.project_id == project_id, LightingGroup.code == payload.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Lighting group code already exists in project")

    group = LightingGroup(
        project_id=project_id,
        room_id=payload.room_id,
        name=payload.name,
        code=payload.code,
        load_type=payload.load_type,
        quantity=payload.quantity
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

@router.get("", response_model=list[LightingGroupRead])
def list_lighting_groups(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.query(LightingGroup).filter(LightingGroup.project_id == project_id).order_by(LightingGroup.id.asc()).all()
