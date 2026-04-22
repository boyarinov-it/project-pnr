from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.schemas.validation import ProjectValidationResult
from app.services.validation_engine import validate_project_export

router = APIRouter(tags=["validation"])


@router.get("/projects/{project_id}/validate-export", response_model=ProjectValidationResult)
def validate_project_export_endpoint(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return validate_project_export(project)
