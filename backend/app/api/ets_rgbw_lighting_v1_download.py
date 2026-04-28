from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.services.ets_rgbw_lighting_csv import build_rgbw_lighting_ets_csv


router = APIRouter(tags=["ets-csv-v1"])


@router.get("/projects/{project_id}/rgbw-lighting-ets-csv-v1-download")
def download_project_rgbw_lighting_ets_csv_v1(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        content = build_rgbw_lighting_ets_csv(db=db, project_id=project_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    filename = f"project_{project_id}_rgbw_lighting_ets_v1.csv"
    file_bytes = content.encode("cp1251", errors="replace")

    return Response(
        content=file_bytes,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Content-Type-Options": "nosniff",
        },
    )
