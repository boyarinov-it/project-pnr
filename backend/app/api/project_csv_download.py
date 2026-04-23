from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.services.encoding_adapter import encode_export_content
from app.services.export_file_service import save_export_file
from app.services.export_job_service import create_project_lighting_export_job
from app.services.project_csv_generator import build_project_lighting_csv_preview
from app.services.validation_engine import validate_project_export

router = APIRouter(tags=["project-csv-download"])


@router.get("/projects/{project_id}/lighting-csv-download")
def download_project_lighting_csv(
    project_id: int,
    encoding: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    validation_result = validate_project_export(project)
    error_issues = [issue.model_dump() for issue in validation_result.issues if issue.level == "error"]

    if error_issues:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Export validation failed",
                "issues": error_issues,
            },
        )

    preview = build_project_lighting_csv_preview(project)
    export_job = create_project_lighting_export_job(db, project)
    save_export_file(db, export_job, preview.content)

    export_bytes = encode_export_content(preview.content, encoding)

    return Response(
        content=export_bytes,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{preview.filename}"'
        },
    )
