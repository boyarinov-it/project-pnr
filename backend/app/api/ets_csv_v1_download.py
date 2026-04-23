from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.services.ets_lighting_writer import build_lighting_ets_csv

router = APIRouter(tags=["ets-csv-v1-download"])


@router.get("/projects/{project_id}/ets-lighting-csv-v1-download")
def download_project_ets_lighting_csv_v1(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    content = build_lighting_ets_csv(project)

    temp_dir = Path("storage") / "temp_exports"
    temp_dir.mkdir(parents=True, exist_ok=True)

    file_path = temp_dir / f"project_{project.id}_lighting_ets_v1.csv"
    file_path.write_bytes(content.encode("cp1251", errors="replace"))

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/octet-stream",
    )
