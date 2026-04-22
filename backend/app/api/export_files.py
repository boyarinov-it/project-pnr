from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.export_file import ExportFile
from app.models.export_job import ExportJob
from app.models.project import Project
from app.schemas.export_file import ExportFileRead

router = APIRouter(tags=["export-files"])


@router.get("/projects/{project_id}/export-files", response_model=list[ExportFileRead])
def list_project_export_files(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return (
        db.query(ExportFile)
        .join(ExportJob, ExportFile.export_job_id == ExportJob.id)
        .filter(ExportJob.project_id == project_id)
        .order_by(ExportFile.id.desc())
        .all()
    )
