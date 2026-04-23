from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.services.ets_lighting_writer import build_lighting_ets_csv

router = APIRouter(tags=["ets-csv-v1"])


@router.get("/projects/{project_id}/ets-lighting-csv-v1-preview")
def get_project_ets_lighting_csv_v1_preview(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    content = build_lighting_ets_csv(project)

    return {
        "project_id": project.id,
        "filename": f"project_{project.id}_lighting_ets_v1.csv",
        "content": content,
    }
