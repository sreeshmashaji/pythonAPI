"""add content to post table

Revision ID: f0dc02fefe70
Revises: f286746bd0b2
Create Date: 2024-02-19 08:58:40.011329

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0dc02fefe70'
down_revision: Union[str, None] = 'f286746bd0b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
