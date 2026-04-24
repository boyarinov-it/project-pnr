from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Mechanism(Base):
    __tablename__ = "mechanisms"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    mechanism_type: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    device_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    device_address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    device_channel: Mapped[str | None] = mapped_column(String(100), nullable=True)

    room = relationship("Room")
    project = relationship("Project")
