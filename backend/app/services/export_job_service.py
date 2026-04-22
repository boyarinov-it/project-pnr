import hashlib
import json

from sqlalchemy.orm import Session

from app.models.export_job import ExportJob
from app.models.project import Project
from app.services.project_csv_generator import build_project_lighting_csv_preview
from app.services.validation_engine import validate_project_export


def create_project_lighting_export_job(db: Session, project: Project) -> ExportJob:
    preview = build_project_lighting_csv_preview(project)
    validation = validate_project_export(project)

    checksum = hashlib.sha256(preview.content.encode("utf-8")).hexdigest()

    job = ExportJob(
        project_id=project.id,
        export_type="lighting_csv",
        status="completed" if validation.is_valid else "failed",
        filename=preview.filename,
        checksum=checksum,
        validation_snapshot=json.dumps([issue.model_dump() for issue in validation.issues], ensure_ascii=False),
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    return job
