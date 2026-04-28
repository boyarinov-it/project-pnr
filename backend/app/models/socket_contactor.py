from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class SocketContactor(Base):
    __tablename__ = "sockets_contactors"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)

    room_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    load_type: Mapped[str] = mapped_column(String(100), nullable=False, default="SOCKET")

    device_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    device_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    device_output: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
