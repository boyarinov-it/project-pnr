from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.models.room import Room
from app.models.lighting_group import LightingGroup
from app.schemas.lighting_group import LightingGroupCreate, LightingGroupRead

router = APIRouter(tags=["lighting-groups"])


@router.post("/projects/{project_id}/lighting-groups", response_model=LightingGroupRead)
def create_lighting_group(project_id: int, payload: LightingGroupCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    room = (
        db.query(Room)
        .filter(Room.project_id == project_id, Room.room_number == payload.room_number)
        .first()
    )
    if not room:
        raise HTTPException(status_code=404, detail="Room with given room_number not found")

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

    return LightingGroupRead(
        id=group.id,
        project_id=group.project_id,
        room_id=group.room_id,
        room_number=room.room_number,
        room_name=room.name_ru or room.name,
        name=group.name,
        code=group.code,
        load_type=group.load_type,
        quantity=group.quantity,
        device_type=group.device_type,
        device_address=group.device_address,
        device_output=group.device_output,
        dimmer_channel=group.dimmer_channel,
        display_name=f"{room.room_number}.{room.name_ru or room.name}-{group.name}",
    )


@router.get("/projects/{project_id}/lighting-groups", response_model=list[LightingGroupRead])
def list_lighting_groups(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    groups = (
        db.query(LightingGroup)
        .join(Room, LightingGroup.room_id == Room.id)
        .filter(LightingGroup.project_id == project_id)
        .order_by(LightingGroup.id.asc())
        .all()
    )

    result = []
    for group in groups:
        room = group.room
        result.append(
            LightingGroupRead(
                id=group.id,
                project_id=group.project_id,
                room_id=group.room_id,
                room_number=room.room_number,
                room_name=room.name_ru or room.name,
                name=group.name,
                code=group.code,
                load_type=group.load_type,
                quantity=group.quantity,
                device_type=group.device_type,
                device_address=group.device_address,
                device_output=group.device_output,
                dimmer_channel=group.dimmer_channel,
                display_name=f"{room.room_number}.{room.name_ru or room.name}-{group.name}",
            )
        )

    return result
