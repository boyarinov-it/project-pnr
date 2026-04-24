from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.climate import Climate
from app.models.room import Room
from app.schemas.climate import ClimateCreate, ClimateRead, ClimateUpdate
from app.services.explication_resolver import get_project_or_404, get_room_by_number_or_404

router = APIRouter(tags=["climate"])


def build_room_name(room: Room) -> str:
    return room.name_ru or room.name or room.code


def build_climate_display_name(room: Room, climate: Climate) -> str:
    return f"{build_room_name(room)} - {climate.name}"


def build_climate_read(climate: Climate) -> ClimateRead:
    room = climate.room

    return ClimateRead(
        id=climate.id,
        project_id=climate.project_id,
        room_id=climate.room_id,
        room_number=room.room_number,
        room_name=build_room_name(room),
        display_name=build_climate_display_name(room, climate),
        name=climate.name,
        code=climate.code,
        climate_type=climate.climate_type,
        quantity=climate.quantity,
        device_type=climate.device_type,
        device_address=climate.device_address,
        device_channel=climate.device_channel,
        gateway_address=climate.gateway_address,
        external_id=climate.external_id,
    )


@router.post("/projects/{project_id}/climate", response_model=ClimateRead)
def create_climate(project_id: int, payload: ClimateCreate, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)
    room = get_room_by_number_or_404(db, project_id, payload.room_number)

    climate = Climate(
        project_id=project_id,
        room_id=room.id,
        name=payload.name,
        code=payload.code,
        climate_type=payload.climate_type,
        quantity=payload.quantity,
        device_type=payload.device_type,
        device_address=payload.device_address,
        device_channel=payload.device_channel,
        gateway_address=payload.gateway_address,
        external_id=payload.external_id,
    )

    db.add(climate)
    db.commit()
    db.refresh(climate)

    return build_climate_read(climate)


@router.get("/projects/{project_id}/climate", response_model=list[ClimateRead])
def list_climate(project_id: int, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)

    climate_items = (
        db.query(Climate)
        .join(Room, Climate.room_id == Room.id)
        .filter(Climate.project_id == project_id)
        .order_by(Climate.id.asc())
        .all()
    )

    return [build_climate_read(item) for item in climate_items]


@router.put("/climate/{climate_id}", response_model=ClimateRead)
def update_climate(
    climate_id: int,
    payload: ClimateUpdate,
    db: Session = Depends(get_db),
):
    climate = db.query(Climate).filter(Climate.id == climate_id).first()
    if not climate:
        raise HTTPException(status_code=404, detail="Climate item not found")

    room = get_room_by_number_or_404(db, climate.project_id, payload.room_number)

    climate.room_id = room.id
    climate.name = payload.name
    climate.code = payload.code
    climate.climate_type = payload.climate_type
    climate.quantity = payload.quantity
    climate.device_type = payload.device_type
    climate.device_address = payload.device_address
    climate.device_channel = payload.device_channel
    climate.gateway_address = payload.gateway_address
    climate.external_id = payload.external_id

    db.commit()
    db.refresh(climate)

    return build_climate_read(climate)


@router.delete("/climate/{climate_id}")
def delete_climate(climate_id: int, db: Session = Depends(get_db)):
    climate = db.query(Climate).filter(Climate.id == climate_id).first()
    if not climate:
        raise HTTPException(status_code=404, detail="Climate item not found")

    db.delete(climate)
    db.commit()

    return {"status": "deleted", "climate_id": climate_id}
