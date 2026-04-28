from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)

    room_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    equipment_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    individual_address: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
