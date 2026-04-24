from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomRead, RoomUpdate

router = APIRouter(tags=["rooms"])


@router.post("/projects/{project_id}/rooms", response_model=RoomRead)
def create_room(project_id: int, payload: RoomCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    room = Room(
        project_id=project_id,
        room_number=payload.room_number,
        name=payload.name,
        code=payload.code,
        name_ru=payload.name_ru,
        name_en=payload.name_en,
    )
    db.add(room)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Room number must be unique within project")

    db.refresh(room)
    return room


@router.put("/rooms/{room_id}", response_model=RoomRead)
def update_room(room_id: int, payload: RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    room.room_number = payload.room_number
    room.name = payload.name
    room.code = payload.code
    room.name_ru = payload.name_ru
    room.name_en = payload.name_en

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Room number must be unique within project")

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
        .order_by(Room.room_number.asc(), Room.id.asc())
        .all()
    )


@router.get("/projects/{project_id}/rooms/by-number/{room_number}", response_model=RoomRead)
def get_room_by_number(project_id: int, room_number: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    room = (
        db.query(Room)
        .filter(Room.project_id == project_id, Room.room_number == room_number)
        .first()
    )
    if not room:
        raise HTTPException(status_code=404, detail="Room with given room_number not found")

    return room
