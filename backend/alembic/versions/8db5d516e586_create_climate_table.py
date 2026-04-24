"""create climate table"""

from alembic import op
import sqlalchemy as sa


revision = "8db5d516e586"
down_revision = "81f105563a90"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "climate",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("climate_type", sa.String(length=100), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("device_type", sa.String(length=100), nullable=True),
        sa.Column("device_address", sa.String(length=100), nullable=True),
        sa.Column("device_channel", sa.String(length=100), nullable=True),
        sa.Column("gateway_address", sa.String(length=100), nullable=True),
        sa.Column("external_id", sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("climate")
