from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.lighting_group import LightingGroup
from app.models.room import Room
from app.schemas.lighting_group import LightingGroupCreate, LightingGroupRead, LightingGroupUpdate
from app.services.explication_resolver import get_project_or_404, get_room_by_number_or_404

router = APIRouter(tags=["lighting-groups"])


def build_room_name(room: Room) -> str:
    return room.name_ru or room.name or room.code


def build_lighting_display_name(room: Room, group: LightingGroup) -> str:
    return f"{build_room_name(room)} - {group.name}"


def build_lighting_group_read(group: LightingGroup) -> LightingGroupRead:
    room = group.room

    return LightingGroupRead(
        id=group.id,
        project_id=group.project_id,
        room_id=group.room_id,
        room_number=room.room_number,
        room_name=build_room_name(room),
        display_name=build_lighting_display_name(room, group),
        name=group.name,
        code=group.code,
        load_type=group.load_type,
        quantity=group.quantity,
        device_type=group.device_type,
        device_address=group.device_address,
        device_output=group.device_output,
        dimmer_channel=group.dimmer_channel,
    )


@router.post("/projects/{project_id}/lighting-groups", response_model=LightingGroupRead)
def create_lighting_group(project_id: int, payload: LightingGroupCreate, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)
    room = get_room_by_number_or_404(db, project_id, payload.room_number)

    group = LightingGroup(
        project_id=project_id,
        room_id=room.id,
        name=payload.name,
        code=payload.code,
        load_type=payload.load_type,
        quantity=payload.quantity,
        device_type=payload.device_type,
        device_address=payload.device_address,
        device_output=payload.device_output,
        dimmer_channel=payload.dimmer_channel,
    )
    db.add(group)
    db.commit()
    db.refresh(group)

    return build_lighting_group_read(group)


@router.put("/lighting-groups/{lighting_group_id}", response_model=LightingGroupRead)
def update_lighting_group(
    lighting_group_id: int,
    payload: LightingGroupUpdate,
    db: Session = Depends(get_db),
):
    group = db.query(LightingGroup).filter(LightingGroup.id == lighting_group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Lighting group not found")

    room = get_room_by_number_or_404(db, group.project_id, payload.room_number)

    group.room_id = room.id
    group.name = payload.name
    group.code = payload.code
    group.load_type = payload.load_type
    group.quantity = payload.quantity
    group.device_type = payload.device_type
    group.device_address = payload.device_address
    group.device_output = payload.device_output
    group.dimmer_channel = payload.dimmer_channel

    db.commit()
    db.refresh(group)

    return build_lighting_group_read(group)


@router.delete("/lighting-groups/{lighting_group_id}")
def delete_lighting_group(lighting_group_id: int, db: Session = Depends(get_db)):
    group = db.query(LightingGroup).filter(LightingGroup.id == lighting_group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Lighting group not found")

    db.delete(group)
    db.commit()

    return {"status": "deleted", "lighting_group_id": lighting_group_id}


@router.get("/projects/{project_id}/lighting-groups", response_model=list[LightingGroupRead])
def list_lighting_groups(project_id: int, db: Session = Depends(get_db)):
    get_project_or_404(db, project_id)

    groups = (
        db.query(LightingGroup)
        .join(Room, LightingGroup.room_id == Room.id)
        .filter(LightingGroup.project_id == project_id)
        .order_by(LightingGroup.id.asc())
        .all()
    )

    return [build_lighting_group_read(group) for group in groups]
