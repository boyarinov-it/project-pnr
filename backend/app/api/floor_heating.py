from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.floor_heating import FloorHeating
from app.models.room import Room
from app.schemas.floor_heating import FloorHeatingCreate, FloorHeatingRead, FloorHeatingUpdate
from app.services.explication_resolver import get_project_or_404, get_room_by_number_or_404

router = APIRouter(tags=["floor-heating"])


def build_room_name(room: Room) -> str:
    return room.name_ru or room.name or room.code


def build_floor_heating_display_name(room: Room, floor_heating: FloorHeating) -> str:
    return f"{build_room_name(room)} - {floor_heating.name}"


def build_floor_heating_read(floor_heating: FloorHeating) -> FloorHeatingRead:
    room = floor_heating.room

    return FloorHeatingRead(
        id=floor_heating.id,
        project_id=floor_heating.project_id,
        room_id=floor_heating.room_id,
        room_number=room.room_number,
        room_name=build_room_name(room),
        display_name=build_floor_heating_display_name(room, floor_heating),
        name=floor_heating.name,
        code=floor_heating.code,
        thermostat_type=floor_heating.thermostat_type,
        quantity=floor_heating.quantity,
        device_type=floor_heating.device_type,
        device_address=floor_heating.device_address,
        device_channel=floor_heating.device_channel,
    )


@router.post("/projects/{project_id}/floor-heating", response_model=FloorHeatingRead)
def create_floor_heating(project_id: int, payload: FloorHeatingCreate, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)
    room = get_room_by_number_or_404(db, project_id, payload.room_number)

    floor_heating = FloorHeating(
        project_id=project_id,
        room_id=room.id,
        name=payload.name,
        code=payload.code,
        thermostat_type=payload.thermostat_type,
        quantity=payload.quantity,
        device_type=payload.device_type,
        device_address=payload.device_address,
        device_channel=payload.device_channel,
    )

    db.add(floor_heating)
    db.commit()
    db.refresh(floor_heating)

    return build_floor_heating_read(floor_heating)


@router.get("/projects/{project_id}/floor-heating", response_model=list[FloorHeatingRead])
def list_floor_heating(project_id: int, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)

    floor_heating_items = (
        db.query(FloorHeating)
        .join(Room, FloorHeating.room_id == Room.id)
        .filter(FloorHeating.project_id == project_id)
        .order_by(FloorHeating.id.asc())
        .all()
    )

    return [build_floor_heating_read(item) for item in floor_heating_items]


@router.put("/floor-heating/{floor_heating_id}", response_model=FloorHeatingRead)
def update_floor_heating(
    floor_heating_id: int,
    payload: FloorHeatingUpdate,
    db: Session = Depends(get_db),
):
    floor_heating = db.query(FloorHeating).filter(FloorHeating.id == floor_heating_id).first()
    if not floor_heating:
        raise HTTPException(status_code=404, detail="Floor heating item not found")

    room = get_room_by_number_or_404(db, floor_heating.project_id, payload.room_number)

    floor_heating.room_id = room.id
    floor_heating.name = payload.name
    floor_heating.code = payload.code
    floor_heating.thermostat_type = payload.thermostat_type
    floor_heating.quantity = payload.quantity
    floor_heating.device_type = payload.device_type
    floor_heating.device_address = payload.device_address
    floor_heating.device_channel = payload.device_channel

    db.commit()
    db.refresh(floor_heating)

    return build_floor_heating_read(floor_heating)


@router.delete("/floor-heating/{floor_heating_id}")
def delete_floor_heating(floor_heating_id: int, db: Session = Depends(get_db)):
    floor_heating = db.query(FloorHeating).filter(FloorHeating.id == floor_heating_id).first()
    if not floor_heating:
        raise HTTPException(status_code=404, detail="Floor heating item not found")

    db.delete(floor_heating)
    db.commit()

    return {"status": "deleted", "floor_heating_id": floor_heating_id}
