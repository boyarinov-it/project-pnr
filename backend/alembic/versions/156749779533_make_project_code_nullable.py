"""make project code nullable"""

from alembic import op


revision = "156749779533"
down_revision = "0416501fdcc8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE projects ALTER COLUMN code DROP NOT NULL")


def downgrade() -> None:
    op.execute("UPDATE projects SET code = name WHERE code IS NULL")
    op.execute("ALTER TABLE projects ALTER COLUMN code SET NOT NULL")
