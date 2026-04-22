from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.schemas.project_csv_preview import ProjectCsvPreview
from app.services.project_csv_generator import build_project_lighting_csv_preview

router = APIRouter(tags=["project-csv-preview"])


@router.get("/projects/{project_id}/lighting-csv-preview", response_model=ProjectCsvPreview)
def get_project_lighting_csv_preview(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return build_project_lighting_csv_preview(project)
