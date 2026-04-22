from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ExportFile(Base):
    __tablename__ = "export_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    export_job_id: Mapped[int] = mapped_column(ForeignKey("export_jobs.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    checksum: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    export_job = relationship("ExportJob", back_populates="export_files")
