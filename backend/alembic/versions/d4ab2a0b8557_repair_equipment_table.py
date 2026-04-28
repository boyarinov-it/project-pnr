"""repair equipment table

Revision ID: d4ab2a0b8557
Revises: 1d1b653fbdbd
Create Date: auto
"""

from alembic import op


revision = "d4ab2a0b8557"
down_revision = "1d1b653fbdbd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id SERIAL PRIMARY KEY,
            project_id INTEGER NOT NULL REFERENCES projects(id),
            room_number VARCHAR(50),
            name VARCHAR(255) NOT NULL,
            equipment_type VARCHAR(100),
            individual_address VARCHAR(50) NOT NULL,
            description TEXT
        )
    """)

    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_equipment_project_id
        ON equipment (project_id)
    """)

    op.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS ux_equipment_project_individual_address
        ON equipment (project_id, individual_address)
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ux_equipment_project_individual_address")
    op.execute("DROP INDEX IF EXISTS ix_equipment_project_id")
    op.execute("DROP TABLE IF EXISTS equipment")
