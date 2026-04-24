from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.services.ets_fans_writer import build_fans_ets_csv
from app.services.fan_validator import validate_fans_for_export

router = APIRouter(tags=["fans-ets-csv-v1"])


@router.get("/projects/{project_id}/fans-ets-csv-v1-preview")
def get_project_fans_ets_csv_v1_preview(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    content = build_fans_ets_csv(project)

    return {
        "project_id": project.id,
        "filename": f"project_{project.id}_fans_ets_v1.csv",
        "content": content,
    }


@router.get("/projects/{project_id}/fans-ets-csv-v1-download")
def download_project_fans_ets_csv_v1(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    issues = validate_fans_for_export(project)
    critical_errors = [x for x in issues if x.level == "error"]
    if critical_errors:
        return {
            "project_id": project.id,
            "is_valid": False,
            "issues": [
                {
                    "level": x.level,
                    "code": x.code,
                    "message": x.message,
                    "entity_id": x.entity_id,
                }
                for x in critical_errors
            ],
        }

    content = build_fans_ets_csv(project)
    filename = f"project_{project.id}_fans_ets_v1.csv"

    file_bytes = content.encode("cp1251", errors="replace")

    return Response(
        content=file_bytes,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Content-Type-Options": "nosniff",
        },
    )
