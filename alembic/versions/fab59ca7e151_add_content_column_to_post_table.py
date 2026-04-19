"""add content column to post table

Revision ID: fab59ca7e151
Revises: a40f2a5ccfb3
Create Date: 2026-04-19 12:49:36.590548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fab59ca7e151'
down_revision: Union[str, Sequence[str], None] = 'a40f2a5ccfb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
