from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.services.ets_central_functions_writer import build_central_functions_ets_csv

router = APIRouter(tags=["central-functions-ets-csv-v1"])


def get_project_or_404(project_id: int, db: Session) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/projects/{project_id}/central-functions-ets-csv-v1-preview")
def get_central_functions_ets_csv_v1_preview(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = get_project_or_404(project_id, db)
    content = build_central_functions_ets_csv()

    return {
        "project_id": project.id,
        "filename": f"project_{project.id}_central_functions_ets_v1.csv",
        "content": content,
    }


@router.get("/projects/{project_id}/central-functions-ets-csv-v1-download")
def download_central_functions_ets_csv_v1(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = get_project_or_404(project_id, db)
    content = build_central_functions_ets_csv()
    filename = f"project_{project.id}_central_functions_ets_v1.csv"

    file_bytes = content.encode("cp1251", errors="replace")

    return Response(
        content=file_bytes,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Content-Type-Options": "nosniff",
        },
    )
