"""add column to post table

Revision ID: 0f538cc826c7
Revises: f3ce9c714ff9
Create Date: 2026-11-16 16:58:52.423916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f538cc826c7'
down_revision: Union[str, Sequence[str], None] = 'f3ce9c714ff9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass