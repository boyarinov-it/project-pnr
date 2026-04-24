from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    rooms = relationship("Room", back_populates="project", cascade="all, delete-orphan")
    lighting_groups = relationship("LightingGroup", back_populates="project", cascade="all, delete-orphan")
    mechanisms = relationship("Mechanism", back_populates="project", cascade="all, delete-orphan")
    floor_heating = relationship("FloorHeating", back_populates="project", cascade="all, delete-orphan")

    # Legacy/internal relationships.
    # Нужны, потому что старые модели export_jobs/export_files еще подключены в backend.
    export_jobs = relationship("ExportJob", back_populates="project", cascade="all, delete-orphan")
