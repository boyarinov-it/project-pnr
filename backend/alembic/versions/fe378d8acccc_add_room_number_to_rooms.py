"""add room number to rooms"""

from alembic import op
import sqlalchemy as sa


revision = "fe378d8acccc"
down_revision = "28b34fae9ed2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("rooms", sa.Column("room_number", sa.String(length=50), nullable=True))

    op.execute("""
        UPDATE rooms
        SET room_number = 'TMP-' || id::text
        WHERE room_number IS NULL
    """)

    op.alter_column("rooms", "room_number", nullable=False)
    op.create_unique_constraint("uq_rooms_project_room_number", "rooms", ["project_id", "room_number"])


def downgrade() -> None:
    op.drop_constraint("uq_rooms_project_room_number", "rooms", type_="unique")
    op.drop_column("rooms", "room_number")
