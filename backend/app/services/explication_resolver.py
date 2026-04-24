from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.room import Room


def get_project_or_404(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def get_room_by_number_or_404(db: Session, project_id: int, room_number: str) -> Room:
    room = (
        db.query(Room)
        .filter(Room.project_id == project_id, Room.room_number == room_number)
        .first()
    )

    if not room:
        raise HTTPException(status_code=404, detail="Room with given room_number not found")

    return room
