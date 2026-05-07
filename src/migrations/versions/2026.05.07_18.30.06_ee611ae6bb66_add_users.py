"""add users

Revision ID: ee611ae6bb66
Revises: ad8cca1aeeda
Create Date: 2026-05-07 18:30:06.402509

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "ee611ae6bb66"
down_revision: Union[str, Sequence[str], None] = "ad8cca1aeeda"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
