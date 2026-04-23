from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
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


@router.get("/export-files/{export_file_id}/download")
def download_export_file(export_file_id: int, db: Session = Depends(get_db)):
    export_file = db.query(ExportFile).filter(ExportFile.id == export_file_id).first()
    if not export_file:
        raise HTTPException(status_code=404, detail="Export file not found")

    file_path = Path(export_file.storage_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Stored file not found on disk")

    return FileResponse(
        path=str(file_path),
        filename=export_file.filename,
        media_type="text/csv; charset=utf-8",
    )
