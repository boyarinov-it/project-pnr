from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomRead

router = APIRouter(tags=["rooms"])


@router.post("/projects/{project_id}/rooms", response_model=RoomRead)
def create_room(project_id: int, payload: RoomCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    room = Room(
        project_id=project_id,
        name=payload.name,
        code=payload.code,
        name_ru=payload.name_ru,
        name_en=payload.name_en,
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.get("/projects/{project_id}/rooms", response_model=list[RoomRead])
def list_rooms(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return (
        db.query(Room)
        .filter(Room.project_id == project_id)
        .order_by(Room.id.asc())
        .all()
    )
