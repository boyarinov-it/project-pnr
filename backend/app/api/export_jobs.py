from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.export_job import ExportJob
from app.models.project import Project
from app.schemas.export_job import ExportJobRead

router = APIRouter(tags=["export-jobs"])


@router.get("/projects/{project_id}/exports", response_model=list[ExportJobRead])
def list_project_exports(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return (
        db.query(ExportJob)
        .filter(ExportJob.project_id == project_id)
        .order_by(ExportJob.id.desc())
        .all()
    )
