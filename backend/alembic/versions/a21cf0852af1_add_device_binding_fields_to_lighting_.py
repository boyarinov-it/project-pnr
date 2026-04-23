"""add device binding fields to lighting groups"""

from alembic import op
import sqlalchemy as sa


revision = "a21cf0852af1"
down_revision = "16cd138a46be"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("lighting_groups", sa.Column("device_type", sa.String(length=100), nullable=True))
    op.add_column("lighting_groups", sa.Column("device_address", sa.String(length=100), nullable=True))
    op.add_column("lighting_groups", sa.Column("device_output", sa.String(length=100), nullable=True))
    op.add_column("lighting_groups", sa.Column("dimmer_channel", sa.String(length=100), nullable=True))


def downgrade() -> None:
    op.drop_column("lighting_groups", "dimmer_channel")
    op.drop_column("lighting_groups", "device_output")
    op.drop_column("lighting_groups", "device_address")
    op.drop_column("lighting_groups", "device_type")
