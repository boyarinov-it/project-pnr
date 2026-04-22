from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomRead

router = APIRouter(prefix="/projects/{project_id}/rooms", tags=["rooms"])

@router.post("", response_model=RoomRead)
def create_room(project_id: int, payload: RoomCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    existing = db.query(Room).filter(Room.project_id == project_id, Room.code == payload.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Room code already exists in project")

    room = Room(project_id=project_id, name=payload.name, code=payload.code)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.get("", response_model=list[RoomRead])
def list_rooms(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.query(Room).filter(Room.project_id == project_id).order_by(Room.id.asc()).all()
