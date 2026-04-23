from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class LightingGroup(Base):
    __tablename__ = "lighting_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    load_type: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    device_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    device_address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    device_output: Mapped[str | None] = mapped_column(String(100), nullable=True)
    dimmer_channel: Mapped[str | None] = mapped_column(String(100), nullable=True)

    project = relationship("Project", back_populates="lighting_groups")
    room = relationship("Room", back_populates="lighting_groups")
