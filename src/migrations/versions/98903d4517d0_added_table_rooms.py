"""added table rooms

Revision ID: 98903d4517d0
Revises: a58727c04f26
Create Date: 2026-04-18 14:57:28.114784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '98903d4517d0'
down_revision: Union[str, Sequence[str], None] = 'a58727c04f26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hotel_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
        sa.PrimaryKeyConstraint('id')
        )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('rooms')

