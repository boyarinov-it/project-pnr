from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.fan import Fan
from app.models.room import Room
from app.schemas.fan import FanCreate, FanRead, FanUpdate
from app.services.explication_resolver import get_project_or_404, get_room_by_number_or_404

router = APIRouter(tags=["fans"])


def build_room_name(room: Room) -> str:
    return room.name_ru or room.name or room.code


def build_fan_display_name(room: Room, fan: Fan) -> str:
    return f"{build_room_name(room)} - {fan.name}"


def build_fan_read(fan: Fan) -> FanRead:
    room = fan.room

    return FanRead(
        id=fan.id,
        project_id=fan.project_id,
        room_id=fan.room_id,
        room_number=room.room_number,
        room_name=build_room_name(room),
        display_name=build_fan_display_name(room, fan),
        name=fan.name,
        code=fan.code,
        quantity=fan.quantity,
        device_type=fan.device_type,
        device_address=fan.device_address,
        device_channel=fan.device_channel,
    )


@router.post("/projects/{project_id}/fans", response_model=FanRead)
def create_fan(project_id: int, payload: FanCreate, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)
    room = get_room_by_number_or_404(db, project_id, payload.room_number)

    fan = Fan(
        project_id=project_id,
        room_id=room.id,
        name=payload.name,
        code=payload.code,
        quantity=payload.quantity,
        device_type=payload.device_type,
        device_address=payload.device_address,
        device_channel=payload.device_channel,
    )

    db.add(fan)
    db.commit()
    db.refresh(fan)

    return build_fan_read(fan)


@router.get("/projects/{project_id}/fans", response_model=list[FanRead])
def list_fans(project_id: int, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)

    fans = (
        db.query(Fan)
        .join(Room, Fan.room_id == Room.id)
        .filter(Fan.project_id == project_id)
        .order_by(Fan.id.asc())
        .all()
    )

    return [build_fan_read(fan) for fan in fans]


@router.put("/fans/{fan_id}", response_model=FanRead)
def update_fan(
    fan_id: int,
    payload: FanUpdate,
    db: Session = Depends(get_db),
):
    fan = db.query(Fan).filter(Fan.id == fan_id).first()
    if not fan:
        raise HTTPException(status_code=404, detail="Fan item not found")

    room = get_room_by_number_or_404(db, fan.project_id, payload.room_number)

    fan.room_id = room.id
    fan.name = payload.name
    fan.code = payload.code
    fan.quantity = payload.quantity
    fan.device_type = payload.device_type
    fan.device_address = payload.device_address
    fan.device_channel = payload.device_channel

    db.commit()
    db.refresh(fan)

    return build_fan_read(fan)


@router.delete("/fans/{fan_id}")
def delete_fan(fan_id: int, db: Session = Depends(get_db)):
    fan = db.query(Fan).filter(Fan.id == fan_id).first()
    if not fan:
        raise HTTPException(status_code=404, detail="Fan item not found")

    db.delete(fan)
    db.commit()

    return {"status": "deleted", "fan_id": fan_id}
