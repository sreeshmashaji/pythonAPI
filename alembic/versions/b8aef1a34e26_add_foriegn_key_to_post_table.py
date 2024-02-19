"""add foriegn key to post table

Revision ID: b8aef1a34e26
Revises: c33cdea78082
Create Date: 2024-02-19 09:37:21.054813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8aef1a34e26'
down_revision: Union[str, None] = 'c33cdea78082'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('user_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users',local_cols=['user_id'],
                          remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','user_id')
    pass
