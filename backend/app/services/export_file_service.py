from pathlib import Path

from sqlalchemy.orm import Session

from app.models.export_file import ExportFile
from app.models.export_job import ExportJob


BASE_DIR = Path(__file__).resolve().parents[2]
EXPORT_STORAGE_DIR = BASE_DIR / "storage" / "exports"


def save_export_file(db: Session, export_job: ExportJob, content: str) -> ExportFile:
    EXPORT_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    file_path = EXPORT_STORAGE_DIR / f"job_{export_job.id}_{export_job.filename}"
    file_path.write_text(content, encoding="utf-8-sig")

    export_file = ExportFile(
        export_job_id=export_job.id,
        filename=export_job.filename,
        storage_path=str(file_path),
        checksum=export_job.checksum,
    )

    db.add(export_file)
    db.commit()
    db.refresh(export_file)
    return export_file
