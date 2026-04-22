from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.lighting_group import LightingGroup
from app.schemas.knx_preview import LightingGroupKnxPreview
from app.services.knx_generator import build_lighting_group_knx_preview

router = APIRouter(tags=["knx-preview"])


@router.get("/lighting-groups/{lighting_group_id}/knx-preview", response_model=LightingGroupKnxPreview)
def get_lighting_group_knx_preview(lighting_group_id: int, db: Session = Depends(get_db)):
    group = db.query(LightingGroup).filter(LightingGroup.id == lighting_group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Lighting group not found")
    return build_lighting_group_knx_preview(group)
