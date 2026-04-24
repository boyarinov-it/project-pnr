from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.services.ets_mechanisms_writer import build_mechanisms_ets_csv

router = APIRouter(tags=["mechanisms-ets-csv-v1"])


@router.get("/projects/{project_id}/mechanisms-ets-csv-v1-preview")
def get_project_mechanisms_ets_csv_v1_preview(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    content = build_mechanisms_ets_csv(project)

    return {
        "project_id": project.id,
        "filename": f"project_{project.id}_mechanisms_ets_v1.csv",
        "content": content,
    }
