from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.mechanism import Mechanism
from app.models.room import Room
from app.schemas.mechanism import MechanismCreate, MechanismRead, MechanismUpdate
from app.services.explication_resolver import get_project_or_404, get_room_by_number_or_404

router = APIRouter(tags=["mechanisms"])


def build_room_name(room: Room) -> str:
    return room.name_ru or room.name or room.code


def build_mechanism_display_name(room: Room, mechanism: Mechanism) -> str:
    return f"{build_room_name(room)} - {mechanism.name}"


def build_mechanism_read(mechanism: Mechanism) -> MechanismRead:
    room = mechanism.room

    return MechanismRead(
        id=mechanism.id,
        project_id=mechanism.project_id,
        room_id=mechanism.room_id,
        room_number=room.room_number,
        room_name=build_room_name(room),
        display_name=build_mechanism_display_name(room, mechanism),
        name=mechanism.name,
        code=mechanism.code,
        mechanism_type=mechanism.mechanism_type,
        quantity=mechanism.quantity,
        device_type=mechanism.device_type,
        device_address=mechanism.device_address,
        device_channel=mechanism.device_channel,
    )


@router.post("/projects/{project_id}/mechanisms", response_model=MechanismRead)
def create_mechanism(project_id: int, payload: MechanismCreate, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)
    room = get_room_by_number_or_404(db, project_id, payload.room_number)

    mechanism = Mechanism(
        project_id=project_id,
        room_id=room.id,
        name=payload.name,
        code=payload.code,
        mechanism_type=payload.mechanism_type,
        quantity=payload.quantity,
        device_type=payload.device_type,
        device_address=payload.device_address,
        device_channel=payload.device_channel,
    )

    db.add(mechanism)
    db.commit()
    db.refresh(mechanism)

    return build_mechanism_read(mechanism)


@router.get("/projects/{project_id}/mechanisms", response_model=list[MechanismRead])
def list_mechanisms(project_id: int, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)

    mechanisms = (
        db.query(Mechanism)
        .join(Room, Mechanism.room_id == Room.id)
        .filter(Mechanism.project_id == project_id)
        .order_by(Mechanism.id.asc())
        .all()
    )

    return [build_mechanism_read(mechanism) for mechanism in mechanisms]


@router.put("/mechanisms/{mechanism_id}", response_model=MechanismRead)
def update_mechanism(
    mechanism_id: int,
    payload: MechanismUpdate,
    db: Session = Depends(get_db),
):
    mechanism = db.query(Mechanism).filter(Mechanism.id == mechanism_id).first()
    if not mechanism:
        raise HTTPException(status_code=404, detail="Mechanism not found")

    room = get_room_by_number_or_404(db, mechanism.project_id, payload.room_number)

    mechanism.room_id = room.id
    mechanism.name = payload.name
    mechanism.code = payload.code
    mechanism.mechanism_type = payload.mechanism_type
    mechanism.quantity = payload.quantity
    mechanism.device_type = payload.device_type
    mechanism.device_address = payload.device_address
    mechanism.device_channel = payload.device_channel

    db.commit()
    db.refresh(mechanism)

    return build_mechanism_read(mechanism)


@router.delete("/mechanisms/{mechanism_id}")
def delete_mechanism(mechanism_id: int, db: Session = Depends(get_db)):
    mechanism = db.query(Mechanism).filter(Mechanism.id == mechanism_id).first()
    if not mechanism:
        raise HTTPException(status_code=404, detail="Mechanism not found")

    db.delete(mechanism)
    db.commit()

    return {"status": "deleted", "mechanism_id": mechanism_id}
