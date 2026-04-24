from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.services.climate_validator import validate_climate_for_export

router = APIRouter(tags=["climate"])


@router.get("/projects/{project_id}/climate-validation")
def get_climate_validation(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    issues = validate_climate_for_export(project)

    return {
        "project_id": project.id,
        "is_valid": len([x for x in issues if x.level == "error"]) == 0,
        "issues": [
            {
                "level": x.level,
                "code": x.code,
                "message": x.message,
                "entity_id": x.entity_id,
            }
            for x in issues
        ],
    }
