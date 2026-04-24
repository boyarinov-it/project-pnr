"""create fans table"""

from alembic import op
import sqlalchemy as sa


revision = "0416501fdcc8"
down_revision = "8db5d516e586"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "fans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("device_type", sa.String(length=100), nullable=True),
        sa.Column("device_address", sa.String(length=100), nullable=True),
        sa.Column("device_channel", sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("fans")
