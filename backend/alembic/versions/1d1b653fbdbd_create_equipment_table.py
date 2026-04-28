"""create equipment table

Revision ID: 1d1b653fbdbd
Revises: 156749779533
Create Date: auto
"""

from alembic import op
import sqlalchemy as sa


revision = "1d1b653fbdbd"
down_revision = "156749779533"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "equipment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("room_number", sa.String(length=50), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("equipment_type", sa.String(length=100), nullable=True),
        sa.Column("individual_address", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_equipment_project_id",
        "equipment",
        ["project_id"],
        unique=False,
    )

    op.create_index(
        "ux_equipment_project_individual_address",
        "equipment",
        ["project_id", "individual_address"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ux_equipment_project_individual_address", table_name="equipment")
    op.drop_index("ix_equipment_project_id", table_name="equipment")
    op.drop_table("equipment")
