from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (
        UniqueConstraint("project_id", "room_number", name="uq_rooms_project_room_number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    room_number: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)

    name_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    project = relationship("Project", back_populates="rooms")
    lighting_groups = relationship("LightingGroup", back_populates="room", cascade="all, delete-orphan")
