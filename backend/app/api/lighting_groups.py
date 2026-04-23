from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.lighting_group import LightingGroup
from app.models.project import Project
from app.schemas.lighting_group import LightingGroupCreate, LightingGroupRead

router = APIRouter(tags=["lighting-groups"])


@router.post("/projects/{project_id}/lighting-groups", response_model=LightingGroupRead)
def create_lighting_group(project_id: int, payload: LightingGroupCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    group = LightingGroup(
        project_id=project_id,
        room_id=payload.room_id,
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
    return group


@router.get("/projects/{project_id}/lighting-groups", response_model=list[LightingGroupRead])
def list_lighting_groups(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return (
        db.query(LightingGroup)
        .filter(LightingGroup.project_id == project_id)
        .order_by(LightingGroup.id.asc())
        .all()
    )
