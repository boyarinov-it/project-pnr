"""create sockets contactors table

Revision ID: dd8169a22250
Revises: d4ab2a0b8557
Create Date: auto
"""

from alembic import op


revision = "dd8169a22250"
down_revision = "d4ab2a0b8557"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS sockets_contactors (
            id SERIAL PRIMARY KEY,
            project_id INTEGER NOT NULL REFERENCES projects(id),
            room_number VARCHAR(50),
            code VARCHAR(50) NOT NULL,
            name VARCHAR(255) NOT NULL,
            load_type VARCHAR(100) NOT NULL DEFAULT 'SOCKET',
            device_type VARCHAR(100),
            device_address VARCHAR(50),
            device_output VARCHAR(50),
            description TEXT
        )
    """)

    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_sockets_contactors_project_id
        ON sockets_contactors (project_id)
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_sockets_contactors_project_id")
    op.execute("DROP TABLE IF EXISTS sockets_contactors")
