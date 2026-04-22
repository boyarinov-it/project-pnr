from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.services.project_csv_generator import build_project_lighting_csv_preview

router = APIRouter(tags=["project-csv-download"])


@router.get("/projects/{project_id}/lighting-csv-download")
def download_project_lighting_csv(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    preview = build_project_lighting_csv_preview(project)

    return Response(
        content=preview.content,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{preview.filename}"'
        },
    )
